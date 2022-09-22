+++
title = "Unused Actors"
description = "A list of defined actor types that never appear in the game."
weight = 390
+++

# Unused Actors

There are a number of actor types that the game accepts and appears to implement (to varying degrees), but for whatever reason they do not appear in any of the original map files or as in-game spawners.

{{< table-of-contents >}}

## Completely Unused

There does not appear to be a way to get any of these actor types to occur naturally in an unmodified copy of the game.

Actor Type | Description              | Usability  | Notes
-----------|--------------------------|------------|------
0          | {{< lookup/actor 0 >}}   | Weird      | The implementation suggests that this should spawn another actor of type 0, in essence yielding a fresh copy of itself. Instead it does nothing because spawner type 0 is used to mark a spawner slot as being "dead," therefore it never runs to the point where a new actor is created.
22         | {{< lookup/actor 22 >}}  | Functional | Works like {{< lookup/actor 20 >}}.
40         | {{< lookup/actor 40 >}}  | Functional | Works like {{< lookup/actor 41 >}}, but remains stationary in the _retracted_ position.
53         | {{< lookup/actor 53 >}}  | Functional | Basket is not used, although its contents -- {{< lookup/actor 136 >}} -- are.
58         | {{< lookup/actor 58 >}}  | Buggy      | Correctly spawns a {{< lookup/actor 2 >}}. The spawn animation generally always ends with the object off the top edge of the screen, so the resulting actor is created out of view. Because {{< lookup/actor type="2" strip="1" >}} actors do not have the "always active" flag set, gravity does not affect the off-screen actor and it does not fall back to the floor. If it scrolls into view later, it will begin falling to the floor then. After that, the new {{< lookup/actor type="2" strip="1" >}} works as expected.
84         | {{< lookup/actor 84 >}}  | Functional | Works like its floor mounted counterpart.
93         | {{< lookup/actor 93 >}}  | Functional | Basket is not used, although its contents -- {{< lookup/actor 94 >}} -- are.
100        | {{< lookup/actor 100 >}} | Functional | Barrel is not used, nor are its contents -- {{< lookup/actor 251 >}}.
116        | {{< lookup/actor 116 >}} | Functional | Basket is not used, although its contents -- {{< lookup/actor 139 >}} -- are.
142        | {{< lookup/actor 142 >}} | Functional | Barrel is not used, although its contents -- {{< lookup/actor 134 >}} -- are.
171        | {{< lookup/actor 171 >}} | Functional | Basket is not used, although its contents -- {{< lookup/actor 172 >}} -- are.
183        | {{< lookup/actor 183 >}} | Functional | Works like all other Floating Scores. Although there are a handful of actor types that award 6,400 points when bombed, none of them create a Floating Score.
251        | {{< lookup/actor 251 >}} | Buggy      | Works like {{< lookup/actor 25 >}}, however the "always active" flag is set. This is appropriate when hidden inside a Barrel, but probably not for direct inclusion in a map -- the actor will continually hop towards the player's location until it either gets stuck in a corner or falls off the map long before the player encounters the location where it was originally placed.
256        | {{< lookup/actor 256 >}} | Buggy      | None of the episodes implement {{< lookup/actor 256 >}}. When the player touches any unimplemented Hint Globe, the notification sound plays, gameplay pauses for a short time, no text window is displayed and then gameplay resumes.
257        | {{< lookup/actor 257 >}} | Buggy      | None of the episodes implement {{< lookup/actor 257 >}}.
258        | {{< lookup/actor 258 >}} | Buggy      | None of the episodes implement {{< lookup/actor 258 >}}.
259        | {{< lookup/actor 259 >}} | Buggy      | None of the episodes implement {{< lookup/actor 259 >}}.
260        | {{< lookup/actor 260 >}} | Buggy      | None of the episodes implement {{< lookup/actor 260 >}}.
261        | {{< lookup/actor 261 >}} | Buggy      | None of the episodes implement {{< lookup/actor 261 >}}.
262        | {{< lookup/actor 262 >}} | Buggy      | None of the episodes implement {{< lookup/actor 262 >}}.

## Only Appear in Barrels/Baskets

These actor types _can_ appear in the game as the result of destroying a Barrel or Basket, but never directly appear in any of the original map files.

Actor Type | Description
-----------|------------
38         | {{< lookup/actor 38 >}}
140        | {{< lookup/actor 140 >}}
153        | {{< lookup/actor 153 >}}
226        | {{< lookup/actor 226 >}}
229        | {{< lookup/actor 229 >}}
232        | {{< lookup/actor 232 >}}
