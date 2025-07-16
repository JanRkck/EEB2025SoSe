#!/usr/bin/env python3

import os, time, pygame, RPi.GPIO as GPIO
from mfrc522       import SimpleMFRC522
from RPLCD.gpio    import CharLCD
from story         import SCENES, WRONG_WAV         


AUDIO_DIR      = "/home/pi/story"
ACTIVATION_UID = 345904649546          # UID der startfigur, hardcoded für prototyp

#LCD Screen init
lcd = CharLCD(cols=16, rows=2,
              pin_rs=26, pin_e=19,
              pins_data=[13, 6, 5, 21],
              numbering_mode=GPIO.BCM)
#RFID-Kit init
reader = SimpleMFRC522()
#pygame für einfaches abspielen der mp3 Dateien             
pygame.mixer.init()

#Hilfs­funktionen
def lcd2(l1: str = "", l2: str = "") -> None:
    lcd.clear()
    lcd.write_string(l1[:16].ljust(16))
    lcd.cursor_pos = (1, 0)
    lcd.write_string(l2[:16].ljust(16))

def play(wav: str, animate=True) -> None:
    snd = pygame.mixer.Sound(os.path.join(AUDIO_DIR, wav))
    snd.play()

    if not animate:                      # nur warten
        while pygame.mixer.get_busy():
            time.sleep(0.05)
        return

    lcd.clear()                          # Narration -> Animation
    while pygame.mixer.get_busy():
        animate_wave()
        time.sleep(0.25)


def animate_wave():
    pattern = "~   " * 12                    
    phase   = animate_wave.phase = (animate_wave.phase - 1) % 48

    # 16-zeichen fenster herausschneiden, wenn am ende -> wrap
    def window(offset):
        idx = (phase + offset) % 48
        return (pattern + pattern)[idx: idx + 16]

    lcd.cursor_pos = (0, 0); lcd.write_string(window(0))   # zeile 1
    lcd.cursor_pos = (1, 0); lcd.write_string(window(2))   # zeile 2
animate_wave.phase = -1

        
def read_digit_or_uid():
    """Liefert (uid, digit_or_None)."""
    uid, raw = reader.read()
    txt = raw.strip()[:1]
    digit = int(txt) if txt.isdigit() else None
    return uid, digit


def wait_for_start_tag():
    lcd2("Lege Figur auf", "das Lesepad")
    while True:
        uid, _ = reader.read()
        if uid == ACTIVATION_UID:
            return

def game_loop():
    for scene in SCENES:
        #erzählung
        play(scene["audio"], animate = True)

        if "answer" not in scene:        # keine frage in szene
            continue

        #frage
        l1, l2 = scene["lcd"]            # zwei kurze LCD-Zeilen
        while True:
            lcd2(l1, l2)
            uid, digit = read_digit_or_uid()

            # Reset jederzeit möglich
            if uid == ACTIVATION_UID:
                lcd2("Neu­start ...", "")
                time.sleep(1.5)
                return                   # zurück zum Idle-Screen

            if digit == scene["answer"]:
                lcd2("Richtig!", "")
                right_wav = scene.get("right")
                if right_wav:            
                    play(right_wav, animate=False)
                time.sleep(1.5)
                break
            else:
                lcd2("Falsch! Versuche", "es erneut!")
                play(WRONG_WAV, animate=False)
                time.sleep(1.2)

    #ende
    lcd2("Du hast es", "geschafft!")
    time.sleep(4)

#Main App
try:
    while True:
        wait_for_start_tag()   # Idle-Phase
        game_loop()            # Spielrunde

except KeyboardInterrupt:
    pass
finally:
    lcd.clear()
    GPIO.cleanup()
