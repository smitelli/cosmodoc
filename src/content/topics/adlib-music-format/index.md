+++
title = "AdLib Music Format"
description = "An analysis of the AdLib music file format and the different pieces of hardware that played it."
weight = 180
+++

# AdLib Music Format

There are 19 different songs across all three episodes, with a total of just over 19 minutes of music in total. The music is stored in a format that some sources call the id Music Format (**IMF**) in honor of its creators, id Software. The code to handle this file format was originally written by Jason Blochowiak, and he most likely designed the whole scheme. IMF music first appeared in _Catacomb 3-D_ in November 1991, and could have appeared earlier in _Commander Keen in Keen Dreams_ if the music hadn't been stripped out before the game's release.

The following is a list of songs within the [group files]({{< relref "group-file-format" >}}):

Entry Name   | Description
-------------|------------
MBANJO.MNI   | {{< lookup/music 13 >}}
MBELLS.MNI   | {{< lookup/music 11 >}}
MBOSS.MNI    | {{< lookup/music 2 >}}
MCAVES.MNI   | {{< lookup/music 0 >}}
MCIRCUS.MNI  | {{< lookup/music 4 >}}
MDADODA.MNI  | {{< lookup/music 10 >}}
MDEVO.MNI    | {{< lookup/music 9 >}}
MDRUMS.MNI   | {{< lookup/music 12 >}}
MEASY2.MNI   | {{< lookup/music 14 >}}
MEASYLEV.MNI | {{< lookup/music 6 >}}
MHAPPY.MNI   | {{< lookup/music 8 >}}
MROCKIT.MNI  | {{< lookup/music 7 >}}
MRUNAWAY.MNI | {{< lookup/music 3 >}}
MSCARRY.MNI  | {{< lookup/music 1 >}}
MTECK2.MNI   | {{< lookup/music 15 >}}
MTECK3.MNI   | {{< lookup/music 16 >}}
MTECK4.MNI   | {{< lookup/music 17 >}}
MTEKWRD.MNI  | {{< lookup/music 5 >}}
MZZTOP.MNI   | {{< lookup/music 18 >}}

Each song was tailor-made for playback via a peripheral card called the AdLib Music Synthesizer Card (**AdLib**), which can play a rich variety of polyphonic instruments through external speakers plugged into the computer.

The AdLib produces music by using a process of **synthesis**, where the actual note frequencies, volumes, and waveform selections are all stored as compact numeric parameters. During playback, these parameters are used to program a bank of oscillators and level controllers which generate sounds in real-time. Contrast this with the digital audio playback features of later cards like the **Sound Blaster**, where the exact amplitude of the source sound wave is sampled thousands of times per second and played back precisely as it was recorded -- at the expense of requiring many hundreds of times the amount of storage space.

The AdLib card is really nothing more than a Yamaha YM3812 sound chip (sometimes called the **OPL2**) with the bare minimum circuitry required to interface it with the PC's AT bus. Its operation was simple to clone, and soon other sound cards became competitive. The original Sound Blaster included an OPL2 chip connected in an AdLib-compatible way in addition to other features like digital sound and a built-in game port. Later cards eliminated the Yamaha sound chips entirely and used a software-emulated replacement. The rise of these inexpensive all-in-one cards eventually drove Ad Lib, Inc. out of business. In spite of that, its programming conventions survived, and many sound cards can play music from games that were only designed to support the original AdLib card.

## AdLib Operation

It's not possible to fully understand the music format without having at least a cursory knowledge of how the AdLib functions, due to how tightly the format is coupled to the hardware.

The AdLib is an I/O device, with its base address conventionally located at port 388h. Any time a program writes a byte to I/O address 388h, it is writing to the OPL2's **address register**. Directly above the base address, at 389h, there is the OPL2's **data register**. To control the AdLib and the OPL2 chip it contains, the program must write one byte to the address register, wait a bit, then write one byte to the data register. These writes always come in pairs. The address register tells the AdLib what parameter(s) should be changed, and the data register tells it what that parameter's value should be changed to.

Any change to the parameter values _immediately_ affects the sound being played, which means commands to start and stop individual notes must be sent to the AdLib in real-time, right when that change should be audible to the listener. This also means that if the program gets stuck or locks up and stops feeding the AdLib, the music will freeze in place and "ring" indefinitely until the program gets unstuck or the user reboots the computer.

Listening to the music, it's easy to fall into the trap of thinking the data consists of nothing but simple "note-on" and "note-off" commands. In reality the music is nuanced and complex, and overall it averages about 75 parameter changes each second.

The music service responsible for updating the AdLib registers runs at a constant rate of 560 Hz. Each time it runs, it reads an address/value pair from the music file, sends them _unmodified_ to the AdLib, then reads a delay value from the file that specifies how many cycles it should wait before reading the next piece of data. Once the end of the file is reached, the read position is reset to the very beginning of the file and the song begins playing again.

## Music File Format

With the concept of AdLib registers and delay values fresh in our minds, the file format almost explains itself: It is simply a byte for the AdLib's address register, followed by a byte for its data register, followed by a little-endian word containing the delay value. This four-byte pattern repeats for the entire length of the file.

Offset (Bytes) | Size | Description
---------------|------|------------
0h             | byte | The value to write to the AdLib's address register.
1h             | byte | The value to write to the AdLib's data register.
2h             | word | The number of cycles to wait before handling the next pair of values. There are 560 cycles per second. A value of `0` will immediately move to the next pair of values without any delay.

Each file begins with four null bytes, resulting in a write of data `0` to the nonexistent AdLib address `0` with zero delay afterwards. This doesn't appear to cause any harm, but it's definitely an invalid write. It's not clear why it does that.

{{< note >}}Later games with more advanced versions of IMF use a different structure that does not start with four null bytes.{{< /note >}}

The OPL2 has well over 120 different registers, and the music in the game uses most of them. It's beyond the scope of this particular section to explain what each of them actually does, but rest assured it is [dark magic]({{< relref "adlib-functions" >}}).
