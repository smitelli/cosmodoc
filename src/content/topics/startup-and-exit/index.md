+++
title = "Startup and Exit"
description = "An exploration of the startup, exit, and long-lived variables of the game."
weight = 220
+++

# Startup and Exit

{{< table-of-contents >}}

There are two closely related functions in the game: {{< lookup/cref Startup >}} and {{< lookup/cref ExitClean >}}. The former sets up the hardware and long-lived global variables necessary to run the game, and the latter resets the hardware and cleans up.

{{< lookup/cref Startup >}} runs exactly once, right as the game first loads. {{< lookup/cref ExitClean >}} also runs once, right before control returns back to DOS.

{{< boilerplate/function-cref Startup >}}

The game starts with a bang. There are number of assets that need to be loaded and pieces of hardware that need to be reconfigured before anything can be drawn to the screen. All of that occurs in this function, which makes it a little unwieldy.

```c
void Startup(void)
{
    SetVideoMode(0x0d);
    StartAdLib();
    ValidateSystem();
    totalMemFreeBefore = coreleft();
```

First and foremost, a call to {{< lookup/cref SetVideoMode >}} attempts to set the graphics adapter to mode Dh. This is an EGA graphics mode supporting 16 colors at 320x200 resolution.

{{< lookup/cref StartAdLib >}} detects an AdLib music card, and if one is present, initializes it. This also installs the timer interrupt service, which serves as the basis for AdLib/PC speaker output and game timekeeping.

{{< lookup/cref ValidateSystem >}} verifies that the EGA adapter accepted the change to mode Dh, and checks that there is enough unused memory available to allocate space for everything that will be needed.

{{< lookup/cref totalMemFreeBefore >}} is a doubleword value, recording the amount of unused memory at this point in the startup procedure. The nonstandard {{< lookup/cref coreleft >}} library function provides this functionality.

```c
    disable();

    savedInt9 = getvect(9);
    setvect(9, KeyboardInterruptService);

    enableSpeaker = false;
    activeSoundPriority = 0;
    gameTickCount = 0;
    isSoundEnabled = true;

    enable();
```

Interrupts are temporarily turned off with the {{< lookup/cref disable >}} function. This ensures that nothing fires while interrupt handlers are being reconfigured.

{{< lookup/cref getvect >}} and {{< lookup/cref setvect >}} are used to swap out the interrupt service routine for interrupt vector 9 -- the PC uses this interrupt for keyboard events. A pointer to the original handler is stashed in {{< lookup/cref savedInt9 >}} and {{< lookup/cref KeyboardInterruptService >}} becomes the new interrupt handler for keyboard events.

The PC speaker service uses a few global variables that maintain state for sound playback and game timekeeping, which are set to initial values. {{< lookup/cref isSoundEnabled >}} defaults on, enabling PC speaker sound effects, although it may be turned off again once the configuration file is loaded.

Interrupts are then restored with the {{< lookup/cref enable >}} function.

```c
    miscData = malloc(35000U);
    DrawFullscreenImage(IMAGE_PRETITLE);
    WaitSoft(200);
```

Here we approach the first point in the program's execution where the user actually gets to see anything displayed on the screen.

{{< lookup/cref miscData >}} points to a freshly-{{< lookup/cref malloc >}}'d 35,000 byte memory block, and can be used for a number of different things at different times. It can hold demo data, music, or bits of graphics. At this point in the program's lifecycle, {{< lookup/cref DrawFullscreenImage >}} is going to require a 32,000 byte scratch area, which {{< lookup/cref miscData >}} provides.

The call to {{< lookup/cref DrawFullscreenImage >}} draws the pre-title image ({{< lookup/cref name="IMAGE" text="IMAGE_PRETITLE" >}}) to the screen and fades it in.

{{< lookup/cref WaitSoft >}} pauses execution for 200 ticks, which can be skipped by pressing any key. Note that this doesn't immediately dismiss the pre-title image -- all of the allocation and load operations below still need to execute before that can happen.

```c
    LoadConfigurationData(JoinPath(writePath, FILENAME_BASE ".CFG"));
    SetBorderColorRegister(MODE1_BLACK);
    InitializeBackdropTable();
    maskedTileData = malloc(40000U);
```

{{< lookup/cref JoinPath >}} is used to combine {{< lookup/cref writePath >}} with the [configuration file]({{< relref "configuration-file-format" >}}) name. The configuration file name is based on the episode-specific {{< lookup/cref FILENAME_BASE >}} value and takes the final form `COSMOx.CFG`. The [write path]({{< relref "main-and-outer-loop#write-path" >}}) is generally an empty string, indicating the current working directory, but it could be set to any arbitrary location via a command line argument.

{{< lookup/cref LoadConfigurationData >}} loads the values in the named configuration file and updates the global game state variables.

{{< lookup/cref SetBorderColorRegister >}} is a bit out of place here. Although it's not often recreated in modern emulations, CRT displays had a blank area around the perimeter of the screen where pixel data could not be drawn. The graphics adapter could fill it with a solid color, however, and that is what this function controls. {{< lookup/cref name="MODE1_COLORS" text="MODE1_BLACK" >}} is the default color, so most of the time this has no visible effect. Also, this probably should've been done before the pre-title image was shown.

{{< lookup/cref InitializeBackdropTable >}} creates a lookup table used when drawing the parallax scrolling backdrop images during gameplay.

{{< lookup/cref maskedTileData >}} points to a new 40,000 byte memory block used to store map tile images that have transparency. It can also be used to hold menu music depending on the context. This is as good a place as any to allocate it.

```c
    soundData1 = malloc((word)GroupEntryLength("SOUNDS.MNI"));
    soundData2 = malloc((word)GroupEntryLength("SOUNDS2.MNI"));
    soundData3 = malloc((word)GroupEntryLength("SOUNDS3.MNI"));

    LoadSoundData("SOUNDS.MNI",  soundData1, 0);
    LoadSoundData("SOUNDS2.MNI", soundData2, 23);
    LoadSoundData("SOUNDS3.MNI", soundData3, 46);
```

Next the [PC speaker sound effect data]({{< relref "pc-speaker-sound-format" >}}) is loaded. The data is split across three [group file]({{< relref "group-file-format" >}}) entries, with each entry containing 23 sound effects.

{{< lookup/cref GroupEntryLength >}} returns the number of bytes needed to hold each file, and that amount is allocated in three separate {{< lookup/cref malloc >}} calls with pointers in {{< lookup/cref name="soundData1" text="soundDataX" >}}. There are no memory access shenanigans occurring here -- there is no requirement that the allocations be contiguous in memory or that they appear in any specific order.

{{< lookup/cref LoadSoundData >}} reads the data from SOUNDSx.MNI into the passed {{< lookup/cref name="soundData1" text="soundDataX" >}} pointer. The number at the end is a skip value -- as the table of sound effects is being constructed, the skip value is used to append the new sound effects without overwriting the sounds that are already present. As each file contains 23 sound effects, the skip value increments by 23 in each call.

```c
    playerTileData = malloc((word)GroupEntryLength("PLAYERS.MNI"));
    mapData.b = malloc(WORD_MAX);
```

More memory allocations occur here. {{< lookup/cref playerTileData >}} is given a memory block with enough space to hold the data in PLAYERS.MNI. This will eventually hold the [masked tile images]({{< relref "tile-image-format#masked-tiles" >}}) for the player character.

{{< lookup/cref mapData >}} is a 65,535 byte block that holds the grid of map tiles used by whichever level is currently being played. This grid represents the navigable areas of [map files]({{< relref "map-format" >}}), but not the level flags or actors. {{< lookup/cref mapData >}} is declared as a union, with `b` referring to bytes and `w` to words. This dual nature is necessary because, at times, this area can be used as a temporary area to load byte-aligned graphics data. When using map data, however, the data is word-aligned.

```c
    /*
    Each actor data block is limited to 65,535 bytes, the first two blocks
    are full, and the last one gets the low word remander plus the two bytes
    that didn't fit into the first two blocks.
    */
    actorTileData[0] = malloc(WORD_MAX);
    actorTileData[1] = malloc(WORD_MAX);
    actorTileData[2] = malloc((word)GroupEntryLength("ACTORS.MNI") + 2);
```

{{< lookup/cref actorTileData >}} is a three-element array of byte pointers, with each allocated block holding sprite tile images for actors, decorations, and other dynamic elements of the game world. These pointers _are_ arranged contiguously in memory, and there _are_ memory access shenanigans happening here.

Due to the segmented nature of memory on the IBM PC, {{< lookup/cref malloc >}} cannot allocate a block of memory larger than 65,535 bytes. (It _is_ possible to do so using {{< lookup/cref farmalloc >}}, but the game chose not to do this.) ACTORS.MNI is 191,910 bytes long, which needs three of these blocks to fully hold. {{< lookup/cref name="actorTileData" text="actorTileData[0]" >}} and {{< lookup/cref name="actorTileData" text="actorTileData[1]" >}} are filled, and {{< lookup/cref name="actorTileData" text="actorTileData[2]" >}} holds the rest.

"The rest" is handled about as unsafely as you might expect. This function is hard-coded with the assumption that there are two-and-a-bit blocks of 65,535 bytes in ACTORS.MNI. The final partial block size is calculated by truncating the doubleword file size to 16 bits and adding 2.

16-bit truncation is essentially `value % 65536`, but each of the full blocks contains 65,535 bytes -- not 65,536. This is an off-by-one error that compounds for each block that precedes the final one. The addition of 2 corrects for this by including the missing byte from each of the previous allocations.

{{< aside class="armchair-engineer" >}}
**Good luck with that.**

Have fun making a total conversion that significantly changes the size or arrangement of the graphics data.
{{< /aside >}}

When accessing actor sprite data, this arrangement recreates a form of segment:offset addressing. `actorTileData[seg] + off` will point to the data for `seg:off`, which is how actor sprite offsets are stored in the [tile info]({{< relref "tile-info-format" >}}) files.

```c
    LoadGroupEntryData("STATUS.MNI", actorTileData[0], 7296);
    CopyTilesToEGA(actorTileData[0], 7296 / 4, EGA_OFFSET_STATUS_TILES);

    LoadGroupEntryData("TILES.MNI", actorTileData[0], 64000U);
    CopyTilesToEGA(actorTileData[0], 64000U / 4, EGA_OFFSET_SOLID_TILES);
```

The brand-new allocation for {{< lookup/cref actorTileData >}} is immediately sullied by using it as a temporary storage area for the [solid tile image data]({{< relref "tile-image-format#solid-tiles" >}}) that makes up the status bar and some portions of the maps.

Instead of using {{< lookup/cref GroupEntryLength >}}, the file sizes are hard-coded: 7,296 bytes for the status bar (STATUS.MNI) and 64,000 bytes for the map tiles (TILES.MNI). Each {{< lookup/cref LoadGroupEntryData >}} call temporarily copies the full file contents into {{< lookup/cref name="actorTileData" text="actorTileData[0]" >}}, but this is not where they stay.

The EGA adapter contains onboard memory that is separate from the system's RAM. EGA memory offsets 0h and 2000h are used for the game's two display pages, but offsets starting at 4000h are unused. They could have been used to hold additional display pages, but the game instead uses this memory to hold graphics data.

{{< lookup/cref CopyTilesToEGA >}} copies data from system memory into EGA memory. It takes three arguments: the source pointer, a length, and a destination offset. The division by 4 in the length argument is a consequence of the EGA's hardware design: Each memory offset actually references one location multiplied across four distinct planes of memory. This is also why there is only 16 KiB of address space between the offsets for {{< lookup/cref name="EGA_OFFSET" text="EGA_OFFSET_SOLID_TILES" >}} (4000h) and {{< lookup/cref name="EGA_OFFSET" text="EGA_OFFSET_STATUS_TILES" >}} (8000h), yet we are able to load almost 64 KiB of tile data there.

The end result of this operation is that 64,000 bytes of map tiles are loaded at EGA memory offset {{< lookup/cref name="EGA_OFFSET" text="EGA_OFFSET_SOLID_TILES" >}}, and 7,296 bytes of status bar graphics are loaded at offset {{< lookup/cref name="EGA_OFFSET" text="EGA_OFFSET_STATUS_TILES" >}}. The data in {{< lookup/cref name="actorTileData" text="actorTileData[0]" >}} is no longer needed and can be overwritten.

```c
    LoadActorTileData("ACTORS.MNI");
```

{{< lookup/cref LoadActorTileData >}} loads all the elements of {{< lookup/cref actorTileData >}} with the real actor [masked tile image data]({{< relref "tile-image-format#masked-tiles" >}}).

```c
    LoadGroupEntryData(
        "PLAYERS.MNI", playerTileData,
        (word)GroupEntryLength("PLAYERS.MNI")
    );

    actorInfoData = malloc((word)GroupEntryLength("ACTRINFO.MNI"));
    LoadInfoData(
        "ACTRINFO.MNI", actorInfoData,
        (word)GroupEntryLength("ACTRINFO.MNI")
    );

    playerInfoData = malloc((word)GroupEntryLength("PLYRINFO.MNI"));
    LoadInfoData(
        "PLYRINFO.MNI", playerInfoData,
        (word)GroupEntryLength("PLYRINFO.MNI")
    );

    cartoonInfoData = malloc((word)GroupEntryLength("CARTINFO.MNI"));
    LoadInfoData(
        "CARTINFO.MNI", cartoonInfoData,
        (word)GroupEntryLength("CARTINFO.MNI")
    );
```

More loading occurs. {{< lookup/cref playerTileData >}} was allocated earlier, but everything else follows the same basic pattern: Measure the size of the data with {{< lookup/cref GroupEntryLength >}}, allocate that amount of space, then use either {{< lookup/cref LoadGroupEntryData >}} or {{< lookup/cref LoadInfoData >}} to fill that allocation with the data.

This loads the player sprite [masked tile image data]({{< relref "tile-image-format#masked-tiles" >}}), followed by the actor [tile info data]({{< relref "tile-info-format" >}}), player tile info, and cartoon tile info. These initialize {{< lookup/cref actorInfoData >}}, {{< lookup/cref playerInfoData >}}, and {{< lookup/cref cartoonInfoData >}}.

{{< lookup/cref LoadGroupEntryData >}} and {{< lookup/cref LoadInfoData >}} are identical in operation. The only difference is that {{< lookup/cref LoadGroupEntryData >}} takes a byte pointer as its destination argument, while {{< lookup/cref LoadInfoData >}} takes a word pointer.

```c
    fontTileData = malloc(4000);
    LoadFontTileData("FONTS.MNI", fontTileData, 4000);
```

Font [masked tile image data]({{< relref "tile-image-format#masked-tiles" >}}) is loaded into a 4,000 byte allocation pointed to by {{< lookup/cref fontTileData  >}}. {{< lookup/cref LoadFontTileData >}} is a bit unusual because it needs to negate the transparency mask, which is stored inverted compared to all the other tile image files. As before, the file size is hard-coded instead of using {{< lookup/cref GroupEntryLength >}}.

```c
    if (isAdLibPresent) {
        tileAttributeData = malloc(7000);
        LoadTileAttributeData("TILEATTR.MNI");
    }
```

A 7,000 byte block is allocated for {{< lookup/cref tileAttributeData >}} and the allocation is filled by {{< lookup/cref LoadTileAttributeData >}}, but _only if the system contains an AdLib card_ ({{< lookup/cref isAdLibPresent >}}). If the system does not have an AdLib card, this load instead happens during the {{< lookup/cref SwitchLevel >}} function each time a level is entered, where the [tile attributes data]({{< relref "tile-attributes-format" >}}) piggybacks on the {{< lookup/cref miscData >}} block alongside any demo data that might be in use.

Because of this conditional, the memory needs of the game change by 7,000 bytes depending on whether or not an AdLib card is installed. This logic is mirrored in the tests within {{< lookup/cref ValidateSystem >}}.

```c
    totalMemFreeAfter = coreleft();
    ClearScreen();
    ShowCopyright();
    isJoystickReady = false;
}
```

At last, the end of the startup function. Another call to {{< lookup/cref coreleft >}} measures the amount of unused memory after all of the allocations. This is saved in the {{< lookup/cref totalMemFreeAfter >}} doubleword variable.

{{< lookup/cref ClearScreen >}} abruptly clears the pre-title image off the screen, and {{< lookup/cref ShowCopyright >}} replaces it with a window containing the copyright text.

As an afterthought, the {{< lookup/cref isJoystickReady >}} flag is turned off, disabling joystick input until the "joystick redefine" procedure has been completed by the user.

{{< boilerplate/function-cref ValidateSystem >}}

The {{< lookup/cref ValidateSystem >}} function accepts no arguments and returns nothing. It can, however, make the program exit to DOS if the system is not equipped to play the game -- either because of a missing EGA card or due to insufficient free memory.

```c
void ValidateSystem(void)
{
    union REGS x86regs;
    dword bytesfree;

    x86regs.h.ah = 0x0f;
    int86(0x10, &x86regs, &x86regs);
    if (x86regs.h.al != 0x0d) {
        textmode(C80);
        printf("EGA Card not detected!\n");
        /* BUG: AdLib isn't shut down here */
        exit(EXIT_SUCCESS);
    }
```

Earlier in the program's execution, during {{< lookup/cref Startup >}}, the video mode was set to Dh. This test verifies that this mode was actually entered.

Rather than use inline assembly, the {{< lookup/cref int86 >}} function and its closely-related {{< lookup/cref REGS >}} structure are used. Interrupt 10h is the BIOS interrupt handler for video services. Calling this interrupt with the AH register set to Fh issues a request to get the current video mode. BIOS responds to this by placing the video mode number into AL, the width of the screen in text columns into AH, and the active display page number into BH.

The expectation is that the value in AL should be Dh to match the setting we requested earlier during {{< lookup/cref Startup >}}. If this is not true, the only reasonable interpretation is that the system does not contain a graphics adapter that is capable of displaying this mode. This is a fatal condition, so the program has to exit.

{{< lookup/cref textmode >}} returns the display to the standard 80-column color text mode ({{< lookup/cref name="text_modes" text="C80" >}}). {{< lookup/cref printf >}} shows a brief message, and {{< lookup/cref exit >}} returns to DOS. The exit status _should_ be nonzero instead of {{< lookup/cref EXIT_SUCCESS >}}, but this is a DOS game and realistically I doubt anyone has ever cared.

There is a non-obvious bug in this code: When the program exits through this path, {{< lookup/cref StopAdLib >}} is never called and, among other things, interrupt 8 is never restored to the value it had when the program started. This leaves the system in a state where its timer is still firing and triggering execution of program memory that has technically been freed. In DOSBox, at least, this causes the emulation to crash the next time any game tries to manipulate the timer interrupt vector.

Assuming the video mode check passed, execution continues:

```c
    bytesfree = coreleft();

    if (
        ( isAdLibPresent && bytesfree < 383792L + 7000) ||
        (!isAdLibPresent && bytesfree < 383792L)
    ) {
        StopAdLib();
        textmode(C80);
        DrawFullscreenText("NOMEMORY.mni");
        exit(EXIT_SUCCESS);
    }
}
```

The second and final system validation check verifies that there is enough free memory available to allocate all of the required game data. The entire EXE file has already been copied into memory by this point, and DOS has reserved an extra area of memory above that to hold the program's BSS area and stack. The memory being measured here by {{< lookup/cref "coreleft" >}} is what future calls to {{< lookup/cref malloc >}} are going to consume. The game requires 383,792 bytes for these calls, plus 7,000 extra bytes if there is an AdLib card installed ({{< lookup/cref isAdLibPresent >}}), per the logic in {{< lookup/cref Startup >}}.

The values 383,792 and 7,000 are close but not _precisely_ right. Empirically, the real numbers are actually 383,072 and 7,008. And I'll tell you why that is:

{{< lookup/cref Startup >}} makes up to fifteen calls to {{< lookup/cref malloc >}}. Each call for `malloc(size)` really subtracts `((size + 0x17) >> 4) << 4` from the total as reported by {{< lookup/cref coreleft >}} due to bookkeeping and paragraph alignment, so the final values end up being 383,072 and 7,008. This can be verified by checking the difference between "Take Up" and "Memory free" in the Memory Usage debug menu with and without an AdLib card installed.

If the system does not have enough memory, {{< lookup/cref StopAdLib >}} is called to turn off any AdLib hardware and restore hardware state, {{< lookup/cref textmode >}} returns the display to the standard 80-column color text mode ({{< lookup/cref name="text_modes" text="C80" >}}), and {{< lookup/cref DrawFullscreenText >}} displays the NOMEMORY.MNI error message on a large [B800 text]({{< relref "b800-text-format" >}}) screen. Once that's done, {{< lookup/cref exit >}} returns to DOS, once again with {{< lookup/cref EXIT_SUCCESS >}} instead of a more meaningful status.

If both tests pass, {{< lookup/cref ValidateSystem >}} returns silently.

{{< boilerplate/function-cref ExitClean >}}

When it is time to quit the game, something (usually the main menu) calls the {{< lookup/cref ExitClean >}} function. This is responsible for resetting everything that was initialized when the program started and ultimately calling the {{< lookup/cref exit >}} function to ask DOS to terminate execution.

```c
void ExitClean(void)
{
    SaveConfigurationData(JoinPath(writePath, FILENAME_BASE ".CFG"));
```

{{< lookup/cref JoinPath >}} is used to combine {{< lookup/cref writePath >}} with the [configuration file]({{< relref "configuration-file-format" >}}) name, based on the value of {{< lookup/cref FILENAME_BASE >}} for the current episode. {{< lookup/cref SaveConfigurationData >}} saves the values from the global game state variables to the named configuration file. This is the only place this occurs, so if the game crashes or is otherwise exited without using this function, no save occurs.

```c
    disable();
    setvect(9, savedInt9);
    enable();
```

{{< lookup/cref savedInt9 >}} is a pointer to the keyboard interrupt handler that was present when the game started. {{< lookup/cref setvect >}} restores this handler to its rightful place in interrupt vector 9, giving keyboard control back to whatever held it before. This is surrounded by calls to {{< lookup/cref disable >}} and {{< lookup/cref enable >}} to temporarily suspend interrupt handling while the modification is being performed.

```c
    FadeOut();
    textmode(C80);
```

The screen is faded out by {{< lookup/cref FadeOut >}}, and {{< lookup/cref textmode >}} returns the display to the standard 80-column color text mode ({{< lookup/cref name="text_modes" text="C80" >}}).

```c
    outportb(0x0061, inportb(0x0061) & ~0x02);
```

This rather cryptic construction silences the PC speaker.

I/O port 61h addresses the control register for the system's keyboard controller. {{< lookup/cref inportb >}} reads the current state of the register, bit 1 is turned off, and then {{< lookup/cref outportb >}} writes the modified value back into the register. Port 61h, bit 1 controls the "speaker data enable" circuit on the system board. If this bit is off, signals are prevented from reaching the speaker driver. This silences the speaker, regardless of the state of the rest of the hardware involved in speaker control.

```c
    StopAdLib();
```

{{< lookup/cref StopAdLib >}} turns off any AdLib hardware and restores the hardware state to how it was when the program started. Of particular importance is the restoration of interrupt 8, which had been modified to run the game timer.

```c
    remove(FILENAME_BASE ".SVT");
    DrawFullscreenText(EXIT_TEXT_PAGE);
    exit(EXIT_SUCCESS);
}
```

The function ends with an attempt to {{< lookup/cref remove >}} (delete) the temporary [save file]({{< relref "save-file-format" >}}) named {{< lookup/cref FILENAME_BASE >}}.SVT. It is not an error if the file does not exist. This does **not** incorporate {{< lookup/cref writePath >}}, and will not delete the intended file if the [write path]({{< relref "main-and-outer-loop#write-path" >}}) was overridden on the command line.

{{< lookup/cref DrawFullscreenText >}} draws a page of [B800 text]({{< relref "b800-text-format" >}}) to the screen. In this case either the shareware info banner in episode one or the registered game info in episodes two and three.

Finally, {{< lookup/cref exit >}} returns control to DOS with a well-deserved {{< lookup/cref EXIT_SUCCESS >}} status code. Note that none of the allocated memory is explicitly freed -- the program assumes that will happen automatically as the process exits and hands control back to the OS.
