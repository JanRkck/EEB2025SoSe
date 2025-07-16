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

**Contrast network (LCD)**  
