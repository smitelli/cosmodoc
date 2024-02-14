+++
title = "Spawner Functions"
description = "Describes the functions that create and process spawners that the player encounters throughout the maps."
weight = 490
+++

# Spawner Functions

A **spawner** is an animation effect that ultimately causes a new actor to be created in the game world. Spawners are represented as upside-down sprites that rise from an origin position until either a timer expires or they hit a solid map tile, at which point a true actor of the same type is created in that spot. The actor then falls back to the ground using its own sense of gravity.

The most common spawners the player interacts with are the prizes released from {{< lookup/actor type=69 plural=true >}} and destroyed barrels/baskets. The prize cannot be "grabbed" during the time when it is a spawner; the spawner must complete its lifecycle and become a true actor first. Similar limitations are in place for things like {{< lookup/actor type=86 plural=true >}} spawned from {{< lookup/actor type=152 plural=true >}} -- these do not truly become living actors until each spawner finishes its work.

{{< table-of-contents >}}

## Spawner Behavior

Spawners are created by using the {{< lookup/cref NewSpawner >}} function, passing a numeric actor type and an X/Y coordinate to start the animation from. The spawn animation begins at that position and moves up on the screen by two tiles during each frame of gameplay until it reaches the point 16 tiles above the starting position. At that time, the vertical speed slows to one tile per frame, and the spawner continues rising for an additional three tiles. If the spawner hits any north-blocking map tile before reaching its full height, the spawn animation ends early.

At the point where the animation ends, the spawner is removed and an actor of the same type is created in the same spot. This actor _should_ be one that experiences gravity, so it can fall back to the point where the spawner first started.

The spawner always uses frame zero from the sprite data, and passes the actor type unmodified into the sprite drawing functions. This means that the actor type number and the sprite type number should be the same (or use the same image data), and that frame zero of that sprite should be a reasonable representation of the actor that will be created. The sprite is drawn upside-down while spawning, then in a normal orientation while falling.

## Spawner Sources

The full list of game elements that can produce spawners is:

* {{< lookup/actor type=152 plural=true >}} spawn {{< lookup/actor type=86 plural=true >}}.
* The harder {{< lookup/actor 102 >}} (from episode three) spawns {{< lookup/actor type=86 plural=true >}} periodically.
* The {{< lookup/actor type=69 plural=true >}} release a random choice of {{< lookup/actor type=172 strip=true >}}, {{< lookup/actor type=34 strip=true >}}, {{< lookup/actor 176 >}}, or {{< lookup/actor 174 >}} each time one touches the player.
* Each {{< lookup/actor type=95 strip=true >}} spawns an {{< lookup/actor 57 >}} when bombed.
* The {{< lookup/actor type=143 strip=true >}} spawns a {{< lookup/actor 82 >}} when destroyed.
* {{< lookup/actor 221 >}} spawns a {{< lookup/actor 82 >}} after the player rescues him.
* When destroyed, each barrel and basket releases its prize using the spawner system.

{{< boilerplate/function-cref InitializeSpawners >}}

The {{< lookup/cref InitializeSpawners >}} function clears all of the memory slots used to store spawner state, immediately terminating all incomplete spawner animations and making each slot available for use.

```c
void InitializeSpawners(void)
{
    word i;

    for (i = 0; i < numSpawners; i++) {
        spawners[i].actor = ACT_BASKET_NULL;
    }
}
```

The {{< lookup/cref numSpawners >}} variable always holds the value from the constant {{< lookup/cref MAX_SPAWNERS >}}, which is 6 regardless of the episode, level, or state of the current map. In the outermost `for` loop, `i` increments from zero to five, covering every spawner slot.

The {{< lookup/cref spawners >}} array maintains a list of {{< lookup/cref Spawner >}} structures, each one having an `actor` member variable. Spawners use the `actor` variable to select which sprite to draw and to know which actor to ultimately create at the end. Idle spawners are expressed by having an `actor` of {{< lookup/cref name="ACT" text="ACT_BASKET_NULL" >}} -- essentially zero, which is assigned to the spawner slot on each iteration.

{{< note >}}{{< lookup/cref name="ACT" text="ACT_BASKET_NULL" >}} is not an actor that should ever be present in a map or created dynamically during the game. It is a sentinel value that acts weird if actually created. See the [unused actors page]({{< relref "unused-actors" >}}).{{< /note >}}

At completion, all spawners will be reset to their idle state, ready to be activated at some future time.

{{< boilerplate/function-cref NewSpawner >}}

The {{< lookup/cref NewSpawner >}} function creates a new instance of a spawner at the passed `x_origin` and `y_origin` map tile coordinates and sets the animation up to run. `actor_type` controls _both_ the type of actor that will be created when the spawner completes, and the sprite type that will be drawn while the spawner is running.

{{< note >}}If there is no room in the {{< lookup/cref spawners >}} array (due to too many spawners already running) this function does nothing.{{< /note >}}

As with all sprite-related functions, the X/Y origin tile is the bottom-left tile of the sprite image.

```c
void NewSpawner(word actor_type, word x_origin, word y_origin)
{
    word i;

    for (i = 0; i < numSpawners; i++) {
        Spawner *sp = spawners + i;
```

The `for` loop iterates over every spawner slot in memory, up to the fixed limit in {{< lookup/cref numSpawners >}}. On each iteration, one {{< lookup/cref Spawner >}} structure is loaded from the {{< lookup/cref spawners >}} array into `sp`. With that done, the `i` iterator isn't needed again until the loop repeats.

```c
        if (sp->actor != ACT_BASKET_NULL) continue;
```

Spawners use the impossible `actor` value {{< lookup/cref name="ACT" text="ACT_BASKET_NULL" >}} to represent a spawner slot that is not in active use. If the current slot has any other `actor` value, we don't want to overwrite that. `continue` to the next slot and try again.

```c
        sp->actor = actor_type;
        sp->x = x_origin;
        sp->y = y_origin;
        sp->age = 0;

        break;
    }
}
```

Otherwise, the current slot holds no active spawner, so we can use it to hold a new one. The caller-provided `actor_type`, `x_origin`, and `y_origin` are saved in `sp`'s `actor`, `x`, and `y` members, and the spawner's `age` is set to zero to prepare it to run a complete animation cycle.

With the new spawner created, no further slots need to be examined and the outer `for` loop ends with `break`.

If the `for` loop runs to exhaustion without finding a suitable slot for the new spawner, this function silently returns without modifying anything.

{{< boilerplate/function-cref MoveAndDrawSpawners >}}

The {{< lookup/cref MoveAndDrawSpawners >}} function moves and draws the sprites for all spawners that are currently active. When a spawner animation ends (either due to finishing the animation or hitting a solid map tile) its slot is marked inactive and a new actor is created in the spawner's final position.

```c
void MoveAndDrawSpawners(void)
{
    word i;

    for (i = 0; i < numSpawners; i++) {
        Spawner *sp = spawners + i;
```

The `for` loop iterates over every spawner slot in memory, up to the fixed limit in {{< lookup/cref numSpawners >}}. On each iteration, one {{< lookup/cref Spawner >}} structure is loaded from the {{< lookup/cref spawners >}} array into `sp`. With that done, the `i` iterator isn't needed again until the loop repeats.

```c
        if (sp->actor == ACT_BASKET_NULL) continue;

        sp->age++;
```

Spawners use the impossible `actor` value {{< lookup/cref name="ACT" text="ACT_BASKET_NULL" >}} to represent a spawner slot that is not in active use. If the current slot matches that value, there is no active spawner in the current slot. `continue` to the next one and try again.

Otherwise, the spawner's `age` is unconditionally incremented. This occurs once per frame (or **tick**) of gameplay.

```c
        if (
            TestSpriteMove(
                DIR4_NORTH, sp->actor, 0, sp->x, --sp->y
            ) != MOVE_FREE ||
            (
                sp->age < 9 &&
                TestSpriteMove(
                    DIR4_NORTH, sp->actor, 0, sp->x, --sp->y
                ) != MOVE_FREE
            )
        ) {
            NewActor(sp->actor, sp->x, sp->y + 1);
            DrawSprite(sp->actor, 0, sp->x, sp->y + 1, DRAW_MODE_NORMAL);
            sp->actor = ACT_BASKET_NULL;
```

There's a lot going on in the `if`'s test expression that has some subtle behaviors. In a certain light, there is an elegance to it.

First and foremost, there is a pre-decrement `--sp->y` inside the arguments in the first call to {{< lookup/cref TestSpriteMove >}}. That always runs no matter what the test results are, which moves the spawner one tile up on the screen. {{< lookup/cref TestSpriteMove >}} is being asked if sprite type `sp->actor`, frame zero, at the new X/Y position was permitted to move up ({{< lookup/cref name="DIR4" text="DIR4_NORTH" >}}) into that tile's space. If the call returns anything other than {{< lookup/cref name="MOVE" text="MOVE_FREE" >}}, the spawner has entered the ceiling by moving into this position. When this happens, the `if` test **short-circuits** and the remaining code after the logical OR "`||`" does not execute. It instead jumps straight into the `if` branch's body.

On the other hand, if the first Y decrement didn't enter the ceiling we get to do the rest of the tests. If the spawner's `age` is nine or above, the code short-circuits _again_ and the `if` body is skipped. Conversely, when `age` is less than nine, there is another pre-decrement `--sp->y` inside another {{< lookup/cref TestSpriteMove >}} which works identically to the one that was just done. This moves the spawner up on the screen another tile, with an associated check for entering the ceiling.

The end result: When `age` is between one and eight, the spawner moves up two tiles each tick. When `age` is nine or above, the spawner moves up only one tile per tick. Every tile position is checked, and the `if` body here executes any time the ceiling is breached. _The `if`'s test expression always moves the spawner, even when its branch isn't taken._

With the ceiling hit, the spawner's life is over and it's time to bring in an actor to replace it. {{< lookup/cref NewActor >}} is called with the spawner's `actor`, `x`, and `y + 1` values. The Y value needs the correction by one because the spawner is currently at least partially inside the ceiling -- that's how we got into this `if` body. Adding one backs it up to the point where it wasn't intersecting the map.

The new actor now exists, but won't get drawn until the next tick of the game loop. To bridge that gap, one final {{< lookup/cref DrawSprite >}} call draws the spawner sprite in the same position where the actor was created -- with Y adjusted by one for the same reason. This is drawn right-side up ({{< lookup/cref name="DRAW_MODE" text="DRAW_MODE_NORMAL" >}}).

To finally clean up the spawner, `sp->actor` is set to {{< lookup/cref name="ACT" text="ACT_BASKET_NULL" >}} to mark the spawner slot as no longer in use.

```c
        } else if (sp->age == 11) {
            NewActor(sp->actor, sp->x, sp->y);
            DrawSprite(sp->actor, 0, sp->x, sp->y, DRAW_MODE_FLIPPED);
            sp->actor = ACT_BASKET_NULL;
```

The `else if` here is evaluated in cases where the spawner did not move into any of the ceilings. This simply checks for the case where the spawner has reached its maximum `age` by running for 11 ticks. If that has happened, the spawner is replaced with an actor in a manner quite similar to the previous branch. The difference here is that Y is _not_ corrected by one, because we do not need to unwind an errant move inside a ceiling.

The sprite here also uses {{< lookup/cref name="DRAW_MODE" text="DRAW_MODE_FLIPPED" >}} to draw upside-down, which feels perhaps like a small visual inconsistency relative to the previous branch.

```c
        } else {
            DrawSprite(sp->actor, 0, sp->x, sp->y, DRAW_MODE_FLIPPED);
        }
    }
}
```

The remaining `else` case is a catch-all. The spawner did not hit any ceilings, and it is not old enough to age out, so the only thing to do is draw it at the current location. {{< lookup/cref DrawSprite >}} does this in the {{< lookup/cref name="DRAW_MODE" text="DRAW_MODE_FLIPPED" >}} style.

The enclosing `for` loop repeats until all spawner slots have been examined, then this function returns.
