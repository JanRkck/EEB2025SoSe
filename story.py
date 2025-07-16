# story.py
SCENES = [
    {"audio": "titel.mp3"},
    {"audio": "prolog.mp3"},

    # Checkpoint 1
    {"audio": "checkpoint1.mp3",
     "lcd":  ("5 Segel +",      # line-1 
              "3 Hute = ?"),    # line-2
     "answer": 8,               #richtige antwort
     "right":  "richtig1.mp3"}, #audio

    {"audio": "storyweiter.mp3"},

    # Checkpoint 2
    {"audio": "checkpoint2.mp3",
     "lcd":  ("10 Munzen - ",   # line-1
              "4 Munzen = ?"),  # line-2
     "answer": 6,
     "right":  "richtig2.mp3"},

    {"audio": "ende.mp3"}
]

WRONG_WAV = "falsch.mp3"          #jede falsche antwort

