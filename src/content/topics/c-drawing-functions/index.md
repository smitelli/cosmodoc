+++
title = "C Drawing Functions"
description = "Describes the higher-level drawing functions that perform more complicated graphical operations."
weight = 320
+++

# C Drawing Functions

Most of the game's individual tile images are drawn with low-level [assembly drawing functions]({{< relref "assembly-drawing-functions" >}}). Higher-level functions that handle drawing groups of tiles, or larger areas of the screen, are implemented in C.

{{< boilerplate/function-cref CopyTilesToEGA >}}

The {{< lookup/cref CopyTilesToEGA >}} function reads solid tile image data from the memory pointed to by `source`, and installs it into a block of `dest_length` bytes of the EGA's memory starting at `dest_offset`. Because the destination memory is planar, each byte of address space covered by `dest_length` consumes four bytes from `source`.

The behavior of this function is a little strange due to the [planar memory]({{< relref "ega-functions#planar-memory" >}}) of the EGA. Very briefly, each byte of address space from the CPU's perspective maps to a position across four distinct memory planes within the EGA. When the CPU writes a byte to the EGA's address space, this byte can be written to as many as four (and as few as zero) memory planes. The planes are selected by the EGA's **map mask** parameter, which can be configured via writes to the EGA's I/O ports.

In regular memory, each solid tile is 32 bytes long. In the EGA's memory, each tile occupies eight bytes of address space, but these eight bytes must be written four times with a different map mask selected during each pass. Because of this planar nature, `dest_length` should be one-fourth the length of the `source` data -- the destination address range will be written four times (once per plane) to compensate.

```c
void CopyTilesToEGA(byte *source, word dest_length, word dest_offset)
{
    word i;
    word mask;
    byte *src = source;
    byte *dest = MK_FP(0xa000, dest_offset);
```

The pointer provided in `source` is copied to `src` for future use, and a call to {{< lookup/cref MK_FP >}} constructs a pointer from the EGA's base segment address (A000h) and the provided `dest_offset` value.

{{< note >}}EGA memory offsets 0h and 2000h are used for screen pages 0 and 1, respectively. Any data written to these blocks may be overwritten by drawing functions. If the intention is to provide long-term tile storage, `dest_offset` should be at least 4000h.{{< /note >}}

```c
    for (i = 0; i < dest_length; i++) {
        for (mask = 0x0100; mask < 0x1000; mask = mask << 1) {
            outport(0x03c4, mask | 0x0002);

            *(dest + i) = *(src++);
        }
    }
}
```

The actual copy occurs here. The outermost `for` loop governs the total range of destination address space that is written, influenced by `dest_length`.

Inside that, a second `for` loop selects the plane mask to be written. This loop runs four times, generating a `mask` value of 1, 2, 4, and 8 to select the blue, green, red, and intensity planes (respectively). The mask value is stored in the _high_ byte of a 16-bit word to save a shift operation later.

{{< lookup/cref outport >}} sends two I/O bytes in one word-sized operation: Port 3C4h gets byte 2h, and port 3C5h gets the value in `mask`, where only the high byte has significant data. I/O port 3C4h is the EGA's sequencer address register, which specifies the address (2h) that the sequencer's data register should point to. I/O port 3C5h is that data register, and address index 2h refers to the "Map Mask" parameter. This receives the value in `mask`, which has the effect of limiting writes to just the one plane being serviced during this iteration.

The copy itself is straightforward. The byte at `src` is copied to the address `i` bytes above `dest`. This pattern of byte copying is necessary to deinterleave the [solid tile image data]({{< relref "tile-image-format#solid-tiles" >}}) -- which is stored in blue-green-red-intensity byte order -- into the planar format required by the EGA.

The `src` pointer is incremented, and the loops move on to their next iterations.

{{< boilerplate/function-cref ClearScreen >}}

The {{< lookup/cref ClearScreen >}} function overwrites the EGA memory for the current draw page with solid black tiles. The end result of this is a completely blank draw page.

```c
void ClearScreen(void)
{
    word x, y;

    EGA_MODE_LATCHED_WRITE();
```

This function uses {{< lookup/cref DrawSolidTile >}} to perform the low-level drawing of each individual tile, and that function requires the EGA to be placed into latched write mode. The call to the {{< lookup/cref EGA_MODE_LATCHED_WRITE >}} macro achieves this.

```c
    for (y = 0; y < 25 * 320; y += 320) {
        for (x = 0; x < 40; x++) {
            DrawSolidTile(TILE_EMPTY, y + x);
        }
    }
}
```

A pair of nested `for` loops causes drawing to iterate over every row/column combination available on the screen. The game runs in a 320 &times; 200 mode, and each tile drawn is 8 &times; 8. The total number of iterations required to traverse the entire screen is therefore 40 tile-widths in the horizontal direction, and 25 tile-heights vertically.

Due to the layout of the EGA's planar memory, a one-byte change in memory offset results in an eight-pixel (or one-tile) displacement horizontally. Each pixel row of display memory occupies 40 bytes of address space, and an eight-row (or one-tile) vertical displacement requires a 320 byte change in offset. This is why the `x` variable increments by one, while the `y` variable uses increments of 320.

At each tile position on the screen (1,000 in total), a call to {{< lookup/cref DrawSolidTile >}} draws the solid tile image {{< lookup/cref name="TILE" text="TILE_EMPTY" >}}. This is an 8 &times; 8 tile of solid black, which overwrites whatever was present in that position of memory.

Once both loops run to completion, the draw page is blank.

{{< boilerplate/function-cref FadeOutCustom >}}

The {{< lookup/cref FadeOutCustom >}} function "fades" the screen image away by incrementally blanking the EGA's palette to black, one entry at a time, pausing `delay` game ticks between each entry. This function blocks until the fade is complete. Once all 16 palette entries are blanked, the function returns.

When the palette is faded out in this way, the actual image data still exists in memory and can be brought back by restoring the palette to its original configuration. Typically the game will fade the screen out to black, then perform drawing functions to build a new screenful of data out of view, and finally perform a "fade in" to show the newly-drawn content.

```c
void FadeOutCustom(word delay)
{
    int reg;

    for (reg = 0; reg < 16; reg++) {
        WaitHard(delay);
        SetPaletteRegister(reg, MODE1_BLACK);
    }
}
```

This function is simply a `for` loop that iterates over the 16 EGA palette entries, with the current palette index stored in `reg`. During each iteration, {{< lookup/cref WaitHard >}} pauses execution for `delay` game ticks so the user can see the change as it progresses. {{< lookup/cref SetPaletteRegister >}} then sets the palette index `reg` to the color {{< lookup/cref name="MODE1_COLORS" text="MODE1_BLACK" >}}, which immediately blanks any pixels of that color that happen to be on the screen.

Once all 16 palette indexes have been set to black, nothing is visible on the screen and the function returns.

{{< boilerplate/function-cref FadeInCustom >}}

The {{< lookup/cref FadeInCustom >}} function "fades" the screen image into view by rebuilding the EGA's default palette, one entry at a time, pausing `delay` game ticks between each entry. This function blocks until the fade is complete. Once all 16 palette entries are configured, the function returns. The effect of this fade is only apparent if the screen had previously been faded out using {{< lookup/cref FadeOutCustom >}} or a similar palette-blanking function.

```c
void FadeInCustom(word delay)
{
    word reg;
    word skip = 0;

    for (reg = 0; reg < 16; reg++) {
        if (reg == 8) skip = 8;

        SetPaletteRegister(reg, reg + skip);
        WaitHard(delay);
    }
}
```

The essence of this function is a `for` loop that iterates over the 16 EGA palette register entries, with the current register index in `reg`. For each index, the color value is reset to the EGA's [default palette]({{< relref "ega-functions#palettes" >}}) for video mode Dh. In this default palette, indexes 0&ndash;7 should have color values 0&ndash;7, and indexes 8&ndash;15 should have color values _16&ndash;23_. (The linked page explains more about why the palette is constructed this way.) The inclusion of the `skip` value creates the necessary discontinuity.

With a palette index and color value pair in hand, the call to {{< lookup/cref SetPaletteRegister >}} writes the change to the video hardware and the new color becomes visible immediately. {{< lookup/cref WaitHard >}} is then called, pausing execution for `delay` game ticks and allowing time for the effect to be perceived by the user.

The function returns once all 16 palette indexes have been set to their default color values.

{{< boilerplate/function-cref FadeOut >}}

The {{< lookup/cref FadeOut >}} function calls {{< lookup/cref FadeOutCustom >}} with a fixed delay of three game ticks per palette entry. This fade takes about one-third of a second to complete.

```c
void FadeOut(void)
{
    FadeOutCustom(3);
}
```

{{< boilerplate/function-cref FadeIn >}}

The {{< lookup/cref FadeIn >}} function calls {{< lookup/cref FadeInCustom >}} with a fixed delay of three game ticks per palette entry. This fade takes about one-third of a second to complete.

```c
void FadeIn(void)
{
    FadeInCustom(3);
}
```

{{< boilerplate/function-cref FadeToWhite >}}

The {{< lookup/cref FadeToWhite >}} function "fades" the screen image away by incrementally blanking the EGA's palette to white, one entry at a time, pausing `delay` game ticks between each entry. This function blocks until the fade is complete. Once all 16 palette entries are blanked, the function returns.

```c
void FadeToWhite(word delay)
{
    word reg;

    for (reg = 0; reg < 16; reg++) {
        SetPaletteRegister(reg, MODE1_WHITE);
        WaitHard(delay);
    }
}
```

This function is essentially identical to {{< lookup/cref FadeOutCustom >}}, except for the different ordering of {{< lookup/cref SetPaletteRegister >}}/{{< lookup/cref WaitHard >}} and the fact that the color here is {{< lookup/cref name="MODE1_COLORS" text="MODE1_WHITE" >}} instead of black. The behavior is the same, but here the screen is left in a state where it is showing solid white.

The screen can be restored using one of the "fade in" functions.

{{< boilerplate/function-cref DrawFullscreenImage >}}

The {{< lookup/cref DrawFullscreenImage >}} function loads and displays the [full-screen image]({{< relref "full-screen-image-format" >}}) identified by `image_num`, fading the screen contents between what has already been drawn and the new image. If the requested `image_num` is anything other than {{< lookup/cref name="IMAGE" text="IMAGE_TITLE" >}} or {{< lookup/cref name="IMAGE" text="IMAGE_CREDITS" >}}, any playing music is stopped.

`image_num` should be one of the available {{< lookup/cref name="IMAGE" text="IMAGE_*" >}} values.

```c
void DrawFullscreenImage(word image_num)
{
    byte *destbase = MK_FP(0xa000, 0);
```

The `destbase` pointer is set up to point to the beginning of the EGA's memory at address A000:0000 by a call to {{< lookup/cref MK_FP >}}. This is the first byte of screen page 0.

```c
    if (image_num != IMAGE_TITLE && image_num != IMAGE_CREDITS) {
        StopMusic();
    }
```

Typically, this function is called during significant changes to game state (during "scene changes" in a sense). Typically such changes would warrant stopping the music, but not always. If the requested `image_num` is either {{< lookup/cref name="IMAGE" text="IMAGE_TITLE" >}} or {{< lookup/cref name="IMAGE" text="IMAGE_CREDITS" >}}, the game is currently cycling through the title loop and the main menu music should not be interrupted.

Otherwise, {{< lookup/cref StopMusic >}} is called to silence any current music that is playing.

```c
    if (image_num != miscDataContents) {
        FILE *fp = GroupEntryFp(fullscreenImageNames[image_num]);

        miscDataContents = image_num;

        fread(miscData, 32000, 1, fp);
        fclose(fp);
    }
```

This section reads the image data from disk and stores it in the {{< lookup/cref miscData >}} memory block. It is wrapped in a most-recently-used cache check: If {{< lookup/cref miscDataContents >}} matches the value in `image_num`, this data has already been loaded by a previous call and we can skip loading it again.

Otherwise, the {{< lookup/cref fullscreenImageNames >}} array is consulted to translate the numeric `image_num` into a group file entry name. This name is passed to a {{< lookup/cref GroupEntryFp >}} call to locate the data. This is returned in the file stream pointer `fp`. {{< lookup/cref miscDataContents >}} is updated to maintain the most-recently-used cache.

{{< lookup/cref fread >}} loads 32,000 bytes of data from `fp` into {{< lookup/cref miscData >}}. Once this is done, `fp` is closed with {{< lookup/cref fclose >}}.

```c
    EGA_MODE_DEFAULT();
    EGA_BIT_MASK_DEFAULT();
    FadeOut();
    SelectDrawPage(0);
```

With the image data loaded into a staging area in main memory, the EGA hardware is programmed to receive it. {{< lookup/cref EGA_MODE_DEFAULT >}} resets its read and write modes into their default states, reverting any possible changes to these modes that may have occurred during the course of drawing. {{< lookup/cref EGA_BIT_MASK_DEFAULT >}} further normalizes the hardware state by resetting the bit mask, allowing all pixels positions on the screen to be changed.

{{< lookup/cref FadeOut >}} is the first visible effect of this function, which fades the screen contents to black. With the hardware in this state, no changes to the screen contents can be seen -- every combination of memory contents produces a solid black screen.

The call to {{< lookup/cref SelectDrawPage >}} is not important. Normally this is used to influence the behavior of the [assembly drawing functions]({{< relref "assembly-drawing-functions" >}}), but none of them are used here. In this specific case, initializing `destbase` to point directly at segment A000h is what selects page 0 for drawing.

```c
    {
        register word srcbase;
        register int i;
        word mask = 0x0100;

        for (srcbase = 0; srcbase < 32000; srcbase += 8000) {
            outport(0x03c4, 0x0002 | mask);

            for (i = 0; i < 8000; i++) {
                *(destbase + i) = *(miscData + i + srcbase);
            }

            mask <<= 1;
        }
    }
```

Here the image data in main memory is installed into the EGA's display memory. The [full-screen image data]({{< relref "full-screen-image-format" >}}) is stored in screen-planar format: 8,000 bytes of blue pixel data, followed by another 8,000 bytes of green, then red, and finally intensity. The EGA memory is similar, but it only exposes 8,000 bytes of address space -- this must be written four times with differing **map mask** values to target each memory plane in turn. This selection is stored in the high byte of `mask`, which is initialized to 1 to start with the memory plane for blue.

The outer `for` loop controls the base offset in the source data. This runs four times, producing a `srcbase` of 0, 8,000, 16,000, and 24,000. This is the offset to the zeroth byte of source data for the current plane being operated on.

Within each plane, {{< lookup/cref outport >}} is used to program the EGA's map mask value. This is done by writing two bytes with a single word-sized I/O operation: I/O port 3C4h is the EGA's sequencer address register, which specifies the address (2h) that the sequencer's data register should point to. I/O port 3C5h is that data register, and address index 2h refers to the "Map Mask" parameter. This receives the high byte in `mask`, which has the effect of limiting writes to just the one plane being written during this iteration.

The inner `for` loop executes 8,000 times, once for each eight-pixel span on the screen. The source data byte is the {{< lookup/cref miscData >}} memory block, plus the `srcbase` offset to the current plane being read, plus the offset in `i`. The destination data byte is the video memory `destbase` plus the offset in `i`. Copying a byte from the former to the latter writes eight pixels of data for a single memory plane.

Once all pixel positions in the plane have been written, the value in `mask` is shifted one bit position to the left. This prepares a subsequent iteration of the outer `for` loop to operate on the next memory plane in sequence.

```c
    SelectActivePage(0);
    FadeIn();
}
```

{{< lookup/cref SelectActivePage >}} configures the video hardware to show screen page 0. All of the previous operations manipulated page 0, and this ensures the correct page will be sent to the display. The palette is still blanked, so the change does not become visible to the user until {{< lookup/cref FadeIn >}} runs to completion, restoring the palette registers to their normal state.

At this point, the image data has been drawn and is visible, so the function returns.

{{< boilerplate/function-cref AnimatePalette >}}

During each frame of gameplay, {{< lookup/cref AnimatePalette >}} is called to cycle through any palette animations that have been requested by the map. If palette animation is necessary, this function determines the color to display.

```c
void AnimatePalette(void)
{
    static byte lightningState = 0;

#ifdef EXPLOSION_PALETTE
    if (paletteAnimationNum == PALANIM_EXPLOSIONS) return;
#endif
```

`lightningState` is a private variable that holds the state of the lightning effect, if the map uses it. Since it is declared static, it retains its value between calls.

Episode three of the game has an `EXPLOSION_PALETTE` feature. If requested by the map, the palette is changed in response to explosions that occur during gameplay. If the map's {{< lookup/cref paletteAnimationNum >}} matches {{< lookup/cref name="PALANIM" text="PALANIM_EXPLOSIONS" >}}, this feature is active for the current map. That is handled elsewhere ({{< lookup/cref DrawExplosions >}}), so return early in this case.

```c
    switch (paletteAnimationNum) {
    case PALANIM_LIGHTNING:
        if (lightningState == 2) {
            lightningState = 0;
            SetPaletteRegister(PALETTE_KEY_INDEX, MODE1_DARKGRAY);
        } else if (lightningState == 1) {
            lightningState = 2;
            SetPaletteRegister(PALETTE_KEY_INDEX, MODE1_LIGHTGRAY);
        } else if (rand() < 1500) {
            SetPaletteRegister(PALETTE_KEY_INDEX, MODE1_WHITE);
            StartSound(SND_THUNDER);
            lightningState = 1;
        } else {
            SetPaletteRegister(PALETTE_KEY_INDEX, MODE1_BLACK);
            lightningState = 0;
        }
        break;
```

The remainder of the function is a large `switch` statement that handles each defined {{< lookup/cref paletteAnimationNum >}} value. If the map uses {{< lookup/cref name="PALANIM" text="PALANIM_LIGHTNING" >}}, a random lightning effect is drawn via calls to {{< lookup/cref SetPaletteRegister >}} with accompanying thunder sound effects from {{< lookup/cref StartSound >}}.

The lifecycle of lightning is as follows: Most of the time, `lightningState` is 0 and there is no active lightning occurring. Whenever the system's random number generator satisfies the precondition, the palette key color is set to white and a thunder sound effect is started -- this is `lightningState` 1. On the subsequent frame, the palette key color changes to light gray and `lightningState` becomes 2. During the next frame, the color changes to dark gray and `lightningState` returns to 0. On the next frame, the palette color is cleaned up and the black color is restored.

In terms of implementation, there isn't much to comment on. In Turbo C, {{< lookup/cref rand >}} returns a value between 0 and 32,767, so there is roughly a 1-in-22 chance of a lightning strike on any given idle frame. The `else` block executes during every idle frame and continually rewrites the key color to black.

When this path is taken, the function returns when `break` is reached.

```c
    case PALANIM_R_Y_W:
        {
            static byte rywTable[] = {
                RED, RED, LIGHTRED, LIGHTRED, YELLOW, YELLOW, WHITE, WHITE,
                YELLOW, YELLOW, LIGHTRED, LIGHTRED, END_ANIMATION
            };

            StepPalette(rywTable);
        }
        break;
```

If the map instead uses {{< lookup/cref name="PALANIM" text="PALANIM_R_Y_W" >}}, a much simpler "red-yellow-white" repeating palette animation is needed. The `rywTable[]` array contains a sequence of {{< lookup/cref COLORS >}} values that define the pattern to use. This pattern is terminated with an {{< lookup/cref END_ANIMATION >}} marker to indicate the loop point.

The color pattern is passed to {{< lookup/cref StepPalette >}}, which handles the actual cycling behavior and palette configuration.

As with the lightning animation, the function returns when `break` is reached.

```c
    case PALANIM_R_G_B:
        {
            static byte rgbTable[] = {
                BLACK, BLACK, RED, RED, LIGHTRED, RED, RED,
                BLACK, BLACK, GREEN, GREEN, LIGHTGREEN, GREEN, GREEN,
                BLACK, BLACK, BLUE, BLUE, LIGHTBLUE, BLUE, BLUE,
                END_ANIMATION
            };

            StepPalette(rgbTable);
        }
        break;

    case PALANIM_MONO:
        {
            static byte monoTable[] = {
                BLACK, BLACK, DARKGRAY, LIGHTGRAY, WHITE, LIGHTGRAY,
                DARKGRAY, END_ANIMATION
            };

            StepPalette(monoTable);
        }
        break;

    case PALANIM_W_R_M:
        {
            static byte wrmTable[] = {
                WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, RED, LIGHTMAGENTA,
                END_ANIMATION
            };

            StepPalette(wrmTable);
        }
        break;
    }
}
```

The previous implementation is repeated three more times, for "red-green-blue", monochrome, and "white-red-magenta" color patterns.

In the event that the {{< lookup/cref paletteAnimationNum >}} doesn't match any of the defined `case` labels, this function returns without doing anything.

{{< boilerplate/function-cref StepPalette >}}

If the current map calls for a simple looping palette animation, {{< lookup/cref AnimatePalette >}} calls {{< lookup/cref StepPalette >}} to handle that. During each frame of gameplay, this function steps through the elements of the passed palette table `pal_table` and sets the palette key color accordingly, repeating once the {{< lookup/cref END_ANIMATION >}} marker has been reached. This function expects an array containing one or more {{< lookup/cref COLORS >}} values followed by the end marker.

```c
void StepPalette(byte *pal_table)
{
    paletteStepCount++;
    if (pal_table[(word)paletteStepCount] == END_ANIMATION) {
        paletteStepCount = 0;
    }
```
This function uses the global {{< lookup/cref paletteStepCount >}} variable to keep track of its position within the palette table. For reasons that are not clear, this was originally declared as a 32-bit doubleword, but all operations treat it as a 16-bit word. This cast is made explicit to call attention to the fact and to silence compiler warnings.

{{< lookup/cref paletteStepCount >}} is incremented during each call. If the `pal_table` element at the new position is {{< lookup/cref END_ANIMATION >}}, the count resets to zero.

```c
    SetPaletteRegister(
        PALETTE_KEY_INDEX,
        pal_table[(word)paletteStepCount] < 8 ?
        pal_table[(word)paletteStepCount] :
        pal_table[(word)paletteStepCount] + 8
    );
}
```

The remainder of the function is a simple {{< lookup/cref SetPaletteRegister >}} call to reprogram the key color with the current color from `pal_table`. The ternary operator converts the {{< lookup/cref COLORS >}}-type numbering scheme (0&ndash;15) into the {{< lookup/cref MODE1_COLORS >}} scheme (0&ndash;7; 16&ndash;23) the palette requires.
