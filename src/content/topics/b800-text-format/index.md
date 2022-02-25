+++
title = "B800 Text Format"
description = "An analysis of the text screens shown when the game ends."
weight = 160
+++

# `B800` Text Format

{{< table-of-contents >}}

Most shareware (and registered!) games of the era displayed a full-screen text page immediately before returning to the DOS prompt, and _Cosmo_ was no exception:

{{< image src="b800-example-2052x.png"
    alt="Sample of a full screen of B800 text."
    1x="b800-example-684x.png"
    2x="b800-example-1368x.png"
    3x="b800-example-2052x.png" >}}

These screens showed colorful line-drawn boxes, customarily in front of a background that resembled the closed curtains on a theater stage. Most contained teasers and ordering information in the case of shareware episodes, or messages thanking the player for purchasing the registered episodes.

Much less commonly, this type of text display was used to provide a more substantial-looking error message in cases where the game was unable to run on a particular system:

{{< image src="b800-low-memory-2052x.png"
    alt="Another sample of B800 text, this time for a low memory error."
    1x="b800-low-memory-684x.png"
    2x="b800-low-memory-1368x.png"
    3x="b800-low-memory-2052x.png" >}}

{{< aside class="armchair-engineer" >}}
**Red Marking Pen**

These were some of the, shall we say, "less proofread" parts of the game.
{{< /aside >}}

There were several `B800` text entries in the game's [group files]({{< relref "group-file-format" >}}):

Entry Name   | Description
-------------|------------
COSMO1.MNI   | End screen for episode 1. Contains teasers for the registered game and ordering information.
COSMO2.MNI   | End screen for episode 2. Contains advertisements for other Apogee games.
COSMO3.MNI   | End screen for episode 3. Identical to COSMO2.MNI except for the episode number in the top line of text.
NOMEMORY.MNI | Error message explaining that the system does not have enough memory.

## The `B800` Mechanism

PC-compatible graphics adapters that supported color usually booted into mode number 03h by default. This was a text mode providing 80x25 characters with 16 colors. The foreground and background color of each character on the screen could be set independently.

`B800` files are named after the segment address where the mode 03h screen buffer is located: `B800:0000`. The 4,000 bytes at this memory-mapped address contain the full screen buffer, and writing data within this address range  immediately changes the text/colors displayed on the screen. That's all the file format is -- 4,000 bytes that are loaded directly into the video memory in order to put characters on the screen.

The printable text content uses 2,000 bytes (80 &times; 25) of memory, the foreground colors use 1,000 bytes (80 &times; 25 &times; log&#x2082; 16 = 8,000 bits), and the background colors use another 1,000 bytes. The colors are encoded using the standard [RGBI palette]({{< relref "full-screen-image-format#colors-and-palettes" >}}) with one key difference: on the background _only_, the intensity bit flashes the foreground text instead of brightening the background color. `B800` text files utilized this liberally.

## Encoding and Decoding

Within a `B800` text file, and the memory area it mirrors, every even-addressed byte controls the **character** displayed on the screen, and every odd-addressed byte controls the **attributes** (foreground color, background color, flashing) on the character that immediately preceded it.

Characters and attributes are stored in row-major order, starting at the top-left corner of the screen.

### Characters

Unicode 1.0 was less than a year old when the game was released, and DOS PCs were rooted firmly in the world of **code pages**. The basic idea was this: Since there were only eight bits available for each character on the screen, there could only be 256 (2<sup>8</sup>) different characters (or **code points**) to choose from. This isn't too much of a problem if all you're doing is writing using the Latin alphabet, but toss in Cyrillic, Greek, Arabic, Hebrew, Urdu... You run out of encoding space real fast. Using code pages, the system can "switch" to a different display font, where the underlying text data doesn't change but the fonts on the display do:

{{< data-table/cp-comparison >}}

Note that in the preceding table, _the raw bytes never change._ All that changes from one code page to another is what the visual representation of a code point is.

The lower half of most code pages was the same, mirroring the 7-bit character assignments originally defined by the American Standard Code for Information Interchange (**ASCII**) in the 1960s. This allowed for compatible rendering of the letters A-Z, digits, and common printable punctuation characters across all configurations. The upper half above 80h, however, was a free-for-all.

The prevailing theory of the day was that files would tend to only be opened on computers that were geographically near one another, and all of those computers would be configured to use the same code page for display. If a file was written with the expectation that it would be displayed in one code page, and was instead opened on a computer with a different code page loaded, it may display as abject gibberish. The IBM PC (and most compatibles sold in the Western world) booted into code page 437 (**CP437**) by default.

CP437 defined a few international characters -- mostly currency symbols, accented vowels to properly write out certain names and loanwords from other languages, and enough Greek letters and mathematical symbols to write physics equations. Most of the rest of the characters were for block and box drawing, allowing solid filled areas and continuous single- or double-lines to be drawn in all four directions with corners and intersections. These box drawing characters were integral to some of the first text-based UIs in DOS software. They were also used extensively in `B800` text screens.

The full CP437 character set is as follows:

{{< data-table/cp437 >}}

{{< aside class="fun-fact" >}}
**Everything old is new again.**

There are some precursors to emoji in the CP437 table -- especially the faces, arrows, and playing card suits. Some computers may even display some of the above characters _as_ emoji.
{{< /aside >}}

In files and console output, the control characters (00h-1Fh) represent newlines, tabs, audible beeps, and other commands to move the cursor around. In the video memory, however, these characters have absolutely no special behavior and display a single character just like any other.

### Attributes

Each attribute byte has four bits that control foreground color, three bits that control background color, and one bit that controls flashing of the foreground text:

Bit Position              | Description
--------------------------|------------
0 (least significant bit) | Foreground blue palette bit.
1                         | Foreground green palette bit.
2                         | Foreground red palette bit.
3                         | Foreground intensity palette bit.
4                         | Background blue palette bit.
5                         | Background green palette bit.
6                         | Background red palette bit.
7 (most significant bit)  | `0` = foreground text displays normally, `1` = foreground text flashes.

The default system color was 07h, or low-intensity white on a black background.

The attribute byte affects the character byte that immediately precedes it:

Offset (Bytes) | Description
---------------|------------
0              | Character at (0, 0).
1              | Attributes for character at (0, 0).
2              | Character at (1, 0).
3              | Attributes for character at (1, 0).
...            | ...
3,996          | Character at (78, 24).
3,997          | Attributes for character at (78, 24).
3,998          | Character at (79, 24).
3,999          | Attributes for character at (79, 24).

## Programming Considerations

DOS is unaware of characters drawn directly to video memory, and the cursor position is not updated in any way to reflect the updated contents of the screen. When the program exits, DOS thinks the screen is blank and the most appropriate place for the prompt should be at the current cursor position, which is near the top of the screen. With `B800` text already occupying space on the screen, this naive assumption results in the DOS prompt appearing on top of the text, with new and old characters and attributes jumbling together in an unreadable mess.

Typically, any program that displayed `B800` text would also emit -- usually via {{< lookup/cref printf >}} -- a series of newline characters to move the cursor down far enough to clear the bottom of the displayed text.
