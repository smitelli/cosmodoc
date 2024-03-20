+++
title = "Platform Functions"
description = "Describes the functions that maintain the platforms and mud fountains in the game."
weight = 520
+++

# Platform Functions

This game has two types of moving platform that are implemented separately from the actors that the player typically encounters. These are **{{< lookup/special-actor type=1 plural=1 >}}** and **{{< lookup/special-actor type=2 strip=1 plural=1 >}}**. As each of these platforms move, they modify the map data in memory and reposition solid tiles. In the case of the fountains, additional sprite images are drawn to obscure these map tiles.

Both platforms and mud fountains are initialized during map loading by {{< lookup/cref NewMapActorAtIndex >}}.

{{< table-of-contents >}}

## Platform Behavior

Each platform is defined in the actor section of the [map data]({{< relref "map-format" >}}). This sets the initial X/Y position of each platform, but does not provide any means to direct the movement. To support that, each platform's path is defined by a series of invisible map tiles in the map data. While tile index 0 is simply rendered as air, tile indices 1--8 are rendered as air _and_ determine the next movement step of any platform that touches that tile.

A reasonable platform path will be constructed as a loop that returns the platform back to its starting position to repeat again. There's no technical reason why the path must be a closed loop, except that such platforms will stop once they reach the end of the path and remain stuck in that position indefinitely -- there is no way to make a platform reverse itself. The only way to support a platform path that crosses itself (or any other platform's path) would be to have both directions cross at a right angle in a diagonal orientation -- think of a figure-eight pattern.

{{< image src="platform-paths-2052x.png"
    alt="Diagram of a few different platform path arrangements and their behavior."
    1x="platform-paths-684x.png"
    2x="platform-paths-1368x.png"
    3x="platform-paths-2052x.png" >}}

A platform is a 5 &times; 1 span of blue solid map tiles that can be jumped through and stood on. Its X/Y position is anchored relative to the center tile of the platform (this is different from the way most other objects in the game are anchored). The platform is constructed of true map blocks; there are no sprites drawn to support them.

{{% note %}}The game code makes some firm assumptions that every platform will always be centered on either a path direction tile or air (tile zero). Allowing a platform to run into arbitrary solid or masked tiles will make {{< lookup/cref MovePlatforms >}} read outside of an array, leading to unpredictable and likely violent platform movement.{{% /note %}}

Platform movement is governed by the global {{< lookup/cref arePlatformsActive >}} variable, which is usually true. If the map contains at least one {{< lookup/actor 59 >}}, {{< lookup/cref arePlatformsActive >}} becomes false until the switch is activated.

## Mud Fountain Behavior

Like platforms, each mud fountain is defined in the actor section of the map data, but there is no corresponding path data in the map tiles. Instead, fountains are anchored at their starting position and move up and down by a fixed amount depending on the actor type. There are four fountain types with heights from six to 15 tiles high:

* {{< lookup/special-actor 2 >}}
* {{< lookup/special-actor 3 >}}
* {{< lookup/special-actor 4 >}}
* {{< lookup/special-actor 5 >}}

Fountains also modify the map data as they move, placing a pair of solid map tiles at the locations where the mud reaches peak height and dissipates in a "spray" pattern. On top of these map tiles, and some distance below, sprite tiles are drawn to make the mud visible.

## Player Interaction

For both platforms and mud fountains, the player's X and Y position must be adjusted to keep the player moving along with the platform. Without this, the platform would slide right past the stationary player until they fell off. Platforms can also knock the player off of a wall they might be clinging to.

Once the player steps off the platform, the modifications to their position cease and the platform continues along without them.

Mud fountains can injure the player if they walk into the stream. Only the top surface of the fountain's spray pattern can be safely touched.

{{< boilerplate/function-cref MovePlatforms >}}

The {{< lookup/cref MovePlatforms >}} function iterates through each platform defined on the current map and adjusts their position by one tile. If the player is standing on one of the platforms, their position will be adjusted in the process. This is intended to be called once per frame (or **tick**) of gameplay. If {{< lookup/cref arePlatformsActive >}} has a false value, this function will perform all of its usual processing steps but none of the platforms will move from their current position.

Because platforms are placed in the world by literally overwriting the map data, provisions need to be made to allow the game to restore the old content of the map once the platform moves away. This data is saved in a five-word `mapstash[]` array attached to each platform in memory.

When trying to make sense of the loops here, bear in mind that each platform is five tiles wide. Each "`x`" loop simply iterates over five tiles horizontally, but uses weird initial offsets and subtractions to get the tile number. The reason for this is because, apparently, the original game cast the entire {{< lookup/cref Platform >}} structure to a `word` pointer and used fixed offsets to access `mapstash[]` to save and restore map tile data. This wasn't really a terribly safe thing to do in 1992, and it remains unsafe today.

```c
void MovePlatforms(void)
{
    register word i;

    for (i = 0; i < numPlatforms; i++) {
        register word x;
        Platform *plat = platforms + i;
        word newdir;
```

The outermost `for` loop runs once for each platform defined by the map, up to {{< lookup/cref numPlatforms >}}. Within the loop, `plat` points to the {{< lookup/cref Platform >}} structure from the {{< lookup/cref platforms >}} array that's currently being processed. `x` is a horizontal iterator value, and `newdir` will hold the direction that the platform moves during this tick.

```c
        for (x = 2; x < 7; x++) {
            SetMapTile(*((word *)plat + x), plat->x + x - 4, plat->y);
        }
```

When this function was entered, the five-element `plat->mapstash[]` array held the map tiles that were previously at the platform's current position, which the platform had replaced. This loop restores those tiles back to the map data, erasing the platform's tiles from the game world.

As called out above, this is done by casting `plat` to a word pointer and then reading offsets 2 through 6, inclusive. As the Borland compiler packed the {{< lookup/cref Platform >}} structure, the words at these positions are the elements of the `mapstash[]` array. Each tile read from `mapstash[]` is passed as the first argument to a {{< lookup/cref SetMapTile >}} call. The second argument is the platform's current `x` position (which, remember, is its center tile) plus the `x` iterator (which, also remember, starts at 2) all minus 4 to offset the fact that neither of the other two variables starts at zero. The `y` argument is much saner, owing to the fact that the platform only occupies a single tile vertically.

```c
        newdir = GetMapTile(plat->x, plat->y) / 8;
```

The center map tile at the current (old) location of the platform controls where it moves next. This is read via {{< lookup/cref GetMapTile >}}, passing `plat->x` and `plat->y` as the arguments. Solid map tile values are indexed in steps of eight (see ["solid tiles" in the map format]({{< relref "map-format#solid-tiles" >}})), thus the division scales the values down. With this scaling, `newdir` should have one of the following values:

`newdir` | Description
---------|------------
0        | Halt indefinitely.
1        | Move north during the next tick.
2        | Move northeast during the next tick.
3        | Move east during the next tick.
4        | Move southeast during the next tick.
5        | Move south during the next tick.
6        | Move southwest during the next tick.
7        | Move west during the next tick.
8        | Move northwest during the next tick.

In essence, the map data encodes one of the values that the {{< lookup/cref DIR8 >}} constants represent. No checks are performed to ensure that `newdir` is confined to the values listed here, but on a well-formed map it always should be.

```c
        if (
            playerDeadTime == 0 && plat->y - 1 == playerY &&
            arePlatformsActive
        ) {
            MovePlayerPlatform(plat->x - 2, plat->x + 2, newdir, newdir);
        }
```

If the player is alive ({{< lookup/cref playerDeadTime >}} is zero), and they are at the correct vertical position to be plausibly standing on this platform, and {{< lookup/cref arePlatformsActive >}} is true, additional processing _may_ need to be done to move the player along with the platform.

The position check here is extremely rudimentary: It passes when {{< lookup/cref playerY >}} (the tile row containing the player's feet) equals the platform's Y position minus one (the tile row containing the empty space directly above the platform). The player and the platform could be separated by a huge distance horizontally -- that gets tested later.

When all the conditions match, {{< lookup/cref MovePlayerPlatform >}} is called to determine what action to take, if any, and adjust the player's position accordingly. The first two arguments are the leftmost and rightmost X positions that the platform occupies. As this platform is five tiles wide and `plat->x` represents its center, the extents of the platform are -2 and +2 tiles away. The remaining two arguments are the movement directions in `newdir`, split into horizontal and vertical components in a way that doesn't seem to have much justification.

When {{< lookup/cref MovePlayerPlatform >}} returns, the player is in the position where the platform is going to be once this function runs to completion.

```c
        if (arePlatformsActive) {
            plat->x += dir8X[newdir];
            plat->y += dir8Y[newdir];
        }
```

Provided {{< lookup/cref arePlatformsActive >}} is true, the platforms can now move. `newdir` is used as an index into the {{< lookup/cref dir8X >}} and {{< lookup/cref dir8Y >}} arrays, yielding a value of either -1, 0, or 1 for each axis of movement. These values are added to `plat->x` and `plat->y`, respectively, to move the platform along both dimensions.

```c
        for (x = 2; x < 7; x++) {
            *((word *)plat + x) = GetMapTile(plat->x + x - 4, plat->y);
        }
```

The map tiles at the new position need to be stashed, similar to the earlier loop. Here {{< lookup/cref GetMapTile >}} reads the existing data and it is stored into `mapstash[]` by casting the {{< lookup/cref Platform >}} structure to a word pointer. All of the offsets and iterators work as described above.

```c
        for (x = 2; x < 7; x++) {
            SetMapTile(
                TILE_BLUE_PLATFORM + ((x - 2) * 8), plat->x + x - 4, plat->y
            );
        }
    }
}
```

Finally, the platform needs to be redrawn in its new position. The solid tile that represents the platform is {{< lookup/cref name="TILE" text="TILE_BLUE_PLATFORM" >}} and the four tiles that follow it sequentially, each source tile address starting at a multiple of eight. These tiles are drawn at the platform's X position, starting two tiles to the left and continuing to cover two tiles to the right.

The `for` loop here takes `x` through the same biased values that all the other loops did, even though nothing here is accessing `mapstash[]`. With appropriate subtraction, the {{< lookup/cref SetMapTile >}} receives the values it needs to draw the platform in its new spot.

The outermost `for` loop continues until all of the map's platforms have been serviced, then this function returns.

{{< boilerplate/function-cref MoveFountains >}}

The {{< lookup/cref MoveFountains >}} function iterates through each mud fountain defined on the current map and adjusts their position by one tile. If the player is standing on one of the fountains, their position will be adjusted in the process. This is intended to be called once per frame (or **tick**) of gameplay.

Each fountain starts at a minimum height, growing in the north direction. During each frame of gameplay, the fountain's height grows and its **step count** is incremented. Once the step count reaches a predefined maximum, the fountain switches direction and begins to shrink back to minimum height, incrementing the step count in the same manner as before. Different fountains reach different maximum step counts based on the actor type encoded in the map data.

When a fountain reaches its maximum or minimum height, it pauses for a ten frame delay before switching direction.

Fountains behave similarly to platforms, by modifying the map data in place to insert and remove tiles that the player (and other actors) stand on. Unlike platforms, fountains do not follow a path in the map data and only move up and down from the spot where the map author placed them. Fountains also do not preserve the old value of any map tiles they move past -- every tile a fountain passes over gets erased to {{< lookup/cref name="TILE" text="TILE_EMPTY" >}}.

```c
void MoveFountains(void)
{
    word i;

    for (i = 0; i < numFountains; i++) {
        Fountain *fnt = fountains + i;
```
The outermost `for` loop runs once for each fountain defined by the map, up to {{< lookup/cref numFountains >}}. Within the loop, `fnt` points to the {{< lookup/cref Fountain >}} structure from the {{< lookup/cref fountains >}} array that's currently being processed.

```c
        if (fnt->delayleft != 0) {
            fnt->delayleft--;
            continue;
        }
```

Each fountain independently tracks its direction-change delay using the `fnt->delayleft` counter. If it holds a nonzero value, the fountain is paused for this frame and does not move. `delayleft` is decremented and the outer loop continues on to the next fountain on the map.

If the fountain is not currently delayed, execution moves on to the following block.

```c
        fnt->stepcount++;

        if (fnt->stepcount == fnt->stepmax) {
            fnt->stepcount = 0;
            fnt->dir = !fnt->dir;
            fnt->delayleft = 10;
            continue;
        }
```

`fnt->stepcount` is incremented each time the fountain moves. At each step, its value is compared against `fnt->stepmax` and, if they become equal, the fountain has reached the maximum number of steps it is allowed and a direction change is required.

To change direction, `stepcount` is zeroed to permit the fountain to travel back the same number of tiles again. `fnt->dir` is negated, exploiting a useful property of the {{< lookup/cref DIR4 >}} values -- the code can ping-pong between north and south, since they are represented by zero and one respectively. `fnt->delayleft` is set to 10, which will pause the fountain's movement for the next ten frames.

Having set up the direction change, the outer loop `continue`s to the next fountain without further movement to the current one.

In the more typical case where a direction change did not occur, execution proceeds:

```c
        SetMapTile(TILE_EMPTY, fnt->x,     fnt->y);
        SetMapTile(TILE_EMPTY, fnt->x + 2, fnt->y);
```
The fountain is moving away from the position at `fnt->y` to a new position one tile above or below it. To prepare for this, the tile at (`fnt->x`, `fnt->y`) is set to {{< lookup/cref name="TILE" text="TILE_EMPTY" >}} using a call to {{< lookup/cref SetMapTile >}}. The position two tiles to the right is also cleared the same way.

These two tile positions are the left and right edges of the top of the fountain's "spray" pattern. The game exploits the fact that pretty much everything in the game is too large to slip through the space between these two tiles, so it's not necessary to create a solid uninterrupted map structure here. Two tiles at the top corners of the fountain's bounding box is sufficient.

```c
        if (playerDeadTime == 0 && fnt->y - 1 == playerY) {
            if (fnt->dir != DIR4_NORTH) {
                MovePlayerPlatform(
                    fnt->x, fnt->x + 2, DIR8_NONE, DIR8_SOUTH
                );
            } else {
                MovePlayerPlatform(
                    fnt->x, fnt->x + 2, DIR8_NONE, DIR8_NORTH
                );
            }
        }
```

If the player is alive ({{< lookup/cref playerDeadTime >}} is zero), and they are at the correct vertical position to be plausibly standing on this fountain, additional processing _may_ need to be done to move the player along with the fountain.

The position check here is extremely rudimentary: It passes when {{< lookup/cref playerY >}} (the tile row containing the player's feet) equals the fountain's Y position minus one (the tile row containing the empty space directly above the fountain's spray). The player and the fountain could be separated by a huge distance horizontally -- that gets tested later.

If the player is in the correct position and the fountain's movement direction (`fnt->dir`) is not {{< lookup/cref name="DIR4" text="DIR4_NORTH" >}} (so, south) then {{< lookup/cref MovePlayerPlatform >}} is called with the fountain's X extents in the first two arguments. This provides the leftmost and rightmost tile positions that this fountain affects. The remaining arguments are the direction components: {{< lookup/cref name="DIR8" text="DIR8_NONE" >}} in the horizontal direction and {{< lookup/cref name="DIR8" text="DIR8_SOUTH" >}} in the vertical.

In the `else` case, the fountain is moving north and the call to {{< lookup/cref MovePlayerPlatform >}} is the same except for {{< lookup/cref name="DIR8" text="DIR8_NORTH" >}} as the vertical direction argument.

{{% aside class="armchair-engineer" %}}
**A good sense of indirection.**

There's really no place where the separation of the two direction components in {{< lookup/cref MovePlayerPlatform >}} makes sense. It feels like this code was originally implemented in a different way that genuinely required the separation to coexist with the platforms. That's no longer the case in the current implementation, but it remains.

Similarly, the use of {{< lookup/cref name="DIR4" text="DIR4_NORTH/SOUTH" >}} constants instead of the more constrained {{< lookup/cref name="DIR2" text="DIR2_NORTH/SOUTH" >}} is a consequence of the two systems having a reversed sense of north vs. south.
{{% /aside %}}

Whichever branch is taken, the player's Y position is adjusted to move them into the position where the fountain is going to be.

```c
        if (fnt->dir != DIR4_NORTH) {
            fnt->y++;
            fnt->height--;
        } else {
            fnt->y--;
            fnt->height++;
        }
```

This performs the actual movement of the fountain. When the fountain's movement direction (`fnt->dir`) is not {{< lookup/cref name="DIR4" text="DIR4_NORTH" >}} (again, south) the fountain is descending back into the ground. `fnt->y` increments to move the top of the spray down, and `fnt->height` decrements to make the overall fountain shorter.

The `else` case is exactly the opposite, rising northward on the screen and growing in height.

```c
        SetMapTile(TILE_INVISIBLE_PLATFORM, fnt->x,     fnt->y);
        SetMapTile(TILE_INVISIBLE_PLATFORM, fnt->x + 2, fnt->y);
    }
}
```

Finally, {{< lookup/cref SetMapTile >}} is called twice to reinsert the map tiles that form the fountain spray's bounding box. These tiles are {{< lookup/cref name="TILE" text="TILE_INVISIBLE_PLATFORM" >}} placed at (`fnt->x`, `fnt->y`) and the position two tiles to the right. Together these produce a new solid construction that the player and other actors can stand on. These tiles are _not_ visible; {{< lookup/cref DrawFountains >}} is responsible for drawing each fountain's sprite tiles.

The outermost `for` loop continues until all of the map's fountains have been serviced, then this function returns.

{{< boilerplate/function-cref DrawFountains >}}

The {{< lookup/cref DrawFountains >}} function iterates through every mud fountain active on the map and draws the sprites that they are built from. If the player is touching any part of the stream beneath the spray at the top of the fountain, damage is inflicted on the player. This function is called once per frame of gameplay.

```c
void DrawFountains(void)
{
    static word slowcount = 0;
    static word fastcount = 0;
    word i;
```

This function has two private variables that retain their value across calls (see "`static`"). These are `slowcount` and `fastcount`. Each of these increments as the game runs, with no provision for their value to be externally reset except by quitting to DOS and restarting the executable. Being 16-bit values, they roll from 65,535 back to zero approximately every 200 and 100 minutes, respectively, at the game's typical frame rate. `i` is used to iterate over all of the fountains.

```c
    fastcount++;
    if (fastcount % 2 != 0) {
        slowcount++;
    }
```

`fastcount` increments each time this function is called, and serves no purpose other than to ensure that `slowcount` is incremented every other tick. This runs `slowcount` at half of the game's frame rate -- about five increments per second.

```c
    for (i = 0; i < numFountains; i++) {
        word y;
        Fountain *fnt = fountains + i;
```

The `for` loop iterates over each fountain in the map, up to {{< lookup/cref numFountains >}}. The {{< lookup/cref fountains >}} array is indexed to access a single {{< lookup/cref Fountain >}} structure, which `fnt` points to.

```c
        DrawSprite(
            SPR_FOUNTAIN, slowcount % 2, fnt->x, fnt->y + 1, DRAW_MODE_NORMAL
        );
```

The Y position of the fountain object is the row of tiles that the player and actors can stand on, which moves up and down over time. The actual spray sprite is two tiles tall, with the upper row of tiles corresponding to the true position of the fountain. The tile drawing functions, on the other hand, consider "origin" of the sprite graphic to be the the _bottom_-left tile. Due to this discrepancy, the Y calculations here need to be increased by one to convert the fountain system's sense of origin to the conventions that sprites use. The X position doesn't need any correction because the fountain and sprite conventions match.

This call to {{< lookup/cref DrawSprite >}} draws the spray at the top of the fountain, which is visible at all times (even when the fountain is at its lowest height). {{< lookup/cref name="SPR" text="SPR_FOUNTAIN" >}} is the sprite type, and `slowcount % 2` is used to continually flip between frames 0 and 1 of the sprite's spray animation. This is drawn using the typical {{< lookup/cref name="DRAW_MODE" text="DRAW_MODE_NORMAL" >}} option.

```c
        for (y = 0; fnt->height + 1 > y; y++) {
            DrawSprite(
                SPR_FOUNTAIN, (slowcount % 2) + 2,
                fnt->x + 1, fnt->y + y + 1, DRAW_MODE_NORMAL
            );
```

Directly beneath the spray at the top of the fountain, there is a variable-height stream of mud where the fountain anchors to the floor. This stream is constructed from a vertical strip of tiles which get drawn here. The `y` variable increments via a `for` loop from zero up to the fountain's height (`fnt->height`). On each iteration, {{< lookup/cref DrawSprite >}} is called to draw one tile of the stream.

The drawing arguments are as follows:

* {{< lookup/cref name="SPR" text="SPR_FOUNTAIN" >}} is constant, and selects the fountain out of all the sprite types available in the game.
* `(slowcount % 2) + 2` evaluates to either 2 or 3, which selects one of the of two stream animation frames. (Frames 0 and 1 are the spray frames for the top of the fountain, which are not appropriate here.)
* `fnt->x + 1` aligns the stream horizontally. The value in `fnt->x` refers to the X position of the left edge of the _spray_, which is three tiles wide. To center the stream relative to that, a one-tile adjustment is required.
* `fnt->y + y + 1` is the stream tile's vertical position, which works similarly to the horizontal. `fnt->y` represents the vertical position of the _top_ row of the spray, while the stream begins one tile beneath -- this begins drawing the stream on top of the lower row of spray tiles, which might be an oversight. As the enclosing `for` loop increments `y`, this location moves further down on the screen.
* {{< lookup/cref name="DRAW_MODE" text="DRAW_MODE_NORMAL" >}} configures the behavior of {{< lookup/cref DrawSprite >}}, causing the X/Y positions to be drawn relative to the map's coordinate system.

{{< image src="fountain-spray-overlap-2052x.png"
    alt="Comparison of the mud fountain spray and stream, with and without overlap."
    1x="fountain-spray-overlap-684x.png"
    2x="fountain-spray-overlap-1368x.png"
    3x="fountain-spray-overlap-2052x.png" >}}

{{< lookup/cref DrawSprite >}} takes care of all visibility and clipping concerns, taking no action if the fountain is partially off the screen.

```c
            if (
                IsTouchingPlayer(SPR_FOUNTAIN, 2, fnt->x + 1, fnt->y + y + 1)
            ) {
                HurtPlayer();
            }
        }
    }
}
```

Still inside the stream-drawing `for` loop, each vertical position is tested for intersection with the player sprite. Each of the arguments in the {{< lookup/cref IsTouchingPlayer >}} call are the same as those that appeared earlier, except the animation frame is constant at 2. This works because both frames of stream animation are the same size on screen, thus it doesn't matter which one is used for intersection checking.

If {{< lookup/cref IsTouchingPlayer >}} returns true, the fountain stream tile that's currently being drawn is touching some part of the player sprite. Per the game's design, this is injurious to the player and {{< lookup/cref HurtPlayer >}} is called to try to deduct a unit of health.

In normal gameplay, multiple stream tiles will intersect the player. (The player is five tiles tall and a fountain could pass through all of them.) This may result in {{< lookup/cref HurtPlayer >}} being called up to five times during a single frame. A cooldown mechanism within the {{< lookup/cref HurtPlayer >}} function prevents the fountain from being too grievous.

The `for` loop repeats, incrementing `y` until the full height of the current fountain has been covered. Following that, the outer `for` loop continues incrementing `i` until all fountains enumerated in {{< lookup/cref numFountains >}} are drawn. Once _that_ completes, the function returns.

{{< boilerplate/function-cref MovePlayerPlatform >}}

The {{< lookup/cref MovePlayerPlatform >}} function determines if a platform covering X positions `x_west` to `x_east` is interacting with the player, and if so, modifies the player's position to keep them attached to the platform as it moves. The current movement direction of the platform is passed in horizontal/vertical arguments `x_dir` and `y_dir`. This function **does not** check the player's Y position when determining if they are touching the platform -- the caller must ensure that the player is at a sensible vertical position for a particular platform before attempting to call this function on it.

{{% note %}}It's worth reading that again. This function should not be called for a platform unless the player's Y position has been found to be correct relative to that platform's Y position.{{% /note %}}

This function ignores the player if they are currently riding on a scooter. If a platform passes under the player while they are clinging to a wall, the cling is released so the player can "fall onto" the passing platform.

```c
void MovePlayerPlatform(word x_west, word x_east, word x_dir, word y_dir)
{
    register word offset;
    register word playerx2;

    if (scooterMounted != 0) return;

    offset = *playerInfoData;
    playerx2 = *(playerInfoData + offset + 1) + playerX - 1;
```

Right off the bat, a check is performed to see if the player is riding on a scooter. If they are (represented by a nonzero {{< lookup/cref scooterMounted >}}), the function immediately returns -- platforms have no effect while the scooter is in use.

Otherwise, the horizontal extents of the player sprite need to be determined. We already know that {{< lookup/cref playerX >}} represents the horizontal location of the player's left edge, but the location of their right edge is not currently known. This is computed using a rather odd combination of static and dynamic programming.

{{< lookup/cref playerInfoData >}} is [tile info data]({{< relref "tile-info-format" >}}) and begins with a list of offsets to each sprite type in the file. Since players only have a single sprite type, the index is implicitly zero and the offset can be read from the immediate beginning of the file. The offset to the real data is read into `offset`.

Within the tile info data, `offset` points to the start of an eight-byte structure for the zeroth frame of the sprite. To reach additional frames, a multiple of four words should be added to the `offset`. This is not done here -- this function always computes the size of the player's zeroth frame regardless of which one is being shown. This is not an issue in practice because most of the player sprites are a constant 3 &times; 5 tiles, but it does call into question why this couldn't have been a compile-time constant.

The width of a sprite frame is stored at index 1 within a tile info record, which is at `playerInfoData + offset + 1`. By dereferencing this value, we determine the width of the player sprite, in tiles. Adding {{< lookup/cref playerX >}} to this locates the first empty tile (in map space) to the right of the player's sprite, and subtracting one yields the position of the rightmost column of tiles occupied by the player. This is stored in `playerx2` for future use.

```c
    if (
        playerClingDir != DIR4_NONE &&
        TestPlayerMove(DIR4_SOUTH, playerX, playerY + 1) != MOVE_FREE
    ) {
        playerClingDir = DIR4_NONE;
    }
```

This check handles a rare edge condition. In order for the player to cling to a wall, there must be empty space directly below them. With moving platforms in the mix, there is now a chance that this empty space constraint could be violated due to a platform moving underneath the player. If that should happen, the cling is released so the player begins to ride on the platform.

The condition requires that {{< lookup/cref playerClingDir >}} has a value other than {{< lookup/cref name="DIR4" text="DIR4_NONE" >}}, which happens when the player is clinging to some wall. {{< lookup/cref TestPlayerMove >}} checks the map position at {{< lookup/cref playerX >}} and one tile lower than {{< lookup/cref playerY >}}, inquiring if a move in the {{< lookup/cref name="DIR4" text="DIR4_SOUTH" >}} direction is permitted. If the call returns anything other than {{< lookup/cref name="MOVE" text="MOVE_FREE" >}}, there is a tile below the player that prohibits southward movement. In essence, the player is simultaneously standing on something while clinging to an adjacent wall. _This should not happen_ during normal gameplay -- the logic in {{< lookup/cref MovePlayer >}} prohibits entering a cling if the player is standing on something.

To resolve this condition, the cling is released by setting {{< lookup/cref playerClingDir >}} to {{< lookup/cref name="DIR4" text="DIR4_NONE" >}}, releasing the cling and letting the player rest on the surface below. Presumably this is a platform, and they will now move along with it.

```c
    if (
        (playerX  < x_west || playerX  > x_east) &&
        (playerx2 < x_west || playerx2 > x_east)
    ) return;
```

At this point in the execution, none of the calling code has actually checked to determine if the horizontal extents of the platform match those of the player position. This block checks the proximity between the player and the platform, and returns early if they are not close enough for an interaction to occur.

{{% aside class="armchair-engineer" %}}
**Gotta do it somewhere, I suppose.**

It appears that the main motivator for splitting the horizontal and vertical checks was the dynamic calculation of the player's width. The horizontal calculations need to know the player width, and that width had to be read from {{< lookup/cref playerInfoData >}}. By conditionally skipping that if the vertical position was not appropriate, some unnecessary work was avoided.

Although, if the player happens to be at a vertical position that more than one platform occupies, then multiple calls to this function occur and all the work gets repeated. This is a much rarer occurrence in practice, however.
{{% /aside %}}

The actual test is as follows: If the player's bottom-left tile ({{< lookup/cref playerX >}}) is off either edge of the platform (`x_west`/`x_east`) **AND** the player's bottom-right tile (`playerx2`) is off either edge of the platform, then this platform is not touching the player at all and no further action should be taken, so return. This test would fall apart in the case where a very wide player rides with both edges overhanging a narrow platform, but nothing in this game is proportioned that way.

```c
    playerX += dir8X[x_dir];
    playerY += dir8Y[y_dir];
```

The actual movement is short and sweet: Increment {{< lookup/cref playerX >}} with the value from the {{< lookup/cref dir8X >}} table entry for `x_dir`, then do the same thing in the vertical direction. The {{< lookup/cref dir8X >}}/{{< lookup/cref dir8Y >}} values are in the range -1--1, producing zero or one tile of movement in any direction.

```c
    if ((cmdNorth || cmdSouth) && !cmdWest && !cmdEast) {
        if (cmdNorth && scrollY > 0 && playerY - scrollY < SCROLLH - 1) {
            scrollY--;
        }

        if (cmdSouth && (
            scrollY + 4 < playerY ||
            (dir8Y[y_dir] == 1 && scrollY + 3 < playerY)
        )) {
            scrollY++;
        }
    }

    if (playerY - scrollY > SCROLLH - 1) {
        scrollY++;
    } else if (playerY - scrollY < 3) {
        scrollY--;
    }

    if (playerX - scrollX > SCROLLW - 15 && mapWidth - SCROLLW > scrollX) {
        scrollX++;
    } else if (playerX - scrollX < 12 && scrollX > 0) {
        scrollX--;
    }

    if (dir8Y[y_dir] == 1 && playerY - scrollY > SCROLLH - 4) {
        scrollY++;
    }

    if (dir8Y[y_dir] == -1 && playerY - scrollY < 3) {
        scrollY--;
    }
}
```

This is [view centering code]({{< relref "view-centering" >}}), similar to that found in a few other areas of the game logic. This ensures that the player always remains positioned prominently on the screen as the platform moves. This is achieved by modifying {{< lookup/cref scrollX >}} and {{< lookup/cref scrollY >}}.

With the player/platform interaction handled, this function returns to the caller. It's possible for this function to be called more than once during a frame of gameplay (in the case where the player momentarily has the same Y position as two or more platforms) but at most one invocation of this function should actually move the player.
