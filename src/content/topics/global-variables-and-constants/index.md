+++
title = "Global Variables and Constants"
description = "Lists and briefly defines all global variables and constants shared between the game's functions."
weight = 330
+++

# Global Variables and Constants

This page contains a listing of every global variable defined in the game, along with the declarations and a brief description of what each one does.

For our purposes, a global variable is anything that is defined outside of a function, whether it is declared `static` (private to its compilation unit) or not. This page also includes `enum`s, `#define`s, and really anything else that seems useful to document.

## Common Types

These are the enumerations and custom types that are frequently used. Generally any variable that holds an unsigned data type will use one of the following:

```c
enum {false = 0, true};
typedef unsigned char byte;   /* 8-bit unsigned integer */
typedef unsigned int  word;   /* 16-bit unsigned integer */
typedef unsigned long dword;  /* 32-bit unsigned integer */
typedef word bool;            /* Boolean stored in a machine word (16-bit) */
typedef byte bbool;           /* Boolean stored in a byte */
```

{{< boilerplate/global-cref CPUTYPE >}}

These are the return values for the {{< lookup/cref GetProcessorType >}} function.

{{< boilerplate/global-cref END_ANIMATION >}}

{{< boilerplate/global-cref END_SCREEN >}}

{{< boilerplate/global-cref FILENAME_BASE >}}

{{< boilerplate/global-cref IMAGE >}}

The names are described in more detail on the [full-screen image database]({{< relref "databases/full-screen-image" >}}) page.

The values for `IMAGE_TILEATTR`, `IMAGE_DEMO`, and `IMAGE_NONE` do not refer to actual files that can be displayed; they are flags placed into {{< lookup/cref miscDataContents >}} to facilitate skipping load operations on data that may already be in memory.

{{< boilerplate/global-cref JOYSTICK >}}

{{< boilerplate/global-cref JoystickState >}}

{{< boilerplate/global-cref MODE1_COLORS >}}

The colors here are based on the Borland {{< lookup/cref COLORS >}} members, with the "light" variants shifted by 8 to compensate for the EGA's color requirements. See {{< lookup/cref SetPaletteRegister >}} for more information about this difference.

{{< boilerplate/global-cref MUSIC >}}

{{< boilerplate/global-cref Music >}}

{{< boilerplate/global-cref PALANIM >}}

{{< boilerplate/global-cref TILE >}}

For space reasons, some of the names are a bit obtuse:

* `TILE_SWITCH_FREE_1N` has **no** ("N") line at its top.
* `TILE_SWITCH_FREE_1L` has a light-colored ("L") line at its top.
* Names that include `EMPTY` or `FREE` do not restrict movement, and essentially behave as "air."
* Names including `PLATFORM` only block movement in the southern direction.
* Names including `BLOCK` are solid, and block movement in all directions.
* Names with a direction indicate that they are meant to be used in conjunction with other, similarly named tiles, and the directions indicate the correct relative position for each tile.

{{< boilerplate/global-cref TITLE_SCREEN >}}

{{< boilerplate/global-cref activeMusic >}}

This is updated whenever {{< lookup/cref StartGameMusic >}} or {{< lookup/cref StartMenuMusic >}} is called, and read whenever the music needs to be restarted -- for instance, after the game is paused and then unpaused.

{{< boilerplate/global-cref activeSoundIndex >}}

{{< boilerplate/global-cref activeSoundPriority >}}

This is checked and updated during calls to {{< lookup/cref StartSound >}}. If the new sound has a priority value that is less than {{< lookup/cref activeSoundPriority >}}, the new sound will not play and the currently-playing sound will continue.

{{< boilerplate/global-cref actorTileData >}}

Its allocations are divided into three distinct byte-aligned memory blocks due to the overall size of the data. The first two blocks each hold 65,535 bytes and the final block holds 60,840 bytes.

{{< boilerplate/global-cref backdropTable >}}

This is also used as scratch storage during calls to {{< lookup/cref DrawFullscreenText >}}.

{{< boilerplate/global-cref cmdBomb >}}

{{< boilerplate/global-cref cmdEast >}}

{{< boilerplate/global-cref cmdJump >}}

{{< boilerplate/global-cref cmdNorth >}}

{{< boilerplate/global-cref cmdSouth >}}

{{< boilerplate/global-cref cmdWest >}}

{{< boilerplate/global-cref demoDataLength >}}

{{< boilerplate/global-cref demoDataPos >}}

{{< boilerplate/global-cref demoState >}}

This variable can hold one of the following values while the game is running:

Symbolic Constant  | Value | Description
-------------------|-------|------------
`DEMOSTATE_NONE`   | 0     | Game is being played interactively, no demo is being recorded or played.
`DEMOSTATE_RECORD` | 1     | Game is being played interactively, and demo data is being recorded from the input.
`DEMOSTATE_PLAY`   | 2     | Game is being controlled by demo data.

When set to `DEMOSTATE_RECORD` or `DEMOSTATE_PLAY`, this suppresses the "Now entering level" message and all in-game hints, and adds a "DEMO" overlay.

{{< boilerplate/global-cref drawPageNumber >}}

{{< boilerplate/global-cref drawPageSegment >}}

{{< boilerplate/global-cref enableAdLib >}}

{{< boilerplate/global-cref enableSpeaker >}}

{{< boilerplate/global-cref fontTileData >}}

{{< boilerplate/global-cref fullscreenImageNames >}}

The values for {{< lookup/cref TITLE_SCREEN >}} and {{< lookup/cref END_SCREEN >}} are different depending on the episode; typically these will be `"TITLEx.MNI"` and `"ENDx.MNI"` (respectively) with `x` matching the episode number.

{{< boilerplate/global-cref gameTickCount >}}

This value is used by various delay functions to produce pauses of a constant length, regardless of processor speed. It is also used to govern the speed of the {{< lookup/cref GameLoop >}} function.

{{< boilerplate/global-cref highScoreNames >}}

The table is arranged in score order, from highest score to lowest.

{{< boilerplate/global-cref highScoreValues >}}

The table is arranged in score order, from highest score to lowest.

{{< boilerplate/global-cref isAdLibPresent >}}

This variable directly mirrors the state of the hardware and cannot be influenced by any in-game setting. This affects the behavior of memory allocation for the {{< lookup/cref tileAttributeData >}} pointer.

{{< boilerplate/global-cref isAdLibPresentPrivate >}}

This is a duplicate (but separately managed) copy of {{< lookup/cref isAdLibPresent >}}. This is used internally by the [AdLib functions]({{< relref "adlib-functions" >}}) only.

{{< boilerplate/global-cref isAdLibServiceRunning >}}

{{< boilerplate/global-cref isAdLibStarted >}}

This variable is managed by {{< lookup/cref StartAdLib >}} and {{< lookup/cref StopAdLib >}} to ensure no attempts are made to start an already-started AdLib card or stop an already-stopped one.

{{< boilerplate/global-cref isDebugMode >}}

This can be toggled while in a game by pressing <kbd>Tab</kbd>+<kbd>F12</kbd>+<kbd>Del</kbd>. It cannot be toggled in the menus.

Debug mode has the following effects:

* In the game, enables the <kbd>F10</kbd>+___ cheat codes.
* In the main menu, adds the ability to press <kbd>F11</kbd> to begin recording a demo.
* At all times, adds the ability to press <kbd>Alt</kbd>+<kbd>C</kbd> to call the system's original keyboard interrupt handler.

{{< boilerplate/global-cref isInGame >}}

This controls whether or not {{< lookup/cref ShowHighScoreTable >}} clears the screen before and after showing.

{{< boilerplate/global-cref isJoystickReady >}}

When true, {{< lookup/cref ProcessGameInput >}} only accepts player movement from the joystick. When false, player movement is only accepted from the keyboard.

Entering the "joystick redefine" menu **and** completing the calibration process sets this value to true. Merely entering the "keyboard redefine" menu sets this value to false.

{{< boilerplate/global-cref isKeyDown >}}

This array is twice as large as it needs to be. Due to the high bit being used as the make/break flag, only 128 keys can actually be encoded by the keyboard controller's input buffer. Elements 128&ndash;255 of this array can never hold true values.

{{< boilerplate/global-cref isMusicEnabled >}}

Music may play when this is true, and music is silenced when false. This setting can be toggled by the user, and the value is persisted in the [configuration file]({{< relref "configuration-file-format" >}}).

{{< boilerplate/global-cref isNewSound >}}

This serves as a communication flag between {{< lookup/cref StartSound >}} and {{< lookup/cref PCSpeakerService >}}.

{{< boilerplate/global-cref isSoundEnabled >}}

Sound effects may play when this is true, and sound effects are silenced when false. This setting can be toggled by the user, and the value is persisted in the [configuration file]({{< relref "configuration-file-format" >}}).

{{< boilerplate/global-cref joinPathBuffer >}}

{{< boilerplate/global-cref joystickBandBottom >}}

{{< boilerplate/global-cref joystickBandLeft >}}

{{< boilerplate/global-cref joystickBandRight >}}

{{< boilerplate/global-cref joystickBandTop >}}

{{< boilerplate/global-cref joystickBtn1Bombs >}}

{{< boilerplate/global-cref lastGroupEntryLength >}}

This value is updated each time {{< lookup/cref GroupEntryFp >}} opens a [group file]({{< relref "group-file-format" >}}) entry.

{{< boilerplate/global-cref lastScancode >}}

In the case of a key down/"make" code, this will be a value in the range 0h&ndash;7Fh. For key up/"break" codes, this will be a value in the range 80h&ndash;FFh. Break codes can be converted into corresponding make codes by taking the value bitwise-AND 7Fh.

In the case of multi-byte scancodes like those added with the 101-key PS/2 keyboard, this will only hold the most recent byte that was received.

{{< boilerplate/global-cref levelNum >}}

This is distinct from the map number -- the level number tracks multiple plays through the bonus maps. The relationship between level and map progression is as follows:

Level Number | Map Number | Notes
-------------|------------|------
0            | 1          |
1            | 2          |
2            | Bonus A    | The warp menu chooses this instance.
3            | Bonus B    | The warp menu chooses this instance.
4            | 3          |
5            | 4          |
6            | Bonus A    |
7            | Bonus B    |
8            | 5          |
9            | 6          |
10           | Bonus A    |
11           | Bonus B    |
12           | 7          |
13           | 8          |
14           | Bonus A    |
15           | Bonus B    |
16           | 9          |
17           | 10         |
18           | Bonus A    |
19           | Bonus B    |
20           | 11         | Only present in episode 1.
21           | 12         | Supported; never used.
22           | Bonus A    |
23           | Bonus B    |
24           | 13         | Supported; never used.
25           | 14         | Supported; never used.
26           | Bonus A    |
27           | Bonus B    |
28           | 15         | Supported; never used.
29           | 16         | Not supported; implementation incomplete.

{{< boilerplate/global-cref mapData >}}

Maps are interpreted as word-aligned data, and temporary data is byte-aligned. This temporary data consists of [masked tile image data]({{< relref "tile-image-format#masked-tiles" >}}) for cartoons and scratch storage needed during the loading of backdrop images.

{{< boilerplate/global-cref maskedTileData >}}

{{< boilerplate/global-cref miscData >}}

Outside of gameplay, this is used as a temporary buffer while copying [full-screen image data]({{< relref "full-screen-image-format" >}}) into EGA memory.

When switching levels, this is used as scratch storage during the loading of backdrop images.

During gameplay, the first 5,000 bytes of this block are used to hold any [demo data]({{< relref "demo-format" >}}) that is being played or recorded. The remainder of the block is used to hold [music data]({{< relref "adlib-music-format" >}}) for the level if there is an AdLib card installed, **or** [tile attributes data]({{< relref "tile-attributes-format" >}}) if there is not an AdLib card installed. (See {{< lookup/cref tileAttributeData >}}.)

{{< boilerplate/global-cref miscDataContents >}}

When functions modify the contents of the {{< lookup/cref miscData >}} memory block, they also update this value with one of the {{< lookup/cref IMAGE >}} values to indicate what has been written there. This value is then used during {{< lookup/cref DrawFullscreenImage >}} to skip loading in cases where {{< lookup/cref miscData >}} already contains the image content that is going to be drawn.

{{< boilerplate/global-cref musicDataHead >}}

{{< boilerplate/global-cref musicDataLeft >}}

{{< boilerplate/global-cref musicDataLength >}}

{{< boilerplate/global-cref musicDataPtr >}}

{{< boilerplate/global-cref musicNames >}}

Each array index matches with a {{< lookup/cref MUSIC >}} constant.

{{< boilerplate/global-cref musicNextDue >}}

{{< boilerplate/global-cref musicTickCount >}}

{{< boilerplate/global-cref paletteAnimationNum >}}

{{< boilerplate/global-cref paletteStepCount >}}

Once the end of the palette table has been reached (as indicated by encountering an {{< lookup/cref END_ANIMATION >}} marker) this resets to 0 and the pattern repeats.

{{< boilerplate/global-cref pit0Value >}}

This is modified during calls to {{< lookup/cref SetPIT0Value >}}, and takes the `value` that is passed during each call. It is treated as a 16-bit value in all contexts where it appears.

{{< boilerplate/global-cref playerTileData >}}

This block is used to hold the [masked tile image data]({{< relref "tile-image-format#masked-tiles" >}}) that the player's sprites are built from.

{{< boilerplate/global-cref profCountCPU >}}

This is updated when the {{< lookup/cref ProfileCPUService >}} function runs, and interpreted during calculations in {{< lookup/cref ProfileCPU >}}.

{{< boilerplate/global-cref profCountPIT >}}

This is updated when the {{< lookup/cref ProfileCPUService >}} function runs, and interpreted during calculations in {{< lookup/cref ProfileCPU >}}. It is read during {{< lookup/cref WaitWallclock >}}, but the actual value is irrelevant in that particular function.

{{< boilerplate/global-cref savedInt8 >}}

This function was the system timer interrupt handler when the program was started.

{{< boilerplate/global-cref savedInt9 >}}

This function was the keyboard handler when the program was started.

{{< boilerplate/global-cref scancodeBomb >}}

This setting can be configured by the user in the "keyboard redefine" menu, and the value is persisted in the [configuration file]({{< relref "configuration-file-format" >}}).

{{< boilerplate/global-cref scancodeEast >}}

This setting can be configured by the user in the "keyboard redefine" menu, and the value is persisted in the [configuration file]({{< relref "configuration-file-format" >}}).

{{< boilerplate/global-cref scancodeJump >}}

This setting can be configured by the user in the "keyboard redefine" menu, and the value is persisted in the [configuration file]({{< relref "configuration-file-format" >}}).

{{< boilerplate/global-cref scancodeNorth >}}

This setting can be configured by the user in the "keyboard redefine" menu, and the value is persisted in the [configuration file]({{< relref "configuration-file-format" >}}).

{{< boilerplate/global-cref scancodeSouth >}}

This setting can be configured by the user in the "keyboard redefine" menu, and the value is persisted in the [configuration file]({{< relref "configuration-file-format" >}}).

{{< boilerplate/global-cref scancodeWest >}}

This setting can be configured by the user in the "keyboard redefine" menu, and the value is persisted in the [configuration file]({{< relref "configuration-file-format" >}}).

{{< boilerplate/global-cref skipDetectAdLib >}}

If the feature were implemented, it would suppress only the first (of two) AdLib detection attempts and the assignment of its return value to {{< lookup/cref isAdLibPresentPrivate >}}.

{{< boilerplate/global-cref soundData1 >}}

This pointer is used for initial allocation and loading of this [PC speaker sound data]({{< relref "pc-speaker-sound-format" >}}). Once loaded, the {{< lookup/cref soundDataPtr >}} array is used to address sound data and this variable is no longer necessary.

{{< boilerplate/global-cref soundData2 >}}

See {{< lookup/cref soundData1 >}}.

{{< boilerplate/global-cref soundData3 >}}

See {{< lookup/cref soundData1 >}}.

{{< boilerplate/global-cref soundDataPtr >}}

{{< boilerplate/global-cref soundPriority >}}

{{< boilerplate/global-cref stnGroupFilename >}}

This value adjusts itself based on the value in {{< lookup/cref FILENAME_BASE >}}.

{{< boilerplate/global-cref tileAttributeData >}}

Regardless of the underlying memory location, the data referenced by this pointer is the [tile attributes data]({{< relref "tile-attributes-format" >}}).

{{< boilerplate/global-cref timerTickCount >}}

This value is maintained by {{< lookup/cref TimerInterruptService >}} where its 16-bit treatment causes an overflow at a rate of 18.2 Hz, mimicking the default timer interrupt rate.

{{< boilerplate/global-cref totalMemFreeAfter >}}

This value can be seen in the "Memory free" line in the Memory Usage debug menu.

{{< boilerplate/global-cref totalMemFreeBefore >}}

This value can be seen in the "Take Up" line in the Memory Usage debug menu.

{{< boilerplate/global-cref volGroupFilename >}}

This value adjusts itself based on the value in {{< lookup/cref FILENAME_BASE >}}.

{{< boilerplate/global-cref wallclock10us >}}

This value is calculated in {{< lookup/cref ProfileCPU >}}, and should only be used as an argument to {{< lookup/cref WaitWallclock >}}.

{{< boilerplate/global-cref wallclock25us >}}

This value is calculated in {{< lookup/cref ProfileCPU >}}, and should only be used as an argument to {{< lookup/cref WaitWallclock >}}.

{{< boilerplate/global-cref wallclock100us >}}

This value is calculated in {{< lookup/cref ProfileCPU >}}, and should only be used as an argument to {{< lookup/cref WaitWallclock >}}.

{{< boilerplate/global-cref winLevel >}}

At the start of each level, {{< lookup/cref winLevel >}} is set to false. At the end of each iteration of the game loop, it is checked for a true value -- if anything between these two points sets the value to true, the level is considered to have been won.

{{< lookup/cref winLevel >}} is activated by several actors and the [demo playback/recording]({{< relref "demo-functions#ReadDemoFrame" >}}) functions.

{{< boilerplate/global-cref writePath >}}

The [write path]({{< relref "main-and-outer-loop#write-path" >}}) is usually an empty string, indicating the current working directory. Can also be either an absolute or a relative path, which is used as a prefix when loading/saving the [configuration]({{< relref "configuration-file-format" >}}) and [save]({{< relref "save-file-format" >}}) files.

{{< boilerplate/global-cref yOffsetTable >}}
