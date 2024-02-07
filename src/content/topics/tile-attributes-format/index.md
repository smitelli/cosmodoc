+++
title = "Tile Attributes Format"
description = "An analysis of the tile attributes file that controls the behavior of map tiles."
weight = 120
+++

# Tile Attributes Format

{{< table-of-contents >}}

The **tile attributes** file specifies what should happen when the player (or actors) touch a map tile of a given value. This data is stored in a [group file]({{< relref "group-file-format" >}}) entry named TILEATTR.MNI. Each of the 2,000 solid and 1,000 masked tiles has an associated **index** within the tile attributes file. Each index is comprised of a single byte which encodes eight boolean **attributes**.

## Index Lookup

The tile attributes file is exactly 7,000 bytes long. The first 2,000 bytes of the file directly correspond to the 2,000 solid tile indices; there is a 1:1 correlation between the tile attributes index and the solid tile index.

The remaining 5,000 bytes of the file correspond to the 1,000 masked tile indices with a 5:1 correlation -- each masked tile's attribute data is still encoded in one byte, but each index in this range is aligned to a five-byte boundary and padded with insignificant data.

This disparity in storage space between the solid tiles and the masked tiles is caused by the tight coupling of this file format with that of the [map files]({{< relref "map-format" >}}): Solid map tile values are multiples of eight, and masked map tile values are multiples of 40. The tile attributes format preserves this ratio, but scales everything down so the solid tile indices are one byte apart. This actually simplifies the lookup of a tile attribute index for a given map tile value:

    [tile attribute index] = [map tile value] / 8

This works regardless of the tile's solid/masked type.

## Attribute Encoding

The attributes at each tile index are encoded into a single byte, with each bit controlling a distinct behavior of that tile:

Bit Position              | Behavior
--------------------------|---------
0 (least significant bit) | `0` = player/actors can move south through this tile, `1` = south movement is blocked (i.e. tile can be stood on).
1                         | `0` = player/actors can move north through this tile, `1` = north movement is blocked (i.e. player will hit their head).
2                         | `0` = player/actors can move west through this tile, `1` = west movement is blocked.
3                         | `0` = player/actors can move east through this tile, `1` = east movement is blocked.
4                         | `0` = tile is not slippery, `1` = tile is slippery, and player will slip south without control input to counteract it.
5                         | `0` = tile appears behind player/actors, `1` = tile appears in front of player/actors and blocks them from view (i.e. the sprites are drawn "behind" this tile).
6                         | `0` = tile does not auto-ascend, `1` = player/actors will auto-ascend if this tile is walked into.
7 (most significant bit)  | `0` = tile cannot be clung using the player's suction hands, `1` = tile is clingable.

It's important to note that the tile attributes index has a fixed relationship with the graphical tile that will ultimately be drawn on the screen. This means that each graphical tile has _constant_ tile attributes that cannot be altered on a case-by-case basis by the map data.

This means, for example, that if a map designer wanted to make a solid wall with a hidden tunnel inside it, using visually indistinguishable graphics for both areas, they would need a redundant copy of the wall tile graphical data to make it work -- the original would represent the solid wall, and the duplicate would represent the tunnel with different tile attributes allowing it to be walked through.

To minimize such waste and reduce the need for duplicated graphics, most tile attributes specify every behavior that could possibly be relevant to the tile, even if some behaviors aren't appropriate in all map contexts where the tile is used.

### Movement Blocking

Four of the tile attribute bits specify whether or not movement through a tile is permitted. Each bit represents one of the four cardinal directions (south, north, west, east). If any of the bits are set to `1`, movement through the tile is not permitted in the associated direction(s).

The two most obvious blocking behaviors are all zeros, representing free and unrestricted movement in all directions (e.g. air, purely aesthetic background decoration) and all ones, representing no movement at all (e.g. solid piece of wall, floor, and/or ceiling). 90% of the tiles in the game have one of these two behaviors.

One of the more common variants is a tile with southern movement blocked, but all other directions permitted. This creates a tile that can be walked and jumped through, but if the player lands on it they will not fall through. Many stationary platforms in the game behave this way, where the player can jump onto a surface freely but not fall through it. There are 159 tile values with this behavior.

Using this scheme it's also possible to make one-way walls or other frustrating and unintuitive constructions. There are only 130 tiles in the game that could plausibly demonstrate such behavior, but most are not used in map locations where their unusual effects would be readily apparent.

### Slippery

If a tile has its "slippery" attribute set to `1`, it will randomly glisten.

If the player is clinging to a tile with its "slippery" attribute set to `1`, they will slide south. The only way to counteract this is to repeatedly press the jump key and re-cling.

If the player is standing on a tile with its "slippery" attribute set to `1`, and that tile also has its "auto-ascend" attribute set to `1`, the player may slip southwest or southeast depending on their surroundings. Trying to counteract this with opposite east/west input will cancel out all movement, making the player walk in place.

### In-Front

If a tile has its "in-front" attribute set to `1`, _most_ sprites will not draw over it. The exceptions tend to be things like score effects and the player's death animation.

### Auto-Ascend

Auto-ascending permits the player to walk on a sloped incline without having to explicitly jump between areas that differ in height by one tile. For an auto-ascend tile to work correctly, it must not block movement in any direction that would prohibit the player from (temporarily) entering the tile.

When the player walks into a tile with its "auto-ascend" attribute set to `1`, the player's position is adjusted one tile to the north. This allows the player to walk along a sloped incline, constructed from a stair-step of auto-ascend tiles, without needing to jump. Once the player is standing on top of an auto-ascend tile, that tile functions similarly to one with "block southern movement" behavior.

As the player descends a sloped incline, the game recognizes that the initial position is directly above an auto-ascend tile and the subsequent position is above a tile of empty space. When this occurs, the player's position is adjusted one tile to the south _without_ invoking any of the typical falling animations or mechanics. This permits a smooth walking descent without the player "falling" down the incline.

### Clingable

If a tile has its "clingable" attribute set to `1` and is being used as part of a wall, the player is capable of clinging to that tile with their suction hands. The player/wall check is performed in approximately the same vertical position as the suction hands in the player graphics.

## Unused Data

The masked tile area of the tile attributes file uses 5,000 bytes to store 1,000 meaningful bytes, which means there are 4,000 slack bytes that serve no useful purpose. There is a small archaeological curiosity hidden in there: All the bytes in the range 2,000&ndash;2,999 that are not multiples of five contain legitimate data that nothing ever uses.

These 800 slack bytes are absolutely identical to those in the range 2,000&ndash;6,999 that _are_ multiples of five. Put another way, it appears as though this file format used only 3,000 bytes at one point, with the solid and masked tiles packed without any slack space, and then later the masked tiles were spread out without zeroing the old data locations.

The rest of the bytes (3,000&ndash;6,999) that are _not_ multiples of five are all zero.
