+++
title = "Map Drawing Functions"
description = "Describes the functions responsible for drawing the static game world described by the map data."
weight = 420
+++

# Map Drawing Functions

During each frame of gameplay, a rectangular window of [map data]({{< relref "map-format" >}}) is drawn to the video memory. A combination of [solid]({{< relref "tile-image-format#solid-tiles" >}}), [masked]({{< relref "tile-image-format#masked-tiles" >}}), and [backdrop]({{< relref "backdrop-initialization-functions" >}}) tiles are brought together to form the static game world described by the map data. On top of this uninhabited world, the sprites are later drawn.

The screen is built tilewise in horizontal strips drawn left-to-right, with each strip drawn in top to bottom order. Transparent or uncovered areas of the map are filled with the backdrop image selected for the map. All tiles on the screen are fully redrawn during every frame, eliminating all need to erase screen content between calls. [Page flipping]({{< relref "dialog-functions#page-flipping" >}}) is employed after each frame to ensure that a partially-updated screen is never shown to the user.

{{< table-of-contents >}}

## A Window to the World

The game window is 38 &times; 18 tiles in size, maintaining a one-tile blank border around its top, left, and right screen edges. This border remains black simply because nothing during the course of gameplay ever writes any nonzero data at those positions. The top-left tile inside the border is at screen position (1, 1) and reflects the map tile at position ({{< lookup/cref scrollX >}}, {{< lookup/cref scrollY >}}) -- this controls which area of the map is visible as the player navigates through the game world (a world that is nearly 48 times larger than the scrolling window).

{{< image src="game-window-2052x.png"
    alt="Game window position and scrolling variables."
    1x="game-window-684x.png"
    2x="game-window-1368x.png"
    3x="game-window-2052x.png" >}}

{{< lookup/cref scrollX >}} and {{< lookup/cref scrollY >}} are bounded at all times to prevent the scrolling window from showing content outside the bounds of the map data.

{{< boilerplate/function-cref DrawMapRegion >}}

The {{< lookup/cref DrawMapRegion >}} function is called by the [game loop]({{< relref "game-loop-functions" >}}) and draws one complete frame of the static game world to the current draw page. This includes the solid and masked tiles read from the [map data]({{< relref "map-format" >}}) and the scrolling backdrop. The game window (everything except the status bar and the one-tile blank area around the perimeter of the screen) is fully redrawn during each call. This function does not draw any player/actor/decoration/etc. sprites; these will need to be drawn later.

The starting offset in the map data is governed by the {{< lookup/cref scrollX >}} and {{< lookup/cref scrollY >}} values. Changing these values will "pan" the window around the larger map area.

```c
void DrawMapRegion(void)
{
    register word ymap;
    word dstoff = 321;
    word ymapmax;
    word yscreen = 1;
    word *mapcell;
    word bdoff;
    word bdsrc = EGA_OFFSET_BDROP_EVEN - EGA_OFFSET_SOLID_TILES;
```

This function maintains a fair number of long-lived variables:

Variable Name | Description
--------------|------------
`ymap`        | The vertical starting position where map data for the current tile row will be read from. It is an index into the {{< lookup/cref mapData >}} word array; changing the value by {{< lookup/cref mapWidth >}} moves one tile vertically. (Changing this value by _one_ would move the read position _horizontally_ by one tile, but this function does not do that.)
`dstoff`      | The EGA address offset where the solid tiles are drawn into video memory to update the screen contents. Changing this value by one will address the next 8 &times; 1 pixel row horizontally. There are 40 of these across the width of the screen, and each new tile starts vertically on an 8 pixel row boundary. This is initialized to 321 to skip the first row of tiles on the screen (40 pixel rows, times 8 rows in a tile, producing the top border), incremented _again_ to skip past the first tile on the left border.
`ymapmax`     | The stop position for `ymap`. Once this max value is reached, the final row of tiles has been drawn and there is nothing left for this function to do.
`yscreen`     | Tracks the vertical drawing position on the screen, in tiles. This is used when drawing masked tiles, since the relevant drawing functions use a different addressing system than the solid tiles do. This starts at _one_ to reflect the fact that the top row of tiles is skipped for the blank border.
`mapcell`     | Points to the current tile in the source map data, and ultimately controls which solid or masked tile graphic is read for this screen position.
`bdoff`       | Represents the vertical position of the current tile row relative to the game's [backdrop table]({{< relref "backdrop-initialization-functions#backdrop-table" >}}). Each time a row of tiles is completed, this is incremented by 80 to skip one row down in the table.
`bdsrc`       | The EGA address offset where the backdrop image data will be read from. There can be up to four versions of this data, each shifted in 4-pixel steps horizontally and/or vertically, to produce sub-tile scrolling effects. This is initialized to the distance between {{< lookup/cref name="EGA_OFFSET" text="EGA_OFFSET_BDROP_EVEN" >}} and {{< lookup/cref name="EGA_OFFSET" text="EGA_OFFSET_SOLID_TILES" >}}, which is explained below.

```c
    if (hasHScrollBackdrop) {
        if (scrollX % 2 != 0) {
            bdsrc = EGA_OFFSET_BDROP_ODD_X - EGA_OFFSET_SOLID_TILES;
        } else {
            bdsrc = EGA_OFFSET_BDROP_EVEN - EGA_OFFSET_SOLID_TILES;
        }
    }
```

If {{< lookup/cref hasHScrollBackdrop >}} is true, this block executes. This condition indicates that the map requests half-tile horizontal backdrop scrolling, and we will need to switch between two horizontal variants of the backdrop image: one that is unmodified, and another that has been shifted to the left by four pixels. Since every map shipped with the retail game uses horizontal scrolling, this block is never skipped.

The odd case (where {{< lookup/cref scrollX >}}` % 2` is nonzero) is handled first. The constant {{< lookup/cref name="EGA_OFFSET" text="EGA_OFFSET_SOLID_TILES" >}} is subtracted from {{< lookup/cref name="EGA_OFFSET" text="EGA_OFFSET_BDROP_ODD_X" >}}, setting `bdsrc` to the constant value 7980h. This points to the first tile of backdrop image data for the horizontally-shifted variant of the backdrop, expressed in the way that {{< lookup/cref DrawSolidTile >}} expects it.

{{% note %}}This warrants a special callout. {{< lookup/cref DrawSolidTile >}} is usually called to draw solid tiles (hence the name), and biases its indexing such that a source offset of zero targets the first solid tile -- _not_ the first byte of the EGA memory segment. Contrarily, the {{< lookup/cref EGA_OFFSET >}} values _**are**_ relative to the start of the EGA memory segment, necessitating a correction here.{{% /note %}}

In the case where {{< lookup/cref scrollX >}} is even, `bdsrc` is set based on the value of {{< lookup/cref name="EGA_OFFSET" text="EGA_OFFSET_BDROP_EVEN" >}} instead, producing the constant value 6300h. This is the same value previously stored during `bdsrc`'s declaration earlier, making this a redundant assignment.

```c
    if (scrollY > maxScrollY) scrollY = maxScrollY;

    if (hasVScrollBackdrop && (scrollY % 2 != 0)) {
        bdsrc += EGA_OFFSET_BDROP_ODD_Y - EGA_OFFSET_BDROP_EVEN;
    }
```

Next is a bit of guard code. If {{< lookup/cref scrollY >}} managed to exceed the maximum defined in {{< lookup/cref maxScrollY >}}, clamp it to prevent scrolling off the bottom edge of the map. Such an error could influence the vertical background position, so it's handled early here.

If {{< lookup/cref hasVScrollBackdrop >}} is true (the map requests vertical scrolling) and {{< lookup/cref scrollY >}} is odd, the backdrop needs to switch to its vertically-shifted variant.

To make sense of the increment to `bdsrc`, look at the {{< lookup/cref EGA_OFFSET >}} layout of the four backdrop variants:

...BDROP_EVEN | ...BDROP_ODD_X | ...BDROP_ODD_Y | ...BDROP_ODD_XY
--------------|----------------|----------------|----------------
A300h         | B980h          | D000h          | E680h

The distance between {{< lookup/cref name="EGA_OFFSET" text="EGA_OFFSET_BDROP_EVEN" >}} and {{< lookup/cref name="EGA_OFFSET" text="EGA_OFFSET_BDROP_ODD_Y" >}} (2D00h) is the same as the distance between {{< lookup/cref name="EGA_OFFSET" text="EGA_OFFSET_BDROP_ODD_X" >}} and {{< lookup/cref name="EGA_OFFSET" text="EGA_OFFSET_BDROP_ODD_XY" >}} (2D00h). By adding either value to whatever horizontal component `bdsrc` already holds, we change "even" to "odd Y" and change "odd X" to "odd X and Y."

```c
    bdoff =
        (hasVScrollBackdrop ? 80 * ((scrollY / 2) % BACKDROP_HEIGHT) : 0) +
        (hasHScrollBackdrop ?       (scrollX / 2) % BACKDROP_WIDTH   : 0);
```

The other key bit of backdrop preparation is `bdoff`, which will point to a location within the backdrop table. To find the starting position (assuming the relevant scroll flags are enabled), {{< lookup/cref scrollX >}} and {{< lookup/cref scrollY >}} are each halved, and then wrapped modulo the {{< lookup/cref BACKDROP_WIDTH >}} and {{< lookup/cref BACKDROP_HEIGHT >}} respectively. The vertical component is multiplied by 80, which is the size of one row in the backdrop table's data, then the horizontal and vertical components are added together to produce the final value of `bdoff`.

If either {{< lookup/cref hasHScrollBackdrop >}} or {{< lookup/cref hasVScrollBackdrop >}} is false, the relevant component contributes nothing to the value and the backdrop is pinned to the zeroth row and/or column.

This places `bdoff` somewhere inside the 40 &times; 18 quadrant at the top-left of the larger 80 &times; 36 [backdrop table]({{< relref "backdrop-initialization-functions#backdrop-table" >}}). The backdrop table exploits this setup to achieve horizontal and vertical wrapping of the backdrop image with zero additional overhead.

```c
    EGA_MODE_LATCHED_WRITE();

    ymapmax = (scrollY + SCROLLH) << mapYPower;
    ymap = scrollY << mapYPower;
```

This is the final bit of preparation before we can enter the drawing loops. {{< lookup/cref EGA_MODE_LATCHED_WRITE >}} puts the EGA hardware in the appropriate state to draw solid tiles (the source data resides in EGA memory, and by leveraging the latches we can copy four bytes within EGA memory by manipulating a single memory byte with the CPU).

`ymapmax` is set to the sum of {{< lookup/cref scrollY >}} and {{< lookup/cref SCROLLH >}} (this is conceptually the first row of tiles that is obscured by the status bar at the bottom of the screen) and the result is shifted left by {{< lookup/cref mapYPower >}} to turn it into a map cell address. This is mathematically the same as multiplying it by the width of the map in tiles, except this is considerably faster.

`ymap` is calculated similarly, except it refers to the top row of map tiles about to be drawn on the screen.

```c
    do {
        register int x = 0;

        do {
            mapcell = mapData.w + ymap + x + scrollX;

            if (*mapcell < TILE_STRIPED_PLATFORM) {
                DrawSolidTile(bdsrc + backdropTable[bdoff + x], x + dstoff);
            } else if (*mapcell >= TILE_MASKED_0) {
                DrawSolidTile(bdsrc + backdropTable[bdoff + x], x + dstoff);
                DrawMaskedTile(maskedTileData + *mapcell, x + 1, yscreen);
            } else {
                DrawSolidTile(*mapcell, x + dstoff);
            }

            x++;
        } while (x < SCROLLW);

        dstoff += 320;
        yscreen++;
        bdoff += 80;
        ymap += mapWidth;
    } while (ymap < ymapmax);
}
```

This pair of `do`...`while` loops draws the screen. The outer loop runs 18 times in the vertical direction, and the inner loop runs 38 times per row to produce horizontal coverage. At the start of each outer loop iteration, `x` resets to zero. (`x` is explicitly declared using the `register` storage class to influence the compiler's decision-making and match the way the original game was compiled.)

The inner loop works as follows: the **w**ord member of the {{< lookup/cref mapData >}} union is used as a base, to which `ymap`, `x`, and {{< lookup/cref scrollX >}} are added. This makes `mapcell` point to the tile of map data that is going to be drawn at this position on the screen.

Depending on the data read from `*mapcell`, one of three things can happen:

* When `*mapcell` is less than {{< lookup/cref name="TILE" text="TILE_STRIPED_PLATFORM" >}}, the map data should not be drawn. This tile is conceptually "air" or an invisible platform movement marker. In this case, {{< lookup/cref DrawSolidTile >}} is called to fill this position with a tile of backdrop imagery. `bdoff` and `x` are summed to produce an index into {{< lookup/cref backdropTable >}}, which results in an offset that gets added to `bdsrc` to locate the correct source offset in the EGA memory. The destination of this write is the vertical `dstoff` plus the current `x` position.
* When `*mapcell` is equal to or greater than {{< lookup/cref name="TILE" text="TILE_MASKED_0" >}} (which is the boundary between the end of solid tiles and the start of masked tiles), then the game draws one masked tile superimposed on a backdrop tile. It draws the backdrop first, using the exact same approach as the previous bullet. {{< lookup/cref DrawMaskedTile >}} then draws the masked tile over the backdrop that was just drawn by adding `*mapcell`'s value to the {{< lookup/cref maskedTileData >}} base address, and using `x + 1` and `yscreen` as the destination tile coordinates. (`x` needs to be adjusted by one because it counts from zero, while the screen is drawn starting at column one due to the blank border.)
* In the default case, `*mapcell` has a larger value than an air tile, but a smaller value than a masked tile. The solid tiles reside in this range. Drawing them is a simple matter of calling {{< lookup/cref DrawSolidTile >}} with the `*mapcell` value to select the source tile image, and `x + dstoff` to locate the destination EGA offset to write this image to.

At the bottom of the inner loop, `x` is incremented to step one tile to the right in preparation for the next iteration. The loop stops once `x` reaches {{< lookup/cref SCROLLW >}}, indicating that the right edge of the tile row has been reached.

The bottom of the outer loop contains similar bookkeeping. `dstoff` is advanced by 320, which is the size (in EGA address space) of one tile row. (That's 40 tiles, each containing 8 pixel rows, with each pixel row using one byte of address space.) `yscreen` is incremented by one, referring to the next row of tiles. `bdoff` is incremented by 80, which is the size of one data row in the backdrop table. `ymap` is incremented by the current value of {{< lookup/cref mapWidth >}}, which steps to the same horizontal position one tile down in the map data. The loop stops once `ymap` reaches `ymapmax`, indicating that the whole screen has been redrawn.

{{< boilerplate/function-cref DrawRandomEffects >}}

The {{< lookup/cref DrawRandomEffects >}} function is called by the [game loop]({{< relref "game-loop-functions" >}}) and adds random decorative effects to the game world based on what is currently visible on the screen. It applies a sparkling effect to map tiles that have the "slippery" attribute, and adds raindrops (if rain is enabled on the map) in any unoccupied areas at the top edge of the screen.

```c
void DrawRandomEffects(void)
{
    word x = scrollX + random(SCROLLW);
    word y = scrollY + random(SCROLLH);
    word maptile = GetMapTile(x, y);
```

The function starts by defining three variables. `x` selects a random position horizontally along the map, constrained to the area between {{< lookup/cref scrollX >}} and a position {{< lookup/cref SCROLLW >}} tiles to the right. Likewise `y` is a random map position between {{< lookup/cref scrollY >}} and {{< lookup/cref SCROLLH >}} tiles below it. This selects a point somewhere in map space that is currently visible within the scrolling game window.

These coordinates are passed to {{< lookup/cref GetMapTile >}} to read the tile value from the map data. This is stored in `maptile`.

```c
    if (random(2U) != 0 && TILE_SLIPPERY(maptile)) {
        NewDecoration(SPR_SPARKLE_SLIPPERY, 5, x, y, DIR8_NONE, 1);
    }
```

{{< lookup/cref random >}} sets up a 50/50 chance that this block will execute, along with a test for {{< lookup/cref TILE_SLIPPERY >}} on the `maptile` that was chosen earlier. If both conditions are true, {{< lookup/cref NewDecoration >}} is called to add {{< lookup/cref name="SPR" text="SPR_SPARKLE_SLIPPERY" >}} to the map at this (`x`, `y`) position. The sparkle animation consists of five frames, does not move ({{< lookup/cref name="DIR8" text="DIR8_NONE" >}}), and the effect plays only once per call.

Only one position on the map is considered per frame. If the chosen tile is not slippery, no decoration is added during that frame.

```c
    if (hasRain) {
        y = scrollY + 1;

        if (GetMapTile(x, y) == TILE_EMPTY) {
            NewDecoration(SPR_RAINDROP, 1, x, y, DIR8_SOUTHWEST, 20);
        }
    }
}
```

Additionally, if the {{< lookup/cref hasRain >}} flag is true, the map has rain enabled and raindrop decorations should be added to the map.

The `y` position is fudged to the current {{< lookup/cref scrollY >}} position plus one. It is unclear why this addition is done, since it (incorrectly) prevents rain from appearing in the topmost tile row of the game window. The `x` position remains the random horizontal position selected at the top of the function.

{{< lookup/cref GetMapTile >}} returns the tile value at this (`x`, `y`) position, and if it contains {{< lookup/cref name="TILE" text="TILE_EMPTY" >}} then there is empty space at this location -- a raindrop sprite can fit there. {{< lookup/cref NewDecoration >}} is called to add {{< lookup/cref name="SPR" text="SPR_RAINDROP" >}} to the map at this (`x`, `y`) position. The raindrop consists of one frame, always moves in the {{< lookup/cref name="DIR8" text="DIR8_SOUTHWEST" >}} direction, and the decoration persists for a maximum of 20 loops. This is more than enough opportunity for it to reach the bottom of the game window, which is only 18 tiles high.

{{% aside class="fun-fact" %}}
**Umbrellas are futile!**

The physics of rain in this game don't make a lot of sense. Rain will not form where solid tiles occupy the top of the screen, yet existing raindrops will happily pass through any and all solid tiles anywhere below. An solid "umbrella"-type structure would do nothing to shield from the raindrops in this game, unless it happened to occupy the top edge where the raindrops initially spawn.
{{% /aside %}}

There is special-purpose code in {{< lookup/cref MoveAndDrawDecorations >}} that pertains to raindrop movement, causing them to travel faster than any other moving decoration in the game.

{{< boilerplate/function-cref DrawLights >}}

The {{< lookup/cref DrawLights >}} function iterates through all the lights present on the current map and draws any that are currently scrolled into view. If {{< lookup/cref areLightsActive >}} is false, this function does nothing.

Each light is defined _only_ by the upper edges of its cone; the brightening effect floods down in a one tile wide vertical strip from each light actor until it hits a solid map tile or it exceeds the episode's {{< lookup/cref LIGHT_CAST_DISTANCE >}} limit. Lights have a "west" edge, a mirrored "east" edge, and a filled "middle" section directly beneath the light source. Taken together, these three different light types create a triangular area where anything touched by the light becomes brightened. As this modifies content already on the screen, this should be one of the last functions called while drawing a frame -- anything drawn after this function returns will not receive the lighting effect.

{{< image src="light-components-2052x.png"
    alt="Light types, typical construction, and flooding behavior."
    1x="light-components-684x.png"
    2x="light-components-1368x.png"
    3x="light-components-2052x.png" >}}

{{% note %}}Pay special attention to the light fixture in the game screenshot on the left above. It does not contribute to the lighting effect; it is merely an arrangement of four solid map tiles, no different from any other decorative element in the game. Only the lightened gray trapezoidal area is part of the lighting system.{{% /note %}}

A map designer should be mindful of how many lights are present in the level and how many tiles they can cover. (The example image contains 18 lights: eight west, eight east, and two middle types. There is an additional 70 tiles of flooding.) The game must evaluate the full area flooded by _every light on the map_ to determine if any part of the effect enters the scrolling game window. This is recomputed from scratch every frame. Conceivably this would allow for situations like moving platforms dynamically interrupting the flooded area and casting "shadows," but none of the stock maps do this and the result looks unconvincing in practice:

{{< image src="light-platform-interaction-2052x.png"
    alt="Interaction between lights and platforms."
    1x="light-platform-interaction-684x.png"
    2x="light-platform-interaction-1368x.png"
    3x="light-platform-interaction-2052x.png" >}}

The unlit area beneath the platform moves as a shadow would.

```c
void DrawLights(void)
{
    register word i;

    if (!areLightsActive) return;

    EGA_MODE_DEFAULT();
```

The variable `i` is an index used later to iterate through each light present on the current map. The global {{< lookup/cref areLightsActive >}} variable is checked at the beginning to determine if the lights are turned on. If they are not, the value will be false and the function returns early.

Otherwise, the lights are on and we need to draw them. {{< lookup/cref EGA_MODE_DEFAULT >}} resets the EGA hardware into its default state, which disables any latch-copying mode that might be left over from a previous solid tile drawing call.

```c
    for (i = 0; i < numLights; i++) {
        register word y;
        word xorigin, yorigin;
        word side = lights[i].side;

        xorigin = lights[i].x;
        yorigin = lights[i].y;
```

A `for` loop iterates over all of the lights currently present on the map. These are stored sequentially as {{< lookup/cref Light >}} structures in the {{< lookup/cref lights >}} array. {{< lookup/cref numLights >}} controls how many array elements to read. `xorigin` and `yorigin` are set to the (X, Y) tile coordinates on the map where each light has been placed, while `side` holds a value that controls the shape of its top tile. `y` is an iterator variable used later in the vertical flooding loop.

```c
        if (
            xorigin >= scrollX && scrollX + SCROLLW > xorigin &&
            yorigin >= scrollY && scrollY + SCROLLH - 1 >= yorigin
        ) {
            if (side == LIGHT_SIDE_WEST) {
                LightenScreenTileWest(
                    (xorigin - scrollX) + 1, (yorigin - scrollY) + 1
                );
            } else if (side == LIGHT_SIDE_MIDDLE) {
                LightenScreenTile(
                    (xorigin - scrollX) + 1, (yorigin - scrollY) + 1
                );
            } else {
                LightenScreenTileEast(
                    (xorigin - scrollX) + 1, (yorigin - scrollY) + 1
                );
            }
        }
```

This draws the topmost tile on a single vertical strip of light. The outer `if` checks if this tile is scrolled into view by ensuring that `xorigin` is between {{< lookup/cref scrollX >}} and the screen edge {{< lookup/cref SCROLLW >}} tiles to the right. The vertical test is the same, using `yorigin`, {{< lookup/cref scrollY >}}, and {{< lookup/cref SCROLLH >}}, although it chooses to adjust the bottom check by one tile so it can use a greater-or-equal test instead.

If the tile is determined to be within the bounds of the scrolling game window, another `if` block is evaluated. This one decides, based on the value in `side`, which type of light to draw here. {{< lookup/cref name="LIGHT_SIDE" text="LIGHT_SIDE_WEST" >}} results in a call to {{< lookup/cref LightenScreenTileWest >}}, {{< lookup/cref name="LIGHT_SIDE" text="LIGHT_SIDE_MIDDLE" >}} leads to {{< lookup/cref LightenScreenTile >}}, and the default case (logically must be {{< lookup/cref name="LIGHT_SIDE" text="LIGHT_SIDE_EAST" >}}) gets {{< lookup/cref LightenScreenTileEast >}}.

Regardless of the function selected, the arguments passed are the same each time. The screen space X coordinate is determined by subtracting the {{< lookup/cref scrollX >}} position from `xorigin` and adding one to compensate for the one-tile blank border at the left edge of the screen. Y is calculated the same way by taking the distance between `yorigin` and {{< lookup/cref scrollY >}} and correcting for the top border. The screen content at that position is brightened, producing different shapes depending on the specific function that was called.

```c
        for (y = yorigin + 1; yorigin + LIGHT_CAST_DISTANCE > y; y++) {
            if (TILE_BLOCK_SOUTH(GetMapTile(xorigin, y))) break;

            if (
                xorigin >= scrollX && scrollX + SCROLLW > xorigin &&
                y >= scrollY && scrollY + SCROLLH - 1 >= y
            ) {
                LightenScreenTile(
                    (xorigin - scrollX) + 1, (y - scrollY) + 1
                );
            }
        }
    }
}
```

The remainder of the loop body handles the downward flood that occurs under each light, which continues until it hits a blocking map tile or {{< lookup/cref LIGHT_CAST_DISTANCE >}} tiles have been covered. The `for` loop starts the `y` iterator variable at `yorigin` _plus one_ because we start flooding immediately below the tile where the light originated. The loop continues incrementing `y` downward on the screen until one of its exit conditions is reached.

{{% note %}}This loop runs for every strip of every light on the map, no matter what is visible on the screen. This is due to the fact that there are scroll positions where the head tile of the light is not in view, but parts of its flood are.{{% /note %}}

At each step, {{< lookup/cref name="GetMapTile" text="GetMapTile(xorigin, y)" >}} reads the map tile in that position and checks its tile attributes using {{< lookup/cref TILE_BLOCK_SOUTH >}}. If the tile contains an attribute bit that blocks southern movement, the loop `break`s -- the light has reached a solid surface that it should not pass into.

Otherwise, a visibility check occurs. This is identical to the earlier check that was performed on the head tile of the light, but this uses the current value of `y`. If this position is within the scrolling game window, the screen tile is lightened via a call to {{< lookup/cref LightenScreenTile >}} similarly to how the head tile was.

At the conclusion of the flood loop, the outer "per light" loop repeats until all of the lights have been evaluated. Once that's done, the function returns.
