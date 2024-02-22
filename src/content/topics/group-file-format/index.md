+++
title = "Group File Format"
description = "An analysis of the .STN and .VOL files that hold the binary assets for each episode of the game."
weight = 100
+++

# Group File Format

{{< table-of-contents >}}

The binary assets of the game are stored in a handful of files that I'll collectively refer to as "group files" in this document. Each episode has one STN file and one VOL file; both are required for the game to function:

File       | Size (Bytes) | Date           | Hashes (MD5, SHA-1)
-----------|--------------|----------------|--------------------
COSMO1.STN | 607,004      | April 15, 1992 | `7d57a6c0bda490adc3ede02fbec14793`,<br>`4e4ba181972cc15f051844b9acceb20a24936465`
COSMO1.VOL | 1,359,939    | April 15, 1992 | `8d6596e26e54cba818449d0cd774368a`,<br>`ff7685781661737c5a9209dd7829fd775287cbcd`
COSMO2.STN | 607,004      | April 15, 1992 | `7d57a6c0bda490adc3ede02fbec14793`,<br>`4e4ba181972cc15f051844b9acceb20a24936465`
COSMO2.VOL | 1,308,939    | April 15, 1992 | `4971bb21107571b91261bf44e7a347c9`,<br>`ebae0110214947b41673a759d8c409330d2b8cfa`
COSMO3.STN | 607,004      | April 15, 1992 | `7d57a6c0bda490adc3ede02fbec14793`,<br>`4e4ba181972cc15f051844b9acceb20a24936465`
COSMO3.VOL | 1,267,305    | April 15, 1992 | `56e30f1949e13875a9b89ce425e3965c`,<br>`fc30ab4025d64beb7d40ecbe75d290fc03b3a204`

The astute will notice that all of the STN files, regardless of the episode they belong to, are bit-for-bit identical. This seems to be a core part of the rationale for the STN/VOL split -- the base functionality that appears in all three games is identical, so the assets that accompany those features can be stored in and fetched from identical STN files. The VOL files, on the other hand, are all very different from episode to episode.

{{% aside class="speculation" %}}
**What do STN and VOL stand for?**

That's known only to the original designer(s) of the layout. If I were forced to wager a guess, I would say **standard** and **volume**.
{{% /aside %}}

A group file is simply a container that holds one or more **entries**. Each entry is a blob of data, indexed by a DOS-style ("8.3") name. Entries within a group file are analogous to files within a directory on a disk.

There is no compression or encoding used anywhere in the group file format. What's stored on disk is exactly what gets copied into memory.

## Location

The group files are always opened relative to the DOS working directory when the game was started. This means that the user *must* `CD` to the directory containing the group files before trying to start the game.

If the working directory is not correct (i.e. entering `CD \` and then something like `C:\COSMO1\COSMO1.EXE`), the game will fail to locate the group files. There is no error handling for this condition, and the game will crash with a bit of display garbage.

## Header

Each group file contains a header structure listing entry names, offsets, and sizes (sort of like a table of contents or, more properly, a file allocation table).

The structure of one header entry is:

Offset (Bytes) | Size     | Description
---------------|----------|------------
00h            | byte[12] | String containing the entry's name, in 8.3 format. The game assumes that all alphabetical characters are stored as uppercase. Unused trailing bytes are set to null. An entry name that uses all twelve bytes of the 8.3 representation is not null-terminated.
0Ch            | dword    | Integer offset to the start of the data, relative to the start of the group file, in bytes.
10h            | dword    | Integer size of the data, in bytes.

Each header entry occupies exactly 20 bytes, and the entries repeat one after another until there are no more entries to list.

Immediately after the last header entry, the total number of entries is encoded as an ASCII string (i.e. `32h 31h` for `"21"`). I do not have enough specimens of this data format to definitively say if the number here is fixed-width, padded, or null-terminated.

Following this, the header is null-padded until offset FA0h. Regardless of the number of entries in each group file, the header is padded to be *exactly* 4,000 bytes long and, presumably, can hold at most 199 entries. (The 200th entry slot would contain the total count as an ASCII string.) Again, I do not have a specimen with that many entries inside, and it's not at all clear what should happen in the corner cases that crop up when processing such a large header.

## Reading Data

The data for all entries starts immediately after the header padding. The data is stored contiguously without special alignment or inter-entry padding. There is not even a requirement that entries start on an even offset; the evenness of so many of the offsets is a consequence of the fact that almost all the entry sizes are naturally even.

To read the data for any entry, first walk the header looking for an entry whose name matches the one needed. Read the `offset` and `size` values from that entry. Seek to `offset`, and read `size` bytes starting from there.

{{% note %}}Like most of the data in the game, the integer values for the offset and size are packed in little-endian order.{{% /note %}}

If the search arrives at an entry with a null name, or if the end of the 4,000 byte header is reached, all entries have been searched without finding a match.

As a pseudocode example, say we wanted to find the data named `my.mni` inside the group file `COSMO1.STN`:

```python
fp = open("COSMO1.STN")
found = false

for (i = 0; i < 4000; i += 20):
    fp.seek(i)
    entryname = fp.read_string(12)

    if entryname == "":  # Put another way, it starts with a null byte
        # There are no more occupied entry slots
        break

    if entryname != uppercase("my.mni"):  # Header names are all-caps
        # Not looking at the right `entryname` yet
        continue

    # The `entryname` matches what we're looking for
    found = true
    offset = fp.read_integer(4)
    size = fp.read_integer(4)
    fp.seek(offset)
    data = fp.read_binary(size)  # `data` contains everything we want
    break

if not found:
    # `my.mni` is not in this group file
```

This format, while quite simple, is also flexible and immensely abusable. Some things that should be possible:

* Storing entry data in a different order than the header indexes it.
* Naming entries as arbitrary 12-byte strings with no dot, or a misplaced dot. The 8.3 naming style is merely a convention.
* Declaring the same name twice in the index (per the techniques described on this page, only the first entry would be accessible).
* Pointing multiple header entries to the same data, or partially-overlapping windows into some larger data.
* Creating slack space between the end of one entry's data and the start of another. Data could be hidden in this way.

Much to my own disappointment, none of these techniques have been used in any of the group files that shipped with the game.

## List of Group File Contents

For anyone who is curious what's contained inside each group file, here is a dump of the header data. Each row contains a brief description of what that entry is used for in the game.

All offsets and sizes are in decimal bytes, to show the "round" nature of many of the entry sizes.

### COSMO{1,2,3}.STN

Entry Name   | Offset (Bytes) | Size (Bytes) | Description
-------------|----------------|--------------|------------
MASKTILE.MNI | 4,000          | 40,000       | Images for the map tiles. These have a transparency mask.
TILES.MNI    | 44,000         | 64,000       | Images for the map tiles. These do not have transparency.
ACTRINFO.MNI | 108,000        | 4,646        | Index containing widths, heights, and pointers to all sprite frames for actors.
PLYRINFO.MNI | 112,646        | 386          | Index containing widths, heights, and pointers to all sprite frames for the player.
CARTINFO.MNI | 113,032        | 178          | Index containing widths, heights, and pointers to all cartoon images used in the menus/story.
CARTOON.MNI  | 113,210        | 64,280       | Images used in the menus/story (cartoons).
FONTS.MNI    | 177,490        | 4,000        | Images used to draw the UI font. Also contains health status bars.
SOUNDS.MNI   | 181,490        | 3,332        | PC speaker sound numbers 1-23.
SOUNDS2.MNI  | 184,822        | 3,876        | PC speaker sound numbers 24-46.
SOUNDS3.MNI  | 188,698        | 4,020        | PC speaker sound numbers 47-65.
ACTORS.MNI   | 192,718        | 191,910      | Images used as actor/decoration sprites.
PLAYERS.MNI  | 384,628        | 30,000       | Images used as player sprites.
PRETITLE.MNI | 414,628        | 32,000       | Full-screen image: {{< lookup/full-screen-image 0 >}}
TILEATTR.MNI | 446,628        | 7,000        | Behavior flags for map tiles (solid, slippery, can cling to wall, etc.).
BONUS.MNI    | 453,628        | 32,000       | Full-screen image: {{< lookup/full-screen-image 3 >}}
CREDIT.MNI   | 485,628        | 32,000       | Full-screen image: {{< lookup/full-screen-image 2 >}}
ONEMOMNT.MNI | 517,628        | 32,000       | Full-screen image: {{< lookup/full-screen-image 5 >}}
STATUS.MNI   | 549,628        | 7,296        | Image for the in-game status bar background.
BDSTAR2.MNI  | 556,924        | 23,040       | Backdrop image: {{< lookup/backdrop 12 >}}
BDSTAR3.MNI  | 579,964        | 23,040       | Backdrop image: {{< lookup/backdrop 13 >}}
NOMEMORY.MNI | 603,004        | 4,000        | B800 text screen: "You do not have enough memory..."

Total entries: 21

### COSMO1.VOL

Entry Name   | Offset (Bytes) | Size (Bytes) | Description
-------------|----------------|--------------|------------
TITLE1.MNI   | 4,000          | 32,000       | Full-screen image: "Forbidden Planet - Adventure 1 of 3"
END1.MNI     | 36,000         | 32,000       | Full-screen image: Cosmo falling toward {{< lookup/actor type=247 strip=true >}}.
A1.MNI       | 68,000         | 67,154       | Map data: E1M1.
A2.MNI       | 135,154        | 67,418       | Map data: E1M2.
A3.MNI       | 202,572        | 67,262       | Map data: E1M3.
A5.MNI       | 269,834        | 67,904       | Map data: E1M5.
A6.MNI       | 337,738        | 66,884       | Map data: E1M6.
A9.MNI       | 404,622        | 66,752       | Map data: E1M9.
A10.MNI      | 471,374        | 68,156       | Map data: E1M10.
A11.MNI      | 539,530        | 65,984       | Map data: E1M11 (deep pit with {{< lookup/actor type=247 strip=true >}} at bottom).
A7.MNI       | 605,514        | 67,700       | Map data: E1M7.
A8.MNI       | 673,214        | 67,502       | Map data: E1M8.
BONUS1.MNI   | 740,716        | 66,794       | Map data: Bonus stage (tall).
BONUS2.MNI   | 807,510        | 67,580       | Map data: Bonus stage (wide).
A4.MNI       | 875,090        | 67,004       | Map data: E1M4.
BDWIERD.MNI  | 942,094        | 23,040       | Backdrop image: {{< lookup/backdrop 6 >}}
BDNEWSKY.MNI | 965,134        | 23,040       | Backdrop image: {{< lookup/backdrop 11 >}}
BDFOREST.MNI | 988,174        | 23,040       | Backdrop image: {{< lookup/backdrop 14 >}}
BDSPOOKY.MNI | 1,011,214      | 23,040       | Backdrop image: {{< lookup/backdrop 22 >}}
BDCLIFF.MNI  | 1,034,254      | 23,040       | Backdrop image: {{< lookup/backdrop 21 >}}
BDICE2.MNI   | 1,057,294      | 23,040       | Backdrop image: {{< lookup/backdrop 20 >}}
BDCLOUDS.MNI | 1,080,334      | 23,040       | Backdrop image: {{< lookup/backdrop 18 >}}
BDROCKTK.MNI | 1,103,374      | 23,040       | Backdrop image: {{< lookup/backdrop 3 >}}
BDMOUNTN.MNI | 1,126,414      | 23,040       | Backdrop image: {{< lookup/backdrop 15 >}}
MHAPPY.MNI   | 1,149,454      | 15,848       | AdLib music: {{< lookup/music 8 >}}
MDRUMS.MNI   | 1,165,302      | 20,640       | AdLib music: {{< lookup/music 12 >}}
MRUNAWAY.MNI | 1,185,942      | 10,892       | AdLib music: {{< lookup/music 3 >}}
MZZTOP.MNI   | 1,196,834      | 25,152       | AdLib music: {{< lookup/music 18 >}}
MDEVO.MNI    | 1,221,986      | 25,784       | AdLib music: {{< lookup/music 9 >}}
MBOSS.MNI    | 1,247,770      | 29,584       | AdLib music: {{< lookup/music 2 >}}
MCAVES.MNI   | 1,277,354      | 17,080       | AdLib music: {{< lookup/music 0 >}}
MDADODA.MNI  | 1,294,434      | 23,768       | AdLib music: {{< lookup/music 10 >}}
COSMO1.MNI   | 1,318,202      | 4,000        | B800 text screen: Normal episode exit screen.
MTECK4.MNI   | 1,322,202      | 14,908       | AdLib music: {{< lookup/music 17 >}}
MEASY2.MNI   | 1,337,110      | 21,060       | AdLib music: {{< lookup/music 14 >}}
PREVDEMO.MNI | 1,358,170      | 1,769        | Recorded keyboard input for the demo.

Total entries: 36

### COSMO2.VOL

Entry Name   | Offset (Bytes) | Size (Bytes) | Description
-------------|----------------|--------------|------------
TITLE2.MNI   | 4,000          | 32,000       | Full-screen image: "Forbidden Planet - Adventure 2 of 3"
END2.MNI     | 36,000         | 32,000       | Full-screen image: Cosmo overlooking a city at night.
BONUS3.MNI   | 68,000         | 66,134       | Map data: Bonus stage (wide).
B1.MNI       | 134,134        | 65,984       | Map data: E2M1. Identical copy of A11.MNI from COSMO1.VOL.
B2.MNI       | 200,118        | 67,256       | Map data: E2M2.
B3.MNI       | 267,374        | 67,520       | Map data: E2M3.
B4.MNI       | 334,894        | 67,004       | Map data: E2M4.
B5.MNI       | 401,898        | 67,370       | Map data: E2M5.
B6.MNI       | 469,268        | 67,514       | Map data: E2M6.
B7.MNI       | 536,782        | 66,896       | Map data: E2M7.
B8.MNI       | 603,678        | 67,154       | Map data: E2M8.
BONUS4.MNI   | 670,832        | 67,160       | Map data: Bonus stage (tall).
MCAVES.MNI   | 737,992        | 17,080       | AdLib music: {{< lookup/music 0 >}}
B9.MNI       | 755,072        | 66,842       | Map data: E2M9.
B10.MNI      | 821,914        | 67,616       | Map data: E2M10.
MSCARRY.MNI  | 889,530        | 17,012       | AdLib music: {{< lookup/music 1 >}}
MTEKWRD.MNI  | 906,542        | 25,924       | AdLib music: {{< lookup/music 5 >}}
MBELLS.MNI   | 932,466        | 14,284       | AdLib music: {{< lookup/music 11 >}}
MDRUMS.MNI   | 946,750        | 20,640       | AdLib music: {{< lookup/music 12 >}}
MEASY2.MNI   | 967,390        | 21,060       | AdLib music: {{< lookup/music 14 >}}
BDWIERD.MNI  | 988,450        | 23,040       | Backdrop image: {{< lookup/backdrop 6 >}}
BDGUTS.MNI   | 1,011,490      | 23,040       | Backdrop image: {{< lookup/backdrop 16 >}}
BDSHRUM.MNI  | 1,034,530      | 23,040       | Backdrop image: {{< lookup/backdrop 9 >}}
BDICE.MNI    | 1,057,570      | 23,040       | Backdrop image: {{< lookup/backdrop 8 >}}
BDCRYSTL.MNI | 1,080,610      | 23,040       | Backdrop image: {{< lookup/backdrop 23 >}}
BDFOREST.MNI | 1,103,650      | 23,040       | Backdrop image: {{< lookup/backdrop 14 >}}
BDCIRCUT.MNI | 1,126,690      | 23,040       | Backdrop image: {{< lookup/backdrop 24 >}}
MRUNAWAY.MNI | 1,149,730      | 10,892       | AdLib music: {{< lookup/music 3 >}}
MBANJO.MNI   | 1,160,622      | 14,636       | AdLib music: {{< lookup/music 13 >}}
BDCAVE.MNI   | 1,175,258      | 23,040       | Backdrop image: {{< lookup/backdrop 7 >}}
COSMO2.MNI   | 1,198,298      | 4,000        | B800 text screen:  Normal episode exit screen.
MZZTOP.MNI   | 1,202,298      | 25,152       | AdLib music: {{< lookup/music 18 >}}
BDPIPE.MNI   | 1,227,450      | 23,040       | Backdrop image: {{< lookup/backdrop 1 >}}
MTECK4.MNI   | 1,250,490      | 14,908       | AdLib music: {{< lookup/music 17 >}}
MROCKIT.MNI  | 1,265,398      | 18,344       | AdLib music: {{< lookup/music 7 >}}
PREVDEMO.MNI | 1,283,742      | 2,157        | Recorded keyboard input for the demo.
BDMOUNTN.MNI | 1,285,899      | 23,040       | Backdrop image: {{< lookup/backdrop 15 >}}

Total entries: 37

{{% aside class="fun-fact" %}}
**Byte Pincher**

COSMO2.VOL includes entries for MDRUMS.MNI and BDFOREST.MNI, neither of which is actually used by any of the maps in that episode. Omitting them would have shaved almost 43 KiB off the size of the file.
{{% /aside %}}

### COSMO3.VOL

Entry Name   | Offset (Bytes) | Size (Bytes) | Description
-------------|----------------|--------------|------------
TITLE3.MNI   | 4,000          | 32,000       | Full-screen image: "Forbidden Planet - Adventure 3 of 3"
END3.MNI     | 36,000         | 32,000       | Full-screen image: Cosmo on a roller coaster with other children.
C4.MNI       | 68,000         | 68,318       | Map data: E3M4.
C1.MNI       | 136,318        | 66,932       | Map data: E3M1.
C2.MNI       | 203,250        | 67,202       | Map data: E3M2.
C3.MNI       | 270,452        | 67,874       | Map data: E3M3.
C5.MNI       | 338,326        | 67,448       | Map data: E3M5.
C6.MNI       | 405,774        | 67,478       | Map data: E3M6.
C7.MNI       | 473,252        | 67,388       | Map data: E3M7.
C8.MNI       | 540,640        | 67,952       | Map data: E3M8.
BONUS5.MNI   | 608,592        | 66,248       | Map data: Bonus stage (contains "HI!" message).
C9.MNI       | 674,840        | 66,812       | Map data: E3M9.
BONUS6.MNI   | 741,652        | 67,220       | Map data: Bonus stage (looks like Dig Dug).
BDPIPE.MNI   | 808,872        | 23,040       | Backdrop image: {{< lookup/backdrop 1 >}}
BDTECHMS.MNI | 831,912        | 23,040       | Backdrop image: {{< lookup/backdrop 10 >}}
BDBRKTEC.MNI | 854,952        | 23,040       | Backdrop image: {{< lookup/backdrop 17 >}}
BDFUTCTY.MNI | 877,992        | 23,040       | Backdrop image: {{< lookup/backdrop 19 >}}
BDCRYSTL.MNI | 901,032        | 23,040       | Backdrop image: {{< lookup/backdrop 23 >}}
BDCIRCPC.MNI | 924,072        | 23,040       | Backdrop image: {{< lookup/backdrop 25 >}}
C10.MNI      | 947,112        | 65,918       | Map data: E3M10.
MEASYLEV.MNI | 1,013,030      | 14,168       | AdLib music: {{< lookup/music 6 >}}
MZZTOP.MNI   | 1,027,198      | 25,152       | AdLib music: {{< lookup/music 18 >}}
MSCARRY.MNI  | 1,052,350      | 17,012       | AdLib music: {{< lookup/music 1 >}}
MROCKIT.MNI  | 1,069,362      | 18,344       | AdLib music: {{< lookup/music 7 >}}
MTECK2.MNI   | 1,087,706      | 14,972       | AdLib music: {{< lookup/music 15 >}}
MTECK3.MNI   | 1,102,678      | 18,076       | AdLib music: {{< lookup/music 16 >}}
MTECK4.MNI   | 1,120,754      | 14,908       | AdLib music: {{< lookup/music 17 >}}
MCIRCUS.MNI  | 1,135,662      | 7,256        | AdLib music: {{< lookup/music 4 >}}
BDJUNGLE.MNI | 1,142,918      | 23,040       | Backdrop image: {{< lookup/backdrop 4 >}}
COSMO3.MNI   | 1,165,958      | 4,000        | B800 text screen: Normal episode exit screen.
MBOSS.MNI    | 1,169,958      | 29,584       | AdLib music: {{< lookup/music 2 >}}
MDEVO.MNI    | 1,199,542      | 25,784       | AdLib music: {{< lookup/music 9 >}}
BDGUTS.MNI   | 1,225,326      | 23,040       | Backdrop image: {{< lookup/backdrop 16 >}}
MHAPPY.MNI   | 1,248,366      | 15,848       | AdLib music: {{< lookup/music 8 >}}
PREVDEMO.MNI | 1,264,214      | 3,091        | Recorded keyboard input for the demo.

Total entries: 35

{{% aside class="speculation" %}}
**What does MNI stand for?**

Why does everybody ask me things I don't know? All I have is an educated guess: **manifest**.

If not that, maybe **moniker** or **mnemonic**.
{{% /aside %}}

Overall the entries are split up in a rational way. MZZTOP.MNI and MTECK4.MNI are the only entries that appear in all three VOL files. They would have been ideal candidates to be stored in the STN files instead, but for whatever reason they ended up where they did.

It appears as though a conscious effort was made to ensure entry names across different episodes were kept unique (for instance, END1/END2/END3 for the end story images and A1/B1/C1 for map one of each episode). If all the group files were extracted into the same directory, the only names that would conflict are identical copies of the same data (and PREVDEMO.MNI).

{{% aside class="speculation" %}}
**I see patterns where none exist.**

There may be some archaeological significance to the order of the entries in each group file, with later entries having been changed/added more recently in the game's development and testing. It's also possible that I'm completely wrong about that.
{{% /aside %}}

## The STN Files Have It All

If you look at what's actually in the VOL files, you'll notice there aren't any sprites, tiles, cartoon images, or sounds anywhere inside. All of those come from the STN file, which means all that data is available in all the episodes -- _even the first shareware episode._

Episode one didn't have the {{< lookup/actor 101 >}}, for instance. Or the {{< lookup/actor 221 >}}. It also did not have any story screens that showed cartoons of Cosmo jumping through a cave ceiling or speaking to Zonk. Nobody playing episode one should have encountered any of these, and yet all the graphical data that supported these elements was on the shareware disk.

Similarly, episodes two and three didn't have the Cosmo family's ship from the beginning of E1M1. Episode two didn't have the {{< lookup/actor 102 >}}. The nontrivial amount of tiles needed to build these are nestled snugly in the STN file regardless, seemingly unaware that nobody ever intended to use them in these episodes.
