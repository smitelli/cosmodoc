+++
title = "Tile Info Format"
description = "An analysis of the tile info files that allow tiles to be grouped together into larger sprites."
weight = 150
+++

# Tile Info Format

{{< table-of-contents >}}

Individual tiles have a fixed size of 8x8 pixels, but most of the sprites in the game are larger than that. The player sprites, for instance, are usually 3x5 tiles (or 24x40 pixels) in size. **Tile info** files specify how individual 8x8 tiles should be arranged on the screen to form larger sprites. Some may know this concept by another name -- **metasprites** -- although that's more commonly used when discussing console gaming.

Tile info files are used when drawing sprites for actors/decorations, cartoons, and the player. The tile info file for each game object has its own [group file]({{< relref "group-file-format" >}}) entry:

Entry Name   | Number of Sprite Types  | Description
-------------|-------------------------|------------
ACTRINFO.MNI | 267                     | Used when drawing actors/decorations. Each sprite type has between 1 and 15 frames.
CARTINFO.MNI | 1                       | Used when drawing cartoon images. Its single sprite type has 22 frames; each frame is a different image.
PLYRINFO.MNI | 1                       | Used when drawing the player. Its single sprite type has 48 frames.

In order to locate data in a tile info file, two pieces of information need to be known:

* The zero-indexed **sprite type** number. This is simple for the cartoons and player; since each only defines a single sprite type, 0 can be used. For the actors and decorations, the sprite type is tied to the [actor type]({{< relref "databases/actor#normal-actors" >}}) or hard-coded into the game in some way. Sometimes the sprite type and actor type are the same, but often they are not.
* The zero-indexed **frame number**. Most sprite types contain more than one frame, either for animation purposes or for complex drawing cases.

The first section of a tile info file contains the lookup table that is used to locate the initial frame for each sprite type. The remainder of the file contains the data -- height, width, and tile image offset -- that defines every frame for each sprite type.

## Frame Data Lookup

To look up the tile info data for a given sprite type/frame pair, do the following:

1. Seek to `[sprite type] * 2` bytes into the tile info file. Read the 16-bit little-endian word at this position. This is the **frame zero offset** in words.
2. Seek to `([frame zero offset] * 2) + ([frame number] * 8)` bytes into the tile info file. Read 8 bytes from this position and interpret according to the following table (all values are little-endian):

Offset (Bytes) | Size (Bytes) | Description
---------------|--------------|------------
0h             | 2h           | Height of the sprite, in tiles.
2h             | 2h           | Width of the sprite, in tiles.
4h             | 2h           | Offset within the tile image file, in bytes.
6h             | 2h           | Segment within the tile image file. Only has a nonzero value in ACTRINFO.MNI, and only considered when drawing an actor/decoration sprite.

{{< aside class="armchair-engineer" >}}
**Go Fish**

The tile info files do not directly encode the total number of sprite types or frames that are available, but that information can usually be guessed by analyzing the files carefully:

* The total size of the sprite type lookup table can be inferred by reading from the start of the file, word by word, and tracking the smallest frame zero offset seen. When the read position reaches the smallest frame zero offset, the end of the sprite type lookup table has been reached and the number of sprite types is known.

* The number of frames for a sprite type can be inferred by calculating the byte distance between its frame zero offset and the frame zero offset for the next nearest sprite type. That distance, divided by eight, is the number of available frames.

The game doesn't do any of this; it's simply hard-coded to know what sprite types are available and how many frames each one has.
{{< /aside >}}

## Building Sprites from Tile Info Data

After looking up the sprite type and frame through the tile info file, values for `height`, `width`, and `segment:offset` are known. This is actually all that is required to draw the sprite.

The sprite will require `width` &times; `height` tiles to draw, and the data for the first tile in the sequence is stored in the tile image file at `segment:offset`. Subsequent tile images are stored sequentially after the first tile at 40-byte intervals. A (e.g.) 3x5 player sprite would require 15 tile images in total, which can be found at `segment:offset`, `segment:offset` + 40, `segment:offset` + 80, ..., `segment:offset` + 560.

Tiles are stored in row-major order, with the tile at the top-left stored first. To lay them out, fill a row (`width` tiles wide) with tiles from left to right. Once the row is full, move down to the start of the next row and repeat. Once all rows (`height` tiles tall) are filled, the sprite is completely drawn:

{{< image src="sprite-layout-2052x.png"
    alt="Arranging tiles into sprites."
    1x="sprite-layout-684x.png"
    2x="sprite-layout-1368x.png"
    3x="sprite-layout-2052x.png" >}}

{{< note >}}
Drawing for a sprite always begins at the top-left tile, but the actual **origin** of the sprite is the _bottom_-left tile. The game does this to (slightly) reduce the amount of work that needs to be done to test the position of game objects relative to the floors.
{{< /note >}}

To draw the sprite at an arbitrary `x_origin` and `y_origin` position (both in units of tiles), do the following:

```python
# These values specify where the sprite will display on the screen (the
# origin of a sprite is the leftmost, *bottommost* tile):
x_origin = ...  # X tile coordinate of the sprite's display origin
y_origin = ...  # Y tile coordinate " " "

# These values came from the tile info file:
height = ...  # Height of the sprite, in tiles
width = ...  # Width of the sprite, in tiles
segment:offset = ...  # Location of the data in the tile image memory

# xi/yi are the count variables for the current draw position. Drawing starts
# at the top-left corner and proceeds in Y-major order.
xi = x_origin
yi = (y_origin - height) + 1

while 1:
    # Low-level drawing method. Reads 40 bytes from the address specified in
    # arg 1 and draws it to the screen at tile position (arg 2, arg 3).
    draw_one_tile(segment:offset, xi, yi)

    offset += 40  # Size of one tile's image data

    if xi == (x_origin + width) - 1:  # Now at the last column of a row
        if yi == y_origin:  # Also at the last row of the sprite
            # The entire sprite has been drawn
            break
        # Wrap back to the first column and advance to the next row
        xi = x_origin
        yi++
    else:
        # Advance to next column
        xi++
```
