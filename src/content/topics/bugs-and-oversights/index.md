+++
title = "Bugs and Oversights"
description = "A listing of all the bugs, quirks, mistakes, and edge cases I discovered during my research."
weight = 420
+++

# Bugs and Oversights

For all the time and attention paid to the game by its developers and testers, there were many errors that were left unfixed in the final version. The majority of them are relatively minor and do not diminish the overall experience of playing. Some of the issues are downright trivial.

This is the listing of every oversight I discovered during the course of my research.

{{< table-of-contents >}}

## Player cannot fall off the map in E2L6.

## E2L10 can be won by dying near the top of the map.

## Joystick buttons are reversed.

## The `apogee` Parameter

This quirk has [its own page]({{< relref "apogee-parameter" >}}).

## Cheat code can be reapplied by abusing the save game function.

## Cheats interfere with demo playback and recording.

## AdLib hardware is not shut down when EGA card is missing.

## {{< lookup/actor 189 >}} spawns Floating Score effect, but no points are given.

## Pressing <kbd>F11</kbd> in main menu (without debug mode) clears and redraws the screen.

## {{< lookup/actor 106 >}} reads west tile attribute instead of north when considering a flip.

## {{< lookup/actor type=95 strip=true plural=true >}} at west edge of map disregard the player.

## Off-screen {{< lookup/actor type=47 plural=true >}} can make sound.

## `.SVT` file is not deleted if the write path was overridden.

## {{< lookup/actor 102 >}} floor/wall impact sounds are preempted.

## Sparkly prizes are drawn flipped

## Two unused actors in E1L8

Both are map actor type 22. First is at position 62, 63 and the second is at position 61, 64. They are ignored when loading the map.

## Sound/music toggle dialog message is truncated.

## Certain star bonus tally superlatives never appear.

## Some actor types never appear in any maps.

The full details are on [a separate page]({{< relref "unused-actors" >}}).

## Some backdrop names are defined but never used.

## {{< lookup/actor 48 >}} has inconsistent bomb damage behavior.

## Inconsistent east/west behavior after bomb hint dialog is displayed.

## Wait spinner placement is inconsistent in Cosmo/Duke conversation.

## Hitch block in E1L5 at 19, 101
