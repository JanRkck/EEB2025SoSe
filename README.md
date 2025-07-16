# EEB2025SoSe

# Story-Math Cubes  
An interactive, RFID-based learning game for early primary pupils  
==================================================================

**Main idea.**  
Two physical cubes cooperate to tell a spoken adventure in German and to pose
short arithmetic challenges.  
* The **Main Console** (Cube 1) plays the audio story, shows prompts on a
  16 × 2 LCD and validates answers.  
* The **Number Cube** (Cube 2) lets the child select a digit 0-9 on a small
  OLED; the chosen digit is written into an RFID tag that remains on its reader.
  The Main Console reads the same tag and decides whether the answer is correct.

Both cubes are powered by Raspberry Pi Zero 2 W boards and communicate only
through the shared RFID tag—no network link is required.

---

## 1  Hardware

| Part | Qty | Cube | Notes |
|------|----:|------|-------|
| Raspberry Pi Zero 2 W | 2 | both | 5 V @ 1 A |
| MFRC522 RFID reader/writer | 2 | both | SPI-0 CE0 |
| HD44780 16 × 2 LCD | 1 | Main | 4-bit mode |
| SH1106 (or SSD1306) 0.96″ OLED | 1 | Number | I²C |
| Momentary push buttons | 2 | Number | GPIO 17 / 27 |
| Bluetooth loud-speaker | 1 | Main | A2DP sink |
| Misc. resistors | — | Main | contrast divider 2 k4 / 1 k |


## 2  Repository structure  

story-cube/
├─ story_cube.py # main-console application
├─ number_cube.py # number-cube firmware
├─ story.py # scene metadata (audio, LCD text, answers)
├─ story/ # audio clips 00_title.wav … wrong.wav
└─ README.md # this file


## 3  Software installation  

```bash
sudo apt update && sudo apt upgrade -y
sudo raspi-config nonint do_spi 0      # enable SPI for MFRC522
sudo raspi-config nonint do_i2c 0      # enable I²C for OLED
sudo apt install python3-pip python3-pygame \
                 bluez pulseaudio pulseaudio-module-bluetooth \
                 python3-rplcd python3-gpiozero python3-rpi.gpio \
                 python3-luma.oled python3-pillow -y
pip3 install mfrc522

#connect to bluetooth speaker
pulseaudio --start
bluetoothctl  # pair, trust, connect
pactl set-default-sink $(pactl list short sinks | grep a2dp | awk '{print $2}')
```

## 4  Wiring / assembly guide  

### 4.1  Main Console (Cube 1)

| Signal | Pi GPIO pin | LCD pin | MFRC522 pin | Notes |
|--------|-------------|---------|-------------|-------|
| 5 V    | 2 or 4      | VDD     | VCC         | LCD back-light also on 5 V via 220 Ω |
| 3 V3   | 1           | —       | —           | MFRC522 uses on-board 3 V regulator |
| GND    | 6, 9, 14…   | GND     | GND         | Common ground |
| RS     | 26          | RS      | —           | |
| E      | 19          | E       | —           | |
| D4–D7  | 13 / 6 / 5 / 21 | D4–D7 | — | |
| MOSI   | 10          | —       | MOSI        | SPI 0 |
| MISO   | 9           | —       | MISO        | SPI 0 |
| SCK    | 11          | —       | SCK         | SPI 0 |
| CE0    | 8           | —       | SDA (SS)    | Chip-select |
| RST    | 25          | —       | RST         | Reset line |

Contrast network: **2 .4 kΩ (5 V → V0)**  
gives ≈ 1 .5 V on V0 → clear background, dark glyphs.

### 4.2  Number Cube (Cube 2)

| Signal | Pi GPIO pin | OLED | MFRC522 | Button |
|--------|-------------|------|---------|--------|
| 3 V3   | 1           | VCC  | —       | — |
| 5 V    | 2           | —    | VCC     | — |
| GND    | 6           | GND  | GND     | One leg of both switches |
| SDA    | 2           | SDA  | —       | — |
| SCL    | 3           | SCL  | —       | — |
| MOSI   | 10          | —    | MOSI    | — |
| MISO   | 9           | —    | MISO    | — |
| SCK    | 11          | —    | SCK     | — |
| CE0    | 8           | —    | SDA (SS)| — |
| RST    | 25          | —    | RST     | — |
| Button ▲ | 17        | —    | —       | other leg to GND |
| Button ▼ | 27        | —    | —       | other leg to GND |

---

## 5  Running the prototype

### 5.1  Manual start (development)

```bash
# Main Console
ssh pi@maincube.local
cd /home/pi//story_cube
python3 story_cube.py

# Number Cube
ssh pi@numbercube.local
cd /home/pi
python3 number_cube.py
```

## 6  Libraries used

| Package | Version tested | Purpose |
|---------|---------------|---------|
| `mfrc522` | 1.4.1 | SPI driver for the MFRC522 reader-writer (read / write) |
| `RPLCD` | 2.0.4 | Control of the HD44780 16 × 2 LCD in 4-bit mode |
| `luma.oled` | 3.13.0 | High-level graphics API for the SH1106 OLED |
| `Pillow` | 10.3.0 | Font rasterisation backend used by *luma.oled* |
| `gpiozero` | 2.0 | Simplified button handling and pull-up configuration |
| `RPi.GPIO` | 0.7.1 | Low-level pin access required by **RPLCD** |
| `pygame` (mixer) | 2.6.1 | Playback of WAV / MP3 files through PulseAudio |
| `bluez` | 5.66 | Bluetooth stack (pairing, A2DP profile support) |
| `pulseaudio` | 16.1 | User-space audio server |
| `pulseaudio-module-bluetooth` | 16.1 | Bridges PulseAudio to BlueZ (creates `a2dp_sink`) |
| `pulseaudio-utils` | 16.1 | CLI tools (`pactl`, `pacmd`) for sink selection |
