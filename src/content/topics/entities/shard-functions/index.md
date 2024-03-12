+++
title = "Shard Functions"
description = "Describes the functions that create and process shards that accompany destruction of actors on the map."
weight = 540
+++

# Shard Functions

A **shard** is a small piece of debris released from a destroyed actor, usually in response to an explosion. Unlike [decorations]({{< relref "decoration-functions" >}}), shards are pulled downward by gravity and interact with solid tiles in the [map data]({{< relref "map-format" >}}). Typically multiple shards will be released simultaneously by the same event, and each one moves somewhat chaotically in a unique direction.

{{< table-of-contents >}}

## A Look at Shards

The most direct way to encounter a shard is to make the player pounce on a barrel or basket. When such items are destroyed, four thin shards are released. It's also common to see shards after blowing an actor up with a bomb, which tends to release one or more shards as they die. Shards are created at the point of destruction and move outward from there. Their sprites are always drawn upside-down, except for the very first frame of animation which is a white outline oriented normally.

A shard has a fixed horizontal movement component called the **X mode** that is chosen at creation time and does not change. Movement along this axis could be zero. As long as the shard is able to move in its assigned horizontal direction without hitting a solid map tile, it will. Vertically, the shard starts moving up at two tiles per game tick until it reaches a point eight tiles above its starting point, at which point it rises one more tile. It then stays suspended in air for two more ticks. Gravity begins to take over, and the shard moves down one tile on the next tick, followed by two tiles on every subsequent tick thereafter.

Each shard can bounce off the ground _exactly once_ as it falls, where it will again rise five tiles back up in the air before repeating its fall behavior. Once it hits the ground the second time, it will continue falling down through the solid tiles in the floor until it leaves the screen entirely.

{{< image src="shard-paths-2052x.png"
    alt="Diagram of the origin and different paths taken by each shard variant."
    1x="shard-paths-684x.png"
    2x="shard-paths-1368x.png"
    3x="shard-paths-2052x.png" >}}

Most wall and floor tiles have the "in-front" [tile attribute]({{< relref "tile-attributes-format" >}}) bit set, which prevents the shard from being seen as it falls through the floor. Typically each shard will appear to be absorbed into the ground as it finishes its lifecycle. Shards are removed after their age exceeds 16 ticks (when out of view) or 40 ticks (if the player is following one of them).

Shards do not test for intersection with map tiles as they rise, which can lead to unintuitive behavior: If a shard enters a wall or ceiling where it cannot free-fall out, a sort of pseudo-bounce occurs which ejects the shard three tiles higher on the map, where it tries to fall again. This adjustment could potentially happen an unbounded number of times, even going as far as to bounce the shard into a negative Y position off the top of the map.

{{% aside class="fun-fact" %}}
**You wanna see?**

This ejection logic is actually apparent in the recorded demo data that ships with episode one. During the playback of E1M8, as the player bombs the {{< lookup/actor type=121 strip=true >}} to get it moving, a {{< lookup/actor 69 >}} is caught in the blast. Its shard leaves the top of the screen, and then almost three seconds later falls back past its starting elevation.

What happens in that case is, the shard reaches its regular apex inside the ceiling, is further ejected up into the empty space in the room above, falls to the floor of that upper area, audibly bounces, then falls back through the floor again down to the original height where it first came from. The solid tiles it passes through have a random assortment of [block-west/block-east]({{< relref "tile-attributes-format#movement-blocking" >}}) behaviors, which keeps the decoration from moving as far horizontally as it might in clear space.

The timing is fortunate as well, because if the shard were off the screen for one or two more ticks it would've been removed due to being out of view for too long.
{{% /aside %}}

{{< boilerplate/function-cref InitializeShards >}}

The {{< lookup/cref InitializeShards >}} function clears all of the memory slots used to store shard state, immediately terminating all incomplete shard animations and making each slot available for use.

```c
void InitializeShards(void)
{
    word i;

    for (i = 0; i < numShards; i++) {
        shards[i].age = 0;
    }
}
```

The {{< lookup/cref numShards >}} variable always holds the value from the constant {{< lookup/cref MAX_SHARDS >}}, which is 16 regardless of the episode, level, or state of the current map. In the outermost `for` loop, `i` increments from zero to 15, covering every shard slot.

The {{< lookup/cref shards >}} array maintains a list of {{< lookup/cref Shard >}} structures, each one having an `age` member variable. As a shard runs, its `age` increments until it reaches a maximum, at which time it becomes idle again. Idle shards are expressed by having an `age` of zero, which is set by the assignment here.

When this function returns, all shards will be reset to their idle state, ready to be activated at some future time.

{{< boilerplate/function-cref NewShard >}}

The {{< lookup/cref NewShard >}} function creates a new shard at `x_origin` and `y_origin` consisting of the passed `sprite_type` and `frame`. The shard will be assigned a random-seeming but predictable horizontal movement mode.

{{% note %}}If there is no room in the {{< lookup/cref shards >}} array (due to too many shards already running) this function does nothing.{{% /note %}}

```c
void NewShard(word sprite_type, word frame, word x_origin, word y_origin)
{
    static word xmode = 0;
    word i;

    xmode++;
    if (xmode == 5) xmode = 0;
```

Horizontal movement of a shard is controlled by a cyclical `xmode` value. The first shard created will receive an `xmode` of one, and each subsequent shard receives the next sequential `xmode`. After the `xmode = 4` shard is created, the value resets to zero for the next shard. The pattern repeats every five shards. The `xmode` behavior is:

`xmode` | Horizontal Behavior
--------|--------------------
0       | Shard moves to the east.
1       | Shard moves to the west.
2       | Shard has no movement in the horizontal direction.
3       | Shard moves to the east at double speed.
4       | Shard moves to the west at double speed.

{{% note %}}`xmode` is a function-`static` variable that cannot be explicitly reset. This means that it is possible for repeated playbacks of identical demo data to have different shard behavior. To guarantee deterministic playback of a demo's shards, it's necessary to quit to DOS and restart the game before each run.{{% /note %}}

```c
    for (i = 0; i < numShards; i++) {
        Shard *sh = shards + i;
```

The outermost `for` loop runs once for each shard slot, up to {{< lookup/cref numShards >}}. Within the loop, `sh` points to the {{< lookup/cref Shard >}} structure from the {{< lookup/cref shards >}} array that's currently being processed. Once a shard reference has been obtained, the index `i` is not used again until the next iteration.

```c
        if (sh->age != 0) continue;
```

Each shard uses the `age` member variable to track its overall lifecycle. If a shard has a nonzero `age`, it indicates that the current slot holds an shard that is still progressing and should not be overwritten. In this case, the loop `continue`s onto the next slot, hopefully eventually finding one with an inactive shard.

```c
        sh->sprite = sprite_type;
        sh->x = x_origin;
        sh->y = y_origin;
        sh->frame = frame;
        sh->age = 1;
        sh->xmode = xmode;
        sh->bounced = false;

        break;
    }
}
```

Otherwise, the current slot holds no active shard, so we can use it to hold a new one. The caller-provided `sprite_type`, `x_origin`, `y_origin`, and `frame` are saved in `sh`'s `sprite`, `x`, `y`, and `frame` members, the generated `xmode` is copied, the shard's `age` is set to one to prepare it to run its animation cycle, and `bounced` is initialized to false.

With the new shard created, no further slots need to be examined and the outer `for` loop ends with `break`.

If the `for` loop runs to exhaustion without finding a suitable slot for the new shard, this function silently returns without modifying anything.

{{< boilerplate/function-cref MoveAndDrawShards >}}

The {{< lookup/cref MoveAndDrawShards >}} function moves and draws the sprites for all shards that are currently active. When a shard animation ends its slot is marked inactive.

In this function, each shard may play the {{< lookup/cref name="SND" text="SND_SHARD_BOUNCE" >}} sound effect even if its sprite is not within the visible area of the map at that time.

```c
void MoveAndDrawShards(void)
{
    word i;

    for (i = 0; i < numShards; i++) {
        Shard *sh = shards + i;
```

The `for` loop iterates over every shard slot in memory, up to the fixed limit in {{< lookup/cref numShards >}}. On each iteration, one {{< lookup/cref Shard >}} structure is loaded from the {{< lookup/cref shards >}} array into `sh`. With that done, the `i` iterator isn't needed again until the loop repeats.

```c
        if (sh->age == 0) continue;
```

Each shard uses the `age` member variable to track its overall lifecycle. If a shard has an `age` of zero, it indicates that the current slot holds a shard that is not currently active and should not be drawn. In this case, the loop `continue`s onto the next slot, looking for a shard that's ready to be drawn.

```c
        if (sh->xmode == 0 || sh->xmode == 3) {
            if (TestSpriteMove(
                DIR4_EAST, sh->sprite, sh->frame, sh->x + 1, sh->y + 1
            ) == MOVE_FREE) {
                sh->x++;

                if (sh->xmode == 3) {
                    sh->x++;
                }
            }
```

This is half of the horizontal movement code, specifically the portion that handles shards that move toward the right on the screen. These have an `xmode` of 0 for the lower velocity shards, and 3 for those that move twice as fast.

{{< lookup/cref TestSpriteMove >}} tests if a move in the {{< lookup/cref name="DIR4" text="DIR4_EAST" >}} direction is permitted. `sh->sprite` and `sh->frame` need to be passed so the function can determine the sprite's overall height, testing the entire right side and not just the X and Y origin positions.

On the topic of origins, the horizontal component is `sh->x + 1`, which is one tile to the right of the shard's current location. This is sensible, because the intention is to check for obstructions in the location where it wants to move, not the location where it already is. Vertically, `sh->y + 1` makes a bit less sense. This shifts all of the movement calculations as if the sprite were planning on moving down one tile, but that is not always what it does -- it can move anywhere from -2 to 2 tiles vertically each tick. This tends to work "well enough," although a side-effect is that a shard that is created at ground level will usually not move horizontally on its first tick, due to most ground tiles prohibiting east/west movement in addition to south.

{{< lookup/cref TestSpriteMove >}} returns {{< lookup/cref name="MOVE" text="MOVE_FREE" >}} if there is enough clearance at the target position for the sprite to move there. In that case, `sh->x` is incremented to make it so.

When `xmode` is 3, the shard is moving at double speed horizontally and `sh->x` is incremented again. **This causes a bug from time to time.** Earlier {{< lookup/cref TestSpriteMove >}} was used to check for the legality of a move one tile to the right, but we never checked _two_ tiles to the right before moving here. These double-speed shards move horizontally in even tile increments, but if one happens to hit a wall an odd distance away it will partially enter the wall. This tends to get the vertical-handling code stuck in an ejection loop, continually walking the shard up the wall until it reaches some empty space.

```c
        } else if (sh->xmode == 1 || sh->xmode == 4) {
            if (TestSpriteMove(
                DIR4_WEST, sh->sprite, sh->frame, sh->x - 1, sh->y + 1
            ) == MOVE_FREE) {
                sh->x--;

                if (sh->xmode == 4) {
                    sh->x--;
                }
            }
        }
```

This is practically identical to the previous branch, but with {{< lookup/cref name="DIR4" text="DIR4_WEST" >}} movement to support `xmode` 1 and 4 and decreasing values for X.

`xmode` 2 does not match either branch, resulting in absolutely no horizontal movement over the lifetime of those types of shards.

```c
restart:
        if (sh->age < 5) {
            sh->y -= 2;
        }

        if (sh->age == 5) {
            sh->y--;
        } else if (sh->age == 8) {
            if (TestSpriteMove(
                DIR4_SOUTH, sh->sprite, sh->frame, sh->x, sh->y + 1
            ) != MOVE_FREE) {
                sh->age = 3;
                sh->y += 2;
                goto restart;
            }

            sh->y++;
        }
```

Note the `restart:` label at the beginning of this code. Anything that makes the shard "bounce" will jump back to that label to immediately restart vertical processing from the beginning.

The first `if` handles the initial four ticks of the shard's life. On each tick, the shard unconditionally rises by two tiles. No attention is paid to intersection with any map tiles. On the fifth tick, the rise rate slows to one tile.

During ticks six and seven, none of the conditions match and the sprite "hangs" at the same vertical position.

On tick eight, it's time to start coming back down, and it's the first time when we start to pay attention to whether or not the map tiles permit the move. {{< lookup/cref TestSpriteMove >}} checks if a move is permitted to the tile directly below the shard in the {{< lookup/cref name="DIR4" text="DIR4_SOUTH" >}} direction. If it is, the return value is {{< lookup/cref name="MOVE" text="MOVE_FREE" >}} and `sh->y` is incremented to move the shard to that spot.

If the move is _not_ permitted, we have a bit of a problem -- apparently the shard moved up into some arrangement of solid map tiles, and now there is no way back down without some part of its sprite getting hung up on a tile that prevents downward movement. To aimlessly stumble out of this, `sh->age` is rewound back to 3 -- putting the shard back into the state where it moves up by two tiles per tick. The shard is then moved _down_ by two tiles, then we `goto restart`. Back at the top, with `age` below five, the shard is moved back _up_ two tiles, canceling out the move it made immediately before the `goto`, and life goes on. The shard will repeat ticks four and five (moving up three tiles in the process) and end up back in the {{< lookup/cref name="DIR4" text="DIR4_SOUTH" >}}-checking code on tick eight. This can happen perpetually because `age` keeps getting reset, with the shard rising in spurts until it finds a clear area to release it.

Shards tend to enter and hop up walls when `xmode` is 3 or 4, due to the horizontal code failing to adequately test the legality of high-velocity moves.

```c
        if (sh->age >= 9) {
            if (
                sh->age > 16 &&
                !IsSpriteVisible(sh->sprite, sh->frame, sh->x, sh->y)
            ) {
                sh->age = 0;
                continue;
            }
```

Once a shard's `age` reaches nine ticks, it's falling at full speed. If the shard is more than 16 ticks old and {{< lookup/cref IsSpriteVisible >}} reports that no part of it is still on the screen, the shard is considered expired and is removed by setting `age` back to zero. It will not be processed further, and any new shard is free to occupy the slot.

With nothing left to do on this one, execution `continue`s onto the next shard slot.

Otherwise, we keep going and let the shard fall a bit.

```c
            if (!sh->bounced && TestSpriteMove(
                DIR4_SOUTH, sh->sprite, sh->frame, sh->x, sh->y + 1
            ) != MOVE_FREE) {
                sh->age = 3;
                sh->bounced = true;
                StartSound(SND_SHARD_BOUNCE);
                goto restart;
            }

            sh->y++;
```

Shards with a `bounced` flag set to false have not yet hit the ground. {{< lookup/cref TestSpriteMove >}} looks one tile below `sh->y` to see if there is a tile at that location that prevents objects from entering it in the {{< lookup/cref name="DIR4" text="DIR4_SOUTH" >}} direction. If that call returns anything other than {{< lookup/cref name="MOVE" text="MOVE_FREE" >}}, there is a movement-blocking tile directly under the shard -- it is effectively sitting on the ground.

With ground contact detected, the shard's `age` is rewound to 3 to return it to the state where it had upward movement. (Skipping the first two `age` ticks takes away some of the shard's "momentum" so it doesn't rise quite as high.) The `bounced` flag is set to true so this can only happen one time, {{< lookup/cref StartSound >}} queues the {{< lookup/cref name="SND" text="SND_SHARD_BOUNCE" >}} sound effect, and we `goto restart` to immediately restart the movement calculations using this new shard age.

Otherwise, {{< lookup/cref TestSpriteMove >}} returned {{< lookup/cref name="MOVE" text="MOVE_FREE" >}}, indicating that there is nothing below the shard but open air. Increment `sh->y` to move the shard down one tile.

```c
            if (!sh->bounced && TestSpriteMove(
                DIR4_SOUTH, sh->sprite, sh->frame, sh->x, sh->y + 1
            ) != MOVE_FREE) {
                sh->age = 3;
                sh->bounced = true;
                StartSound(SND_SHARD_BOUNCE);
                goto restart;
            }

            sh->y++;
        }
```

This is exactly the same code again. Shards that are at least nine ticks old always fall by two tiles each frame, so the ground tests, bounce logic, and position adjustments all happen twice in a row.

```c
        if (sh->age == 1) {
            DrawSprite(
                sh->sprite, sh->frame, sh->x, sh->y, DRAW_MODE_WHITE
            );
        } else {
            DrawSprite(
                sh->sprite, sh->frame, sh->x, sh->y, DRAW_MODE_FLIPPED
            );
        }
```

Unless the shard expired and had its `age` set to zero, all shards will end up at these {{< lookup/cref DrawSprite >}} calls. This simply renders the shard sprite at the most up-to-date `sh->x` and `sh->y` positions within the map. Most shards are drawn upside-down using {{< lookup/cref name="DRAW_MODE" text="DRAW_MODE_FLIPPED" >}}, but the very first tick of a new shard is drawn as a (right side up) {{< lookup/cref name="DRAW_MODE" text="DRAW_MODE_WHITE" >}} outline.

```c
        sh->age++;
        if (sh->age > 40) sh->age = 0;
    }
}
```

Each time a shard is drawn, its `age` increases by one. If the `age` should exceed 40 at any point, regardless of visibility or state, it is removed from the world by setting `sh->age` to zero. Note that this isn't an absolute guarantee that every shard will expire at a predictable rate -- shards stuck in an ejection loop will continually have their `age` reset to 3 before they come anywhere near satisfying this test.

The outer `for` loop continues running until all shard slots have been examined, and then the function returns.
