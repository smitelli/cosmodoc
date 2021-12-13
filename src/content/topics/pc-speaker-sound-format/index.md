+++
title = "PC Speaker Sound Format"
description = "An analysis of the PC speaker sound effect files and the sound samples contained within."
weight = 170
+++

# PC Speaker Sound Format

All of the sound effects in the game were played through the **PC speaker**, a small device inside the computer case that was really only designed to play single beeps to provide audible feedback to a user. By rapidly varying the **frequency** (sometimes colloquially called "pitch") of the beep, interesting **sound effects** could be produced. A total of 65 sound effects are included in the game.

Individual sound effects are packed together into **sound files**. Each sound file in the game contains up to 23 sound effects, and the [group files]({{< relref "group-file-format" >}}) contain three sound file entries in total:

Entry Name   | Description
-------------|------------
SOUNDS.MNI   | PC speaker sound effects 1&ndash;23.
SOUNDS2.MNI  | PC speaker sound effects 24&ndash;46.
SOUNDS3.MNI  | PC speaker sound effects 47&ndash;65. Contains silence data for effects 66&ndash;69, which are loaded (but never used) by the game.

{{< note >}}
When all three sound files are loaded into the game's memory, the sound effect numbers are 1-indexed. Whenever a sound file is analyzed directly in this document, the sound effect numbers are 0-indexed.
{{< /note >}}

Some sources call these **Inverse Frequency Sound Format** files because the data words are inversely related to the frequency of the tone that is played. The format was most likely designed by id Software, first appearing in both _Commander Keen in Invasion of the Vorticons_ for Apogee and _Shadow Knights_ for Softdisk. This format, and variations built from it, was used in Apogee and Softdisk games throughout the early 1990s.

## File Header

Sound files are noteworthy because they are among the few file formats in the game that have a formal header structure. This is required because each sound file contains many different sound effects, each of which has a different size.

The file begins with this header:

Offset (Bytes) | Size     | Description
---------------|----------|------------
0h             | byte[4]  | The string `SND\0` (three characters followed by one null byte).
4h             | word     | Ostensibly the total size of the file, in bytes. In practice, all of the sound files contain some amount of data past this boundary that is not normally accessed.
6h             | word     | The number of entries in the file's sound effect table.
8h             | word     | Unknown purpose; always 0032h.
Ah             | byte[6]  | Six null bytes, which pad the header to a paragraph boundary.

The header is really more of a formality than anything else. The game skips reading it entirely, and the total size value is incorrect at best and outright misleading at worst.

## Sound Effect Table

Immediately following the file header, there is a 16-byte structure repeated once per sound effect:

Offset (Bytes) | Size     | Description
---------------|----------|------------
0h             | word     | Offset to the sound data relative to the beginning of the file, in bytes.
2h             | byte     | Priority value for this sound effect, in the range 0&ndash;255. New sounds will interrupt old sounds if the new priority is equal to or greater than the old priority.
3h             | byte     | Unknown purpose; always 08h. Not used by the game.
4h             | byte[12] | Name of the sound effect. Maximum 11 characters, plus a terminating null byte. Only SOUNDS.MNI contains meaningful names, the other files use `__UnNamed__\0` for every sound effect. Not used by the game.

The game makes some blind assumptions about the content and structure of the sound files. It assumes, without checking, that the 0th sound effect table entry is at offset 10h, and it reads exactly 23 table entries from every file. Since each sound file actually contains 24 table entries, the last one in each file is never used.

{{< note >}}
Sound files intended for use with the game _must_ have at least 23 valid table entries. Otherwise the sound loader will begin interpreting unintended data as offset values, which could potentially lead to playing arbitrary memory contents as sounds.
{{< /note >}}

## Sound Data

The actual data for each sound effect is stored as a variable-length sequence of little-endian words. The sound data starts at the offset specified in a sound effect table entry and continues until word value FFFFh is read.

The sound effects service runs at a frequency of 140 **hertz** (Hz), or 140 times each second. Each time the service runs, it consumes one word from the sound data and writes the value to the system's Programmable Interval Timer. This timer is connected to the speaker inside the computer case, which emits an audible tone with a pitch related to the sound data value. Typical values encountered in the stock sound files range from 150&ndash;8,600 (in steps of 50) decimal, which translate roughly to 7,955&ndash;139 Hz, respectively. The rapid changes in pitch over time allows for interesting (albeit monophonic) sound effects to be generated.

{{< aside class="armchair-engineer" >}}
**Byte Pincher**

Since the data values in the game's sound files all fit in the range 150&ndash;8,600 in steps of 50, there are only 170 different values the game uses. These could've been encoded in bytes instead of words, halving the size of the sound data at the expense of requiring a multiplication during each run of the sound effects service. Granted, it would only save about 5,000 bytes overall.
{{< /aside >}}

If the value 0000h is read in the sound data, the speaker is silenced for that service cycle. If the value FFFFh is read, the speaker is silenced and the sound effects service goes dormant until another sound effect is started.

## Abandoned Data

The simple reality is that the sound files seem to have been created with a sloppy tool.[^muse] The accuracy of the file headers cannot be trusted and each file contains unreachable data beyond where any such data should logically occur. This section is a brief attempt to salvage and/or identify the data where possible.

### SOUNDS.MNI

The 23rd sound table entry is named JETSON. It cannot be readily determined if this is simply the phrase "jets on" or some kind of reference to _The Jetsons_ television show. The game never reads this entry and the sound can never be heard during gameplay. This is what it sounds like:

{{< audio "jetson" >}}

Following this, there are four slack bytes that are totally unreachable. These appear to be the first four bytes of JETSON repeated.

### SOUNDS2.MNI

The 23rd sound table entry in this file is silence, encoded validly.

Following this, there are 950(!) unreachable slack bytes. These appear to be a mixture of silence, copies of other sound fragments, and junk. Here are the file offsets and analyses:

* B6Eh: 70 ms of silence followed by 330 ms of a 2.4 kHz tone. Not rendered here because it's uninteresting and rather unpleasant to listen to.
* BDEh: Copy of sound effect 20.
* BF4h: Copy of sound effect 21.
* DF0h: Copy of sound effect 22.
* E0Ch: Silence, perhaps from sound effect 23.
* E10h: Copy of the tail end of sound effect 21.
* ED8h: Copy of sound effect 22.
* EF4h: Silence, perhaps from sound effect 23.
* EF8h: Copy of the tail end of sound effect 22.
* F0Ch: Silence, perhaps from sound effect 23.
* F10h: Extremely short (50 ms) descending tone. Similar data does not appear at any other point in any sound file. May be a remnant of an early version of a sound effect: {{< audio "sounds2-F10h" >}}
* F20h: Silence.

### SOUNDS3.MNI

The 19th&ndash;23rd sound table entries in this file are all silence, encoded validly.

Following this, there are 60 unreachable slack bytes. These contain a semi-regular pattern of 0000h and FFFFh words. These all appear to be pieces of silence -- the 0000h words deactivate the speaker and the FFFFh words terminate the sound effect data. No other audible information appears in this range.

[^muse]: There's a chance the software used to create the sound effects was [Muse](http://www.shikadi.net/moddingwiki/Muse), an internal tool developed by id Software (possibly a solo effort by John Romero). The only evidence I have to support this theory is the mention of Muse in Tom Hall's [Doom Bible](https://5years.doomworld.com/doombible/appendices.shtml) and the, uh, less than stellar opinion he had of it.
