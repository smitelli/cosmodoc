+++
title = "Composite Drawing Functions"
description = "Describes functions that build large visual constructions out of smaller 8x8 tiles."
weight = 340
+++

# Composite Drawing Functions

The game's [assembly drawing functions]({{< relref "assembly-drawing-functions" >}}) are highly optimized and fast, however they are restricted to drawing only single 8&times;8 pixel tiles on a 40&times;25 tile screen grid. Most of the objects and menu graphics in the game are larger than 8&times;8 pixels and need a higher-level function to orchestrate multiple calls to an assembly routine to draw the larger screen areas. The functions here perform this orchestration.

{{< table-of-contents >}}

There are three distinct types of objects that are large enough to be drawn in this way:

* **Sprites:** Generic visual representations of several types of in-game objects (actors, decorations, explosions, fountains, shards, and spawners).
* **Cartoons:** The graphics shown in the story pages of the menus. The name appears to derive from the fact that these images, interleaved with the text content on each page, read a bit like a comic book.
* The **Player:** The object controlled by the user. Really a special case of a sprite, but with additional behaviors and draw modes that are unique enough to warrant special handling.

Each object is stored in two [group files]({{< relref "group-file-format" >}}): the [masked tile image file]({{< relref "tile-image-format#masked-tiles" >}}) that holds the visible graphics, and the [tile info file]({{< relref "tile-info-format" >}}) that holds indexing and size information.

To draw an composite object, the caller must provide a **sprite type** number and a **frame** number. Together, these point to a location in the tile info file that holds the height, width, and starting address of the image data within the tile image file. By seeking to that offset in the image data and calling a tile drawing function _width &times; height_ times, the complete object is drawn.

For sprites, there are a total of 267 different sprite type numbers, each of which can have anywhere from one to 15 frames. Both cartoons and the player only define one sprite type number containing 22 or 48 frames, respectively.

## Origin and Draw Order

A composite object by definition can occupy more than one tile horizontally and/or vertically. When an X,Y position is passed to one of these drawing functions, that tile position is treated as the **origin** of the object and the tiles _above_ and to the _right_ from that tile are filled. Put another way, the origin tile is the _bottom-leftmost_ tile in the object. The game does this to somewhat simplify calculations between objects and the floors of maps.

Drawing order, however, proceeds in the usual left-to-right, top-to-bottom row-major order. Tiles are stored in the image files in this sequence as well. Combined with the origin details in the previous paragraph, drawing starts at the tile position given by _X_ horizontally, but _Y - height + 1_ vertically.

{{< boilerplate/function-cref DrawSprite >}}

The {{< lookup/cref DrawSprite >}} function draws a sprite of the provided `sprite_type` and `frame`, with the lower-left tile at coordinates (`x_origin`, `y_origin`). The `mode` influences the origin calculations and visual appearance, and should be one of the {{< lookup/cref DRAW_MODE >}} constants.

In most calls, `x_origin` and `y_origin` are measured relative to the game world, which is several hundred tiles in both dimensions. The screen's current scroll position is subtracted from each value to convert these positions into screen space. When `mode` is set to {{< lookup/cref name="DRAW_MODE" text="DRAW_MODE_ABSOLUTE" >}}, the origin values are used directly as screen coordinates.

```c
void DrawSprite(
    word sprite_type, word frame, word x_origin, word y_origin, word mode
) {
    word x = x_origin;
    word y;
    word height, width;
    word offset;
    byte *src;
    DrawFunction drawfn;
```

A number of local variables are defined right off the bat:

* `x` and `y`: The current X and Y position being drawn, relative to either the world or the screen (depending on `mode`).
* `height` and `width`: The dimensions of the sprite, in tiles, read from the tile info file.
* `offset`: An offset (in bytes) into the tile image data for the sprite. This is the location of the first byte of the first tile that comprises the sprite.
* `*src`: A pointer into the byte of tile image data for the sprite. This advances as image data is read.
* `drawfn`: A pointer to a function with the following signature:
    ```c
    void (*DrawFunction)(byte *, word, word);
    ```
  This is compatible with the assembly drawing functions, and allows for this function to dynamically switch between implementations based on `mode`.

```c
    EGA_MODE_DEFAULT();
```

The call to {{< lookup/cref "EGA_MODE_DEFAULT" >}} puts the EGA hardware into its default (non-latched) write state. This is the appropriate configuration to use when drawing masked tiles.

This call is necessary because the solid tiles are drawn in a different write mode, but there is no real "ownership" of this setting in the game's code. Sometimes this function is entered with the appropriate EGA write mode, and sometimes not. It all depends on when this function is being called relative to all the other areas of the code that could draw a tile. A sometimes-redundant call is safer than potentially drawing corrupted sprite data.

```c
    offset = *(actorInfoData + sprite_type) + (frame * 4);
    height = *(actorInfoData + offset);
    width = *(actorInfoData + offset + 1);

    src = actorTileData[*(actorInfoData + offset + 3)] +
        *(actorInfoData + offset + 2);
```

Here the [tile info file]({{< relref "tile-info-format" >}}) is parsed, translating the passed `sprite_type` and `frame` values into a pointer to the actual image data. {{< lookup/cref actorInfoData >}} is a `word` pointer that begins with a list of offsets to frame zero of each sprite type, followed by the four-word frame structures that comprise the sprite. `*(actorInfoData + sprite_type)` is the word offset to the structure for zeroth frame of `sprite_type`. Each frame structure is packed contiguously, so adding `(frame * 4)` skips to the offset of the structure for `frame`. The final offset to the frame structure is stored in `offset`.

The first word referenced by `offset` contains the `height` of the sprite, and the next word at `offset + 1` contains the `width`.

The word at `offset + 2` contains the offset portion of the address in the tile image data, and `offset + 3` contains the segment. The segment is used as an index into {{< lookup/cref actorTileData >}} to find the correct 64 KiB segment of image data, and the offset is added to that for byte-granular addressing. These are combined into the `src` pointer, which now points to the first byte of the first tile of the passed sprite/frame pair.

```c
    switch (mode) {
    case DRAW_MODE_NORMAL:
    case DRAW_MODE_IN_FRONT:
    case DRAW_MODE_ABSOLUTE:
        drawfn = DrawSpriteTile;
        break;
    case DRAW_MODE_WHITE:
        drawfn = DrawSpriteTileWhite;
        break;
    case DRAW_MODE_TRANSLUCENT:
        drawfn = DrawSpriteTileTranslucent;
        break;
    }

    if (mode == DRAW_MODE_FLIPPED)  goto flipped;
    if (mode == DRAW_MODE_IN_FRONT) goto infront;
    if (mode == DRAW_MODE_ABSOLUTE) goto absolute;
```

The value for `mode` is considered next, and `drawfn` is set to either {{< lookup/cref DrawSpriteTile >}}, {{< lookup/cref DrawSpriteTileWhite >}}, or {{< lookup/cref DrawSpriteTileTranslucent >}} accordingly. {{< lookup/cref name="DRAW_MODE" text="DRAW_MODE_FLIPPED" >}} is handled elsewhere, and {{< lookup/cref name="DRAW_MODE" text="DRAW_MODE_HIDDEN" >}} is not handled at all -- leading to a likely crash if used!

A bit of an abuse of `goto` is used to simulate something like a `switch` statement, with all other cases falling through. The labeled code appears later.

{{< aside class="armchair-engineer" >}}
**Really? Really.**

I stared at the disassembly of this function for a good long while trying to figure out what I missed -- surely this must've been a `switch` and not a bunch of `goto`s, right?

Nope. Every kind of `switch` construction compiles into some variant of machine code where `mode` goes into the AX register, and that's not what happens here. This _had_ to be a bunch of `goto`s -- there's no other way to make the compiler do what it did.
{{< /aside >}}

```c
    y = (y_origin - height) + 1;
    for (;;) {
        if (
            x >= scrollX && scrollX + SCROLLW > x &&
            y >= scrollY && scrollY + SCROLLH > y &&
            !TILE_IN_FRONT(MAP_CELL_DATA(x, y))
        ) {
            drawfn(src, (x - scrollX) + 1, (y - scrollY) + 1);
        }

        src += 40;

        if (x == x_origin + width - 1) {
            if (y == y_origin) {
                EGA_BIT_MASK_DEFAULT();
                break;
            }
            x = x_origin;
            y++;
        } else {
            x++;
        }
    }

    return;
```

This is the code that handles the "default" case -- normal, white or translucent drawing. These are all common in that the X/Y origins are measured relative to the game world, the sprite may be covered by "in-front" map tiles, and the sprite is drawn unmodified save for the color effects achieved through differing values of `drawfn`. The initial `y` position is determined by subtracting `height` from the provided `y_origin` value and correcting for an off-by-one error. `x` does not need any correction.

The rest of the code is a `for` loop. On each iteration, `x` is tested to make sure it's between the horizontal scroll position ({{< lookup/cref scrollX >}}) and the right edge of the visible area ({{< lookup/cref scrollX >}} + {{< lookup/cref SCROLLW >}}). `y` is tested similarly, against {{< lookup/cref scrollY >}} and {{< lookup/cref SCROLLH >}}. Additionally, a third test is performed to verify that the current tile occupies a location on the map _without_ the "in-front" flag set. (The {{< lookup/cref TILE_IN_FRONT >}} macro extracts that flag from the map cell returned by {{< lookup/cref name="MAP_CELL_DATA" text="MAP_CELL_DATA(x, y)" >}}). If all three tests pass, the current tile is visible on the screen and should be drawn.

Drawing the tile is a simple matter of calling `drawfn`, passing it the screen position computed by subtracting {{< lookup/cref scrollX >}} and {{< lookup/cref scrollY >}} from `x` and `y` (and correcting for off-by-one errors). The `src` pointer contains a tile's worth of data to be drawn at this location, and once drawing is complete it is advanced by 40 bytes to set it up for the next tile.

The remainder of the loop handles end-of-row and end-of-sprite conditions. If `x` reaches `x_origin + width - 1`, the end of a row has been reached. If `y` _also_ reached `y_origin`, the bottom-rightmost tile has been drawn and there is nothing more to do. Set {{< lookup/cref EGA_BIT_MASK_DEFAULT >}} to clean up in case any translucent drawing functions the EGA's bit mask register, then `break` out of the loop.

Otherwise, we completed drawing a row of tiles but did _not_ complete the sprite. In this case, reset `x` to the value held in `x_origin` (which wraps drawing back to the left edge of the sprite) and advance `y` to the next row down for another iteration.

The outer `else` block handles the case where a row is not yet complete -- in that case simply advance `x` one position to the right and begin the next iteration.

When the loop is finally broken out of, there is nothing left to do here and `return` passes control back to the caller.

```c
flipped:
    y = y_origin;
    for (;;) {
        if (
            x >= scrollX && scrollX + SCROLLW > x &&
            y >= scrollY && scrollY + SCROLLH > y &&
            !TILE_IN_FRONT(MAP_CELL_DATA(x, y))
        ) {
            DrawSpriteTileFlipped(src, (x - scrollX) + 1, (y - scrollY) + 1);
        }

        src += 40;

        if (x == x_origin + width - 1) {
            if (y == (y_origin - height) + 1) break;
            x = x_origin;
            y--;
        } else {
            x++;
        }
    }

    return;
```

The `flipped` case looks and works substantially the same as the default case, but all calculations pertaining to the `y` value on screen are flipped vertically: Drawing starts at `y_origin`, the termination condition checks `(y_origin - height) + 1`, and `y` decrements with each row.

The altered loop here draws the _tiles_ in a flipped sequence, but the special drawing function {{< lookup/cref DrawSpriteTileFlipped >}} is needed to draw the _pixel rows_ flipped. Since `drawfn` is not used, and there is no opportunity to call one of the translucent draw functions, this loop does not need to call {{< lookup/cref EGA_BIT_MASK_DEFAULT >}} to clean up like the default case did.

The end result is a sprite that is drawn in the expected location with a vertical flip.

```c
infront:
    y = (y_origin - height) + 1;
    for (;;) {
        if (
            x >= scrollX && scrollX + SCROLLW > x &&
            y >= scrollY && scrollY + SCROLLH > y
        ) {
            drawfn(src, (x - scrollX) + 1, (y - scrollY) + 1);
        }

        src += 40;

        if (x == x_origin + width - 1) {
            if (y == y_origin) break;
            x = x_origin;
            y++;
        } else {
            x++;
        }
    }

    return;
```

The `infront` case handles drawing sprites that cannot be blocked by "in-front" map tiles. The logic here is identical to the default case, except here the {{< lookup/cref TILE_IN_FRONT >}} is removed. This makes the map data irrelevant -- every tile of the sprite is always drawn (unless it's off the screen edge, of course).

Since `drawfn` is always set to {{< lookup/cref DrawSpriteTile >}} here, there is no opportunity for a translucent drawing mode to be used. This makes the {{< lookup/cref EGA_BIT_MASK_DEFAULT >}} cleanup call unnecessary here as well.

```c
absolute:
    y = (y_origin - height) + 1;
    for (;;) {
        DrawSpriteTile(src, x, y);

        src += 40;

        if (x == x_origin + width - 1) {
            if (y == y_origin) break;
            x = x_origin;
            y++;
        } else {
            x++;
        }
    }
}
```

The `absolute` case is used when the provided `x_origin` and `y_origin` values refer to screen coordinates, not positions in the game world, rendering the checks and corrections for scroll position unnecessary. The remaining code is substantially similar to the `infront` case.

The only interesting thing to mention is that the call to {{< lookup/cref DrawSpriteTile >}} could've been replaced with `drawfn` here -- it has the correct value from the earlier `switch`.

Since this is the final case in the function, it does not need a `return`; execution falls off the end of the function regardless.

{{< boilerplate/function-cref DrawCartoon >}}

The {{< lookup/cref DrawCartoon >}} function draws a cartoon having the provided `frame` number, with the lower-left tile at coordinates (`x_origin`, `y_origin`). This is meant to be called in the menu system only, so coordinates are all measured relative to the screen.

This function works substantially like {{< lookup/cref DrawSprite >}} with `mode` set to {{< lookup/cref name="DRAW_MODE" text="DRAW_MODE_ABSOLUTE" >}}.

```c
void DrawCartoon(byte frame, word x_origin, word y_origin)
{
    word x = x_origin;
    word y;
    word height, width;
    word offset;
    byte *src;

    EGA_BIT_MASK_DEFAULT();
    EGA_MODE_DEFAULT();
```

Each of the local variables here have the same purpose as those in {{< lookup/cref DrawSprite >}}.

{{< lookup/cref EGA_BIT_MASK_DEFAULT >}} restores the EGA's bit mask register to its default state. The bit mask is modified whenever sprites are drawn with a translucency effect, but each of those functions already cleans up before returning. This call is therefore likely unnecessary.

{{< lookup/cref EGA_MODE_DEFAULT >}} puts the EGA hardware into its default (non-latched) write state. This is the appropriate configuration to use when drawing masked tiles.

```c
    if (isCartoonDataLoaded != true) {
        isCartoonDataLoaded = true;
        LoadCartoonData("CARTOON.MNI");
    }
```

This function employs a bit of a memory-saving hack, which somewhat limits the places where this function can be called. The {{< lookup/cref isCartoonDataLoaded >}} variable tracks whether the memory contains cartoon data already and, if not, the {{< lookup/cref LoadCartoonData >}} function reads the [group file]({{< relref "group-file-format" >}}) entry named `CARTOON.MNI`.

{{< aside class="note" >}}
**Note:** `isCartoonDataLoaded` is explicitly compared against `1` in the disassembly, indicating that it was most likely an integer variable in the original code. I made it a boolean to make its intention clear, but it still requires an explicit compare against `true` to keep the original behavior.
{{< /aside >}}

{{< lookup/cref LoadCartoonData >}} loads the cartoon data from disk and stores it in the {{< lookup/cref mapData >}} variable. As a consequence of this, any map data held there is overwritten. Due to this memory-sharing, cartoons can only be shown in contexts where the map data is not being used (i.e. in the main menu).

```c
    offset = *cartoonInfoData + (frame * 4);
    height = *(cartoonInfoData + offset);
    width = *(cartoonInfoData + offset + 1);

    y = (y_origin - height) + 1;
    src = mapData.b + *(cartoonInfoData + offset + 2);
```

As in {{< lookup/cref DrawSprite >}}, the [tile info]({{< relref "tile-info-format" >}}) data stored in {{< lookup/cref cartoonInfoData >}} is interpreted to find the `offset`, `height`, and `width` of the cartoon image. The initial `y` position is calculated, and `src` is constructed to point to the first byte of image data, which was stashed in the byte-sized union member of {{< lookup/cref mapData >}}.

```c
    for (;;) {
        DrawSpriteTile(src, x, y);

        src += 40;

        if (x == x_origin + width - 1) {
            if (y == y_origin) break;
            x = x_origin;
            y++;
        } else {
            x++;
        }
    }
}
```

The remainder of the function performs the drawing, one 8&times;8 tile at a time, through repeated calls to {{< lookup/cref DrawSpriteTile >}}. Again, this is the same as the `absolute` drawing case in {{< lookup/cref DrawSprite >}}.

{{< boilerplate/function-cref DrawPlayer >}}

The {{< lookup/cref DrawPlayer >}} function draws a player sprite having the provided `frame` number, with the lower-left tile at coordinates (`x_origin`, `y_origin`). The `mode` influences the origin calculations and visual appearance, and should be one of the {{< lookup/cref DRAW_MODE >}} constants.

This function has many similarities to {{< lookup/cref DrawSprite >}}, with a few player-specific modifications.

```c
void DrawPlayer(byte frame, word x_origin, word y_origin, word mode)
{
    word x = x_origin;
    word y;
    word height, width;
    word offset;
    byte *src;
    DrawFunction drawfn;

    EGA_MODE_DEFAULT();
```

Each of the local variables here have the same purpose as those in {{< lookup/cref DrawSprite >}}.

{{< lookup/cref EGA_MODE_DEFAULT >}} puts the EGA hardware into its default (non-latched) write state. This is the appropriate configuration to use when drawing masked tiles.

```c
    switch (mode) {
    case DRAW_MODE_NORMAL:
    case DRAW_MODE_IN_FRONT:
    case DRAW_MODE_ABSOLUTE:
        drawfn = DrawSpriteTile;
        break;
    case DRAW_MODE_WHITE:
        drawfn = DrawSpriteTileWhite;
        break;
    case DRAW_MODE_TRANSLUCENT:
        drawfn = DrawSpriteTileTranslucent;
        break;
    }
```

Here the `mode` variable is translated into one of the tile-drawing functions. The selection is stored in `drawfn`. Although {{< lookup/cref name="DRAW_MODE" text="DRAW_MODE_TRANSLUCENT" >}} is implemented, it is never used in the game and might cause visual glitches (see below).

There is no `drawfn` defined for either {{< lookup/cref name="DRAW_MODE" text="DRAW_MODE_HIDDEN" >}} _or_ {{< lookup/cref name="DRAW_MODE" text="DRAW_MODE_FLIPPED" >}} -- these modes will try to call a function address based on stack garbage, leading to a likely crash.

```c
    if (mode != DRAW_MODE_ABSOLUTE && (
        playerPushFrame == PLAYER_HIDDEN ||
        activeTransporter != 0 ||
        playerHurtCooldown % 2 != 0 ||
        blockActionCmds
    )) return;
```

Some special handling is necessary for the player that is not present for any other sprite type. If the draw mode is {{< lookup/cref name="DRAW_MODE" text="DRAW_MODE_ABSOLUTE" >}}, always proceed with drawing. This is generally used in menus, and it would be undesirable for menu decoration to sometimes not appear because of game state. Otherwise, a few conditions could cause an early return, leading to no player being drawn:

* {{< lookup/cref playerPushFrame >}} is set to {{< lookup/cref name="PLAYER" text="PLAYER_HIDDEN" >}}. This happens when the player is interacting with pipe systems.
* {{< lookup/cref activeTransporter >}} is nonzero. This happens when the player is in the process of disappearing in one transporter and reappearing in another.
* {{< lookup/cref playerHurtCooldown >}} is odd. This happens for a short duration after the player has been hurt, and results in the player sprite flashing approximately 20 times.
* {{< lookup/cref blockActionCmds >}} is true. This happens when the player is "removed" from the map, like when interacting with a {{< lookup/actor 152 >}}, {{< lookup/actor type=149 strip=true >}}, {{< lookup/actor 186 >}}, or the {{< lookup/actor type=247 strip=true >}}.

```c
    offset = *playerInfoData + (frame * 4);
    height = *(playerInfoData + offset);
    width = *(playerInfoData + offset + 1);

    y = (y_origin - height) + 1;
    src = playerTileData + *(playerInfoData + offset + 2);
```

As in {{< lookup/cref DrawSprite >}}, the [tile info]({{< relref "tile-info-format" >}}) data stored in {{< lookup/cref playerInfoData >}} is interpreted to find the `offset`, `height`, and `width` of the player sprite image. The initial `y` position is calculated, and `src` is constructed to point to the first byte of the tile's image data in {{< lookup/cref playerTileData >}}.

```c
    if (mode == DRAW_MODE_IN_FRONT) goto infront;
    if (mode == DRAW_MODE_ABSOLUTE) goto absolute;
```

The "in-front" and absolute draw modes are handled elsewhere (below). For all other values of `mode`, execution falls to the following loop.

```c
    for (;;) {
        if (
            x >= scrollX && scrollX + SCROLLW > x &&
            y >= scrollY && scrollY + SCROLLH > y &&
            !TILE_IN_FRONT(MAP_CELL_DATA(x, y))
        ) {
            drawfn(src, (x - scrollX) + 1, (y - scrollY) + 1);
        }

        src += 40;

        if (x == x_origin + width - 1) {
            if (y == y_origin) break;
            x = x_origin;
            y++;
        } else {
            x++;
        }
    }

    return;
```

This (and the subsequent implementations) are the same as {{< lookup/cref DrawSprite >}}.

One interesting detail is the hypothetical situation where `mode` is set to {{< lookup/cref name="DRAW_MODE" text="DRAW_MODE_TRANSLUCENT" >}}: Since translucent drawing involves manipulating the EGA bit mask register, a call to {{< lookup/cref EGA_BIT_MASK_DEFAULT >}} would be necessary to restore the bit mask after player drawing is complete, which is not done here. When a subsequent sprite tile is drawn, it will (unintentionally) inherit the bit mask of the last player tile drawn, causing unwanted vertical strips of transparency in the sprite. Eventually something else will reset the bit mask register, correcting subsequent writes and somewhat limiting the impact of this glitch.

```c
absolute:
    for (;;) {
        DrawSpriteTile(src, x, y);

        src += 40;

        if (x == x_origin + width - 1) {
            if (y == y_origin) break;
            x = x_origin;
            y++;
        } else {
            x++;
        }
    }

    return;
```

This loop handles absolute drawing, placing the player sprite directly onto the screen without considering the position on in the game world.

```c
infront:
    for (;;) {
        if (
            x >= scrollX && scrollX + SCROLLW > x &&
            y >= scrollY && scrollY + SCROLLH > y
        ) {
            drawfn(src, (x - scrollX) + 1, (y - scrollY) + 1);
        }

        src += 40;

        if (x == x_origin + width - 1) {
            if (y == y_origin) break;
            x = x_origin;
            y++;
        } else {
            x++;
        }
    }
}
```

This loop is identical to the "default" case, but without the {{< lookup/cref TILE_IN_FRONT >}} test. This causes the player to be drawn in front of all map tiles, such as when the player becomes dead and floats off the top of the screen.

{{< boilerplate/function-cref IsSpriteVisible >}}

The {{< lookup/cref IsSpriteVisible >}} function returns true if the provided `sprite_type` and `frame` located at `x_origin` and `y_origin` is at least partially visible within the scrolling game window. The return value is true if at least one tile belonging to the sprite is located within the screen boundary (even if that tile does not contain any visible pixels).

```c
bool IsSpriteVisible(
    word sprite_type, word frame, word x_origin, word y_origin
) {
    register word width, height;
    word offset = *(actorInfoData + sprite_type) + (frame * 4);

    height = *(actorInfoData + offset);
    width = *(actorInfoData + offset + 1);

    return (
        (scrollX <= x_origin && scrollX + SCROLLW > x_origin) ||
        (scrollX >= x_origin && x_origin + width > scrollX)
    ) && (
        (
            scrollY + SCROLLH > (y_origin - height) + 1 &&
            scrollY + SCROLLH <= y_origin
        ) || (y_origin >= scrollY && scrollY + SCROLLH > y_origin)
    );
}
```

`sprite_type` and `frame` are interpreted in the same manner as {{< lookup/cref DrawSprite >}} with the ultimate goal of discovering the `height` and `width` of the passed sprite, in tiles.

The actual comparison happens in a big blob of a `return` expression, with the horizontal tests in the first half and the vertical tests following.

Horizontally, when the sprite's `x_origin` is to the right of the screen's left edge ({{< lookup/cref scrollX >}}), that `x_origin` must also be to the left of the screen's right edge ({{< lookup/cref scrollX >}} + {{< lookup/cref SCROLLW >}}) to have any possibility of being on the screen.

When the sprite's `x_origin` is to the left of the screen's left edge ({{< lookup/cref scrollX >}}), the sprite's origin is off the screen but portions of the sprite might still be in view. The sprite's right edge (`x_origin` + `width`) will end up to the right of the screen's left edge if so.

The vertical tests are similar although the order of operations is a bit different. In cases where the sprite's `y_origin` is below the bottom edge of the screen ({{< lookup/cref scrollY >}} + {{< lookup/cref SCROLLH >}}), the sprite may still be partially visible whenever its top row of tiles ([`y_origin` - `height`] + 1) is above the bottom edge of the screen.

When the sprite's `y_origin` is above the bottom edge of the screen ({{< lookup/cref scrollY >}} + {{< lookup/cref SCROLLH >}}), it must also be below or equal to the top row of tiles on the screen ({{< lookup/cref scrollY >}}) to be visible.

If at least one horizontal and one vertical test passes, the sprite is located in a position where it can be seen on the screen and a true value is returned by the function. Otherwise the sprite is too far outside the bounds of the screen to be visible, producing a false return.
