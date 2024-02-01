+++
title = "The apogee Parameter"
description = "What happens when you run the game with the `apogee` parameter, as so many cheat sites suggest."
weight = 490
+++

# The `apogee` Parameter

{{< table-of-contents >}}

Many online cheat guides (a notable example being 3D Realms[^3drealms] themselves) refer to a special cheat mode where running the game with `apogee` as a command line argument will unlock a special mode of operation. It doesn't. Providing `apogee` (or anything that doesn't resolve to a valid directory) as the [write path]({{< relref "main-and-outer-loop#write-path" >}}) makes it so that the game cannot load or save its configuration or save files, and this results in strange behavior:

> The effects of this are many. One, the game will not recognize your old high scores or saved games. (The high scores will be reset to those of Simpsons' characters until you exit and re-enter the program normally.) In this mode, if you die quickly enough after entering a level, you'll be invincible from then on, to everything but pits on the bottom of each level.
>
> -- http://legacy.3drealms.com/cheat/cosmo.html

For [configuration files]({{< relref "configuration-file-format" >}}), it doesn't matter so much -- the game is designed to handle the case where the file is missing. This is where the default values in the high score table come from.

For [saved games]({{< relref "save-file-format" >}}), the behavior is also predictable. No games can be loaded, because no files exist in the invalid directory. Save attempts fail silently. One of the stranger side effects of this condition is that it's relatively easy for the player to become invincible by dying during gameplay. This is caused by the interaction of a few different components of the game.

## Unintended Invincibility

When a new level is entered ({{< lookup/cref InitializeLevel >}}), a temporary save file named `COSMOx.SVT` is written which contains the game state at that point. When the player dies and the level needs to be restarted ({{< lookup/cref DrawPlayerHelper >}}), this save file is reloaded to return the player's score, stars, health, and so on back to the state they were in when the level was originally entered. If the save directory is not writable, this file is never written.

While the game is running, the player's health is tracked in the {{< lookup/cref playerHealth >}} variable that decrements when damage is taken and increments when {{< lookup/actor type=28 strip=true plural=true >}} are collected. When health drops to zero the player dies, but this check only happens at the instant the player is taking damage ({{< lookup/cref HurtPlayer >}}).

Once the player takes enough damage to drop their health to zero (falling off the bottom of the map does not count) the level restarts. A {{< lookup/cref LoadGameState >}} call is attempted on the `COSMOx.SVT` save file to reset the game state, but its {{< lookup/cref fopen >}} call returns a null pointer due to the file having never been written in the first place. {{< lookup/cref LoadGameState >}} does detect this condition, but simply returns early without resetting any of the save game variables.

As a result, the level is restarted with the player health value still at zero. The game is fully playable in this state. The "HEALTH" area of the status bar uses {{< lookup/cref name="playerHealth" text="playerHealth - 1" >}} to determine how many bars to draw, and since this particular variable is an unsigned 16-bit value which wraps around zero, the player effectively has 65,535 filled bars of health. Similar wraparound occurs in {{< lookup/cref HurtPlayer >}} as the player takes damage from enemies -- the player is actually taking damage, but the amount of health available is now so preposterously high they will practically never die.

## Other Observable Effects

When invoked, this quirk briefly desynchronizes demo playback during episode three, after the player first dies on map 6. Playback eventually corrects itself once the demo advances to map 9.

Another potentially interesting side-effect of playing without a `COSMOx.SVT` file comes as the result of the score/stars values not resetting during level restarts. If one were to continually replay the same levels, but fall off the bottom of the map instead of exiting to the next level, it's quite possible to amass so many stars that it overflows the two-digit "STARS" space in the status bar. Conceivably the same thing could happen to the score as well, given enough dedication.

[^3drealms]: http://legacy.3drealms.com/cheat/cosmo.html
