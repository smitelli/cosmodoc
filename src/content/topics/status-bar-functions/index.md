+++
title = "Status Bar Functions"
description = "Describes functions that display the in-game status bar and update the values it holds."
weight = 380
+++

# Status Bar Functions

The game's **status bar** is a 38&times;6 tile region centered at the bottom of the screen, visible while the game is being played. It is built from a static background image onto which the current score, health situation, bombs, and star count are drawn.

The status bar is part of the larger **static game screen** which is a solid black region covering the entire display. When the **game window** is drawn over the static game screen, one tile of black remains along the top, left, and right edges of the screen.

{{< image src="static-game-screen-2052x.png"
    alt="Static game screen and status bar."
    1x="static-game-screen-684x.png"
    2x="static-game-screen-1368x.png"
    3x="static-game-screen-2052x.png" >}}

{{< table-of-contents >}}

The dynamic areas of the status bar are:

* A 7&times;1 tile area for the current score, drawn right-aligned without any leading zeros.
* A 5&times;2 tile health region. Health is represented by a right-aligned series of **health cells** containing green bars. A filled bar represents health the player currently has, and an outlined bar represents health the player could recover by picking up {{< lookup/actor type=28 strip=true plural=true >}}. The game starts with some empty gray space to the left of the cells, which represents additional health capacity the player can unlock up by finding {{< lookup/actor type=82 plural=true >}}.
* A 1&times;1 tile bomb count. This is always a single digit between zero and nine.
* A 2&times;1 tile star count, drawn similarly to the score.

## Source Data

The status bar's background is a [solid tile image]({{< relref "tile-image-format#solid-tiles" >}}) stored in the STATUS.MNI [group file]({{< relref "group-file-format" >}}) entry. The tiles for the status bar are stored sequentially in row-major order (left to right, then top to bottom). During the {{< lookup/cref Startup >}} function near the beginning of the program's execution, this image data is copied to the EGA memory starting at offset 8000h ({{< lookup/cref name="EGA_OFFSET" text="EGA_OFFSET_STATUS_TILES" >}}). The status bar data uses 1,824 bytes of EGA address space.

From the point of view of the processor, the EGA memory begins at segment A000h. Combining the offset and data size, the status bar tiles can be found at memory addresses A000:8000h through A000:871Fh.

## Digit Display

Every number drawn to the status bar comes by way of {{< lookup/cref DrawNumberFlushRight >}}. Such numbers are anchored by their least-significant (rightmost) digit and grow toward the left as the numbers increase and occupy more space.

The numbers in the [game font]({{< relref "databases/font" >}}) are all drawn opaque on a gray background -- the same color gray that the status bar image uses in its placeholders -- so it is not necessary to erase any of the screen contents before drawing an updated number. As long as the character being drawn is a digit between zero and nine, it is guaranteed to fully erase anything behind it.

The health bar images are slightly different because they are drawn one tile at a time using {{< lookup/cref DrawSpriteTile >}} calls, but they too are built from game font glyphs with fully opaque backgrounds.

{{< boilerplate/function-cref ClearGameScreen >}}

The {{< lookup/cref ClearGameScreen >}} function clears all content from both draw pages of the EGA's memory and redraws a fresh status bar. It is a wrapper around {{< lookup/cref DrawStaticGameScreen >}}, which does the actual work.

```c
void ClearGameScreen(void)
{
    SelectDrawPage(0);
    DrawStaticGameScreen();

    SelectDrawPage(1);
    DrawStaticGameScreen();
}
```

The call to {{< lookup/cref DrawStaticGameScreen >}} is responsible for clearing and redrawing the screen, but it only operates on the current draw page. In order to ensure that both pages display identically when activated, this drawing is performed twice with different arguments provided to {{< lookup/cref SelectDrawPage >}} each time.

{{< boilerplate/function-cref DrawStaticGameScreen >}}

The {{< lookup/cref DrawStaticGameScreen >}} function initializes the static components of the game screen by clearing everything from the current draw page and redrawing the status bar on the freshly-cleared screen. The current score, health, bombs, and stars values are drawn onto the status bar in the process.

```c
void DrawStaticGameScreen(void)
{
    word x, y;
    word src = EGA_OFFSET_STATUS_TILES - EGA_OFFSET_SOLID_TILES;
```

There are some quick address gymnastics involved in constructing the `src` offset. This value is ultimately passed to the {{< lookup/cref DRAW_SOLID_TILE_XY >}} macro, which wraps {{< lookup/cref DrawSolidTile >}}. In _there_, the memory address is constructed with a call to {{< lookup/cref MK_FP >}} with A400h as the first argument and the unmodified offset as the second.

Recall that each segment address refers to a 16-byte "paragraph" in memory, while offsets refer to the individual bytes. A segment address of A400h could be expressed as a segment of A000h plus an offset of 4000h and still refer to the same location in memory. It's useful to frame things this way because the EGA's memory space starts at segment A000h, and by using the same segments in all calculations we can omit the segment and focus solely on the offsets.

An offset of 4000h is equivalent to the named constant {{< lookup/cref name="EGA_OFFSET" text="EGA_OFFSET_SOLID_TILES" >}}, which is the starting address of the first solid tile stored in the EGA's memory. {{< lookup/cref DrawSolidTile >}} constructs its addresses relative to this point, so a caller passing zero as the source offset would end up getting the zeroth solid tile in memory. Most of the time, this is what the caller wants.

Here, however, we are doing something novel. Instead of trying to find a specific solid tile by counting a distance from the tile zero, we have an absolute offset {{< lookup/cref name="EGA_OFFSET" text="EGA_OFFSET_STATUS_TILES" >}} that we want to access directly. In order to do that, we have to pre-subtract the {{< lookup/cref name="EGA_OFFSET" text="EGA_OFFSET_SOLID_TILES" >}} that {{< lookup/cref DrawSolidTile >}} is going to add later.

What we end up with is a `src` offset that points _past_ the end of the regular solid tile storage area, to the first byte of the status bar tiles.

```c
    ClearScreen();

    for (y = 19; y < 25; y++) {
        for (x = 1; x < 39; x++) {
            DRAW_SOLID_TILE_XY(src, x, y);
            src += 8;
        }
    }
```

{{< lookup/cref ClearScreen >}} erases the current draw page by filling the entire screen with solid black. Next a pair of nested `for` loops iterates horizontally and vertically over a 38&times;6 area at the bottom of the screen. On each iteration, {{< lookup/cref DRAW_SOLID_TILE_XY >}} copies a single status bar tile between the source area in the EGA's memory to the draw page at tile position `x`,`y`.

The `src` offset is incremented by eight, which is the size of one tile in the EGA's address space. (Each tile is 32 real bytes, but when stored in the EGA's four-plane format it only takes one fourth of that in address bytes.)

When the loops complete, the entire status bar image has been copied onto the screen, but the dynamic areas for the score, etc. are empty.

```c
    AddScore(0);
    UpdateStars();
    UpdateBombs();
    UpdateHealth();
}
```

A series of calls to {{< lookup/cref AddScore >}}, {{< lookup/cref UpdateStars >}}, {{< lookup/cref UpdateBombs >}}, and {{< lookup/cref UpdateHealth >}} finish the job. Each of these functions is responsible for (re)drawing one element of the status bar, filling in all of the blanks with whatever values the global state of the program holds.

{{% note %}}{{< lookup/cref AddScore >}} increments the player's score in the process of redrawing it, so passing zero as the argument has the effect of adding zero points but redrawing regardless.{{% /note %}}

{{< boilerplate/function-cref AddScore >}}

The {{< lookup/cref AddScore >}} function wraps {{< lookup/cref DrawStatusBarScore >}} with the correct X,Y position for display on the screen. It adds `points` to the player's score and updates the status bar with the new value.

```c
void AddScore(dword points)
{
    DrawStatusBarScore(points, 9, 22);
}
```

{{< boilerplate/function-cref DrawStatusBarScore >}}

The {{< lookup/cref DrawStatusBarScore >}} function increments the player's score by `add_points` then updates the score counter in the status bar. Requires `x_origin` and `y_origin` for positioning, which anchors the rightmost (least significant) digit at an absolute tile position on the screen.

```c
void DrawStatusBarScore(dword add_points, word x_origin, word y_origin)
{
    gameScore += add_points;
```

This is admittedly an odd place to modify the global {{< lookup/cref gameScore >}}, but that's how it was done.

```c
    SelectDrawPage(activePage);
    DrawNumberFlushRight(x_origin, y_origin, gameScore);

    SelectDrawPage(!activePage);
    DrawNumberFlushRight(x_origin, y_origin, gameScore);
```

Since the game uses page flipping, there are always two copies of the screen in memory at any given time and they are constantly flip-flopping into view. In order to prevent things from flashing or moving around, both pages must have identical copies of the screen data for anything that is not actively moving. To do this, everything is drawn twice: once on the {{< lookup/cref activePage >}}, and again on the non-active page. (Since the pages are numbered 0 and 1, the `!` operator switches them correctly.)

{{< lookup/cref SelectDrawPage >}} selects the page that should be drawn to -- first the page that is currently being displayed, and second the hidden page that is being redrawn for the next frame of gameplay. On each page, an identical {{< lookup/cref DrawNumberFlushRight >}} call draws the value held in {{< lookup/cref gameScore >}} to the screen location `x_origin`,`y_origin`.

```c
    EGA_MODE_LATCHED_WRITE();
}
```

Before returning, the {{< lookup/cref EGA_MODE_LATCHED_WRITE >}} places the hardware back into latched write mode, which is appropriate for drawing solid tiles. This is arguably the wrong mode to leave the hardware in, because most score changes occur during actor processing and most actor drawing uses transparency masks that require the EGA's default mode. This call does not cause issues, since the other drawing functions set the EGA state appropriately before drawing, but it is a bit of a wasteful call.

{{% aside class="armchair-engineer" %}}
**Or maybe...**

This could have been a vestige of an earlier state of the game's development. Check out {{< lookup/cref DrawStatusBarBombs >}} for a taste of why this might have been something that was thought to be needed at one time or another.
{{% /aside %}}

{{< boilerplate/function-cref UpdateStars >}}

The {{< lookup/cref UpdateStars >}} function wraps {{< lookup/cref DrawStatusBarStars >}} with the correct X,Y position for display on the screen. It refreshes the star count on the status bar with the current global value.

```c
void UpdateStars(void)
{
    DrawStatusBarStars(35, 22);
}
```

{{< boilerplate/function-cref DrawStatusBarStars >}}

The {{< lookup/cref DrawStatusBarStars >}} function updates the "stars" counter in the status bar. Requires `x_origin` and `y_origin` for positioning, which anchors the rightmost (least significant) digit at an absolute tile position on the screen.

```c
void DrawStatusBarStars(word x_origin, word y_origin)
{
    SelectDrawPage(activePage);
    DrawNumberFlushRight(x_origin, y_origin, (word)gameStars);

    SelectDrawPage(!activePage);
    DrawNumberFlushRight(x_origin, y_origin, (word)gameStars);

    EGA_MODE_LATCHED_WRITE();
}
```

This works identically to {{< lookup/cref DrawStatusBarScore >}}, except it does not take an `add_...` parameter or modify any of the game's global variables.

{{< boilerplate/function-cref UpdateBombs >}}

The {{< lookup/cref UpdateBombs >}} function wraps {{< lookup/cref DrawStatusBarBombs >}} with the correct X,Y position for display on the screen. It refreshes the bomb count on the status bar with the current global value.

```c
void UpdateBombs(void)
{
    DrawStatusBarBombs(24, 23);
}
```

{{< boilerplate/function-cref DrawStatusBarBombs >}}

The {{< lookup/cref DrawStatusBarBombs >}} function updates the "bombs" counter in the status bar. Requires `x_origin` and `y_origin` for positioning, which anchors the single digit at an absolute tile position on the screen.

```c
void DrawStatusBarBombs(word x_origin, word y_origin)
{
    EGA_MODE_DEFAULT();

    SelectDrawPage(activePage);
    DrawSpriteTile(fontTileData + FONT_BACKGROUND_GRAY, x_origin, y_origin);
    DrawNumberFlushRight(x_origin, y_origin, playerBombs);

    SelectDrawPage(!activePage);
    DrawSpriteTile(fontTileData + FONT_BACKGROUND_GRAY, x_origin, y_origin);
    DrawNumberFlushRight(x_origin, y_origin, playerBombs);

    EGA_MODE_LATCHED_WRITE();
}
```

This function is reminiscent of {{< lookup/cref DrawStatusBarScore >}} and {{< lookup/cref DrawStatusBarStars >}}, but it does some unnecessary work. At the top, it sets {{< lookup/cref EGA_MODE_DEFAULT >}} to disable the EGA's "latched write" mechanism. This is the correct and necessary mode for the subsequent {{< lookup/cref DrawSpriteTile >}} calls.

The {{< lookup/cref DrawSpriteTile >}} calls, however, are not even necessary. Each of those calls draws a {{< lookup/cref name="FONT" text="FONT_BACKGROUND_GRAY" >}} tile from {{< lookup/cref fontTileData >}} to the `x`,`y` tile position on the screen -- ostensibly to erase the digit that is already there. But as detailed [near the top of this page](#digit-display), the digit characters in the [game font]({{< relref "databases/font" >}}) are fully opaque and the numbers drawn here are fully capable of erasing themselves.

As fruitless as this effort is, it does somewhat explain why this function and its siblings end with the {{< lookup/cref EGA_MODE_LATCHED_WRITE >}} call. In a world where latched write is considered the default state by convention, this function is simply cleaning up after itself. The game may no longer exist in such a world, but remnants of it remain.

{{< boilerplate/function-cref UpdateHealth >}}

The {{< lookup/cref UpdateHealth >}} function wraps {{< lookup/cref DrawSBarHealthHelper >}} and handles draw page selection. It redraws all of the health cells with either filled or empty bars to represent the player's current health.

```c
void UpdateHealth(void)
{
    EGA_MODE_DEFAULT();

    SelectDrawPage(activePage);
    DrawSBarHealthHelper();

    SelectDrawPage(!activePage);
    DrawSBarHealthHelper();
}
```

This function begins with a call to {{< lookup/cref EGA_MODE_DEFAULT >}} to place the EGA hardware in the regular, non-latched write mode. This is in anticipation of eventual calls to {{< lookup/cref DrawSpriteTile >}}, which require the hardware to be in this state to draw tiles with transparency masks.

The rest of this function works similarly to the page-flipping in {{< lookup/cref DrawStatusBarScore >}}, calling {{< lookup/cref DrawSBarHealthHelper >}} identically for each of the two video pages.

{{< boilerplate/function-cref DrawSBarHealthHelper >}}

The {{< lookup/cref DrawSBarHealthHelper >}} function wraps {{< lookup/cref DrawStatusBarHealth >}} with the correct X,Y position for display on the screen.

```c
void DrawSBarHealthHelper(void)
{
    DrawStatusBarHealth(17, 22);
}
```

{{< boilerplate/function-cref DrawStatusBarHealth >}}

The {{< lookup/cref DrawStatusBarHealth >}} function updates the health indicator in the status bar. Requires `x_origin` and `y_origin` for positioning, which anchors the top of the rightmost cell at an absolute tile position on the screen. Each bar image is made out of two distinct font character tiles, stacked vertically. All images are drawn opaque, and the number of cells drawn never decreases during the course of a game, so there are no special tile-erasing considerations needed.

```c
void DrawStatusBarHealth(word x_origin, word y_origin)
{
    word cell;

    for (cell = 0; cell < playerHealthCells; cell++) {
        if (cell >= 8) continue;
```

This function is built from a `for` loop that iterates over the available number of {{< lookup/cref playerHealthCells >}} the player currently has. Initially the player starts the game with three of these cells, but they can increase up to a limit of five by picking up {{< lookup/actor type=82 plural=true >}}. There is no way to decrease {{< lookup/cref playerHealthCells >}} during the course of the game; the only way to accomplish that would be to load a saved game or start a new one. The current cell index is stored in the local `cell` variable.

Immediately inside the loop, a check is made to skip a particular iteration if the current `cell` is equal to or greater than 8. This cannot happen in the game -- {{< lookup/cref playerHealthCells >}} has a maximum value of 5, therefore `cell` can never be greater than 4. This is most likely code that was copied from the original _Duke Nukem_, which had eight health cells:

{{< image src="duke1-screenshot-2052x.png"
    alt="Screenshot of the original Duke Nukem, showing eight health cells."
    1x="duke1-screenshot-684x.png"
    2x="duke1-screenshot-1368x.png"
    3x="duke1-screenshot-2052x.png" >}}

There are some differences in design here: in _Duke_, the health bars disappear instead of becoming unfilled (due to the absence of the {{< lookup/cref playerHealthCells >}} concept), and they increase in left-to-right order. Still, this old check remains even after its raison d'&ecirc;tre has long gone.

```c
        if (playerHealth - 1 > cell) {
            DrawSpriteTile(
                fontTileData + FONT_UPPER_BAR_1,
                x_origin - cell, y_origin
            );
            DrawSpriteTile(
                fontTileData + FONT_LOWER_BAR_1,
                x_origin - cell, y_origin + 1
            );
```

The health of the player, which increases and decrease as damage is taken and recovered from, is tracked in {{< lookup/cref playerHealth >}}. If this value is greater than zero, the player is still considered to be alive. An off-by-one error is introduced by this facet of the game's design: with all of the health bars unfilled, the player is at their lowest possible health count _but they're still alive_. Put another way, the game starts with {{< lookup/cref playerHealthCells >}} set to 3, but with {{< lookup/cref playerHealth >}} set to 4.

Because the player always has one more unit of health than the number of filled bars, {{< lookup/cref playerHealth >}} must be decremented by one to make the comparison with `cell` meaningful. If, after this adjustment, the player has more health available then the cell that is currently being drawn, the cell should be drawn as a full health bar.

{{< lookup/cref DrawSpriteTile >}} does this drawing. Each bar is built from two separate [game font]({{< relref "databases/font" >}}) characters: {{< lookup/cref name="FONT" text="FONT_UPPER_BAR_1" >}} drawn at the passed `y_origin` position and {{< lookup/cref name="FONT" text="FONT_LOWER_BAR_1" >}} one tile lower at `y_origin + 1`. The horizontal position is based on the passed `x_origin` position, moving farther to the left as the loop increments `cell`.

```c
        } else {
            DrawSpriteTile(
                fontTileData + FONT_UPPER_BAR_0,
                x_origin - cell, y_origin
            );
            DrawSpriteTile(
                fontTileData + FONT_LOWER_BAR_0,
                x_origin - cell, y_origin + 1
            );
        }
    }
}
```

In the opposite case, the player does not have enough health to draw this cell as a filled bar. The code works the same as the other branch, except here the font characters are {{< lookup/cref name="FONT" text="FONT_UPPER_BAR_0" >}} and {{< lookup/cref name="FONT" text="FONT_LOWER_BAR_0" >}} to draw unfilled bars instead.
