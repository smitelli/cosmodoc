+++
title = "Demo Format"
description = "An analysis of the demo file format and the procedure for creating it."
weight = 190
+++

# Demo Format

{{< table-of-contents >}}

If the game receives no input after showing the title sequence for about 25 seconds, or if the user explicitly requests it via the main menu, a demo begins playing. This demo ships with the game in a [group file]({{< relref "group-file-format" >}}) entry named PREVDEMO.MNI. This name is used regardless of the episode being played, and this is the only case across all group files where data from different episodes is stored with conflicting names.

New demos can be recorded by entering debug mode and using the correct key combinations, although the experience is a bit spartan.

{{% aside class="speculation" %}}
**... prevised demo?**

The name "PREVDEMO" might be a holdover from Duke Nukem 1, where the demo playback option in the main menu was titled "Previews/Main Demo!"

It _could_ also simply mean "previous demo."
{{% /aside %}}

## File Contents

The demo file begins with a single little-endian word which specifies the number of bytes in the demo stream. After that, there is one byte per frame of gameplay. Each byte encodes the pressed/released state of all six input keys (left, right, up, down, jump, bomb) plus one additional flag to indicate if the current level should end. The byte packing is as follows:

Bit Position              | Description
--------------------------|------------
0 (least significant bit) | "Walk left" key state. `0` = key is not pressed, `1` = key is pressed.
1                         | "Walk right" key state. `0` = key is not pressed, `1` = key is pressed.
2                         | "Look up" key state. `0` = key is not pressed, `1` = key is pressed.
3                         | "Look down" key state. `0` = key is not pressed, `1` = key is pressed.
4                         | "Jump" key state. `0` = key is not pressed, `1` = key is pressed.
5                         | "Drop bomb" key state. `0` = key is not pressed, `1` = key is pressed.
6                         | Controls progression to the next level. `0` = normal play, `1` = win current level and move to the next one.
7 (most significant bit)  | Unused; always `0`.

The level progression during demo recording and playback is hard-coded into the game and is the same across all three episodes. The sequence is:

1. Level 0 (map 1)
2. Level 13 (map 8)
3. Level 5 (map 4)
4. Level 9 (map 6)
5. Level 16 (map 9)

Levels can be advanced in the usual way by interacting with an "end level" actor, or they can be forced to end early based on bit 6 in any demo byte. Demo playback stops entirely once the end of the demo data is reached.

{{% aside class="fun-fact" %}}
**It keeps going, and going, and going...**

Just as when playing the game normally, player variables like score, health, bombs, and stars do not reset when the demo level changes. If the player dies during a demo, that level restarts with the same player state that existed when the level was first entered.
{{% /aside %}}

## Recording Demos

The game supports recording demos without any special modification. To record a demo, a few things need to happen:

1. Begin a new game or restore a saved game.
2. Enable debug mode by pressing <kbd>Tab</kbd> + <kbd>Del</kbd> + <kbd>F12</kbd>.
3. Quit the game and return to the main menu.
4. Press <kbd>F11</kbd>.

If the steps were performed correctly, a new game will begin on level 0 (map 1) with a "DEMO" overlay message in the center top of the screen. Play the game normally and all movements will be recorded. A few things will be different:

* The "Now entering level..." screen will not display when entering any levels.
* The high score table will not display when the game is exited.
* Help text for bombs, pouncing, and power-ups will never display.
* Hint Globes will not auto-activate when touched. (However, they can still be activated manually via use of the "look up" key.)

{{% note %}}
Do not activate Hint Globes while recording a demo! If a Hint Globe is activated while the demo is being played back later, the game will pause indefinitely waiting for keyboard input to dismiss the message. Quickly striking any key will dismiss the Hint Globe message and resume demo playback. A longer keypress will dismiss the message _and then_ exit the demo entirely.

Cheat codes and debug keys work while recording a demo, but their effects are not stored in the recorded data. This could lead to desynchronization during playback.
{{% /note %}}

To move to the next level, either find and use the normal level exit or press the <kbd>X</kbd> key. The game will advance to the next level in the demo progression -- _not_ the usual next level. Once level 16 (map 9) is reached, there are no further levels defined in the sequence. Any attempt to finish level 16 will result in the level simply starting over again. At this point the game must be exited via Esc, Q, or the F1 menu.

When the game ends and the title screen is shown, demo recording stops and a new file named PREVDEMO.MNI is created in the current working directory. If a file of this name already exists, it is silently overwritten.

The maximum supported demo size is 4,999 bytes (5,001 bytes if the header is counted), which works out to a little over seven minutes and 40 seconds of uninterrupted gameplay. Once a demo reaches this size, the game and its recording will automatically end.

## Playing Recorded Demos

Since a PREVDEMO.MNI entry always exists in the group files, the original demo will always take precedence over any loose files on the disk. To use a new PREVDEMO.MNI file instead, the group file would need to be modified to remove, hide, or replace the original demo entry.

As an alternative, it is also possible to extract _all_ the entries from the group files into the game's directory, then rename/remove the group files so they are no longer accessible. The game will then fall back to searching for group file entries using filenames on disk. With this setup, a new demo can be played back immediately after recording has finished, without even exiting the game.
