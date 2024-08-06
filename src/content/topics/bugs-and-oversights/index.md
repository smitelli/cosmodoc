+++
title = "Bugs and Oversights"
description = "A listing of all the bugs, quirks, mistakes, and edge cases I discovered during my research."
weight = 600
+++

# Bugs and Oversights

For all the time and attention paid to the game by its developers and testers, there were many errors that were left unfixed in the final version. The majority of them are relatively minor and do not diminish the overall experience of playing. Some of the issues are downright trivial.

This is the listing of every oversight I discovered during the course of my research.

## Player cannot fall off the map in E2M6.

When the player falls into a bottomless pit, their position overflows the map data buffer and wraps back to zero due to the large size of the maps. Due to the unusual construction of this map in particular, [the player can stand on solid tiles near the top of the map while simultaneously falling out the bottom of it.]({{< relref "player-movement-functions#dancing-on-the-ceiling" >}})

## E2M10 can be won by dying near the top of the map.

<!-- TODO Continue describing bugs -->

## Joystick buttons are reversed.

## Player can walk out of a closed {{< lookup/actor 162 >}} if using the joystick.

## The `apogee` Parameter

This quirk has [its own page]({{< relref "apogee-parameter" >}}).

## Cheat code can be reapplied by abusing the save game function.

## Cheats interfere with demo playback and recording.

## AdLib hardware is not shut down when EGA card is missing.

## Presence of a {{< lookup/actor 152 >}} prevents the 50,000 point barrel bonus from being earned.

## {{< lookup/actor 189 >}} spawns Floating Score effect, but no points are given.

## Pressing <kbd>F11</kbd> in main menu (without debug mode) clears and redraws the screen.

## {{< lookup/actor 106 >}} reads west tile attribute instead of north when considering a flip.

## {{< lookup/actor type=95 strip=true plural=true >}} at west edge of map disregard the player.

## Rain spawns one tile lower in the game window than it should.

## Certain shards have a tendency to enter and then hop up walls.

## Off-screen {{< lookup/actor type=47 plural=true >}} can make sound.

## Certain decorations can disappear prematurely near the left or bottom screen edges.

The sprite visibility check in {{< lookup/cref MoveAndDrawDecorations >}} calculates sprite dimensions incorrectly, [causing certain decorations to expire while still partially on the screen.]({{< relref "decoration-functions#sprite-visibility-bug" >}})

## `.SVT` file is not deleted if the write path was overridden.

## {{< lookup/actor 102 >}} floor/wall impact sounds are preempted.

## Fountain stream overlaps bottom of spray sprite.

## {{< lookup/actor type=59 strip=true plural=true >}} flash a white line for one frame after their initial movement.

This is investigated in detail on the [actor implementation page]({{< relref "foot-switches#visual-construction" >}}) for the switches.

## Scooter is invisible for one frame after touching bottom edge of the screen.

## Sparkly prizes are drawn flipped.

## {{< lookup/actor 62 >}} on E2M5 doesn't sparkle.

## Two unused actors in E1M8.

Both are map actor type 22. First is at position 62, 63 and the second is at position 61, 64. They are ignored when loading the map.

## Sound/music toggle dialog message is truncated.

## Certain star bonus tally superlatives never appear.

## Some actor types never appear in any maps.

The full details are on [a separate page]({{< relref "unused-actors" >}}).

## Some backdrop names are defined but never used.

## {{< lookup/actor 48 >}} has inconsistent bomb damage behavior.

## Inconsistent east/west behavior after bomb hint dialog is displayed.

## Wait spinner placement is inconsistent in Cosmo/Duke conversation.

## Hitch block in E1M5 at 19, 101.
