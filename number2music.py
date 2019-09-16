import sys
import textwrap
import pysynth

from DirectionEnum import Direction
from NoteEnum import Notes
from NoteFreq import NoteFreq
from DurationEnum import Duration

TEMPO = 90 

def file_to_array(file_arg):
    with open(file_arg, 'r') as f:
        content = f.readlines()[0].rstrip()
        width = 3
        array = [content[i:i + width] for i in range(0, len(content), width)] # https://stackoverflow.com/a/13673133
        if len(array[-1]) != 3:
            del array[-1]
        return array

def array_to_dict(array):
    new = []
    for index, item in enumerate(array):
        new.append({
            "direction": int(item[0]),
            "change": int(item[1]),
            "duration": int(item[2])
        })
    return new

def get_direction(mus_data):
    for index, item in enumerate(mus_data):
        number = item["direction"]
        if number >= 0 and number <= 1:
            direction = Direction.NO
        elif number >= 2 and number <= 5:
            direction = Direction.UP
        elif number >= 6 and number <= 9:
            direction = Direction.DOWN
        mus_data[index]["direction"] = direction
    return mus_data

def get_change(mus_data):
    for index, item in enumerate(mus_data):
        number = item["change"]
        if item["direction"] == Direction.NO:
            change = 0 # no change
        elif item["direction"] == Direction.UP:
            change = number # its the same
        elif item["direction"] == Direction.DOWN:
            # invert so that the change is negative (ie down)
            change = -number
        mus_data[index]["change"] = change
    return mus_data

def fix_high_low(note, change):
    # make sure we haven't gone above the highest note
    if note > 85:
        # must use - to invert the sign
        # weird math
        note = note - change * 2
    # or below the lowest
    elif note < 1:
        note = note - change * 2
    return note

def get_notes(mus_data):
    mus_data[0]["note"] = Notes.c4
    for index, item in enumerate(mus_data):
        if index == 0:
            continue
        change = item["change"]
        prev_note = mus_data[index - 1]["note"]
        note = Notes(fix_high_low(prev_note.value + change, change))
        mus_data[index]["note"] = note
    return mus_data

def get_duration(mus_data):
    for index, item in enumerate(mus_data):
        number = item["duration"]
        if number == 0:
            duration = Duration.SEMIBREVE
        elif number == 1 or number == 2:
            duration = Duration.MINIM
        elif number == 3 or number == 4 or number == 5:
            duration = Duration.CROTCHET
        elif number == 6 or number == 7:
            duration = Duration.QUAVER
        elif number == 8 or number == 9:
            duration = Duration.SEMIQUAVER
        mus_data[index]["duration"] = duration
    return mus_data

def get_array(mus_data):
    notes = []
    for item in mus_data:
        notes.append((
            item["note"].name.replace("S", "#"),
            item["duration"].value
        ))
    return tuple(notes)

def main():
    # get the durations and notes
    mus_data = file_to_array(sys.argv[1])
    mus_data = array_to_dict(mus_data)
    mus_data = get_direction(mus_data) 
    mus_data = get_change(mus_data)
    mus_data = get_notes(mus_data)
    mus_data = get_duration(mus_data)
    notes = get_array(mus_data)
    pysynth.make_wav(notes, fn="output.wav", bpm=TEMPO)

if __name__ == '__main__':
    main()
