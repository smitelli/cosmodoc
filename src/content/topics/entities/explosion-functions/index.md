+++
title = "Explosion Functions"
description = "Describes the functions that create and process explosions that occur during gameplay."
weight = 480
+++

# Explosion Functions

An **explosion** is a short-lived animation of a destructive fireball sprite that damages anything it comes in contact with. The most common way to produce an explosion is through the use of an {{< lookup/actor 24 >}}, although each of the {{< lookup/actor type=50 strip=true plural=true >}}, {{< lookup/actor type=90 plural=true >}}, {{< lookup/actor type=130 plural=true >}}, and {{< lookup/actor type=188 plural=true >}} can create explosions during their lifespans as well.

{{< table-of-contents >}}

Explosions are useful because they can destroy certain actors that do not respond to the player's "pounce" offense. Carefully-placed explosions can be used to access additional points and bonuses. In episode three (only), a special [palette animation mode]({{< relref "palette-animation" >}}) is available that, when enabled, flashes magenta-keyed areas on the screen in tandem with the explosion for dramatic effect.

The game has a hard-coded limit of seven explosions that can be active at any one time. Once this limit is reached, any attempt to add an additional explosion will be silently ignored until one of the occupied explosion slots becomes free.

## Anatomy of an Explosion

The actual sprite data for an explosion consists of four animation frames, each 6 &times; 6 tiles in size. The four-frame animation plays _twice_ while the explosion is ongoing, with a separate eight-frame sparkle animation superimposed at the center. The explosion and sparkle animations end at the same time, at which point a large plume of smoke rises from the explosion site.

Any contact with the explosion sprite will cause injury to both the player and any explosion-sensitive actors. Neither the smoke nor the sparkle animation cause injury directly.

{{< boilerplate/function-cref InitializeExplosions >}}

The {{< lookup/cref InitializeExplosions >}} function clears all of the memory slots used to store explosion state, immediately terminating all incomplete explosion animations and making each slot available for use.

```c
void InitializeExplosions(void)
{
    word i;

    for (i = 0; i < numExplosions; i++) {
        explosions[i].age = 0;
    }
}
```

The {{< lookup/cref numExplosions >}} variable always holds the value from the constant {{< lookup/cref MAX_EXPLOSIONS >}}, which is 7 regardless of the episode, level, or state of the current map. In the outermost `for` loop, `i` increments from zero to six, covering every explosion slot.

The {{< lookup/cref explosions >}} array maintains a list of {{< lookup/cref Explosion >}} structures, each one having an `age` member variable. As an explosion runs, its `age` increments until it reaches a maximum, at which time it becomes idle again. Idle explosions are expressed by having an `age` of zero, which is set by the assignment here.

At completion, all explosions will be reset to their idle state, ready to be activated at some future time.

{{< boilerplate/function-cref NewExplosion >}}

The {{< lookup/cref NewExplosion >}} function creates a new instance of an explosion at the passed `x_origin` and `y_origin` map tile coordinates and sets the animation up to run. The actual location of the explosion sprite will be two tiles lower on the screen than `y_origin` requests; this helps (somewhat) to vertically align the explosion relative to common actor sprites that create explosions.

{{% note %}}If there is no room in the {{< lookup/cref explosions >}} array (due to too many explosions already running) this function does nothing.{{% /note %}}

Upon successful creation of a new explosion, the {{< lookup/cref name="SND" text="SND_EXPLOSION" >}} sound effect is queued to play.

```c
void NewExplosion(word x_origin, word y_origin)
{
    word i;

    for (i = 0; i < numExplosions; i++) {
        Explosion *ex = explosions + i;
```

The outermost `for` loop runs once for each explosion slot, up to {{< lookup/cref numExplosions >}}. Within the loop, `ex` points to the {{< lookup/cref Explosion >}} structure from the {{< lookup/cref explosions >}} array that's currently being processed. Once an explosion reference has been obtained, the index `i` is not used again until the next iteration.

```c
        if (ex->age != 0) continue;
```

Each explosion uses the `age` member variable to track its overall lifecycle. If an explosion has a nonzero `age`, it indicates that the current slot holds an explosion that is still progressing and should not be overwritten. In this case, the loop `continue`s onto the next slot, hopefully eventually finding one with an inactive explosion.

```c
        ex->age = 1;
        ex->x = x_origin;
        ex->y = y_origin + 2;
```

Once an explosion slot with an `age` of zero is found, the slot is marked in use by setting `age` to one (beginning the explosion's animation sequence) and storing the `x` and `y` positions that the caller provided via `x_origin` and `y_origin`.

The Y position is increased by two, artificially moving the explosion lower on the screen than the caller requested. The _general_ rationale for this is because the explosion is six tiles tall, while most of the actor sprites that generate explosions are significantly shorter. This correction helps to align the center of the explosion sprite with the centers of the associated actor sprites, but it could be argued that it would be easier to reason about by keeping all the adjustments with the caller instead of putting it here.

```c
        StartSound(SND_EXPLOSION);

        break;
    }
}
```

Before finishing, {{< lookup/cref StartSound >}} is called to queue the {{< lookup/cref name="SND" text="SND_EXPLOSION" >}} sound effect for playback. This will coincide with the explosion's animation.

The last thing done here is a `break` to terminate the outer `for` loop, since we no longer need to check for any more free explosion slots -- we just found and used one up. With this `break` (or with the `for` loop running to exhaustion without finding a suitable explosion slot), the function returns.

{{< boilerplate/function-cref DrawExplosions >}}

The {{< lookup/cref DrawExplosions >}} function draws the animation sequence for each active explosion, along with the starting/ending decorations and the flashing palette effect if enabled. This function will cause the player to become hurt if they are in close proximity to any active explosions.

```c
void DrawExplosions(void)
{
    word i;

    for (i = 0; i < numExplosions; i++) {
        Explosion *ex = explosions + i;
```

The outermost `for` loop runs once for each explosion slot, up to {{< lookup/cref numExplosions >}}. Within the loop, `ex` points to the {{< lookup/cref Explosion >}} structure from the {{< lookup/cref explosions >}} array that's currently being processed. Once an explosion reference has been obtained, the index `i` is not used again until the next iteration.

```c
        if (ex->age == 0) continue;
```

Each explosion uses the `age` member variable to track its overall lifecycle. If an explosion has an `age` of zero, it indicates that the current slot holds an explosion that is not currently active and should not be drawn. In this case, the loop `continue`s onto the next slot, looking for an explosion that's ready to be drawn.

```c
#ifdef EXPLOSION_PALETTE
        if (paletteAnimationNum == PAL_ANIM_EXPLOSIONS) {
            byte paletteColors[] = {
                MODE1_WHITE, MODE1_YELLOW, MODE1_WHITE, MODE1_BLACK,
                MODE1_YELLOW, MODE1_WHITE, MODE1_YELLOW, MODE1_BLACK,
                MODE1_BLACK
            };

            SetPaletteRegister(
                PALETTE_KEY_INDEX, paletteColors[ex->age - 1]
            );
        }
#endif
```

This code is conditionally compiled based on the presence of the `EXPLOSION_PALETTE` define. Episode three is the only one with this feature. For that episode, if the map requests a {{< lookup/cref paletteAnimationNum >}} of {{< lookup/cref name="PAL_ANIM" text="PAL_ANIM_EXPLOSIONS" >}}, all explosions should modify the game palette to flash certain pixels on the screen in a white-yellow-black pattern. (This occurs prominently in the first level of episode three.)

`paletteColors[]` holds a list of colors to use during each frame of the explosion (plus a trailing instance of black that is not used). On each explosion frame, the incrementing value in `ex->age` is used as an index into the `paletteColors[]` list, and the result is passed to {{< lookup/cref SetPaletteRegister >}} to change the screen color that gets displayed for any pixel with a value of {{< lookup/cref PALETTE_KEY_INDEX >}}.

```c
        if (ex->age == 1) {
            NewDecoration(
                SPR_SPARKLE_LONG, 8, ex->x + 2, ex->y - 2, DIR8_NONE, 1
            );
        }
```

During the very first frame of an explosion's existence, when its `age` is one, a "sparkle" decoration is added near the center of the explosion's fireball to add a bit of visual interest. This is accomplished with {{< lookup/cref NewDecoration >}}, using a sprite type of {{< lookup/cref name="SPR" text="SPR_SPARKLE_LONG" >}} with an animation consisting of eight frames. The sparkle is 2 &times; 2 tiles, centered within the 6 &times; 6 explosion fireball, so the decoration position is modified to be two tiles right and two tiles above the explosion, which centers it. This decoration does not move ({{< lookup/cref name="DIR8" text="DIR8_NONE" >}}) and it plays one time.

```c
        DrawSprite(
            SPR_EXPLOSION, (ex->age - 1) % 4, ex->x, ex->y, DRAW_MODE_NORMAL
        );

        if (IsTouchingPlayer(
            SPR_EXPLOSION, (ex->age - 1) % 4, ex->x, ex->y
        )) {
            HurtPlayer();
        }
```

{{< lookup/cref DrawSprite >}} draws the current frame of the explosion's animation at `x` and `y`, using {{< lookup/cref name="SPR" text="SPR_EXPLOSION" >}} as the sprite type and the `age` modulo four as the animation frame to show. The explosion has four frames while `age` increments through eight, resulting in the animation playing twice. {{< lookup/cref name="DRAW_MODE" text="DRAW_MODE_NORMAL" >}} permits the explosion to be obscured by any "in-front" map tiles that may be in the same area.

{{< lookup/cref IsTouchingPlayer >}} receives the same sprite position arguments, and returns true if any part of the explosion is touching any part of the player sprite. If this is the case, {{< lookup/cref HurtPlayer >}} is called to cause explosion damage to the player.

```c
        ex->age++;
        if (ex->age == 9) {
            ex->age = 0;
            NewDecoration(
                SPR_SMOKE_LARGE, 6, ex->x + 1, ex->y - 1, DIR8_NORTH, 1
            );
        }
    }
}
```

The loop body ends with lifecycle maintenance code. During every frame of the explosion, `age` increments. Once `age` reaches 9, it is immediately zeroed (deactivating the explosion in this slot) and a large puff of smoke is released. The smoke comes from {{< lookup/cref NewDecoration >}}, requesting {{< lookup/cref name="SPR" text="SPR_SMOKE_LARGE" >}} as the sprite type with a six frame animation. The smoke is a bit smaller than the explosion (4 &times; 3 tiles) so the `x` and `y` positions are adjusted a bit to keep it centered relative to where the explosion was. Smoke rises in the {{< lookup/cref name="DIR8" text="DIR8_NORTH" >}} direction and plays one time.

The outer `for` loop continues running until all explosion slots have been examined, and then the function returns.

{{< boilerplate/function-cref IsNearExplosion >}}

The {{< lookup/cref IsNearExplosion >}} function returns true if a sprite (consisting of a `sprite_type` and a `frame`) located at (`x_origin`, `y_origin`) is intersecting any active explosion.

```c
bool IsNearExplosion(
    word sprite_type, word frame, word x_origin, word y_origin
) {
    word i;

    for (i = 0; i < numExplosions; i++) {
        if (explosions[i].age != 0) {
            Explosion *ex = explosions + i;
```

The outermost `for` loop runs once for each explosion slot, up to {{< lookup/cref numExplosions >}}. Each {{< lookup/cref explosions >}} element uses its `age` member variable to track its overall lifecycle. If an explosion has an `age` of zero, it indicates that the current slot holds an explosion that is not currently active and should not be considered. In this case, the `if` condition fails and the body of the loop does nothing on this iteration.

Assuming an active explosion is being considered, `ex` points to the {{< lookup/cref Explosion >}} structure from the {{< lookup/cref explosions >}} array that's currently being processed. Once an explosion reference has been obtained, the index `i` is not used again until the next iteration.

```c
            if (IsIntersecting(
                SPR_EXPLOSION, 0, ex->x, ex->y,
                sprite_type, frame, x_origin, y_origin
            )) {
                return true;
            }
        }
    }

    return false;
}
```

The {{< lookup/cref IsIntersecting >}} function compares two sprites of a given type and frame, each positioned at a pair of X/Y coordinates, and returns true if any portions of the two sprites overlap. The comparison is done between the {{< lookup/cref name="SPR" text="SPR_EXPLOSION" >}} sprite type at frame zero, and the caller-provided `sprite_type` and `frame` being tested. All explosion frames are 6 &times; 6 tiles, so testing frame zero produces the same effect as testing the actual explosion frame in view.

{{< lookup/cref IsIntersecting >}} requires the X and Y positions of both sprites, which come from `ex->x`, `ex->y`, `x_origin`, and `y_origin`. If it detects an intersection, `true` is immediately returned and the function returns without considering any other explosions that may be active -- the first explosion touching the passed sprite is all that matters.

If there is no intersection, the enclosing `for` loop continues searching through explosion slots. If it exhausts all possibilities without finding any intersections, `false` is returned.

{{< boilerplate/function-cref CanExplode >}}

The {{< lookup/cref CanExplode >}} function returns true if a sprite (consisting of a `sprite_type` and a `frame`) is able to be destroyed by _any_ explosion. If so, destruction shards and effects are inserted at (`x_origin`, `y_origin`) and points are awarded to the score, but the target actor is not destroyed. This code is not testing the positions of specific actors at well-defined positions; the test is whether an actor in the abstract sense is explodable based on the game's rules.

There is special case code to grant {{< lookup/actor type=125 strip=true >}} and {{< lookup/actor type=95 strip=true >}} score bonuses.

```c
bool CanExplode(word sprite_type, word frame, word x_origin, word y_origin)
{
    switch (sprite_type) {
    case SPR_ARROW_PISTON_W:
    case SPR_ARROW_PISTON_E:
    case SPR_SPIKES_FLOOR:
    case SPR_SPIKES_FLOOR_RECIP:
    case SPR_SAW_BLADE:
    case SPR_CABBAGE:
    case SPR_SPEAR:
    case SPR_JUMPING_BULLET:
    case SPR_STONE_HEAD_CRUSHER:
    case SPR_GHOST:
    case SPR_MOON:
    case SPR_HEART_PLANT:
    case SPR_BABY_GHOST:
    case SPR_ROAMER_SLUG:
    case SPR_BABY_GHOST_EGG:
    case SPR_SHARP_ROBOT_FLOOR:
    case SPR_SHARP_ROBOT_CEIL:
    case SPR_CLAM_PLANT:
    case SPR_PARACHUTE_BALL:
    case SPR_SPIKES_E:
    case SPR_SPIKES_E_RECIP:
    case SPR_SPIKES_W:
    case SPR_SPARK:
    case SPR_EYE_PLANT:
    case SPR_RED_JUMPER:
    case SPR_SUCTION_WALKER:
    case SPR_SPIT_WALL_PLANT_E:
    case SPR_SPIT_WALL_PLANT_W:
    case SPR_SPITTING_TURRET:
    case SPR_RED_CHOMPER:
    case SPR_PINK_WORM:
    case SPR_HINT_GLOBE:
    case SPR_PUSHER_ROBOT:
    case SPR_SENTRY_ROBOT:
    case SPR_PINK_WORM_SLIME:
    case SPR_DRAGONFLY:
    case SPR_BIRD:
    case SPR_ROCKET:
    case SPR_74:
    case SPR_84:
    case SPR_96:
```

This function is structured as a long list of `switch` cases that define explodability. Any `sprite_type` contained in this list will fall into the explosion processing code, while omitted values will leave the `switch` without taking any action.

{{< lookup/cref name="SPR" text="SPR_74" >}} is a vestigial case that refers to a sprite type that is never assigned to any actor type. Based on the image data in the ACTORS.MNI file, this was most likely intended to be for the {{< lookup/actor type=74 strip=true >}} variant that cracks when the player approaches. This case is already covered by {{< lookup/cref name="SPR" text="SPR_BABY_GHOST_EGG" >}}.

Similarly, {{< lookup/cref name="SPR" text="SPR_84" >}} and {{< lookup/cref name="SPR" text="SPR_96" >}} are similar duplicates for the ceiling-mounted variants of {{< lookup/actor type=84 strip=true >}} ({{< lookup/cref name="SPR" text="SPR_CLAM_PLANT" >}}) and {{< lookup/actor type=96 strip=true >}} ({{< lookup/cref name="SPR" text="SPR_EYE_PLANT" >}}), respectively.

```c
        if (sprite_type == SPR_HINT_GLOBE) {
            NewActor(ACT_SCORE_EFFECT_12800, x_origin, y_origin);
        }
```

At this point, explodability has been confirmed and it's necessary to determine exactly what needs to happen as each actor explodes.

The first special case occurs when the passed `sprite_type` is a {{< lookup/actor type=125 strip=true >}}. Every actor named in this function grants points during destruction (see the {{< lookup/cref AddScoreForSprite >}} call a bit lower in this function) but only the {{< lookup/actor type=125 strip=true >}} produces a floating score effect in the process. This is accomplished with a {{< lookup/cref NewActor >}} call to insert {{< lookup/cref name="ACT" text="ACT_SCORE_EFFECT_12800" >}} at the sprite's `x_origin` and `y_origin`. No score is given at this point.

```c
        if (
            (
                sprite_type == SPR_SPIKES_FLOOR_RECIP ||
                sprite_type == SPR_SPIKES_E_RECIP
            ) && frame == 2
        ) return false;
```

The next special case is for the reciprocating {{< lookup/actor type=18 strip=true >}} and {{< lookup/actor type=88 strip=true >}}. Each of these can periodically retract into the map, leaving the view and becoming immune to explosions. When one of these actors has a `frame` of 2, they are in the retracted state and explosions should not be able to touch them. In such a case, an early return of `false` prevents further processing and instructs the caller to not consider this actor to be explodable at this time.

```c
        NewShard(sprite_type, frame, x_origin, y_origin);
        AddScoreForSprite(sprite_type);
```

Now the destructive effects of the explosion start to become apparent. {{< lookup/cref NewShard >}} inserts a shard effect based on the passed `sprite_type` and `frame` at the time the explosion occurred, which originates at `x_origin` and `y_origin`. {{< lookup/cref AddScoreForSprite >}} awards points to the player's score based on the value of the `sprite_type` according to the game's rules.

Points awarded for bombed objects do not, in the general case, spawn floating score effects.

```c
        if (sprite_type == SPR_EYE_PLANT) {
            if (numEyePlants == 1) {
                NewActor(ACT_SPEECH_WOW_50K, playerX - 1, playerY - 5);
            }

            NewDecoration(
                SPR_SPARKLE_LONG, 8, x_origin, y_origin, DIR8_NONE, 1
            );
            NewSpawner(ACT_BOMB_IDLE, x_origin, y_origin);

            numEyePlants--;
        }
```

Another special case block handles the situation where the passed `sprite_type` represents one of the {{< lookup/actor type=95 strip=true >}} types. The {{< lookup/cref numEyePlants >}} variable tracks the number of eye plants currently inhabiting the map and, when this value decrements to 1, it means that the player is currently bombing the last surviving one. Exterminating all of them is worth a large point bonus, which is eventually awarded by the "{{< lookup/actor 246 >}}" that {{< lookup/cref NewActor >}} creates here. This new speech bubble is inserted relative to {{< lookup/cref playerX >}}/{{< lookup/cref playerY >}}, _not_ the eye plant that was bombed.

At the explosion site, {{< lookup/cref NewDecoration >}} adds an eight-frame sparkle effect ({{< lookup/cref name="SPR" text="SPR_SPARKLE_LONG" >}}) at `x_origin`/`y_origin` which does not move ({{< lookup/cref name="DIR8" text="DIR8_NONE" >}}) and plays one time.

Sill at `x_origin` and `y_origin`, {{< lookup/cref NewSpawner >}} pops a new {{< lookup/actor 57 >}} out of the spot where the plant was bombed, rewarding the player's insatiable bloodlust. {{< lookup/cref numEyePlants >}} is solemnly decremented to zero.

```c
        return true;
    }

    return false;
}
```

The `return`s are structured such that any completed processing here returns `true`, while a non-matching sprite type returns `false`. The caller can use this return value to quickly determine if the actor should respond to the explosion.

{{< boilerplate/function-cref IsIntersecting >}}

The {{< lookup/cref IsIntersecting >}} function returns true if one sprite (consisting of a `sprite` type and a `frame`) located at an `x`/`y` position on the map is intersecting any part of a second sprite passed in the same form. Despite its general utility, this function is only used by {{< lookup/cref IsNearExplosion >}}.

```c
bool IsIntersecting(
    word sprite1, word frame1, word x1, word y1,
    word sprite2, word frame2, word x2, word y2
) {
    register word height1;
    word width1, offset1;
    register word height2;
    word width2, offset2;
```

The `sprite1`/`sprite2` and `frame1`/`frame2` variables are only used to look up data in the [tile info data]({{< relref "tile-info-format" >}}) for the actor sprites. Similarly, `offset1`/`offset2` are intermediate values used for this lookup, and are not used in the final intersection calculations.

Only X/Y positions and sprite widths/heights are needed. We know the positions because the caller provided them, but the sprite sizes need to be retrieved from the passed sprite and frame combination.

```c
    offset1 = *(actorInfoData + sprite1) + (frame1 * 4);
    height1 = *(actorInfoData + offset1);
    width1 = *(actorInfoData + offset1 + 1);
```

All tile info in memory begins with a lookup table, which contains one 16-bit value per sprite type. The value read from this position is an offset to the tile info for frame zero for that sprite type. Frame zero, and all subsequent frames beyond, contain a four-word structure of height, width, image data offset, and image data segment. Arbitrary frames can be selected by stepping past frame zero in four-word increments.

The assignment to `offset1` uses the above addressing math to produce an offset, in words, where the {{< lookup/cref actorInfoData >}} record for `frame1` of `sprite1` can be found. By adding this offset to the {{< lookup/cref actorInfoData >}} pointer and dereferencing it, the `height1` of the sprite is found. `width1` is calculated similarly, adding one to the offset to address the next field in the structure.

```
    offset2 = *(actorInfoData + sprite2) + (frame2 * 4);
    height2 = *(actorInfoData + offset2);
    width2 = *(actorInfoData + offset2 + 1);
```

The height and width process is repeated for the second sprite.

```c
    if (x1 > mapWidth && x1 <= WORD_MAX) {
        width1 = x1 + width1;
        x1 = 0;
    }
```

This is tricky, and I was ready to dismiss it as an impossible case that had been left in as old cruft. But it turns out this actually does something, and it does it correctly (although hackily).

Explosions are wider than many actors. When an actor wishes to center an explosion relative to itself, it will subtract some fixed distance from its own X position to determine where the explosion's X position should fall. This becomes an issue when the actor is at or near the left edge of the screen -- the explosion's X coordinate might become negative.

{{% aside class="fun-fact" %}}
**Adversarial Case**

This offscreen condition occurs reliably in the unmodified game. In E2M10, there is a {{< lookup/actor 188 >}} at the left edge of the map. When it travels the fixed path it was placed on and crashes into the barrier above, the left-hand explosion is inserted _four_ tiles to the left of the rocket, outside of the screen bounds.
{{% /aside %}}

In this game, all the relevant variables for these types of calculations tend to be machine `word`s, which are unsigned. That means the expression `0 - 1` **underflows** and produces 65,535 (or FFFF in hexadecimal). This is not a small negative number, it is a large positive one.

The `if` here is testing for cases where `x1` is larger than {{< lookup/cref mapWidth >}}, which is how a negative number in unsigned form would behave. (The test for `x1` being less or equal than {{< lookup/cref WORD_MAX >}} is pointless, though. It probably was `x1 <= -1` in the original source, but that would annoy the compiler as well as anyone trying to make sense of the code.)

By adding `width1` to a slightly underflowed `x1`, `x1` **overflows** back across zero to a small positive number equaling `width1` minus the absolute value of `x1`. This is effectively the width of the part of the sprite that is not in negative coordinate space.

Since the width of the sprite has been shrunk to fit in the unsigned universe, `x1` can be fudged to zero to make the usual intersection math work.

```c
    return (
        (x2 <= x1 && x2 + width2 > x1) || (x2 >= x1 && x1 + width1 > x2)
    ) && (
        (y1 - height1 < y2 && y2 <= y1) || (y2 - height2 < y1 && y1 <= y2)
    );
}
```

The function ends with a `return` of the actual intersection test result.

The horizontal test is in the first cluster of comparisons. The sub-expressions check for intersection when sprite #1 is to the right of sprite #2, then the reverse case is tested. If the X position of the left-hand sprite, plus its width, is greater than the X position of the right-hand sprite, there is horizontal overlap.

The vertical tests follow, first testing for the case where sprite #1 is below sprite #2, followed by the opposite. If the Y position of the lower sprite, minus its height, is less than the Y position of the higher sprite, there is vertical overlap.

If both horizontal and vertical tests show overlap, the sprites are touching to some degree.
