+++
title = "Actor Movement Functions"
linkTitle = "Movement Functions"
description = "Describes the functions used to move and draw standard actors, and the movement functions that handle common tasks for actors that walk along the ground."
weight = 480
+++

# Actor Movement Functions

During each tick of gameplay, every actor in memory needs to be serviced and some subset of those need to be drawn onto the screen. Part of this processing uses common state management and movement code, which is what this page focuses on. All actors share the same activation/visibility code, "weighted" actors typically use common gravity code, and the majority of actors use the common sprite drawing facility.

The code described here also calls each actor's **tick function**, and those are responsible for the unique aspects of an actor type's behavior. The specifics of these are described elsewhere, but the functions here serve as their caller as well as their utility library.

{{< table-of-contents >}}

{{< boilerplate/function-cref MoveAndDrawActors >}}

The {{< lookup/cref MoveAndDrawActors >}} function iterates over each actor currently "alive" in the game and calls the per-actor processing function. Before the first actor is serviced, and after the last one completes, a small number of global state management tasks are handled.

This function is called by the [game loop]({{< relref "game-loop-functions" >}}) once per frame.

```c
void MoveAndDrawActors(void)
{
    word i;

    isPlayerNearHintGlobe = false;

    for (i = 0; i < numActors; i++) {
        ProcessActor(i);
    }

    if (mysteryWallTime != 0) mysteryWallTime = 0;
}
```

The {{< lookup/cref isPlayerNearHintGlobe >}} global variable is is used to determine if the <kbd>&uparrow;</kbd> key should allow the player to look up, or if that key needs to be overridden to display a hint message. To differentiate these cases, the tick function for each {{< lookup/actor type=125 strip=true >}} sets this flag each time one of them detects that the player is close enough to "use" it. As the hint globes are unaware of each other's existence, it is not possible for them to confidently clear this flag when the player moves away. Instead, the approach is to unconditionally clear the flag here at the beginning of each game tick, and allow each hint globe to re-enable the flag as long as the activation condition holds.

The `for` loop iterates over every actor slot that has been used (up to {{< lookup/cref numActors >}}) and calls the {{< lookup/cref ProcessActor >}} function to perform the per-tick behavior for that one actor. The passed `i` is used by the callee to select the correct actor slot to operate on.

If the player activated a {{< lookup/actor 61 >}} during this game tick, the switch actor's tick function will have set the global {{< lookup/cref mysteryWallTime >}} variable to a nonzero value. This is detected by each {{< lookup/actor 62 >}} actor on the map and they awaken themselves in response. Because there could be more than one mystery wall on the map, {{< lookup/cref mysteryWallTime >}} is not reset by any of the actors that respond to its value. Instead, this function waits until the loop completes handling all of the actors, then it resets {{< lookup/cref mysteryWallTime >}} on their behalf.

{{< boilerplate/function-cref ProcessActor >}}

The {{< lookup/cref ProcessActor >}} function handles the overall per-tick movement for one actor, identified by its `index` position in the actors array. If the actor is marked as dead, this function is a no-op.

The responsibilities of this function are:

* Killing actors that fall off the bottom of the map
* Managing the hurt cooldown
* Deciding if the actor is visible and translating that into active/inactive and drawn/hidden states, respecting the actor's configuration
* Ejecting the actor from any solid areas they may have fallen into
* Pulling weighted actors down due to gravity
* Calling the actor's tick function
* Checking if any nearby explosions should destroy the actor
* Calling the player-actor interaction function
* Drawing the sprite

The actions performed in this function are the "typical" case for an unremarkable actor -- some actor types have more complicated movements or display requirements that are not well handled by the implementations here. These actors will either disable some flags in their configuration to deactivate the conflicting parts of this function, or outright revert/override the work performed here.

```c
void ProcessActor(word index)
{
    Actor *act = actors + index;

    if (act->dead) return;
```

The passed `index` represents the element of the {{< lookup/cref actors >}} array that's being processed here. These are combined into a local `act` pointer to the {{< lookup/cref Actor >}} structure within.

If the actor has its `dead` flag set, there is nothing left to do for it -- it is unconditionally skipped with an early `return`. Some future actor may re-use this actor slot and clear the `dead` flag, but for now there is nothing that can or should be done.

```c
    if (act->y > maxScrollY + SCROLLH + 3) {
        act->dead = true;
        return;
    }
```

This checks if the actor has fallen off the map. {{< lookup/cref maxScrollY >}} represents the vertical row of map tiles that would be at the top of the screen when the scrolling game window is showing the absolute bottom of the map. Adding {{< lookup/cref SCROLLH >}} to that produces the first row of tiles that is conceptually blocked by the status bar at the bottom of the screen. Adding an additional three tiles to that moves the reference row even lower. When the actor's `y` position exceeds this sum, the actor has fallen far enough off the bottom of the map that a sprite five tiles tall would no longer be visible.

When an actor falls that far, the `if` condition will be true and the body executes, setting the actor's `dead` flag. An early `return` prevents further processing of this actor, and subsequent calls for this slot will not operate on the dead actor.

```c
    nextDrawMode = DRAW_MODE_NORMAL;

    if (act->hurtcooldown != 0) act->hurtcooldown--;
```

The {{< lookup/cref nextDrawMode >}} global controls how (and if) this actor's sprite will be drawn by this function. The initial assumption is that the actor should be drawn using the default behavior ({{< lookup/cref name="DRAW_MODE" text="DRAW_MODE_NORMAL" >}}) but this may change as execution proceeds. The variable is global so that the actor's tick function can override this decision before drawing occurs.

Separately, if the actor has recently suffered damage, it will have a nonzero `hurtcooldown` which prevents it from being hurt again for a short time. The cooldown always decays toward zero, which occurs here.

```c
    if (IsSpriteVisible(act->sprite, act->frame, act->x, act->y)) {
        if (act->stayactive) {
            act->forceactive = true;
        }
    } else if (!act->forceactive) {
        return;
    } else {
        nextDrawMode = DRAW_MODE_HIDDEN;
    }
```

These `if`s control the actor's active/inactive state based on visibility.

If the actor's sprite (represented by a `sprite`, `frame`, `x`, and `y`) is at least partially visible on the screen according to {{< lookup/cref IsSpriteVisible >}}, the first `if` body will execute _and the function will continue executing below._ Additionally, if the actor has its `stayactive` flag enabled, it will have its `forceactive` flag turned on as well. This will keep it active indefinitely, even if it later scrolls out of view.

In the `else if` case, the actor is not currently visible anywhere on the screen. If the `forceactive` flag is disabled, the actor should not move or be drawn and an early `return` ensures this.

In the `else` case, the actor is not visible on the screen but its `forceactive` flag is enabled. Execution continues below and the actor moves like usual, but {{< lookup/cref nextDrawMode >}} is updated to {{< lookup/cref name="DRAW_MODE" text="DRAW_MODE_HIDDEN" >}} so that no time is wasted trying to draw something that cannot be seen in the current view.

```c
    if (act->weighted) {
        if (TestSpriteMove(
            DIR4_SOUTH, act->sprite, 0, act->x, act->y
        ) != MOVE_FREE) {
            act->y--;
            act->falltime = 0;
        }
```

Actors that are `weighted` experience gravity and will fall down if they are not resting at least partially on an impassible map tile. The actor logic tries its best to ensure that an actor never falls inside of an impassible area, but sometimes such an area moves into an actor's space. An intuitive example would be an actor sitting on top of a [platform or mud fountain]({{< relref "../../entities/platform-functions" >}}) -- a descending platform is no trouble because the actor will fall naturally once the platform moves away. But a rising platform will rise into the actor's feet, requiring the actor to detect this condition and eject itself upwards to resolve the conflict.

If {{< lookup/cref TestSpriteMove >}}, given the actor's current `x` and `y` positions, indicates that the actor is standing inside a tile that prohibits {{< lookup/cref name="DIR4" text="DIR4_SOUTH" >}} movement (so the result is not {{< lookup/cref name="MOVE" text="MOVE_FREE" >}}), the actor should've never been allowed to move into the location where it now is. Decrement `y` in response, moving the actor one tile higher on the map (and one tile further away from the problem). Since the actor is not only standing _on_ the ground, they're standing _in_ it, `falltime` is zeroed since they are most assuredly not falling.

{{% note %}}The frame number in these {{< lookup/cref TestSpriteMove >}} calls is hard-coded to zero instead of the actual display frame. This could (and does; see {{< lookup/actor type=124 plural=true >}}) lead to incorrect behavior if the zeroth sprite frame has a different width than the one that's currently displayed.{{% /note %}}

```c
        if (TestSpriteMove(
            DIR4_SOUTH, act->sprite, 0, act->x, act->y + 1
        ) == MOVE_FREE) {
            if (act->falltime < 5) act->falltime++;

            if (act->falltime > 1 && act->falltime < 6) {
                act->y++;
            }

            if (act->falltime == 5) {
                if (TestSpriteMove(
                    DIR4_SOUTH, act->sprite, 0, act->x, act->y + 1
                ) != MOVE_FREE) {
                    act->falltime = 0;
                } else {
                    act->y++;
                }
            }
        } else {
            act->falltime = 0;
        }
    }
```

Still inside the `if` block where `act->weighted` is true, we check for the case where the actor is not currently standing on solid ground. The map tile at the actor's `y + 1` position is tested using the {{< lookup/cref TestSpriteMove >}} function, and if this returns {{< lookup/cref name="MOVE" text="MOVE_FREE" >}} in the {{< lookup/cref name="DIR4" text="DIR4_SOUTH" >}} direction, it indicates that there is nothing solid directly underneath the actor's feet -- they could freely fall at least one tile.

As long as the actor is not standing on anything, `falltime` is incremented up to a maximum of five. If `falltime` is greater than one (the `< 6` part is always true) the actor is moved one tile down by incrementing `y`. It's worth noting that, during the first tick where an actor is initially found to be in a falling state, `falltime` will not be _greater_ than one. This introduces a one-tick delay before the actor begins falling.

When `falltime` reaches its maximum of five, the actor falls at double speed by incrementing `y` twice per tick. This necessitates an additional {{< lookup/cref TestSpriteMove >}} call, structured identically to the first one, to check if the actor can freely fall the additional tile.

If either of the {{< lookup/cref TestSpriteMove >}} calls indicate that the actor is now in a position where there is solid ground beneath their feet, `falltime` is zeroed to disable subsequent fall handling.

```c
    if (IsSpriteVisible(act->sprite, act->frame, act->x, act->y)) {
        nextDrawMode = DRAW_MODE_NORMAL;
    }
```

Because a falling actor may have moved far enough to invalidate the result of the original visibility test, an additional check is made to see if the actor entered the screen at its current position. If so, {{< lookup/cref nextDrawMode >}} is defaulted to {{< lookup/cref name="DRAW_MODE" text="DRAW_MODE_NORMAL" >}}.

{{% note %}}This doesn't cover the inverse case, where an actor fell to a position where they are no longer visible. There are times where {{< lookup/cref name="DRAW_MODE" text="DRAW_MODE_HIDDEN" >}} would be an appropriate value to set here, which is not done.{{% /note %}}

```c
    act->tickfunc(index);
```

This calls whichever tick function the actor is configured to use, passing the `index` in the actor array as the sole argument. The most common things that this call would change are the actor's `x`/`y` position, the displayed `frame`, or the value in {{< lookup/cref nextDrawMode >}}.

Several actors draw their own sprites from inside the tick function. These will set {{< lookup/cref nextDrawMode >}} to {{< lookup/cref name="DRAW_MODE" text="DRAW_MODE_HIDDEN" >}} to prevent this function from performing a superfluous draw call of its own.

```c
    if (
        IsNearExplosion(act->sprite, act->frame, act->x, act->y) &&
        CanExplode(act->sprite, act->frame, act->x, act->y)
    ) {
        act->dead = true;
        return;
    }
```

If this actor is not near any active explosion, {{< lookup/cref IsNearExplosion >}} will return false and the `if` condition will short-circuit, taking no further action. When an explosion is nearby, {{< lookup/cref CanExplode >}} is called to determine if the actor can be damaged by an explosion, and to handle the scoring and visual effects that accompany the destruction of an explodable actor type.

When {{< lookup/cref CanExplode >}} returns true, the actor is indeed explodable and the actor immediately dies, having already released its points to the player. The `dead` flag is enabled and the function immediately `return`s.

```c
    if (InteractPlayer(index, act->sprite, act->frame, act->x, act->y)) return;
```

{{< lookup/cref InteractPlayer >}} determines what should happen when the player and an actor touch each other. That function determines if the actor is being touched at all, and if this touch is the result of the player pouncing on the actor or the actor damaging the player.

The {{< lookup/cref InteractPlayer >}} return value controls whether this function should continue drawing the sprite for this actor. A true value accompanies conditions like a prize being picked up or an actor suffering a fatal pounce, both of which should remove the sprite from the screen. The early `return` prevents drawing in these situations.

```c
    if (nextDrawMode != DRAW_MODE_HIDDEN) {
        DrawSprite(act->sprite, act->frame, act->x, act->y, nextDrawMode);
    }
}
```

Finally, execution finds its way to the standard sprite-drawing step. If the {{< lookup/cref nextDrawMode >}} value is set to anything other than {{< lookup/cref name="DRAW_MODE" text="DRAW_MODE_HIDDEN" >}}, the {{< lookup/cref DrawSprite >}} function is called to draw the sprite to the screen. Any actor whose tick function does not contain custom sprite-drawing logic will rely on this call for its drawing needs.

{{< boilerplate/function-cref TestSpriteMove >}}

The {{< lookup/cref TestSpriteMove >}} function tests if the sprite identified by `sprite_type` and `frame` is permitted to move in the direction specified by `dir` and enter the map tiles around `x_origin` and `y_origin`. Depending on the result of the test, one of the {{< lookup/cref MOVE >}} constants is returned according to the following table:

Return Value                                        | Description
----------------------------------------------------|------------
{{< lookup/cref name="MOVE" text="MOVE_FREE" >}}    | The move is permitted; none of the map tiles the sprite touches in the new location interfere with movement in the specified direction.
{{< lookup/cref name="MOVE" text="MOVE_BLOCKED" >}} | The move is forbidden; at least one of the map tiles the sprite touches in the new location forbids movement in the specified direction.
{{< lookup/cref name="MOVE" text="MOVE_SLOPED" >}}  | The move is permitted as with {{< lookup/cref name="MOVE" text="MOVE_FREE" >}}, however at least one tile at the sprite's base is sloped and a subsequent vertical adjustment will be required to keep the sprite at the correct height.

This function is quite similar to {{< lookup/cref TestPlayerMove >}}, with the main difference being that this function can accept any arbitrarily-sized actor or entity sprite.

```c
word TestSpriteMove(
    word dir, word sprite_type, word frame, word x_origin, word y_origin
) {
    word *mapcell;
    register word i;
    register word height;
    word width;
    word offset = *(actorInfoData + sprite_type) + (frame * 4);

    height = *(actorInfoData + offset);
    width = *(actorInfoData + offset + 1);
```

In order to determine the sprite's interaction with its environment, both the X/Y position of the sprite _and_ its width/height need to be known. This is looked up inside the [tile info data]({{< relref "tile-info-format" >}}) at {{< lookup/cref actorInfoData >}}. The `offset` to the sprite's zeroth frame's is stored in `*(actorInfoData + sprite_type)`, and adding `frame * 4` steps over the correct number of four-word frame structures to locate the necessary frame data.

The `height` of the sprite frame is read from `*(actorInfoData + offset)`, and the `width` is one word later in the data.

```c
    switch (dir) {
```

The remainder of this function is structured as a `switch` on the passed `dir`. Each case handles one of the four possible {{< lookup/cref DIR4 >}} values.

```c
    case DIR4_NORTH:
        mapcell = MAP_CELL_ADDR(x_origin, (y_origin - height) + 1);

        for (i = 0; i < width; i++) {
            if (TILE_BLOCK_NORTH(*(mapcell + i))) return MOVE_BLOCKED;
        }

        break;
```

In the {{< lookup/cref name="DIR4" text="DIR4_NORTH" >}} case, each tile along the top edge of the sprite must be tested for intersection with a north-blocking tile. The starting position is the unmodified `x_origin` in the horizontal direction, and the `y_origin - height` plus one to select the top row. (Remember, `y_origin` refers to the bottom row of sprite tiles.) These coordinates are passed through the {{< lookup/cref MAP_CELL_ADDR >}} macro to produce a pointer to the tile within {{< lookup/cref mapData >}} that the top-left tile occupies. This is stored in `mapcell`.

The `for` loop steps the `i` variable from zero to one less than the sprite's width. This produces one iteration per sprite tile column. On each iteration, the tile value at `*(mapcell + i)` is tested for the {{< lookup/cref TILE_BLOCK_NORTH >}} attribute. The increasing values of `i` advance the tile horizontally across the map. If any tile is encountered that blocks the move, {{< lookup/cref name="MOVE" text="MOVE_BLOCKED" >}} is immediately returned without considering any additional columns -- one tile is all it takes to block the whole sprite.

If the `for` loop ends naturally, the entire top edge of the sprite has been examined without finding any blocking map tiles. In this case, `break` jumps out of the `switch` and ultimately returns {{< lookup/cref name="MOVE" text="MOVE_FREE" >}} at the bottom of the function.

```c
    case DIR4_SOUTH:
        mapcell = MAP_CELL_ADDR(x_origin, y_origin);

        for (i = 0; i < width; i++) {
            if (TILE_SLOPED(*(mapcell + i))) return MOVE_SLOPED;

            if (TILE_BLOCK_SOUTH(*(mapcell + i))) return MOVE_BLOCKED;
        }

        break;
```

The {{< lookup/cref name="DIR4" text="DIR4_SOUTH" >}} is similar to {{< lookup/cref name="DIR4" text="DIR4_NORTH" >}}, but the initial Y position is the unmodified `y_origin` to select the bottom row of sprite tiles.

The `for` loop contains two tests. The first checks for sloped ground via the {{< lookup/cref TILE_SLOPED >}} attribute lookup macro, returning {{< lookup/cref name="MOVE" text="MOVE_SLOPED" >}} if such a tile is found. The remaining test is {{< lookup/cref TILE_BLOCK_SOUTH >}}, returning {{< lookup/cref name="MOVE" text="MOVE_BLOCKED" >}} as before.

```c
    case DIR4_WEST:
        if (x_origin == 0) return MOVE_BLOCKED;

        mapcell = MAP_CELL_ADDR(x_origin, y_origin);

        for (i = 0; i < height; i++) {
            if (
                i == 0 &&
                TILE_SLOPED(*mapcell) &&
                !TILE_BLOCK_WEST(*(mapcell - mapWidth))
            ) return MOVE_SLOPED;

            if (TILE_BLOCK_WEST(*mapcell)) return MOVE_BLOCKED;

            mapcell -= mapWidth;
        }

        break;
```

The {{< lookup/cref name="DIR4" text="DIR4_WEST" >}} case covers movement toward the left. Right off the bat, if `x_origin` is zero, the sprite is considering moving off the left edge of the map and the move should be unconditionally denied with a {{< lookup/cref name="MOVE" text="MOVE_BLOCKED" >}} return. Otherwise, {{< lookup/cref MAP_CELL_ADDR >}} sets up the initial value of the `mapcell` pointer to use the bottom-left sprite tile at `x_origin` and `y_origin`.

The `for` loop increments `i` from zero to the `height` of the sprite minus one. Conceptually this walks from the bottom row of the sprite to the top.

On the first iteration only, `i` will be zero and the {{< lookup/cref TILE_SLOPED >}} attribute is checked. If this test passes, the bottom-left tile of the sprite is positioned on a tile that has a "sloped" attribute. When such a tile is negotiated, the caller will need to be informed that, while the move is permitted, the sprite will also need to move up one tile to follow the slope uphill. To save the caller from needing to test if the vertical-adjusted position is also free to be moved into, an abbreviated test is done: If the tile at `*(mapcell - mapWidth)` does not have a {{< lookup/cref TILE_BLOCK_WEST >}} attribute, the move is assumed to be acceptable. (See below for a bit more about what {{< lookup/cref mapWidth >}} is doing here.) Upon passing all the tests, {{< lookup/cref name="MOVE" text="MOVE_SLOPED" >}} is returned without considering any other tiles in the sprite.

In all other cases, the position at `mapcell` is tested using {{< lookup/cref TILE_BLOCK_WEST >}} and any blocking tile is immediately reported with a {{< lookup/cref name="MOVE" text="MOVE_BLOCKED" >}} return.

The next tile to be tested is one position higher in the map data. The map is a two-dimensional grid of tiles stored in a one-dimensional array in row-major order. A one-tile step in the vertical direction corresponds to a step of {{< lookup/cref mapWidth >}} tiles along the array. The `mapcell` pointer is rewound by one map-width to select the next higher tile.

If all tiles along the left edge of the sprite have been examined without finding a blocking tile, `break` leaves the switch for the common {{< lookup/cref name="MOVE" text="MOVE_FREE" >}} return.

```c
    case DIR4_EAST:
        if (x_origin + width == mapWidth) return MOVE_BLOCKED;

        mapcell = MAP_CELL_ADDR(x_origin + width - 1, y_origin);

        for (i = 0; i < height; i++) {
            if (
                i == 0 &&
                TILE_SLOPED(*mapcell) &&
                !TILE_BLOCK_EAST(*(mapcell - mapWidth))
            ) return MOVE_SLOPED;

            if (TILE_BLOCK_EAST(*mapcell)) return MOVE_BLOCKED;

            mapcell -= mapWidth;
        }

        break;
    }
```

{{< lookup/cref name="DIR4" text="DIR4_EAST" >}} is much the same as {{< lookup/cref name="DIR4" text="DIR4_WEST" >}} with only a few symmetrical differences: The map edge test compares `x_origin + width` against {{< lookup/cref mapWidth >}} to keep the right edge of the sprite within the map bounds. `mapcell` is initialized to the bottom _right_ tile (`x_origin + width - 1`) and the blocking tests all use {{< lookup/cref TILE_BLOCK_EAST >}}.

```c

    return MOVE_FREE;
}
```

In every case where a loop exited naturally without returning due to a blocking tile, this move is unimpeded and {{< lookup/cref name="MOVE" text="MOVE_FREE" >}} is returned to the caller.

{{< boilerplate/function-cref AdjustActorMove >}}

The {{< lookup/cref AdjustActorMove >}} function verifies the legality of a map position that the actor (identified by slot `index`) has just moved into and reverts/adjusts their position accordingly. `dir` should be either {{< lookup/cref name="DIR4" text="DIR4_WEST" >}} or {{< lookup/cref name="DIR4" text="DIR4_EAST" >}} to match the direction of movement.

This will either completely revert a move, adjust the vertical position, or leave the move exactly as it was with the actor's `westfree`/`eastfree` flags set accordingly.

```c
void AdjustActorMove(word index, word dir)
{
    Actor *act = actors + index;
    word offset;
    word width;
    word result = 0;

    offset = *(actorInfoData + act->sprite);
    width = *(actorInfoData + offset + 1);
```

The `act` pointer is set up to point to the element in the {{< lookup/cref actors >}} array that `index` refers to. This function uses the index (and only the index) to select the appropriate actor.

`result` is a scratch variable used to hold the raw value of a {{< lookup/cref TestSpriteMove >}} call. It is explicitly zeroed here, although it's not strictly necessary given the way it's used below.

The `width` of the actor's sprite is required for movement in (only) the west direction, so this is looked up in the [tile info data]({{< relref "tile-info-format" >}}) for actor sprites, which is read from {{< lookup/cref actorInfoData >}}. The `offset` to the zeroth frame is calculated for the current `act->sprite`, then that offset is used to locate the frame structure. The value at offset 1 is the width.

{{% note %}}At no point is `act->frame` considered when looking up the `width`; the width of the sprite's zeroth frame is always loaded here. Actors with variable-width sprite frames may experience inappropriate movement behavior using this function.{{% /note %}}

```c
    if (dir == DIR4_WEST) {
        /* Western movement code ... */
    } else {
        /* Eastern movement code ... */
    }
}
```

The `dir` is used to switch between two branches: The {{< lookup/cref name="DIR4" text="DIR4_WEST" >}} direction, or everything else. The "everything else" case is assumed to mean {{< lookup/cref name="DIR4" text="DIR4_EAST" >}}. Each of these sub-sections is described next.

After the relevant sub-section finishes, there is nothing left to be done and the function returns.

### Western Movement

There are _seven_ possible movement cases that could occur in the western direction (including the implicit seventh "no-op" case that may occur if none of the conditions match). Regardless of the path taken, the actor's `westfree` member is updated to reflect the map conditions in this direction.

```c
    result = TestSpriteMove(
        DIR4_WEST, act->sprite, act->frame, act->x, act->y);
    act->westfree = !result;
```

This function is always called after an actor has had its X position adjusted -- in this branch, X has already been decremented to move the actor toward the {{< lookup/cref name="DIR4" text="DIR4_WEST" >}} direction. {{< lookup/cref TestSpriteMove >}} checks the position where the player now is, returning one of the {{< lookup/cref MOVE >}} values into `result`.

Negating `result` converts {{< lookup/cref name="MOVE" text="MOVE_FREE" >}} into a true value for the actor's `westfree` boolean flag, and collapses {{< lookup/cref name="MOVE" text="MOVE_BLOCKED" >}} and {{< lookup/cref name="MOVE" text="MOVE_SLOPED" >}} into false values.

#### Case 1: Ejection from a solid wall

```c
    if (act->westfree == 0 && result != MOVE_SLOPED) {
        act->x++;
```

If `westfree` is false, it could either be because the result of the movement check indicated the tile was blocked _or_ that it was sloped. If `result` is not {{< lookup/cref name="MOVE" text="MOVE_SLOPED" >}} we know it must've been the "blocked" case. The actor simply cannot walk west into the position where they currently are, so the move is unwound by moving them back one tile to the east.

#### Case 2: Ejection from a sloped floor

```c
    } else if (result == MOVE_SLOPED) {
        act->westfree = 1;
        act->y--;
```

By reaching this case, we know that the move was permitted. The `result` of the movement test is checked against {{< lookup/cref name="MOVE" text="MOVE_SLOPED" >}}. When true, this indicates that the player walked horizontally into a sloped piece of ground, and they now need to be ejected "up" to keep them at the correct elevation. This is done by decrementing the actor's `y` position by one tile.

The initial negation of `result` was insufficient to correctly handle this case, so here the actor's `westfree` flag is explicitly set to indicate that, yes, the movement in this direction was permitted after vertical correction.

#### Case 3: Walking on a solid floor

```c
    } else if (TestSpriteMove(
        DIR4_SOUTH, act->sprite, act->frame, act->x, act->y + 1
    ) > MOVE_FREE) {
        act->westfree = 1;
```

To reach this case (and all cases after), the move did not encounter any blocking or sloped tiles.

{{< lookup/cref TestSpriteMove >}} is called on the tile directly below the player's position, testing the {{< lookup/cref name="DIR4" text="DIR4_SOUTH" >}} direction. This is verifying the attributes of the tile the actor is purportedly standing on, and a value greater than {{< lookup/cref name="MOVE" text="MOVE_FREE" >}} (so, {{< lookup/cref name="MOVE" text="MOVE_BLOCKED" >}} or {{< lookup/cref name="MOVE" text="MOVE_SLOPED" >}}) is expected here.

If the test passes, the actor is indeed standing on solid ground and no position adjustments are required. `westfree` is gratuitously reenabled -- it should already have a true value if this branch was reached.

More importantly, this branch prevents any of the subsequent cases from being tested or taking action.

#### Case 4: Descending a slope

```c
    } else if (
        TILE_SLOPED(GetMapTile(act->x + width, act->y + 1)) &&
        TILE_SLOPED(GetMapTile(act->x + width - 1, act->y + 2))
    ) {
        if (!TILE_BLOCK_SOUTH(GetMapTile(act->x + width - 1, act->y + 1))) {
            act->westfree = 1;
            if (!TILE_SLOPED(GetMapTile(act->x + width - 1, act->y + 1))) {
                act->y++;
            }
        }
```

This case handles the possibility that the actor is walking west down a slope. They have only moved in the horizontal direction thus far, and could now be "floating" one tile above the ground in their new position.

The two {{< lookup/cref GetMapTile >}} calls select two map tiles that are near the bottom-right tile of the actor sprite. The first tile is the one they walked off of, and the second tile is the piece of ground they are floating above. Each of these is verified to be sloped using the {{< lookup/cref TILE_SLOPED >}} macro, and if both are true this case is applicable.

A third map tile is considered with {{< lookup/cref GetMapTile >}}: the probably-empty tile the actor is floating above. The {{< lookup/cref TILE_BLOCK_SOUTH >}} macro checks that the tile at this position can be entered from above. If it is, it must also _not_ be sloped according to {{< lookup/cref TILE_SLOPED >}} before `y` is incremented to lower the actor to that position.

The assignment to `westfree` is redundant; it will already be set for this branch to be taken.

#### Case 5: Redundant ejection from a solid wall

```c
    } else if (act->westfree == 0) {
        act->x++;
```

This is a less-specific implementation of case 1, and should not be reachable if either case 1 or 2 occurs.

#### Case 6: Ledge aversion

```c
    } else if (
        !act->acrophile &&
        TestSpriteMove(
            DIR4_WEST, act->sprite, act->frame, act->x, act->y + 1
        ) == MOVE_FREE &&
        !TILE_SLOPED(GetMapTile(act->x + width - 1, act->y + 1))
    ) {
        act->x++;
        act->westfree = 0;
    }
```

If the actor does not have its `acrophile` flag set, it is unwilling to walk off ledges to intentionally fall. This case detects ledges and treats them similarly to impassable walls.

{{< lookup/cref TestSpriteMove >}} is called to test the position one tile below the actor's current position -- the surface they are standing on. If this returns {{< lookup/cref name="MOVE" text="MOVE_FREE" >}} there is nothing solid below them.

{{% note %}}
The {{< lookup/cref name="DIR4" text="DIR4_WEST" >}} direction is tested here rather than {{< lookup/cref name="DIR4" text="DIR4_SOUTH" >}}. This might be an oversight, since this does not match the condition tested in case 3 and could lead to inconsistent behavior.

There are a bit more than two dozen entries in the [tile attributes data]({{< relref "tile-attributes-format" >}}) that permit southern movement but block one or both of the horizontal directions. An enterprising map designer might be able to leverage these tiles to form a construction that non-acrophilic actors will willingly walk onto then immediately fall through.

That would be a mean thing to do to them.
{{% /note %}}

A second check is performed by calling {{< lookup/cref GetMapTile >}} on the tile below the actor's bottom-right corner tile. If the tile at this position is sloped according to {{< lookup/cref TILE_SLOPED >}}, the actor is actually standing on a slope and they're not technically floating -- do nothing in this case.

Otherwise, the actor has walked entirely off a ledge and is now in a _Wile E. Coyote_ state where the only thing keeping them from falling is the fact that they haven't looked down yet. This is handled similarly to the ejection case where the actor walked into a wall (see case 1): Unwind the move by pushing the actor back to the right by one tile (`x++`) and clear the `westfree` flag to indicate that an impassible area was encountered. This will leave a single tile at the actor's bottom-right corner sitting on solid ground (this is sufficient to stop them from falling), with the flag indicating that the actor should not try to walk west again.

#### Case 7: The last resort

Sometimes a call will make it all the way through the function without activating any cases. This would be an acrophilic actor that is not inside any wall or slope, not standing on the ground, and that had just moved horizontally. The only actor I have witnessed match all these preconditions is an {{< lookup/actor 86 >}} at the moment it rolls off a ledge. When this happens, no movement adjustment is performed here -- it falls from that position unimpeded.

### Eastern Movement

This code is structurally identical to the western branch with only symmetrical differences:

* `westfree` becomes `eastfree`
* {{< lookup/cref name="DIR4" text="DIR4_WEST" >}} becomes {{< lookup/cref name="DIR4" text="DIR4_EAST" >}}
* Increments and decrements to `act->x` are swapped
* Map slope intersection tests at the actor's right side change to the left side

```c
    result = TestSpriteMove(
        DIR4_EAST, act->sprite, act->frame, act->x, act->y);
    act->eastfree = !result;

    if (act->eastfree == 0 && result != MOVE_SLOPED) {
        act->x--;
    } else if (result == MOVE_SLOPED) {
        act->eastfree = 1;
        act->y--;
    } else if (TestSpriteMove(
        DIR4_SOUTH, act->sprite, act->frame, act->x, act->y + 1
    ) > MOVE_FREE) {
        act->eastfree = 1;
    } else if (
        TILE_SLOPED(GetMapTile(act->x - 1, act->y + 1)) &&
        TILE_SLOPED(GetMapTile(act->x, act->y + 2))
    ) {
        if (!TILE_BLOCK_SOUTH(GetMapTile(act->x, act->y + 1))) {
            act->eastfree = 1;
            if (!TILE_SLOPED(GetMapTile(act->x, act->y + 1))) {
                act->y++;
            }
        }
    } else if (act->eastfree == 0) {
        act->x--;
    } else if (
        !act->acrophile &&
        TestSpriteMove(
            DIR4_EAST, act->sprite, act->frame, act->x, act->y + 1
        ) == MOVE_FREE &&
        !TILE_SLOPED(GetMapTile(act->x, act->y + 1))
    ) {
        act->x--;
        act->eastfree = 0;
    }
```
