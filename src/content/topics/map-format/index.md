+++
title = "Map Format"
description = "An analysis of the map files that define the game's playable world."
weight = 110
+++

# Map Format

{{< table-of-contents >}}

The game world is stored across several distinct files called **maps**. These map files define the floors, walls, and ceilings of the world, along with other stationary structures like trees, pipes, and ice formations. Map files also contain a list of all actors that should be inserted into the world, and the starting position for each one. Everything the player encounters while progressing through the levels of each episode is specified in a sequence of map files.

Within the [group files]({{< relref "group-file-format" >}}), individual maps are stored in entries named A1--11.MNI (for episode one), B1--10.MNI (for episode two), C1--10.MNI (for episode three), and BONUS1--6.MNI (two bonus levels per episode). There are 37 maps across all three episodes, 36 of them unique (A11 and B1 are identical).

Each map file contains the following sections:

* Global variables, which control the backdrop, music, and other map-specific global parameters.
* A list of actors to insert into the game world, along with the initial coordinates for each.
* A two-dimensional grid of (almost) 32,768 map tiles, which defines the static architecture of the game world.

## Global Variables

All of the map variables are stored in the first six bytes of the file. The format is as follows:

Offset (Bytes) | Size | Description
---------------|------|------------
0h             | word | Encoded map variables. See next section.
2h             | word | Width of the map, in tiles.
4h             | word | Size of the actor list, in words.

### Map Variables Word

The map variables are packed into a single 16-bit little-endian word, with some values interpreted as boolean flags and others as integers:

Bit Position                    | Size (Bits) | Description
--------------------------------|-------------|------------
0--4   (least significant bits) | 5           | Numeric [backdrop ID]({{< relref "databases/backdrop" >}}) (0--31).
5                               | 1           | Rain flag. `0` = no rain, `1` = rain falls in empty map areas.
6                               | 1           | Backdrop horizontal scroll flag. `0` = backdrop is fixed in the horizontal direction, `1` = backdrop scrolls horizontally with the world.
7                               | 1           | Backdrop vertical scroll flag. `0` = backdrop is fixed in the vertical direction, `1` = backdrop scrolls vertically with the world.
8--10                           | 3           | Numeric [palette animation ID]({{< relref "databases/palette-animation" >}}) (0--7).
11--15 (most significant bits)  | 5           | Numeric [music ID]({{< relref "databases/music" >}}) (0--31).

{{% note %}}The parenthetical number ranges indicate the smallest and largest values that can be encoded in the map format. Not all expressible IDs are defined, and selecting an invalid ID may cause a read outside of array bounds and other unpredictable behavior.{{% /note %}}

### Map Width and Height

The game world size is conceptually fixed at 32,768 tiles&sup2; regardless of the actual dimensions, so the height of the map is constrained by the width. There are a limited number of width values that the game implements:

Width (Tiles) | Height (Tiles) | {{< lookup/cref mapYPower >}} | Notes
--------------|----------------|-------------------------------|------
32            | 1,024          | 5                             | Not used; width is too small to fill the screen entirely.
64            | 512            | 6                             |
128           | 256            | 7                             |
256           | 128            | 8                             |
512           | 64             | 9                             |
1,024         | 32             | 10                            | Not used.
2,048         | 16             | 11                            | Not used; height is too small to fill the screen entirely.

Smaller factors of 32,768, while expressible in the map file format, are not implemented by the game and will not work correctly. Non-factors of 32,768 could also be expressed, and will _certainly_ break things.

## List of Actors

The actor list has a variable size depending on the number of actors actually present in the map. The list always begins at offset 6h in the map file, and continues for the number of _words_ specified in the preceding map variable.

Each actor list entry has the following structure, repeated at three-word intervals until the total size has been read:

Offset (Bytes) | Size | Description
---------------|------|------------
0h             | word | Map actor type. Further processing is required to differentiate "special" actors from "normal" ones. See next paragraph.
2h             | word | Initial X position, in tiles, relative to the west edge of the map.
4h             | word | Initial Y position, in tiles, relative to the north edge of the map.

The actor type read from the map file may represent either of the following:

* **Special actor:** Includes {{< lookup/special-actor 0 >}}, {{< lookup/special-actor type=1 plural=true >}}, {{< lookup/special-actor type=2 strip=true plural=true >}}, and {{< lookup/special-actor type=6 strip=true plural=true >}}.
* **Normal actor:** All other actor types typically encountered.

If the map actor type is less than 31, it is treated as a [special actor]({{< relref "databases/actor#special-actors" >}}) and the type is used unchanged. If the map actor type is 31 or greater, it is treated as a [normal actor]({{< relref "databases/actor#normal-actors" >}}) and the type is decremented by 31 before insertion into the world.

{{% note %}}The X/Y coordinates always refer to the leftmost/bottommost tile of multi-tile actors. Some normal actors have a positive or negative "shift" value imposed on their initial X and/or Y positions. If a shift is defined for a particular actor type, the starting position is adjusted by the predefined number of tiles before insertion. The shift value is typically used to compensate for the width or height of an actor's sprite when aligning it to a specific wall or ceiling coordinate.{{% /note %}}

Due to the limited number of fields available in the actor list format, it's not possible to define any per-actor attributes or characteristics -- all actors of a given type display the same way, take the same amount of damage, and behave identically.

### Limitations

The game has a fixed amount of memory allocated for the different structures that comprise the game world (and scant error handling for some conditions). This means there are practical limits that a valid actor list should never exceed:

Map Actor Type                                  | Limit | What happens if limit is exceeded?
------------------------------------------------|-------|-----------------------------------
{{< lookup/special-actor 0 >}}                  | 1     | Later {{< lookup/special-actor type=0 plural=true >}} overwrite the earlier ones.
{{< lookup/special-actor 1 >}}                  | 10    | Writes outside of array bounds, leading to memory corruption.
{{< lookup/special-actor type=2 strip=true >}} | 10    | Writes outside of array bounds, leading to memory corruption.
{{< lookup/special-actor type=6 strip=true >}} | 199   | Any additional {{< lookup/special-actor type=6 strip=true plural=true >}} are ignored.
Normal Actor                                    | 410   | Completely stops reading the actor list from the map file.

## Map Tiles

Immediately following the end of the actor list, there are _exactly_ 65,528 bytes of map tile data. This is interpreted as a two-dimensional array of 32,764 unsigned little-endian words in row-major order. Each of these words represents a single graphical tile of the game world, with the four tiles at the southeast corner of the map undefined. (The first tile in the array is at the northwest corner of the world, and the last tile is at the southeast corner.)

The bottom row of tiles is never shown on the screen and the player movement functions disregard anything present there. It is essentially a discarded row of garbage data which protects the undefined tiles from causing visual issues or odd movement behavior. Any "air" or passable tiles immediately above the garbage row may be fallen through to implement bottomless pits.

{{% aside class="armchair-engineer" %}}
**Weird Numbers**

Each map contains exactly four fewer tiles than it should, for reasons that are only partially apparent.

In order to allocate a contiguous block of 65,536 bytes in memory, {{< lookup/cref farmalloc >}} would need to be used due to the constraints of the underlying 16-bit system. It appears as though {{< lookup/cref malloc >}} was used instead, which can only provide up to 65,535 usable bytes in a single call. That reduction in space knocked one tile off the total usable number.

The other three missing tiles, I have no idea about.
{{% /aside %}}

The map data is largely static; once a map tile has been read into memory it does not generally change. (There are a few specific actor types -- mostly those that restrict movement or allow the player/actors to stand on top of them -- that manipulate map tile values during gameplay, but these are relatively rare.) The **attributes** for each map tile value are defined in a [separate file]({{< relref "tile-attributes-format" >}}) and specify how the player/actors interact with each tile during gameplay.

Depending on the numeric value of each map tile, it is drawn as either a **solid** tile (with no transparency) or a **masked** tile (with transparent areas where the backdrop shows through). Map tile values below 16,000 are treated as solid tiles, and values 16,000 or above are treated as masked tiles. Tiles with the same value will look the same, have the same tile attributes index, and behave the same way.

### Masked Tiles

Masked tiles are relatively simple. First, a conversion is performed to convert the map tile value into a masked tile index:

    [masked tile index] = ([map tile value] - 16000) / 40

The subtraction by 16,000 is necessary to remove the offset that differentiates the masked tiles from solid tiles. The division by 40 accounts for the in-memory alignment of the actual graphical data. (This is an implementation detail that is discussed in depth in the drawing chapter.) Map tiles in this range are _always_ an even multiple of 40.

The map format allows up to 1,238 distinct masked tile indices to be expressed, but the game graphics only define 1,000 masked tiles. This means that the only indices that should be encountered in practice are 0--999, corresponding to map tile values 16,000--55,960.

Each masked tile graphic is drawn into the game world at the specified position. Transparent areas within a masked tile graphic are filled with the appropriate piece of the backdrop behind it.

### Solid Tiles

Solid tiles work similarly to masked tiles, but they are packed more densely and there are more special cases. To convert the map tile value into a solid tile index:

    [solid tile index] = [map tile value] / 8

The division by 8 accounts for the in-memory alignment of the actual graphical data. (Again, this is an implementation detail that is discussed in depth in the drawing chapter.) Map tiles in this range are _always_ an even multiple of 8.

The map format allows 2,000 distinct solid tile indices to be expressed, and all of them are defined in the game graphics. Each solid tile index from 0--1,999 (map tile values 0--15,992) should do _something_, even if the result is not directly visible on the screen.

* Indices **10--1,964** are typical cases, where each solid tile is drawn directly into the game world at the specified position.
* Indices **1,965--1,986** are not directly used in any maps, however solid tiles of this type are dynamically created and removed by various actors during the course of the game. These generally display normally in the game world once created, although sometimes sprites are strategically positioned to hide the tiles from view.
* Indices **1,987--1,999** are used in menu frames and text display areas, and never display in any part of the game world.
* Indices **0--9** are _never drawn_ by the game and the backdrop is shown in their place. Typically these are used to represent empty space or sky. Aside from their invisibility, these tiles have special meanings to the game:

Tile Index | Description
-----------|------------
0          | Empty space where the player and actors can move freely. If a {{< lookup/special-actor 1 >}} is centered on this tile, it will halt indefinitely.
1          | Empty space. If a {{< lookup/special-actor 1 >}} is centered on this tile, it will move north during its next tick.
2          | Empty space. If a {{< lookup/special-actor 1 >}} is centered on this tile, it will move northeast during its next tick.
3          | Empty space. If a {{< lookup/special-actor 1 >}} is centered on this tile, it will move east during its next tick.
4          | Empty space. If a {{< lookup/special-actor 1 >}} is centered on this tile, it will move southeast during its next tick.
5          | Empty space. If a {{< lookup/special-actor 1 >}} is centered on this tile, it will move south during its next tick.
6          | Empty space. If a {{< lookup/special-actor 1 >}} is centered on this tile, it will move southwest during its next tick.
7          | Empty space. If a {{< lookup/special-actor 1 >}} is centered on this tile, it will move west during its next tick.
8          | Empty space. If a {{< lookup/special-actor 1 >}} is centered on this tile, it will move northwest during its next tick.
9          | Invisible tile which blocks southern movement. (Player/actors can walk and jump through the tile, but cannot fall through it.) Not directly used in any maps, however tiles of this type are dynamically created at the tops of {{< lookup/actor type=190 strip=true >}} and {{< lookup/special-actor type=2 strip=true >}} actors.
