+++
title = "Global Variables and Constants"
description = "Lists and briefly defines all global variables and constants shared between the game's functions."
weight = 390
+++

# Global Variables and Constants

This page contains a listing of every global variable defined in the game, along with the declarations and a brief description of what each one does.

For our purposes, a global variable is anything that is defined outside of a function, whether it is declared `static` (private to its compilation unit) or not. This page also includes `enum`s, `#define`s, and really anything else that seems useful to document.

{{< table-of-contents >}}

---

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

{{< boilerplate/global-cref ACT >}}

{{< lookup/cref name="ACT" text="ACT_BASKET_NULL" >}} is a special sentinel value for the spawner functions and cannot be expressed in the map format. {{< lookup/cref name="ACT" text="ACT_STAR_FLOAT" >}} has the value 32 in the [map format]({{< relref "map-format" >}}), and all other actor types follow sequentially.

{{< boilerplate/global-cref CPUTYPE >}}

These are the return values for the {{< lookup/cref GetProcessorType >}} function.

{{< boilerplate/global-cref DEMOSTATE >}}

Symbolic Constant  | Value | Description
-------------------|-------|------------
`DEMOSTATE_NONE`   | 0     | The game is played in the usual way, with user keyboard input controlling the player. All in-game hints and intermission screens are displated.
`DEMOSTATE_RECORD` | 1     | The game is played in demo recording mode. The keyboard controls the player, but the level progression is altered and in-game hints are skipped. All player movement is captured into a demo file on disk.
`DEMOSTATE_PLAY`   | 2     | The game runs in demo playback mode. Keyboard input is ignored (any keypress ends the game) and player movement commands are read from the demo file. Level progression and hint display are altered in the same way as with `DEMOSTATE_RECORD`.

These are the return values for the {{< lookup/cref TitleLoop >}} function.

{{< boilerplate/global-cref DRAWMODE >}}

Symbolic Constant      | Value | Description
-----------------------|-------|------------
`DRAWMODE_NORMAL`      | 0     | Draw the sprite unmodified, with X/Y positions measured relative to the game world. If the map data contains a "draw in front" tiles that intersect the sprite, the map tiles will prevail.
`DRAWMODE_HIDDEN`      | 1     | Do not draw any part of the sprite.
`DRAWMODE_WHITE`       | 2     | Same as `DRAWMODE_NORMAL`, but all opaque pixel positions in the sprite are drawn in bright white.
`DRAWMODE_TRANSLUCENT` | 3     | Same as `DRAWMODE_WHITE`, but the sprite color is translucent.
`DRAWMODE_FLIPPED`     | 4     | Same as `DRAWMODE_NORMAL`, but the sprite is drawn flipped vertically.
`DRAWMODE_IN_FRONT`    | 5     | Same as `DRAWMODE_NORMAL`, but the sprite will cover _all_ map tiles, regardless of their "draw in front" attribute.
`DRAWMODE_ABSOLUTE`    | 6     | Draw the sprite unmodified, with X/Y positions measured relative to the screen. Since there is no relationship to the game world in this mode, "draw in front" attributes from the map (if present) have no effect.

{{< boilerplate/global-cref EGA_OFFSET >}}

{{< boilerplate/global-cref END_ANIMATION >}}

{{< boilerplate/global-cref END_SCREEN >}}

{{< boilerplate/global-cref FILENAME_BASE >}}

{{< boilerplate/global-cref FONT >}}

The [game font]({{< relref "databases/font" >}}) is built from 100 [masked tiles]({{< relref "tile-image-format#masked-tiles" >}}), each beginning on a 40-byte boundary. Only a handful of these tiles are referenced directly in the game code; all other tile offsets are calculated by adding a multiple of 40 to one of the above base values.

{{< boilerplate/global-cref GAME_VERSION >}}

{{< boilerplate/global-cref HELP_MENU >}}

Symbolic Constant    | Value | Description
---------------------|-------|------------
`HELP_MENU_CONTINUE` | 0     | The user did not do anything that would affect the current iteration of the game loop or the state of gameplay as a whole.
`HELP_MENU_RESTART`  | 1     | The user loaded a saved game, and the game loop needs to restart from the beginning with this new state.
`HELP_MENU_QUIT`     | 2     | The user wants to quit the current game, and the game loop needs to stop running.

These are the return values for the {{< lookup/cref ShowHelpMenu >}} function.

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

{{< boilerplate/global-cref PLAYER >}}

Most of these values must be combined with one of the {{< lookup/cref PLAYER_BASE >}} constants to select between the west- and east-facing variants of each frame. The only exceptions are the "dead" and "hidden" values, which are directionless.

{{< boilerplate/global-cref PLAYER_BASE >}}

The values here should be added to one of the {{< lookup/cref PLAYER >}} constants to produce the true frame number for the desired combination.

{{< boilerplate/global-cref POUNCE_HINT >}}

Symbolic Constant    | Value | Description
---------------------|-------|------------
`POUNCE_HINT_UNSEEN` | 0     | The hint has never been shown. If the player is hurt, it is appropriate to show the hint.
`POUNCE_HINT_QUEUED` | 1     | The player has just been hurt, and the hint needs to be shown. The hint message is queued for display when the current frame's drawing is complete.
`POUNCE_HINT_SEEN`   | 2     | The hint has been shown, or the player has demonstrated that they know how to pounce on enemies. All saved games are written with this pounce hint state, so all loaded games will suppress the hint.

{{< boilerplate/global-cref RESTORE_GAME >}}

Symbolic Constant        | Value | Description
-------------------------|-------|------------
`RESTORE_GAME_NOT_FOUND` | 0     | The user chose a valid save slot, but there was no file saved there.
`RESTORE_GAME_SUCCESS`   | 1     | The restore completed successfully and the new game state is ready to play.
`RESTORE_GAME_ABORT`     | 2     | The user aborted the restore procedure, either explicitly by pressing <kbd>Esc</kbd> or implicitly by choosing an invalid save slot.

These are the return values for the {{< lookup/cref PromptRestoreGame >}} function.

{{< boilerplate/global-cref SAVE_SLOT_INDEX >}}

In the official version of the game, the save file template is `"COSMOx.SV "` with `x` having a value between `'1'` and `'3'` depending on the episode. The ninth index of this string is a space character, which is replaced with the save slot character during calls to {{< lookup/cref LoadGameState >}} and {{< lookup/cref SaveGameState >}}.

{{< boilerplate/global-cref SCANCODE >}}

{{< boilerplate/global-cref SCROLLH >}}

{{< boilerplate/global-cref SCROLLW >}}

{{< boilerplate/global-cref SND >}}

These constants should be passed to {{< lookup/cref StartSound >}} to start playing a [PC speaker sound effect]({{< relref "pc-speaker-sound-format" >}}). Each sound number is described in more detail on the [sound database]({{< relref "databases/sound" >}}) page.

{{< boilerplate/global-cref TILE >}}

For space reasons, some of the names are a bit obtuse:

* `TILE_SWITCH_FREE_1N` has **no** ("N") line at its top.
* `TILE_SWITCH_FREE_1L` has a **light**-colored ("L") line at its top.
* Names that include `EMPTY` or `FREE` do not restrict movement, and essentially behave as "air."
* Names including `PLATFORM` only block movement in the southern direction. The player may jump up through them freely, but movement will stop if they land on it from above.
* Names including `BLOCK` are solid, and block movement in all directions.
* Names with a direction indicate that they are meant to be used in conjunction with other, similarly named tiles to draw larger constructions. The directions indicate the correct relative position for each tile.

{{< boilerplate/global-cref TITLE_SCREEN >}}

{{< boilerplate/global-cref activeMusic >}}

This is updated whenever {{< lookup/cref StartGameMusic >}} or {{< lookup/cref StartMenuMusic >}} is called, and read whenever the music needs to be restarted -- for instance, after the game is paused and then unpaused.

This is a {{< lookup/cref Music >}} structure.

{{< boilerplate/global-cref activePage >}}

This is only used during gameplay, where it will usually hold the opposite value that {{< lookup/cref drawPageNumber >}} has.

{{< boilerplate/global-cref activeSoundIndex >}}

{{< boilerplate/global-cref activeSoundPriority >}}

This is checked and updated during calls to {{< lookup/cref StartSound >}}. If the new sound has a priority value that is less than {{< lookup/cref activeSoundPriority >}}, the new sound will not play and the currently-playing sound will continue.

{{< boilerplate/global-cref activeTransporter >}}

This is the identifier of the transporter the player is moving _to_, but the test for this is rather simplistic. For each transporter in the map, if its "to address" data is different from {{< lookup/cref activeTransporter >}}, that transporter is the destination. This limits each map to having two transporters that ping-pong the player between them.

As a special case, a {{< lookup/cref activeTransporter >}} value of 3 will win the level, allowing for one or more {{< lookup/actor type=203 plural=true >}} to be implemented separately from any other transporters on the map.

{{< boilerplate/global-cref actorTileData >}}

Its allocations are divided into three distinct byte-aligned memory blocks due to the overall size of the data. The first two blocks each hold 65,535 bytes and the final block holds 60,840 bytes.

{{< boilerplate/global-cref backdropTable >}}

This is also used as scratch storage during calls to {{< lookup/cref DrawFullscreenText >}}.

{{< boilerplate/global-cref blockActionCmds >}}

This variable takes a true value when the player is "removed" from the map, like when interacting with a {{< lookup/actor 152 >}}, {{< lookup/actor type=149 strip=true >}}, {{< lookup/actor 186 >}}, or the {{< lookup/actor type=247 strip=true >}}.

{{< boilerplate/global-cref cartoonInfoData >}}

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

During gameplay (where double-buffering is used) {{< lookup/cref activePage >}} will usually hold the opposite value, preventing changes from becoming visible on the screen until the pages are flipped.

{{< boilerplate/global-cref drawPageSegment >}}

{{< boilerplate/global-cref enableAdLib >}}

{{< boilerplate/global-cref enableSpeaker >}}

{{< boilerplate/global-cref fontTileData >}}

{{< boilerplate/global-cref fullscreenImageNames >}}

The values for {{< lookup/cref TITLE_SCREEN >}} and {{< lookup/cref END_SCREEN >}} are different depending on the episode; typically these will be `"TITLEx.MNI"` and `"ENDx.MNI"` (respectively) with `x` matching the episode number.

{{< boilerplate/global-cref gameScore >}}

Most events in the game add points to this variable. Its purpose is purely vanity, the only effect is to earn a spot in the high score table at the end of the game. The smallest score value implemented in the game is worth 100 points, and the score should always be a multiple of 50 unless e.g. a save file was manipulated.

The acceptable range of values for this variable is 0&ndash;9,999,999. Numbers with more than seven characters must be avoided, otherwise draw overflow issues will occur in the status bar.

{{< boilerplate/global-cref gameStars >}}

Each star represents a 1,000 point bonus which is added to {{< lookup/cref gameScore >}} during the {{< lookup/cref ShowStarBonus >}} sequence. The star count is reset to zero once the bonus has been added. The star count also influences which bonus levels are entered over the course of the game:

Stars       | Bonus Level
------------|------------
0&ndash;24  | Skipped.
25&ndash;49 | BONUS1 (E1), BONUS3 (E2), or BONUS5 (E3).
&ge;50      | BONUS2 (E1), BONUS4 (E2), or BONUS6 (E3).

The acceptable range of values for this variable is 0&ndash;99. Numbers with two or more characters must be avoided, otherwise draw overflow issues will occur in the status bar.

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

{{< boilerplate/global-cref isCartoonDataLoaded >}}

This is checked by {{< lookup/cref DrawCartoon >}} to determine if the cartoon data needs to be loaded from disk, avoiding an extra disk access if so. The memory area used for cartoon images (or map data) is {{< lookup/cref mapData >}}.

{{< boilerplate/global-cref isDebugMode >}}

This can be toggled while in a game by pressing <kbd>Tab</kbd>+<kbd>F12</kbd>+<kbd>Del</kbd>. It cannot be toggled in the menus.

Debug mode has the following effects:

* In the game, enables the <kbd>F10</kbd>+___ cheat codes.
* In the main menu, adds the ability to press <kbd>F11</kbd> to begin recording a demo.
* At all times, adds the ability to press <kbd>Alt</kbd>+<kbd>C</kbd> to call the system's original keyboard interrupt handler.

{{< boilerplate/global-cref isGodMode >}}

If {{< lookup/cref isDebugMode >}} is true, this can be toggled while in a game by pressing <kbd>F10</kbd>+<kbd>G</kbd>.

God mode makes the player invincible to any damage that would deduct health. The player can still die by falling off bottom of the map.

{{< boilerplate/global-cref isInGame >}}

This controls whether or not {{< lookup/cref ShowHighScoreTable >}} clears the screen before and after showing.

{{< boilerplate/global-cref isJoystickReady >}}

When true, {{< lookup/cref ProcessGameInput >}} only accepts player movement from the joystick. When false, player movement is only accepted from the keyboard.

Entering the "joystick redefine" menu **and** completing the calibration process sets this value to true. Merely entering the "keyboard redefine" menu sets this value to false.

{{< boilerplate/global-cref isKeyDown >}}

This array is twice as large as it needs to be. Due to the high bit being used as the make/break flag, only 128 keys can actually be encoded by the keyboard controller's input buffer. Elements 128&ndash;255 of this array can never hold true values.

{{< boilerplate/global-cref isMusicEnabled >}}

Music may play when this is true, and music is silenced when false. This setting can be toggled by the user, and the value is persisted in the [configuration file]({{< relref "configuration-file-format" >}}).

{{< boilerplate/global-cref isNewGame >}}

This is set in {{< lookup/cref TitleLoop >}} and controls whether {{< lookup/cref SwitchLevel >}} displays a "One Moment" image before loading the first level.

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

{{< boilerplate/global-cref keyNames >}}

Generally keys are named using their base (unshifted) case, but all letters are stored capitalized. There are some exceptions and oddities:

* <kbd>NULL</kbd> is not a key, and is generally indicative of an error condition. There shouldn't be any circumstance in the game where this name is shown.
* The keys <kbd>[</kbd>, <kbd>]</kbd>, <kbd>&grave;</kbd>, and <kbd>&bsol;</kbd> are defined as blank spaces. The [game font]({{< relref "databases/font" >}}) does not contain any tiles for these characters or their shifted companions.
* The <kbd>'</kbd> key renders as `"`, despite both characters being available in the game font.
* The <kbd>/</kbd> key renders as `?`.
* The numeric keypad keys render as their non-numeric functions, if available.
* The character codes 18h, 19h, 1Bh, and 1Ch produce the symbols <code>&#8593;</code>, <code>&#8595;</code>, <code>&#8592;</code>, and <code>&#8594;</code> respectively.

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

{{< boilerplate/global-cref playerBombs >}}

The acceptable range of values for this variable is 0&ndash;9. Numbers with two or more characters must be avoided, otherwise draw overflow issues will occur in the status bar.

{{< boilerplate/global-cref playerHealth >}}

When a new game is started, this is initialized to 4, which represents three filled bars of health. It can decrement down to 1, representing all health bars unfilled. Once it decrements to zero, the player immediately dies.

The maximum amount of health obtainable, once all {{< lookup/actor type=82 plural=true >}} have been picked up, is 6.

{{< boilerplate/global-cref playerHealthCells >}}

When a new game is started, this is initialized to 3, which represents three available bars of health.

The maximum amount of health cells obtainable, once all {{< lookup/actor type=82 plural=true >}} have been picked up, is 5.

{{< boilerplate/global-cref playerHurtCooldown >}}

This is modified during calls to {{< lookup/cref SetPIT0Value >}}, and takes the `value` that is passed during each call. It is treated as a 16-bit value in all contexts where it appears.

{{< boilerplate/global-cref playerInfoData >}}

{{< boilerplate/global-cref playerPushFrame >}}

When the player is pushed by actors, this will be set to one of the "force-pushed" frames based on the relative position of the actor. In pipe systems, this will be {{< lookup/cref name="PLAYER" text="PLAYER_HIDDEN" >}} to temporarily remove the player from the map.

{{< boilerplate/global-cref playerTileData >}}

This block is used to hold the [masked tile image data]({{< relref "tile-image-format#masked-tiles" >}}) that the player's sprites are built from.

{{< boilerplate/global-cref pounceHintState >}}

At any time, the value of this variable should be one of the {{< lookup/cref POUNCE_HINT >}} values. The hint is shown the first time the player is hurt, even if the injury came from an un-pounceable actor.

{{< boilerplate/global-cref profCountCPU >}}

This is updated when the {{< lookup/cref ProfileCPUService >}} function runs, and interpreted during calculations in {{< lookup/cref ProfileCPU >}}.

{{< boilerplate/global-cref profCountPIT >}}

This is updated when the {{< lookup/cref ProfileCPUService >}} function runs, and interpreted during calculations in {{< lookup/cref ProfileCPU >}}. It is read during {{< lookup/cref WaitWallclock >}}, but the actual value is irrelevant in that particular function.

{{< boilerplate/global-cref savedInt8 >}}

This function was the system timer interrupt handler when the program was started.

{{< boilerplate/global-cref savedInt9 >}}

This function was the keyboard handler when the program was started.

{{< boilerplate/global-cref sawBombHint >}}

{{< boilerplate/global-cref sawHealthHint >}}

{{< boilerplate/global-cref scrollX >}}

{{< boilerplate/global-cref scrollY >}}

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

{{< boilerplate/global-cref starBonusRanks >}}

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

{{< boilerplate/global-cref usedCheatCode >}}

This is usually false until the user enters the <kbd>C</kbd>+<kbd>0</kbd>+<kbd>F10</kbd> cheat. The intention of this variable is to prevent the user from using the cheat code more than once in a single game.

{{< boilerplate/global-cref volGroupFilename >}}

This value adjusts itself based on the value in {{< lookup/cref FILENAME_BASE >}}.

{{< boilerplate/global-cref wallclock10us >}}

This value is calculated in {{< lookup/cref ProfileCPU >}}, and should only be used as an argument to {{< lookup/cref WaitWallclock >}}.

{{< boilerplate/global-cref wallclock25us >}}

This value is calculated in {{< lookup/cref ProfileCPU >}}, and should only be used as an argument to {{< lookup/cref WaitWallclock >}}.

{{< boilerplate/global-cref wallclock100us >}}

This value is calculated in {{< lookup/cref ProfileCPU >}}, and should only be used as an argument to {{< lookup/cref WaitWallclock >}}.

{{< boilerplate/global-cref winGame >}}

At the start of each level, {{< lookup/cref winGame >}} is set to false. At the end of each iteration of the game loop, it is checked for a true value -- if anything between these two points sets the value to true, the game is considered to have been won.

{{< lookup/cref winGame >}} is activated by the {{< lookup/actor 102 >}}, {{< lookup/actor type=166 strip=true >}}, and {{< lookup/actor type=265 strip=true >}} actors.

{{< boilerplate/global-cref winLevel >}}

At the start of each level, {{< lookup/cref winLevel >}} is set to false. At the end of each iteration of the game loop, it is checked for a true value -- if anything between these two points sets the value to true, the level is considered to have been won.

{{< lookup/cref winLevel >}} is activated by several actors and the [demo playback/recording]({{< relref "demo-functions#ReadDemoFrame" >}}) functions.

{{< boilerplate/global-cref writePath >}}

The [write path]({{< relref "main-and-outer-loop#write-path" >}}) is usually an empty string, indicating the current working directory. Can also be either an absolute or a relative path, which is used as a prefix when loading/saving the [configuration]({{< relref "configuration-file-format" >}}) and [save]({{< relref "save-file-format" >}}) files.

{{< boilerplate/global-cref yOffsetTable >}}
