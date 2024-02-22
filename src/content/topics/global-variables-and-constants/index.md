+++
title = "Global Variables and Constants"
description = "Lists and briefly defines all global variables and constants shared between the game's functions."
weight = 520
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

{{< lookup/cref name="ACT" text="ACT_BASKET_NULL" >}} is a special sentinel value for the spawner functions and cannot be expressed in the map format. {{< lookup/cref name="ACT" text="ACT_STAR_FLOAT" >}} has the value 32 in the [map format]({{< relref "map-format" >}}), and all other actor types follow sequentially. Map actor types below 32 are special actors, see {{< lookup/cref SPA >}}.

{{< boilerplate/global-cref BACKDROP_HEIGHT >}}

{{< boilerplate/global-cref BACKDROP_SIZE >}}

{{< boilerplate/global-cref BACKDROP_SIZE_EGA_MEM >}}

Derived from one fourth of {{< lookup/cref BACKDROP_SIZE >}}, or 5,760 bytes.

{{< boilerplate/global-cref BACKDROP_WIDTH >}}

{{< boilerplate/global-cref CPU_TYPE >}}

These are the return values for the {{< lookup/cref GetProcessorType >}} function.

{{< boilerplate/global-cref DEMO_STATE >}}

Symbolic Constant   | Value | Description
--------------------|-------|------------
`DEMO_STATE_NONE`   | 0     | The game is played in the usual way, with user keyboard input controlling the player. All in-game hints and intermission screens are displayed.
`DEMO_STATE_RECORD` | 1     | The game is played in demo recording mode. The keyboard controls the player, but the level progression is altered and in-game hints are skipped. All player movement is captured into a demo file on disk.
`DEMO_STATE_PLAY`   | 2     | The game runs in demo playback mode. Keyboard input is ignored (any keypress ends the game) and player movement commands are read from the demo file. Level progression and hint display are altered in the same way as with `DEMO_STATE_RECORD`.

These are the return values for the {{< lookup/cref TitleLoop >}} function.

{{< boilerplate/global-cref DIR2 >}}

Symbolic Constant | Value | Description
------------------|-------|------------
`DIR2_SOUTH`      | 0     | Points toward the bottom edge of the screen.
`DIR2_NORTH`      | 1     | Points toward the top edge of the screen.
`DIR2_WEST`       | 0     | Points toward the left edge of the screen.
`DIR2_EAST`       | 1     | Points toward the right edge of the screen.

This is conceptually similar to {{< lookup/cref DIR4 >}}, but the values here should only be used in cases where objects move in one dimension.

{{% note %}}{{< lookup/cref name="DIR2" text="DIR2_SOUTH" >}} equals _{{< lookup/cref name="DIR4" text="DIR4_NORTH" >}}_, while {{< lookup/cref name="DIR2" text="DIR2_NORTH" >}} equals _{{< lookup/cref name="DIR4" text="DIR4_SOUTH" >}}_. They are **not** interchangeable.{{% /note %}}

{{< boilerplate/global-cref DIR4 >}}

Symbolic Constant | Value | Description
------------------|-------|------------
`DIR4_NONE`       | 0     | Refers to a "directionless" state. Numerically identical to `DIR4_NORTH`, but used in code to clarify that there is no direction instead of it being interpreted as a literal "north."
`DIR4_NORTH`      | 0     | Points toward the top edge of the screen.
`DIR4_SOUTH`      | 1     | Points toward the bottom edge of the screen.
`DIR4_WEST`       | 2     | Points toward the left edge of the screen.
`DIR4_EAST`       | 3     | Points toward the right edge of the screen.

The arrangement of these cardinal directions follows the conventional layout of a compass rose.

{{< boilerplate/global-cref DIR8 >}}

Symbolic Constant | Value | Description
------------------|-------|------------
`DIR8_NONE`       | 0     | Represents the absence of direction and/or a state of no movement.
`DIR8_NORTH`      | 1     | Points toward the top edge of the screen.
`DIR8_NORTHEAST`  | 2     | Points up and to the right.
`DIR8_EAST`       | 3     | Points toward the right edge of the screen.
`DIR8_SOUTHEAST`  | 4     | Points down and toward the right.
`DIR8_SOUTH`      | 5     | Points toward the bottom edge of the screen.
`DIR8_SOUTHWEST`  | 6     | Points down and toward the left.
`DIR8_WEST`       | 7     | Points toward the left edge of the screen.
`DIR8_NORTHWEST`  | 8     | Points up and toward the left.

The arrangement of these cardinal directions follows the conventional layout of a compass rose. The values defined here can be converted into X/Y deltas by using the {{< lookup/cref dir8X >}} and {{< lookup/cref dir8Y >}} arrays.

{{< boilerplate/global-cref DRAW_MODE >}}

Symbolic Constant       | Value | Description
------------------------|-------|------------
`DRAW_MODE_NORMAL`      | 0     | Draw the sprite unmodified, with X/Y positions measured relative to the game world. If the map data contains a "draw in front" tiles that intersect the sprite, the map tiles will prevail.
`DRAW_MODE_HIDDEN`      | 1     | Do not draw any part of the sprite.
`DRAW_MODE_WHITE`       | 2     | Same as `DRAW_MODE_NORMAL`, but all opaque pixel positions in the sprite are drawn in bright white.
`DRAW_MODE_TRANSLUCENT` | 3     | Same as `DRAW_MODE_WHITE`, but the sprite color is translucent.
`DRAW_MODE_FLIPPED`     | 4     | Same as `DRAW_MODE_NORMAL`, but the sprite is drawn flipped vertically.
`DRAW_MODE_IN_FRONT`    | 5     | Same as `DRAW_MODE_NORMAL`, but the sprite will cover _all_ map tiles, regardless of their "draw in front" attribute.
`DRAW_MODE_ABSOLUTE`    | 6     | Draw the sprite unmodified, with X/Y positions measured relative to the screen. Since there is no relationship to the game world in this mode, "draw in front" attributes from the map (if present) have no effect.

{{< boilerplate/global-cref Decoration >}}

The `dir` member should contain one of the {{< lookup/cref DIR8 >}} values.

The {{< lookup/cref Decoration >}} structure has associated data stored separately in the {{< lookup/cref decorationFrame >}} array.

{{< boilerplate/global-cref EGA_OFFSET >}}

{{< boilerplate/global-cref END_ANIMATION >}}

{{< boilerplate/global-cref END_SCREEN >}}

{{< boilerplate/global-cref Explosion >}}

{{< boilerplate/global-cref FILENAME_BASE >}}

{{< boilerplate/global-cref FONT >}}

The [game font]({{< relref "databases/font" >}}) is built from 100 [masked tiles]({{< relref "tile-image-format#masked-tiles" >}}), each beginning on a 40-byte boundary. Only a handful of these tiles are referenced directly in the game code; all other tile offsets are calculated by adding a multiple of 40 to one of the above base values.

{{< boilerplate/global-cref Fountain >}}

* `dir` is a {{< lookup/cref DIR4 >}} value representing the current movement direction. Each fountain starts in {{< lookup/cref name="DIR8" text="DIR4_NORTH" >}}.
* `stepcount` is an incrementing counter that tracks the number of frames the fountain has moved since it last changed direction. Once the direction change occurs, this value is zeroed again.
* `height` is the height of the stream beneath the portion of the fountain that can be stood on.
* `stepmax` is the maximum value for `stepcount` that can be reached before the fountain switches directions. This is derived from the actor's type in the map data.
* `delayleft` is a decrementing counter that, if nonzero, means that the fountain is pausing to change directions.

{{< boilerplate/global-cref GAME_INPUT >}}

These are the return values for the {{< lookup/cref ProcessGameInput >}} function, used to differentiate how the game loop should respond.

Symbolic Constant     | Value | Description
----------------------|-------|------------
`GAME_INPUT_CONTINUE` | 0     | The user did not do anything that would affect the current iteration of the game loop or the state of gameplay as a whole.
`GAME_INPUT_QUIT`     | 1     | The user wants to quit the current game, and the game loop needs to stop running.
`GAME_INPUT_RESTART`  | 2     | The user loaded a saved game, and the game loop needs to restart from the beginning with this new state.

Contrast with the values defined in {{< lookup/cref HELP_MENU >}}.

{{< boilerplate/global-cref GAME_VERSION >}}

{{< boilerplate/global-cref HELP_MENU >}}

These are the return values for the {{< lookup/cref ShowHelpMenu >}} function.

Symbolic Constant    | Value | Description
---------------------|-------|------------
`HELP_MENU_CONTINUE` | 0     | The user did not do anything that would affect the current iteration of the game loop or the state of gameplay as a whole.
`HELP_MENU_RESTART`  | 1     | The user loaded a saved game, and the game loop needs to restart from the beginning with this new state.
`HELP_MENU_QUIT`     | 2     | The user wants to quit the current game, and the game loop needs to stop running.

Contrast with the values defined in {{< lookup/cref GAME_INPUT >}}.

{{< boilerplate/global-cref IMAGE >}}

The names are described in more detail on the [full-screen image database]({{< relref "databases/full-screen-image" >}}) page.

The values for `IMAGE_TILEATTR`, `IMAGE_DEMO`, and `IMAGE_NONE` do not refer to actual files that can be displayed; they are flags placed into {{< lookup/cref miscDataContents >}} to facilitate skipping load operations on data that may already be in memory.

{{< boilerplate/global-cref JOYSTICK >}}

{{< boilerplate/global-cref JoystickState >}}

{{< boilerplate/global-cref LIGHT_SIDE >}}

Symbolic Constant   | Value | Shape               | Description
--------------------|-------|---------------------|------------
`LIGHT_SIDE_WEST`   | 0     | &#9698;             | Represents the left side of a light cone. This lightens the lower-right area of a tile.
`LIGHT_SIDE_MIDDLE` | 1     | &FilledSmallSquare; | Represents the middle of a lighted area. The entire tile is lightened.
`LIGHT_SIDE_EAST`   | 2     | &#9699;             | Represents the right side of a light cone. This lightens the lower-left area of a tile.

See the {{< lookup/cref Light >}} structure.

{{< boilerplate/global-cref LIGHT_CAST_DISTANCE >}}

{{< boilerplate/global-cref Light >}}

{{< boilerplate/global-cref MAX_ACTORS >}}

{{< boilerplate/global-cref MAX_DECORATIONS >}}

{{< boilerplate/global-cref MAX_EXPLOSIONS >}}

{{< boilerplate/global-cref MAX_FOUNTAINS >}}

{{< boilerplate/global-cref MAX_LIGHTS >}}

{{< boilerplate/global-cref MAX_PLATFORMS >}}

{{< boilerplate/global-cref MAX_SHARDS >}}

{{< boilerplate/global-cref MAX_SPAWNERS >}}

{{< boilerplate/global-cref MODE1_COLORS >}}

The colors here are based on the Borland {{< lookup/cref COLORS >}} members, with the "light" variants shifted by 8 to compensate for the EGA's color requirements. See {{< lookup/cref SetPaletteRegister >}} for more information about this difference.

{{< boilerplate/global-cref MOVE >}}

These are the return values for the {{< lookup/cref TestPlayerMove >}} and {{< lookup/cref TestSpriteMove >}} functions.

Symbolic Constant | Value | Description
------------------|-------|------------
`MOVE_FREE`       | 0     | The attempted move places the sprite into an area of free space on the map; hence the move is permissible.
`MOVE_BLOCKED`    | 1     | The attempted move places the sprite either partially or completely inside an impassible area of the map; the move attempt should be blocked.
`MOVE_SLOPED`     | 2     | The attempted move is legal (similar to `MOVE_FREE`) but it involves a sloped surface that requires further adjustment in the vertical direction.

{{< boilerplate/global-cref MUSIC >}}

{{< boilerplate/global-cref Music >}}

{{< boilerplate/global-cref PAL_ANIM >}}

{{< boilerplate/global-cref PALETTE_KEY_INDEX >}}

{{< boilerplate/global-cref PLAYER >}}

Most of these values must be combined with one of the {{< lookup/cref PLAYER_BASE >}} constants to select between the west- and east-facing variants of each frame. The only exceptions are the "dead" and "hidden" values, which are directionless.

{{< boilerplate/global-cref PLAYER_BASE >}}

The values here should be added to one of the {{< lookup/cref PLAYER >}} constants to produce the true frame number for the desired combination.

{{< boilerplate/global-cref Platform >}}

Due to hard-coded offsets in {{< lookup/cref LoadMapData >}} and {{< lookup/cref MovePlatforms >}}, the `mapstash[]` array **must** begin at word offset 2 in this structure.

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

{{< boilerplate/global-cref SPA >}}

These **sp**ecial **a**ctor types map directly to the values found in the [map files]({{< relref "map-format" >}}).

{{< boilerplate/global-cref SPR >}}

Sprite type numbers map directly to graphics in the ACTORS.MNI [masked tile image data]({{< relref "tile-image-format#masked-tiles" >}}). These sprites are not just used by actors -- decorations, shards, explosions, and other arbitrary elements draw from this set of objects.

Some of the constants use a number instead of a description of the sprite. These are "non-canonical" names that either serve as an additional handle to the same data (i.e. there are two different constants that point to the same image data after being looked up through the [tile info]({{< relref "tile-info-format" >}}) table) or they hold a nonsensical value that doesn't matter because the sprite never actually displays on the screen. The following table explains these cases:

Symbolic Constant | Duplicate Version Of | Description
------------------|----------------------|------------
`SPR_6`           | `SPR_FIREBALL`       | Referenced in {{< lookup/cref TouchPlayer >}} as a possible object that could interact with the player. Most likely left over from an older implementation of {{< lookup/actor 6 >}} which now cannot occur anymore.
`SPR_48`          | `SPR_PYRAMID`        | Referenced in {{< lookup/cref TouchPlayer >}} as a possible object that could interact with the player. Most likely left over from an older implementation of {{< lookup/actor 48 >}} which now cannot occur anymore.
`SPR_50`          | `SPR_GHOST`          | Referenced in {{< lookup/cref TouchPlayer >}} as a possible object that could interact with the player. Most likely left over from an older implementation of {{< lookup/actor 50 >}} which now cannot occur anymore.
`SPR_74`          | `SPR_BABY_GHOST_EGG` | Referenced in {{< lookup/cref TouchPlayer >}}, {{< lookup/cref CanExplode >}}, and {{< lookup/cref AddScoreForSprite >}} as a possible object that could interact with the player. Most likely left over from an older implementation of {{< lookup/actor 74 >}} which now cannot occur anymore.
`SPR_84`          | `SPR_GRAPES`         | Referenced in {{< lookup/cref TouchPlayer >}}, {{< lookup/cref CanExplode >}}, and {{< lookup/cref AddScoreForSprite >}} as a possible object that could interact with the player. Most likely left over from an older implementation of {{< lookup/actor 84 >}} which now cannot occur anymore.
`SPR_96`          | `SPR_SMOKE`          | Referenced in {{< lookup/cref CanExplode >}} and {{< lookup/cref AddScoreForSprite >}} as a possible object that could interact with the player. Most likely left over from an older implementation of {{< lookup/actor 96 >}} which now cannot occur anymore.
`SPR_150`         | `SPR_SMALL_FLAME`    | Referenced in {{< lookup/cref NewActorAtIndex >}} as the sprite type for the invisible actor {{< lookup/actor 150 >}}.
`SPR_164`         | `SPR_ROOT`           | Referenced in {{< lookup/cref NewActorAtIndex >}} as the sprite type for the invisible actors {{< lookup/actor 164 >}}, {{< lookup/actor 165 >}}, and {{< lookup/actor 166 >}}.
`SPR_248`         | `SPR_CABBAGE`        | Referenced in {{< lookup/cref NewActorAtIndex >}} as the sprite type for the invisible actor {{< lookup/actor 248 >}}. The graphics referenced here only contain one frame of the `SPR_CABBAGE` sprite.
`SPR_249`         | `SPR_CABBAGE`        | Referenced in {{< lookup/cref NewActorAtIndex >}} as the sprite type for the invisible actor {{< lookup/actor 249 >}}. The graphics referenced here only contain one frame of the `SPR_CABBAGE` sprite.
`SPR_250`         | `SPR_CABBAGE`        | Referenced in {{< lookup/cref NewActorAtIndex >}} as the sprite type for the invisible actor {{< lookup/actor 250 >}}. The graphics referenced here only contain one frame of the `SPR_CABBAGE` sprite.
`SPR_265`         | `SPR_DEMO_OVERLAY`   | Referenced in {{< lookup/cref NewActorAtIndex >}} as the sprite type for the invisible actor {{< lookup/actor 265 >}}.

{{< boilerplate/global-cref Shard >}}

{{< boilerplate/global-cref Spawner >}}

{{< boilerplate/global-cref TILE >}}

For space reasons, some of the names are a bit obtuse:

* `TILE_SWITCH_FREE_1N` has **no** ("N") line at its top.
* `TILE_SWITCH_FREE_1L` has a **light**-colored ("L") line at its top.
* Names that include `EMPTY` or `FREE` do not restrict movement, and essentially behave as "air."
* Names including `PLATFORM` only block movement in the southern direction. The player may jump up through them freely, but movement will stop if they land on it from above.
* Names including `BLOCK` are solid, and block movement in all directions.
* Names with a direction indicate that they are meant to be used in conjunction with other, similarly named tiles to draw larger constructions. The directions indicate the correct relative position for each tile.

{{< boilerplate/global-cref TITLE_SCREEN >}}

{{< boilerplate/global-cref WORD_MAX >}}

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

{{< boilerplate/global-cref areForceFieldsActive >}}

This is _always_ true by default, and can only be set false by using a {{< lookup/actor 121 >}}.

{{< boilerplate/global-cref areLightsActive >}}

On most maps, this variable is set to true by default. It only becomes false if a {{< lookup/actor 120 >}} is loaded into the map, and activation of that switch can set it true again. This variable also influences the behavior of {{< lookup/actor type=127 plural=true >}}: when false, the do not shoot at the player.

Related to {{< lookup/cref hasLightSwitch >}}.

{{< boilerplate/global-cref arePlatformsActive >}}

This is usually true, except on maps that have a {{< lookup/actor 59 >}}. On these maps, this variable is set to false when the actor is constructed and remains in that state until the player activates that switch.

{{< boilerplate/global-cref backdropNames >}}

{{% note %}}Not all of the names defined here exist in all of the group files. Some of these names do not exist in _any_ group file.{{% /note %}}

{{< boilerplate/global-cref backdropTable >}}

This is also used as scratch storage during calls to {{< lookup/cref DrawFullscreenText >}}.

See also {{< lookup/cref BACKDROP_WIDTH >}} and {{< lookup/cref BACKDROP_HEIGHT >}}.

{{< boilerplate/global-cref blockActionCmds >}}

This variable takes a true value when the player is "removed" from the map, like when interacting with a {{< lookup/actor 152 >}}, {{< lookup/actor type=149 strip=true >}}, {{< lookup/actor 186 >}}, or the {{< lookup/actor type=247 strip=true >}}.

{{< boilerplate/global-cref  blockMovementCmds >}}

Unlike {{< lookup/cref blockActionCmds >}}, this variable does not hide the player or make them invincible; this is purely an immobilization flag. The only place this is used without an accompanying {{< lookup/cref blockActionCmds >}} is with the {{< lookup/actor 162 >}} actor.

Due to an oversight, this only immobilizes the player when keyboard input is being used. This variable is ignored when a joystick is employed.

{{< boilerplate/global-cref canPlayerCling >}}

This is set by {{< lookup/cref TestPlayerMove >}} and will receive a different result depending on whether {{< lookup/cref name="DIR4" text="DIR4_WEST" >}} or {{< lookup/cref name="DIR4" text="DIR4_EAST" >}} was most recently tested.

{{< boilerplate/global-cref cartoonInfoData >}}

This points to [tile info data]({{< relref "tile-info-format" >}}) which has been read directly from disk. No processing is done to pre-parse this data.

{{< boilerplate/global-cref cmdBomb >}}

{{< boilerplate/global-cref cmdEast >}}

{{< boilerplate/global-cref cmdJump >}}

{{< boilerplate/global-cref cmdNorth >}}

{{< boilerplate/global-cref cmdSouth >}}

{{< boilerplate/global-cref cmdWest >}}

{{< boilerplate/global-cref decorationFrame >}}

This is conceptually a missing member of the {{< lookup/cref Decoration >}} structure, indexed identically to {{< lookup/cref decorations >}}.

{{< boilerplate/global-cref decorations >}}

Each element of this array is a {{< lookup/cref Decoration >}} structure. The array size is bounded by the {{< lookup/cref MAX_DECORATIONS >}} constant.

{{< boilerplate/global-cref demoDataLength >}}

{{< boilerplate/global-cref demoDataPos >}}

{{< boilerplate/global-cref demoState >}}

This variable can hold one of the following {{< lookup/cref DEMO_STATE >}} values while the game is running:

Symbolic Constant   | Value | Description
--------------------|-------|------------
`DEMO_STATE_NONE`   | 0     | Game is being played interactively, no demo is being recorded or played.
`DEMO_STATE_RECORD` | 1     | Game is being played interactively, and demo data is being recorded from the input.
`DEMO_STATE_PLAY`   | 2     | Game is being controlled by demo data.

When set to {{< lookup/cref name="DEMO_STATE" text="DEMO_STATE_RECORD" >}} or {{< lookup/cref name="DEMO_STATE" text="DEMO_STATE_PLAY" >}}, this suppresses the "Now entering level" message and all in-game hints, and adds a "DEMO" overlay.

{{< boilerplate/global-cref dir8X >}}

Related to the {{< lookup/cref DIR8 >}} constants, this array and its counterpart {{< lookup/cref dir8Y >}} specify how to change an object's X and Y coordinates to affect a move in the necessary direction. The {{< lookup/cref dir8X >}} and {{< lookup/cref dir8Y >}} elements should be added to an object's X and Y coordinates (respectively).

Symbolic Constant | Value | `dir8X[Value]` | `dir8Y[Value]`
------------------|-------|----------------|---------------
`DIR8_NONE`       | 0     | 0              | 0
`DIR8_NORTH`      | 1     | 0              | -1
`DIR8_NORTHEAST`  | 2     | 1              | -1
`DIR8_EAST`       | 3     | 1              | 0
`DIR8_SOUTHEAST`  | 4     | 1              | 1
`DIR8_SOUTH`      | 5     | 0              | 1
`DIR8_SOUTHWEST`  | 6     | -1             | 1
`DIR8_WEST`       | 7     | -1             | 0
`DIR8_NORTHWEST`  | 8     | -1             | -1

{{< boilerplate/global-cref dir8Y >}}

See {{< lookup/cref dir8X >}} for details.

{{< boilerplate/global-cref drawPageNumber >}}

During gameplay (where double-buffering is used) {{< lookup/cref activePage >}} will usually hold the opposite value, preventing changes from becoming visible on the screen until the pages are flipped.

{{< boilerplate/global-cref drawPageSegment >}}

{{< boilerplate/global-cref enableAdLib >}}

{{< boilerplate/global-cref enableSpeaker >}}

{{< boilerplate/global-cref explosions >}}

Each element of this array is an {{< lookup/cref Explosion >}} structure. The array size is bounded by the {{< lookup/cref MAX_EXPLOSIONS >}} constant.

{{< boilerplate/global-cref fontTileData >}}

{{< boilerplate/global-cref fountains >}}

Each element of this array is a {{< lookup/cref Fountain >}} structure. The array size is bounded by the {{< lookup/cref MAX_FOUNTAINS >}} constant.

{{< boilerplate/global-cref fullscreenImageNames >}}

The values for {{< lookup/cref TITLE_SCREEN >}} and {{< lookup/cref END_SCREEN >}} are different depending on the episode; typically these will be `"TITLEx.MNI"` and `"ENDx.MNI"` (respectively) with `x` matching the episode number.

{{< boilerplate/global-cref gameScore >}}

Most events in the game add points to this variable. Its purpose is purely vanity, the only effect is to earn a spot in the high score table at the end of the game. The smallest score value implemented in the game is worth 100 points, and the score should always be a multiple of 50 unless e.g. a save file was manipulated.

The acceptable range of values for this variable is 0--9,999,999. Numbers with more than seven characters must be avoided, otherwise draw overflow issues will occur in the status bar.

{{< boilerplate/global-cref gameStars >}}

Each star represents a 1,000 point bonus which is added to {{< lookup/cref gameScore >}} during the {{< lookup/cref ShowStarBonus >}} sequence. The star count is reset to zero once the bonus has been added. The star count also influences which bonus maps are entered over the course of the game:

Stars  | Bonus Map
-------|----------
0--24  | Skipped.
25--49 | BONUS1 (E1), BONUS3 (E2), or BONUS5 (E3).
&ge;50 | BONUS2 (E1), BONUS4 (E2), or BONUS6 (E3).

The acceptable range of values for this variable is 0--99. Numbers with two or more characters must be avoided, otherwise draw overflow issues will occur in the status bar.

{{< boilerplate/global-cref gameTickCount >}}

This value is used by various delay functions to produce pauses of a constant length, regardless of processor speed. It is also used to govern the speed of the {{< lookup/cref GameLoop >}} function.

{{< boilerplate/global-cref hasHScrollBackdrop >}}

{{< boilerplate/global-cref hasLightSwitch >}}

This variable influences the behavior of {{< lookup/actor type=127 plural=true >}} to help them differentiate if {{< lookup/cref areLightsActive >}} is true because there is no {{< lookup/actor 120 >}} on the map, or because the switch is present and has been activated by the player.

{{< boilerplate/global-cref hasRain >}}

{{< boilerplate/global-cref hasVScrollBackdrop >}}

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

This array is twice as large as it needs to be. Due to the high bit being used as the make/break flag, only 128 keys can actually be encoded by the keyboard controller's input buffer. Elements 128--255 of this array can never hold true values.

{{< boilerplate/global-cref isMusicEnabled >}}

Music may play when this is true, and music is silenced when false. This setting can be toggled by the user, and the value is persisted in the [configuration file]({{< relref "configuration-file-format" >}}).

{{< boilerplate/global-cref isNewGame >}}

This is set in {{< lookup/cref TitleLoop >}} and controls whether {{< lookup/cref InitializeLevel >}} displays a "One Moment" image before loading the first level.

{{< boilerplate/global-cref isNewSound >}}

This serves as a communication flag between {{< lookup/cref StartSound >}} and {{< lookup/cref PCSpeakerService >}}.

{{< boilerplate/global-cref isPlayerInPipe >}}

While this variable is true, the player cannot take damage by touching enemies, and will be pushed around the map any time a pipe corner actor is touched.

{{< boilerplate/global-cref isPlayerInvincible >}}

This variable is only true while an {{< lookup/actor 201 >}} is present on the map. It gives the same level of protection as the {{< lookup/cref isGodMode >}} cheat flag.

{{< boilerplate/global-cref isPlayerNearHintGlobe >}}

This is used to override the "look up" input command, instead using it to activate a hint globe.

{{< boilerplate/global-cref isPlayerNearTransporter >}}

This is used to override the "look up" input command, instead using it to activate a transporter. In order for this to be true, the player must specifically be standing "inside" the transporter sprite. Merely touching its edge is not sufficient.

{{< boilerplate/global-cref isPlayerPushAbortable >}}

None of the pushes available in the retail game set up a push that enables this flag. Its effect can never be seen without modification.

{{< boilerplate/global-cref isPlayerPushBlockable >}}

With this flag unset; the player can be pushed through solid walls. This is how the pipe system moves the player.

{{< boilerplate/global-cref isPlayerPushed >}}

When true, any player cling is immediately released, the scooter is force-unmounted, and regular player input and movement processing is suspended. After the push has run its course (or the player smacks into something) this becomes false again.

{{< boilerplate/global-cref isPlayerSlidingEast >}}

This value is unconditionally cleared during every call to {{< lookup/cref TestPlayerMove >}}. It is only possible for it to be reset during cases where {{< lookup/cref name="DIR4" text="DIR4_EAST" >}} was the direction tested.

{{< boilerplate/global-cref isPlayerSlidingWest >}}

This value is unconditionally cleared during every call to {{< lookup/cref TestPlayerMove >}}. It is only possible for it to be reset during cases where {{< lookup/cref name="DIR4" text="DIR4_WEST" >}} was the direction tested.

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
* The keys <kbd>[</kbd>, <kbd>]</kbd>, <kbd>`</kbd>, and <kbd>\\</kbd> are defined as blank spaces. The [game font]({{< relref "databases/font" >}}) does not contain any tiles for these characters or their shifted companions.
* The <kbd>'</kbd> key renders as `"`, despite both characters being available in the game font.
* The <kbd>/</kbd> key renders as `?`.
* The numeric keypad keys render as their non-numeric functions, if available.
* The character codes 18h, 19h, 1Bh, and 1Ch produce the symbols <code>&uparrow;</code>, <code>&downarrow;</code>, <code>&leftarrow;</code>, and <code>&rightarrow;</code> respectively.

{{< boilerplate/global-cref lastGroupEntryLength >}}

This value is updated each time {{< lookup/cref GroupEntryFp >}} opens a [group file]({{< relref "group-file-format" >}}) entry.

{{< boilerplate/global-cref lastScancode >}}

In the case of a key down/"make" code, this will be a value in the range 0h--7Fh. For key up/"break" codes, this will be a value in the range 80h--FFh. Break codes can be converted into corresponding make codes by taking the value bitwise-AND 7Fh.

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

{{< boilerplate/global-cref lights >}}

Each element of this array is a {{< lookup/cref Light >}} structure. The array size is bounded by the {{< lookup/cref MAX_LIGHTS >}} constant.

{{< boilerplate/global-cref mapData >}}

Maps are interpreted as word-aligned data, and temporary data is byte-aligned. This temporary data consists of [masked tile image data]({{< relref "tile-image-format#masked-tiles" >}}) for cartoons and scratch storage needed during the loading of backdrop images.

{{< boilerplate/global-cref mapNames >}}

{{< boilerplate/global-cref mapVariables >}}

See {{< lookup/cref hasHScrollBackdrop >}}, {{< lookup/cref hasRain >}}, {{< lookup/cref hasVScrollBackdrop >}}, {{< lookup/cref musicNum >}}, {{< lookup/cref paletteAnimationNum >}}, and the [backdrop numbers]({{< relref "databases/backdrop" >}}).

{{< boilerplate/global-cref mapWidth >}}

This is also the number of tiles that must be added or subtracted to reach a given horizontal position in the next or previous row of the map data. This is usually _not_ used to stride over a fixed number of rows; see {{< lookup/cref mapYPower >}} for that.

{{< boilerplate/global-cref mapYPower >}}

By expressing map width as **2<sup>n</sup>**, it becomes possible to convert X,Y positions to linear tile offsets by calculating **X + (Y \<\< mapYPower)**. This is considerably faster than multiplying Y by {{< lookup/cref mapWidth >}}.

{{< boilerplate/global-cref maskedTileData >}}

{{< boilerplate/global-cref maxScrollY >}}

This is _not_ the same thing as map height; this is instead the height of the map minus the height of the game window. This is the largest possible value for {{< lookup/cref scrollY >}} before garbage begins to display at the bottom of the game window.

{{< boilerplate/global-cref miscData >}}

Outside of gameplay, this is used as a temporary buffer while copying [full-screen image data]({{< relref "full-screen-image-format" >}}) into EGA memory.

When switching maps, this is used as scratch storage during the loading of backdrop images.

During gameplay, the first 5,000 bytes of this block are used to hold any [demo data]({{< relref "demo-format" >}}) that is being played or recorded. The remainder of the block is used to hold [music data]({{< relref "adlib-music-format" >}}) for the maps if there is an AdLib card installed, **or** [tile attributes data]({{< relref "tile-attributes-format" >}}) if there is not an AdLib card installed. (See {{< lookup/cref tileAttributeData >}}.)

{{< boilerplate/global-cref miscDataContents >}}

When functions modify the contents of the {{< lookup/cref miscData >}} memory block, they also update this value with one of the {{< lookup/cref IMAGE >}} values to indicate what has been written there. This value is then used during {{< lookup/cref DrawFullscreenImage >}} to skip loading in cases where {{< lookup/cref miscData >}} already contains the image content that is going to be drawn.

{{< boilerplate/global-cref musicDataHead >}}

{{< boilerplate/global-cref musicDataLeft >}}

{{< boilerplate/global-cref musicDataLength >}}

{{< boilerplate/global-cref musicDataPtr >}}

{{< boilerplate/global-cref musicNames >}}

Each array index matches with a {{< lookup/cref MUSIC >}} constant.

{{< boilerplate/global-cref musicNextDue >}}

{{< boilerplate/global-cref musicNum >}}

This is an index to one of the {{< lookup/cref musicNames >}} elements, and matches the numbering of the {{< lookup/cref MUSIC >}} constants.

{{< boilerplate/global-cref musicTickCount >}}

{{< boilerplate/global-cref numActors >}}

This is used as an insertion cursor as actors are being created, pointing to the next available element where one could be inserted. It also is checked against {{< lookup/cref MAX_ACTORS >}} to prevent overflowing the array.

{{< boilerplate/global-cref numBarrels >}}

This value in incremented when {{< lookup/cref ConstructActor >}} adds barrel/basket actors to the map, and it is decremented in {{< lookup/cref DestroyBarrel >}}. When the last remaining barrel is destroyed, the player is given a 50,000 point bonus.

{{< boilerplate/global-cref numDecorations >}}

This _always_ has the value of {{< lookup/cref MAX_DECORATIONS >}}.

{{< boilerplate/global-cref numExplosions >}}

This _always_ has the value of {{< lookup/cref MAX_EXPLOSIONS >}}.

{{< boilerplate/global-cref numEyePlants >}}

This value in incremented when {{< lookup/cref NewActorAtIndex >}} adds {{< lookup/actor type=95 strip=1 >}} actors to the map, and it is decremented in {{< lookup/cref CanExplode >}}. When the last remaining {{< lookup/actor type=95 strip=1 >}} is destroyed, the player is given a 50,000 point bonus.

This value is artificially constrained to 15. If a map has more than this many {{< lookup/actor type=95 strip=1 plural=1 >}}, only the first 15 are counted.

{{< boilerplate/global-cref numFountains >}}

This is used as an insertion cursor as fountains are being created, pointing to the next available element where one could be inserted. This variable is _not_ used for bounds checking, and overflow is possible with a malicious map file.

{{< boilerplate/global-cref numLights >}}

This is used as an insertion cursor as lights are being created, pointing to the next available element where one could be inserted. It also is checked against {{< lookup/cref MAX_LIGHTS >}} to prevent overflowing the array.

{{< boilerplate/global-cref numPlatforms >}}

This is used as an insertion cursor as platforms are being created, pointing to the next available element where one could be inserted. This variable is _not_ used for bounds checking, and overflow is possible with a malicious map file.

{{< boilerplate/global-cref numShards >}}

This _always_ has the value of {{< lookup/cref MAX_SHARDS >}}.

{{< boilerplate/global-cref numSpawners >}}

This _always_ has the value of {{< lookup/cref MAX_SPAWNERS >}}.

{{< boilerplate/global-cref paletteAnimationNum >}}

{{< boilerplate/global-cref paletteStepCount >}}

Once the end of the palette table has been reached (as indicated by encountering an {{< lookup/cref END_ANIMATION >}} marker) this resets to 0 and the pattern repeats.

{{< boilerplate/global-cref pit0Value >}}

This is modified during calls to {{< lookup/cref SetPIT0Value >}}, and takes the `value` that is passed during each call. It is treated as a 16-bit value in all contexts where it appears.

{{< boilerplate/global-cref platforms >}}

Each element of this array is a {{< lookup/cref Platform >}} structure. The array size is bounded by the {{< lookup/cref MAX_PLATFORMS >}} constant.

{{< boilerplate/global-cref playerBaseFrame >}}

This should always contain one of the {{< lookup/cref PLAYER_BASE >}} values, and represents the number of player sprite frames that must be skipped over to index the appropriately-oriented version of a player sprite. (Left-facing frames require an offset of zero, while an equivalent right-facing frame requires an offset of 23.) When combined with the value in {{< lookup/cref playerFrame >}}, the correct sprite frame is identified.

Several functions in the game use this to determine the direction the player is facing, making this the canonical direction variable (as opposed to {{< lookup/cref playerFaceDir >}}).

{{< boilerplate/global-cref playerBombs >}}

The acceptable range of values for this variable is 0--9. Numbers with two or more characters must be avoided, otherwise draw overflow issues will occur in the status bar.

{{< boilerplate/global-cref playerClingDir >}}

This should always contain one of the {{< lookup/cref DIR4 >}} values. When this equals {{< lookup/cref name="DIR4" text="DIR4_WEST" >}}, the player is clinging to a wall that is to their west (i.e. towards the left edge of the screen). Likewise with {{< lookup/cref name="DIR4" text="DIR4_EAST" >}} and an east/right wall. In the case of {{< lookup/cref name="DIR4" text="DIR4_NONE" >}}, the player is not clinging to any walls.

The remaining {{< lookup/cref DIR4 >}} values do not make sense as cling directions and should not be used.

{{< boilerplate/global-cref playerDeadTime >}}

During normal gameplay, this holds a zero value. It is set to one the moment the player dies, either by depleting all the health bars or falling off the bottom of the map.

Once the player is dead _from health depletion_, the counter increments by one during each frame and performs the following actions:

`playerDeadTime` Value(s) | Death Animation Sequence
--------------------------|-------------------------
1                         | {{< lookup/cref name="SND" text="SND_PLAYER_HURT" >}} sound effect is started.
1--9                      | Player sprite is shown as a stationary angel, with a two-frame "wing flap" animation based on the value `playerDeadTime % 2`.
10                        | {{< lookup/cref name="SND" text="SND_PLAYER_DEATH" >}} sound effect is started.
10--11                    | The game window scrolls up by one tile on each frame.
10--37                    | Player sprite moves up by one tile on each frame. Regardless of the player's starting position, this moves them far above the top edge of the screen.
37                        | With the player fully off the screen, the level restarts.

Death by falling off the map is handled separately based on {{< lookup/cref playerFallDeadTime >}}.

{{< boilerplate/global-cref playerDizzyLeft >}}

The lifecycle of this variable is controlled by {{< lookup/cref ProcessPlayerDizzy >}}, and it can immediately be canceled by calling {{< lookup/cref ClearPlayerDizzy >}}.

{{< boilerplate/global-cref playerFaceDir >}}

This should always be one of the east/west {{< lookup/cref DIR4 >}} values.

This is **not** the primary means of determining the player's direction; see {{< lookup/cref playerBaseFrame >}} for that. This variable is principally responsible for adding a one-frame "turn around" when a player switches direction. As an example: With the player facing right, quickly tap the "walk left" key. The player will switch directions, but will _not_ move in the horizontal direction. It is only on subsequent "walk left" inputs that the horizontal position will change. This variable is involved in producing that delay.

{{< boilerplate/global-cref playerFallDeadTime >}}

During normal gameplay, this holds a zero value. It is set to one the moment the player falls off the bottom of the map.

Once the player is off the map, the counter increments by one during each frame and performs the following actions:

`playerFallDeadTime` Value(s) | Death Animation Sequence
------------------------------|-------------------------
1                             | Skipped; `playerFallDeadTime` is incremented before any comparisons occur.
2                             | {{< lookup/cref name="SND" text="SND_PLAYER_HURT" >}} sound effect is started.
2--11                         | Occurs during a single game frame, incrementing `playerFallDeadTime` from 2 to 11 with a hard wait of two ticks between each iteration. This freezes all gameplay for about 1 &frasl; 7 of a second.
13                            | {{< lookup/cref name="SND" text="SND_PLAYER_DEATH" >}} sound effect is started.
13--18                        | One of the speech bubbles appears above the player, rising by one tile each frame.
19--31                        | The speech bubble remains fixed in its final position.
31                            | The level restarts.

{{< boilerplate/global-cref playerFrame >}}

The value here should always be one of the {{< lookup/cref PLAYER >}} values, which represent the sprite frames described in the lower half of the [player sprite database]({{< relref "databases/player-sprite" >}}).

This variable is changed by {{< lookup/cref MovePlayer >}}, {{< lookup/cref MovePlayerScooter >}}, and {{< lookup/cref ProcessPlayerDizzy >}}. It is read by {{< lookup/cref ProcessPlayer >}}, where it is combined with {{< lookup/cref playerBaseFrame >}} to control the player sprite frame displayed on the screen.

{{< boilerplate/global-cref playerHealth >}}

When a new game is started, this is initialized to 4, which represents three filled bars of health. It can decrement down to 1, representing all health bars unfilled. Once it decrements to zero, the player immediately dies.

The maximum amount of health obtainable, once all {{< lookup/actor type=82 plural=true >}} have been picked up, is 6.

{{< boilerplate/global-cref playerHealthCells >}}

When a new game is started, this is initialized to 3, which represents three available bars of health.

The maximum amount of health cells obtainable, once all {{< lookup/actor type=82 plural=true >}} have been picked up, is 5.

{{< boilerplate/global-cref playerHurtCooldown >}}

{{< boilerplate/global-cref playerInfoData >}}

This points to [tile info data]({{< relref "tile-info-format" >}}) which has been read directly from disk. No processing is done to pre-parse this data.

{{< boilerplate/global-cref playerPushDir >}}

This should be set to one of the {{< lookup/cref DIR8 >}} constants.

{{< boilerplate/global-cref playerPushForceFrame >}}

When the player is pushed by actors, this will be set to one of the "force-pushed" frames based on the relative position of the actor. In pipe systems, this will be {{< lookup/cref name="PLAYER" text="PLAYER_HIDDEN" >}} to temporarily remove the player from the map.

{{< boilerplate/global-cref playerPushMaxTime >}}

{{< boilerplate/global-cref playerPushSpeed >}}

{{< boilerplate/global-cref playerPushTime >}}

When this value equals {{< lookup/cref playerPushMaxTime >}}, the push has run to its natural point of completion and stops affecting the player.

{{< boilerplate/global-cref playerTileData >}}

This block is used to hold the [masked tile image data]({{< relref "tile-image-format#masked-tiles" >}}) that the player's sprites are built from.

{{< boilerplate/global-cref playerX >}}

{{< boilerplate/global-cref playerY >}}

{{< boilerplate/global-cref pounceHintState >}}

At any time, the value of this variable should be one of the {{< lookup/cref POUNCE_HINT >}} values. The hint is shown the first time the player is hurt, even if the injury came from an un-pounceable actor.

{{< boilerplate/global-cref pounceStreak >}}

This value is incremented and tested in {{< lookup/cref PounceHelper >}}, which also gives a 50,000 bonus point on the tenth consecutive pounce. This counter is reset to zero when the player touches the ground, or when they pounce on an actor who is designed to be used as a platform. Notably, the pounce streak is _not_ reset when the player clings to a wall.

{{< boilerplate/global-cref profCountCPU >}}

This is updated when the {{< lookup/cref ProfileCPUService >}} function runs, and interpreted during calculations in {{< lookup/cref ProfileCPU >}}.

{{< boilerplate/global-cref profCountPIT >}}

This is updated when the {{< lookup/cref ProfileCPUService >}} function runs, and interpreted during calculations in {{< lookup/cref ProfileCPU >}}. It is read during {{< lookup/cref WaitWallclock >}}, but the actual value is irrelevant in that particular function.

{{< boilerplate/global-cref queuePlayerDizzy >}}

This variable is usually set while the player is off the ground (either free-falling or moving through pipes). Once the player lands on the ground, the presence of this flag initiates the dizzy countdown tracked in {{< lookup/cref playerDizzyLeft >}}.

{{< boilerplate/global-cref randStepCount >}}

Used exclusively by {{< lookup/cref GameRand >}}; only exposed globally so that it can be reset by {{< lookup/cref InitializeMapGlobals >}}.

{{< boilerplate/global-cref savedInt8 >}}

This function was the system timer interrupt handler when the program was started.

{{< boilerplate/global-cref savedInt9 >}}

This function was the keyboard handler when the program was started.

{{< boilerplate/global-cref sawAutoHintGlobe >}}

Once a hint globe has auto-activated once, no other hint globe will do that on the current level -- the player must explicitly press the "look up" key to see subsequent messages.

This variable is forced true during demo recording and playback to prevent hint display from interfering with gameplay in those contexts.

{{< boilerplate/global-cref sawBearTrapBubble >}}

{{< boilerplate/global-cref sawBombHint >}}

{{< boilerplate/global-cref sawBossBubble >}}

{{< boilerplate/global-cref sawHamburgerBubble >}}

{{< boilerplate/global-cref sawHealthHint >}}

{{< boilerplate/global-cref sawHurtBubble >}}

{{< boilerplate/global-cref sawJumpPadBubble >}}

{{< boilerplate/global-cref sawMonumentBubble >}}

{{< boilerplate/global-cref sawMysteryWallBubble >}}

{{< boilerplate/global-cref sawPipeBubble >}}

{{< boilerplate/global-cref sawPusherRobotBubble >}}

{{< boilerplate/global-cref sawScooterBubble >}}

{{< boilerplate/global-cref sawTransporterBubble >}}

{{< boilerplate/global-cref sawTulipLauncherBubble >}}

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

{{< boilerplate/global-cref scooterMounted >}}

This variable will hold zero when the player is not riding a scooter, and nonzero when the player is doing so. At the moment a scooter is initially mounted, this variable is set to 4 and decrements on each successive frame until reaching 1, where it remains until the scooter is unmounted. This decrementing counter governs the initial upward "takeoff" at mount time.

{{< boilerplate/global-cref scrollX >}}

{{< boilerplate/global-cref scrollY >}}

{{< boilerplate/global-cref shards >}}

Each element of this array is a {{< lookup/cref Shard >}} structure. The array size is bounded by the {{< lookup/cref MAX_SHARDS >}} constant.

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

{{% note %}}`soundPriority[0]` is used to hold the data that underpins the (completely unrelated) {{< lookup/cref playerJumpTime >}} variable. Functions that use `soundPriority[]` should always be aware that the zeroth element should not be touched under any circumstances.{{% /note %}}

{{< boilerplate/global-cref spawners >}}

Each element of this array is a {{< lookup/cref Spawner >}} structure. The array size is bounded by the {{< lookup/cref MAX_SPAWNERS >}} constant.

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

{{< boilerplate/global-cref transporterTimeLeft >}}

When any transporter is used, this value is set to 15. At that moment, _all_ the transporters on the map emit several sparkle decorations and the {{< lookup/cref name="SND" text="SND_TRANSPORTER_ON" >}} sound effect is started. While this value decrements toward zero, _all_ transporter sprites randomly flash white. Once zero is reached, the requisite transporter action occurs -- either relocating the player or winning the level.

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
