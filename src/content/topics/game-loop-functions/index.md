+++
title = "Game Loop Functions"
description = "Describes the main game loop and the supporting functions that it relies on."
weight = 400
+++

# Game Loop Functions

The **game loop** is the core code that executes once per frame of gameplay and dispatches all of the per-frame functionality needed to run each of the game's subsystems. This loop is responsible for controlling the overall pace of gameplay, screen redrawing, input handling, and the movement of the player and all of the elements that exist in the game world. The game loop is also responsible for checking to see if the current level has been "won" and calling for a level change in that case.

The game loop runs continually until the entire episode has been won or the user quits the game.

{{< table-of-contents >}}

## Supporting Functions

Before the game loop begins, a pair of functions ({{< lookup/cref InitializeEpisode >}} and {{< lookup/cref InitializeLevel >}}) run to set up all of the global variables needed for the game to work. {{< lookup/cref InitializeEpisode >}} is responsible for setting up the initial state of the game (so the player starts on the first level, with three filled health bars, etc.) when a fresh game is started. In the case where a saved game is loaded, {{< lookup/cref LoadGameState >}} performs these actions using the saved values instead.

{{< lookup/cref InitializeLevel >}} is responsible for loading the map data into memory and setting up the initial state of the level that is being entered. This function runs each time a level is entered -- via regular level progression, loading a saved game, beginning a new game, or by the player dying and restarting the current level. In broad strokes, {{< lookup/cref InitializeLevel >}} initializes all of the variables that are processed during each iteration of the game loop.

A third function, {{< lookup/cref InitializeMapGlobals >}} is called by {{< lookup/cref InitializeLevel >}} to set the initial state of many global variables pertaining specifically to player movement and map object interactivity.

{{< boilerplate/function-cref InitializeEpisode >}}

The {{< lookup/cref InitializeEpisode >}} function sets up the initial values for a few of the episode-related global variables tracked by the game. This sets up the initial score, health, level number, etc. when a new game is started. This places the player on the first level with a zero score, three full bars of health, and so forth.

This function is _not_ used when a saved game is loaded; the [save file]({{< relref "save-file-format" >}}) contains its own values that should be restored. See {{< lookup/cref LoadGameState >}} for that implementation.

```c
void InitializeEpisode(void)
{
    gameScore = 0;
    playerHealth = 4;
    playerHealthCells = 3;
    levelNum = 0;
    playerBombs = 0;
    gameStars = 0;
    demoDataPos = 0;
    demoDataLength = 0;
    usedCheatCode = false;
    sawBombHint = false;
    sawHealthHint = false;
}
```

This function contains no logic; it simply sets the default initial values for all of the relevant game globals. {{< lookup/cref gameScore >}}, {{< lookup/cref playerBombs >}}, and {{< lookup/cref gameStars >}} are all set to zero, which sets the initial state of those elements on the status bar. {{< lookup/cref playerHealth >}} and {{< lookup/cref playerHealthCells >}} are set to four and three respectively, setting the player's initial health to 4 (i.e. the player can be damaged four times without dying) and the number of health bars available in the status bar to 3.

By setting {{< lookup/cref levelNum >}} to zero, the first level is selected for play. (See [level and map functions]({{< relref "level-and-map-functions#maps-vs-levels" >}}) for information about the level progression.) {{< lookup/cref demoDataPos >}} and {{< lookup/cref demoDataLength >}} are both zeroed to ensure that any subsequent demo file playback or recording operations start in a sensible state.

Finally, the {{< lookup/cref usedCheatCode >}}, {{< lookup/cref sawBombHint >}}, and {{< lookup/cref sawHealthHint >}} flags are set to false. The {{< lookup/cref usedCheatCode >}} flag prevents the cheat key sequence from being used more than once during an episode, and the remaining flags determine if contextual hint dialogs should be shown as different events happen in the game. In this state, the game presumes that the user might not know how to use bombs or how to regain health.

{{< note >}}There is an additional hint variable {{< lookup/cref pounceHintState >}} that is not initialized here; that happened earlier in the "begin new game" branch of {{< lookup/cref TitleLoop >}}.{{< /note >}}

{{< boilerplate/function-cref InitializeLevel >}}

The {{< lookup/cref InitializeLevel >}} function initializes all of the global variables and related subsystems for the start (or restart) of the level identified by `level_num`. This function runs every time a level is entered, whether by starting a new game, playing a demo, loading a game, or restarting due to player death. This function handles the screen/music transitions, loads the level data, initializes the player, and sets up all of the interactive elements on the map.

```c
void InitializeLevel(word level_num)
{
    FILE *fp;
    word bdnum;

    if (level_num == 0 && isNewGame) {
        DrawFullscreenImage(IMAGE_ONE_MOMENT);
        WaitSoft(300);
    } else {
        FadeOut();
    }
```

In the case when the `level_num` being entered is the zeroth level _and_ the {{< lookup/cref isNewGame >}} flag is set, this function knows that the user chose to begin a new game (as opposed to loading a game or starting demo playback that might happen to be on the zeroth level). In this case, the {{< lookup/cref DrawFullscreenImage >}} function displays {{< lookup/cref name="IMAGE" text="IMAGE_ONE_MOMENT" >}} (an image of an alien, who we learn _much_ later is Zonk, saying "One Moment") and {{< lookup/cref WaitSoft >}} inserts an artificial (but partially skippable) delay of 300 game ticks. If the user chooses to skip the delay, the subsequent code will take a perceptible amount of time to load the level data and construct the backdrop image tables, so the image will not immediately disappear on many computers.

{{< aside class="fun-fact" >}}
**I guess that's growing up.**

All my childhood, I wondered what the game was doing while it was showing this "One Moment" screen. I always figured it was doing some important calculation or data load operation, but it turns out it's just sitting idle. In retrospect, I probably should've realized that it wasn't doing anything critical since demos and saved games loaded without such a delay.
{{< /aside >}}

In all other cases, the screen immediately fades out due to a call to {{< lookup/cref FadeOut >}} and the function continues with the screen blank.

```c
    fp = GroupEntryFp(mapNames[level_num]);
    mapVariables = getw(fp);
    fclose(fp);
```

The passed `level_num` is looked up in the {{< lookup/cref mapNames >}} array to translate it into a group entry name. This name is passed to {{< lookup/cref GroupEntryFp >}} which looks up the correct data in the [group files]({{< relref "group-file-format" >}}) and returns a file stream pointer to this data in `fp`.

The first two bytes in the [map file format]({{< relref "map-format" >}}) are [map variables]({{< relref "map-format#map-variables-word" >}}) that control a few details about the global environment of the map. These are read with a call to {{< lookup/cref getw >}} and stored in the 16-bit word variable {{< lookup/cref mapVariables >}}. Since this is the only part of the map data that needs to be processed here, `fp` is closed by the call to {{< lookup/cref fclose >}}.

{{< note >}}The map file will be reopened as part of the subsequent {{< lookup/cref LoadMapData >}} call, which is a bit redundant and wasteful.{{< /note >}}

```c
    StopMusic();

    hasRain = (bool)(mapVariables & 0x0020);
    bdnum = mapVariables & 0x001f;
    hasHScrollBackdrop = (bool)(mapVariables & 0x0040);
    hasVScrollBackdrop = (bool)(mapVariables & 0x0080);
    paletteAnimationNum = (byte)(mapVariables >> 8) & 0x07;
    musicNum = (mapVariables >> 11) & 0x001f;
```

{{< lookup/cref StopMusic >}} stops any menu or in-game music that might be playing. It has to happen somewhere, may as well be here.

Next, the {{< lookup/cref mapVariables >}} are decoded. The 16-bit value is packed according to the [map variables]({{< relref "map-format#map-variables-word" >}}) table, and its bit fields are extracted into the boolean {{< lookup/cref hasRain >}}, {{< lookup/cref hasHScrollBackdrop >}}, and {{< lookup/cref hasVScrollBackdrop >}} variables, while the numeric fields are stored in `bdnum`, {{< lookup/cref paletteAnimationNum >}}, and {{< lookup/cref musicNum >}}. The `bdnum` variable contains the map's backdrop number, which is handled locally and does not get stored in any global variables here.

```c
    InitializeMapGlobals();
```

{{< lookup/cref InitializeMapGlobals >}} is responsible for initializing almost four dozen global variables pertaining to player movement, actor interaction, and map state. There is no logic performed in there; all of these variables are unconditionally set to the same initial value every time this function is called.

```c
    if (IsNewBackdrop(bdnum)) {
        LoadBackdropData(backdropNames[bdnum], mapData.b);
    }
```

Here the backdrop data is loaded and the scrolling preprocessing is done if needed. This is governed by calling {{< lookup/cref IsNewBackdrop >}} with the map's `bdnum` as the argument. If the new backdrop is the same as the backdrop that has previously been loaded, there is no reason to load it again and the `if` body does not execute. Otherwise, {{< lookup/cref LoadBackdropData >}} is called to prepare the new backdrop for use. The backdrop's [group file]({{< relref "group-file-format" >}}) name is looked up in the {{< lookup/cref backdropNames >}} array by using `bdnum` as the index.

{{< lookup/cref LoadBackdropData >}} requires a block of memory to use as scratch space, and the byte-addressable view into {{< lookup/cref mapData >}} is large enough to serve that purpose. After the load is complete, {{< lookup/cref mapData >}} and its contents are no longer needed and it can be refilled with the actual, correct map data.

```c
    LoadMapData(level_num);

    if (level_num == 0 && isNewGame) {
        FadeOut();
        isNewGame = false;
    }
```

The actual loading of the map data and the construction of the actors it contains is handled in the {{< lookup/cref LoadMapData >}} function. It takes the `level_num` as an argument to specify which level to load.

Similar to the beginning of the function, a special condition checks for the case where a new game has been started. In this case, the "One Moment" image is still visible on the screen, so {{< lookup/cref FadeOut >}} takes it down. To prevent it from showing again if this level restarts, the {{< lookup/cref isNewGame >}} flag is unset here.

```c
    if (demoState == DEMO_STATE_NONE) {
        switch (level_num) {
        case 0:
        case 1:
        case 4:
        case 5:
        case 8:
        case 9:
        case 12:
        case 13:
        case 16:
        case 17:
            SelectDrawPage(0);
            SelectActivePage(0);
            ClearScreen();
            FadeIn();
            ShowLevelIntro(level_num);
            WaitSoft(150);
            FadeOut();
            break;
        }
    }
```

This block of code handles UI feedback in the form of the "Now entering level..." text before each level begins. If {{< lookup/cref demoState >}} is {{< lookup/cref name="DEMO_STATE" text="DEMO_STATE_NONE" >}}, a demo is neither being recorded nor played back and such feedback is appropriate. The `switch` cases mirror the [level progression]({{< relref "level-and-map-functions#maps-vs-levels" >}}) of the game. This ensures that this dialog only appears before maps 1&ndash;10, without appearing before bonus levels or the eleventh level of the first episode.

For these regular levels, the dialog is shown by calling both {{< lookup/cref SelectDrawPage >}} and {{< lookup/cref SelectActivePage >}} with the zeroth video page as the argument. This makes it so that the effect of all draw functions becomes immediately visible without the page-flipping machinery getting in the way. {{< lookup/cref ClearScreen >}} erases this draw page by replacing it with solid black tiles, and {{< lookup/cref FadeIn >}} restores the palette to its normal state, making this solid black screen visible.

{{< lookup/cref ShowLevelIntro >}} displays the "Now entering level..." dialog with `level_num` used to influence the number shown in the message. {{< lookup/cref WaitSoft >}} pauses on the message for an interruptible 150 game ticks, then {{< lookup/cref FadeOut >}} fades the message away. From there, execution `break`s back to the main flow of the function.

```c
    InitializeShards();
    InitializeExplosions();
    InitializeDecorations();
    ClearPlayerPush();
    InitializeSpawners();
```

These functions initialize the actor-like elements that all maps can have, as well as a bit of player movement.

{{< lookup/cref InitializeShards >}}, {{< lookup/cref InitializeExplosions >}}, {{< lookup/cref InitializeDecorations >}}, and {{< lookup/cref InitializeSpawners >}} reset the fixed-size arrays for the map's shards, explosions, decorations, and spawners, respectively. Each level should start with none of these in an active state, so this clears any such elements that might have been left running from the previous map.

{{< lookup/cref ClearPlayerPush >}} resets the global player control variables that come into play when the player is involuntarily pushed around the map. Each map should begin with the player in a "not pushed" state, and this function achieves that.

```c
    ClearGameScreen();
    SelectDrawPage(activePage);
    activePage = !activePage;
    SelectActivePage(activePage);
```

Next the in-game drawing environment is set up. {{< lookup/cref ClearGameScreen >}} erases the screen and draws the status bar background and current score/bombs/health/stars values on top of it. This sets up the static areas of the game screen on both video pages.

The initial state of the page-flipping is set up next. In steady-state, the value in {{< lookup/cref activePage >}} represents the page number that is currently being displayed on the screen, leaving the opposite page number (the "draw" page) to be the one being redrawn in the background. This sequence reverses the pages' roles: {{< lookup/cref SelectDrawPage >}} tells drawing to occur on the (old) active page, then {{< lookup/cref activePage >}} is negated to produce the (new) active page, and {{< lookup/cref SelectActivePage >}} displays this (new) active page.

Visually this does not do anything at this point in the execution, since both pages contain identical content, but it does ensure that the pages are in a reasonable state for the game loop to begin drawing and flipping pages itself later. The {{< lookup/cref GameLoop >}} function performs these same steps at the end of each frame it draws.

```c
    SaveGameState('T');
    StartGameMusic(musicNum);
```

{{< lookup/cref SaveGameState >}} saves a snapshot of the current level's global variables into the temporary save slot (identified by the character `'T'`), which defines the restore point that will be subsequently used if the player dies and the level needs to restart with the score/health/etc. that the player had when they initially entered.

{{< lookup/cref StartGameMusic >}} loads and begins playing the map's chosen music (identified by {{< lookup/cref musicNum >}}) from the beginning. If there is no AdLib hardware installed or the music is disabled, this function skips doing some of that work.

```c
    if (!isAdLibPresent) {
        tileAttributeData = miscData + 5000;
        miscDataContents = IMAGE_TILEATTR;
        LoadTileAttributeData("TILEATTR.MNI");
    }
```

This code is the inverse implementation of a similar fragment found near the end of {{< lookup/cref Startup >}}. In this case, the `if` body is executed when the system does _not_ have an AdLib card installed ({{< lookup/cref isAdLibPresent >}} is false). The reason for this separation is for reasons of memory efficiency: If the system does not have an AdLib card, there is no need to load any music data into the memory backed by {{< lookup/cref miscData >}} and that space can be repurposed to hold [tile attribute data]({{< relref "tile-attributes-format" >}}) instead. (Otherwise, when {{< lookup/cref miscData >}} is holding music, there is a separate allocation of memory that {{< lookup/cref tileAttributeData >}} permanently points to.)

Here {{< lookup/cref miscData >}} points to a 35,000 byte arena of memory, where the first 5,000 bytes are reserved for [demo data]({{< relref "demo-format" >}}) that may be playing or being recorded. The {{< lookup/cref tileAttributeData >}} pointer is set to the first byte past the end of this data. {{< lookup/cref miscDataContents >}} is set to {{< lookup/cref name="IMAGE" text="IMAGE_TILEATTR" >}} to mark that this memory has been claimed for this purpose. Finally, {{< lookup/cref LoadTileAttributeData >}} loads the data from the named [group entry]({{< relref "group-file-format" >}}) into this memory.

```c
    FadeIn();
```

At this point in the execution, the screen is faded to black via palette manipulation, but the video memory contains a black game window with an initialized status bar at the bottom of the screen. The call to {{< lookup/cref FadeIn >}} fades this into view. {{< lookup/cref FadeIn >}} blocks until completion, so the initialization does not proceed (and the game loop does not start) until after it returns.

```c
#ifdef EXPLOSION_PALETTE
    if (paletteAnimationNum == PAL_ANIM_EXPLOSIONS) {
        SetPaletteRegister(PALETTE_KEY_INDEX, MODE1_BLACK);
    }
#endif
}
```

There is one last bit of palette manipulation that occurs in episode three, which is the only episode with the `EXPLOSION_PALETTE` macro defined. In this episode, the level's {{< lookup/cref paletteAnimationNum >}} is checked to see if it matches {{< lookup/cref name="PAL_ANIM" text="PAL_ANIM_EXPLOSIONS" >}}, in which case the special "flash during explosions" palette animation mode is activated. In this mode, all magenta areas of the screen show as black by default, but flash bright white and yellow while explosions occur. To facilitate the initial state for this mode, {{< lookup/cref SetPaletteRegister >}} is called to set the palette register named by {{< lookup/cref PALETTE_KEY_INDEX >}} (which represents magenta areas in the game's graphics) to the EGA's {{< lookup/cref name="MODE1_COLORS" text="MODE1_BLACK" >}} color.

{{< boilerplate/function-cref InitializeMapGlobals >}}

The {{< lookup/cref InitializeMapGlobals >}} function resets many of the global variables pertaining to player movement and map/actor interactivity. This function is called whenever a level begins and ensures it has a consistent and clean state, with nothing from the previous level carried over.

```c
void InitializeMapGlobals(void)
{
    winGame = false;
    playerClingDir = DIR4_NONE;
    isPlayerFalling = true;
    cmdJumpLatch = true;
    playerJumpTime = 0;
    playerFallTime = 1;
    isPlayerRecoiling = false;
    playerMomentumNorth = 0;
    playerFaceDir = DIR4_EAST;
    playerFrame = PLAYER_WALK_1;
    playerBaseFrame = PLAYER_BASE_EAST;
    playerDeadTime = 0;
    winLevel = false;
    playerHurtCooldown = 40;
    transporterTimeLeft = 0;
    activeTransporter = 0;
    isPlayerInPipe = false;
    scooterMounted = 0;
    isPlayerNearTransporter = false;
    isPlayerNearHintGlobe = false;
    areForceFieldsActive = true;
    blockMovementCmds = false;

    ClearPlayerDizzy();

    blockActionCmds = false;
    arePlatformsActive = true;
    isPlayerInvincible = false;
    paletteStepCount = 0;
    randStepCount = 0;
    playerFallDeadTime  = 0;
    sawHurtBubble  = false;
    sawAutoHintGlobe = false;
    numBarrels = 0;
    numEyePlants = 0;
    pounceStreak = 0;

    sawJumpPadBubble =
        sawMonumentBubble =
        sawScooterBubble =
        sawTransporterBubble =
        sawPipeBubble =
        sawBossBubble =
        sawPusherRobotBubble =
        sawBearTrapBubble =
        sawMysteryWallBubble =
        sawTulipLauncherBubble =
        sawHamburgerBubble = false;
}
```

This function contains no logic and behaves identically in every context where it is run. It sets the following variables:

* {{< lookup/cref winGame >}} is set to false, ensuring that the player must reach an episode-specific goal to complete the game and see the end story.
* {{< lookup/cref playerClingDir >}} is set to {{< lookup/cref name="DIR4" text="DIR4_NONE" >}}, indicating that the player is not currently clinging to any walls. In this state, the player is standing on solid ground (or possibly free-falling toward it).
* {{< lookup/cref isPlayerFalling >}} is set to true, which simplifies the interaction between the player's starting position and the various movement variables that control the player. The game assumes that the player starts every map in empty space, ready to free-fall. Whenever the player is free-falling, the {{< lookup/cref MovePlayer >}} function continually tries to pull the player down until they land on a solid map tile. If the player's start position should happen to be on such a map tile already, the free-fall will be canceled and the player will be switched to a standing state immediately.
* {{< lookup/cref cmdJumpLatch >}} = true <!-- TODO Continue describing map global initialization -->
* {{< lookup/cref playerJumpTime >}} = 0
* {{< lookup/cref playerFallTime >}} = 1
* {{< lookup/cref isPlayerRecoiling >}} = false
* {{< lookup/cref playerMomentumNorth >}} = 0 <!-- END -->
* {{< lookup/cref playerFaceDir >}} is set to {{< lookup/cref name="DIR4" text="DIR4_EAST" >}}, which makes the player start each level facing east. By convention, the player usually starts toward the left side of the map, looking in the direction they need to travel to progress.
* {{< lookup/cref playerFrame >}} is set to {{< lookup/cref name="PLAYER" text="PLAYER_WALK_1" >}}, but this assignment is not that important since this value will be immediately overwritten with the correct standing/falling frame during the next call to {{< lookup/cref MovePlayer >}}.
* {{< lookup/cref playerBaseFrame >}} is set to {{< lookup/cref name="PLAYER_BASE" text="PLAYER_BASE_EAST" >}}, following the same motivations as {{< lookup/cref playerFaceDir >}} above.
* {{< lookup/cref playerDeadTime >}} is set to zero, indicating that the player has not died yet.
* {{< lookup/cref winLevel >}} is set to false, ensuring that the player must reach a map-specific goal to complete the level and progress to the next one.
* {{< lookup/cref playerHurtCooldown >}} is initialized to 40. This makes the player invincible for roughly the first four seconds of gameplay to allow them to get situated in their surroundings without taking damage. This invincibility is accompanied by the player sprite flashing.
* {{< lookup/cref transporterTimeLeft >}} is set to zero, since the player is not using any transporters at the start of the level.
* {{< lookup/cref activeTransporter >}} is set to zero, indicating that there is currently no transporter actor being interacted with.
* {{< lookup/cref isPlayerInPipe >}} is set to false, conceptually placing the player "outside" the pipe system where the pipe corner actors will have no effect.
* {{< lookup/cref scooterMounted >}} is set to zero, ensuring the player enters every map without a scooter.
* {{< lookup/cref isPlayerNearTransporter >}} and {{< lookup/cref isPlayerNearHintGlobe >}} are both set to false, since the player should not be touching either of these actor types when entering a level.
* {{< lookup/cref areForceFieldsActive >}} is set to true. The game's design is such that force fields are _always_ active when a level is started, and can only be deactivated by using the {{< lookup/actor 121 >}}.
* {{< lookup/cref blockMovementCmds >}} is set to false, allowing the player to walk and jump freely.
* {{< lookup/cref ClearPlayerDizzy >}} is called to reset the state variables pertaining to the "dizzy" immobilization the player can sometimes experience.
* {{< lookup/cref blockActionCmds >}} is set to false, allowing the player to be moved freely.
* {{< lookup/cref arePlatformsActive >}} is set to true, specifying that all platforms on the map are active and moving by default. As the map is loaded, the presence of a {{< lookup/actor 59 >}} may turn this off, requiring the player to find and interact with that switch to make the platforms run again.
* {{< lookup/cref isPlayerInvincible >}} is set to false, since the player will not have an {{< lookup/actor 201 >}} to start with.
* {{< lookup/cref paletteStepCount >}} is set to zero, ensuring that any palette animations used on the current map start at the beginning of their color sequence.
* {{< lookup/cref randStepCount >}} is set to zero, which resets the pseudorandom number generator in {{< lookup/cref GameRand >}} to a predictable and stable state. This is critically important to ensure that actors that use randomness behave identically during demo recording and playback.
* {{< lookup/cref playerFallDeadTime >}} is set to zero, indicating that the player has not fallen off the bottom of the map yet.
* {{< lookup/cref sawHurtBubble >}} is set to false, allowing the "OUCH!" bubble to show once the player is hurt for the first time.
* {{< lookup/cref sawAutoHintGlobe >}} is set false, which will auto-activate the first hint globe the player happens to touch.
* {{< lookup/cref numBarrels >}} and {{< lookup/cref numEyePlants >}} are both set to zero. These variables track the number of barrels/baskets and the number of {{< lookup/actor type=95 strip=1 plural=1 >}} on the map, respectively. Since each map initially loads with zero actors of any type, zero is appropriate here.
* {{< lookup/cref pounceStreak >}} is set to zero, eliminating any chance of a carryover of the previous map's pounce streak.
* All of the speech bubble flags -- {{< lookup/cref sawJumpPadBubble >}}, {{< lookup/cref sawMonumentBubble >}}, {{< lookup/cref sawScooterBubble >}}, {{< lookup/cref sawTransporterBubble >}}, {{< lookup/cref sawPipeBubble >}}, {{< lookup/cref sawBossBubble >}}, {{< lookup/cref sawPusherRobotBubble >}}, {{< lookup/cref sawBearTrapBubble >}}, {{< lookup/cref sawMysteryWallBubble >}}, {{< lookup/cref sawTulipLauncherBubble >}}, and {{< lookup/cref sawHamburgerBubble >}} -- are set to false. This re-enables the speech bubbles (generally "WHOA!" but occasionally "UMPH!") that appear when the player first interacts with each of these actor types.

{{< boilerplate/function-cref GameLoop >}}

The {{< lookup/cref GameLoop >}} function runs once for each frame of gameplay and is responsible for running the appropriate sub-functions for timing, input, player/actor movement, world drawing, and level exit conditions. This function takes a `demo_state` argument which should be one of the {{< lookup/cref DEMO_STATE >}} constants -- this controls the presence of the "DEMO" overlay sprite and is passed through to the input handling functions.

The game loop is structured as a true infinite loop that can only terminate under the following conditions:

1. The user presses one of the "quit game" keys and confirms their choice at the prompt. In this case the loop exits immediately with a `return` statement.
2. The episode is "won." In this case, the loop exits due to a `break` statement and the ending story is shown before this function returns.

In either case, this function returns back to the title loop in the {{< lookup/cref InnerMain >}} function.

### Overall Structure

```c
void GameLoop(byte demo_state)
{
    for (;;) {
        while (gameTickCount < 13)
            ;  /* VOID */

        gameTickCount = 0;

        /* ... Sub-function calls are discussed below ... */

        if (winLevel) {
            winLevel = false;
            StartSound(SND_WIN_LEVEL);
            NextLevel();
            InitializeLevel(levelNum);
        } else if (winGame) {
            break;
        }
    }

    ShowEnding();
}
```

Only the outermost structure of the game loop is shown here for clarity. Almost the entire function is contained inside the body of an infinite `for` loop. On each iteration, the value of {{< lookup/cref gameTickCount >}} is checked, and execution only proceeds once the count reaches 13. (This counter is incremented externally in the {{< lookup/cref PCSpeakerService >}} function, which is called by a timer interrupt 140 times per second.) This busy loop ensures that the game waits _at least_ 13 &#8725; 140 seconds between successive frames, effectively creating a frame-rate limiter a bit shy of 11 frames per second. Once the requisite amount of time has passed, {{< lookup/cref gameTickCount >}} is reset to zero to set up for the delay on the subsequent iteration and the rest of the game loop body runs.

For a fast computer that can draw a frame quickly, this loop eats up the remaining unused time before another loop iteration is allowed to start. On a very slow computer, it's possible for {{< lookup/cref gameTickCount >}} to be at or above 13 by the time the next game loop iteration is entered, resulting in no busy wait at all. In these cases, the gameplay will appear noticeably sluggish because there are no mechanisms in place to skip frames or adjust the movement speeds of objects.

After the timing loop, the sub-functions are called. They are discussed [below](#sub-functions).

Near the end of the loop body, a check is made against the {{< lookup/cref winLevel >}} flag. If it holds a true value, the player interacted with a level-winning object on the map during the current iteration. When this happens, the {{< lookup/cref winLevel >}} is set back to false, the {{< lookup/cref name="SND" text="SND_WIN_LEVEL" >}} fanfare is queued via a call to {{< lookup/cref StartSound >}}, and the next level number is selected by {{< lookup/cref NextLevel >}}. This has the side-effect of changing the value in {{< lookup/cref levelNum >}}. That new level number is passed to {{< lookup/cref InitializeLevel >}}, which loads the new map data and reinitializes all of the relevant global state to make it playable from the beginning. On the next iteration of the game loop, the player will be in the starting position of that new map with fresh actors to face.

A different exit condition can be reached when {{< lookup/cref winGame >}} is true, in which case the player has qualified to win the entire episode of the game during the current iteration of the game loop. In this case, execution `break`s out of the infinite `for` loop and falls to the {{< lookup/cref ShowEnding >}} call. This shows the relevant end story for the episode being played, and the {{< lookup/cref GameLoop >}} function returns once the story has been shown to completion.

### Sub-Functions

During each iteration of the outer infinite `for` loop, after the timing loop and before the end-level checks, the bulk of the function calls occur. There is very little logic done in the game loop itself; almost everything is handled in a function specific to each of the game's subsystems.

```c
        AnimatePalette();
```

If the current map has enabled one of the [palette animation modes]({{< relref "databases/palette-animation" >}}), each call to {{< lookup/cref AnimatePalette >}} will "step" the animation to the next color defined in the sequence and change the visual representation of the magenta areas on the screen.

```c
        {  /* for scope */
            word result = ProcessGameInputHelper(activePage, demo_state);
            if (result == GAME_INPUT_QUIT) return;
            if (result == GAME_INPUT_RESTART) continue;
        }

        MovePlayer();

        if (scooterMounted != 0) {
            MovePlayerScooter();
        }

        if (queuePlayerDizzy || playerDizzyLeft != 0) {
            ProcessPlayerDizzy();
        }
```

This section handles the input devices (keyboard, joystick, or the demo system) and moves the player through the map in response.

{{< lookup/cref ProcessGameInputHelper >}} performs input handling based on the value passed in `demo_state`. In the case where a demo is being played back, input is ignored except as a signal to quit. Otherwise input is accepted and used for player movement. {{< lookup/cref ProcessGameInputHelper >}} can also display [menus]({{< relref "menu-functions" >}}) and [dialogs]({{< relref "dialog-functions" >}}). To do this it must bypass the usual page-flipping mechanism and draw directly to the video page in {{< lookup/cref activePage >}} -- that is why it is passed here.

{{< lookup/cref ProcessGameInputHelper >}} returns a `result` code that can exit or restart the game loop. In the case of {{< lookup/cref name="GAME_INPUT" text="GAME_INPUT_QUIT" >}}, the user has requested to quit the game with <kbd>Esc</kbd> or <kbd>Q</kbd>, finished/dismissed the playback of a demo, or ran out of space while recording a demo. For these cases, `return` from the game loop immediately. For {{< lookup/cref name="GAME_INPUT" text="GAME_INPUT_RESTART" >}}, either a saved game was restored or the level warp cheat was used. In either case, the global state of the game world has changed and the game loop must be restarted from the top; `continue` accomplishes this.

The call to {{< lookup/cref MovePlayer >}} interprets the raw movement commands read from the input device and uses them to adjust the position of the player in the game world. This is a heinously complicated function with one simple to understand precondition -- if the player happens to be riding a scooter, it returns without doing anything.

The game loop checks the player's scooter state by reading {{< lookup/cref scooterMounted >}}. If it has a nonzero value, the scooter is active and {{< lookup/cref MovePlayerScooter >}} should be called to invoke the alternate, slightly simpler player movement logic.

The player can sometimes become temporarily "dizzy" by exiting a pipe system or falling from a great distance. This condition can be detected by either the {{< lookup/cref queuePlayerDizzy >}} flag being true or the {{< lookup/cref playerDizzyLeft >}} counter having a nonzero value. In either case, the {{< lookup/cref ProcessPlayerDizzy >}} function is called to do the per-frame bookkeeping for this state.

```c
        MovePlatforms();
        MoveFountains();
```

The combination of {{< lookup/cref MovePlatforms >}} and {{< lookup/cref MoveFountains >}} calls take care of moving map elements that the player can stand and walk on. These movements need to happen relatively early because the player's position can be adjusted if they happen to be standing on top of one of these during this frame.

```c
        DrawMapRegion();
        if (DrawPlayerHelper()) continue;
        DrawFountains();
```

This is the first point during a regular iteration of the game loop where something is drawn to the screen. {{< lookup/cref DrawMapRegion >}} draws the _entire_ map visible map area -- solid tiles, masked tiles, and the backdrop behind empty areas -- over the game window based on the current X and Y scroll position. This fully erases everything that was left over in the video memory on the draw page. Platforms are regular solid tiles in the map memory that move around, so they are drawn as part of this function. Fountains contain no visible map tiles, so they are hidden at this point. (The player can still stand on these invisible tiles, however.)

The {{< lookup/cref DrawPlayerHelper >}} ultimately draws the player sprite onto the screen, but also does some per-frame checks to handle the player's response to being hurt. Most notably, if the player dies or falls off the map, {{< lookup/cref DrawPlayerHelper >}} reloads the current level and returns true to request a game loop restart (`continue`). Anything drawn after this point can cover the player sprite, including all actors and visual effects.

{{< lookup/cref DrawFountains >}} draws the necessary sprite tiles onto the screen to show any fountains within the scrolling game window, even if the player is not currently interacting with any.

```c
        MoveAndDrawActors();
        MoveAndDrawShards();
        MoveAndDrawSpawners();
        DrawRandomEffects();
        DrawExplosions();
        MoveAndDrawDecorations();
        DrawLights();
```

This is the "everything else" section of object movement and drawing. Some objects do not move (e.g. explosions and lights) but all are drawn at this time, in this order:

* {{< lookup/cref MoveAndDrawActors >}} updates the position of every "awake" actor on the map, including ones that may be off a screen edge. Sprites are drawn for those visible within the scrolling game window.
* {{< lookup/cref MoveAndDrawShards >}} updates the positions and draws all the sprites belonging to any shards that are visible. Those that are fully off the screen are stopped and removed.
* {{< lookup/cref MoveAndDrawSpawners >}} updates and draws all spawning objects, and creates new actor objects once each spawner's lifecycle is complete.
* {{< lookup/cref DrawRandomEffects >}} draws random sparkles on slippery areas of the map, and spawns raindrops if the map requires them.
* {{< lookup/cref DrawExplosions >}} animates a successive frame of each active explosion visible on the screen and draws the corresponding sprite.
* {{< lookup/cref MoveAndDrawDecorations >}} handles the movement, animation, and looping properties of every decoration visible inside the game window. The sprite for each is drawn in the process. Decorations are stopped and removed once their loop count runs out or they leave the visible screen area.
* {{< lookup/cref DrawLights >}} handles the special map actors that represent lighted areas of the map. Such lights shine "down" the screen and continue until they hit a solid map tile (or they reach a hard-coded maximum distance). Anything currently drawn on the screen at this point can be "lightened" if one of these light beams touches it.

```c
        if (demoState != DEMO_STATE_NONE) {
            DrawSprite(SPR_DEMO_OVERLAY, 0, 18, 4, DRAW_MODE_ABSOLUTE);
        }
```

If a demo is being recorded _or_ played back, {{< lookup/cref demoState >}} will have a value other than {{< lookup/cref name="DEMO_STATE" text="DEMO_STATE_NONE" >}}. In this case, {{< lookup/cref DrawSprite >}} draws frame zero of the {{< lookup/cref name="SPR" text="SPR_DEMO_OVERLAY" >}} "DEMO" sprite on the screen. This call uses the screen-relative {{< lookup/cref name="DRAW_MODE" text="DRAW_MODE_ABSOLUTE" >}}, so the coordinates (18, 4) represent a fixed position near the center-top of the game window. This is the last thing drawn during a typical iteration of the game loop, and nothing should subsequently cover it.

```c
        SelectDrawPage(activePage);
        activePage = !activePage;
        SelectActivePage(activePage);
```

This is the page-flipping. Up until this point, all of the drawing had been directed at the "draw" page, which is the opposite of the "active" page that is currently being shown on the screen. {{< lookup/cref SelectDrawPage >}} is called with {{< lookup/cref activePage >}} as the argument, informing the [drawing functions]({{< relref "assembly-drawing-functions" >}}) that they should subsequently draw to the area of video memory that is currently on the screen.

Immediately after that, {{< lookup/cref activePage >}} is inverted to select the page that is _not_ targeted by the drawing functions. This value is then passed to {{< lookup/cref SelectActivePage >}}, which switches the content on the screen to the opposite page. This immediately makes visible everything that had been drawn in this iteration of the game loop, while also giving the _next_ iteration of the game loop an area of video memory where it can perform its drawing work without it being visible on the screen.

```c
        if (pounceHintState == POUNCE_HINT_QUEUED) {
            pounceHintState = POUNCE_HINT_SEEN;
            ShowPounceHint();
        }
```

A conceivably late addition to the game loop is this pounce hint check. If the value in {{< lookup/cref pounceHintState >}} is equal to {{< lookup/cref name="POUNCE_HINT" text="POUNCE_HINT_QUEUED" >}}, something occurred during the current iteration of the game loop to warrant displaying the pounce hint dialog. Update {{< lookup/cref pounceHintState >}} to {{< lookup/cref name="POUNCE_HINT" text="POUNCE_HINT_SEEN" >}} so this cannot recur, then call {{< lookup/cref ShowPounceHint >}} to show the dialog.

{{< aside class="armchair-engineer" >}}
**Queue you!**

The queuing implementation used here is probably not necessary; the behavior of the health hints in {{< lookup/cref TouchPlayer >}} demonstrates a more direct way to do this. The placement here suggests that maybe an older version of this function interacted badly with the page-flipping, perhaps appearing and pausing gameplay with some of the actors not yet drawn for the current frame.
{{< /aside >}}

{{< boilerplate/function-cref ProcessGameInputHelper >}}

The {{< lookup/cref ProcessGameInputHelper >}} function is a small wrapper around the {{< lookup/cref ProcessGameInput >}} function that prepares the video hardware for the possibility of showing a menu or dialog during the [game loop](#GameLoop). `active_page` should contain the "active" (i.e. currently displayed) video page number, and `demo_state` should hold one of the {{< lookup/cref DEMO_STATE >}} values.

```c
byte ProcessGameInputHelper(word active_page, byte demo_state)
{
    byte result;

    EGA_MODE_LATCHED_WRITE();

    SelectDrawPage(active_page);

    result = ProcessGameInput(demo_state);

    SelectDrawPage(!active_page);

    return result;
}
```

This function is effectively a wrapper around {{< lookup/cref ProcessGameInput >}}, passing the `demo_state` value directly through and returning its `result` without modification. This function exists to prepare the video hardware for certain drawing operations that {{< lookup/cref ProcessGameInput >}} may need to do.

{{< lookup/cref EGA_MODE_LATCHED_WRITE >}} puts the EGA hardware into "latched" write mode. This is the mode used when drawing solid tile images, since these are stored in the EGA's onboard memory and need to use the latches to copy data onto a video page.

{{< aside class="armchair-engineer" >}}
**Work harder, not smarter.**

The call to {{< lookup/cref EGA_MODE_LATCHED_WRITE >}} is _arguably_ not needed, since all of the dialog/menu functions that can be invoked during the game ultimately call {{< lookup/cref DrawTextFrame >}} which sets the EGA mode anyway. It could also be argued that, since most of the frames drawn by the game loop never show a menu or dialog in the first place, performing this call on every loop iteration is simply a waste of clock cycles.
{{< /aside >}}

The call to {{< lookup/cref SelectDrawPage >}} sets the draw page -- that is, the area of video memory that is visible on the screen _right now_ -- to `active_page`. This sets it up so that any subsequent drawing operation goes directly and immediately to the screen, visible to the user without page flipping coming into play.

In this state, anything drawn inside {{< lookup/cref ProcessGameInput >}} and the functions it calls are immediately visible.

Once the input handling is done, {{< lookup/cref SelectDrawPage >}} is called again with the inverse of `page` as the argument. This resets the draw page back to the way it was when the function was first entered, and leaves the hardware in the "draw everything in a hidden buffer" mode it expects.

Finally, the original return value of {{< lookup/cref ProcessGameInput >}}, stashed in `result`, is returned to the caller.

{{< boilerplate/function-cref ProcessGameInput >}}

The {{< lookup/cref ProcessGameInput >}} function handles all keyboard and joystick input while the game is being played. Depending on the value passed in `demo_state` (which should be one of the {{< lookup/cref DEMO_STATE >}} values), this behavior is modified to record or play back demo data. Returns one of the {{< lookup/cref GAME_INPUT >}} values to control the game loop's flow.

In addition to setting up player movment, this function also calls the in-game menus and dialogs for game options and cheat keys.

```c
byte ProcessGameInput(byte demo_state)
{
    if (demo_state != DEMO_STATE_PLAY) {
```

This function does the most work when the passed `demo_state` is not {{< lookup/cref name="DEMO_STATE" text="DEMO_STATE_PLAY" >}}. This state is encountered when the player is playing the game normally or recording a demo. Later the `else` block will handle the demo playback case.

```c
        if (
            isKeyDown[SCANCODE_TAB] && isKeyDown[SCANCODE_F12] &&
            isKeyDown[SCANCODE_KP_DOT]  /* Del */
        ) {
            isDebugMode = !isDebugMode;
            StartSound(SND_PAUSE_GAME);
            WaitHard(90);
        }
```

If the user is pressing the <kbd>Tab</kbd> + <kbd>F12</kbd> + <kbd>Del / Num .</kbd> debug key combination during the current frame, they want to toggle the state of the debug mode. The key state is read from the {{< lookup/cref isKeyDown >}} array indexed by the appropriate {{< lookup/cref SCANCODE >}} values, with the "delete" key sharing a scancode with the "dot" on the numeric keybad. When this key combination is down, {{< lookup/cref isDebugMode >}} is toggled and {{< lookup/cref StartSound >}} plays the {{< lookup/cref name="SND" text="SND_PAUSE_GAME" >}} effect to give feedback that the input was accepted.

To give the user a chance to release the keys without unintentionally toggling the debug mode further, {{< lookup/cref WaitHard >}} pauses the entire game for a bit over half a second.

```c
        if (isKeyDown[SCANCODE_F10] && isDebugMode) {
```

This `if` block handles the <kbd>F10</kbd> + ... debug keys. {{< lookup/cref isDebugMode >}} must be true for <kbd>F10</kbd> to have significance to the game.

```c
            if (isKeyDown[SCANCODE_G]) {
                ToggleGodMode();
            }
```

In the case of <kbd>F10</kbd> + <kbd>G</kbd>, the user wants to toggle the state of the god mode cheat. {{< lookup/cref ToggleGodMode >}} does that and displays the dialog showing the result of the change.

```c
            if (isKeyDown[SCANCODE_W]) {
                if (PromptLevelWarp()) return GAME_INPUT_RESTART;
            }
```

For In the case of <kbd>F10</kbd> + <kbd>W</kbd>, the user wants to warp to a different level. {{< lookup/cref PromptLevelWarp >}} collects that input. If the user cancels or enters a nonsense value, {{< lookup/cref PromptLevelWarp >}} will return false and execution here will continue uninterrupted.

In the case where the user selected a valid level number, that level will be loaded and initialized then {{< lookup/cref PromptLevelWarp >}} returns true. In that case, {{< lookup/cref name="GAME_INPUT" text="GAME_INPUT_RESTART" >}} is returned here to indicate that the game loop must restart on this new level.

```c
            if (isKeyDown[SCANCODE_P]) {
                StartSound(SND_PAUSE_GAME);
                while (isKeyDown[SCANCODE_P])
                    ;  /* VOID */
                while (!isKeyDown[SCANCODE_P])
                    ;  /* VOID */
                while (isKeyDown[SCANCODE_P])
                    ;  /* VOID */
            }
```

When the user presses <kbd>F10</kbd> + <kbd>P</kbd>, the game pauses _without_ any UI elements covering up any part of the screen. {{< lookup/cref StartSound >}} plays the {{< lookup/cref name="SND" text="SND_PAUSE_GAME" >}} effect as an indication that this is a pause and not some kind of program crash, then a series of `while` loops is entered.

The first `while` loop spins, performing no work for as long as the <kbd>P</kbd> key is pressed. This absorbs the initial keypress that brought the program into the pause mode. The keyboard interrupt handler is called as keys are pressed and released, which updates the values in the {{< lookup/cref isKeyDown >}} array while this loop runs.

The second `while` loop comprises the bulk of the pause. The program waits here for as long as the user wants to stay.

The third `while` loop is entered when the <kbd>P</kbd> key is pressed again (it does not need to be accompanied with <kbd>F10</kbd> here). This keeps the game paused while <kbd>P</kbd> is pressed this second time, unpausing and resuming execution as soon as the key is released.

The combined effect of these three loops is a **latch**. The game pauses on the first _press_ of the <kbd>F10</kbd> + <kbd>P</kbd> combination, and does not unpause until the <kbd>P</kbd> key is pressed _and released_ a subsequent time.

```c
            if (isKeyDown[SCANCODE_M]) {
                ShowMemoryUsage();
            }
```

In the case of <kbd>F10</kbd> + <kbd>M</kbd>, the user wants to see the memory usage statistics. {{< lookup/cref ShowMemoryUsage >}} handles that display.

```c
            if (
                isKeyDown[SCANCODE_E] &&
                isKeyDown[SCANCODE_N] &&
                isKeyDown[SCANCODE_D]
            ) {
                winGame = true;
            }
        }
```

If the user presses the (convoluted) <kbd>F10</kbd> + <kbd>E</kbd> + <kbd>N</kbd> + <kbd>D</kbd> combination, the episode is immediately "won" by setting {{< lookup/cref winGame >}} to true, informing the game loop that it should stop running and instead display the ending story.

This is the final check for <kbd>F10</kbd> debug keys, and the `if` block from above ends.

```c
        if (
            isKeyDown[SCANCODE_C] &&
            isKeyDown[SCANCODE_0] &&
            isKeyDown[SCANCODE_F10] &&
            !usedCheatCode
        ) {
            StartSound(SND_PAUSE_GAME);
            usedCheatCode = true;
            ShowCheatMessage();
            playerHealthCells = 5;
            playerBombs = 9;
            sawBombHint = true;
            playerHealth = 6;
            UpdateBombs();
            UpdateHealth();
        }
```

This is the <kbd>C</kbd> + <kbd>0</kbd> + <kbd>F10</kbd> customer cheat, invoked by seeing the correct combination of keys in the {{< lookup/cref isKeyDown >}} array. {{< lookup/cref usedCheatCode >}} must be false here, which prevents the user from requesting this cheat more than once during the course of an episode.

{{< lookup/cref StartSound >}} queues the {{< lookup/cref name="SND" text="SND_PAUSE_GAME" >}} effect, which continues playing on top of the subsequent cheat message. {{< lookup/cref usedCheatCode >}} is set to true, making this a one-shot operation unless the episode is restarted. The call to {{< lookup/cref ShowCheatMessage >}} explains what is happening before further changes occur.

Once the message is dismissed, the player is given five bars of available health when {{< lookup/cref playerHealthCells >}} is set to 5. These bars become filled when {{< lookup/cref playerHealth >}} is set to _6_. The player is also given nine bombs (the maximum permitted) with {{< lookup/cref playerBombs >}}`= 9`. This also sets the {{< lookup/cref sawBombHint >}} flag, which prevents the bomb hint from showing again during the episode. (Usually, this hint is disabled when the player picks up their first bomb -- the assignment here covers the case where the player cheated before picking any up.)

After the changes are made, a pair of calls to {{< lookup/cref UpdateBombs >}} and {{< lookup/cref UpdateHealth >}} makes the changes visible in the status bar.

```c
        if (isKeyDown[SCANCODE_S]) {
            ToggleSound();
        } else if (isKeyDown[SCANCODE_M]) {
            ToggleMusic();
        } else if (isKeyDown[SCANCODE_ESC] || isKeyDown[SCANCODE_Q]) {
            if (PromptQuitConfirm()) return GAME_INPUT_QUIT;
```

These are the in-game keys. At any point during gameplay, the <kbd>S</kbd> key toggles sound, <kbd>M</kbd> toggles music, and <kbd>Esc</kbd>/<kbd>Q</kbd> brings up a "quit game" confirmation.

Each of these keys is checked via the {{< lookup/cref isKeyDown >}} array, indexed by the selected {{< lookup/cref SCANCODE >}} value. Sound and music is toggled (and the resulting state shown) by the {{< lookup/cref ToggleSound >}} and {{< lookup/cref ToggleMusic >}} functions, respectively.

The quit confirmation is shown in {{< lookup/cref PromptQuitConfirm >}}, and returns true if the user said yes. This returns {{< lookup/cref name="GAME_INPUT" text="GAME_INPUT_QUIT" >}} to the game loop, terminating it. If the user cancels, nothing is returned here and execution continues.

```c
        } else if (isKeyDown[SCANCODE_F1]) {
            byte result = ShowHelpMenu();
            if (result == HELP_MENU_RESTART) {
                return GAME_INPUT_RESTART;
            } else if (result == HELP_MENU_QUIT) {
                if (PromptQuitConfirm()) return GAME_INPUT_QUIT;
            }
```

This block handles the case where the <kbd>F1</kbd> key is pressed. This is advertised in the status bar as the "help" key, which presents a menu with a few configuration options and help screens. {{< lookup/cref ShowHelpMenu >}} is responsible for showing this menu and dispatching to all of the available sub-options. When the menu is dismissed, a `result` byte is returned.

The game menu is capable of changing the level being played (by restoring a saved game) or quitting the game. These states need to be passed up to the game loop, which could restart or terminate based on this information.

Internally, there is a mismatch in the numbering scheme used by {{< lookup/cref HELP_MENU >}} and {{< lookup/cref GAME_INPUT >}}, which is why the result value needs to be translated. {{< lookup/cref name="HELP_MENU" text="HELP_MENU_RESTART" >}} becomes {{< lookup/cref name="GAME_INPUT" text="GAME_INPUT_RESTART" >}} while {{< lookup/cref name="HELP_MENU" text="HELP_MENU_QUIT" >}} -- if confirmed by {{< lookup/cref PromptQuitConfirm >}} -- becomes {{< lookup/cref name="GAME_INPUT" text="GAME_INPUT_QUIT" >}}.

In other cases, `result` contains a value that needs no special handling, and execution continues with no further modification of the game loop's execution flow.

```c
        } else if (isKeyDown[SCANCODE_P]) {
            StartSound(SND_PAUSE_GAME);
            ShowPauseMessage();
        }
```

The final game key is <kbd>P</kbd>, which pauses the game with a sound effect and a visible message. This is produced by a combination of {{< lookup/cref StartSound >}} ({{< lookup/cref name="SND" text="SND_PAUSE_GAME" >}}) and the accompanying {{< lookup/cref ShowPauseMessage >}}.

```c
    } else if ((inportb(0x0060) & 0x80) == 0) {
        return GAME_INPUT_QUIT;
    }
```

This is the `else` branch of the `demo_state` check near the start of the function. This path is taken when a demo is being played back. The condition is a copy of the {{< lookup/cref IsAnyKeyDown >}} implementation, with the technical details discussed in the documentation for that function.

This causes {{< lookup/cref name="GAME_INPUT" text="GAME_INPUT_QUIT" >}} to be returned to the game loop when any key is pressed, providing a way for the user to quit demo playback at any point by pressing a key.

```c
    if (demo_state != DEMO_STATE_PLAY) {
```

This is a duplicate of the larger `if` in the first half of the function -- running the first body if the game is being played normally (or a demo is being recorded), and the second body while playing a demo back.

```c
        if (!isJoystickReady) {
            cmdWest  = isKeyDown[scancodeWest] >> blockMovementCmds;
            cmdEast  = isKeyDown[scancodeEast] >> blockMovementCmds;
            cmdJump  = isKeyDown[scancodeJump] >> blockMovementCmds;
            cmdNorth = isKeyDown[scancodeNorth];
            cmdSouth = isKeyDown[scancodeSouth];
            cmdBomb  = isKeyDown[scancodeBomb];
        } else {
            ReadJoystickState(JOYSTICK_A);
        }
```

If {{< lookup/cref isJoystickReady >}} is false, the user is not using joystick input for player movement and the keyboard should be used instead. For each movement command, the configured scancode index ({{< lookup/cref scancodeWest >}}, {{< lookup/cref scancodeEast >}}, {{< lookup/cref scancodeJump >}}, {{< lookup/cref scancodeNorth >}}, {{< lookup/cref scancodeSouth >}}, and {{< lookup/cref scancodeBomb >}}) is read from the {{< lookup/cref isKeyDown >}} array and the key up/down state becomes the inactive/active state of that movement command.

{{< lookup/cref cmdWest >}}, {{< lookup/cref cmdEast >}}, and {{< lookup/cref cmdJump >}} have an additional processing step: If {{< lookup/cref blockMovementCmds >}} holds a nonzero (i.e. not-false) value, the boolean {{< lookup/cref isKeyDown >}} value is bitwist-shifted to the right. Since boolean false/true is equivalent to integer zero/nonzero, this functions as a boolean AND NOT expression -- the command variable is set if the key is down and commands are not blocked. {{< lookup/cref cmdNorth >}}, {{< lookup/cref cmdSouth >}}, and {{< lookup/cref cmdBomb >}} are not affected in this way because the player doesn't conceptually "move" for those inputs.

In the opposite case, {{< lookup/cref isJoystickReady >}} is true and joystick input _is_ being used. Don't process keyboard input at all, and instead call {{< lookup/cref ReadJoystickState >}} to read the movement commands from {{< lookup/cref name="JOYSTICK" text="JOYSTICK_A" >}}. Although {{< lookup/cref ReadJoystickState >}} returns a {{< lookup/cref JoystickState >}} structure with button press info, that return value is not used here -- all global variables are set without considering the return value.

{{< note >}}There is a bug here due to {{< lookup/cref blockMovementCmds >}} never being checked. It is possible for the player to walk or jump out of situations when using the joystick that they would not be able to while using the keyboard.{{< /note >}}

```c
        if (blockActionCmds) {
            cmdNorth = cmdSouth = cmdBomb = false;
        }
```

Regardless of the input device, if {{< lookup/cref blockActionCmds >}} is true, the {{< lookup/cref cmdNorth >}}, {{< lookup/cref cmdSouth >}}, and {{< lookup/cref cmdBomb >}} variables are all forced off, preventing the user from doing these actions.

```c
        if (demo_state == DEMO_STATE_RECORD) {
            if (WriteDemoFrame()) return GAME_INPUT_QUIT;
        }
```

If the user is recording a demo, `demo_state` will have the value {{< lookup/cref name="DEMO_STATE" text="DEMO_STATE_RECORD" >}}. This doesn't significantly change input handling; most inputs are processed identically. The difference here is that {{< lookup/cref WriteDemoFrame >}} is called during each frame to capture the state of the input commands.

{{< lookup/cref WriteDemoFrame >}} usually returns false, but can return true if the demo has been running for so long that the entire buffer has been filled (this takes seven to eight minutes to accomplish). When this happens, {{< lookup/cref name="GAME_INPUT" text="GAME_INPUT_QUIT" >}} tells the game loop to immediately quit -- nothing more can be stored.

```c
    } else if (ReadDemoFrame()) {
        return GAME_INPUT_QUIT;
    }
```

This is the opposite branch of the `demo_state` check, and is reached when a demo is being played back. In this case, {{< lookup/cref ReadDemoFrame >}} is called on every frame to fill the movement command variables from the stream of demo data.

{{< lookup/cref ReadDemoFrame >}} usually returns false, but will return true once the last frame of demo data has been read -- this is the end of the recording. When that happens, {{< lookup/cref name="GAME_INPUT" text="GAME_INPUT_QUIT" >}} tells the game loop to immediately quit -- the demo is over.

```c
    return GAME_INPUT_CONTINUE;
}
```

If execution ended up here, nothing special occurred during this frame: the user did not quit, the level was not changed, and a demo did not end. {{< lookup/cref name="GAME_INPUT" text="GAME_INPUT_CONTINUE" >}} tells the game loop that it should proceed with drawing the frame as usual.
