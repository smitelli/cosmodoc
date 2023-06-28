+++
title = "Dialog Functions"
description = "Describes functions that display simple dialog screens."
weight = 370
+++

# Dialog Functions

While the [menu functions]({{< relref "menu-functions" >}}) are responsible for presenting multiple-choice input prompts and handling UI logic, the **dialog functions** are much simpler means of presenting information. Dialogs are presented progressively, showing a static page of text (and sometimes graphics) with no interactivity beyond waiting for keypresses that dismiss the messages.

{{< table-of-contents >}}

Some dialogs are split across multiple pages, and any keypress will advance to the next page. Some of these multi-page dialogs allow the user to move backward through the pages by pressing a different key, and can be exited early by pressing the <kbd>Esc</kbd> key.

Dialogs presented during gameplay are usually a single page with text displayed progressively using a "typewriter" animation effect. The user can press <kbd>Space</kbd> during these dialogs to hurry through the animation and get back to playing the game.

## Dialog Structure

The essence of any dialog is spread across three function calls: {{< lookup/cref UnfoldTextFrame >}} presents an empty area where the content will be drawn, {{< lookup/cref DrawTextLine >}} fills the frame with text (and occasionally graphical elements), and {{< lookup/cref WaitSpinner >}} pauses execution until a key is pressed. With these core functions, and an occasional smattering of additional logic, the vast majority of dialogs can be constructed.

Each call to {{< lookup/cref UnfoldTextFrame >}} takes values for width, height, and the top position of the frame. Two lines of text -- one for the top of the frame and one for the bottom -- are also passed and can be used to pre-fill some of the frame's content. Usually these text fragments will be a type of header or footer, but sometimes the bulk of the dialog message can be conveyed if it is short enough.

The new text frame overwrites anything that may have been on the screen previously, leaving a solid gray canvas for subsequent drawing operations to use.

{{< image src="demo-frame-2052x.png"
    alt="Dialog demo frame, highlighting top and bottom texts."
    1x="demo-frame-684x.png"
    2x="demo-frame-1368x.png"
    3x="demo-frame-2052x.png" >}}

{{< lookup/cref DrawTextLine >}} is the next step in filling the frame, and this function does the majority of the work in dialog functions. This function (quite obviously) renders text from the [game font]({{< relref "databases/font" >}}) onto the specified location on screen, but it can also use a primitive form of markup to insert graphics for the [player]({{< relref "databases/player-sprite" >}}), an [actor sprite]({{< relref "databases/actor-sprite" >}}), or a [cartoon image]({{< relref "databases/cartoon-sprite" >}}) within the text. It can also be configured to animate the text character-by-character, playing a typewriter sound effect as each non-space symbol appears.

Each call to {{< lookup/cref DrawTextLine >}} produces one line of output -- newline characters are not handled. If an image that is more than one tile high is drawn, its bottom row is aligned with the text line. Any text that should be drawn to the right of an inline image needs to be prefixed with some number of space characters to prevent the characters from being drawn on top of the image's tiles.

Finally, {{< lookup/cref WaitSpinner >}} presents an animated green spinning icon at the requested X,Y position and execution blocks until a key is pressed. Once that happens, the scancode of that key is returned to the dialog function in case it wants to take different actions depending on the chosen key.

{{< aside class="fun-fact" >}}
**You impetuous young boy.**

Due to a quirk in {{< lookup/cref WaitSpinner >}}'s handling of extended PS/2 scancodes, it's possible to speed through most dialogs (including those that occur during gameplay) by holding one of the extended keys -- a good example is the standalone arrow keys.
{{< /aside >}}

{{< image src="demo-2052x.png"
    alt="Dialog demo."
    1x="demo-684x.png"
    2x="demo-1368x.png"
    3x="demo-2052x.png" >}}

In code, this representative dialog function looks like this:

```c
void DialogDemo(void)
{
    word x = UnfoldTextFrame(3, 19, 35, "Dialog Demo", "Press any key.");

    DrawTextLine(x + 1,  6,  "This is a plain line of text.");
    DrawTextLine(x + 20, 9,  "Right-align,");
    DrawTextLine(x + 20, 10, "if you must.");
    DrawTextLine(x + 1,  11, "\xFD""027   Players\xFD""004");
    DrawTextLine(x + 1,  16, "Barrel:\xFE""029000");
    DrawTextLine(x + 16, 16, "Cartoon:\xFB""003");
    DrawTextLine(x + 1,  18, "\xFC""003This was animated (trust me).");

    WaitSpinner(x + 32, 20);
}
```

This function is rife with magic numbers, so we'll go through them piece by piece.

The outermost frame presented by {{< lookup/cref UnfoldTextFrame >}} is 35&times;19 tiles in size. This includes the border tiles, so the actual inner area is 33&times;17 tiles. In this example, the frame is drawn three tiles down from the top of the screen. (The image here is cropped, so this position is not visible.) The frame is drawn horizontally centered on the screen -- there is no math in this function that computes horizontal position. The top and bottom texts on the dialog frame are also drawn centered automatically without any additional calculation.

The value returned into `x` is the horizontal screen position of the first column of gray tiles inside the frame. This is utilized by the subsequent {{< lookup/cref DrawTextLine >}} and {{< lookup/cref WaitSpinner >}} calls as a way to determine where the left edge of the frame ended up after the centering calculations were done. (For narrower frames, `x` holds a larger value and left-aligned elements move towards the right to stay inside the frame boundaries.)

Horizontal calculations are all relative to the frame, so the additions of `+ 1`, `+ 20`, `+ 16`, and `+ 32` all reference screen columns some fixed number of tiles away from the left edge of the frame.

The vertical positions are _absolute_, and do not change as the top position of the frame is adjusted. An an example, the line of text containing "Right-align" is on screen row 9, while the frame starts on screen row 3, implying that the line would appear on the sixth row of the frame.

{{< image src="demo-annotated-2052x.png"
    alt="Dialog demo with coordinates."
    1x="demo-annotated-684x.png"
    2x="demo-annotated-1368x.png"
    3x="demo-annotated-2052x.png" >}}

There are no provisions to automatically right- or bottom-align any content within the frame. The designer of the frame must set the position of the first character in the text line such that the last character ends up where it needs to be. Likewise, text flow does not automatically advance to clear any images that have been drawn, meaning that space characters must be inserted before any element that appears to the right of an image (an example of this occurs in the "Players" construction).

Graphics are inserted by using an escape sequence in the text argument passed to {{< lookup/cref DrawTextLine >}}. The bytes `\xFD027` are interpreted as FDh (this is the command to draw a player sprite) followed by the three-digit fixed decimal number 027. This draws [player sprite]({{< relref "databases/player-sprite" >}}) frame 27 with its bottom-left tile anchored at the position where the sequence was encountered. Similarly, `\xFB003` is a "draw [cartoon image]({{< relref "databases/cartoon-sprite" >}})" command with frame 3 as its three-digit argument. `\xFE029000` is a "draw [actor sprite]({{< relref "databases/actor-sprite" >}})" command, which takes _two_ three-digit arguments: the sprite type is 29, and the frame is 0. These command sequences are split up in the C code to prevent the parser from treating them as hexadecimal values &ge; 256.

The last command is a little different. `\xFC003` is the "draw animated" command, and its three-digit argument sets an inter-character delay of 3. (One delay unit is approximately 1 &#x2215; 47 of a second.) This command draws all subsequent characters one-by-one with a delay and a sound effect between each one. Any time such animated text is being drawn, the user can hold <kbd>Space</kbd> to speed through the animation.

{{< note >}}The "draw animated" command is not persisted after {{< lookup/cref DrawTextLine >}} returns. To draw multiple lines of text with animation, each call needs to re-enable the "draw animated" mode explicitly.{{< /note >}}

The {{< lookup/cref DrawTextLine >}} commentary explains all of the drawing commands in great detail.

Finally, {{< lookup/cref WaitSpinner >}} blocks until a key is pressed. The X any Y position of this element need to be carefully determined, as the game's design conventions dictate that the spinner should always be in the bottom right corner. This makes it sensitive to changes in the frame's top, width, _and_ height. Here we discard the return value, so all keypresses are treated identically and end the dialog function. Some dialogs act on the return value, which holds the scancode of the key that was pressed.

When the dialog function returns, the frame is still visible on the screen. Aside from the wait spinner, which erases itself upon return, none of the frame contents know how to clean themselves up. The caller is responsible for redrawing something sensible on top of the defunct dialog's screen contents once it regains control.

## Dialog Sequences

Some longer dialog functions consist of "sequences" of two or more dialog frames. As the reader progresses through the frames, there are a few different ways to handle switching from one frame to the next.

### Fades

With one dialog on the screen, {{< lookup/cref FadeOut >}} or a similar function fades the screen contents away by modifying the EGA palette registers. The old frame is still present in the video memory, but it does not appear on the screen because all the colors are mapped to black. While the screen is faded, a function like {{< lookup/cref ClearScreen >}} can erase the buffer and prepare for a new frame to be drawn. Once the screen content has been recreated to the designer's liking, {{< lookup/cref FadeIn >}} will bring it into view. This is also the common technique used when transitioning from/to a gameplay mode or a full-screen image.

The animation employed by {{< lookup/cref UnfoldTextFrame >}} is not visible while the screen is faded, but it does still occur and it does take some time to complete. This can artificially increase the amount of time the screen stays faded.

### Overwrites

With one dialog on the screen, {{< lookup/cref UnfoldTextFrame >}} simply draws a replacement frame directly on top of it. This works well when the new frame is larger, or has the same size/position as the old frame. When the new frame is smaller than the old, remnants of the old frame remain visible in areas that the new frame did not cover up.

## Gameplay Interactions

It's relatively straightforward to reason about the behavior of the drawing functions during the main menu and any submenus that are accessed below it. While the game is running, however, there are a few additional considerations.

### Screen Contents

The screen is conceptually divided into two regions during gameplay -- the game world which is redrawn every frame, and the status bar which is partially redrawn when one of the score values changes. (There is also a one-tile black border at the top/left/right edges of the game world area, which behaves as the status bar does.)

The area covered by the game world requires no special attention. When a dialog is dismissed, a new frame of gameplay replaces it automatically. The status bar, however, is sensitive -- its background image is only drawn when the level begins, and the values in the bar are only redrawn when they change. If a dialog were to cover part of the status bar, it would not be properly cleaned up and a ghost image would persist for the remainder of the game.

{{< image src="ghost-dialog-2052x.png"
    alt="Dialog-over-status bar ghost image demonstration."
    1x="ghost-dialog-684x.png"
    2x="ghost-dialog-1368x.png"
    3x="ghost-dialog-2052x.png" >}}

### Page Flipping

The game maintains two copies of the screen contents. While one page is being drawn, the opposite page is being shown on the screen. Once drawing completes, the two pages switch roles and the screen's full contents are updated atomically. This is done to prevent the user from being able to see a half-drawn screen of content as the display hardware updates faster than the game's redrawing rate.

As a consequence of this, any of the [low-level drawing functions]({{< relref "assembly-drawing-functions" >}}) called as part of a dialog's presentation could be drawing to a page that is not visible to the user. If such a dialog function were to block waiting for input, the game would appear to freeze without giving the user any indication of what the wait is for or what they should do about it.

Dialogs shown during the game must ensure that they are drawing to the page that is actively being displayed (or to set the active page to the one being drawn to). Typically this is done by either calling {{< lookup/cref SelectDrawPage >}} with {{< lookup/cref activePage >}} as the argument, or by calling {{< lookup/cref SelectDrawPage >}} and {{< lookup/cref SelectActivePage >}} and setting both to the same page number (usually page zero).

{{< boilerplate/function-cref ShowCopyright >}}

The {{< lookup/cref ShowCopyright >}} function is the first dialog presented after the title screen. It shows an abbreviated list of credits, the copyright year, and the game version. The frame is adorned with a pair of player sprites looking inward.

{{< image src="copyright-2052x.png"
    alt="Copyright Dialog"
    1x="copyright-684x.png"
    2x="copyright-1368x.png"
    3x="copyright-2052x.png" >}}

```c
void ShowCopyright(void)
{
    word x = UnfoldTextFrame(4, 13, 26, "A game by", "Copyright (c) 1992");
    DrawTextLine(x,      7,  "     Todd J Replogle");
    DrawTextLine(x + 11, 9,  "and");
    DrawTextLine(x,      11, "\xFD""027   Stephen A Hornback\xFD""004");
    DrawTextLine(x,      13, "      Version " GAME_VERSION);

    WaitSoft(700);
    FadeOut();
}
```

The {{< lookup/cref GAME_VERSION >}} constant is "1.20" in every copy of the game I have ever seen -- if you have a different version or a non-English release of the game, I would be very interested in taking a look at it!

Unlike most dialogs, this uses {{< lookup/cref WaitSoft >}} to pause for a fixed length of time in lieu of presenting a wait spinner. If the user presses a key, the wait can be skipped.

In preparation for the [title loop]({{< relref "menu-functions#title-loop" >}}), this dialog ends with a call to {{< lookup/cref FadeOut >}} which blanks the screen before any subsequent drawing operations occur.

{{< boilerplate/function-cref ShowRestoreGameError >}}

The {{< lookup/cref ShowRestoreGameError >}} function shows when the user tries to restore a saved game whose file does not exist. This dialog is shown when {{< lookup/cref PromptRestoreGame >}} returns the {{< lookup/cref name="RESTORE_GAME" text="RESTORE_GAME_NOT_FOUND" >}} status.

{{< boilerplate/menu-gameplay object="dialog" may=true >}}

{{< image src="restore-game-error-2052x.png"
    alt="Restore Game Error Dialog"
    1x="restore-game-error-684x.png"
    2x="restore-game-error-1368x.png"
    3x="restore-game-error-2052x.png" >}}

```c
void ShowRestoreGameError(void)
{
    word x = UnfoldTextFrame(5, 4, 20, "Can't find that",
        "game to restore! ");
    WaitSpinner(x + 17, 7);
}
```

The bottom text of this dialog ends with a trailing space, perhaps to ensure that there is always room for the wait spinner. It is not actually necessary in practice.

{{< boilerplate/function-cref ShowAlteredFileError >}}

The {{< lookup/cref ShowAlteredFileError >}} function shows when the user tries to load a manipulated save file whose checksum does not match the expected value. It is called by {{< lookup/cref LoadGameState >}} and is always followed by an unconditional call to {{< lookup/cref ExitClean >}}, quitting the game.

{{< boilerplate/menu-gameplay object="dialog" may=true >}}

{{< image src="altered-file-error-2052x.png"
    alt="Altered File Error Dialog"
    1x="altered-file-error-684x.png"
    2x="altered-file-error-1368x.png"
    3x="altered-file-error-2052x.png" >}}

```c
void ShowAlteredFileError(void)
{
    word x = UnfoldTextFrame(2, 4, 28, "Altered file error!!",
        "Now exiting game!");
    WaitSpinner(x + 25, 4);
}
```

{{< boilerplate/function-cref ShowStory >}}

The {{< lookup/cref ShowStory >}} function shows a progression of six pages of dialog frames that explain the basic premise of the game. The screens can only be viewed sequentially, with no provision to exit or view a previous page once dismissed.

{{< image src="story-2052x.png"
    alt="Story Dialogs"
    1x="story-684x.png"
    2x="story-1368x.png"
    3x="story-2052x.png" >}}

```c
void ShowStory(void)
{
    word x;

    FadeOut();
    ClearScreen();

    x = UnfoldTextFrame(1, 23, 38, "STORY", "Press ANY key.");
    DrawTextLine(x + 1,  8,  "\xFB""000");
    DrawTextLine(x + 1,  20, "\xFB""002");
    DrawTextLine(x + 16, 5,  "Tomorrow is Cosmo's");
    DrawTextLine(x + 16, 7,  "birthday, and his");
    DrawTextLine(x + 16, 9,  "parents are taking");
    DrawTextLine(x + 16, 11, "him to the one place");
    DrawTextLine(x + 16, 13, "in the Milky Way");
    DrawTextLine(x + 16, 15, "galaxy that all kids");
    DrawTextLine(x + 16, 17, "would love to go to:");
    DrawTextLine(x + 16, 19, "   Disney World!");
    FadeIn();
    WaitSpinner(x + 35, 22);

    FadeOut();
    ClearScreen();

    x = UnfoldTextFrame(1, 23, 38, "STORY", "Press ANY key.");
    DrawTextLine(x + 3,  12, "\xFB""003");
    DrawTextLine(x + 25, 12, "\xFB""004");
    DrawTextLine(x + 3,  5,  "Suddenly a blazing comet zooms");
    DrawTextLine(x + 4,  7,  "toward their ship--leaving no");
    DrawTextLine(x + 16, 10, "time");
    DrawTextLine(x + 17, 12, "to");
    DrawTextLine(x + 10, 15, "change course...");
    FadeIn();
    WaitSpinner(x + 35, 22);

    FadeOut();
    ClearScreen();

    x = UnfoldTextFrame(1, 23, 38, "STORY", "Press ANY key.");
    DrawTextLine(x + 2,  7,  "\xFB""005");
    DrawTextLine(x + 25, 20, "\xFB""006");
    DrawTextLine(x + 15, 7,  "The comet slams into");
    DrawTextLine(x + 1,  10, "the ship and forces Cosmo's");
    DrawTextLine(x + 1,  13, "dad to make an");
    DrawTextLine(x + 1,  15, "emergency landing");
    DrawTextLine(x + 1,  17, "on an uncharted");
    DrawTextLine(x + 1,  19, "planet.");
    FadeIn();
    WaitSpinner(x + 35, 22);

    FadeOut();
    ClearScreen();

    x = UnfoldTextFrame(1, 23, 38, "STORY", "Press ANY key.");
    DrawTextLine(x + 17, 9,  "\xFB""007");
    DrawTextLine(x + 1,  20, "\xFB""008");
    DrawTextLine(x + 2,  5,  "While Cosmo's");
    DrawTextLine(x + 2,  7,  "dad repairs");
    DrawTextLine(x + 2,  9,  "the ship,");
    DrawTextLine(x + 11, 15, "Cosmo heads off to");
    DrawTextLine(x + 11, 17, "explore and have");
    DrawTextLine(x + 11, 19, "some fun.");
    FadeIn();
    WaitSpinner(x + 35, 22);

    FadeOut();
    ClearScreen();

    x = UnfoldTextFrame(1, 23, 38, "STORY", "Press ANY key.");
    DrawTextLine(x + 3,  15, "\xFB""009");
    DrawTextLine(x + 6,  7,  "Returning an hour later,");
    DrawTextLine(x + 17, 11, "Cosmo cannot find");
    DrawTextLine(x + 17, 13, "his Mom or Dad.");
    DrawTextLine(x + 17, 15, "Instead, he finds");
    DrawTextLine(x + 8,  18, "strange foot prints...");
    FadeIn();
    WaitSpinner(x + 35, 22);

    FadeOut();
    ClearScreen();

    x = UnfoldTextFrame(1, 23, 38, "STORY", "Press ANY key.");
    DrawTextLine(x + 21, 19, "\xFB""010");
    DrawTextLine(x + 2,  5,  "...oh no!  Has his");
    DrawTextLine(x + 2,  7,  "family been taken");
    DrawTextLine(x + 2,  9,  "away by a hungry");
    DrawTextLine(x + 2,  11, "alien creature to");
    DrawTextLine(x + 2,  13, "be eaten?  Cosmo");
    DrawTextLine(x + 2,  15, "must rescue his");
    DrawTextLine(x + 2,  17, "parents before");
    DrawTextLine(x + 2,  19, "it's too late...!");
    FadeIn();
    WaitSpinner(x + 35, 22);
}
```

Before each page is shown, {{< lookup/cref FadeOut >}} is called to blank the screen so the actual drawing happens out of the user's view. The screen is cleared with {{< lookup/cref ClearScreen >}} before each dialog is drawn, and {{< lookup/cref FadeIn >}} fades the fresh content into view once it has been drawn, but right before {{< lookup/cref WaitSpinner >}} blocks waiting for a keypress.

These dialogs make extensive use of the `\xFB` commands in {{< lookup/cref DrawTextLine >}} to drawn [cartoon images]({{< relref "databases/cartoon-sprite" >}}).

{{< boilerplate/function-cref ShowInstructions >}}

The {{< lookup/cref ShowInstructions >}} function shows a progression of five pages of dialog frames that teach the user how to play the game. The pages may be advanced in either a forward direction (by pressing pretty much any key) or reverse direction by pressing either <kbd>&uarr;</kbd> or <kbd>Page Up</kbd>. The <kbd>Esc</kbd> key exits the instructions entirely. Once the fifth page has been dismissed, the {{< lookup/cref ShowHintsAndKeys >}} function displays additional information.

{{< image src="instructions-2052x.png"
    alt="Instructions Dialog Sequence"
    1x="instructions-684x.png"
    2x="instructions-1368x.png"
    3x="instructions-2052x.png" >}}

```c
void ShowInstructions(void)
{
    word x;
    byte scancode;

    FadeOut();
    ClearScreen();

page1:
    FadeOutCustom(1);

    x = UnfoldTextFrame(0, 24, 38, "Instructions  Page One of Five",
        "Press PgDn for next.  ESC to Exit.");
    DrawTextLine(x, 4,  " OBJECT OF GAME:");
    DrawTextLine(x, 6,  " On a strange and dangerous planet,");
    DrawTextLine(x, 8,  " Cosmo must find and rescue his");
    DrawTextLine(x, 10, " parents.");
    DrawTextLine(x, 13, " Cosmo, having seen big scary alien");
    DrawTextLine(x, 15, " footprints, believes his parents");
    DrawTextLine(x, 17, " have been captured and taken away");
    DrawTextLine(x, 19, " to be eaten!");
    FadeInCustom(1);
```

The prologue of this function is similar to other dialogs in the game -- {{< lookup/cref FadeOut >}} fades the existing content off the screen, {{< lookup/cref ClearScreen >}} clears all the contents of the draw page in video memory, and the regular dialog drawing functions render new content in its place.

The instruction dialogs are a little unique because they use {{< lookup/cref FadeInCustom >}} and {{< lookup/cref FadeOutCustom >}} to achieve a quicker fade by using a delay of 1. The first call to {{< lookup/cref FadeOutCustom >}} is superfluous -- the screen is already faded out -- but it becomes necessary in cases where the user backtracks from page two back to the `page1` label.

```c
    do {
        scancode = WaitSpinner(x + 35, 22);
    } while (scancode == SCANCODE_KP_9 || scancode == SCANCODE_KP_8);
    if (scancode == SCANCODE_ESC) return;
```

The {{< lookup/cref WaitSpinner >}} call here is nested inside a `do...while` loop that repeats if the `scancode` entered by the user matches either {{< lookup/cref name="SCANCODE" text="SCANCODE_KP_9" >}} or {{< lookup/cref name="SCANCODE" text="SCANCODE_KP_8" >}}, which are <kbd>Num 9</kbd>/<kbd>Page Up</kbd> and <kbd>Num 8</kbd>/<kbd>&uarr;</kbd> respectively. This absorbs any "previous page" keypresses, causing them to do nothing -- the user is already on the first page.

If `scancode` matches {{< lookup/cref name="SCANCODE" text="SCANCODE_ESC" >}}, the user pressed the `Esc` key and the function returns to its caller without presenting any more information.

In the fallthrough case, the user hit some other key, and it doesn't really matter which key it was. Execution continues with the display code for page two.

```c
page2:
    FadeOutCustom(1);

    x = UnfoldTextFrame(0, 24, 38, "Instructions  Page Two of Five",
        "Press PgUp or PgDn.  Esc to Exit.");
    DrawTextLine(x, 4,  " Cosmo has a very special ability:");
    DrawTextLine(x, 6,  " He can use his suction hands to");
    DrawTextLine(x, 8,  " climb up walls.");
    DrawTextLine(x, 11, " Warning:  Some surfaces, such as");
    DrawTextLine(x, 13, " ice, might be too slippery for");
    DrawTextLine(x, 15, " Cosmo to cling on firmly.");
    DrawTextLine(x, 20,
        "\xFD""011                                 \xFD""034");
    FadeInCustom(1);

    scancode = WaitSpinner(x + 35, 22);
    if (scancode == SCANCODE_ESC) return;
    if (scancode == SCANCODE_KP_8 || scancode == SCANCODE_KP_9) goto page1;
```

This is substantially the same as page one. The key difference is that here {{< lookup/cref name="SCANCODE" text="SCANCODE_KP_9" >}} and {{< lookup/cref name="SCANCODE" text="SCANCODE_KP_8" >}} can do something, by jumping back to the `page1` label.

Otherwise, the progression continues.

```c
page3:
    FadeOutCustom(1);

    x = UnfoldTextFrame(0, 24, 38, "Instructions  Page Three of Five",
        "Press PgUp or PgDn.  Esc to Exit.");
    DrawTextLine(x,     4,  " Cosmo can jump onto attacking");
    DrawTextLine(x,     6,  " creatures without being harmed.");
    DrawTextLine(x,     8,  " This is also Cosmo's way of");
    DrawTextLine(x,     10, " defending himself.");
    DrawTextLine(x,     13, " Cosmo can also find and use bombs.");
    DrawTextLine(x + 5, 18, "   \xFD""036");
    DrawTextLine(x + 5, 20, "         \xFD""024          \xFD""037");
    DrawTextLine(x + 5, 20,
        "   \xFE""118000         \xFE""057000         \xFE""024000");
    FadeInCustom(1);

    scancode = WaitSpinner(x + 35, 22);
    if (scancode == SCANCODE_ESC) return;
    if (scancode == SCANCODE_KP_8 || scancode == SCANCODE_KP_9) goto page2;

page4:
    FadeOutCustom(1);

    x = UnfoldTextFrame(0, 24, 38, "Instructions  Page Four of Five",
        "Press PgUp or PgDn.  Esc to Exit.");
    DrawTextLine(x,     5,  " Use the up and down arrow keys to");
    DrawTextLine(x,     7,  " make Cosmo look up and down,");
    DrawTextLine(x,     9,  " enabling him to see areas that");
    DrawTextLine(x,     11, " might be off the screen.");
    DrawTextLine(x + 4, 18, "   \xFD""028                  \xFD""029");
    DrawTextLine(x,     19, "      Up Key           Down Key");
    FadeInCustom(1);

    scancode = WaitSpinner(x + 35, 22);
    if (scancode == SCANCODE_ESC) return;
    if (scancode == SCANCODE_KP_8 || scancode == SCANCODE_KP_9) goto page3;

    FadeOutCustom(1);

    x = UnfoldTextFrame(0, 24, 38, "Instructions  Page Five of Five",
        "Press PgUp.  Esc to Exit.");
    DrawTextLine(x, 5,  " In Cosmo's Cosmic Adventure, it's");
    DrawTextLine(x, 7,  " up to you to discover the use of");
    DrawTextLine(x, 9,  " all the neat and strange objects");
    DrawTextLine(x, 11, " you'll encounter on your journey.");
    DrawTextLine(x, 13, " Secret Hint Globes will help");
    DrawTextLine(x, 15, " you along the way.");
    DrawTextLine(x, 18, "                 \xFE""125000");
    DrawTextLine(x, 20, "              \xFD""027   \xFE""125002");
    FadeInCustom(1);

    scancode = WaitSpinner(x + 35, 22);
    if (scancode == SCANCODE_ESC) return;
    if (scancode == SCANCODE_KP_8 || scancode == SCANCODE_KP_9) goto page4;
```

Pages three through five are more of the same.

```c
    ClearScreen();

    ShowHintsAndKeys(3);
}
```

After page five is dismissed, {{< lookup/cref ClearScreen >}} abruptly erases the screen content and {{< lookup/cref ShowHintsAndKeys >}} is called to present the additional hints as well as the current keyboard configuration. The `3` argument influences the vertical position of the hints dialog -- since this sequence of dialogs is only reachable through the main menu, there is no need to ensure that the hints dialog clears the status bar and the dialog can be presented a bit lower than during gameplay.

{{< boilerplate/function-cref ShowHintsAndKeys >}}

The {{< lookup/cref ShowHintsAndKeys >}} function displays a page of helpful hints, followed by two pages of keyboard help. The `top` parameter influences the vertical position of the frames, to allow the dialogs to be placed higher on the screen while the game is being played.

{{< boilerplate/menu-gameplay object="dialog" may=true >}}

{{< image src="hints-and-keys-2052x.png"
    alt="Hints and Keys Dialog Sequence"
    1x="hints-and-keys-684x.png"
    2x="hints-and-keys-1368x.png"
    3x="hints-and-keys-2052x.png" >}}

```c
void ShowHintsAndKeys(word top)
{
    word x;
    word y = top - 1;
```

The calculations involving `y` are strange. When this function is called via the in-game {{< lookup/cref ShowHelpMenu >}} function, `top` is 1 so `y` is 0. This suggests that the content was originally designed to display fixed at that position, and it was a late modification to make the frames movable. Rather than recompute everything to be relative to `top`, it was probably easier to position everything relative to a `y` that was known to already work correctly.

```c
    x = UnfoldTextFrame(top, 18, 38, "Cosmic Hints", "Press ANY key.");
    DrawTextLine(x, y + 4,  " * Usually jumping in the paths of");
    DrawTextLine(x, y + 5,  "   bonus objects will lead you in");
    DrawTextLine(x, y + 6,  "   the right direction.");
    DrawTextLine(x, y + 8,  " * There are many secret bonuses in");
    DrawTextLine(x, y + 9,  "   this game, such as bombing 15 of");
    DrawTextLine(x, y + 10, "   the Eye Plants.  (Registered");
    DrawTextLine(x, y + 11, "   players will get the full list.)");
    DrawTextLine(x, y + 13, " * When clinging to a wall, tap the");
    DrawTextLine(x, y + 14, "   jump key to let go and fall.  To");
    DrawTextLine(x, y + 15, "   re-cling to the wall, push");
    DrawTextLine(x, y + 16, "   yourself into the wall again.");
    WaitSpinner(x + 35, y + 17);

    x = UnfoldTextFrame(top, 18, 38, "Key Definition Screen", "");
    DrawTextLine(x,      y + 4,  "                     Look");
    DrawTextLine(x,      y + 5,  "                      UP");
    DrawTextLine(x,      y + 7,  "              Walk            Walk");
    DrawTextLine(x,      y + 8,  "  Jump  Drop  LEFT            RIGHT");
    DrawTextLine(x,      y + 9,  "   UP   BOMB");
    DrawTextLine(x,      y + 10, "                     \xFD""028");
    DrawTextLine(x,      y + 11, "                     Look");
    DrawTextLine(x,      y + 12, "                     DOWN");
    DrawTextLine(x,      y + 13,
        "              \xFD""001                 \xFD""023");
    DrawTextLine(x,      y + 14,
        "  \xFD""030      \xFD""037   \xFE""024000");
    DrawTextLine(x,      y + 17, "                     \xFD""029");
    DrawTextLine(x + 24, y + 7,  keyNames[scancodeNorth]);
    DrawTextLine(x + 24, y + 14, keyNames[scancodeSouth]);
    DrawTextLine(x + 14, y + 14, keyNames[scancodeWest]);
    DrawTextLine(x + 30, y + 14, keyNames[scancodeEast]);
    DrawTextLine(x + 2,  y + 15, keyNames[scancodeJump]);
    DrawTextLine(x + 8,  y + 15, keyNames[scancodeBomb]);
    WaitSpinner(x + 35, y + 17);
```

The second page dynamically presents the current key bindings in the dialog text. It accomplishes this by translating the scancodes held in {{< lookup/cref scancodeNorth >}}, {{< lookup/cref scancodeSouth >}}, {{< lookup/cref scancodeWest >}}, {{< lookup/cref scancodeEast >}}, {{< lookup/cref scancodeJump >}}, and {{< lookup/cref scancodeBomb >}} to regular C strings via the {{< lookup/cref keyNames >}} lookup table.

Multiple `\xFD` commands are used to draw [player sprites]({{< relref "databases/player-sprite" >}}) onto the frame, and a single `\xFE` command draws the bomb's [actor sprite]({{< relref "databases/actor-sprite" >}}).

```c
    x = UnfoldTextFrame(4, 11, 34, "During the game, you can...",
        "Press ANY key.");
    DrawTextLine(x, 7,  " Press 'P' to PAUSE GAME");
    DrawTextLine(x, 8,  " Press 'ESC' or 'Q' to QUIT game");
    DrawTextLine(x, 9,  " Press 'S' to toggle SOUND");
    DrawTextLine(x, 10, " Press 'M' to toggle MUSIC");
    DrawTextLine(x, 11, " Press 'F1' to show HELP");
    WaitSpinner(x + 31, 13);
}
```

The final page is a static (and comprehensive) list of the keys that can be pressed during gameplay. The only keys not mentioned are the debug and cheat key combinations.

{{< boilerplate/function-cref ShowOrderingInformation >}}

The {{< lookup/cref ShowOrderingInformation >}} function displays five sequential pages of ordering information in the shareware episode of the game, or a single page thanking the user for purchasing one of the registered episodes in other cases. The pages can only be viewed in the forward direction, and cannot be exited early.

{{< image src="ordering-information-2052x.png"
    alt="Ordering Information Dialog Sequence"
    1x="ordering-information-684x.png"
    2x="ordering-information-1368x.png"
    3x="ordering-information-2052x.png" >}}

```c
void ShowOrderingInformation(void)
{
    word x;

    FadeOut();
    ClearScreen();

#ifdef SHAREWARE
    x = UnfoldTextFrame(0, 24, 38, "Ordering Information", "Press ANY key.");
    DrawTextLine(x, 2,
        "  \xFE""223000                              \xFE""223000");
    DrawTextLine(x, 4,  "      COSMO'S COSMIC ADVENTURE");
    DrawTextLine(x, 5,  "    consists of three adventures.");
    DrawTextLine(x, 7,  "    Only the first adventure is");
    DrawTextLine(x, 8,  " available as shareware.  The final");
    DrawTextLine(x, 9,  "   two amazing adventures must be");
    DrawTextLine(x, 10, "    purchased from Apogee, or an");
    DrawTextLine(x, 11, "          authorized dealer.");
    DrawTextLine(x, 13, "  The last two adventures of Cosmo");
    DrawTextLine(x, 14, "   feature exciting new graphics,");
    DrawTextLine(x, 15, "  new creatures, new puzzles, new");
    DrawTextLine(x, 16, "   music and all-new challenges!");
    DrawTextLine(x, 18, "    The next few screens provide");
    DrawTextLine(x, 19, "       ordering instructions.");
    DrawTextLine(x, 22,
        "  \xFE""155000                              \xFE""154001");
    FadeInCustom(1);
    WaitSpinner(x + 35, 22);

    FadeOutCustom(1);
    ClearScreen();

    x = UnfoldTextFrame(1, 22, 38, "Ordering Information", "Press ANY key.");
    DrawTextLine(x, 4,  "       Order now and receive:");
    DrawTextLine(x, 6,  "   * All three exciting adventures");
    DrawTextLine(x, 7,  "   * The hints and tricks sheet");
    DrawTextLine(x, 8,  "   * The Secret Cheat password");
    DrawTextLine(x, 9,  "   * Exciting new bonus games");
    DrawTextLine(x, 11, "      To order, call toll free:");
    DrawTextLine(x, 12, "           1-800-426-3123");
    DrawTextLine(x, 13, "   (Visa and MasterCard Welcome)");
    DrawTextLine(x, 15, "   Order all three adventures for");
    DrawTextLine(x, 16, "     only $35, plus $4 shipping.");
    DrawTextLine(x, 19, "              \xFE""129002");
    DrawTextLine(x, 20, "  \xFB""014                          \xFB""015");
    FadeInCustom(1);
    WaitSpinner(x + 35, 21);

    FadeOutCustom(1);
    ClearScreen();

    x = UnfoldTextFrame(1, 22, 38, "Ordering Information", "Press ANY key.");
    DrawTextLine(x, 4,  "      Please specify disk size:");
    DrawTextLine(x, 5,  "           5.25\"  or  3.5\"");
    DrawTextLine(x, 7,  "     To order send $35, plus $4");
    DrawTextLine(x, 8,  "      shipping, USA funds, to:");
    DrawTextLine(x, 10, "           Apogee Software");
    DrawTextLine(x, 11, "           P.O. Box 476389");
    DrawTextLine(x, 12, "       Garland, TX 75047  (USA)");
    DrawTextLine(x, 14,
        "\xFE""101003       Or CALL NOW toll free:  \xFE""101000");
    DrawTextLine(x, 15, "           1-800-426-3123");
    DrawTextLine(x, 18, "         ORDER COSMO TODAY!");
    DrawTextLine(x, 19, "           All 3 for $39!");
    DrawTextLine(x, 20, "  \xFB""014                          \xFB""015");
    FadeInCustom(1);
    WaitSpinner(x + 35, 21);

    FadeOutCustom(1);
    ClearScreen();

    x = UnfoldTextFrame(4, 15, 38, "USE YOUR FAX MACHINE TO ORDER!",
        "Press ANY key.");
    DrawTextLine(x, 7,  "  You can now use your FAX machine");
    DrawTextLine(x, 8,  "   to order your favorite Apogee");
    DrawTextLine(x, 9,  "     games quickly and easily.");
    DrawTextLine(x, 11, "   Simply print out the ORDER.FRM");
    DrawTextLine(x, 12, "    file, fill it out and FAX it");
    DrawTextLine(x, 13, "    to us for prompt processing.");
    DrawTextLine(x, 15, "     FAX Orders: (214) 278-4670");
    FadeInCustom(1);
    WaitSpinner(x + 35, 17);

    FadeOutCustom(1);
    ClearScreen();

    x = UnfoldTextFrame(1, 20, 38, "About Apogee Software",
        "Press ANY key.") + 2;
    DrawTextLine(x, 4,  "Our goal is to establish Apogee");
    DrawTextLine(x, 5,  "  as the leader in commercial");
    DrawTextLine(x, 6,  " quality shareware games. With");
    DrawTextLine(x, 7,  " enthusiasm and dedication we");
    DrawTextLine(x, 8,  "think our goal can be achieved.");
    DrawTextLine(x, 10, "However,  we need your support.");
    DrawTextLine(x, 11, "Shareware is not free software.");
    DrawTextLine(x, 13, "  We thank you in advance for");
    DrawTextLine(x, 14, "   your contribution to the");
    DrawTextLine(x, 15, "  growing shareware community.");
    DrawTextLine(x - 2, 17,
        "\xFD""010        Your honesty pays...     \xFD""033");
    FadeInCustom(1);
    WaitSpinner(x + 33, 19);
#else
    x = UnfoldTextFrame(0, 24, 38, "Ordering Information", "Press ANY key.");
    DrawTextLine(x,  4, "      COSMO'S COSMIC ADVENTURE");
    DrawTextLine(x,  6, "  This game IS commercial software.");
    DrawTextLine(x,  8, "    This episode of Cosmo is NOT");
    DrawTextLine(x,  9, " available as shareware.  It is not");
    DrawTextLine(x, 10, "  freeware, nor public domain.  It");
    DrawTextLine(x, 11, "  is only available from Apogee or");
    DrawTextLine(x, 12, "        authorized dealers.");
    DrawTextLine(x, 14, " If you are a registered player, we");
    DrawTextLine(x, 15, "    thank you for your patronage.");
    DrawTextLine(x, 17, "  Please report any illegal selling");
    DrawTextLine(x, 18, "  and distribution of this game to");
    DrawTextLine(x, 19, "  Apogee by calling 1-800-GAME123.");
    FadeInCustom(1);
    WaitSpinner(x + 35, 22);
#endif
}
```

The presence or absence of the `SHAREWARE` macro determines which dialog or sequence of dialogs is compiled into the game executable.

This is a standard multi-page dialog sequence, with the only customization being the use of {{< lookup/cref FadeInCustom >}} and {{< lookup/cref FadeOutCustom >}} to produce a quick fade with a one-tick delay between each palette change.

{{< boilerplate/function-cref ShowForeignOrders >}}

The {{< lookup/cref ShowForeignOrders >}} function displays five consecutive pages of ordering information for international customers. The pages can only be viewed in the forward direction, and cannot be exited early.

{{< image src="foreign-orders-2052x.png"
    alt="Foreign Orders Dialog Sequence"
    1x="foreign-orders-684x.png"
    2x="foreign-orders-1368x.png"
    3x="foreign-orders-2052x.png" >}}

This function is only present in the shareware episode of the game, and its inclusion in the executable is controlled by the presence or absence of the `FOREIGN_ORDERS` macro.

```c
#ifdef FOREIGN_ORDERS
void ShowForeignOrders(void)
{
    word x;

    FadeOut();
    ClearScreen();

    x = UnfoldTextFrame(1, 19, 38, "FOREIGN CUSTOMERS",
        "Press ANY key.") + 2;
    DrawTextLine(x, 3,  "        -----------------");
    DrawTextLine(x, 5,  " The following screens list our");
    DrawTextLine(x, 6,  "   dealers outside the United");
    DrawTextLine(x, 7,  " States, for Australia, Germany,");
    DrawTextLine(x, 8,  " Canada and the United Kingdom.");
    DrawTextLine(x, 10, "   These are official Apogee");
    DrawTextLine(x, 11, "    dealers with the latest");
    DrawTextLine(x, 12,
        "\xFE""153000       games and updates.    \xFE""153001");
    DrawTextLine(x, 14, " If your country is not listed,");
    DrawTextLine(x, 15, "  you may order directly from");
    DrawTextLine(x, 16, "Apogee by phone: (214) 278-5655.");
    FadeInCustom(1);
    WaitSpinner(x + 33, 18);

    FadeOutCustom(1);
    ClearScreen();

    x = UnfoldTextFrame(1, 19, 38, "AUSTRALIAN CUSTOMERS",
        "Press ANY key.") + 3;
    DrawTextLine(x, 4,  "PRICE: $45 + $5 shipping.");
    DrawTextLine(x, 6,  "BudgetWare");
    DrawTextLine(x, 7,  "P.O. Box 496");
    DrawTextLine(x, 8,  "Newtown, NSW  2042        \xFE""113000");
    DrawTextLine(x, 10, "Phone:      (02) 519-4233");
    DrawTextLine(x, 11, "Toll free:  (008) 022-064");
    DrawTextLine(x, 12, "Fax:        (02) 516-4236");
    DrawTextLine(x, 13, "CompuServe: 71520,1475");
    DrawTextLine(x, 15, "Use MasterCard, Visa, Bankcard,");
    DrawTextLine(x, 16, "cheques.");
    FadeInCustom(1);
    WaitSpinner(x + 32, 18);

    FadeOutCustom(1);
    ClearScreen();

    x = UnfoldTextFrame(1, 20, 38, "CANADIAN CUSTOMERS",
        "Press ANY key.") + 3;
    DrawTextLine(x, 4,  "PRICE: $42 Canadian.       \xFE""146000");
    DrawTextLine(x, 6,  "Distant Markets");
    DrawTextLine(x, 7,  "Box 1149");
    DrawTextLine(x, 8,  "194 - 3803 Calgary Trail S.");
    DrawTextLine(x, 9,  "Edmondton, Alb.  T6J 5M8");
    DrawTextLine(x, 10, "CANADA");
    DrawTextLine(x, 12, "Orders:    1-800-661-7383");
    DrawTextLine(x, 13, "Inquiries: (403) 436-3009");
    DrawTextLine(x, 14, "Fax:       (403) 435-0928  \xFE""086002");
    DrawTextLine(x, 16, "Use MasterCard, Visa or");
    DrawTextLine(x, 17, "money orders.");
    FadeInCustom(1);
    WaitSpinner(x + 32, 19);

    FadeOutCustom(1);
    ClearScreen();

    x = UnfoldTextFrame(1, 20, 38, "GERMAN CUSTOMERS", "Press ANY key.") + 3;
    DrawTextLine(x, 4,  "Price: 49,-- DM plus 10,-- DM");
    DrawTextLine(x, 5,  "Total: 59,-- DM (Deutsche Mark)");
    DrawTextLine(x, 7,  "CDV-Software");
    DrawTextLine(x, 8,  "Ettlingerstr. 5");
    DrawTextLine(x, 9,  "7500 Karlsruhe 1  GERMANY");
    DrawTextLine(x, 11, "Phone: 0721-22295");
    DrawTextLine(x, 12, "Fax:   0721-21314            \xFE""127004");
    DrawTextLine(x, 13, "Compuserve: 1000022,274");
    DrawTextLine(x, 15, "Use Visa, MasterCard, EuroCard,");
    DrawTextLine(x, 16, "American Express, cheque, money");
    DrawTextLine(x, 17, "order, or C.O.D.");
    FadeInCustom(1);
    WaitSpinner(x + 32, 19);

    FadeOutCustom(1);
    ClearScreen();

    x = UnfoldTextFrame(1, 20, 38, "UNITED KINGDOM CUSTOMERS",
        "Press ANY key.") + 3;
    DrawTextLine(x, 4,  "Price: /29 + VAT + 2 P&P     \xFE""085000");
```

{{< note >}}The [game font]({{< relref "databases/font" >}}) does not contain a `/` character, and instead displays the symbol for the pound sterling (<code>&pound;</code>) in its place.{{< /note >}}

```c
    DrawTextLine(x, 6,  "Precision Software Applications");
    DrawTextLine(x, 7,  "Unit 3, Valley Court Offices");
    DrawTextLine(x, 8,  "Lower Rd");
    DrawTextLine(x, 9,  "Croydon, Near Royston");
    DrawTextLine(x, 10, "Herts. SG8 0HF, United Kingdom");
    DrawTextLine(x, 12, "Phone: +44 (0) 223 208 288");
    DrawTextLine(x, 13, "FAX:   +44 (0) 223 208 089");
    DrawTextLine(x, 15, "Credit cards, Access, cheques,");
    DrawTextLine(x, 16, "postal & Bankers orders.");
    DrawTextLine(x, 17, "Make cheques payable to PSA.");
    FadeInCustom(1);
    WaitSpinner(x + 32, 19);
}
#endif
```

{{< boilerplate/function-cref ShowPublisherBBS >}}

The {{< lookup/cref ShowPublisherBBS >}} function displays two consecutive pages of information on how to access Apogee's official channels on popular bulletin board systems (**BBS**es) of the day.

{{< image src="publisher-bbs-2052x.png"
    alt="Publisher BBS Dialog Sequence"
    1x="publisher-bbs-684x.png"
    2x="publisher-bbs-1368x.png"
    3x="publisher-bbs-2052x.png" >}}

A BBS was a predecessor to the World Wide Web as we know it today. It consisted of a centralized server connected to the telephone network via a bank of modems. Individuals could instruct their modem-equipped PCs to dial the BBS phone number, giving them access to a shared area to send, receive, and store messages and files. This, along with regular postal mail, was the main distribution channel for shareware in the early 1990s.

2400 and 9600 baud modems could transfer data at speeds of 240 and 960 bytes(!) per second, respectively. A 14.4 kbps modem could do 1,800 bytes per second. This game, appropriately compressed, would be on the order of 400-500,000 bytes. This means that a user retrieving this game through one of the modems described here could spend anywhere from a few minutes to _half an hour_ downloading the shareware episode.

America Online (AOL) was, at the time, similar to BBSes in that it was a relatively isolated universe where the only interactions a user typically had were with others who were also AOL customers. It was geared to people who were not highly technical, but still wanted to explore what an interconnected system of computers was capable of. This stands in contrast to other services (e.g. CompuServe) that catered to more advanced users who were curious about the new frontier of the Internet at large.

```c
void ShowPublisherBBS(void)
{
    word x;

    FadeOut();
    ClearScreen();

    x = UnfoldTextFrame(1, 22, 38, "THE OFFICIAL APOGEE BBS",
        "Press ANY key.") + 3;
    DrawTextLine(x, 3,  "    -----------------------");
    DrawTextLine(x, 5,  "The SOFTWARE CREATIONS BBS is");
    DrawTextLine(x, 6,  " the home BBS for the latest");
    DrawTextLine(x, 7,  " Apogee games.  Check out our");
    DrawTextLine(x, 8,  "FREE 'Apogee' file section for");
    DrawTextLine(x, 9,  "  new releases and updates.");
    DrawTextLine(x, 11, "       BBS phone lines:");
    DrawTextLine(x, 13, "(508) 365-2359  2400 baud");
    DrawTextLine(x, 14, "(508) 365-9825  9600 baud");
    DrawTextLine(x, 15, "(508) 365-9668  14.4k dual HST");
    DrawTextLine(x, 17, "Home of the Apogee BBS Network!");
    DrawTextLine(x, 19, "    A Major Multi-Line BBS.");
    FadeIn();
    WaitSpinner(x + 32, 21);

    FadeOut();
    ClearScreen();

    x = UnfoldTextFrame(0, 25, 40, "APOGEE ON AMERICA ONLINE! ",
        "Press ANY key.");
    DrawTextLine(x, 2,  "      -------------------------");
    DrawTextLine(x, 4,  "   America Online (AOL) is host of");
    DrawTextLine(x, 5,  " the Apogee Forum, where you can get");
    DrawTextLine(x, 6,  "   new Apogee games. Use the Apogee");
    DrawTextLine(x, 7,  "  message areas to talk and exchange");
    DrawTextLine(x, 8,  "   ideas, comments and secrets with");
    DrawTextLine(x, 9,  "   our designers and other players.");
    DrawTextLine(x, 11, "  If you are already a member, after");
    DrawTextLine(x, 12, " you log on, use the keyword \"Apogee\"");
    DrawTextLine(x, 13, " (Ctrl-K) to jump to the Apogee area.");
    DrawTextLine(x, 15, "  If you'd like to know how to join,");
    DrawTextLine(x, 16, "        please call toll free:");
    DrawTextLine(x, 18, "            1-800-827-6364");
    DrawTextLine(x, 19, "    Please ask for extension 5703.");
    DrawTextLine(x, 21, "   You'll get the FREE startup kit.");
    FadeIn();
    WaitSpinner(x + 37, 23);
}
```

{{< boilerplate/function-cref ToggleSound >}}

The {{< lookup/cref ToggleSound >}} function inverts the setting of the global {{< lookup/cref isSoundEnabled >}} variable then presents a dialog confirming the resulting state.

{{< boilerplate/menu-gameplay object="dialog" may=true >}}

{{< image src="sound-2052x.png"
    alt="Sound Dialogs"
    1x="sound-684x.png"
    2x="sound-1368x.png"
    3x="sound-2052x.png" >}}

```c
void ToggleSound(void)
{
    word x;

    isSoundEnabled = !isSoundEnabled;

    if (isSoundEnabled) {
        x = UnfoldTextFrame(2, 4, 24, "Sound Toggle",
            "The sound is now ON!");
    } else {
        x = UnfoldTextFrame(2, 4, 24, "Sound Toggle",
            "The sound is now OFF!");
    }

    WaitSpinner(x + 21, 4);
}
```

Each call to this dialog function changes global state, causing {{< lookup/cref isSoundEnabled >}} to flip-flop between true and false each call. Depending on the resulting value held in {{< lookup/cref isSoundEnabled >}}, one of two different messages is displayed via the top/bottom texts of an {{< lookup/cref UnfoldTextFrame >}} call.

In both cases, the function blocks until {{< lookup/cref WaitSpinner >}} returns, then the dialog function ends.

There is a layout oversight in the "sound is now OFF" case -- the bottom text of the frame is 21 characters long, which does not center evenly in the 22-tile space afforded by the frame. The single centering space ends up at the beginning of the line, placing the exclamation point on the tile that is eventually covered by the wait spinner, leading to loss of that character when the wait spinner is drawn.

{{< boilerplate/function-cref ToggleMusic >}}

The {{< lookup/cref ToggleMusic >}} function inverts the setting of the global {{< lookup/cref isMusicEnabled >}} variable then presents a dialog confirming the resulting state. If the system does not have an AdLib compatible card installed, this function is a no-op.

{{< boilerplate/menu-gameplay object="dialog" may=true >}}

{{< image src="music-2052x.png"
    alt="Music Dialogs"
    1x="music-684x.png"
    2x="music-1368x.png"
    3x="music-2052x.png" >}}

```c
void ToggleMusic(void)
{
    word x;

    if (IsAdLibAbsent()) return;

    isMusicEnabled = !isMusicEnabled;

    if (isMusicEnabled) {
        x = UnfoldTextFrame(2, 4, 24, "Music Toggle",
            "The music is now ON!");

        SwitchMusic(activeMusic);
        StartAdLibPlayback();
    } else {
        x = UnfoldTextFrame(2, 4, 24, "Music Toggle",
            "The music is now OFF!");

        StopAdLibPlayback();
    }

    WaitSpinner(x + 21, 4);
}
```

This function works identically to {{< lookup/cref ToggleSound >}} (and has the same layout bug in the "music is now OFF" dialog) but with the following differences:

* The function begins with a call to {{< lookup/cref IsAdLibAbsent >}} to verify presence of an AdLib music card. If the hardware is not installed, this function returns immediately without performing any action.
* When music is enabled, {{< lookup/cref SwitchMusic >}} is called to start playing the appropriate music (which has already been loaded into the {{< lookup/cref activeMusic >}} structure) from the beginning. This is followed by a superfluous call to {{< lookup/cref StartAdLibPlayback >}} -- that function had already been called during the {{< lookup/cref SwitchMusic >}} call.
* When music is disabled, {{< lookup/cref StopAdLibPlayback >}} is called to immediately silence the music before presenting the wait spinner.

{{< boilerplate/function-cref ShowLevelIntro >}}

The {{< lookup/cref ShowLevelIntro >}} function presents the animated message "Now entering level..." followed by the map number of the passed `level_num`. It is displayed before a regular non-bonus map begins.

{{< image src="level-intro-2052x.png"
    alt="Level Intro Dialog"
    1x="level-intro-684x.png"
    2x="level-intro-1368x.png"
    3x="level-intro-2052x.png" >}}

{{< note >}}It is not safe to call this function with `level_num` higher than 17.{{< /note >}}

The global state of the program differentiates **levels** (each of which is played once in the game's progression) and **maps** (the actual worlds the player moves through, including the bonus maps which can be played multiple times). The text presented to the user is looser with the terminology, here using the word "level" where it's more appropriately referred to as "map."

```c
void ShowLevelIntro(word level_num)
{
    byte mapnums[] = {1, 2, 0, 0, 3, 4, 0, 0, 5, 6, 0, 0, 7, 8, 0, 0, 9, 10};
    word x;
```

The `mapnums[]` array links the level numbers to the maps. Levels 0&ndash;1 are maps 1&ndash;2, levels 2&ndash;3 are the _first_ occurrences of the two bonus maps, and levels 4&ndash;5 are maps 3&ndash;4. This pattern repeats, with the two bonus maps repeated between every two regular maps, until map 10. Since the bonus maps are not introduced by this dialog function, their positions hold a space-filler zero value.

```c
    if (demoState != DEMO_STATE_NONE) return;
```

If the global {{< lookup/cref demoState >}} is anything other than {{< lookup/cref name="DEMO_STATE" text="DEMO_STATE_NONE" >}}, a demo is being recorded or played back and this function should return without doing anything. This doesn't occur in practice, as the caller ({{< lookup/cref InitializeLevel >}}) only calls this function when the demo state is {{< lookup/cref name="DEMO_STATE" text="DEMO_STATE_NONE" >}}.

```c
    x = UnfoldTextFrame(7, 3, 24, "\xFC""003  Now entering level", "");
    WaitHard(20);
    StartSound(SND_ENTERING_LEVEL_NUM);

    if (mapnums[level_num] == 10) {
        DrawNumberFlushRight(x + 21, 8, (dword)mapnums[level_num]);
    } else {
        DrawNumberFlushRight(x + 20, 8, (dword)mapnums[level_num]);
    }
}
```

The remainder of the function is a regular dialog with some extra flourish. {{< lookup/cref UnfoldTextFrame >}} uses the `\xFC` command to animate the "Now entering level" top text with a typewriter sound effect, and {{< lookup/cref WaitHard >}} imposes a 20-tick delay to add some impact to the number that will be drawn.

{{< lookup/cref StartSound >}} queues the higher-pitched sound effect {{< lookup/cref name="SND" text="SND_ENTERING_LEVEL_NUM" >}}, which begins to play as the number appears.

The `if` covers up a bit of a hack: If the value read from `mapnums[]` is equal to `10`, the number being drawn is two digits long and needs to be shifted one tile to the _right_ to display correctly. This is because the number is drawn _right-aligned_ via {{< lookup/cref DrawNumberFlushRight >}}, making everything on the horizontal axis behave opposite to how one would expect it to.

{{< aside class="armchair-engineer" >}}
**Couldn't `mapnums[]` have been an array of fixed-length strings instead, avoiding this issue entirely?**

Shush, you.
{{< /aside >}}

While the first episode of the game has map 11, the caller ({{< lookup/cref InitializeLevel >}}) does not call this function when that map is entered. No other two-digit maps numbers are implemented in the retail game.

{{< boilerplate/function-cref ShowSectionIntermission >}}

The {{< lookup/cref ShowSectionIntermission >}} function is shown to tie different "sections" of the level progression together. Sections are two levels long, followed by a conditional bonus level. Depending on the context (section complete, or bonus level complete) different values may be passed in `top_text` and `bottom_text`. Once the intermission dialog is dismissed, {{< lookup/cref ShowStarBonus >}} is called to tally up additional bonus points.

{{< image src="section-intermission-2052x.png"
    alt="Section Intermission Dialogs"
    1x="section-intermission-684x.png"
    2x="section-intermission-1368x.png"
    3x="section-intermission-2052x.png" >}}

This function is essentially "glue" around the {{< lookup/cref ShowStarBonus >}} dialog feature, which centralizes (to a degree) the screen-clearing and fading behavior.

```c
void ShowSectionIntermission(char *top_text, char *bottom_text)
{
    word x;

    FadeOut();
    SelectDrawPage(0);
    SelectActivePage(0);
    ClearScreen();
```

When this function is entered, the player has just "won" the level they were on and the last frame of gameplay is still visible on the screen. {{< lookup/cref FadeOut >}} fades this view away, and then {{< lookup/cref SelectDrawPage >}} and {{< lookup/cref SelectActivePage >}} are both set to page zero. This disables the double-buffering behavior that gameplay uses, and makes it so that any drawing calls are visible on the screen immediately. {{< lookup/cref ClearScreen >}} discards everything on that draw page.

```c
    x = UnfoldTextFrame(6, 4, 30, top_text, bottom_text);
    FadeIn();
    WaitSpinner(x + 27, 8);
```

{{< lookup/cref UnfoldTextFrame >}} presents the intermission dialog, with whatever `top_text` or `bottom_text` the caller provided. {{< lookup/cref FadeIn >}} fades it into view, then {{< lookup/cref WaitSpinner >}} blocks until a key is pressed.

```c
    ShowStarBonus();
```

{{< lookup/cref ShowStarBonus >}} is another dialog that counts up the stars that the player collected during the previous section (if any) and gives points in response. When it returns, the star bonus dialog is still visible on the screen.

```c
    FadeOut();
    ClearScreen();
}
```

The {{< lookup/cref FadeOut >}} and {{< lookup/cref ClearScreen >}} pair fade the star bonus away and clean up the screen buffer. The function returns with the screen in this state.

{{< boilerplate/function-cref ShowStarBonus >}}

The {{< lookup/cref ShowStarBonus >}} function presents a dialog that tallies up the number of stars collected by the player during the previous section. Each star adds 1,000 additional points to the player's score, and higher star counts display an increasingly higher ranking text at the bottom of the frame. As a side effect, this function zeroes {{< lookup/cref gameStars >}} and increases {{< lookup/cref gameScore >}} accordingly.

{{< image src="star-bonus-2052x.png"
    alt="Star Bonus Dialog"
    1x="star-bonus-684x.png"
    2x="star-bonus-1368x.png"
    3x="star-bonus-2052x.png" >}}

If the player did not collect any stars in the preceding section, the dialog does not display.

When first displayed, the dialog shows the current number of stars collected and the current player score. After a brief delay, the star count decrements by one and the score increments by 1,000. Each time this occurs, a sound effect plays. Once the star count decrements to zero, this dialog dismisses itself after a delay. Keyboard input is not considered here, and there is no way to speed through the sequence or exit early.

As the stars are tallied, a progression of ten (could have been thirteen; see the below bug) "ranks" are shown at the bottom of the frame. Every eight stars, the rank increases from "Not Bad!" all the way up to "Rocket Scientist." These ranks are purely for show; they have no special effects beyond giving the user something to read while waiting for the count to complete.

```c
void ShowStarBonus(void)
{
    register word stars;
    word i = 0;
```

This function uses two local variables. `stars` decrements during the sequence, reaching zero once all stars have been counted. `i` _starts_ at zero, and increments with each star to influence the rank shown.

```c
    StopMusic();

    if (gameStars == 0) {
        FadeOut();
        return;
    }
```

Typically this dialog will begin while music from the previous level (or the ending story) is playing. {{< lookup/cref StopMusic >}} stops this playback, ensuring the star count occurs in silence.

If the player collected no stars during the most recent section of gameplay, {{< lookup/cref gameStars >}} will be zero and the `if` body is taken. {{< lookup/cref FadeOut >}} fades the screen out. (Strictly speaking, this fade is not necessary since every caller of this function calls {{< lookup/cref FadeOut >}} itself before continuing.) With the screen faded, the function returns without doing anything else.

```c
    FadeWhiteCustom(3);
    SelectDrawPage(0);
    SelectActivePage(0);
    ClearScreen();
```

If the player has collected at least one star, this dialog qualifies for display. {{< lookup/cref FadeWhiteCustom >}} fades the screen out, but by using white as the color instead of black. In this state, changes to the video memory have no visible effect to the user.

{{< lookup/cref SelectDrawPage >}} and {{< lookup/cref SelectActivePage >}} are both set to page zero. This disables the double-buffering behavior that gameplay uses, and makes it so that any drawing calls are visible on the screen immediately. {{< lookup/cref ClearScreen >}} discards everything on that draw page.

```c
    UnfoldTextFrame(2, 14, 30, "Super Star Bonus!!!!", "");
    DrawSprite(SPR_STAR, 2, 8, 8, DRAW_MODE_ABSOLUTE);
    DrawTextLine(14, 7, "X 1000 =");
    DrawNumberFlushRight(27, 7, gameStars * 1000);
    WaitHard(50);
    DrawTextLine(10, 12, "YOUR SCORE =  ");
    DrawNumberFlushRight(29, 12, gameScore);
```

Here the dialog is constructed. It consists of an outer frame, a star sprite, and a pair of static "X 1000 =" multiplier and "YOUR SCORE =" result labels. The initial state of the dialog shows the number of stars collected ({{< lookup/cref gameStars >}}) multiplied by 1,000 and the current score held in {{< lookup/cref gameScore >}}.

There is a {{< lookup/cref WaitHard >}} delay buried inside this, which suggests that at one point there was a different pattern to the animation than what was used in the final game. As written, the 50-tick delay simply extends the length of time the sequence pauses in its faded-out-to-white state.

```c
    FadeIn();
    WaitHard(100);
```

With the initial state of the dialog fully drawn, {{< lookup/cref FadeIn >}} fades it into view by restoring the EGA palette to its default state. {{< lookup/cref WaitHard >}} pauses again before counting starts.

```c
    for (stars = (word)gameStars; stars > 0; stars--) {
        register word x;

        gameScore += 1000;

        WaitHard(15);
```

This `for` loop begins by setting `stars` to the value held in {{< lookup/cref gameStars >}}. The value in `stars` decrements by one after each iteration, until it reaches zero. The total number of iterations here equals the number of stars the player collected.

On each iteration, the player's score in {{< lookup/cref gameScore >}} is incremented by 1,000 points and {{< lookup/cref WaitHard >}} pauses for 15 ticks to prevent the loop from moving too fast.

```c
        for (x = 0; x < 7; x++) {
            DrawSpriteTile(fontTileData + FONT_BACKGROUND_GRAY, 23 + x, 12);
        }

        StartSound(SND_BIG_PRIZE);
        DrawNumberFlushRight(29, 12, gameScore);
```

Every iteration, the area occupied by the score is erased by drawing a span of seven solid gray tiles via {{< lookup/cref DrawSpriteTile >}}. This is not actually necessary -- the digits in the font tiles have fully opaque backgrounds that are already the appropriate gray color.

{{< lookup/cref StartSound >}} queues the {{< lookup/cref name="SND" text="SND_BIG_PRIZE" >}} sound effect, and {{< lookup/cref DrawNumberFlushRight >}} redraws the updated {{< lookup/cref gameScore >}} value onto the dialog.

```c
        if (i / 6 < 13) i++;
```

The `i` variable is used to determine which rank text should be shown at this time. The array of ranks has thirteen elements numbered 0&ndash;12, and the intention here is to use `i / 6` as the index into this array, thus advancing the displayed rank on every sixth iteration.

As written, `i` stops incrementing once it reaches 78. `78 / 6` is 13, which is past the end of the ranks array, but this does not cause issues due to another condition that happens a bit later.

```c
        for (x = 0; x < 16; x++) {
            if (x < 7) {
                DrawSpriteTile(fontTileData + FONT_BACKGROUND_GRAY,
                    22 + x, 7);
            }

            if (i % 8 == 1) {
                DrawSpriteTile(fontTileData + FONT_BACKGROUND_GRAY,
                    13 + x, 14);
            }
        }
```

Here, two separate content areas are erased using a single `for` loop. The seven-digit "stars times 1,000" area is cleared one tile at a time during the first seven iterations of the loop, while the 16-character rank area is cleared during all iterations _if_ `i` modulo 8 equals 1. (Erasing two areas using a single loop feels like a questionable optimization given the context.)

Clearing the star multiplier area makes sense. Even though the digits are opaque and will fully replace any existing content at a tile position, the number shrinks over time (from five digits, to four, and finally a single zero). Erasing the leading digits is a necessary step to ensure the number is shown accurately as its length decreases.

Similarly, the rank text area needs to be explicitly erased because its font characters _do_ have transparency, and failing to do this will lead to visual garbage as new characters pile on top of old ones.

The `i % 8 == 1` conditional makes it so that the rank text is only erased on every eighth iteration of the loop. The text is later redrawn using the same criteria.

```c
        DrawNumberFlushRight(27, 7, (stars - 1) * 1000L);
```

The decremented value of `stars` is multiplied by 1,000 and drawn in place. The subtract-by-one here is due to the fact that the true star count will not be decremented until this iteration of the outermost `for` loop completes fully.

```c
        if (i % 8 == 1) {
            DrawTextLine(13, 14, starBonusRanks[i / 6]);
        }
    }
```

Here, when `i` modulo 8 equals 1, we are in an iteration where the rank text has just been erased and needs to be redrawn. This is done by looking up a rank string in the global {{< lookup/cref starBonusRanks >}} array and drawing it with {{< lookup/cref DrawTextLine >}}. The more stars the player collects, the more iterations are seen here, and the more sequential ranks are encountered.

Earlier it was mentioned that `i` stops at 78, which would result in indexing out-of-bounds array index 13. This does not happen, because `78 % 8` is never 1 and the `if` body does not execute in that case.

There is, however, a bug in the code. Because the text is erased and redrawn every eighth star, but the array indexing uses 6 as the divisor, the text is not redrawn at the same rate that the array index is changing. The end result is that there are only ten text updates while thirteen array elements are traversed, resulting in three of them never displaying. These ranks are "Radical!", "Incredible", and "Towering."

```c
    WaitHard(400);

    gameStars = 0;
}
```

Once all the stars have been tallied, the `for` loop ends and {{< lookup/cref WaitHard >}} gives one final pause for the user to see where they stand. {{< lookup/cref gameStars >}} is zeroed, since the stars have conceptually been "converted" into points and added to the score. From here, the function returns.

{{< boilerplate/function-cref ShowPauseMessage >}}

The {{< lookup/cref ShowPauseMessage >}} function presents a "game paused" dialog, stops music playback, and stops all execution until a key is pressed. Once that happens, the music is restarted and the function returns to its caller.

{{< boilerplate/menu-gameplay object="dialog" >}}

{{< image src="pause-message-2052x.png"
    alt="Pause Message Dialog"
    1x="pause-message-684x.png"
    2x="pause-message-1368x.png"
    3x="pause-message-2052x.png" >}}

```c
void ShowPauseMessage(void)
{
    word x = UnfoldTextFrame(2, 4, 18, "Game Paused.", "Press ANY key.");
    StopAdLibPlayback();
    WaitSpinner(x + 15, 4);
```

The entire message is constructed with clever use of the top/bottom texts in the call to {{< lookup/cref UnfoldTextFrame >}}. Once the dialog is fully on the screen, {{< lookup/cref StopAdLibPlayback >}} immediately stops the music, if any happens to be playing.

{{< lookup/cref WaitSpinner >}} presents the animated spinning cursor in the bottom right of the dialog, and this call blocks until a key is pressed. Until that happens, no other functions in the game (aside from the interrupt handlers) can run. This is what creates the pause effect.

```c
    if (isMusicEnabled) {
        SwitchMusic(activeMusic);
        StartAdLibPlayback();
    }
}
```

Once the player presses a key, execution continues. If the user has enabled music in the game's configuration, {{< lookup/cref isMusicEnabled >}} will be true and the `if` body executes. The call to {{< lookup/cref SwitchMusic >}} restarts the current {{< lookup/cref activeMusic >}} from the beginning _if_ the system has an AdLib compatible card installed -- otherwise the call is a no-op.

{{< lookup/cref StartAdLibPlayback >}} is a superfluous call; {{< lookup/cref SwitchMusic >}} does that before returning.

When this function returns, normal game execution is allowed to resume and the game will unpause. When the next frame is ready to be drawn, the old pause dialog in video memory will be overwritten.

{{< boilerplate/function-cref ShowCheatMessage >}}

The {{< lookup/cref ShowCheatMessage >}} function displays a static dialog informing the user that they have entered the cheat code successfully and explaining the effect. Aside from pausing gameplay while on screen, this function performs no other actions.

{{< boilerplate/menu-gameplay object="dialog" >}}

{{< image src="cheat-message-2052x.png"
    alt="Cheat Message Dialog"
    1x="cheat-message-684x.png"
    2x="cheat-message-1368x.png"
    3x="cheat-message-2052x.png" >}}

```c
void ShowCheatMessage(void)
{
    word x = UnfoldTextFrame(3, 9, 32, "You are now cheating!",
        "Press ANY key.");
    DrawTextLine(x, 6, "  You have been awarded full");
    DrawTextLine(x, 7, " health and maximum amount of");
    DrawTextLine(x, 8, "            bombs!");
    WaitSpinner(x + 29, 10);
}
```

{{< boilerplate/function-cref ToggleGodMode >}}

The {{< lookup/cref ToggleGodMode >}} function inverts the state of the global "god mode" debug flag and presents a dialog informing the user of the current setting.

{{< boilerplate/menu-gameplay object="dialog" >}}

{{< image src="god-mode-2052x.png"
    alt="God Mode Dialogs"
    1x="god-mode-684x.png"
    2x="god-mode-1368x.png"
    3x="god-mode-2052x.png" >}}

```c
void ToggleGodMode(void)
{
    word x;

    isGodMode = !isGodMode;

    if (isGodMode) {
        x = UnfoldTextFrame(2, 4, 28, "God Toggle",
            "The god mode is now ON!");
    } else {
        x = UnfoldTextFrame(2, 4, 28, "God Toggle",
            "The god mode is now OFF!");
    }

    WaitSpinner(x + 25, 4);
}
```

Each time this function is called, it flips the state of the {{< lookup/cref isGodMode >}} flag from false to true, or from true to false. Depending on the resulting value, one of two messages can be displayed: either "The god mode is now ON" or "The god mode is now OFF."

{{< boilerplate/function-cref ShowMemoryUsage >}}

The {{< lookup/cref ShowMemoryUsage >}} function displays a debug dialog with a few live statistics about available system memory and the current number of actors.

{{< boilerplate/menu-gameplay object="dialog" >}}

{{< image src="memory-usage-2052x.png"
    alt="Memory Usage Dialog"
    1x="memory-usage-684x.png"
    2x="memory-usage-1368x.png"
    3x="memory-usage-2052x.png" >}}

```c
void ShowMemoryUsage(void)
{
    word x = UnfoldTextFrame(2, 8, 30, "- Memory Usage -", "Press ANY key.");
    DrawTextLine(x + 6,  4, "Memory free:");
    DrawTextLine(x + 10, 5, "Take Up:");
    DrawTextLine(x + 1,  6, "Total Map Memory:  65049");
    DrawTextLine(x + 5,  7, "Total Actors:");
    DrawNumberFlushRight(x + 24, 4, totalMemFreeAfter);
    DrawNumberFlushRight(x + 24, 5, totalMemFreeBefore);
    DrawNumberFlushRight(x + 24, 7, numActors);
    WaitSpinner(x + 27, 8);
}
```

Some of the lines in this dialog are built with multiple calls: {{< lookup/cref DrawTextLine >}} to draw the static text on the left, and {{< lookup/cref DrawNumberFlushRight >}} to display the number with proper right alignment.

The three dynamic fields are:

* **Memory Free:** Reports the value held in {{< lookup/cref totalMemFreeAfter >}}. This is the amount of system memory available, in bytes, after all calls to {{< lookup/cref malloc >}} were completed. In essence, this is the amount of memory that is unallocated _right now_.
* **Take Up:** Reports the value held in {{< lookup/cref totalMemFreeBefore >}}. This is the amount of system memory, in bytes, that was available when the program first started. This is approximately the amount of conventional memory installed in the system, minus what is being used by DOS and any drivers/TSRs that may be loaded, minus the size of the game's executable image in memory, minus areas used by the BSS variable area and the stack. The difference between this number and the number reported in "Memory Free" is the combined size of all {{< lookup/cref malloc >}}s in the program, plus a bit of slop. The sum of all allocations is always 383,072 bytes if no AdLib music card is installed, or 390,080 bytes with an AdLib. (See {{< lookup/cref ValidateSystem >}} for more discussion on the allocation sizes.) The difference between "Take Up" and Memory Free" should be one of those two values.
* **Total Actors:** This is the peak number of actor slots that have been used since the current level started. Since the actors' state is stored in a fixed-size array, this number informs a level designer how close the game is to its storage limits. This number does not decrease when actors die, nor does it increase if a new actor is created in a dead actor's slot.

The remaining **Total Map Memory** value is hard-coded to 65,049 and there is no clear reason why. This cannot refer to the variables in the BSS area, as those use less than 26 KiB of memory per the EXE header. Furthermore, no combination of the dynamic memory allocations add up to anything close to this amount.

{{< aside class="armchair-engineer" >}}
**But wait, there's more!**

65,049 is simply a weird number. It's the product of two primes (3 and 21,683) and highly unlikely to be a real measurement of any object in memory. Furthermore, the number is embedded in an ASCII string in the data segment of the compiled code, meaning that its value was known at compile time. Even if we assume the value was a true measurement of something, operators like `sizeof` return integers -- not strings. Without using a `printf()` variant or the non-standard `itoa()` function, there is no way I can figure to construct this string other than typing it directly into the source code.

If you have any thoughts about what else this value could mean or any C preprocessor tricks that could have been used to get it there, [please let me know!](mailto:scott@smitelli.com)
{{< /aside >}}

{{< boilerplate/function-cref ShowBombHint >}}

The {{< lookup/cref ShowBombHint >}} function displays a hint dialog that informs the player that they can't use the bomb key until they have picked up a bomb.

{{< boilerplate/menu-gameplay object="dialog" >}}

{{< image src="bomb-hint-2052x.png"
    alt="Bomb Hint Dialog"
    1x="bomb-hint-684x.png"
    2x="bomb-hint-1368x.png"
    3x="bomb-hint-2052x.png" >}}

```c
void ShowBombHint(void)
{
    word x;

    if (demoState != DEMO_STATE_NONE) return;
```

If the {{< lookup/cref demoState >}} value is anything other than {{< lookup/cref name="DEMO_STATE" text="DEMO_STATE_NONE" >}}, a demo is either being played back or recorded. Both of these scenarios would conflict with dialog display, so this function returns early in such cases.

```c
    EGA_MODE_LATCHED_WRITE();
    SelectDrawPage(activePage);
    StartSound(SND_HINT_DIALOG_ALERT);
```

{{< lookup/cref EGA_MODE_LATCHED_WRITE >}} is a superfluous call; it will occur automatically as part of {{< lookup/cref UnfoldTextFrame >}}'s operation. The intent is to switch the EGA hardware into "latched write" mode, which is necessary to draw the solid tiles that comprise the dialog frame. This may have been necessary during an earlier iteration of the game's development.

The game is normally run with double-buffering for the screen contents. While one page of screen content is being shown to the user (the **active page**) another page is being redrawn in a background buffer (the **draw page**). Generally the active page is never touched as long as it is visible, preventing the user from ever seeing a partially-drawn frame of content. When a new frame is ready, the active and draw pages reverse roles to update the visible content on screen. By explicitly calling {{< lookup/cref SelectDrawPage >}} with {{< lookup/cref activePage >}} as the argument, the double-buffering behavior is disabled and any drawing functions will immediately appear on the screen.

{{< lookup/cref StartSound >}} queues the {{< lookup/cref name="SND" text="SND_HINT_DIALOG_ALERT" >}} beep, which plays asynchronously as execution continues here.

```c
    x = UnfoldTextFrame(2, 4, 28, "", "");
    DrawTextLine(x + 1, 3, "You haven't found any");
    DrawTextLine(x + 1, 4, "bombs to use yet!     \xFE""056000");
    WaitHard(60);
    WaitSpinner(x + 25, 4);
```

The dialog is relatively simple, containing a hint for the player along with a "draw actor sprite" command string to include an image of a bomb sprite.

{{< lookup/cref WaitHard >}} pauses before presenting the wait spinner, which can absorb any button presses the user might have made that would dismiss the dialog before they realized it was there. Once the delay expires, {{< lookup/cref WaitSpinner >}} allows the player to acknowledge and dismiss the dialog.

{{< note >}}The wait spinner can only be dismissed by pressing a key on the keyboard. If a joystick is being used, pressing a joystick button will _not_ dismiss this hint dialog.{{< /note >}}

```c
    SelectDrawPage(!activePage);
}
```

Before returning, {{< lookup/cref SelectDrawPage >}} is called again to undo the page manipulation that was performed earlier. The game uses two screen pages -- numbered 0 and 1 -- so setting the draw page to {{< lookup/cref name="activePage" text="!activePage" >}} restores the behavior where the draw functions target the current non-active page.

When the next frame completes its drawing and the screen pages flip, the old frame of gameplay (along with the content of this dialog) will be overwritten by the next frame of gameplay.

{{< boilerplate/function-cref ShowPounceHint >}}

The {{< lookup/cref ShowPounceHint >}} function displays a sequence of two hint dialogs that teach the player how to pounce on enemies for defense.

{{< boilerplate/menu-gameplay object="dialog" >}}

{{< image src="pounce-hint-2052x.png"
    alt="Pounce Hint Dialogs"
    1x="pounce-hint-684x.png"
    2x="pounce-hint-1368x.png"
    3x="pounce-hint-2052x.png" >}}

```c
void ShowPounceHint(void)
{
    word x;

    if (demoState != DEMO_STATE_NONE) return;

    EGA_MODE_LATCHED_WRITE();
    SelectDrawPage(activePage);
    StartSound(SND_HINT_DIALOG_ALERT);

    x = UnfoldTextFrame(2, 5, 22, "REMINDER:  Jump on",
        "defend yourself.  ");
    DrawTextLine(x, 4, " top of creatures to");
    WaitHard(60);
    WaitSpinner(x + 19, 5);

    x = UnfoldTextFrame(2, 13, 20, "Like this...", "Press ANY key.");
    DrawTextLine(x + 5, 9,  "   \xFD""036");
    DrawTextLine(x + 5, 11, "   \xFE""118000");
    WaitHard(60);
    WaitSpinner(x + 17, 13);

    SelectDrawPage(!activePage);
}
```

This works identically to {{< lookup/cref ShowBombHint >}}, except here two dialogs are presented instead of one. The second dialog contains a combination of "draw player sprite" and "draw actor sprite" commands to produce a small scene demonstrating the action of a player jumping on a {{< lookup/actor 118 >}}.

{{< boilerplate/function-cref ShowHealthHint >}}

The {{< lookup/cref ShowHealthHint >}} function displays a hint dialog that teaches the player what {{< lookup/actor type=28 strip=true plural=true >}} are and how they affect gameplay.

{{< boilerplate/menu-gameplay object="dialog" >}}

{{< image src="health-hint-2052x.png"
    alt="Health Hint Dialog"
    1x="health-hint-684x.png"
    2x="health-hint-1368x.png"
    3x="health-hint-2052x.png" >}}

```c
void ShowHealthHint(void)
{
    word x;

    if (demoState != DEMO_STATE_NONE) return;

    EGA_MODE_LATCHED_WRITE();
    SelectDrawPage(activePage);
    StartSound(SND_HINT_DIALOG_ALERT);

    x = UnfoldTextFrame(2, 5, 22, "", "");
    DrawTextLine(x, 3, " Power Up modules");
    DrawTextLine(x, 4, " increase Cosmo's");
    DrawTextLine(x, 5, " health.         \xFE""028002");
    WaitHard(60);
    WaitSpinner(x + 8, 5);

    SelectDrawPage(!activePage);
}
```

This works identically to {{< lookup/cref ShowBombHint >}}.

{{< boilerplate/function-cref ShowHintGlobeMessage >}}

The {{< lookup/cref ShowHintGlobeMessage >}} function displays a dialog containing an animated context-appropriate hint message. The message is selected via the numeric `hint_num` argument. Different episodes have different `hint_num` ranges: 0&ndash;18 in episode one, 0&ndash;7 in episode two, and 0&ndash;5 in episode three. These numbers are reused and refer to different messages from episode to episode.

Passing an undefined `hint_num` has a different effect depending on the episode being played. In episode 1, the function essentially becomes a no-op. In episodes 2 and 3, the function displays a frame without any inner hint text.

{{< boilerplate/menu-gameplay object="dialog" >}}

{{< image src="hint-globe-message-2052x.png"
    alt="Hint Globe Message Dialog"
    1x="hint-globe-message-684x.png"
    2x="hint-globe-message-1368x.png"
    3x="hint-globe-message-2052x.png" >}}

```c
void ShowHintGlobeMessage(word hint_num)
{
    word x;

    SelectDrawPage(activePage);
    WaitHard(30);
```

These dialogs interrupt the usual page-flipping mechanisms employed by the game loop. To ensure that the effect of the drawing calls is immediately visible, the draw page is temporarily reset to {{< lookup/cref activePage >}} via a call to {{< lookup/cref SelectDrawPage >}}.

{{< lookup/cref WaitHard >}} pauses to ensure that no keys are being hit that might prematurely dismiss or hurry through a message before it is noticed.

```c
#if EPISODE == 1
    if (hint_num != 0 && hint_num < 15) {
        x = UnfoldTextFrame(2, 9, 28, "COSMIC HINT!",
            "Press any key to exit.");
        DrawTextLine(x, 8, " Press SPACE to hurry or");
    }
```

The content of the hint messages changes from episode to episode, so a conditional check is made against the `EPISODE` macro. If the game is currently being compiled for episode one, this section is included.

Episode one is special because some of the hint texts are longer or contain some kind of sprite in addition to the text. These longer texts need a larger frame, which means the construction of that frame might need to change on a message by message basis. The choice is made here: if `hint_num` is between 1 and 14, inclusive, it is one of the "standard" hints that can use the common dialog frame and hint spinner. In those cases, {{< lookup/cref UnfoldTextFrame >}} and {{< lookup/cref DrawTextLine >}} creates that frame here.

If `hint_num` is zero or anything greater than 14, the frame is _not_ drawn here and must be done manually later.

```c
    switch (hint_num) {
    case 0:
        x = UnfoldTextFrame(2, 11, 28, "COSMIC HINT!",
            "Press any key to exit.");
        DrawTextLine(x, 10, " Press SPACE to hurry or");
        DrawTextLine(x, 5, "\xFC""003 These hint globes will");
        DrawTextLine(x, 6, "\xFC""003 help you along your");
        DrawTextLine(x, 7, "\xFC""003 journey.  Press the up");
        DrawTextLine(x, 8, "\xFC""003 key to reread them.");
        WaitSpinner(x + 25, 11);
        break;
```

The `switch` block handles the actual conditional switching between the different `hint_num` values. Each `case` is a hint text implementation. In this case, we are showing `hint_num` 0, which uses a non-standard frame which must be constructed manually, hence the call to {{< lookup/cref UnfoldTextFrame >}} and {{< lookup/cref WaitSpinner >}} here.

```c
    case 1:
        DrawTextLine(x, 5, "\xFC""003 Bump head into switch");
        DrawTextLine(x, 6, "\xFC""003 above!");
        break;
```

This is `hint_num` 1, which is one of the standard hints. It can rely on the presence of the standard frame from earlier in the function's execution.

```c
    case 2:
        DrawTextLine(x, 5, "\xFC""003 The ice in this cave is");
        DrawTextLine(x, 6, "\xFC""003 very, very slippery.");
        break;

    case 3:
        DrawTextLine(x, 5, "\xFC""003 Use this shield for");
        DrawTextLine(x, 6, "\xFC""003 temporary invincibility.");
        break;

    case 4:
        DrawTextLine(x, 5, "\xFC""003 You found a secret");
        DrawTextLine(x, 6, "\xFC""003 area!!!  Good job!");
        break;

    case 5:
        DrawTextLine(x, 5, "\xFC""003 In high places look up");
        DrawTextLine(x, 6, "\xFC""003 to find bonus objects.");
        break;

    case 6:
        DrawTextLine(x, 5, "\xFC""003      Out of Order...");
        break;

    case 7:
        DrawTextLine(x, 5, "\xFC""003 This might be a good");
        DrawTextLine(x, 6, "\xFC""003 time to save your game!");
        break;

    case 8:
        DrawTextLine(x, 5, "\xFC""003 Press your up key to");
        DrawTextLine(x, 6, "\xFC""003 use the transporter.");
        break;

    case 9:
        DrawTextLine(x, 5, "\xFC""003  (1) FOR...");
        break;

    case 10:
        DrawTextLine(x, 5, "\xFC""003  (2) EXTRA...");
        break;

    case 11:
        DrawTextLine(x, 5, "\xFC""003  (3) POINTS,...");
        break;

    case 12:
        DrawTextLine(x, 5, "\xFC""003  (4) DESTROY...");
        break;

    case 13:
        DrawTextLine(x, 5, "\xFC""003  (5) HINT...");
        break;

    case 14:
        DrawTextLine(x, 5, "\xFC""003  (6) GLOBES!!!");
        break;
```

These are the remaining standard-size hints.

```c
    case 15:
        x = UnfoldTextFrame(2, 11, 28, "COSMIC HINT!",
            "Press any key to exit.");
        DrawTextLine(x + 22, 8, "\xFE""083000");
        DrawTextLine(x, 10, " Press SPACE to hurry or");
        DrawTextLine(x, 5, "\xFC""003  The Clam Plants won't");
        DrawTextLine(x, 6, "\xFC""003  hurt you if their");
        DrawTextLine(x, 7, "\xFC""003  mouths are closed.");
        WaitSpinner(x + 25, 11);
        break;
```

This is another non-standard hint that must construct its frame from scratch. This includes a Clam Plant sprite along with the text.

```c
    case 16:
        x = UnfoldTextFrame(2, 10, 28, "COSMIC HINT!",
            "Press any key to exit.");
        DrawTextLine(x, 9, " Press SPACE to hurry or");
        DrawTextLine(x + 23, 7, "\xFE""001002");
        DrawTextLine(x, 5, "\xFC""003  Collect the STARS to");
        DrawTextLine(x, 6, "\xFC""003  advance to BONUS");
        DrawTextLine(x, 7, "\xFC""003  STAGES.");
        WaitSpinner(x + 25, 10);
        break;

    case 17:
        x = UnfoldTextFrame(2, 10, 28, "COSMIC HINT!",
            "Press any key to exit.");
        DrawTextLine(x, 9, " Press SPACE to hurry or");
        DrawTextLine(x, 5, "\xFC""003  Some creatures require");
        DrawTextLine(x, 6, "\xFC""003  more than one pounce");
        DrawTextLine(x, 7, "\xFC""003  to defeat!");
        WaitSpinner(x + 25, 10);
        break;

    case 18:
        x = UnfoldTextFrame(2, 9, 30, "COSMIC HINT!",
            "Press any key to exit.");
        DrawTextLine(x + 25, 8, "\xFD""032");
        DrawTextLine(x, 8, "  Press SPACE to hurry or");
        /* Incorrect possessive form preserved faithfully */
        DrawTextLine(x, 5, "\xFC""003 Cosmo can climb wall's");
        DrawTextLine(x, 6, "\xFC""003 with his suction hands.");
        WaitSpinner(x + 27, 9);
        break;
    }
```

The `case` block ends with the remaining few non-standard hints.

```c
    if (hint_num != 0 && hint_num < 15) {
        WaitSpinner(x + 25, 9);
    }
```

As before, the standard frames need a standard wait spinner, which is created by the call to {{< lookup/cref WaitSpinner >}} here. Non-standard hints will not satisfy the condition, and are each responsible for constructing their own wait spinner at the appropriate screen position for their size.

```c
#elif EPISODE == 2
    x = UnfoldTextFrame(2, 9, 28, "COSMIC HINT!", "Press any key to exit.");
    DrawTextLine(x, 8, " Press SPACE to hurry or");
```

The conditional compilation moves on to episode two. All the hints in this episode are the same, standard, size and do not require the conditional check that episode one did -- all the frames and wait spinners are drawn in one place in this episode.

```c
    switch (hint_num) {
    case 0:
        DrawTextLine(x, 5, "\xFC""003 Look out for enemies");
        DrawTextLine(x, 6, "\xFC""003 from above!");
        break;

    case 1:
        DrawTextLine(x, 5, "\xFC""003    Don't...");
        break;

    case 2:
        DrawTextLine(x, 5, "\xFC""003    step...");
        break;

    case 3:
        DrawTextLine(x, 5, "\xFC""003    on...");
        break;

    case 4:
        DrawTextLine(x, 5, "\xFC""003    worms...");
        break;

    case 5:
        DrawTextLine(x, 5, "\xFC""003 There is a secret area");
        DrawTextLine(x, 6, "\xFC""003 in this level!");
        break;

    case 6:
        DrawTextLine(x, 5, "\xFC""003 You found the secret");
        DrawTextLine(x, 6, "\xFC""003 area.  Well done.");
        break;

    case 7:
        DrawTextLine(x, 5, "\xFC""003    Out of order.");
        break;
    }

    WaitSpinner(x + 25, 9);
```

Each hint text is shown for the appropriate `hint_num` case. There is only one {{< lookup/cref WaitSpinner >}} needed, as all the hints use a frame of the same size.

```c
#elif EPISODE == 3
    x = UnfoldTextFrame(2, 9, 28, "COSMIC HINT!", "Press any key to exit.");
    DrawTextLine(x, 8, " Press SPACE to hurry or");

    switch (hint_num) {
    case 0:
        DrawTextLine(x, 5, "\xFC""003 Did you find the");
        DrawTextLine(x, 6, "\xFC""003 hamburger in this level?");
        break;

    case 1:
        DrawTextLine(x, 5, "\xFC""003 This hint globe being");
        DrawTextLine(x, 6, "\xFC""003 upgraded to a 80986.");
        break;

    case 2:
        DrawTextLine(x, 5, "\xFC""003 WARNING:  Robots shoot");
        DrawTextLine(x, 6, "\xFC""003 when the lights are on!");
        break;

    case 3:
        DrawTextLine(x, 5, "\xFC""003 There is a hidden scooter");
        DrawTextLine(x, 6, "\xFC""003 in this level.");
        break;

    case 4:
        DrawTextLine(x, 5, "\xFC""003 Did you find the");
        DrawTextLine(x, 6, "\xFC""003 hamburger in level 8!");
        break;

    case 5:
        DrawTextLine(x, 5, "\xFC""003   Out of order...!");
        break;
    }

    WaitSpinner(x + 25, 9);
```

Episode three works the same as episode two.

```c
#endif

    SelectDrawPage(!activePage);
}
```

The conditionally-compiled code ends here, followed by a call to {{< lookup/cref SelectDrawPage >}} to restore the page-flipping mechanism to how it normally works during gameplay. Here the draw page is set to the page that is _not_ {{< lookup/cref activePage >}}, which is the normal state for the game to be in.

{{< boilerplate/function-cref ShowRescuedDNMessage >}}

The {{< lookup/cref ShowRescuedDNMessage >}} function displays a dialog sequence between the player and Duke Nukem (here using the short-lived but canonical spelling "Nukum"). This is part easter egg, part secret bonus that can be encountered in the second episode of the game.

This function uses two helper functions named {{< lookup/cref UnfoldPlayerFrame >}} and {{< lookup/cref UnfoldDNFrame >}} to simplify repetitive creation of dialog frames with the characters' sprites positioned inside them. Each of these functions takes no parameters, displays a frame with a fixed size and position, and returns the appropriate X position where text should be rendered for that frame.

{{< boilerplate/menu-gameplay object="dialog" >}}

{{< image src="rescued-dn-message-2052x.png"
    alt="Rescued Duke Nukem Message Dialogs"
    1x="rescued-dn-message-684x.png"
    2x="rescued-dn-message-1368x.png"
    3x="rescued-dn-message-2052x.png" >}}

```c
void ShowRescuedDNMessage(void)
{
    register word x;

#ifdef HAS_ACT_FROZEN_DN
    SelectDrawPage(activePage);
```

This sequence can only occur in episodes that have the {{< lookup/actor 221 >}} actor defined, which is conditionally controlled by the `HAS_ACT_FROZEN_DN` macro. If that macro is not set, this function still exists in the compiled code, but it has no body and does nothing.

To ensure that the effect of the drawing calls is immediately visible, the draw page is temporarily reset to {{< lookup/cref activePage >}} via a call to {{< lookup/cref SelectDrawPage >}}.

```c
    x = UnfoldPlayerFrame();
    DrawTextLine(x, 5, "\xFC""003  Yikes, who are you?");
    WaitSpinner(x + 27, 8);
```

The function starts with the player speaking, represented by the content in an {{< lookup/cref UnfoldPlayerFrame >}} dialog. The wait spinner in these dialogs is positioned immediately after the "press a key to continue" text.

```c
    x = UnfoldDNFrame();
    DrawTextLine(x, 4, "\xFC""003 I'm Duke Nukum, green");
    DrawTextLine(x, 5, "\xFC""003 alien dude.              ");
    WaitSpinner(x + 27, 8);

    x = UnfoldDNFrame();
    DrawTextLine(x, 4, "\xFC""003 Until you rescued me, I");
    DrawTextLine(x, 5, "\xFC""003 was stopped cold by an");
    DrawTextLine(x, 6, "\xFC""003 alien invasion force!");
    WaitSpinner(x + 27, 8);
```

Duke responds in his own set of {{< lookup/cref UnfoldDNFrame >}} dialogs. The wait spinner in these dialogs is in the bottom-right corner of the frame, which is slightly inconsistent from how {{< lookup/cref UnfoldPlayerFrame >}} aligns it.

```c
    x = UnfoldPlayerFrame();
    DrawTextLine(x, 4, "\xFC""003 Wow!  Can you help rescue ");
    DrawTextLine(x, 5, "\xFC""003 my parents?");
    WaitSpinner(x + 27, 8);

    x = UnfoldDNFrame();
    DrawTextLine(x, 4, "\xFC""003 Sorry, kid, I've got to");
    DrawTextLine(x, 5, "\xFC""003 save the galaxy...");
    WaitSpinner(x + 27, 8);

    x = UnfoldDNFrame();
    DrawTextLine(x, 4, "\xFC""003 ...but, I can give you");
    DrawTextLine(x, 5, "\xFC""003 something that will help");
    DrawTextLine(x, 6, "\xFC""003 you out.");
    WaitSpinner(x + 27, 8);

    x = UnfoldPlayerFrame();
    DrawTextLine(x, 4, "\xFC""003 Thanks, Mr. Nukum, and");
    DrawTextLine(x, 5, "\xFC""003 good luck on your mission.");
    WaitSpinner(x + 27, 8);

    x = UnfoldDNFrame();
    DrawTextLine(x, 4, "\xFC""003 Just look for me in my");
    DrawTextLine(x, 5, "\xFC""003 next exciting adventure,");
    DrawTextLine(x, 6, "\xFC""003 Duke Nukum II!");
    WaitSpinner(x + 27, 8);

    x = UnfoldPlayerFrame();
    DrawTextLine(x, 5, "\xFC""003             Bye.");
    WaitSpinner(x + 27, 8);

    x = UnfoldDNFrame();
    DrawTextLine(x, 4, "\xFC""003 See ya... and have those");
    DrawTextLine(x, 5, "\xFC""003 spots checked...!");
    WaitSpinner(x + 27, 8);

    SelectDrawPage(!activePage);
#endif
}
```

The player and Duke converse for a bit, then they part ways.

{{< aside class="fun-fact" >}}
**Hey, wait!**

Cosmo never even told Duke his name here.
{{< /aside >}}

{{< lookup/cref SelectDrawPage >}} restores the page-flipping mechanism to how it normally works during gameplay. Here the draw page is set to the page that is _not_ {{< lookup/cref activePage >}}, which is the normal state for the game to be in.

{{< boilerplate/function-cref UnfoldPlayerFrame >}}

{{< lookup/cref UnfoldPlayerFrame >}} is a helper function that draws the dialog frame that is used when the player is speaking to Duke. It contains no inner content aside from a player sprite image on the right side. Returns the X coordinate where text should be placed to appear within the frame.

{{< boilerplate/menu-gameplay object="dialog" >}}

```c
word UnfoldPlayerFrame(void)
{
    register word x;

#ifdef HAS_ACT_FROZEN_DN
    x = UnfoldTextFrame(2, 8, 34, "", "Press a key to continue.");
    DrawTextLine(x + 29, 7, "\xFD""004");

    return x + 1;
#endif
}
```

This function's body is conditionally compiled based on the `HAS_ACT_FROZEN_DN` macro. If unset, the function is an empty no-op that returns uninitialized garbage.

{{< boilerplate/function-cref UnfoldDNFrame >}}

{{< lookup/cref UnfoldDNFrame >}} is a helper function that draws the dialog frame that is used when Duke is speaking to the player. It contains no inner content aside from a Duke sprite image on the left side. Returns the X coordinate where text should be placed to appear within the frame.

{{< boilerplate/menu-gameplay object="dialog" >}}

```c
word UnfoldDNFrame(void)
{
    register word x;

#ifdef HAS_ACT_FROZEN_DN
    x = UnfoldTextFrame(2, 8, 34, "", "Press a key to continue.");
    DrawTextLine(x + 1, 7, "\xFE""221003");

    return x + 4;
#endif
}
```

This function's body is conditionally compiled based on the `HAS_ACT_FROZEN_DN` macro. If unset, the function is an empty no-op that returns uninitialized garbage.

{{< boilerplate/function-cref ShowE1CliffhangerMessage >}}

The {{< lookup/cref ShowE1CliffhangerMessage >}} function presents a sequence of two dialogs introducing the "cliffhanger" ending sequence of episode one, followed by ending the game by setting {{< lookup/cref winGame >}} to true. During each call, the passed `actor_type` value is used to determine which text to show, or if the game should end.

{{< boilerplate/menu-gameplay object="dialog" >}}

{{< image src="e1-cliffhanger-message-2052x.png"
    alt="Episode 1 Cliffhanger Message Dialogs"
    1x="e1-cliffhanger-message-684x.png"
    2x="e1-cliffhanger-message-1368x.png"
    3x="e1-cliffhanger-message-2052x.png" >}}

```c
void ShowE1CliffhangerMessage(word actor_type)
{
    register word x;

#ifdef E1_CLIFFHANGER
    SelectDrawPage(activePage);
```

This function is conditionally compiled into certain episodes, and compiles to a no-op function if the `E1_CLIFFHANGER` macro is not defined. This function only exists in episode one of the original game.

The game is normally run with double-buffering for the screen contents. While one page of screen content is being shown to the user (the **active page**) another page is being redrawn in a background buffer (the **draw page**). Generally the active page is never touched as long as it is visible, preventing the user from ever seeing a partially-drawn frame of content. When a new frame is ready, the active and draw pages reverse roles to update the visible content on screen. By explicitly calling {{< lookup/cref SelectDrawPage >}} with {{< lookup/cref activePage >}} as the argument, the double-buffering behavior is disabled and any drawing functions will immediately appear on the screen.

```c
    switch (actor_type) {
    case ACT_EP1_END_1:
        x = UnfoldTextFrame(2, 8, 28, "", "Press any key to exit.");
        DrawTextLine(x, 4, "\xFC""003 What's happening?  Is ");
        DrawTextLine(x, 5, "\xFC""003 Cosmo falling to his ");
        DrawTextLine(x, 6, "\xFC""003 doom?");
        WaitSpinner(x + 25, 8);
        break;
```

The code `switch`es on the `actor_type` passed to the function. If the actor's type matches {{< lookup/cref name="ACT" text="ACT_EP1_END_1" >}}, this is an {{< lookup/actor type=164 strip=true >}} and this first dialog should be presented.

```c
    case ACT_EP1_END_2:
        x = UnfoldTextFrame(2, 8, 28, "", "Press any key to exit.");
        DrawTextLine(x, 4, "\xFC""003 Is there no end to this ");
        DrawTextLine(x, 5, "\xFC""003 pit?  And what danger ");
        DrawTextLine(x, 6, "\xFC""003 awaits below?! ");
        WaitSpinner(x + 25, 8);
        break;
```

In the {{< lookup/cref name="ACT" text="ACT_EP1_END_2" >}} case ({{< lookup/actor type=165 strip=true >}}), things work similarly but with new text.

```c
    case ACT_EP1_END_3:
        winGame = true;
        break;
    }
```

For {{< lookup/cref name="ACT" text="ACT_EP1_END_3" >}} ({{< lookup/actor type=166 strip=true >}}), however, no dialog is shown. This is the last reachable point in this episode of the game, and {{< lookup/cref winGame >}} is set true here. This ultimately breaks out of the game loop and moves into the ending sequence.

```c
    SelectDrawPage(!activePage);
#endif
}
```

Before returning, {{< lookup/cref SelectDrawPage >}} is called again to undo the page manipulation that was performed earlier. The game uses two screen pages -- numbered 0 and 1 -- so setting the draw page to {{< lookup/cref name="activePage" text="!activePage" >}} restores the behavior where the draw functions target the current non-active page.

When the next frame completes its drawing and the screen pages flip, the old frame of gameplay (along with the content of this dialog) will be replaced by the new frame.

{{< boilerplate/function-cref ShowEnding >}}

The {{< lookup/cref ShowEnding >}} function presents a sequence of dialogs when an episode of the game has been played to completion. The length of this end-game story and its overall behavior changes from episode to episode, but each ends with a call to {{< lookup/cref ShowOrderingInformation >}} followed by {{< lookup/cref ShowStarBonus >}}.

```c
void ShowEnding(void)
{
    word x;
```

From this point, the behavior changes with each episode based on the value of the `EPISODE` macro. Only one of these sections will be present in a particular episode's code.

### Episode One

{{< image src="ending-e1-2052x.png"
    alt="Episode 1 Ending Dialogs"
    1x="ending-e1-684x.png"
    2x="ending-e1-1368x.png"
    3x="ending-e1-2052x.png" >}}

```c
#if EPISODE == 1
    SelectDrawPage(0);
    SelectActivePage(0);
    WaitHard(5);
    FadeOut();
```

Together, {{< lookup/cref SelectDrawPage >}} and {{< lookup/cref SelectActivePage >}} select display page zero for both display and drawing. This makes it so that any drawing operation will be immediately visible on the screen without involving the page-flipping mechanisms.

{{< lookup/cref WaitHard >}} pauses for five ticks (an almost imperceptible amount of time) then {{< lookup/cref FadeOut >}} fades the screen to black using palette manipulation.

```c
    DrawFullscreenImage(IMAGE_END);
    WaitSpinner(39, 24);
```

{{< lookup/cref DrawFullscreenImage >}} draws the {{< lookup/cref name="IMAGE" text="IMAGE_END" >}} image to the screen, which in this episode is a view of the player falling towards a large creature's mouth. As part of the image drawing, the screen will get faded back into view _and_ any playing music will be stopped. Once the image is visible, {{< lookup/cref WaitSpinner >}} draws its cursor on the bottom-rightmost tile of the screen and waits for any key to be pressed.

```c
    FadeWhiteCustom(4);
    ClearScreen();
```

{{< lookup/cref FadeWhiteCustom >}} is similar to {{< lookup/cref FadeOutCustom >}}, but fades all the palette registers to white. This allows {{< lookup/cref ClearScreen >}} to erase the display memory without the changes being immediately visible.

```c
    x = UnfoldTextFrame(1, 24, 38, "", "Press ANY key.");
    DrawTextLine(x + 4,  13, "\xFB""016");
    DrawTextLine(x + 28, 22, "\xFB""017");
    FadeIn();
```

With the screen still showing solid white, a dialog frame is constructed with calls to {{< lookup/cref UnfoldTextFrame >}} and {{< lookup/cref DrawTextLine >}}.

{{< lookup/cref FadeIn >}} fades the screen back to normal, showing a dialog frame that is empty aside from two cartoon images. The text animation begins:

```c
    DrawTextLine(x + 14, 4,  "\xFC""003Are Cosmo's cosmic ");
    DrawTextLine(x + 14, 5,  "\xFC""003adventuring days ");
    DrawTextLine(x + 14, 6,  "\xFC""003finally over?    ");
    DrawTextLine(x + 14, 8,  "\xFC""003Will Cosmo's parents ");
    DrawTextLine(x + 14, 9,  "\xFC""003be lightly seasoned ");
    DrawTextLine(x + 14, 10, "\xFC""003and devoured before ");
    DrawTextLine(x + 14, 11, "\xFC""003he can save them?      ");
    DrawTextLine(x + 1,  15, "\xFC""003Find the stunning ");
    DrawTextLine(x + 1,  16, "\xFC""003answers in the next two ");
    DrawTextLine(x + 1,  17, "\xFC""003NEW, shocking, amazing, ");
    DrawTextLine(x + 1,  18, "\xFC""003horrifying, wacky and ");
    DrawTextLine(x + 1,  19, "\xFC""003exciting episodes of...         ");
    DrawTextLine(x + 1,  21, "\xFC""003COSMO'S COSMIC ADVENTURE!");
    WaitSpinner(x + 35, 23);
```

The cliffhanger text is presented over multiple {{< lookup/cref DrawTextLine >}} calls, and {{< lookup/cref WaitSpinner >}} waits for a key press.

```c
    FadeOut();
    ClearScreen();

    x = UnfoldTextFrame(6, 4, 24, "Thank you", " for playing!");
    FadeIn();
    WaitHard(100);
    WaitSpinner(x + 21, 8);
```

The previous dialog is faded out with {{< lookup/cref FadeOut >}}, then erased from video memory with {{< lookup/cref ClearScreen >}}.

A new "thank you" message is drawn with {{< lookup/cref UnfoldTextFrame >}}, and that is brought into view with {{< lookup/cref FadeIn >}}. {{< lookup/cref WaitHard >}} imposes a delay of 100 ticks, then {{< lookup/cref WaitSpinner >}} permits the user to press a key to continue.

From here, execution jumps out of the conditionally-compiled code into the [epilogue](#common-epilogue).

### Episode Two

{{< image src="ending-e2-2052x.png"
    alt="Episode 2 Ending Dialogs"
    1x="ending-e2-684x.png"
    2x="ending-e2-1368x.png"
    3x="ending-e2-2052x.png" >}}

```c
#elif EPISODE == 2
    FadeOut();
    SelectDrawPage(0);
    SelectActivePage(0);
    ClearScreen();
```

This begins similarly to the episode one version. The main difference here is that {{< lookup/cref ClearScreen >}} is called explicitly -- since no full-screen image is drawn initially, the screen needs to be emptied before the first dialog is drawn.

```c
    x = UnfoldTextFrame(1, 24, 38, "", "Press ANY key.");
    DrawTextLine(x + 25, 15, "\xFB""021");
    FadeIn();
```

As with episode one, {{< lookup/cref FadeIn >}} initially shows an empty dialog with only the cartoon image present.

```c
    DrawTextLine(x + 1,  7,  "\xFC""003 Young Cosmo leaps ");
    DrawTextLine(x + 1,  9,  "\xFC""003 through a small hole ");
    DrawTextLine(x + 1,  11, "\xFC""003 in the cave ceiling, ");
    DrawTextLine(x + 1,  13, "\xFC""003 and finally sees what ");
    DrawTextLine(x + 1,  15, "\xFC""003 he's searching for... ");
    WaitSpinner(x + 35, 23);
```

The story text is animated in with {{< lookup/cref DrawTextLine >}} and {{< lookup/cref WaitSpinner >}} waits for a key press.

```c
    DrawFullscreenImage(IMAGE_END);
    StartMenuMusic(MUSIC_ROCKIT);

    x = UnfoldTextFrame(18, 5, 38, "", "");
    DrawTextLine(x + 1, 19, "\xFC""003 ...the city where his parents are ");
    DrawTextLine(x + 1, 20, "\xFC""003  held captive--undoubtedly being");
    DrawTextLine(x + 1, 21, "\xFC""003     readied for the big feast!");
    WaitSpinner(37, 21);
```

{{< lookup/cref DrawFullscreenImage >}} will fade the screen out and back in while replacing the screen contents with the passed image, here an image of Cosmo looking over a distant city ({{< lookup/cref name="IMAGE" text="IMAGE_END" >}}). Once the new image finishes fading in, {{< lookup/cref StartMenuMusic >}} plays {{< lookup/cref name="MUSIC" text="MUSIC_ROCKIT" >}} from the start.

{{< lookup/cref UnfoldTextFrame >}} draws a text frame directly over the bottom of the city image, and {{< lookup/cref DrawTextLine >}} fills it with the story's continuation. {{< lookup/cref WaitSpinner >}} waits for another key press.

```c
    x = UnfoldTextFrame(18, 5, 38, "", "");
    DrawTextLine(x + 1, 19, "\xFC""003    Cosmo knows what he must do.");
    DrawTextLine(x + 1, 20, "\xFC""003    Enter the city and save his ");
    DrawTextLine(x + 1, 21, "\xFC""003   parents before it's too late!");
    WaitSpinner(37, 21);
```

As before, the new dialog frame is drawn entirely over the previous frame, replacing it.

```c
    FadeWhiteCustom(4);
    ClearScreen();

    x = UnfoldTextFrame(6, 4, 24, "Thank you", " for playing!");
    FadeIn();
    WaitHard(100);
    WaitSpinner(x + 21, 8);
```

This "thank you" message is identical to the one in episode one. Execution jumps to the [epilogue](#common-epilogue).

### Episode Three

The third and final episode of the game has the longest end-game story. It also may contain spoilers, if that's something you're interested in avoiding.

{{< image src="ending-e3-2052x.png"
    alt="Episode 3 Ending Dialogs"
    1x="ending-e3-684x.png"
    2x="ending-e3-1368x.png"
    3x="ending-e3-2052x.png" >}}

Overall, there aren't many techniques or details in this episode that the other two episodes haven't already done.

```c
#elif EPISODE == 3
    StartMenuMusic(MUSIC_HAPPY);
    FadeOut();
    SelectDrawPage(0);
    SelectActivePage(0);
    ClearScreen();
```

The transition into the ending is similar to episode two. New here is the addition of {{< lookup/cref StartMenuMusic >}}, starting {{< lookup/cref name="MUSIC" text="MUSIC_HAPPY" >}} at the very beginning of the sequence.

```c
    x = UnfoldTextFrame(1, 22, 38, "", "Press ANY key.");
    DrawTextLine(x + 1, 17, "\xFB""018");
    DrawTextLine(x + 17, 6,  "The creature is");
    DrawTextLine(x + 17, 7,  "finally defeated");
    DrawTextLine(x + 17, 8,  "and flies away.");
    DrawTextLine(x + 17, 9,  "Suddenly, a door");
    DrawTextLine(x + 17, 10, "opens and Cosmo");
    DrawTextLine(x + 17, 11, "enters slowly.");
    DrawTextLine(x + 17, 13, "A big, scary blue");
    DrawTextLine(x + 17, 14, "alien creature");
    DrawTextLine(x + 17, 15, "wraps his arm");
    DrawTextLine(x + 17, 16, "around Cosmo...");
    FadeIn();
    WaitSpinner(x + 35, 21);
```

A complete frame is drawn (without any animation) through calls to {{< lookup/cref UnfoldTextFrame >}} and {{< lookup/cref DrawTextLine >}}. It displays as a unit when {{< lookup/cref FadeIn >}} fades it into view. {{< lookup/cref WaitSpinner >}} waits for the next key press.

```c
    FadeOut();

    x = UnfoldTextFrame(1, 22, 38, "", "Press ANY key.");
    DrawTextLine(x + 1, 16, "\xFB""019");
    /* Unbalanced dialog quotes preserved faithfully */
    DrawTextLine(x + 10, 3,  "\"Hi Cosmo,\" says the blue");
    DrawTextLine(x + 10, 4,  "alien, \"I'm Zonk,\" and");
    DrawTextLine(x + 10, 5,  "we've been looking all");
    DrawTextLine(x + 10, 6,  "over the planet for you\"");
    DrawTextLine(x + 10, 8,  "\"This is a very dangerous");
    DrawTextLine(x + 10, 9,  "planet, and when we found");
    DrawTextLine(x + 10, 10, "your parents, we brought");
    DrawTextLine(x + 10, 11, "them here for safety.\"");
    DrawTextLine(x + 10, 13, "\"We have been looking for");
    DrawTextLine(x + 10, 14, "you all this time, but");
    DrawTextLine(x + 10, 15, "it looks like you did a");
    DrawTextLine(x + 10, 16, "better job finding us!\"");
    DrawTextLine(x + 10, 18, "\"Here, I got a surprise");
    DrawTextLine(x + 10, 19, "for you...\"");
    FadeIn();
    WaitSpinner(x + 35, 21);
```

{{< lookup/cref FadeOut >}} hides the previous frame, and a new frame is drawn directly over it without clearing the screen. The rest of this frame works the same as the one that came before.

```c
    FadeOut();

    x = UnfoldTextFrame(1, 22, 38, "", "Press ANY key.");
    DrawTextLine(x + 27, 14, "\xFB""020");
    DrawTextLine(x + 2, 7,  "\"Mommy!  Daddy!\"");
    DrawTextLine(x + 2, 8,  "Cosmo and his parents");
    DrawTextLine(x + 2, 9,  "are finally reunited,");
    DrawTextLine(x + 2, 10, "and hugs are passed");
    DrawTextLine(x + 2, 11, "all around.");
    DrawTextLine(x + 2, 13, "Daddy explains that");
    DrawTextLine(x + 2, 14, "Zonk helped fix their");
    DrawTextLine(x + 2, 15, "ship, and they can");
    DrawTextLine(x + 2, 16, "resume their trip to");
    DrawTextLine(x + 2, 17, "Disney World.");
    FadeIn();
    WaitSpinner(x + 35, 21);

    FadeOut();

    x = UnfoldTextFrame(1, 22, 38, "", "Press ANY key.");
    DrawTextLine(x + 27, 19, "\xFB""003");
    DrawTextLine(x + 1,  10, "\xFB""011");
    DrawTextLine(x + 12, 6, "After saying goodbye");
    DrawTextLine(x + 12, 7, "to Zonk,");
    DrawTextLine(x + 1, 17, "Cosmo and his family");
    DrawTextLine(x + 1, 18, "blast off toward earth...");
    FadeIn();
    WaitSpinner(x + 35, 21);

    FadeOut();

    x = UnfoldTextFrame(1, 22, 38, "", "Press ANY key.");
    DrawTextLine(x + 13, 19, "\xFB""012");
    DrawTextLine(x + 2, 5, "    ...and arrive just four");
    DrawTextLine(x + 2, 6, "     galactic hours later!!");
    DrawTextLine(x + 2, 7, "Using their inviso-cloak device,");
    DrawTextLine(x + 2, 8, " they park their ship on top of");
    DrawTextLine(x + 2, 9, "        Space Mountain.");
    FadeIn();
    WaitSpinner(x + 35, 21);

    FadeOut();

    x = UnfoldTextFrame(1, 22, 38, "", "Press ANY key.");
    DrawTextLine(x + 12, 12, "\xFB""013");
    DrawTextLine(x + 2, 15, "  Disney World has always been");
    DrawTextLine(x + 2, 16, "    a great place for aliens");
    DrawTextLine(x + 2, 17, "  to visit on their vacations!");
    FadeIn();
    WaitSpinner(x + 35, 21);
```

Four more screens of dialog, all implemented the same as before.

```c
    DrawFullscreenImage(IMAGE_END);

    x = UnfoldTextFrame(0, 3, 24, "WEEEEEEEE!", "");
    StartSound(SND_WEEEEEEEE);
    WaitHard(200);
    StartMenuMusic(MUSIC_ZZTOP);
    WaitSpinner(x + 21, 1);
```

Similarly to the city image in episode two, this calls {{< lookup/cref DrawFullscreenImage >}} to draw {{< lookup/cref name="IMAGE" text="IMAGE_END" >}} (here an image of Cosmo on a roller coaster) and then draws a text frame on top of it with {{< lookup/cref UnfoldTextFrame >}}. Since this frame is only three tiles in height, and two of those tiles are used by the border, there is only room for one line of text -- the top text. The bottom text is an empty string, which causes no trouble.

{{< lookup/cref StartSound >}} queues {{< lookup/cref name="SND" text="SND_WEEEEEEEE" >}} for playback, and {{< lookup/cref WaitHard >}} pauses for 200 ticks -- a bit over one second -- which is long enough to allow most of the sound effect to play before execution continues. At that point, {{< lookup/cref StartMenuMusic >}} starts playing the {{< lookup/cref name="MUSIC" text="MUSIC_ZZTOP" >}} "main menu" song, and {{< lookup/cref WaitSpinner >}} waits for the next key press.

```c
    FadeWhiteCustom(4);

    x = UnfoldTextFrame(0, 5, 24, "Cosmo has the best", "The End!");
    DrawTextLine(x + 1, 2, "birthday of his life.");
    FadeIn();
    WaitHard(100);
    WaitSpinner(x + 21, 3);

    ShowCongratulations();
#endif
```

{{< lookup/cref FadeWhiteCustom >}} fades the screen to white one last time while {{< lookup/cref UnfoldTextFrame >}} and {{< lookup/cref DrawTextLine >}} do their work, then {{< lookup/cref FadeIn >}} makes it visible. {{< lookup/cref WaitHard >}} pauses for 100 ticks, then {{< lookup/cref WaitSpinner >}} allows the player to press a key to move on.

At the end of episode three (only), {{< lookup/cref ShowCongratulations >}} is called to show one more page of story.

### Common Epilogue

```c
    ShowOrderingInformation();
    ShowStarBonus();
}
```

At the end of all episodes, {{< lookup/cref ShowOrderingInformation >}} shows either ordering information (for episode one) or information about the registered version of the game (for episodes two and three). {{< lookup/cref ShowStarBonus >}} does one last tally of any stars collected in the final section of the game to ensure they are accurately reflected in the player's final score.

{{< boilerplate/function-cref ShowCongratulations >}}

The {{< lookup/cref ShowCongratulations >}} function shows a brief page of post-ending story and a pitch for another upcoming game.

{{< image src="congratulations-2052x.png"
    alt="Congratulations Dialog"
    1x="congratulations-684x.png"
    2x="congratulations-1368x.png"
    3x="congratulations-2052x.png" >}}

```c
void ShowCongratulations(void)
{
#ifdef END_GAME_CONGRATS
    word x;
```

This function's body is conditionally compiled into the executable based on the presence of the `END_GAME_CONGRATS` macro. In episodes without this message, the function exists but behaves as a no-op.

```c
    FadeOut();
    ClearScreen();
```

Any existing content on the screen is faded out via palette animation in {{< lookup/cref FadeOut >}}, and the screen memory is blanked with {{< lookup/cref ClearScreen >}}.

```c
    x = UnfoldTextFrame(0, 23, 38, "CONGRATULATIONS!", "Press ANY key.") + 2;
    DrawTextLine(x, 3,  "You saved Cosmo's parents and");
    DrawTextLine(x, 4,  "landed at Disney World for the");
    DrawTextLine(x, 5,  "best birthday of your life.");
    DrawTextLine(x, 7,  "After a great birthday on Earth,");
    DrawTextLine(x, 8,  "you headed home and told all of");
    DrawTextLine(x, 9,  "your friends about your amazing");
    DrawTextLine(x, 10, "adventure--no one believed you!");
    DrawTextLine(x, 12, "Maybe on your next adventure you");
    DrawTextLine(x, 13, "can take pictures!");
    DrawTextLine(x, 15, "Coming Dec. 92: Duke Nukum II --");
    DrawTextLine(x, 16, "The amazing sequel to the first");
    DrawTextLine(x, 17, "Nukum trilogy, in which Duke is");
    DrawTextLine(x, 18, "kidnapped by an alien race to");
    DrawTextLine(x, 19, "save them from termination...");
    FadeInCustom(1);
    WaitSpinner(x + 33, 21);
#endif
}
```

The dialog is constructed out of view with calls to {{< lookup/cref UnfoldTextFrame >}} and {{< lookup/cref DrawTextLine >}}. Once the dialog has been fully drawn, {{< lookup/cref FadeInCustom >}} fades it into view using a rather quick speed setting of 1.

{{< aside class="fun-fact" >}}
**Better late than never.**

Duke Nukem &#8545; ended up being released a year later than the advertised date here. The story also changed somewhat -- rather than _saving_ the alien race, he ended up _conquering_ them to save Earth from enslavement.

The canonical spelling of "Nukem" also changed from "Nukum" by the release date as well.
{{< /aside >}}

{{< lookup/cref WaitSpinner >}} blocks until a key is pressed, then this dialog's function returns.
