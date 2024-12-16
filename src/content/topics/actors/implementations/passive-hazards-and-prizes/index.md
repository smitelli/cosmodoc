+++
title = "Passive Hazards and Prizes"
description = "Describes the actor tick function for hazards and prizes that can be interacted with, but which do not have any regular movement."
weight = 520

actorTypes = [17, 32, 34, 36, 38, 39, 40, 48, 63, 82, 85, 87, 89, 134, 135, 136, 137, 138, 139, 140, 141, 146, 147, 159, 160, 161, 168, 170, 172, 219, 220, 223, 225, 226, 228, 229, 231, 232, 247]
+++

# Passive Hazards and Prizes

The **passive hazards** and **passive prizes** (together called **passive actors**) are game elements that the player can encounter and interact with, but which do not have any movement code. Passive hazards simply "exist"; the player will be hurt if they walk into one, but the hazard does not actively seek out or attack the player. Passive prizes can be picked up by the player for points or other benefits, but have no idle animation effects.

{{< image src="exhibit-2052x.png"
    alt="Appearance of all passive hazards and prizes in the game."
    1x="exhibit-684x.png"
    2x="exhibit-1368x.png"
    3x="exhibit-2052x.png" >}}

Passive actors can utilize the common [actor movement functions]({{< relref "movement-functions" >}}), permitting hazards to be destroyed by [explosions]({{< relref "explosion-functions" >}}) and for weighted prizes to fall down due to [gravity]({{< relref "movement-functions#ProcessActor" >}}). All passive actors have an implementation inside {{< lookup/cref InteractPlayer >}} that specifies what should happen when the player and the actor touch each other.

Every passive actor uses {{< lookup/cref ActFootSwitch >}} as its tick function. {{< lookup/cref ActFootSwitch >}} begins with a test to differentiate passive actors from genuine {{< lookup/actor type=59 strip=true plural=true >}}; passive actors are treated as no-ops.

{{< table-of-contents >}}

## Data Fields

The `data1`--`data5` fields for each of these actors is initialized to zero and, in almost all cases, nothing reads or writes the data values at any time. The exception is `data1` on the {{< lookup/actor type=247 link=false strip=true >}}. For this and only this actor, the value increments by one during each game tick in which the player's sprite is touching the actor.

## Initial Values

To keep the tables a manageable size, the actor tables have been split into "weighted" and "unweighted" (i.e., floating) groups.

### Weighted

{{< data-table/actor-initial-values
    types="32; 34; 36; 38; 82; 134; 135; 136; 137; 138; 139; 140; 147; 168; 170; 172; 220; 226; 229; 232"
    sideways="actor_type; sprite_type"
    augmentActorTypes=`
        {{< lookup/cref name="ACT" text="ACT_GRN_TOMATO" >}};
        {{< lookup/cref name="ACT" text="ACT_RED_TOMATO" >}};
        {{< lookup/cref name="ACT" text="ACT_YEL_PEAR" >}};
        {{< lookup/cref name="ACT" text="ACT_ONION" >}};
        {{< lookup/cref name="ACT" text="ACT_HAMBURGER" >}};
        {{< lookup/cref name="ACT" text="ACT_BOTTLE_DRINK" >}};
        {{< lookup/cref name="ACT" text="ACT_GRN_GOURD" >}};
        {{< lookup/cref name="ACT" text="ACT_BLU_SPHERES" >}};
        {{< lookup/cref name="ACT" text="ACT_POD" >}};
        {{< lookup/cref name="ACT" text="ACT_PEA_PILE" >}};
        {{< lookup/cref name="ACT" text="ACT_LUMPY_FRUIT" >}};
        {{< lookup/cref name="ACT" text="ACT_HORN" >}};
        {{< lookup/cref name="ACT" text="ACT_HEADDRESS" >}};
        {{< lookup/cref name="ACT" text="ACT_ROOT" >}};
        {{< lookup/cref name="ACT" text="ACT_REDGRN_BERRIES" >}};
        {{< lookup/cref name="ACT" text="ACT_RED_GOURD" >}};
        {{< lookup/cref name="ACT" text="ACT_HEADPHONES" >}};
        {{< lookup/cref name="ACT" text="ACT_RED_LEAFY" >}};
        {{< lookup/cref name="ACT" text="ACT_BRN_PEAR" >}};
        {{< lookup/cref name="ACT" text="ACT_CANDY_CORN" >}}`
    augmentSpriteTypes=`
        {{< lookup/cref name="SPR" text="SPR_GRN_TOMATO" >}};
        {{< lookup/cref name="SPR" text="SPR_RED_TOMATO" >}};
        {{< lookup/cref name="SPR" text="SPR_YEL_PEAR" >}};
        {{< lookup/cref name="SPR" text="SPR_ONION" >}};
        {{< lookup/cref name="SPR" text="SPR_HAMBURGER" >}};
        {{< lookup/cref name="SPR" text="SPR_BOTTLE_DRINK" >}};
        {{< lookup/cref name="SPR" text="SPR_GRN_GOURD" >}};
        {{< lookup/cref name="SPR" text="SPR_BLU_SPHERES" >}};
        {{< lookup/cref name="SPR" text="SPR_POD" >}};
        {{< lookup/cref name="SPR" text="SPR_PEA_PILE" >}};
        {{< lookup/cref name="SPR" text="SPR_LUMPY_FRUIT" >}};
        {{< lookup/cref name="SPR" text="SPR_HORN" >}};
        {{< lookup/cref name="SPR" text="SPR_HEADDRESS" >}};
        {{< lookup/cref name="SPR" text="SPR_ROOT" >}};
        {{< lookup/cref name="SPR" text="SPR_REDGRN_BERRIES" >}};
        {{< lookup/cref name="SPR" text="SPR_RED_GOURD" >}};
        {{< lookup/cref name="SPR" text="SPR_HEADPHONES" >}};
        {{< lookup/cref name="SPR" text="SPR_RED_LEAFY" >}};
        {{< lookup/cref name="SPR" text="SPR_BRN_PEAR" >}};
        {{< lookup/cref name="SPR" text="SPR_CANDY_CORN" >}}`
    augmentData1="not used"
    augmentData2="not used"
    augmentData3="not used"
    augmentData4="not used"
    augmentData5="not used" >}}

### Unweighted

{{< data-table/actor-initial-values
    types="17; 39; 40; 48; 63; 85; 87; 89; 141; 146; 159; 160; 161; 219; 223; 225; 228; 231; 247"
    sideways="actor_type; sprite_type"
    augmentActorTypes=`
        {{< lookup/cref name="ACT" text="ACT_SPIKES_FLOOR" >}};
        {{< lookup/cref name="ACT" text="ACT_EXIT_SIGN" >}};
        {{< lookup/cref name="ACT" text="ACT_SPEAR" >}};
        {{< lookup/cref name="ACT" text="ACT_PYRAMID_CEIL" >}};
        {{< lookup/cref name="ACT" text="ACT_SPIKES_FLOOR_BENT" >}};
        {{< lookup/cref name="ACT" text="ACT_GRAPES" >}};
        {{< lookup/cref name="ACT" text="ACT_SPIKES_E" >}};
        {{< lookup/cref name="ACT" text="ACT_SPIKES_W" >}};
        {{< lookup/cref name="ACT" text="ACT_RED_BERRIES" >}};
        {{< lookup/cref name="ACT" text="ACT_YEL_FRUIT_VINE" >}};
        {{< lookup/cref name="ACT" text="ACT_GRN_TOMATO_FLOAT" >}};
        {{< lookup/cref name="ACT" text="ACT_RED_TOMATO_FLOAT" >}};
        {{< lookup/cref name="ACT" text="ACT_YEL_PEAR_FLOAT" >}};
        {{< lookup/cref name="ACT" text="ACT_HEADPHONES_FLOAT" >}};
        {{< lookup/cref name="ACT" text="ACT_BANANAS" >}};
        {{< lookup/cref name="ACT" text="ACT_RED_LEAFY_FLOAT" >}};
        {{< lookup/cref name="ACT" text="ACT_BRN_PEAR_FLOAT" >}};
        {{< lookup/cref name="ACT" text="ACT_CANDY_CORN_FLOAT" >}};
        {{< lookup/cref name="ACT" text="ACT_EXIT_MONSTER_N" >}}`
    augmentSpriteTypes=`
        {{< lookup/cref name="SPR" text="SPR_SPIKES_FLOOR" >}};
        {{< lookup/cref name="SPR" text="SPR_EXIT_SIGN" >}};
        {{< lookup/cref name="SPR" text="SPR_SPEAR" >}};
        {{< lookup/cref name="SPR" text="SPR_PYRAMID" >}};
        {{< lookup/cref name="SPR" text="SPR_SPIKES_FLOOR_BENT" >}};
        {{< lookup/cref name="SPR" text="SPR_GRAPES" >}};
        {{< lookup/cref name="SPR" text="SPR_SPIKES_E" >}};
        {{< lookup/cref name="SPR" text="SPR_SPIKES_W" >}};
        {{< lookup/cref name="SPR" text="SPR_RED_BERRIES" >}};
        {{< lookup/cref name="SPR" text="SPR_YEL_FRUIT_VINE" >}};
        {{< lookup/cref name="SPR" text="SPR_GRN_TOMATO" >}};
        {{< lookup/cref name="SPR" text="SPR_RED_TOMATO" >}};
        {{< lookup/cref name="SPR" text="SPR_YEL_PEAR" >}};
        {{< lookup/cref name="SPR" text="SPR_HEADPHONES" >}};
        {{< lookup/cref name="SPR" text="SPR_BANANAS" >}};
        {{< lookup/cref name="SPR" text="SPR_RED_LEAFY" >}};
        {{< lookup/cref name="SPR" text="SPR_BRN_PEAR" >}};
        {{< lookup/cref name="SPR" text="SPR_CANDY_CORN" >}};
        {{< lookup/cref name="SPR" text="SPR_EXIT_MONSTER_N" >}}`
    augmentData1="not used"
    augmentData2="not used"
    augmentData3="not used"
    augmentData4="not used"
    augmentData5="not used; not used; not used; not used; not used; not used; not used; not used; not used; not used; not used; not used; not used; not used; not used; not used; not used; not used; frame count" >}}

{{% note %}}The differences in the "force active" flag do not matter since unweighted passive prizes do not change their behavior based on visibility.{{% /note %}}

## Player Interaction

Inside the {{< lookup/cref InteractPlayer >}} function, one of the following cases occurs every time a passive actor is touching the player's sprite.

### {{< lookup/actor type=17 link=false >}} / {{< lookup/actor type=87 link=false >}} / {{< lookup/actor type=89 link=false >}}

{{< actor-behavior name-origin="hint-sheet" harmful="true"
    explosions=1 explosion-points=250 >}}

```c
    case SPR_SPIKES_FLOOR:
    case SPR_SPIKES_FLOOR_RECIP: /* non-passive actor; discussed elsewhere */
    case SPR_SPIKES_E:
    case SPR_SPIKES_E_RECIP:     /* non-passive actor; discussed elsewhere */
    case SPR_SPIKES_W:
        if (act->frame > 1) return true;

        HurtPlayer();

        return false;
```

This responds to actors having the {{< lookup/cref name="SPR" text="SPR_SPIKES_FLOOR" >}}, {{< lookup/cref name="SPR" text="SPR_SPIKES_E" >}}, or {{< lookup/cref name="SPR" text="SPR_SPIKES_W" >}} sprite types.

This case also handles the reciprocating variants of the floor-mounted and east-facing spikes, which could have a nonzero `frame` value while in the retracted state. This never occurs for the passive spikes, so the `return true` is not relevant to them.

Since passive spikes never retract, the player is always hurt when touching these actors. {{< lookup/cref HurtPlayer >}} causes this injury, and `false` is returned. Per {{< lookup/cref InteractPlayer >}}'s conventions, a false return value indicates that the actor should be drawn normally for this frame.

### {{< lookup/actor type=32 link=false >}} / {{< lookup/actor type=159 link=false >}} / {{< lookup/actor type=34 link=false >}} / {{< lookup/actor type=160 link=false >}} / {{< lookup/actor type=36 link=false >}} / {{< lookup/actor type=161 link=false >}} / {{< lookup/actor type=38 link=false >}}

{{< actor-behavior name-origin="invented"
    prize-points=200 >}}

```c
    case SPR_GRN_TOMATO:
    case SPR_RED_TOMATO:
    case SPR_YEL_PEAR:
    case SPR_ONION:
        act->dead = true;

        AddScore(200);
        NewActor(ACT_SCORE_EFFECT_200, x, y);

        NewDecoration(SPR_SPARKLE_SHORT, 4, act->x, act->y, DIR8_NONE, 3);
        StartSound(SND_PRIZE);

        return true;
```

This responds to actors having the {{< lookup/cref name="SPR" text="SPR_GRN_TOMATO" >}}, {{< lookup/cref name="SPR" text="SPR_RED_TOMATO" >}}, {{< lookup/cref name="SPR" text="SPR_YEL_PEAR" >}}, or {{< lookup/cref name="SPR" text="SPR_ONION" >}} sprite types. These are all prize actors which are removed from the map when the player sprite touches them. This removal is achieved by setting the actor's `dead` flag to true.

The player earns 200 points via {{< lookup/cref AddScore >}} for picking up one of these actors. This is accompanied by a {{< lookup/actor 178 >}} created by {{< lookup/cref NewActor >}} with an actor type of {{< lookup/cref name="ACT" text="ACT_SCORE_EFFECT_200" >}}. The score effect is inserted at the prize's last known `x`/`y` position.

At the same location (although now using the `act->x` and `act->y` values for unknown reasons) a "{{< lookup/sprite 15 >}}" ({{< lookup/cref name="SPR" text="SPR_SPARKLE_SHORT" >}}) animation is started with {{< lookup/cref NewDecoration >}}. This animation is four frames long and plays three times without moving from its start position ({{< lookup/cref name="DIR8" text="DIR8_NONE" >}}). Along with this visual, the {{< lookup/cref name="SND" text="SND_PRIZE" >}} sound effect is queued for playback with {{< lookup/cref StartSound >}}.

Because the prize actor has become dead here, the value `true` is returned to the caller. Per {{< lookup/cref InteractPlayer >}}'s conventions, a true return value indicates that the actor should not be drawn during this frame.

### {{< lookup/actor type=39 link=false >}}

{{< actor-behavior name-origin="hint-sheet" harmful=false
    name-origin="Influenced by sprite appearance." >}}

```c
    case SPR_EXIT_SIGN:
        winLevel = true;

        return false;
```

This responds to actors having the {{< lookup/cref name="SPR" text="SPR_EXIT_SIGN" >}} sprite type. Whenever the player touches one of these actors, the {{< lookup/cref winLevel >}} flag is unconditionally set, informing the [game loop]({{< relref "game-loop-functions#GameLoop" >}}) that the current level has been completed.

Per {{< lookup/cref InteractPlayer >}}'s conventions, a false return value indicates that the actor should be drawn normally for this frame.

### {{< lookup/actor type=40 link=false >}} / {{< lookup/actor type=48 link=false >}}

{{< actor-behavior name-origin="invented" harmful="true"
    explosions=1 explosion-points=1600
    notes="Only the {{< lookup/actor type=40 link=false >}} can be exploded." >}}

```c
    case SPR_ARROW_PISTON_W:     /* non-passive actor; discussed elsewhere */
    case SPR_ARROW_PISTON_E:     /* non-passive actor; discussed elsewhere */
    case SPR_FIREBALL:           /* non-passive actor; discussed elsewhere */
    case SPR_SAW_BLADE:          /* non-passive actor; discussed elsewhere */
    case SPR_SPEAR:
    case SPR_FLYING_WISP:        /* non-passive actor; discussed elsewhere */
    case SPR_TWO_TONS_CRUSHER:   /* non-passive actor; discussed elsewhere */
    case SPR_JUMPING_BULLET:     /* non-passive actor; discussed elsewhere */
    case SPR_STONE_HEAD_CRUSHER: /* non-passive actor; discussed elsewhere */
    case SPR_PYRAMID:
    case SPR_PROJECTILE:         /* non-passive actor; discussed elsewhere */
    case SPR_SHARP_ROBOT_FLOOR:  /* non-passive actor; discussed elsewhere */
    case SPR_SHARP_ROBOT_CEIL:   /* non-passive actor; discussed elsewhere */
    case SPR_SPARK:              /* non-passive actor; discussed elsewhere */
    case SPR_SMALL_FLAME:        /* non-passive actor; discussed elsewhere */
        HurtPlayer();

        if (act->sprite == SPR_PROJECTILE) {
            act->dead = true;
        }

        return false;
```

This responds to actors having the {{< lookup/cref name="SPR" text="SPR_SPEAR" >}} or {{< lookup/cref name="SPR" text="SPR_PYRAMID" >}} sprite types along with a bit more than a dozen other unrelated types that are not described here. One of those unrelated types is {{< lookup/cref name="SPR" text="SPR_PROJECTILE" >}} which governs the execution of an `if` body that is of no concern to passive actors.

The only relevant bit for passive actors is the call to {{< lookup/cref HurtPlayer >}}, which imparts the actual injury.

Per {{< lookup/cref InteractPlayer >}}'s conventions, a false return value indicates that the actor should be drawn normally for this frame.

### {{< lookup/actor type=63 link=false >}}

{{< actor-behavior name-origin="hint-sheet" harmful="true" >}}

```c
    case SPR_SPIKES_FLOOR_BENT:
    ...
        HurtPlayer();

        return false;
```

This responds to actors having the {{< lookup/cref name="SPR" text="SPR_SPIKES_FLOOR_BENT" >}} sprite type along with a handful of other unrelated types that have been omitted.

These actors simply call {{< lookup/cref HurtPlayer >}} and return `false` to the caller. Per {{< lookup/cref InteractPlayer >}}'s conventions, a false return value indicates that the actor should be drawn normally for this frame.

### {{< lookup/actor type=82 link=false >}}

{{< actor-behavior name-origin="hint-sheet" prize-points=12800 >}}

```c
    case SPR_HAMBURGER:
        act->dead = true;

        AddScore(12800);
        NewActor(ACT_SCORE_EFFECT_12800, x, y);

        NewDecoration(SPR_SPARKLE_SHORT, 4, act->x, act->y, DIR8_NONE, 3);
        StartSound(SND_PRIZE);

        if (playerHealthCells < 5) playerHealthCells++;

        if (!sawHamburgerBubble) {
            NewActor(ACT_SPEECH_WHOA, playerX - 1, playerY - 5);
            sawHamburgerBubble = true;
        }

        UpdateHealth();

        return true;
```

This responds to actors having the {{< lookup/cref name="SPR" text="SPR_HAMBURGER" >}} sprite type. These {{< lookup/actor type=82 link=false plural=true >}} have a unique ability: Each one adds an additional health cell to the player. This health cell begins unfilled, and requires a subsequent {{< lookup/actor type=28 strip=true >}} to increase the player's health to the new maximum.

This prize actor is removed from the map when the player sprite touches it, which is achieved by setting the actor's `dead` flag to true.

The player earns 12,800 points via {{< lookup/cref AddScore >}} for picking up one of these actors. This is accompanied by a {{< lookup/actor 184 >}} created by {{< lookup/cref NewActor >}} with an actor type of {{< lookup/cref name="SPR" text="SPR_SCORE_EFFECT_12800" >}}. The score effect is inserted at the prize's last known `x`/`y` position.

At the same location (although now using the `act->x` and `act->y` values for unknown reasons) a "{{< lookup/sprite 15 >}}" ({{< lookup/cref name="SPR" text="SPR_SPARKLE_SHORT" >}}) animation is started with {{< lookup/cref NewDecoration >}}. This animation is four frames long and plays three times without moving from its start position ({{< lookup/cref name="DIR8" text="DIR8_NONE" >}}). Along with this visual, the {{< lookup/cref name="SND" text="SND_PRIZE" >}} sound effect is queued for playback with {{< lookup/cref StartSound >}}.

The real meat of this actor, so to speak, is the increment of the {{< lookup/cref playerHealthCells >}} variable. The increment is conditional on the current value being less than five, which limits the maximum number of cells that can be held.

If the player has not encountered one of these since the current level started, {{< lookup/cref sawHamburgerBubble >}} will be false and the `if` body will run. {{< lookup/cref NewActor >}} creates a "{{< lookup/actor 244 >}}" ({{< lookup/cref name="ACT" text="ACT_SPEECH_WHOA" >}}) centered above the player's current {{< lookup/cref playerX >}}/{{< lookup/cref playerY >}} position. To prevent this from recurring again if another {{< lookup/actor type=82 link=false >}} is encountered on this level, the {{< lookup/cref sawHamburgerBubble >}} flag is set to true.

{{% aside class="fun-fact" %}}
**... Make that two triple cheeseburgers...**

There are no maps in the retail game with two or more {{< lookup/actor type=82 link=false plural=true >}}, so this `if` body always runs.
{{% /aside %}}

Although the newly-incremented {{< lookup/cref playerHealthCells >}} variable takes care of everything that the game logic cares about, the status bar at the bottom of the screen does not redraw unless explicitly asked to. The call to {{< lookup/cref UpdateHealth >}} redraws the "HEALTH" area in the status bar with the fresh state.

Because the prize actor has become dead here, the value `true` is returned to the caller. Per {{< lookup/cref InteractPlayer >}}'s conventions, a true return value indicates that the actor should not be drawn during this frame.

### {{< lookup/actor type=85 link=false >}} / {{< lookup/actor type=134 link=false >}} / {{< lookup/actor type=135 link=false >}} / {{< lookup/actor type=136 link=false >}} / {{< lookup/actor type=137 link=false >}} / {{< lookup/actor type=138 link=false >}} / {{< lookup/actor type=139 link=false >}} / {{< lookup/actor type=140 link=false >}} / {{< lookup/actor type=141 link=false >}} / {{< lookup/actor type=146 link=false >}} / {{< lookup/actor type=147 link=false >}} / {{< lookup/actor type=168 link=false >}} / {{< lookup/actor type=170 link=false >}} / {{< lookup/actor type=172 link=false >}} / {{< lookup/actor type=223 link=false >}} / {{< lookup/actor type=225 link=false >}} / {{< lookup/actor type=226 link=false >}} / {{< lookup/actor type=228 link=false >}} / {{< lookup/actor type=229 link=false >}} / {{< lookup/actor type=231 link=false >}} / {{< lookup/actor type=232 link=false >}}

{{< actor-behavior name-origin="invented"
    prize-points=400
    notes="A few of these are worth 800 points instead." >}}

```c
    case SPR_GRAPES:
    case SPR_DANCING_MUSHROOM:  /* non-passive actor; discussed elsewhere */
    case SPR_BOTTLE_DRINK:
    case SPR_GRN_GOURD:
    case SPR_BLU_SPHERES:
    case SPR_POD:
    case SPR_PEA_PILE:
    case SPR_LUMPY_FRUIT:
    case SPR_HORN:
    case SPR_RED_BERRIES:
    case SPR_YEL_FRUIT_VINE:
    case SPR_HEADDRESS:
    case SPR_ROOT:
    case SPR_REDGRN_BERRIES:
    case SPR_RED_GOURD:
    case SPR_BANANAS:
    case SPR_RED_LEAFY:
    case SPR_BRN_PEAR:
    case SPR_CANDY_CORN:
        act->dead = true;

        if (
            sprite_type == SPR_YEL_FRUIT_VINE || sprite_type == SPR_BANANAS
            || sprite_type == SPR_GRAPES || sprite_type == SPR_RED_BERRIES
        ) {
            AddScore(800);
            NewActor(ACT_SCORE_EFFECT_800, x, y);
        } else {
            AddScore(400);
            NewActor(ACT_SCORE_EFFECT_400, x, y);
        }

        NewDecoration(SPR_SPARKLE_SHORT, 4, act->x, act->y, DIR8_NONE, 3);
        StartSound(SND_PRIZE);

        return true;
```

This responds to actors having the {{< lookup/cref name="SPR" text="SPR_DANCING_MUSHROOM" >}}, {{< lookup/cref name="SPR" text="SPR_BOTTLE_DRINK" >}}, {{< lookup/cref name="SPR" text="SPR_GRN_GOURD" >}}, {{< lookup/cref name="SPR" text="SPR_BLU_SPHERES" >}}, {{< lookup/cref name="SPR" text="SPR_POD" >}}, {{< lookup/cref name="SPR" text="SPR_PEA_PILE" >}}, {{< lookup/cref name="SPR" text="SPR_LUMPY_FRUIT" >}}, {{< lookup/cref name="SPR" text="SPR_HORN" >}}, {{< lookup/cref name="SPR" text="SPR_HEADDRESS" >}}, {{< lookup/cref name="SPR" text="SPR_ROOT" >}}, {{< lookup/cref name="SPR" text="SPR_REDGRN_BERRIES" >}}, {{< lookup/cref name="SPR" text="SPR_RED_GOURD" >}}, {{< lookup/cref name="SPR" text="SPR_RED_LEAFY" >}}, {{< lookup/cref name="SPR" text="SPR_BRN_PEAR" >}}, or {{< lookup/cref name="SPR" text="SPR_CANDY_CORN" >}} sprite types, all of which are prize actors that give 400 points. This also responds to {{< lookup/cref name="SPR" text="SPR_GRAPES" >}}, {{< lookup/cref name="SPR" text="SPR_RED_BERRIES" >}}, {{< lookup/cref name="SPR" text="SPR_YEL_FRUIT_VINE" >}}, or {{< lookup/cref name="SPR" text="SPR_BANANAS" >}}, which all give 800 points instead. These actors are removed from the map when the player sprite touches them. This removal is achieved by setting the actor's `dead` flag to true.

Depending on the `sprite_type`, the player earns 800 or 400 points via {{< lookup/cref AddScore >}} for picking up one of these actors. This is accompanied by either a {{< lookup/actor 180 >}} or a {{< lookup/actor 179 >}} created by {{< lookup/cref NewActor >}} with an actor type of {{< lookup/cref name="ACT" text="ACT_SCORE_EFFECT_800" >}} or {{< lookup/cref name="ACT" text="ACT_SCORE_EFFECT_400" >}}. The score effect is inserted at the prize's last known `x`/`y` position.

At the same location (although now using the `act->x` and `act->y` values for unknown reasons) a "{{< lookup/sprite 15 >}}" ({{< lookup/cref name="SPR" text="SPR_SPARKLE_SHORT" >}}) animation is started with {{< lookup/cref NewDecoration >}}. This animation is four frames long and plays three times without moving from its start position ({{< lookup/cref name="DIR8" text="DIR8_NONE" >}}). Along with this visual, the {{< lookup/cref name="SND" text="SND_PRIZE" >}} sound effect is queued for playback with {{< lookup/cref StartSound >}}.

Because the prize actor has become dead here, the value `true` is returned to the caller. Per {{< lookup/cref InteractPlayer >}}'s conventions, a true return value indicates that the actor should not be drawn during this frame.

### {{< lookup/actor type=219 link=false >}} / {{< lookup/actor type=220 link=false >}}

{{< actor-behavior name-origin="invented" prize-points=800 >}}

```c
    case SPR_CYA_DIAMOND:     /* non-passive actor; discussed elsewhere */
    case SPR_RED_DIAMOND:     /* non-passive actor; discussed elsewhere */
    case SPR_GRY_OCTAHEDRON:  /* non-passive actor; discussed elsewhere */
    case SPR_BLU_EMERALD:     /* non-passive actor; discussed elsewhere */
    case SPR_HEADPHONES:
        act->dead = true;

        NewDecoration(SPR_SPARKLE_SHORT, 4, act->x, act->y, DIR8_NONE, 3);

        AddScore(800);
        NewActor(ACT_SCORE_EFFECT_800, x, y);

        StartSound(SND_PRIZE);

        return true;
```

This responds to actors having the {{< lookup/cref name="SPR" text="SPR_HEADPHONES" >}} sprite type along with a handful of non-passive types which have idle animations and are not discussed in this section. These actors are removed from the map when the player sprite touches them. This removal is achieved by setting the actor's `dead` flag to true.

At the prize's last known `act->x`/`act->y` position a "{{< lookup/sprite 15 >}}" ({{< lookup/cref name="SPR" text="SPR_SPARKLE_SHORT" >}}) animation is started with {{< lookup/cref NewDecoration >}}. This animation is four frames long and plays three times without moving from its start position ({{< lookup/cref name="DIR8" text="DIR8_NONE" >}}).

The player earns 800 points via {{< lookup/cref AddScore >}} for picking up one of these actors. This is accompanied by a {{< lookup/actor 180 >}} created by {{< lookup/cref NewActor >}} with an actor type of {{< lookup/cref name="ACT" text="ACT_SCORE_EFFECT_800" >}}. The score effect is inserted at the same location (although now using the local `x` and `y` values for unknown reasons). Along with these visuals, the {{< lookup/cref name="SND" text="SND_PRIZE" >}} sound effect is queued for playback with {{< lookup/cref StartSound >}}.

Because the prize actor has become dead here, the value `true` is returned to the caller. Per {{< lookup/cref InteractPlayer >}}'s conventions, a true return value indicates that the actor should not be drawn during this frame.

### {{< lookup/actor type=247 link=false >}}

{{< actor-behavior name-origin="invented" >}}

```c
#ifdef HAS_ACT_EXIT_MONSTER_N
    case SPR_EXIT_MONSTER_N:
        blockActionCmds = true;
        blockMovementCmds = true;

        act->data1++;
```

This code is conditionally compiled into the executable based on the presence of the `HAS_ACT_EXIT_MONSTER_N` define, and is only found in the second episode of the retail game. (Both the first and second episodes feature a level that ends with the player encountering this actor, but the first episode ends with an {{< lookup/actor type=166 strip=true >}} before the player falls far enough to make contact with the monster.)

This case handles actors having the {{< lookup/cref name="SPR" text="SPR_EXIT_MONSTER_N" >}} sprite type. These Exit Monsters are unusual passive actors because they _do_ react to the player's presence, but do not have a tick function that controls their behavior. All interactivity from this actor occurs here as a side effect of the player sprite touching it.

On every tick of gameplay where the player sprite is touching this actor, the player's {{< lookup/cref blockActionCmds >}} and {{< lookup/cref blockMovementCmds >}} flags are both set to true. These make the player invisible, invulnerable, and unable to respond to any keyboard input. The actor's `data1` variable is also incremented to serve as a timer. The remainder of this code performs a short timed animation and the conditions occur in bottom-to-top order.

{{% aside class="armchair-engineer" %}}
**Where'd you go?**

It's not all that easy to see because of the number of objects on the screen combined with the vertical scrolling motion, but the player disappears from view several frames before the monster's jaws actually snap shut.
{{% /aside %}}

```c
        if (act->frame != 0) {
            winLevel = true;
        } else if (act->data1 == 3) {
            act->frame++;
        }

        if (act->data1 > 1) {
            playerY = act->y;
            playerY = act->y;
            isPlayerFalling = false;
        }

        return false;
#endif
```

On a future tick of gameplay after the player first contacts the sprite, `act->data1` will be greater than one and the lowest `if` body will run. This overrides the player's vertical position by setting {{< lookup/cref playerY >}} equal to the actor's `y` position _twice_ -- the repetition does not have any effect beyond what a single assignment would've done. Additionally the {{< lookup/cref isPlayerFalling >}} flag is set to false. _None of these state changes have any observable effect._ Because the {{< lookup/cref blockActionCmds >}} flag is set to true, none of the player movement code in {{< lookup/cref MovePlayer >}} runs, so the player remains frozen in place regardless of what is changed here.

Once `data1` reaches three, the actor's `frame` value is incremented from zero to one. This changes the actor's appearance from open-mouthed to closed.

On a subsequent tick, when this code executes with a nonzero `frame`, the sequence is completed and {{< lookup/cref winLevel >}} is set to true to signal the [game loop]({{< relref "game-loop-functions#GameLoop" >}}) that the current level has been completed.

Regardless of the path taken through the code, the value `false` is always returned to the caller. Per {{< lookup/cref InteractPlayer >}}'s conventions, a false return value indicates that the actor should be drawn normally for this frame.
