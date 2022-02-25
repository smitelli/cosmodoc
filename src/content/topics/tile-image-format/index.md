+++
title = "Tile Image Format"
description = "A description of the full-screen planar EGA image file format."
weight = 140
+++

# Tile Image Format

{{< table-of-contents >}}

All of the in-game graphics are stored across about 30 different **tile image** files. Each tile image file contains the graphical data for hundreds or _thousands_ of discrete 8x8 pixel tiles. Some tile image files incorporate a transparency mask, while others are used fully opaque. The large actors and complex map constructions in the game are built from a careful arrangement of these small tiles.

The following is a list of tile-based [group file]({{< relref "group-file-format" >}}) entries:

Entry Name   | Transparency  | Description
-------------|---------------|------------
ACTORS.MNI   | yes           | Actor/decoration sprites.
BD*.MNI      | no            | Backdrops.
CARTOON.MNI  | yes           | Sprites used in the menus/story (cartoons).
FONTS.MNI    | yes, reversed | UI font. Also contains health status bars.
MASKTILE.MNI | yes           | Map tiles with transparent (masked) areas.
PLAYERS.MNI  | yes           | Player sprites.
STATUS.MNI   | no            | In-game status bar background.
TILES.MNI    | no            | Map tiles without transparent areas.

Tile image files utilize the same color, palette, and plane concepts as the [full-screen image format]({{< relref "full-screen-image-format" >}}), with differences in the high-level arrangement of the data. It's important to understand the way full-screen images work before diving into the tiles.

## Solid Tiles

A solid tile consists of 64 pixels in an 8x8 grid with 16 available colors. Each tile of this type uses **32 bytes** (8 &times; 8 &times; log&#x2082; 16 = 256 bits) of storage space in its image file. These tiles are stored contiguously, one every 32 bytes, with no header information or padding. Depending on the way a particular file is used, an individual tile may be located either by using its zero-based index (multiplied by 32 to get a byte offset) or by using a direct byte or word offset into the file.

As with all the game graphics, individual tile images are stored in a planar format with blue, green, red, and intensity bits separated from one another. Unlike their full-screen counterparts, however, tiles are stored in a **row-planar** form where the planes are interleaved much more tightly. The four planes that comprise a single pixel row are stored in four consecutive bytes before the next row's data begins.

This is best demonstrated with a diagram. To display the 628th tile image from TILES.MNI, we seek to offset 4E80h (628 &times; 32) and read 32 bytes from that position:

{{< image src="row-planar-solid-2052x.png"
    alt="Solid row-planar data storage example."
    1x="row-planar-solid-684x.png"
    2x="row-planar-solid-1368x.png"
    3x="row-planar-solid-2052x.png" >}}

Things line up nicely: each byte contains eight bits, each bit represents one screen pixel, and the tiles are all eight pixels wide. Therefore each byte of the file represents one single row of tile pixels.

The plane order is blue, green, red, intensity. All the planes for a single row of pixels are stored sequentially, so the first four bytes encode the four planes for the first pixel row, the next four bytes encode the second pixel row, and the pattern continues until the final four bytes encode the eighth pixel row.

## Masked Tiles

A masked tile is also an 8x8 grid of pixels with 16 colors, plus one additional bit on each pixel to indicate transparency. This means a single masked tile uses **40 bytes** of storage space in a tile image file. As with the solid tiles, each masked tile is stored contiguously, one every 40 bytes, with no header information or padding.[^actorseg]

Masked tiles are almost identical to solid tiles, except there are _five_ planes instead of four. The extra plane contains the transparency mask, and the plane order here is mask, blue, green, red, intensity. A mask bit of `1` represents a transparent/invisible pixel, while `0` represents a solid/visible pixel -- but be advised that this is reversed in FONTS.MNI for no apparent reason.

Another diagram is warranted. To display the 1,452nd tile image from ACTORS.MNI, we seek to offset E2E0h (1,452 &times; 40) and read 40 bytes from that position:

{{< image src="row-planar-masked-2052x.png"
    alt="Masked row-planar data storage example."
    1x="row-planar-masked-684x.png"
    2x="row-planar-masked-1368x.png"
    3x="row-planar-masked-2052x.png" >}}

{{< note >}}
Some tile image files (ACTORS.MNI, CARTOON.MNI, and PLAYER.MNI) are not designed to be accessed using direct indexing alone, and generally require reading a byte offset from a [tile info file]({{< relref "tile-info-format" >}}) to draw anything larger than 8x8 pixels.
{{< /note >}}

## ACTORS.MNI Segmentation

The ACTORS.MNI file is 191,910 bytes in size, which is far too large for a single 65,535-byte memory allocation. To make everything fit, the game reads this file piecewise into two 65,535-byte segments, followed by one 60,840 segment containing the remaining data.

The 40-byte masked tile size does not divide evenly into 65,535, which results in 15 bytes of slack space at the end of the first two segments. Because the file mirrors the memory layout, this means the file itself has slack space as well.

Offset (Bytes) | Size (Bytes) | Description
---------------|--------------|------------
0              | 40           | Tile 0.
40             | 65,440       | Tiles 1&ndash;1,636, one every 40 bytes.
65,480         | 40           | Tile 1,637.
65,520         | 15           | Slack space; contains a redundant copy of the first part of tile 1,638.
65,535         | 40           | Tile 1,638.
65,575         | 65,440       | Tiles 1,639&ndash;3,274, one every 40 bytes.
131,015        | 40           | Tile 3,275.
131,055        | 15           | Slack space; contains a redundant copy of the first part of tile _3,292_.
131,070        | 40           | Tile 3,276.
131,110        | 60,760       | Tiles 3,277&ndash;4,795, one every 40 bytes.
191,870        | 40           | Tile 4,796.

{{< note >}}
Several tiles are duplicated around the second segment boundary. Tiles 3,260&ndash;3,275 are unused redundant copies of tiles 3,276&ndash;3,291, and the slack space at the end of the second segment contains a redundant fragment of tile 3,292. This was done to avoid breaking a 2x9-tile actor sprite ({{< lookup/actor 145 >}}, frame 3) across two segments.
{{< /note >}}

When trying to locate the starting offset of a tile index in ACTORS.MNI, one must add 15 bytes to the offset each time a segment boundary is crossed:

```python
# 1638 is the number of full tiles in a segment: floor(65535 / 40)
num_boundaries_crossed = floor(index / 1638)
offset = (index * 40) + (num_boundaries_crossed * 15)
```

Typically this conversion is not necessary, as correct actor tile offsets are directly stored inside the ACTRINFO.MNI [tile info file]({{< relref "tile-info-format" >}}).

[^actorseg]: The segmenting shenanigans in ACTORS.MNI notwithstanding.
