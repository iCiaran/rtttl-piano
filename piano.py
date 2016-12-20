import json
import re
import sys


def main():
    notes = {"A": 13, "A#": 14, "Bb": 14, "B": 15, "C": 4, "C#": 5, "Db": 5,
             "D": 6, "D#": 7, "Eb": 7, "E": 8, "F": 9, "F#": 10, "Gb": 10,
             "G": 11, "G#": 12, "Ab": 12}
    make(notes)


def make(notes):
    try:
        with open(sys.argv[1], 'r') as f:
            rtttl = f.readline().strip().strip(",").split(":")
    except IndexError:
        sys.stderr.write("No File specified\n")
        sys.exit(1)
    except FileNotFoundError:
        sys.stderr.write("File {} Not Found\n".format(sys.argv[1]))
        sys.exit(1)

    json_data = getSong(notes, rtttl)

    file = "{}{}".format(re.sub("\W", '_', rtttl[0]), ".json")
    with open(file, 'w') as f:
        f.write(json_data)


def getSong(notes, rtttl):
    settings = rtttl[1].split(",")
    defaultD = int(settings[0].split("=")[1])
    defaultO = int(settings[1].split("=")[1])
    defaultB = int(settings[2].split("=")[1])

    song = []
    split_notes = rtttl[2].split(",")

    for i in range(len(split_notes)):
        note = split_notes[i].strip()
        if "p" not in note:

            rest_duration = 0

            if i != len(split_notes)-1:
                if "p" in split_notes[i+1].lower():
                    rest = split_notes[i+1].strip().lower().replace("p", "")
                    if len(rest) > 0 and rest[-1] == ".":
                        rest_dotted = True
                        rest = rest[:-1]
                    else:
                        rest_dotted = False
                    if len(rest) == 0:
                        rest_d = defaultD
                    else:
                        rest_d = int(rest)
                    rest_duration = getDuration(rest_d, defaultB,
                                                rest_dotted)

            if note[-1].isdigit():
                o = int(note[-1])
                note = note[:-1]
            else:
                o = defaultO

            if note[-1] == ".":
                dotted = True
                note = note[:-1]
            else:
                dotted = False

            if note[-1] == "#":
                pitch = note[-2:].upper()
                note = note[:-2]
            else:
                pitch = note[-1].upper()
                note = note[:-1]

            if len(note) == 0:
                d = defaultD
            else:
                d = int(note) + rest_duration

            pianoNote = (o - 2) * 12 + notes[pitch]
            duration = getDuration(d, defaultB, dotted) + rest_duration
            song.append((pianoNote, duration))
    return getJson(song)


def getJson(song):
    json_data = {}
    for i in range(len(song)):
        json_data[str(i+1)] = {}
        json_data[str(i+1)]["notes"] = [str(song[i][0])]
        json_data[str(i+1)]["interval"] = song[i][1]
    return json.dumps(json_data)


def getDuration(d, b, dotted):
    qDuration = 60 * 1000 / b
    duration = qDuration * 4 / d
    if dotted:
        duration *= 1.5
    return int(duration)


if __name__ == '__main__':
    main()
