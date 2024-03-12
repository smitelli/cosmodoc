+++
title = "Actor Initialization Functions"
linkTitle = "Initialization Functions"
description = "Describes the different paths taken to create actor objects from map data as well as dynamic insertion during gameplay."
weight = 470
+++

# Actor Initialization Functions

Every actor encountered during the game was initialized and inserted into the game world using a small group of common functions. This page describes the actions performed as each actor is created, either statically by the map's original author or dynamically during the course of gameplay.

{{< table-of-contents >}}

To create an actor, three pieces of information are needed: the actor type number, the X origin tile on the map, and the Y origin.

The actor type number represents the complete identity and behavior of the actor. All actors with the same type number look and act the same, begin in the same state, and have the same difficulty. There is no way to customize a particular instance of an actor without duplicating it to a new actor type number.

The X and Y coordinates of an actor refer to the tile at the bottom-left of their sprite, measured from the upper-left corner of the map. Several actors have some amount of **X** and **Y Shift** that adjusts their initial position away from the location where their creation was requested. This may be done for centering purposes or to make map authoring easier, and should be considered whenever an actor is created -- a nonzero shift value will place the actor in a slightly different place than the function calls requested.

There are two paths that can be taken to insert an actor into the game world:

```goat
+---------------+     +----------------------+
|               |     |                      +------------------------------------------------> Special Actor
| LoadMapData() +---->| NewMapActorAtIndex() +-.
|               |     |                      |  \   +-------------------+     +------------------+
+---------------+     +----------------------+   .->|                   |     |                  |
                                                    | NewActorAtIndex() +---->| ConstructActor() +----> Actor
+------------+                                   .->|                   |     |                  |
|            |                                  /   +-------------------+     +------------------+
| NewActor() +---------------------------------.
|            |
+------------+
```

* When a map is first loaded into memory, {{< lookup/cref LoadMapData >}} parses the [list of actors]({{< relref "map-format#list-of-actors" >}}) in the file and calls {{< lookup/cref NewMapActorAtIndex >}} for each actor encountered in the file. Depending on the map actor type, either a **special actor** will be created directly, or {{< lookup/cref NewActorAtIndex >}} will be called to create a normal actor. Special actors are those with a map actor type less than 31.
* When an actor needs to be dynamically created during the course of the game, {{< lookup/cref NewActor >}} is used. This directly calls {{< lookup/cref NewActorAtIndex >}}. (N.B.: It is not possible to create a special actor using this dynamic path.)

{{< lookup/cref NewActorAtIndex >}} is the common function that all normal (that is, not special) actors pass through, while {{< lookup/cref ConstructActor >}} is the function responsible for actually initializing an actor's data.

The actor list in memory is built and maintained using {{< lookup/cref numActors >}} as an index pointer. The actor list begins in an empty state, and map-defined actors are inserted at sequentially increasing index positions. Once map loading is complete, the {{< lookup/cref numActors >}} index points to the first slot in the array where no actor has yet been created.

When additional actors are created dynamically, a two-step approach is used. First the actor list is traversed from element zero up to {{< lookup/cref numActors >}}, looking for any actor that has been marked as dead. If one is located, the new actor replaces the dead one and searching ends. If no dead actor slots were encountered, the new actor is inserted at the {{< lookup/cref numActors >}} position and the index pointer advances. {{< lookup/cref numActors >}} does not decrement as actors die, and it does not increment if a new actor reuses a previously-occupied slot. {{< lookup/cref numActors >}} essentially represents the peak "high water mark" of actor memory usage.

The two `...AtIndex()` functions rely on their callers to determine appropriate index positions, whether at the end of the actor list or somewhere in the middle.

{{< boilerplate/function-cref NewMapActorAtIndex >}}

The {{< lookup/cref NewMapActorAtIndex >}} function creates actors and special actors based on the passed `map_actor_type`. For normal actors, `index` controls the position in the actors array where the new actor will be created; for special actors it does nothing. For both actor kinds, `x_origin` and `y_origin` control the actor's initial position within the map.

As implemented, there is an overlap between the two actor kinds: When `map_actor_type` is 31, it is processed by both the special _and_ the normal actor code. The special actor code does nothing as there is no matching `case` for this value. The normal actor code inserts an actor of type zero, which is a [buggy]({{< relref "unused-actors" >}}) {{< lookup/cref name="ACT" text="ACT_BASKET_NULL" >}} type.

```c
void NewMapActorAtIndex(
    word index, word map_actor_type, word x_origin, word y_origin
) {
    if (map_actor_type < 32) {
        switch (map_actor_type) {
```

Special actors are those with a `map_actor_type` less than 32. For each entry in a map's [list of actors]({{< relref "map-format#list-of-actors" >}}), a `switch` decodes any special actors encountered.

Each special actor handling block ends with a `break` that jumps to the closing `switch` brace.

```c
        case SPA_PLAYER_START:
            if (x_origin > mapWidth - 15) {
                scrollX = mapWidth - SCROLLW;
            } else if ((int)x_origin - 15 >= 0 && mapYPower > 5) {
                scrollX = x_origin - 15;
            } else {
                scrollX = 0;
            }

            if ((int)y_origin - 10 >= 0) {
                scrollY = y_origin - 10;
            } else {
                scrollY = 0;
            }

            playerX = x_origin;
            playerY = y_origin;

            break;
```

For the {{< lookup/cref name="SPA" text="SPA_PLAYER_START" >}} case, the **SP**ecial **A**ctor represents a {{< lookup/special-actor 0 >}}. This requires a bit of [view centering]({{< relref "view-centering#level-start" >}}), followed simply by setting {{< lookup/cref playerX >}} and {{< lookup/cref playerY >}} to the associated `x_origin` and `y_origin` read from the map.

```c
        case SPA_PLATFORM:
            platforms[numPlatforms].x = x_origin;
            platforms[numPlatforms].y = y_origin;
            numPlatforms++;

            break;
```

Each {{< lookup/cref name="SPA" text="SPA_PLATFORM" >}} creates and sets the initial position of one of the {{< lookup/special-actor type=1 plural=true >}}.

At any given time, {{< lookup/cref numPlatforms >}} represents the total number of platforms that have been defined on the map, and it _also_ represents the index of the first unused element in the {{< lookup/cref platforms >}} array. This position contains an uninitialized {{< lookup/cref Platform >}} structure that gets filled with the corresponding `x`/`y_origin` values here. {{< lookup/cref numPlatforms >}} is then incremented to point to the next free slot in preparation for another platform, should one come.

```c
        case SPA_FOUNTAIN_SMALL:
        case SPA_FOUNTAIN_MEDIUM:
        case SPA_FOUNTAIN_LARGE:
        case SPA_FOUNTAIN_HUGE:
            fountains[numFountains].x = x_origin - 1;
            fountains[numFountains].y = y_origin - 1;
            fountains[numFountains].dir = DIR4_NORTH;
            fountains[numFountains].stepcount = 0;
            fountains[numFountains].height = 0;
            fountains[numFountains].stepmax = map_actor_type * 3;
            fountains[numFountains].delayleft = 0;
            numFountains++;

            break;
```

There are four different types of {{< lookup/special-actor type=3 strip=true >}} represented by {{< lookup/cref name="SPA" text="SPA_FOUNTAIN_SMALL/MEDIUM/LARGE/HUGE" >}}. They are all handled identically, aside from a difference in the `stepmax` member.

The use of {{< lookup/cref numFountains >}} to index into the {{< lookup/cref fountains >}} array mirrors the approach taken above for {{< lookup/cref name="SPA" text="SPA_PLATFORM" >}}.

The `stepcount`, `height`, and `delayleft` members are all initialized to zero, and `dir` takes the value {{< lookup/cref name="DIR4" text="DIR4_NORTH" >}}. This starts every fountain at its lowest possible position, with its initial move being in the north direction.

The `x` and `y` members are set to `x_origin - 1` and `y_origin - 1`; this represents an X and Y shift of -1 in each dimension. This places the fountain's true origin sightly above and to the left of its placed position. (See {{< lookup/cref MoveFountains >}} for details about how the fountains are drawn, and how their sense of origin is unusual compared to most actors.) `stepmax` represents the maximum height the fountain should reach (in tiles), which is set to three times the `map_actor_type` passed to this function. Fountains are represented by map actor types 2--5, producing heights in the range 6--15.

```c
        case SPA_LIGHT_WEST:
        case SPA_LIGHT_MIDDLE:
        case SPA_LIGHT_EAST:
            if (numLights == MAX_LIGHTS - 1) break;

            lights[numLights].side = map_actor_type - SPA_LIGHT_WEST;
            lights[numLights].x = x_origin;
            lights[numLights].y = y_origin;
            numLights++;

            break;
        }
    }
```

The three {{< lookup/special-actor type=6 strip=true >}} types are represented by {{< lookup/cref name="SPA" text="SPA_LIGHT_WEST/MIDDLE/EAST" >}} and the code here is substantially similar to that of the fountains. This is the only group of special actor types that guards against buffer overflow (here testing {{< lookup/cref numLights >}} against {{< lookup/cref MAX_LIGHTS >}}` - 1` and `break`ing if the limit has been reached).

To normalize `map_actor_type` (which is 6 for {{< lookup/cref name="SPA" text="SPA_LIGHT_WEST" >}}) into a `side` value (zero for {{< lookup/cref name="LIGHT_SIDE" text="LIGHT_SIDE_WEST" >}}) we subtract {{< lookup/cref name="SPA" text="SPA_LIGHT_WEST" >}} from `map_actor_type`.

`x` and `y` need no correction and can use `x_origin` and `y_origin` unmodified.

```c
    if (map_actor_type < 31) return;

    if (NewActorAtIndex(index, map_actor_type - 31, x_origin, y_origin)) {
        numActors++;
    }
}
```

The intention of the first `if` is to `return` from the function early if `map_actor_type` was low enough to be handled by the special actor `switch` block above. There is an overlap when `map_actor_type` equals 31 -- both sections of the code handle this case, but only the normal actor code performs an action in response. It is for that reason that this project considers map actor type 31 to be a normal actor, with the highest special actor type being 30.

With `map_actor_type` having a value 31 or greater, the first `if` takes no action and {{< lookup/cref NewActorAtIndex >}} gets called with `map_actor_type - 31` as its actor type. This removes the bias used by special actors, and allows all normal actors from type zero and up to be accessed. `index`, `x_origin`, and `y_origin` are passed through unchanged.

{{< lookup/cref NewActorAtIndex >}} will return true as long as the passed actor type is a defined actor type. In that case, {{< lookup/cref numActors >}} is incremented to reflect the new number of actors.

{{% note %}}When {{< lookup/cref LoadMapData >}} calls this function, it passes the current value stored at {{< lookup/cref numActors >}} as `index`. {{< lookup/cref LoadMapData >}} is also responsible for checking if the {{< lookup/cref MAX_ACTORS >}} limit has been breached. This split responsibility can be difficult to keep track of at times.{{% /note %}}

{{< boilerplate/function-cref NewActor >}}

The {{< lookup/cref NewActor >}} function dynamically inserts a new actor having the specified `actor_type` into the game world at the location specified by `x_origin` and `y_origin`. This function's search algorithm operates in two stages, first scanning through the occupied slots in the actor array looking for any actor that has become dead and replacing it with the new actor. If no such slot is found, the new actor is added at the {{< lookup/cref numActors >}} slot and this index pointer is incremented.

Actors created by this function are identical to those created during map loading by {{< lookup/cref NewMapActorAtIndex >}} except for one key difference: Any {{< lookup/actor type=86 plural=true >}} created here will have their "force active" flag set on. This permits them to think and move offscreen prior to the player "seeing" them. This is necessary because these actors are typically created using the [spawner system]({{< relref "spawner-functions" >}}) which tends to shoot the actors off the top of the screen before {{< lookup/cref NewActor >}} is actually called. Without being forced active, they would hang frozen in the air until the player moved close enough to scroll them into view, and only then would they awaken and fall back down.

```c
void NewActor(word actor_type, word x_origin, word y_origin)
{
    word i;
    Actor *act;

    for (i = 0; i < numActors; i++) {
        act = actors + i;

        if (!act->dead) continue;

        NewActorAtIndex(i, actor_type, x_origin, y_origin);

        if (actor_type == ACT_PARACHUTE_BALL) {
            act->forceactive = true;
        }

        return;
    }
```

During the first stage of the function, the goal is to find any slot in the {{< lookup/cref actors >}} array where the {{< lookup/cref Actor >}} structure has a `dead` flag that's set. Dead actors have no further use and can never come back, so it's appropriate to overwrite any such slot with a new actor's data.

The `for` loop takes `i` from zero up to {{< lookup/cref numActors >}}, covering every actor slot that has ever been used since the current level started. On each iteration an element is selected from the {{< lookup/cref actors >}} array and `act` receives the reference to it.

If the `dead` flag on the actor is unset, this slot holds an active actor and can't be used; `continue` on to another one.

Otherwise, we have found a reclaimable slot and `i` points to the index where it's located. This is passed to {{< lookup/cref NewActorAtIndex >}} along with the `actor_type`, `x_origin`, and `y_origin` from the caller and the actor is created.

As explained in the introduction for this function, the `actor_type` matching {{< lookup/cref name="ACT" text="ACT_PARACHUTE_BALL" >}} needs a special exception to enable the `forceactive` flag -- {{< lookup/cref NewActorAtIndex >}} will have created it with with the flag unset.

With the new actor created, we are able to abandon the loop and `return` to the caller.

Otherwise, the `for` loop continues until it either finds a usable actor slot or all the active slots have been exhausted.

```c
    if (numActors < MAX_ACTORS - 2) {
        act = actors + numActors;

        NewActorAtIndex(numActors, actor_type, x_origin, y_origin);

        if (actor_type == ACT_PARACHUTE_BALL) {
            act->forceactive = true;
        }

        numActors++;
    }
}
```

When we find ourselves in this part of the function, we have checked every actor slot from zero through the peak value in {{< lookup/cref numActors >}} and didn't find a single one containing a dead actor. (In practice, this condition is rare.) In order to insert this actor, we'll need to put it at the end of the used part of the actors array and increment {{< lookup/cref numActors >}} accordingly.

The outer `if` limits the total number of actors that can be appended to the array. As implemented, the {{< lookup/cref MAX_ACTORS >}}` - 2` value artificially limits the total number of active slots to two less than {{< lookup/cref actors >}} can support -- Unless all 410 actor slots are filled during map loading, the final two slots are forever inaccessible for further use.

{{< lookup/cref numActors >}} refers to _both_ the peak number of actor slots that have been used _and_ the index of the first unused slot. This is added to the {{< lookup/cref actors >}} array pointer to point `act` at this empty slot.

{{< lookup/cref NewActorAtIndex >}} does the actual work of creating the actor, again using {{< lookup/cref numActors >}} as the index to be used. Following this is the "force active" modification for {{< lookup/cref name="ACT" text="ACT_PARACHUTE_BALL" >}}, both operations similar to what appeared earlier in the `for` loop.

With the {{< lookup/cref actors >}} array modified, {{< lookup/cref numActors >}} is incremented to reflect the new peak index and the function returns.

{{< boilerplate/function-cref NewActorAtIndex >}}

The {{< lookup/cref NewActorAtIndex >}} function inserts an actor of the specified `actor_type` into the {{< lookup/cref actors >}} array at the specified `index` position. The initial origin position is provided in `x` and `y`, and X/Y shifts are applied here. Returns true as long as `actor_type` referred to a defined actor type -- any false return indicates either a map design or programming error.

The main responsibility of this function is to decode `actor_type` into the actual component variables that make each actor type look and behave in a unique way. There are a handful of actors that have special initialization needs, but most follow the same pattern overall.

{{% aside class="fun-fact" %}}
**Yo dawg, I heard you like `push` instructions.**

When compiled, this function is friggin' huge -- it constitutes nearly 10 KiB of the game's memory footprint. That might not seem like a lot, but it represents about 8.5% of the whole EXE file.
{{% /aside %}}

This function contains a total of 243 cases. One case ({{< lookup/actor type=164 strip=true >}}) handles three distinct actor types ({{< lookup/cref name="ACT" text="ACT_EP1_END_1/2/3" >}}). All 245 actor types defined by the game are covered. The values hard-coded in this function have been extracted into table form on the [actor database]({{< relref "../../databases/actor#normal-actors" >}}) page.

```c
bbool NewActorAtIndex(word index, word actor_type, word x, word y)
{
    nextActorIndex = index;
```

To avoid needing to pass `index` during each call made by this function, a pass-by-global convention is set by stashing the `index` value in {{< lookup/cref nextActorIndex >}}. Any subsequent call to the {{< lookup/cref ConstructActor >}} below will read the intended value of `index` through this variable.

```c
#define F false
#define T true

    switch (actor_type) {
```

The entirety of this function is structured as a `switch` on the passed `actor_type`. To save horizontal space, the boolean values `false` and `true` are temporarily aliased to the single-character `F` and `T` symbols. This is done for clarity, allowing the reader to differentiate `0`/`1` as integers from `F`/`T` as booleans.

```c
    case ACT_BASKET_NULL:
        ConstructActor(
            SPR_BASKET, x, y, T, F, T, F, ActBarrel,
            ACT_BASKET_NULL, SPR_BASKET_SHARDS, 0, 0, 0);
        break;
    case ACT_STAR_FLOAT:
        ConstructActor(SPR_STAR, x, y, F, F, F, F, ActPrize, 0, 0, 0, 0, 4);
        break;
```

This is the pattern. When the passed `actor_type` matches the {{< lookup/cref name="ACT" text="ACT_BASKET_NULL" >}} case, a unique set of arguments are passed to the {{< lookup/cref ConstructActor >}} call. The parameter order is:

1. **Sprite Type:** One of the {{< lookup/cref SPR >}} values, representing the base sprite type that this actor displays as. This is usually the most identifying characteristic of the actor and the closest representation to the original actor type that was passed.
2. **X Origin:** The horizontal position on the map where this actor is placed. Takes the `x` parameter that this function was called with, plus or minus an optional constant shift value.
3. **Y Origin:** Similar to X origin, but using `y` for vertical placement.
4. **"Force Active" flag:** An actor is considered "visible" if any portion of its sprite can be seen anywhere inside the scrolling game window. An actor's "active" state controls whether it thinks and moves, versus being paused and frozen in place. By default an actor is only active while it is visible, and activity stops as soon as it leaves the visible area. The "force active" flag overrides the visibility check and makes the actor permanently active.
5. **"Stay Active" flag:** When enabled, causes an actor to enable its own "force active" flag once it has become visible for the first time.
6. **"Weighted" flag:** When enabled, indicates that the actor has "weight" and should automatically be pulled down by the force of gravity. Actors that float in the air (e.g. prizes and ceiling-mounted actors) must have this flag disabled to prevent falling, and actors that have complicated vertical movement behavior _may_ disable this flag to prevent the global gravity system from interfering.
7. **"Acrophile" flag:** When enabled, informs the common actor-movement code that this actor should be willing to walk off ledges. Otherwise actors will treat such ledges as impassible terrain and turn around. Not all actors use the common movement code.
8. **Tick Function:** A pointer to one of the C functions that contains the actor's per-tick behavior and movement code. Many actors share tick functions, and these shared functions generally use the sprite type or one of the data fields to differentiate the underlying actor types.
9. **Freeform Data #1:** This configures the initial state for opaque internal data specific to each tick function's needs. There are no simple generalizations about what these arguments contain or how they should be interpreted; these would be explained on the page specific to the tick function in question. Freeform data values have names like `data1` in the code.
10. **Freeform Data #2:** Same as above.
11. **Freeform Data #3:** Same as above.
12. **Freeform Data #4:** Same as above.
13. **Freeform Data #5:** Same as above.

Looking at the actual cases highlighted above, {{< lookup/cref name="ACT" text="ACT_BASKET_NULL" >}} uses the {{< lookup/cref name="SPR" text="SPR_BASKET" >}} sprite, has an initial location at `x` and `y` with no shift applied, it is forced active (rendering the "stay active" value irrelevant) and it is weighted. The acrophile flag value is also irrelevant as basket actors do not walk. The tick function is {{< lookup/cref ActBarrel >}} and the five freeform data values are {{< lookup/cref name="ACT" text="ACT_BASKET_NULL" >}}, {{< lookup/cref name="SPR" text="SPR_BASKET_SHARDS" >}}, 0, 0, and 0. All of these arguments are passed to {{< lookup/cref ConstructActor >}} which does the actual work of creating the actor.

For actors that use {{< lookup/cref ActBarrel >}}, `data1` controls the actor type to spawn when the barrel/basket is destroyed, and `data2` dictates which sprite is drawn on the shards that accompany the destruction. `data3`--`data5` are not used and their values are left at zero.

For the {{< lookup/cref name="ACT" text="ACT_STAR_FLOAT" >}} case, the arguments state that the sprite type will be {{< lookup/cref name="SPR" text="SPR_STAR" >}} with no shift applied to `x` or `y`, the actor is not forced active nor does it stay active, and the actor is _not_ weighted -- this keeps it floating in the air. The acrophile flag is irrelevant as stars do not walk, and {{< lookup/cref ActPrize >}} is the tick function.

{{< lookup/cref ActPrize >}}'s interpretation of the data values is:

* `data1`: Holds the horizontal width of the sprite, used to control the range over which a random sparkle decoration could be inserted. Here set to zero, as stars do not sparkle that way.
* `data2`: The height of the sprite for sparkling purposes, also zero here.
* `data3`: This is a private value used to halve the speed of the actor's animation (see `data4`). As stars do not use half-speed animation, this value is not used.
* `data4`: Controls the speed of the actor's animation, either fast or slow. The zero value means that the animation is fast, advancing once per frame of gameplay.
* `data5`: Holds the number of frames in the sprite's animation. The displayed frame is advanced until it reaches this limit then the animation restarts at frame zero. Here set to 4, as stars have a four-frame animation sequence.

The freeform data is _heavily_ dependent on the implementation of the tick function.

Skipping many, many cases, we arrive at the next interesting occurrence:

```c
    case ACT_ARROW_PISTON_E:
        ConstructActor(
            SPR_ARROW_PISTON_E, x - 4, y, F, T, F, F, ActArrowPiston,
            0, 0, 0, 0, DIR2_EAST);
        break;
```

{{< lookup/cref name="ACT" text="ACT_ARROW_PISTON_E" >}} has an X shift of -4 tiles.

```c
    case ACT_GRN_TOMATO:
        ConstructActor(
            SPR_GRN_TOMATO, x, y, T, F, T, F, ActFootSwitch, 0, 0, 0, 0, 0);
        break;
```

Several actors (e.g. {{< lookup/cref name="ACT" text="ACT_GRN_TOMATO" >}} here) use {{< lookup/cref ActFootSwitch >}} as the tick function even though there doesn't seem to be a logical relationship between the two. {{< lookup/cref ActFootSwitch >}} is a common no-op function used by actors that don't actually need to do any per-tick thinking, and its guard code prevents it from doing anything for these sprite types.

```c
    case ACT_SWITCH_PLATFORMS:
        ConstructActor(
            SPR_FOOT_SWITCH, x, y, F, F, F, F, ActFootSwitch,
            0, 0, 0, 0, ACT_SWITCH_PLATFORMS);
        arePlatformsActive = false;
        break;
```

If the map contains an {{< lookup/cref name="ACT" text="ACT_SWITCH_PLATFORMS" >}} actor, the platforms become disabled by default ({{< lookup/cref arePlatformsActive >}}` = false`) and the player will need to find and use this switch to re-enable them.

```c
    case ACT_MYSTERY_WALL:
        ConstructActor(
            SPR_MYSTERY_WALL, x, y, T, F, F, F, ActMysteryWall,
            0, 0, 0, 0, 0);
        mysteryWallTime = 0;
        break;
```

Similarly, maps containing a {{< lookup/actor 62 >}} initialize {{< lookup/cref mysteryWallTime >}} to zero, although {{< lookup/cref InitializeMapGlobals >}} would've certainly been a better place to do that.

```c
    case ACT_EYE_PLANT_FLOOR:
        ConstructActor(
            SPR_EYE_PLANT, x, y, F, T, F, F, ActEyePlant,
            0, 0, 0, 0, DRAW_MODE_NORMAL);
        if (numEyePlants < 15) numEyePlants++;
        break;
```

Each {{< lookup/cref name="ACT" text="ACT_EYE_PLANT_FLOOR" >}} (but not {{< lookup/cref name="ACT" text="ACT_EYE_PLANT_CEIL" >}}!) increments the running count in {{< lookup/cref numEyePlants >}} up to a maximum of 15. This counter governs the bonus given to the player for bombing all of the {{< lookup/actor type=95 strip=true plural=true >}} on a level.

```c
    case ACT_SWITCH_LIGHTS:
        ConstructActor(
            SPR_FOOT_SWITCH, x, y, F, F, F, F, ActFootSwitch,
            0, 0, 0, 0, ACT_SWITCH_LIGHTS);
        areLightsActive = false;
        hasLightSwitch = true;
        break;
```

The presence of an {{< lookup/cref name="ACT" text="ACT_SWITCH_LIGHTS" >}} sets the global {{< lookup/cref hasLightSwitch >}} flag and unsets the {{< lookup/cref areLightsActive >}} flag -- the player will need to find and use this switch to turn the map's lights on.

```c
    case ACT_WORM_CRATE:
        ConstructActor(
            SPR_WORM_CRATE, x, y, T, F, F, F, ActWormCrate,
            0, 0, 0, 0, ((GameRand() % 20) * 5) + 50);
        break;
```

Each {{< lookup/cref name="ACT" text="ACT_WORM_CRATE" >}} receives a random value based on {{< lookup/cref GameRand >}} for `data5`. This controls how long each {{< lookup/actor 130 >}} will sit in view before automatically bursting open.

```c
    case ACT_EP1_END_1:
    case ACT_EP1_END_2:
    case ACT_EP1_END_3:
        ConstructActor(
            SPR_164, x, y, T, F, F, F, ActEpisode1End,
            actor_type, 0, 0, 0, 0);
        break;
```

All of the {{< lookup/actor type=164 strip=true >}} actors use a common implementation, passing the `actor_type` value to `data1` to allow the tick function to differentiate between them. These actor types also reference the nonexistent sprite type {{< lookup/cref name="SPR" text="SPR_164" >}} -- this is not an issue in practice because this actor is never actually drawn at any time.

```c
    case ACT_HINT_GLOBE_1:
        ConstructActor(
            SPR_HINT_GLOBE, x, y, F, F, F, F, ActHintGlobe, 0, 0, 0, 0, 1);
        break;
    case ACT_HINT_GLOBE_2:
        ConstructActor(
            SPR_HINT_GLOBE, x, y, F, F, F, F, ActHintGlobe, 0, 0, 0, 0, 2);
        break;
    case ACT_HINT_GLOBE_3:
        ConstructActor(
            SPR_HINT_GLOBE, x, y, F, F, F, F, ActHintGlobe, 0, 0, 0, 0, 3);
        break;
```

Some actors (like the {{< lookup/actor type=204 strip=true plural=true >}} here) are absolutely identical except for one of the data values (here, `data5`). This is all that is required to display the different hint messages throughout the game.

There are many more actor cases than what has been described here, but they all follow one or more of the patterns shown above. The most unusual part of any actor's definition usually involves the `data1`--`data5` initial values, which must be examined on a case-by-case basis when dealing with that actor type specifically.

```c
    default:
        return false;
    }

#undef F
#undef T

    return true;
}
```

The `default` case occurs when an unimplemented `actor_type` is passed to the function. In that case `false` is returned and no actor is created. Otherwise the return value is `true`.

The `F` and `T` macros are no longer needed, either.

{{< boilerplate/function-cref ConstructActor >}}

The {{< lookup/cref ConstructActor >}} function is called by {{< lookup/cref NewActorAtIndex >}} as a helper to initialize each member of an {{< lookup/cref Actor >}} structure. The actor slot position is provided in the pass-by-global {{< lookup/cref nextActorIndex >}} variable, and the structure at that position is initialized according to the values passed in the arguments.

If the actor being constructed looks like a barrel or a basket, the {{< lookup/cref numBarrels >}} counter is incremented.

```c
void ConstructActor(
    word sprite_type, word x_origin, word y_origin,
    bool force_active, bool stay_active, bool weighted, bool acrophile,
    ActorTickFunction tick_func,
    word data1, word data2, word data3, word data4, word data5
) {
    Actor *act;

    if (data2 == SPR_BARREL_SHARDS || data2 == SPR_BASKET_SHARDS) {
        numBarrels++;
    }
```

This function has one special-case behavior: If the value in `data2` equals either {{< lookup/cref name="SPR" text="SPR_BARREL_SHARDS" >}} or {{< lookup/cref name="SPR" text="SPR_BASKET_SHARDS" >}}, the actor is assumed to be a barrel or basket. This saves the caller from having to add this test into its 30+ switch cases that cover such actors. In response, {{< lookup/cref numBarrels >}} is incremented. This tracks the number of barrels/baskets the player needs to break open in order to earn the bonus for finding them all.

{{% aside class="armchair-engineer" %}}
**Sweet precision and soft collision.**

It would arguably be more bulletproof to test `sprite_type` being equal to either {{< lookup/cref name="SPR" text="SPR_BARREL" >}} or {{< lookup/cref name="SPR" text="SPR_BASKET" >}}, rather than relying on no other actor types happening to have a matching initial `data2` value by chance.

Some may pass this off as an "it's not a problem as long as it works" situation, but it causes a bug: The unrelated {{< lookup/actor 152 >}} happens to be created with a `data2` value of 30, same as {{< lookup/cref name="SPR" text="SPR_BARREL_SHARDS" >}}. This causes each of these actors to be counted as barrels/baskets here, but without being treated as such during destruction. Because of this desynchronization, it is not possible to earn the 50,000 point bonus for destroying all the barrels/baskets on a map where a {{< lookup/actor 152 >}} has ever existed.
{{% /aside %}}

```c
    act = actors + nextActorIndex;
```

The {{< lookup/cref actors >}} array holds {{< lookup/cref Actor >}} structures, and the one we are creating here is indexed by the global {{< lookup/cref nextActorIndex >}} value. This had been set by {{< lookup/cref NewActorAtIndex >}} before this function was called, and removes the need to pass yet another argument into this function. The local `act` variable points to the chosen {{< lookup/cref Actor >}} structure.

```c
    act->sprite = sprite_type;
    act->frame = 0;
    act->x = x_origin;
    act->y = y_origin;
    act->forceactive = force_active;
    act->stayactive = stay_active;
    act->weighted = weighted;
    act->acrophile = acrophile;
    act->dead = false;
    act->tickfunc = tick_func;
    act->westfree = 0;
    act->eastfree = 0;
    act->falltime = 0;
    act->data1 = data1;
    act->data2 = data2;
    act->data3 = data3;
    act->data4 = data4;
    act->data5 = data5;
    act->hurtcooldown = 0;
}
```

Everything in the structure is set to either zero/false or one of the passed arguments without modification. The explanations for each passed field are described in {{< lookup/cref NewActorAtIndex >}}, while the other members are described either elsewhere on this page or on the page for an actor type's [per-tick behavior]({{< relref "movement-functions" >}}).
