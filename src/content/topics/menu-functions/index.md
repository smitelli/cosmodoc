+++
title = "Menu Functions"
description = "Describes functions that display and handle the overall menu system."
weight = 360
+++

# Menu Functions

Throughout the game, the **menu system** allows the user to control the overall flow of the program. Each available command (begin game, restore saved game, view instructions, quit...) is handled by a separate function that is made available from the menu system.

{{< table-of-contents >}}

## Menu Progression

In this document, a distinction is made between a **menu** (which is conceptually a prompt that can receive different responses) and a **dialog** (which is a message that can only be dismissed or advanced through sequentially). The functions described here are menus; the dialogs are on a [separate page]({{< relref "dialog-functions" >}}).

### Title Loop

When the program starts, the **title loop** is entered. From here, several screens can be shown:

* Title Screen
* Credits
* Demo
* Main Menu

If the user does not press any keys, the title loop will show the title screen, credits, and demo in a loop. Once the demo completes, the title screen will be shown again and the loop continues indefinitely. If the loop is interrupted with a key press, the main menu is shown.

The main menu is typically shown over the title screen graphic, although it is possible to make it appear over the credits screen by pressing a key while the title loop is showing the credits. It is implemented in {{< lookup/cref TitleLoop >}} and {{< lookup/cref DrawMainMenu >}}. The following options are available:

{{< image src="main-2052x.png"
    alt="Main Menu"
    1x="main-684x.png"
    2x="main-1368x.png"
    3x="main-2052x.png" >}}

* <kbd>B</kbd>, <kbd>Enter</kbd>, or <kbd>Space</kbd>: Begin New Game
* <kbd>R</kbd>: [Restore A Game]({{< relref "#restore-game" >}})
* <kbd>S</kbd>: [Story]({{< relref "dialog-functions#ShowStory" >}})
* <kbd>I</kbd>: [Instructions]({{< relref "dialog-functions#ShowInstructions" >}}) (then [Hints]({{< relref "dialog-functions#ShowHintsAndKeys" >}}))
* <kbd>H</kbd>: [High Scores]({{< relref "#hall-of-fame" >}})
* <kbd>G</kbd>: [Game Redefine]({{< relref "#game-redefine-menu" >}})
* <kbd>O</kbd>: [Ordering Information]({{< relref "dialog-functions#ShowOrderingInformation" >}})
* <kbd>F</kbd>: [Foreign Orders]({{< relref "dialog-functions#ShowForeignOrders" >}}) (if shareware episode)
* <kbd>A</kbd>: [Apogee's BBS]({{< relref "dialog-functions#ShowPublisherBBS" >}})
* <kbd>D</kbd>: Demo
* <kbd>C</kbd>: Credits
* <kbd>T</kbd>: Title Screen
* <kbd>Q</kbd> or <kbd>Esc</kbd>: [Quit Game]({{< relref "#quit-game" >}})
* <kbd>F11</kbd>: If debug mode has been activated, starts [recording a demo]({{< relref "demo-format#recording-demos">}}).

### Help Menu

The help menu is accessible by pressing <kbd>F1</kbd> while the game is being played, and presents a subset of options:

{{< image src="help-2052x.png"
    alt="Help Menu"
    1x="help-684x.png"
    2x="help-1368x.png"
    3x="help-2052x.png" >}}

* <kbd>S</kbd>: [Save your game]({{< relref "#save-game" >}})
* <kbd>R</kbd>: [Restore a game]({{< relref "#restore-game" >}})
* <kbd>H</kbd>: Help (actually [Hints]({{< relref "dialog-functions#ShowHintsAndKeys" >}}))
* <kbd>G</kbd>: [Game redefine]({{< relref "#game-redefine-menu" >}})
* <kbd>V</kbd>: [View High Scores]({{< relref "#hall-of-fame" >}})
* <kbd>Q</kbd>: [Quit Game]({{< relref "#quit-game" >}})
* <kbd>Esc</kbd>: Return to the game

It is implemented in {{< lookup/cref ShowHelpMenu >}}.

### Game Redefine Menu

The game redefine menu is available from both the main menu and the in-game help menu, and allows a few options to be configured:

{{< image src="game-redefine-2052x.png"
    alt="Game Redefine Menu"
    1x="game-redefine-684x.png"
    2x="game-redefine-1368x.png"
    3x="game-redefine-2052x.png" >}}

* <kbd>K</kbd>: [Keyboard redefine]({{< relref "#keyboard-redefine" >}})
* <kbd>J</kbd>: [Joystick redefine]({{< relref "#joystick-redefine" >}})
* <kbd>S</kbd>: [Sound toggle]({{< relref "dialog-functions#ToggleSound" >}})
* <kbd>T</kbd>: [Test sound]({{< relref "#test-sound" >}})
* <kbd>M</kbd>: [Music toggle]({{< relref "dialog-functions#ToggleMusic" >}}))
* <kbd>Esc</kbd>: Dismiss the menu

It is implemented in {{< lookup/cref ShowGameRedefineMenu >}}.

## Submenus

### Hall of Fame

The Hall of Fame, sometimes inconsistently called High Scores, shows the top ten scores and the name of the person who achieved each one, with the option to clear all the scores if desired by pressing <kbd>F10</kbd>. Any other key dismisses the window.

{{< image src="hall-of-fame-2052x.png"
    alt="Hall of Fame"
    1x="hall-of-fame-684x.png"
    2x="hall-of-fame-1368x.png"
    3x="hall-of-fame-2052x.png" >}}

It is implemented in {{< lookup/cref ShowHighScoreTable >}}.

### Enter Your Name

The "Enter your name" prompt function is also responsible for managing the content of the high score table. Each time the function is called, the high score table is scanned to find the appropriate location for the new entry, moving all inferior scores down in the list. Once this space has been freed, the prompt fills it with the provided name and score.

{{< image src="enter-your-name-2052x.png"
    alt="Enter Your Name"
    1x="enter-your-name-684x.png"
    2x="enter-your-name-1368x.png"
    3x="enter-your-name-2052x.png" >}}

It is implemented in {{< lookup/cref CheckHighScoreAndShow >}}.

### Quit Game

The quit menu presents a yes/no confirmation prompt if the user wants to quit the program (or the current game). Answering <kbd>Y</kbd>, depending on the context, either aborts the current game (returning the user to the main menu) or the entire program exits back to DOS.

{{< image src="quit-confirm-2052x.png"
    alt="Quit Game Confirmation"
    1x="quit-confirm-684x.png"
    2x="quit-confirm-1368x.png"
    3x="quit-confirm-2052x.png" >}}

It is implemented in {{< lookup/cref PromptQuitConfirm >}}.

### Keyboard Redefine

The keyboard redefine menu allows the user to configure the six keys that control the player.

{{< image src="keyboard-redefine-2052x.png"
    alt="Keyboard Redefine Menu"
    1x="keyboard-redefine-684x.png"
    2x="keyboard-redefine-1368x.png"
    3x="keyboard-redefine-2052x.png" >}}

It is implemented in {{< lookup/cref ShowKeyboardConfiguration >}} and {{< lookup/cref PromptKeyBind >}}.

### Joystick Redefine

The joystick redefine menu calibrates the joystick (if one is installed) and configures it as the active input device if successful.

{{< image src="joystick-redefine-2052x.png"
    alt="Joystick Redefine Menu"
    1x="joystick-redefine-684x.png"
    2x="joystick-redefine-1368x.png"
    3x="joystick-redefine-2052x.png" >}}

It is implemented in {{< lookup/cref ShowJoystickConfiguration >}}.

### Test Sound

The test sound menu allows the user to audition each of the sound effects available in the game.

{{< image src="test-sound-2052x.png"
    alt="Test Sound Menu"
    1x="test-sound-684x.png"
    2x="test-sound-1368x.png"
    3x="test-sound-2052x.png" >}}

It is implemented in {{< lookup/cref ShowSoundTest >}}.

### Save Game

When a game is being played, the save game menu will write the game variables _from the starting point of the level_ into one of the nine available save game slots.

{{< image src="save-game-2052x.png"
    alt="Save Game Menu"
    1x="save-game-684x.png"
    2x="save-game-1368x.png"
    3x="save-game-2052x.png" >}}

It is implemented in {{< lookup/cref PromptSaveGame >}}.

### Restore Game

At any point, the user can choose to abandon their current game (if one is in progress) and load a previous game from one of the nine available save game slots.

{{< image src="restore-game-2052x.png"
    alt="Restore Game Menu"
    1x="restore-game-684x.png"
    2x="restore-game-1368x.png"
    3x="restore-game-2052x.png" >}}

It is implemented in {{< lookup/cref PromptRestoreGame >}}.

### Level Warp

If debug mode is enabled, the warp menu allows the user to directly jump to the beginning of any map available in the game.

{{< image src="warp-mode-2052x.png"
    alt="Warp Mode Menu"
    1x="warp-mode-684x.png"
    2x="warp-mode-1368x.png"
    3x="warp-mode-2052x.png" >}}

It is implemented in {{< lookup/cref PromptLevelWarp >}}.

## In-Game Keys

Although not shown as a traditional menu, the following keys are always available during gameplay and perform similar functions to a menu:

* <kbd>P</kbd>: [Pause Game]({{< relref "dialog-functions#ShowPauseMessage" >}})
* <kbd>Q</kbd> or <kbd>Esc</kbd>: [Quit Game]({{< relref "#quit-game" >}})
* <kbd>S</kbd>: [Sound Toggle]({{< relref "dialog-functions#ToggleSound" >}})
* <kbd>M</kbd>: [Music Toggle]({{< relref "dialog-functions#ToggleMusic" >}})
* <kbd>F1</kbd>: [Help Menu]({{< relref "#help-menu" >}})
* <kbd>C</kbd> + <kbd>0</kbd> + <kbd>F10</kbd>: Cheat Code
* <kbd>Tab</kbd> + <kbd>F12</kbd> + <kbd>Del</kbd>: Debug Mode Toggle

This handling occurs in {{< lookup/cref ProcessGameInput >}}.

### Debug Mode Keys

If debug mode is activated, the following key combinations can be pressed during gameplay to access additional functionality. Like the in-game keys, there is no menu shown to enumerate these options; the user must either know they exist or perform a brute-force search for them:

* <kbd>E</kbd> + <kbd>N</kbd> + <kbd>D</kbd>: [End Story]({{< relref "dialog-functions#ShowEnding" >}})
* <kbd>F10</kbd> + <kbd>G</kbd>: [God Mode Toggle]({{< relref "dialog-functions#ToggleGodMode" >}})
* <kbd>F10</kbd> + <kbd>M</kbd>: [Memory Usage]({{< relref "dialog-functions#ShowMemoryUsage" >}})
* <kbd>F10</kbd> + <kbd>P</kbd>: Debug Pause
* <kbd>F10</kbd> + <kbd>W</kbd>: [Level Warp]({{< relref "#level-warp" >}})
* <kbd>Alt</kbd> + <kbd>C</kbd>: Invoke the [original keyboard interrupt handler]({{< relref "keyboard-functions#KeyboardInterruptService" >}})

This handling also occurs in {{< lookup/cref ProcessGameInput >}}.

{{< boilerplate/function-cref TitleLoop >}}

The {{< lookup/cref TitleLoop >}} function runs at the start of the program and is responsible for showing the title screen, credits, demo, and main menu. Additionally, this function reads the keyboard input for the main menu selection and calls the appropriate function in response. Returns one of the {{< lookup/cref DEMO_STATE >}} variables, to instruct the caller to run the game loop with the appropriate demo playback/record state.

```c
byte TitleLoop(void)
{
#ifdef FOREIGN_ORDERS
#   define YSHIFT 1
#else
#   define YSHIFT 0
#endif

    word idlecount;
    byte scancode;

    isNewGame = false;
```

Even though this function is responsible for a rather significant part of the menu experience, it does not define all that many local variables. `idlecount` tracks the number of busy loop iterations that have passed with no keyboard input, and `scancode` holds the scancode of the key that was most recently pressed. The `YSHIFT` macro is defined based on the presence or absence of the `FOREIGN_ORDERS` flag. When this is set, the main menu has a "Foreign Orders" option and needs to be taller to make room for it.

{{< lookup/cref isNewGame >}} is a flag, used later (in {{< lookup/cref InitializeLevel >}}) to slightly change the menu transition to the "Begin New Game" mode by conditionally showing a "One Moment" image. This is initially cleared under the assumption that a demo or restored game is going to start -- those modes do not show the "One Moment" screen.

```c
title:
    StartMenuMusic(MUSIC_ZZTOP);
    DrawFullscreenImage(IMAGE_TITLE);
    idlecount = 0;
    gameTickCount = 0;

    while (!IsAnyKeyDown()) {
        WaitHard(3);
        idlecount++;

        if (idlecount == 600) {
            DrawFullscreenImage(IMAGE_CREDITS);
        }

        if (idlecount == 1200) {
            InitializeEpisode();
            return DEMO_STATE_PLAY;
        }
    }
```

This is the main title loop. At the top, it starts (or restarts) playing {{< lookup/cref name="MUSIC" text="MUSIC_ZZTOP" >}} via a call to {{< lookup/cref StartMenuMusic >}}. The main title screen {{< lookup/cref name="IMAGE" text="IMAGE_TITLE" >}} is shown next via {{< lookup/cref DrawFullscreenImage >}}. `idlecount` is zeroed to start the timer. {{< lookup/cref gameTickCount >}} is also zeroed to ensure subsequent calls to {{< lookup/cref WaitHard >}} count the appropriate number of ticks, but this is not necessary -- {{< lookup/cref WaitHard >}} takes care of that itself. This might be vestigial behavior.

The `while` loop performs the actual repetitive work here. As long as {{< lookup/cref IsAnyKeyDown >}} is false, continue iterating. On each iteration, wait three game ticks with {{< lookup/cref WaitHard >}} and advance the `idlecount`. This limits the execution speed of this loop to 3 &frasl; 140 Hz, or 46.{{< overline >}}6{{< /overline >}} iterations per second. Although these seem like rather arbitrary numbers, they actually divide roughly evenly into the music's approximate tempo of 137 beats per minute. Combining _those_ numbers, we find this loop iterates just about 20 times for each beat in the music. Using this relationship, the menu progression can be synchronized (to an extent) to the music being played.

When `idlecount` reaches 600 (30 musical beats, or 7.5 bars) {{< lookup/cref DrawFullscreenImage >}} is called again to replace the screen content with the credits image {{< lookup/cref name="IMAGE" text="IMAGE_CREDITS" >}}. Interestingly, if a key is pressed when the credits are being shown, the main menu will appear drawn over them.

Once `idlecount` reaches 1,200 (60 beats, 15 bars) the demo starts. This is accomplished by calling {{< lookup/cref InitializeEpisode >}} to set up the game globals, and returning {{< lookup/cref name="DEMO_STATE" text="DEMO_STATE_PLAY" >}} to the caller. When the demo ends, {{< lookup/cref TitleLoop >}} will be called again.

If the user presses a key before the demo begins, this loop terminates and execution continues.

```c
    scancode = WaitForAnyKey();
    if (scancode == SCANCODE_Q || scancode == SCANCODE_ESC) {
        if (PromptQuitConfirm()) ExitClean();
        goto title;
    }
```

Before the menu is shown, a quick check is done to see if the user pressed <kbd>Q</kbd> or <kbd>Esc</kbd>. In that case, prompt for confirmation and exit if appropriate. For any other key, this block is skipped and execution continues below.

{{< lookup/cref WaitForAnyKey >}} blocks until a key on the keyboard is pressed _and released._ The act of pressing the key causes the previous `while` loop to terminate, but the release is what is returned into `scancode`. If the key matches {{< lookup/cref name="SCANCODE" text="SCANCODE_Q" >}} or {{< lookup/cref name="SCANCODE" text="SCANCODE_ESC" >}}, call {{< lookup/cref PromptQuitConfirm >}} to show the "Are you sure you want to quit?" message and, if that returns true, exit to DOS with {{< lookup/cref ExitClean >}}.

If the user answered anything other then <kbd>Y</kbd> to the quit confirmation, jump back to the `title` label to restart the entire title loop sequence.

```c
    for (;;) {
        DrawMainMenu();

getkey:
        scancode = WaitSpinner(28, 20 + YSHIFT);

        /* ... See "Main Menu Input Handling" ... */

        DrawFullscreenImage(IMAGE_TITLE);
    }

#undef YSHIFT
}
```

The remainder of the function is a `for` loop that (re)draws the menu, handles the user's selection, and redraws the title screen image. This loop iterates each time a submenu is visited and then exited -- since new menus destroy everything behind them, the main menu and title image need to be redrawn fresh when they are resurfaced.

On each iteration of the loop, {{< lookup/cref DrawMainMenu >}} presents the menu text and {{< lookup/cref WaitSpinner >}} blocks until a key is pressed. The scancode of that key in saved in `scancode`, and the [input handler]({{< relref "#main-menu-input-handling" >}}) decides how to respond. The Y position of the wait spinner may be adjusted on a per-episode basis through the `YSHIFT` macro. (Episode 1 has a "Foreign Orders" option, which makes the menu one tile taller and the wait spinner needs to be placed one tile lower accordingly.)

The input handler can respond to a keypress in multiple ways:

* If the game should start (either under user control or in one of the demo modes) a `return` statement jumps completely out of the entire function.
* If the user quits and confirms the choice, {{< lookup/cref ExitClean >}} exits the program from inside this loop.
* To redisplay the title screen, `goto title` jumps out of the loop to near the top of this function.
* If an unimplemented key is pressed, `goto getkey` silently ignores it and restarts the current iteration midway.
* While navigating the rest of the menus, the input handler falls through to {{< lookup/cref name="DrawFullscreenImage" text="DrawFullscreenImage(IMAGE_TITLE)" >}}, redrawing the title screen image. A new loop iteration begins -- displaying the main menu fresh.

Except for the cases where a game begins or the program quits to DOS, this is an inescapable function.

### Main Menu Input Handling

The input handler within the title loop is a simple `switch` overall, but it has a large number of cases and some of them have some nuance.

```c
        switch (scancode) {
        case SCANCODE_B:
        case SCANCODE_ENTER:
        case SCANCODE_SPACE:
            InitializeEpisode();
            isNewGame = true;
            pounceHintState = POUNCE_HINT_UNSEEN;
            StartSound(SND_NEW_GAME);
            return DEMO_STATE_NONE;
```

In response to <kbd>B</kbd>, <kbd>Enter</kbd>, or <kbd>Space</kbd>, the "Begin New Game" action is taken.

{{< lookup/cref InitializeEpisode >}} sets the initial state for the game's global variables. It selects the first level, sets the player score to zero, gives the player at three full bars of health, and so on. Setting {{< lookup/cref isNewGame >}} enables the future display of the "One Moment" screen.

{{< lookup/cref pounceHintState >}} is set to {{< lookup/cref name="POUNCE_HINT" text="POUNCE_HINT_UNSEEN" >}}, which enables the "jump on creatures" hint the first time the player is hurt. (Why this wasn't done in {{< lookup/cref InitializeEpisode >}} with the rest of the hint variable initializations, who can say.)

{{< lookup/cref StartSound >}} is called to play {{< lookup/cref name="SND" text="SND_NEW_GAME" >}}, and this function returns with a value of {{< lookup/cref name="DEMO_STATE" text="DEMO_STATE_NONE" >}} to indicate that a demo is not being played, nor is one being recorded -- the game must be under user control. Control passes back to the caller ({{< lookup/cref InnerMain >}}), which uses the returned demo state value to decide how to run the game loop.

To return to the main menu, {{< lookup/cref InnerMain >}} must call {{< lookup/cref TitleLoop >}} again.

```c
        case SCANCODE_O:
            ShowOrderingInformation();
            break;
        case SCANCODE_I:
            ShowInstructions();
            break;
        case SCANCODE_A:
            ShowPublisherBBS();
            break;
```

The <kbd>O</kbd>, <kbd>I</kbd>, and <kbd>A</kbd> cases are straightforward and display the "Ordering Information," "Instructions," or "Apogee's BBS" menus, respectively. Each is drawn directly on top of the existing main menu and title image.

Once {{< lookup/cref ShowOrderingInformation >}}, {{< lookup/cref ShowInstructions >}}, or {{< lookup/cref ShowPublisherBBS >}} returns, a `break` exits out of the `switch` and continues running the code in the enclosing `for` loop. The title screen image is redrawn, which erases the menu that was just dismissed. As the loop repeats, the main menu is redrawn and the wait spinner blocks until a new selection is made.

```c
        case SCANCODE_R:
            {  /* for scope */
                byte result = PromptRestoreGame();
                if (result == RESTORE_GAME_SUCCESS) {
                    return DEMO_STATE_NONE;
                } else if (result == RESTORE_GAME_NOT_FOUND) {
                    ShowRestoreGameError();
                }
            }
            break;
```

The <kbd>R</kbd> key selects "Restore A Game," which contains a small submenu. The submenu prompts the user to enter a game number, and returns one of three states:

* If the user pressed <kbd>Esc</kbd> or entered another input that suggests they did not want to proceed, the return value indicates the input was aborted. ({{< lookup/cref name="RESTORE_GAME" text="RESTORE_GAME_ABORT" >}})
* If the user entered a number but the save file for that slot did not exist, the return value indicates this condition. ({{< lookup/cref name="RESTORE_GAME" text="RESTORE_GAME_NOT_FOUND" >}})
* Otherwise the game state has been restored successfully and all relevant global variables have been set. ({{< lookup/cref name="RESTORE_GAME" text="RESTORE_GAME_SUCCESS" >}})

{{< lookup/cref PromptRestoreGame >}} is responsible for the aforementioned behavior, and returns the restore status into `result`. In the success case, this function returns {{< lookup/cref name="DEMO_STATE" text="DEMO_STATE_NONE" >}} and behaves similarly to the "Begin New Game" case.

If the saved game was not found, the {{< lookup/cref ShowRestoreGameError >}} dialog is drawn on top of the screen contents. When the message is dismissed, `break` returns to the enclosing loop.

In the abort case, execution simply falls to the `break`.

In both `break` situations, the enclosing loop takes over again, redrawing the title image and main menu.

```c
        case SCANCODE_S:
            ShowStory();
            break;
```

The <kbd>S</kbd> key shows the "Story" pages via a call to {{< lookup/cref ShowStory >}}, which works the same as "Instructions" earlier.

```c
        case SCANCODE_F11:
            if (isDebugMode) {
                InitializeEpisode();
                return DEMO_STATE_RECORD;
            }
            break;
```

<kbd>F11</kbd> is an undocumented debug key that starts recording a demo if the right preconditions are met. To do this, {{< lookup/cref isDebugMode >}} must be true, which means the user must've started a game at least once and enabled debug mode using <kbd>Tab</kbd> + <kbd>F12</kbd> + <kbd>Del</kbd>, then returned to the main menu to invoke this command.

When activated, it works essentially the same as the "Begin New Game" case: {{< lookup/cref InitializeEpisode >}} sets up all the appropriate variables, and `return` passes control back to the caller. The difference here, however, is that the return value is {{< lookup/cref name="DEMO_STATE" text="DEMO_STATE_RECORD" >}} -- this is what configures the game loop to record the demo data (and some other differences) as the game is played.

If debug mode is _not_ enabled, the `break` here returns to the main menu similarly to how other simple menus like "Instructions" do. This has the side effect of fading the screen out and back in for seemingly no reason.

```c
        case SCANCODE_D:
            InitializeEpisode();
            return DEMO_STATE_PLAY;
```

The <kbd>D</kbd> is the "Demo" playback feature, which works identically to the "record demo" case. The only difference is the {{< lookup/cref name="DEMO_STATE" text="DEMO_STATE_PLAY" >}} return value, which instructs the game loop to load the stored demo data and use it instead of the keyboard (or joystick) when processing input.

```c
        case SCANCODE_T:
            goto title;
```

The <kbd>T</kbd> key is a nice little touch that returns to an unobstructed view of the "Title Screen" image through an unconditional `goto`. This jumps to the `title` label at (almost) the top of the function and starts everything, including the music and idle counters, from the beginning.

```c
        case SCANCODE_Q:
        case SCANCODE_ESC:
            if (PromptQuitConfirm()) ExitClean();
            break;
```

<kbd>Q</kbd> and <kbd>Esc</kbd> both perform the "Quit Game" action after a simple yes/no confirmation.

{{< lookup/cref PromptQuitConfirm >}} draws an "are you sure?" message over the screen contents and waits for a response. If <kbd>Y</kbd> is entered, the function returns true and {{< lookup/cref ExitClean >}} shuts down the game and exits unconditionally back to DOS.

If any other key is pressed at the prompt, `break` returns to the main menu in the same way as "Instructions" and other similar menu options.

```c
        case SCANCODE_C:
            DrawFullscreenImage(IMAGE_CREDITS);
            WaitForAnyKey();
            break;
```

The <kbd>C</kbd> key shows "Credits," which is a full-screen image that remains up until a key is pressed. {{< lookup/cref DrawFullscreenImage >}} replaces the entire screen contents with {{< lookup/cref name="IMAGE" text="IMAGE_CREDITS" >}}, then {{< lookup/cref WaitForAnyKey >}} waits indefinitely until a key is pressed and released.

Finally, `break` returns to the main menu in the same way as "Instructions" and other similar menu options.

```c
        case SCANCODE_G:
            ShowGameRedefineMenu();
            break;
```

<kbd>G</kbd> shows the "Game Redefine" menu, which contains a number of other submenus. That complexity is hidden from view here, all the main menu knows is that it should call {{< lookup/cref ShowGameRedefineMenu >}} to show this menu, and to `break` back to the title screen/main menu whenever the game redefine menu function returns.

```c
#ifdef FOREIGN_ORDERS
        case SCANCODE_F:
            ShowForeignOrders();
            break;
#endif
```

The <kbd>F</kbd> key shows "Foreign Orders," which only the first episode includes. As a result, this is conditionally compiled and only some of the executables have the code. When selected, {{< lookup/cref ShowForeignOrders >}} shows the menu and `break` returns to the main menu, same as the "Instructions" case.

```c
        case SCANCODE_H:
            FadeOut();
            ClearScreen();
            ShowHighScoreTable();
            break;
```

Finally, <kbd>H</kbd> is the "High Scores" option. This is a bit unusual since it clears the screen before drawing -- perhaps a stylistic choice more than anything else.

In order to transition from the main menu to the high score table, {{< lookup/cref FadeOut >}} is called to fade the screen to black by using palette manipulation. Once this returns, nothing drawn to the screen is visible to the user. {{< lookup/cref ClearScreen >}} is then free to fill the screen with black pixels, then {{< lookup/cref ShowHighScoreTable >}} draws the table. {{< lookup/cref ShowHighScoreTable >}} fades the screen back _in_ as well, which is why we don't see that being done here.

{{< lookup/cref ShowHighScoreTable >}} returns when the user dismisses the high score table, whereupon execution reaches the `break` and the title image/main menu are redrawn.

```c
        default:
            goto getkey;
        }
```

The last bit of code handles the `default` case, which occurs whenever a key is pressed at the main menu that does not have a defined `case` above. Whenever that happens, execution jumps via `goto` to the `getkey` label. This discards the keypress and immediately prepares to read the next one without redrawing anything.

{{< boilerplate/function-cref DrawMainMenu >}}

The {{< lookup/cref DrawMainMenu >}} function is a small helper that draws the main menu frame and text, but does not do any input handling. It is only called from {{< lookup/cref TitleLoop >}}.

```c
void DrawMainMenu(void)
{
#ifdef FOREIGN_ORDERS
#   define YSHIFT 1
#else
#   define YSHIFT 0
#endif

    word x = UnfoldTextFrame(2, 20 + YSHIFT, 20, "MAIN MENU", "");
    DrawTextLine(x, 5,           " B)egin New Game");
    DrawTextLine(x, 6,           " R)estore A Game");
    DrawTextLine(x, 7,           " S)tory");
    DrawTextLine(x, 8,           " I)nstructions");
    DrawTextLine(x, 9,           " H)igh Scores");
    DrawTextLine(x, 10,          " G)ame Redefine");
    DrawTextLine(x, 12,          " O)rdering Info.");
#ifdef FOREIGN_ORDERS
    DrawTextLine(x, 14,          " F)oreign Orders");
#endif
    DrawTextLine(x, 14 + YSHIFT, " A)pogee's BBS");
    DrawTextLine(x, 15 + YSHIFT, " D)emo");
    DrawTextLine(x, 16 + YSHIFT, " C)redits");
    DrawTextLine(x, 17 + YSHIFT, " T)itle Screen");
    DrawTextLine(x, 19 + YSHIFT, " Q)uit Game");

#undef YSHIFT
}
```

Depending on the episode, the main menu might or might not have a "Foreign Orders" option. If it does, the menu needs to be one tile taller, and all of the options that appear below "Foreign Orders" need to be shifted one tile down. The `FOREIGN_ORDERS` macro controls visibility of this menu item, and its associated `YSHIFT` macro takes care of shifting subsequent items where necessary.

The remainder of the function is a few calls to {{< lookup/cref UnfoldTextFrame >}} and {{< lookup/cref DrawTextLine >}}, which constructs the menu's frame and writes all of the text inside it. When this is complete, control returns to the caller who is responsible for actually reading and handling the input.

{{< boilerplate/function-cref ShowHelpMenu >}}

The {{< lookup/cref ShowHelpMenu >}} function shows a menu labeled "Help Menu" in response to the user pressing <kbd>F1</kbd> during the game. It gives access to save/restore functions and a subset of options offered by the main menu. Returns one of the {{< lookup/cref HELP_MENU >}} variables.

Depending on what the user does in this menu, the caller will take one of three actions in response to the return value from this function:

* In the typical case, the user leaves the menu without making any impactful change. The game should pick up right where it left off. ({{< lookup/cref name="HELP_MENU" text="HELP_MENU_CONTINUE" >}})
* If the user restores a saved game, the game loop needs to abort what it's doing in preparation to load a different game state into memory. ({{< lookup/cref name="HELP_MENU" text="HELP_MENU_RESTART" >}})
* If the user quits the game, the game loop needs to stop itself and return control back to its own caller. ({{< lookup/cref name="HELP_MENU" text="HELP_MENU_QUIT" >}})

{{< boilerplate/dialog-gameplay object="menu" >}}

```c
byte ShowHelpMenu(void)
{
    word x = UnfoldTextFrame(2, 12, 22, "HELP MENU", "Press ESC to quit.");
    DrawTextLine(x, 5,  " S)ave your game");
    DrawTextLine(x, 6,  " R)estore a game");
    DrawTextLine(x, 7,  " H)elp");
    DrawTextLine(x, 8,  " G)ame redefine");
    DrawTextLine(x, 9,  " V)iew High Scores");
    DrawTextLine(x, 10, " Q)uit Game");
```

This menu is built from a frame drawn with {{< lookup/cref UnfoldTextFrame >}} and several lines of text, each drawn with a call to {{< lookup/cref DrawTextLine >}}. The `x` variable here is a convenience to find the X-position of the inner tiles of this horizontally-centered frame.

```c
    for (;;) {
        byte scancode = WaitSpinner(29, 12);
```

Input handling occurs in an infinite `for` loop. {{< lookup/cref WaitSpinner >}} blocks until a key is pressed, then execution continues with the pressed key's scancode stored in `scancode`.

```c
        switch (scancode) {
        case SCANCODE_G:
            ShowGameRedefineMenu();
            return HELP_MENU_CONTINUE;
```

The <kbd>G</kbd> key in this menu shows the "Game redefine" submenu.

The programming paradigm here is quite similar to that of the [main menu]({{< relref "#main-menu-input-handling" >}}) -- call a function that draws content on top of the existing menu, then return when that subfunction is done.

In this case {{< lookup/cref ShowGameRedefineMenu >}} presents and handles the game redefine menu. Once it's dismissed, this function returns {{< lookup/cref name="HELP_MENU" text="HELP_MENU_CONTINUE" >}} to indicate to its caller ({{< lookup/cref ProcessGameInput >}}) that the game should continue executing in the same state it was before.

```c
        case SCANCODE_S:
            PromptSaveGame();
            return HELP_MENU_CONTINUE;
```

The <kbd>S</kbd> key presents the "Save your game" prompt via a call to {{< lookup/cref PromptSaveGame >}}, and otherwise behaves identically to the "Game redefine" case.

```c
        case SCANCODE_R:
            {  /* for scope */
                byte result = PromptRestoreGame();
                if (result == RESTORE_GAME_SUCCESS) {
                    InitializeLevel(levelNum);
                    return HELP_MENU_RESTART;
                } else if (result == RESTORE_GAME_NOT_FOUND) {
                    ShowRestoreGameError();
                }
            }
            return HELP_MENU_CONTINUE;
```

The <kbd>R</kbd> key invokes the "Restore a game" option, which prompts the user for a slot number to restore from. Depending on the result of the selection, three possible paths are taken:

* If the user pressed <kbd>Esc</kbd> or entered another input that suggests they did not want to proceed, the return value indicates the input was aborted. ({{< lookup/cref name="RESTORE_GAME" text="RESTORE_GAME_ABORT" >}})
* If the user entered a number but the save file for that slot did not exist, the return value indicates this condition. ({{< lookup/cref name="RESTORE_GAME" text="RESTORE_GAME_NOT_FOUND" >}})
* Otherwise the game state has been restored successfully and all relevant global variables have been set. ({{< lookup/cref name="RESTORE_GAME" text="RESTORE_GAME_SUCCESS" >}})

{{< lookup/cref PromptRestoreGame >}} is responsible for the aforementioned behavior, and returns the restore status into `result`. In the success case, {{< lookup/cref PromptRestoreGame >}} will have set all the necessary global variables that were read from the file, including {{< lookup/cref levelNum >}}. {{< lookup/cref InitializeLevel >}} handles further game state initialization and loads the map data. Finally, {{< lookup/cref name="HELP_MENU" text="HELP_MENU_RESTART" >}} is returned, informing the caller that the game loop needs to start from the beginning with the new game state.

If the saved game was not found, the {{< lookup/cref ShowRestoreGameError >}} dialog is drawn on top of the screen contents. Once the message is dismissed, the `return` path is taken.

In the abort case, execution simply falls to the `return`.

In both of these `return` situations, {{< lookup/cref name="HELP_MENU" text="HELP_MENU_CONTINUE" >}} instructs the caller to continue running the game loop in its current state, since nothing has changed.

```c
        case SCANCODE_V:
            ShowHighScoreTable();
            return HELP_MENU_CONTINUE;
```

The <kbd>V</kbd> key performs the "View High Scores" action. {{< lookup/cref ShowHighScoreTable >}} draws the high score table on top of the existing screen contents. (Contrary to the behavior in the main menu, here {{< lookup/cref ShowHighScoreTable >}} skips clearing and fading the screen.)

When the high score table is dismissed, its function returns and {{< lookup/cref name="HELP_MENU" text="HELP_MENU_CONTINUE" >}} is returned here. This instructs the caller to resume the game loop as usual.

```c
        case SCANCODE_Q:
            return HELP_MENU_QUIT;
```

The <kbd>Q</kbd> key performs the "Quit" action with a yes/no confirmation prompt. The logic is handled elsewhere in the caller, and invoked by returning {{< lookup/cref name="HELP_MENU" text="HELP_MENU_QUIT" >}}.

```c
        case SCANCODE_H:
            ShowHintsAndKeys(1);
            return HELP_MENU_CONTINUE;
```

The <kbd>H</kbd> key presents three pages of in-game "Help" text. These are a subset of the "Instructions" available from the main menu.

{{< lookup/cref ShowHintsAndKeys >}} is responsible for drawing each page of text, and waiting for the keypresses that advance or dismiss the information. It takes a single parameter, here `1`, which controls the vertical position where the frame and its contents are drawn. The help text is drawn higher on the screen here than it would be from the main menu "instructions" dialogs, because otherwise it would overlap the status bar and lead to corruption when the game is continued. (The status bar background is not regularly redrawn for performance reasons.)

{{< lookup/cref ShowHintsAndKeys >}} returns once all pages of text have been viewed. From here, {{< lookup/cref name="HELP_MENU" text="HELP_MENU_CONTINUE" >}} is returned to inform the caller to resume the game loop.

```c
        case SCANCODE_ESC:
            return HELP_MENU_CONTINUE;
        }
    }
}
```

The last case is the <kbd>Esc</kbd> key, which dismisses the menu. This is accomplished by returning {{< lookup/cref name="HELP_MENU" text="HELP_MENU_CONTINUE" >}} to the caller. This resumes the game loop, which overwrites the entire area occupied by this menu as the next frame of gameplay is drawn.

{{< boilerplate/function-cref ShowGameRedefineMenu >}}

The {{< lookup/cref ShowGameRedefineMenu >}} function shows a menu labeled "Game Redefine" in response to the user selecting the <kbd>G</kbd> option in either the [main menu]({{< relref "#title-loop" >}}) or the in-game [help menu]({{< relref "#help-menu" >}}). This function simply dispatches one of the submenu functions in response to the user's input.

{{< boilerplate/dialog-gameplay object="menu" may=true >}}

```c
void ShowGameRedefineMenu(void)
{
    word x = UnfoldTextFrame(4, 11, 22, "Game Redefine",
        "Press ESC to quit.");
    DrawTextLine(x, 7,  " K)eyboard redefine");
    DrawTextLine(x, 8,  " J)oystick redefine");
    DrawTextLine(x, 9,  " S)ound toggle");
    DrawTextLine(x, 10, " T)est sound");
    DrawTextLine(x, 11, " M)usic toggle");
```

The function begins with a straightforward set of calls to {{< lookup/cref UnfoldTextFrame >}} followed by {{< lookup/cref DrawTextLine >}}, which constructs the menu's frame and writes all of the text inside it.

```c
    for (;;) {
        byte scancode = WaitSpinner(29, 13);

        switch (scancode) {
        case SCANCODE_ESC:
            return;
        case SCANCODE_S:
            ToggleSound();
            return;
        case SCANCODE_J:
            ShowJoystickConfiguration(JOYSTICK_A);
            return;
        case SCANCODE_K:
            ShowKeyboardConfiguration();
            return;
        case SCANCODE_T:
            ShowSoundTest();
            return;
        case SCANCODE_M:
            ToggleMusic();
            return;
        }
    }
}
```

The remainder of the function is an infinite `for` loop that repeats until a valid key has been pressed.

{{< lookup/cref WaitSpinner >}} blocks until a key press arrives, at which point it returns the key's scancode into the `scancode` variable. A `switch` decodes its value and takes the appropriate action.

If <kbd>Esc</kbd> was pressed, the user dismissed the menu and the function returns without further action. The caller is responsible for redrawing any screen contents that the game redefine menu overwrote.

The <kbd>S</kbd> key invokes the sound toggling function, {{< lookup/cref ToggleSound >}}. Likewise, the <kbd>M</kbd> key toward the bottom of the loop body toggles the music with the {{< lookup/cref ToggleMusic >}} function.

The <kbd>J</kbd> key starts the joystick configuration option {{< lookup/cref ShowJoystickConfiguration >}}. Passing {{< lookup/cref name="JOYSTICK" text="JOYSTICK_A" >}} informs the function that it should configure the first joystick only. (Support for a second joystick is not fully implemented, and has no use in this game.)

The <kbd>K</kbd> key allows the keyboard controls to be customized through the {{< lookup/cref ShowKeyboardConfiguration >}} option.

Finally, <kbd>T</kbd> starts the sound effect testing screen at {{< lookup/cref ShowSoundTest >}}. This allows the user to listen to every sound effect shipped with the game.

If any valid menu option is selected, the relevant function is called and, upon return, {{< lookup/cref ShowGameRedefineMenu >}} returns as well. If an invalid key is entered, the `for` loop begins a new iteration and another keypress is awaited.

{{< boilerplate/function-cref ShowHighScoreTable >}}

The {{< lookup/cref ShowHighScoreTable >}} function shows the top ten scores that have been reached and the name of the player who earned each spot. The table can optionally be erased by pressing the <kbd>F10</kbd> key and confirming with the <kbd>Y</kbd> key. Whenever the high score table is cleared, the table is redrawn with the new empty content. The user is free to press <kbd>F10</kbd> again, repeatedly clearing the already-cleared table in a loop until their fingers are wizened and callused.

Depending on the state of the {{< lookup/cref isInGame >}} variable, this function may or may not fade the screen and clear its contents.

{{< boilerplate/dialog-gameplay object="menu" may=true >}}

```c
void ShowHighScoreTable(void)
{
    for (;;) {
        byte scancode;
        word i;
        word x = UnfoldTextFrame(2, 17, 30, "Hall of Fame",
            "any other key to exit.");
```

The high score table display is housed inside of an infinite `for` loop that provides the redrawing behavior if the table is cleared.

{{< lookup/cref UnfoldTextFrame >}} draws the outer frame of the high score table, along with the second half of the message "Press 'F10' to erase or any other key to exit." The frame only supports a single line of text at each edge of the frame, so the first half of the message must be written separately.

```c
        for (i = 0; i < 10; i++) {
            DrawNumberFlushRight(x + 2, i + 5, i + 1);
            DrawTextLine(x + 3, i + 5, ".");
            DrawNumberFlushRight(x + 11, i + 5, highScoreValues[i]);
            DrawTextLine(x + 13, i + 5, highScoreNames[i]);
        }
        DrawTextLine(x + 3, 16, "Press 'F10' to erase or");
```

The scores are drawn in a nested `for` loop, which counts `i` from 0 to 9. {{< lookup/cref DrawNumberFlushRight >}} draws the rank number (with a single leading space for values less than 10) followed by a dot placed by {{< lookup/cref DrawTextLine >}}. A second call to {{< lookup/cref DrawNumberFlushRight >}} writes the associated score from the {{< lookup/cref highScoreValues >}} array (with up to six leading spaces) and {{< lookup/cref DrawTextLine >}} writes the name from {{< lookup/cref highScoreNames >}}.

Although each high score name is allotted 16 bytes in memory (which is enough to store 15 characters plus the null string terminator), high score names are limited on entry to 14 visible characters to prevent the last character from encroaching on the right frame border.

After all ten scores have been written, {{< lookup/cref DrawTextLine >}} is called one more time to write the first half of the "Press 'F10' to erase..." message that was started earlier.

```c
        if (!isInGame) {
            FadeIn();
        }
```

There are two places where the high score table can be called up: the [main menu]({{< relref "#title-loop" >}}) or the in-game [help menu]({{< relref "#help-menu" >}}). The in-game version is unadorned, appearing directly on top of the screen contents and eventually being erased by the next frame of gameplay. In the main menu, however, the screen fades out and is cleared before this function begins. In that context, it is necessary to fade the screen in now that the table has been fully drawn.

This behavior is controlled by the {{< lookup/cref isInGame >}} flag. When it is false, this function knows that the main menu called it and that the screen needs to be faded back in. {{< lookup/cref FadeIn >}} accomplishes that.

```c
        scancode = WaitSpinner(x + 27, 17);

        if (scancode != SCANCODE_F10) break;
```

With the high score table now visible on the screen, execution pauses at {{< lookup/cref WaitSpinner >}} until the user presses a key. The scancode of the pressed key is returned in `scancode`. If the key pressed is anything _but_ <kbd>F10</kbd>, `break` out of the outermost `for` loop and run off the end of the function, returning to the caller.

When the loop is exited this way, it is up to the caller to clean up the screen.

If the key _is_ <kbd>F10</kbd>, there is more to be done here and execution continues.

### Erasing High Scores

```c
        x = UnfoldTextFrame(5, 4, 28, "Are you sure you want to",
            "ERASE High Scores?");
        scancode = WaitSpinner(x + 22, 7);
```

Here the user has expressed their intention to erase the high scores, so a prompt is shown on top of the existing screen contents. {{< lookup/cref UnfoldTextFrame >}} draws a small frame containing the confirmation message, and {{< lookup/cref WaitSpinner >}} blocks until input is received. The scancode of the pressed key is returned in `scancode`.

```c
        if (scancode == SCANCODE_Y) {
            for (i = 0; i < 10; i++) {
                highScoreValues[i] = 0;
                highScoreNames[i][0] = '\0';
            }
        }
```

If the user pressed <kbd>Y</kbd>, they meant it when they said they wanted to erase the scores. Inside a `for` loop that runs from 0 to 9, set the corresponding element of {{< lookup/cref highScoreValues >}} to 0 (clearing the score) and set the first byte of the {{< lookup/cref highScoreNames >}} element to the null byte (setting the name to an empty string with inaccessible garbage data following it).

This does _not_ reset the scores to the Simpsons characters like {{< lookup/cref LoadConfigurationData >}} would. The user would need to manually remove their configuration file to achieve that. This loop zeros the scores and blanks the names instead.

```c
        if (!isInGame) {
            FadeOut();
            ClearScreen();
        }
    }
}
```

Similarly to the earlier {{< lookup/cref isInGame >}} test, this block differentiates main menu behavior from that of the help menu. From the main menu, the high score table should fade out and back in between menu function calls. During the game, in-place overwrites are fine.

{{< lookup/cref FadeOut >}} fades the screen to black, allowing subsequent drawing to occur invisibly to the user, then {{< lookup/cref ClearScreen >}} blanks out the screen contents. The outer `for` loop begins a new iteration, redrawing the freshly-cleared high score table and fading back in.

{{< boilerplate/function-cref CheckHighScoreAndShow >}}

The {{< lookup/cref CheckHighScoreAndShow >}} function scans the high score table for a position where the current {{< lookup/cref gameScore >}} could be sorted. If a position is located, a prompt is presented asking for a name to be associated with the score at that position, and all inferior scores are shifted one position lower. The tenth score falls off the bottom of the list. Calls {{< lookup/cref ShowHighScoreTable >}} unconditionally before returning.

If the value in {{< lookup/cref gameScore >}} is lower than all scores currently in the table, no prompt is shown. If the current score exactly equals an existing score in the table, the newer score will be inserted at a lower position than the older one.

```c
void CheckHighScoreAndShow(void)
{
    int i;

    FadeOut();
    SelectDrawPage(0);
    SelectActivePage(0);
    ClearScreen();
```

The function begins with visual transition code. {{< lookup/cref FadeOut >}} fades the contents of the screen to black by manipulating the palette registers, preventing anything from being shown to the user. {{< lookup/cref SelectDrawPage >}} and {{< lookup/cref SelectActivePage >}} select page zero for both drawing and display, meaning that any changes to video memory will be immediately visible to the user without involving page flipping. {{< lookup/cref ClearScreen >}} replaces the contents of the video memory on this draw page with solid black.

```c
    for (i = 0; i < 10; i++) {
        int inferior;
        word x;

        if (highScoreValues[i] >= gameScore) continue;
```

The high score table has ten slots, which are iterated in a `for` loop. The current slot number is held in `i`.

If the {{< lookup/cref highScoreValues >}} value at `i` is higher or equal to {{< lookup/cref gameScore >}}, the player's current score is not high enough to occupy this slot; `continue` on to the next one. If `continue` is called on the final slot, the player's score isn't high enough to appear anywhere in the table and the `for` loop terminates here.

When a suitable slot has been found, execution continues.

```c
        for (inferior = 10; inferior > i; inferior--) {
            highScoreValues[inferior] = highScoreValues[inferior - 1];
            strcpy(highScoreNames[inferior], highScoreNames[inferior - 1]);
        }

        highScoreNames[i][0] = '\0';
        highScoreValues[i] = gameScore;
```

We do not want to overwrite the selected slot with this new entry. Rather, we want to shift everything from this point down one position, making room for the new entry to be inserted between existing entries.

A second `for` loop does this, iterating from 10 _down_ to the current slot number in `i`. On each iteration, the values in {{< lookup/cref highScoreValues >}} and {{< lookup/cref highScoreNames >}} at index `inferior` are replaced with the values from index `inferior - 1`. The more slots need to shift down, the more times this loop body executes.

There is an important implementation detail in here to handle the boundary case of the lowest score falling off the end of the list. Both {{< lookup/cref highScoreValues >}} and {{< lookup/cref highScoreNames >}} are declared as fixed-size arrays of _eleven_ slots each, even though only ten of the slots are ever displayed. By allocating this eleventh slot, the loop here does not have to perform any special handling to "drop" the tenth value -- it simply moves it into the purgatorial eleventh position to be forgotten about.

When the inner `for` loop terminates, the slot at position `i` is ready to receive the new entry. {{< lookup/cref name="highScoreNames" text="highScoreNames[i]" >}} is set to a null string (it will be filled in later) and {{< lookup/cref name="highScoreValues" text="highScoreValues[i]" >}} gets the current {{< lookup/cref gameScore >}}. All that's left to do is receive the name for the slot.

```c
        x = UnfoldTextFrame(5, 7, 36, "You made it into the hall of fame!",
            "Press ESC to quit.");
        DrawTextLine(x, 8, "Enter your name:");
        FadeIn();
        StartSound(SND_HIGH_SCORE_SET);
```

{{< lookup/cref UnfoldTextFrame >}} and {{< lookup/cref DrawTextLine >}} construct the static components of the frame, and {{< lookup/cref FadeIn >}} restores the screen palette to fade the new content into view. {{< lookup/cref StartSound >}} queues a quick little melody ({{< lookup/cref name="SND" text="SND_HIGH_SCORE_SET" >}}) to be played through the PC speaker.

```c
        ReadAndEchoText(x + 16, 8, highScoreNames[i],
            sizeof(HighScoreName) - 2);

        break;
    }
```

The interactive part of the frame is handled separately, in a call to {{< lookup/cref ReadAndEchoText >}}. This presents a wait spinner, processes keyboard input, and returns when the <kbd>Enter</kbd> key is pressed. The {{< lookup/cref name="highScoreNames" text="highScoreNames[i]" >}} pointer is the memory where the input will be stored, and `sizeof(HighScoreName) - 2` sets the maximum length of that value -- 14 characters.

{{% note %}}Subtracting one from the maximum input length is necessary to leave room for the null terminator byte. Subtracting two, however, is likely a stylistic choice to prevent longer names from encroaching on the right-hand border of the high score table.{{% /note %}}

With the inferior scores shifted down and the new score entered in the table, there is no need to continue scanning through the high score table; `break` out of the outermost `for` loop and proceed below.

```c
    FadeOut();
    ClearScreen();
    StartSound(SND_HIGH_SCORE_DISPLAY);
    ShowHighScoreTable();
}
```

We can arrive here in two ways: Either the player qualified for a spot in the high score table and has just entered their name, or they did not earn a high enough score and nothing has been displayed.

The {{< lookup/cref FadeOut >}} and {{< lookup/cref ClearScreen >}} calls assume the former case, and fade the frame contents away before erasing them entirely. In the case where the score was not high enough, the screen is _already_ faded out and had been erased at the top of the function, so these calls are superfluous.

{{< lookup/cref StartSound >}} queues a fanfare ({{< lookup/cref name="SND" text="SND_HIGH_SCORE_SET" >}}) and {{< lookup/cref ShowHighScoreTable >}} shows the table, including any entry that may have just been added.

This function returns as soon as {{< lookup/cref ShowHighScoreTable >}} does.

{{< boilerplate/function-cref PromptQuitConfirm >}}

The {{< lookup/cref PromptQuitConfirm >}} function displays a window prompting the user to confirm their intention to quit, and blocks until a key is pressed. The return value is true if the <kbd>Y</kbd> key was pressed, or false in the case of any other key. The message "Are you sure you want to quit?" is intentionally vague, to allow this single function to handle confirmations for exiting the game (back to the menu) and exiting the program (back to DOS).

{{< boilerplate/dialog-gameplay object="menu" may=true >}}

```c
bbool PromptQuitConfirm(void)
{
    word x = UnfoldTextFrame(11, 4, 18, "Are you sure you",
        "want to quit? ");
    byte scancode = WaitSpinner(x + 14, 13);

    if (scancode == SCANCODE_Y) return true;

    return false;
}
```

{{< lookup/cref UnfoldTextFrame >}} presents a tiny frame, only large enough to hold two lines of text. By strategically packing the message into the call's `top_text` and `bottom_text` parameters, no other text-writing functions need to be called to present the message.

{{< lookup/cref WaitSpinner >}} blocks until a key is pressed, at which point the scancode of that key is returned in the `scancode` variable. `scancode` is compared against {{< lookup/cref name="SCANCODE" text="SCANCODE_Y" >}} and `true` is returned if they match. Otherwise, the return value is `false`.

{{< boilerplate/function-cref ShowKeyboardConfiguration >}}

The {{< lookup/cref ShowKeyboardConfiguration >}} function shows and handles the keyboard configuration (sometimes called keyboard _redefine_) menu. By pressing the <kbd>1</kbd> -- <kbd>6</kbd> keys, the user can change the key binding for the "move north/south/west/east," "jump," or "bomb" commands. Almost any key can be bound to any command, and at any stage of the configuration <kbd>Esc</kbd> will exit the menu.

{{< boilerplate/dialog-gameplay object="menu" may=true >}}

The following keys either _cannot_ or _should not_ be bound:

* <kbd>Esc</kbd>: This key always exits the keyboard configuration menu, and therefore cannot be assigned to any command.
* <kbd>M</kbd>, <kbd>P</kbd>, <kbd>Q</kbd>, <kbd>S</kbd>, and <kbd>F1</kbd>: Each of these keys performs an in-game command that presents a menu and interrupts gameplay.
* <kbd>Caps Lock</kbd>: While this key can be bound, it has a "latching" behavior and does not clear when the key is released. If, as an example, the "walk east" command was bound to this key, the first press of <kbd>Caps Lock</kbd> would start the player moving, and movement would continue even after the key was released. To stop walking east, the key has to be pressed a second time.
* <kbd>Num Lock</kbd>: Same symptoms as <kbd>Caps Lock</kbd>.
* Any extended key on the 101-key layout is treated like a duplicate of its corresponding key on the 84-key layout. E.g. <kbd>Home</kbd> and <kbd>Keypad 7</kbd> are interpreted the same, both appearing as "HOME" and do not present as two distinct keys.

Some keys do not have corresponding characters in the [game font]({{< relref "databases/font" >}}), and their key names will display as blanks in this menu. The keys still operate correctly.

{{% note %}}The game does not check or enforce that each command is bound to a unique key. It is possible (and oftentimes fun) to map multiple actions to the same key, which will all occur simultaneously whenever that key is pressed.{{% /note %}}

```c
void ShowKeyboardConfiguration(void)
{
    word x;

    isJoystickReady = false;
```

Just by entering this menu, {{< lookup/cref isJoystickReady >}} is set to false and joystick input is disabled. In order to (re)enable the joystick, the configuration sequence in {{< lookup/cref ShowJoystickConfiguration >}} must be performed again.

```c
    x = UnfoldTextFrame(3, 15, 27, "Keyboard Config.", "Press ESC to quit.");
```

The positioning of this menu is important for a few reasons. Firstly, as described above, this frame _may_ be drawn during gameplay and, as a result, cannot draw over the status bar or one-tile screen border since that will leave garbage on the screen after the menu is dismissed.

Secondly, the text-drawing calls in the inner {{< lookup/cref PromptKeyBind >}} add text into this frame dynamically, and those calls need to be compatible with the position and size of the empty area inside.

Thirdly, each time a new key setting is accepted, this menu is rapidly redrawn in place with a non-animating call to {{< lookup/cref DrawTextFrame >}}. In order to avoid having screen content move around when this occurs, the two calls need to produce visually identical results.

```c
    for (;;) {
        byte scancode;

        DrawTextLine(x,      6,  " #1) Up key is:");
        DrawTextLine(x + 19, 6,  keyNames[scancodeNorth]);
        DrawTextLine(x,      7,  " #2) Down key is:");
        DrawTextLine(x + 19, 7,  keyNames[scancodeSouth]);
        DrawTextLine(x,      8,  " #3) Left key is:");
        DrawTextLine(x + 19, 8,  keyNames[scancodeWest]);
        DrawTextLine(x,      9,  " #4) Right key is:");
        DrawTextLine(x + 19, 9,  keyNames[scancodeEast]);
        DrawTextLine(x,      10, " #5) Jump key is:");
        DrawTextLine(x + 19, 10, keyNames[scancodeJump]);
        DrawTextLine(x,      11, " #6) Bomb key is:");
        DrawTextLine(x + 19, 11, keyNames[scancodeBomb]);
        DrawTextLine(x,      15, "Select key # to change or");
        scancode = WaitSpinner(x + 21, 16);
```

The display/input sequence lives in an infinite `for` loop. On each iteration, the current key configuration is printed and a wait spinner blocks until a new selection (or <kbd>Esc</kbd>) is entered. The message "Select key # to change or[...]" appears directly above the text "Press ESC to quit." that has already been drawn into the frame.

{{< lookup/cref DrawTextLine >}} presents a combination of static text and dynamic key names looked up from the global {{< lookup/cref keyNames >}} array. This translates the numeric keyboard scancode held in the configuration variables ({{< lookup/cref scancodeNorth >}}/{{< lookup/cref scancodeSouth >}}/{{< lookup/cref scancodeWest >}}/{{< lookup/cref scancodeEast >}}/{{< lookup/cref scancodeJump >}}/{{< lookup/cref scancodeBomb >}}) into displayable strings like "&uparrow;" or "CTRL".

The call to {{< lookup/cref WaitSpinner >}} blocks until a key is pressed, then the scancode of that key is stored in the local `scancode` byte.

```c
        switch (scancode) {
        case SCANCODE_ESC:
            return;
```

Each available action is defined in a `case` inside this `switch`. In the case where the user pressed the <kbd>Esc</kbd> key, `scancode` will contain {{< lookup/cref name="SCANCODE" text="SCANCODE_ESC" >}} and execution will immediately return to the caller, terminating this function.

The caller is responsible for cleaning up the screen area that this menu occupied.

```c
        case SCANCODE_1:
            if (!PromptKeyBind(&scancodeNorth, x, "Modifying UP.")) break;
            return;
```

Otherwise, see if the first defined number key (<kbd>1</kbd>) was pressed. `scancode` would be {{< lookup/cref name="SCANCODE" text="SCANCODE_1" >}} here.

To read and process the next keystroke, the {{< lookup/cref PromptKeyBind >}} helper function is called. That function is passed a message to display ("Modifying UP.") along with a _reference_ to the variable to store the user's input into ({{< lookup/cref name="scancodeNorth" text="&scancodeNorth" >}}).

After {{< lookup/cref PromptKeyBind >}} processes the input, it returns a boolean flag indicating what the user did. The return value is _true_ when the user cancels the input by pressing <kbd>Esc</kbd>, and _false_ if the key was reconfigured successfully. This is rather backwards from what the more natural convention would dictate.

In the case where {{< lookup/cref PromptKeyBind >}} returns false, the `if` condition succeeds and execution `break`s to the statement immediately after the end of the `switch` block. In the true case, execution falls to the `return` and this menu function returns to its caller.

```c
        case SCANCODE_2:
            if (!PromptKeyBind(&scancodeSouth, x, "Modifying DOWN.")) break;
            return;
        case SCANCODE_3:
            if (!PromptKeyBind(&scancodeWest, x, "Modifying LEFT.")) break;
            return;
        case SCANCODE_4:
            if (!PromptKeyBind(&scancodeEast, x, "Modifying RIGHT.")) break;
            return;
        case SCANCODE_5:
            if (!PromptKeyBind(&scancodeJump, x, "Modifying JUMP.")) break;
            return;
        case SCANCODE_6:
            if (!PromptKeyBind(&scancodeBomb, x, "Modifying BOMB.")) break;
            return;
        }
```

The rest of the keys are more of the same. Each case responds to a different number key, displays a different prompt message, and stores the response in a distinct variable, but otherwise the operation is identical.

```c
        DrawTextFrame(7, 3, 15, 27, "Keyboard Config.", "Press ESC to quit.",
            true);
    }
}
```

This is the first statement after the end of the previous `switch` block, and is reached in response to any `break` statement encountered above. Whenever one of the key bindings is successfully changed (without canceling) we end up here.

{{< lookup/cref DrawTextFrame >}} draws the _exact_ same text frame as the initial call to {{< lookup/cref UnfoldTextFrame >}} at the top of the function, but does so without any animation. This frame is drawn practically instantaneously on top of the previous frame and all its contents, erasing all menu interactions that have occurred up until this point.

For this to work, the call arguments here have to visually match every detail of the original frame. In particular, the values for `left` and `centered` must be explicitly configured here to produce the same result.

Once the new frame has been drawn, the `for` loop repeats and redraws the inner menu text along with the updated key bindings.


{{< boilerplate/function-cref PromptKeyBind >}}

The {{< lookup/cref PromptKeyBind >}} function displays `message` text at the provided `x` position (and a fixed Y position) on the screen and reads a single scancode into the memory pointed to by `target_var`. Returns true if the user pressed the <kbd>Esc</kbd> key and false for all other keys. This is a private helper for {{< lookup/cref ShowKeyboardConfiguration >}} and should not be called outside that context.

```c
bbool PromptKeyBind(byte *target_var, word x, char *message)
{
    byte scancode;

    DrawTextLine(x + 4, 12, message);
    DrawTextLine(x + 4, 13, "Enter new key:");
    scancode = WaitSpinner(x + 18, 13);
```

Since the layout of this function is intrinsically linked to that of {{< lookup/cref ShowKeyboardConfiguration >}}, the positioning variables here are quite sensitive to changes. {{< lookup/cref DrawTextLine >}} first draws the `message` text (something like "Modifying UP.") followed by a static prompt to press the new key for this action.

{{< lookup/cref WaitSpinner >}} blocks until a key is pressed, then that key's scancode is stored in `scancode` and execution continues.

```c
    if (scancode == SCANCODE_ESC) return true;

    *target_var = scancode;

    return false;
}
```

If the user happened to press the <kbd>Esc</kbd> key, `scancode` will be {{< lookup/cref name="SCANCODE" text="SCANCODE_ESC" >}}. In this case, do not change anything and immediately `return` a true value to the caller indicating this.

Otherwise, replace the content of the memory that `target_var` points to with the value in `scancode`. This changes the scancode for a particular in-game action globally for the rest of the program. After doing that, `return` a false value to inform the caller that a change has been made.

{{< boilerplate/function-cref ShowSoundTest >}}

The {{< lookup/cref ShowSoundTest >}} function presents a menu that allows the user to seek through and preview each sound effect available in the game. Sounds are selected using the <kbd>&downarrow;</kbd>/<kbd>&uparrow;</kbd> keys and played with the <kbd>Enter</kbd> key. At any time, <kbd>Esc</kbd> exits this menu.

{{< boilerplate/dialog-gameplay object="menu" may=true >}}

This menu is less of a "test" and more of a "demonstration" of the sound effects -- if any one of them plays correctly they all should. Sound effect priority is respected, meaning some sounds are capable of interrupting others while some cannot. Sounds play from this menu regardless of the global sound on/off configuration.

If a key is held down, the keyboard will continually send "make" codes to the keyboard controller which _for certain keys_ is interpreted as rapid pressing of that key. This occurs with the "extended" keys from the 101-key layout -- holding the standalone arrow keys seeks quickly through the numbers, and the numeric keypad <kbd>Enter</kbd> key keeps restarting each sound effect's playback -- while the main <kbd>Enter</kbd> key and numeric keypad arrow keys aren't repeated in this way. This behavior is caused by an oversight in the {{< lookup/cref WaitSpinner >}} function.

```c
void ShowSoundTest(void)
{
    word x;
    bool enabled = isSoundEnabled;
    dword soundnum = 1;

    isSoundEnabled = true;
```

In order to produce sound regardless of the user's current sound effect preferences, the global {{< lookup/cref isSoundEnabled >}} variable is fudged true in this function. To facilitate restoring this setting to its previous state, a copy of the original value is maintained in `enabled`.

`soundnum` is the selected sound effect number, which starts at 1 each time the menu is entered.

```c
    x = UnfoldTextFrame(2, 7, 34, "Test Sound", "Press ESC to quit.");
    DrawTextLine(x, 4, " Press \x18 or \x19 to change sound #.");
    DrawTextLine(x, 5, "   Press Enter to hear sound.");
```

An empty frame is drawn with a call to {{< lookup/cref UnfoldTextFrame >}} and instructions are added with {{< lookup/cref DrawTextLine >}}. The escaped bytes `\x18` and `\x19` display as "&uparrow;" and "&downarrow;" respectively.

```c
    for (;;) {
        byte scancode;
        int i;

        DrawNumberFlushRight(x + 16, 6, soundnum);
        scancode = WaitSpinner(x + 31, 7);
```

The main body of this function is an infinite `for` loop that repeats for each keypress. On each iteration, {{< lookup/cref DrawNumberFlushRight >}} draws the current value for `soundnum` into the frame, and {{< lookup/cref WaitSpinner >}} blocks until a key is pressed. Once that occurs, the scancode of the pressed key is returned into `scancode`.

```c
        if (scancode == SCANCODE_KP_2 && soundnum > 1)  soundnum--;
        if (scancode == SCANCODE_KP_8 && soundnum < 65) soundnum++;
```

If the `scancode` received is {{< lookup/cref name="SCANCODE" text="SCANCODE_KP_2" >}} (the numeric keypad <kbd>2 / &downarrow;</kbd> key) and the `soundnum` is greater than 1, decrement `soundnum`. This handles the "seek down" behavior without allowing the user to scroll earlier then the first sound.

If the `scancode` received is {{< lookup/cref name="SCANCODE" text="SCANCODE_KP_8" >}} (the numeric keypad <kbd>8 / &uparrow;</kbd> key) and the `soundnum` is less than 65 (the highest sound number used in the game), increment `soundnum`. This is "seek up," without proceeding past the last sound.

```c
        if (scancode == SCANCODE_ESC) {
            isSoundEnabled = enabled;
            break;
        }
```

At any point, the user can press the <kbd>Esc</kbd> key, which stores {{< lookup/cref name="SCANCODE" text="SCANCODE_ESC" >}} in `scancode`. This means the user wants to leave this menu.

Before returning, the original value of {{< lookup/cref isSoundEnabled >}} must be restored from `enabled`. (Recall that this was forced true to allow sound playback here, even if the user disabled the sound elsewhere in the game.)

The `break` statement terminates the `for` loop, and execution falls off the end of the function. Control returns to the caller, who is responsible for cleaning up the screen area where this menu was.

```c
        if (scancode == SCANCODE_ENTER) {
            StartSound((word)soundnum);
        }
```

The final case to handle is <kbd>Enter</kbd> ({{< lookup/cref name="SCANCODE" text="SCANCODE_ENTER" >}}), which plays the selected sound. This is accomplished simply by passing the current value of `soundnum` to {{< lookup/cref StartSound >}}. (`soundnum` is defined as a doubleword, while a word is expected here, hence the cast.)

{{< lookup/cref StartSound >}} returns immediately, having queued the sound effect for asynchronous playback.

```c
        for (i = 0; i < 3; i++) {
            EraseWaitSpinner(x + 14 + i, 6);
        }
    }
}
```

Finally, a bit of visual cleanup: It's possible that the sound number has changed during this loop iteration (as would be the case if an up or down key was pressed). Due to this fact, it's possible that the next iteration will draw numbers with transparent areas on top of the old digits, leaving those screen tiles in an unreadable state. To counter this, {{< lookup/cref EraseWaitSpinner >}} is called in a loop to blank the three(!) tiles where the sound number appears, leaving them clear for their values to be redrawn anew.

{{% aside class="armchair-engineer" %}}
**Better to clear too much than too little.**

This explicit tile-clearing behavior is only _partially_ necessary -- all of the digits in the game's font are fully opaque on a solid gray background. Simply drawing a new digit directly on top of an old one is enough to accomplish most of the job, and that's exactly what the status bar does during gameplay.

The necessity comes when the counter decrements from e.g. 10 to 9. In that case, absent this clearing loop, nothing redraws the tens place and the resulting display would be "19." A similar thing occurs in the hundreds place going from 100 to 99, resulting in an incorrect "199" being displayed. Rather than try to catch these cases as they occur, the entire number area is wiped and redrawn during every iteration.
{{% /aside %}}

This code would allow a three-digit sound number to be displayed correctly, although this game only goes up to double-digits.

The `for` loop repeats, redrawing the current value of `soundnum` and waiting for the next keypress.

{{< boilerplate/function-cref PromptSaveGame >}}

The {{< lookup/cref PromptSaveGame >}} function displays a menu that prompts the user to pick a save game slot (1-9) to save the state of their game into, then the save is carried out. The user may cancel this prompt without saving by pressing <kbd>Esc</kbd>, <kbd>Space</kbd>, or <kbd>Enter</kbd>. Due to the limited structure of the [save file format]({{< relref "save-file-format" >}}), the initial state of the map and all its state variables is used -- all progress made since the level was last (re)started is abandoned when a save is loaded.

{{< boilerplate/dialog-gameplay object="menu" >}}

```c
void PromptSaveGame(void)
{
    byte scancode;
    word tmphealth, tmpbombs, tmplevel, tmpstars, tmpbars;
    dword tmpscore;
    word x = UnfoldTextFrame(8, 10, 28, "Save a game.",
        "Press ESC to quit.");

    DrawTextLine(x, 11, " What game number (1-9)?");
    DrawTextLine(x, 13, " NOTE: Game is saved at");
    DrawTextLine(x, 14, " BEGINNING of level.");
    scancode = WaitSpinner(x + 24, 11);
```

This function defines a number of `tmp...` variables that are used to hold the state of a few of the global player state variables while the save function is being carried out.

{{< lookup/cref UnfoldTextFrame >}} and {{< lookup/cref DrawTextLine >}} present the initial UI of the save dialog, then {{< lookup/cref WaitSpinner >}} blocks until a key is pressed. The scancode of that pressed key is returned into `scancode`.

```c
    if (
        scancode == SCANCODE_ESC || scancode == SCANCODE_SPACE ||
        scancode == SCANCODE_ENTER
    ) {
        return;
    }
```

The "cancel" case is handled first, responding to any of the <kbd>Esc</kbd>/<kbd>Space</kbd>/<kbd>Enter</kbd> keys (`scancode` is one of {{< lookup/cref name="SCANCODE" text="SCANCODE_ESC" >}}/{{< lookup/cref name="SCANCODE" text="SCANCODE_SPACE" >}}/{{< lookup/cref name="SCANCODE" text="SCANCODE_ENTER" >}}). If any of these keys matched, immediately `return` to the caller without doing anything further.

```c
    if (scancode >= SCANCODE_1 && scancode < SCANCODE_0) {
        DrawScancodeCharacter(x + 24, 11, scancode);

        tmphealth = playerHealth;
        tmpbombs = playerBombs;
        tmpstars = (word)gameStars;
        tmplevel = levelNum;
        tmpbars = playerHealthCells;
        tmpscore = gameScore;

        LoadGameState('T');
        SaveGameState('1' + (scancode - SCANCODE_1));

        playerHealth = tmphealth;
        playerBombs = tmpbombs;
        gameStars = tmpstars;
        levelNum = tmplevel;
        gameScore = tmpscore;
        playerHealthCells = tmpbars;
```

Otherwise, if `scancode` is between {{< lookup/cref name="SCANCODE" text="SCANCODE_1" >}} and _{{< lookup/cref name="SCANCODE" text="SCANCODE_9" >}}_ (remember, <kbd>0</kbd> comes after <kbd>9</kbd> on the keyboard) the user selected a valid save slot. Do the save.

Before moving on, {{< lookup/cref DrawScancodeCharacter >}} draws the `scancode` character that the user typed on top of the last wait spinner that was showing. This nice bit of polish creates the illusion that the previous wait spinner was a full-fledged text entry area, and ensures that there is not an abandoned spinner frozen elsewhere on the screen.

To explain the use of all the `tmp...` variables, we need to first jump to the center of the save: the {{< lookup/cref LoadGameState >}}/{{< lookup/cref SaveGameState >}} pair. In a hypothetical world where the [save file]({{< relref "save-file-format" >}}) could represent a level midway through, the file would need to contain data for every player variable, actor structure, and global map variable in the game. The act of saving and reloading would be quite complicated, with any bit of mishandled state creating an opportunity for a potentially game-ruining bug. Instead of doing all this, the game simply saves and loads game state at the beginning of each level, relying on the regular game initialization code to ensure all the variables and structures for map objects are set in a predictable way. By handling saved games in this way, the game can leverage the existing systems that handle the case where the player dies and the current level restarts: the level returns to its initial state, and the player's score/health/etc. variables return to the values they had when the level was first entered.

This "restart at the beginning" bookkeeping is performed during every call to {{< lookup/cref InitializeLevel >}}. As part of its level-changing duties, it calls {{< lookup/cref name="SaveGameState" text="SaveGameState('T')" >}} to fill the temporary (`T`) save slot with the level state. Later, any call to {{< lookup/cref name="LoadGameState" text="LoadGameState('T')" >}} restores that state, thus returning the player variables to the way they were when the level started.

In this function, we aren't interested in restoring the state to restart the level, but rather to produce a save file that has the _effect_ of restarting the level. To accomplish that, {{< lookup/cref LoadGameState >}} restores the temporary save state, which is immediately rewritten via {{< lookup/cref SaveGameState >}} to the specified save slot. The save slot identifier is a character between `1` and `9`, generated by computing the difference between the entered `scancode` and {{< lookup/cref name="SCANCODE" text="SCANCODE_1" >}} and adding that to the numeric value of the `1` byte (31h). This becomes the final character of the save file's extension on disk.

{{% aside class="armchair-engineer" %}}
**\<raises hand sheepishly>**

If you're wondering, "couldn't the same thing have been accomplished by simply copying the `.SVT` file on disk to the specified `.SV?` file?" you are absolutely right -- that would accomplish the same thing without messing with the global state of the program.

The main downside to that approach is that the game would then have to implement a "file copy" function of its own. There is no such thing available in the C standard library. Even today, there is no standardized cross-platform way to copy files without reading one file and writing the other in a loop.
{{% /aside %}}

With all of that in context, the `tmp...` variables make more sense: {{< lookup/cref LoadGameState >}} destroys the current player's progress by resetting the game state to the way it was at the start of the level, so each affected variable ({{< lookup/cref playerHealth >}}/{{< lookup/cref playerBombs >}}/{{< lookup/cref gameStars >}}/{{< lookup/cref levelNum >}}/{{< lookup/cref playerHealthCells >}}/{{< lookup/cref gameScore >}}) must be stashed and then restored. As you might imagine, all this rigmarole [creates a bug]({{< relref "#cheat-re-use-bug" >}}).

```c
        x = UnfoldTextFrame(7, 4, 20, "Game Saved.", "Press ANY key.");
        WaitSpinner(x + 17, 9);
```

With the save file written and the game state restored, inform the user that the process succeeded with a small {{< lookup/cref UnfoldTextFrame >}} message. {{< lookup/cref WaitSpinner >}} waits for any key to be pressed, and the return value is discarded.

The function returns from here.

```c
    } else {
        x = UnfoldTextFrame(11, 4, 28, "Invalid game number!",
            "Press ANY key.");
        WaitSpinner(x + 25, 13);
    }
}
```

An error-handling case occurs if the user pressed any key at the original prompt other than a valid save slot number or a "cancel" key. Whenever that happens, {{< lookup/cref UnfoldTextFrame >}} shows a small error message and {{< lookup/cref WaitSpinner >}} blocks until any key is pressed. The return value is discarded, and execution falls off the end of the function.

This function can return from a few points. In all cases, none of the screen content presented by this menu is explicitly cleaned up. The caller is responsible for clearing and redrawing a sensible screen after this menu is dismissed.

### Cheat Re-Use Bug

There is a bug in this function that occurs in the code path where a save file gets written.

While the important player variables are stashed and restored using `tmp...` variables in this function, not every variable affected by {{< lookup/cref LoadGameState >}} is preserved. In particular, the {{< lookup/cref usedCheatCode >}} boolean flag is reloaded without protection. This allows a careful player to circumvent the "one cheat per game" limitation.

If the cheat code had not yet been used when a level was entered, the temporary save file will have recorded a false value in the {{< lookup/cref usedCheatCode >}} field. If the cheat is later used, {{< lookup/cref usedCheatCode >}} becomes true and stays that way -- preventing another invocation of the cheat code. However, saving the game will unintentionally restore this flag back to the false value it had previously, allowing it to be used again.

As long as the user performs a "save game" command shortly after every use of the cheat code, the cheat can be reused as many times as desired without restriction.

{{< boilerplate/function-cref PromptRestoreGame >}}

The {{< lookup/cref PromptRestoreGame >}} function displays a menu that prompts the user to pick a save game slot (1-9) to load from, and gameplay jumps to that state. The user may cancel this prompt without loading by pressing <kbd>Esc</kbd>, <kbd>Space</kbd>, or <kbd>Enter</kbd>. The return value is one of the {{< lookup/cref RESTORE_GAME >}} constants:

* {{< lookup/cref name="RESTORE_GAME" text="RESTORE_GAME_SUCCESS" >}} when the saved game has been successfully loaded
* {{< lookup/cref name="RESTORE_GAME" text="RESTORE_GAME_NOT_FOUND" >}} if a nonexistent slot was picked, or
* {{< lookup/cref name="RESTORE_GAME" text="RESTORE_GAME_ABORT" >}} if the request was canceled.

{{< boilerplate/dialog-gameplay object="menu" may=true >}}

```c
byte PromptRestoreGame(void)
{
    byte scancode;
    word x = UnfoldTextFrame(11, 7, 28, "Restore a game.",
        "Press ESC to quit.");

    DrawTextLine(x, 14, " What game number (1-9)?");
    scancode = WaitSpinner(x + 24, 14);

    if (
        scancode == SCANCODE_ESC || scancode == SCANCODE_SPACE ||
        scancode == SCANCODE_ENTER
    ) {
        return RESTORE_GAME_ABORT;
    }
```

The first half of this function is essentially identical to {{< lookup/cref PromptSaveGame >}} and there's no need to repeat all that here. One small difference is the return value -- when the user cancels here, {{< lookup/cref name="RESTORE_GAME" text="RESTORE_GAME_ABORT" >}} is returned to inform the caller that the current state of the game should continue.

```c
    if (scancode >= SCANCODE_1 && scancode < SCANCODE_0) {
        DrawScancodeCharacter(x + 24, 14, scancode);
```

Also similar to {{< lookup/cref PromptSaveGame >}}, the input validation and input echo behavior work the same.

```c
        if (!LoadGameState('1' + (scancode - SCANCODE_1))) {
            return RESTORE_GAME_NOT_FOUND;
        } else {
            return RESTORE_GAME_SUCCESS;
        }
```

While the saved game's slot character is computed the same way as in {{< lookup/cref PromptSaveGame >}} (the difference between `scancode` and {{< lookup/cref name="SCANCODE" text="SCANCODE_1" >}}, combined with the numeric value of the `1` character), the similarities end there.

The save slot character (`1`--`9`) is passed to a {{< lookup/cref LoadGameState >}} call, which carries out the actual load duties. That function returns true if the load completed successfully, or false if the requested save file could not be loaded. These returned values are mapped to either {{< lookup/cref name="RESTORE_GAME" text="RESTORE_GAME_SUCCESS" >}} or {{< lookup/cref name="RESTORE_GAME" text="RESTORE_GAME_NOT_FOUND" >}} as appropriate, and that value is returned to the caller.

{{< lookup/cref LoadGameState >}} has a side-effect that may occur from time to time: If the save file has been manipulated such that its internal checksum no longer matches, it will show an "altered file error" message and exit to DOS. If that happens, control never returns back here prior to the program exiting.

```c
    } else {
        x = UnfoldTextFrame(11, 4, 28, "Invalid game number!",
            "Press ANY key.");
        WaitSpinner(x + 25, 13);
    }

    return RESTORE_GAME_ABORT;
}
```

As with {{< lookup/cref PromptSaveGame >}}, validation failure is met with an error message, and {{< lookup/cref name="RESTORE_GAME" text="RESTORE_GAME_ABORT" >}} is returned to the caller.

{{< boilerplate/function-cref PromptLevelWarp >}}

The {{< lookup/cref PromptLevelWarp >}} function prompts the user to select a map number from 1 to 12 (or 13, depending on the episode) and jumps to the start of the chosen map. Returns true if the map changed, or false if the user entered a non-numeric or out-of-range value.

{{< boilerplate/dialog-gameplay object="menu" >}}

```c
bbool PromptLevelWarp(void)
{
#ifdef HAS_MAP_11
#   define MAX_MAP "13"
    word levels[] = {0, 1, 4, 5, 8, 9, 12, 13, 16, 17, 20, 2, 3};
#else
#   define MAX_MAP "12"
    word levels[] = {0, 1, 4, 5, 8, 9, 12, 13, 16, 17, 2, 3};
#endif
```

This menu has a slightly different range based on the episode being played. In episode 1 `HAS_MAP_11` is defined, indicating eleven regular maps, while episodes 2 and 3 only have ten. All episodes have two bonus maps in addition to the regular ones. Here a `MAX_MAP` macro is defined to adjust the prompt text to the actual number of maps available, and the `levels[]` array is initialized with the internal level numbers of the map progression.

The distinction between maps and levels, while usually inconsequential, matters here. The **maps** are the concrete data grids that the players and actors can move around, and the **levels** track the sequential order in which the maps are played. Levels 0 and 1 correspond to maps 1 and 2, which is logical and simple enough to follow. In the gameplay progression, however, the next level in sequence is one of the "bonus" levels, selected based on how many stars the player collected. These bonus levels occupy level slots 2 and 3, and switching logic selects one (or none) of them dynamically. By the time level slot 4/5 are reached, maps 3/4 are loaded. Then level slots 6/7 _replay_ the same bonus map(s), and level slot 8 begins map 5. This pattern continues until the game ends. (See {{< lookup/cref NextLevel >}} for the implementation of this progression.)

With that in mind, the (zero-indexed) map progression and its relationship to the level number stored in `levels[]` makes sense. Every two levels, the level number skips ahead by two to jump over the bonus levels. The last two elements are the bonus levels _whose positions in the progression are hard-coded to their first occurrences in the game._ Concretely, this means that warping to one of the bonus levels and playing to completion will always take you to level 4, the third map in the episode.

```c
    char buffer[3];
    int x = UnfoldTextFrame(2, 4, 28, "Warp Mode!",
        "Enter level (1-" MAX_MAP "):");
```

More local variables are defined. `buffer[]` is a three-byte buffer used to store the string entered by the user, which is a maximum two-digit string with an additional null terminator byte. `x` is the X coordinate of the inside of the message frame drawn by {{< lookup/cref UnfoldTextFrame >}}.

`MAX_MAP` is used here to dynamically change the maximum map number displayed.

```c
    ReadAndEchoText(x + 21, 4, buffer, 2);

    x = atoi(buffer) - 1;
```

{{< lookup/cref ReadAndEchoText >}} displays a wait spinner and reads keyboard input, moving the spinner as a text insertion caret. As characters are entered, they are written into the passed `buffer` area. When the user completes their input and presses the <kbd>Enter</kbd> key, this function returns and `buffer` contains the entered text along with a null terminator.

`buffer` is then passed to the {{< lookup/cref atoi >}} (**A**SCII **to** **i**nteger) library function, which returns the numeric representation of the user's entry into the repurposed `x` variable. This variable is decremented by one to make it zero based.

The subtraction also has the secondary benefit of discerning invalid input: For any input value that cannot be parsed into an integer, {{< lookup/cref atoi >}} returns 0. `x` would then have a value of -1 for any input that is not numeric.

```c
    if (x >= 0 && x <= (sizeof levels / sizeof levels[0]) - 1) {
        levelNum = x;
        LoadGameState('T');
        InitializeLevel(levels[x]);

        return true;
    }

    return false;
}
```

Here `x` is bounds-checked: It should be at least 0, and less than the number of elements in the `levels[]` array for this episode (`sizeof levels` divided by `sizeof levels[0]`). If the input is within that range, it's a valid map number and we should jump there.

{{< lookup/cref levelNum >}} is set to `x`, which is an incorrect (and pointless) assignment. `x` contains a map number, while {{< lookup/cref levelNum >}} is a level number. This does not matter anyway, because the following two function calls rewrite {{< lookup/cref levelNum >}} again.

{{< lookup/cref name="LoadGameState" text="LoadGameState('T')" >}} reloads the player's state from the most recently written temporary save file. This has the effect of resetting the player's health/score/etc. to the values they had when the current level started -- similar to what would happen if the player died and the level restarted.

The actual work occurs in {{< lookup/cref InitializeLevel >}}, which actually loads the specified map and resets all of the actors and dynamic variables needed to play it. The `levels[x]` lookup translates the user-provided map number into a usable level number.

The function returns true in this path, to indicate to the caller that the game loop must restart from the beginning on this new level. Otherwise false is returned, indicating that the user entered junk (or nothing) at the prompt. The caller takes this to mean that no changes occurred and the game loop should continue as before.
