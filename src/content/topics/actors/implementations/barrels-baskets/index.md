+++
title = "Barrels/Baskets"
description = "Describes the actor tick function for barrels and baskets."
weight = 500

actorTypes = [0, 29, 31, 33, 35, 37, 52, 53, 56, 58, 81, 93, 100, 115, 116, 117, 119, 142, 148, 156, 157, 158, 167, 169, 171, 173, 175, 193, 195, 197, 199, 218, 224, 227, 230]
+++

# Barrels/Baskets

{{< image class="float-image" src="exhibit-702x.png"
    alt="Idle appearance of a barrel and a basket."
    1x="sine-function-234x.png"
    2x="exhibit-468x.png"
    3x="exhibit-702x.png" >}}

The **Barrels** and **Baskets** (shortened to just "barrels" when repetition gets tedious) are two visually distinct types of object that function identically. In their initial state, they sit on the ground and appear as static, motionless metallic drums or woven fabric squares. Each barrel releases a different predefined actor when destroyed, either as a result of the player pouncing on it or due to an [explosion]({{< relref "explosion-functions" >}}) in close proximity. All of the barrels encountered in an unmodified game will release a prize of some sort, although unusual and [unused]({{< relref "unused-actors" >}}) barrel types do exist.

{{< actor-behavior name-origin="hint-sheet"
    pounces=1 pounce-points=100
    explosions=1 explosion-points=1600 >}}

## Data Fields

`data1`
: The actor type that will be [spawned]({{< relref "spawner-functions" >}}) when the barrel is destroyed. This actor should have its "always active" and "weighted" flags enabled to allow the actor to potentially spawn off the top edge of the scrolling game window and fall back down.

`data2`
: The sprite type that will be shown as [shards]({{< relref "shard-functions" >}}) when the barrel is destroyed. This sprite type is expected to have at least four frames available. This value should be {{< lookup/cref name="SPR" text="SPR_BARREL_SHARDS" >}} or {{< lookup/cref name="SPR" text="SPR_BASKET_SHARDS" >}}.

## Initial Values

### Barrels

<table>
    <tr>
        <th>Actor Type</th>
        <th class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BARREL_POWER_UP" >}} (29)</div></th>
        <th class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BARREL_YEL_PEAR" >}} (35)</div></th>
        <th class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BARREL_ONION" >}} (37)</div></th>
        <th class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BARREL_JUMP_PAD_FL" >}} (58)</div></th>
        <th class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BARREL_BOMB" >}} (56)</div></th>
        <th class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BARREL_CABB_HARDER" >}} (100)</div></th>
        <th class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BARREL_BOTL_DRINK" >}} (142)</div></th>
        <th class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BARREL_HORN" >}} (117)</div></th>
        <th class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BARREL_RT_ORNAMENT" >}} (156)</div></th>
        <th class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BARREL_BLU_CRYSTAL" >}} (157)</div></th>
        <th class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BARREL_RED_CRYSTAL" >}} (158)</div></th>
        <th class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BARREL_GRN_EMERALD" >}} (173)</div></th>
        <th class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BARREL_CLR_DIAMOND" >}} (175)</div></th>
        <th class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BARREL_CYA_DIAMOND" >}} (193)</div></th>
        <th class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BARREL_RED_DIAMOND" >}} (195)</div></th>
        <th class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BARREL_GRY_OCTAHED" >}} (197)</div></th>
        <th class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BARREL_BLU_EMERALD" >}} (199)</div></th>
        <th class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BARREL_HEADPHONES" >}} (218)</div></th>
    </tr>
    <tr><th>Sprite Type</th><td colspan="18">{{< lookup/cref name="SPR" text="SPR_BARREL" >}}</td></tr>
    <tr><th>X Shift</th><td colspan="18">0</td></tr>
    <tr><th>Y Shift</th><td colspan="18">0</td></tr>
    <tr><th>Force Active</th><td colspan="18">yes</td></tr>
    <tr><th>Stay Active</th><td colspan="18">no</td></tr>
    <tr><th>Weighted</th><td colspan="18">yes</td></tr>
    <tr><th>Acrophile</th><td colspan="3">no</td><td>yes</td><td colspan="14">no</td></tr>
    <tr>
        <th>Data 1</th>
        <td class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_POWER_UP_FLOAT" >}}</div></td>
        <td class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_YEL_PEAR" >}}</div></td>
        <td class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_ONION" >}}</div></td>
        <td class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_JUMP_PAD_FLOOR" >}}</div></td>
        <td class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BOMB_IDLE" >}}</div></td>
        <td class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_CABBAGE_HARDER" >}}</div></td>
        <td class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BOTTLE_DRINK" >}}</div></td>
        <td class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_HORN" >}}</div></td>
        <td class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_ROTATING_ORNAMENT" >}}</div></td>
        <td class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BLU_CRYSTAL" >}}</div></td>
        <td class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_RED_CRYSTAL_FLOOR" >}}</div></td>
        <td class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_GRN_EMERALD" >}}</div></td>
        <td class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_CLR_DIAMOND" >}}</div></td>
        <td class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_CYA_DIAMOND" >}}</div></td>
        <td class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_RED_DIAMOND" >}}</div></td>
        <td class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_GRY_OCTAHEDRON" >}}</div></td>
        <td class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BLU_EMERALD" >}}</div></td>
        <td class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_HEADPHONES" >}}</div></td>
    </tr>
    <tr><th>Data 2</th><td colspan="18">{{< lookup/cref name="SPR" text="SPR_BARREL_SHARDS" >}}</td></tr>
    <tr><th>Data 3</th><td colspan="18">0 (not used)</td></tr>
    <tr><th>Data 4</th><td colspan="18">0 (not used)</td></tr>
    <tr><th>Data 5</th><td colspan="18">0 (not used)</td></tr>
</table>

{{% note %}}The differences in the `acrophile` flag do not matter since barrels do not walk.{{% /note %}}

### Baskets

<table>
    <tr>
        <th>Actor Type</th>
        <th class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BASKET_NULL" >}} (0)</div></th>
        <th class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BASKET_GRN_TOMATO" >}} (31)</div></th>
        <th class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BASKET_RED_TOMATO" >}} (33)</div></th>
        <th class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BASKET_HAMBURGER" >}} (81)</div></th>
        <th class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BASKET_DANCE_MUSH" >}} (93)</div></th>
        <th class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BASKET_GRN_GOURD" >}} (52)</div></th>
        <th class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BASKET_BLU_SPHERES" >}} (53)</div></th>
        <th class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BASKET_POD" >}} (119)</div></th>
        <th class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BASKET_PEA_PILE" >}} (115)</div></th>
        <th class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BASKET_LUMPY_FRUIT" >}} (116)</div></th>
        <th class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BASKET_HEADDRESS" >}} (148)</div></th>
        <th class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BASKET_ROOT" >}} (167)</div></th>
        <th class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BASKET_RG_BERRIES" >}} (169)</div></th>
        <th class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BASKET_RED_GOURD" >}} (171)</div></th>
        <th class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BASKET_RED_LEAFY" >}} (224)</div></th>
        <th class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BASKET_BRN_PEAR" >}} (227)</div></th>
        <th class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BASKET_CANDY_CORN" >}} (230)</div></th>
    </tr>
    <tr><th>Sprite Type</th><td colspan="17">{{< lookup/cref name="SPR" text="SPR_BASKET" >}}</td></tr>
    <tr><th>X Shift</th><td colspan="17">0</td></tr>
    <tr><th>Y Shift</th><td colspan="17">0</td></tr>
    <tr><th>Force Active</th><td colspan="17">yes</td></tr>
    <tr><th>Stay Active</th><td colspan="17">no</td></tr>
    <tr><th>Weighted</th><td colspan="9">yes</td><td>no</td><td colspan="7">yes</td></tr>
    <tr><th>Acrophile</th><td colspan="17">no</td></tr>
    <tr>
        <th>Data 1</th>
        <td class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BASKET_NULL" >}}</div></td>
        <td class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_GRN_TOMATO" >}}</div></td>
        <td class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_RED_TOMATO" >}}</div></td>
        <td class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_HAMBURGER" >}}</div></td>
        <td class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_DANCING_MUSHROOM" >}}</div></td>
        <td class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_GRN_GOURD" >}}</div></td>
        <td class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BLU_SPHERES" >}}</div></td>
        <td class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_POD" >}}</div></td>
        <td class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_PEA_PILE" >}}</div></td>
        <td class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_LUMPY_FRUIT" >}}</div></td>
        <td class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_HEADDRESS" >}}</div></td>
        <td class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_ROOT" >}}</div></td>
        <td class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_REDGRN_BERRIES" >}}</div></td>
        <td class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_RED_GOURD" >}}</div></td>
        <td class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_RED_LEAFY" >}}</div></td>
        <td class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_BRN_PEAR" >}}</div></td>
        <td class="sideways"><div>{{< lookup/cref name="ACT" text="ACT_CANDY_CORN" >}}</div></td>
    </tr>
    <tr><th>Data 2</th><td colspan="17">{{< lookup/cref name="SPR" text="SPR_BASKET_SHARDS" >}}</td></tr>
    <tr><th>Data 3</th><td colspan="17">0 (not used)</td></tr>
    <tr><th>Data 4</th><td colspan="17">0 (not used)</td></tr>
    <tr><th>Data 5</th><td colspan="17">0 (not used)</td></tr>
</table>

{{% note %}}The differences in the `weighted` flag could have a visible effect, in the case of e.g. a {{< lookup/actor 116 >}} sitting on a [moving platform]({{< relref "platform-functions" >}}) -- it would not descend along with the platform. This is a moot issue in practice since this actor type is [unused]({{< relref "unused-actors" >}}).{{% /note %}}

## Player Interaction

Inside the {{< lookup/cref InteractPlayer >}} function, this case occurs every time a barrel actor is processed:

```c
    case SPR_BASKET:
    case SPR_BARREL:
        if (act->hurtcooldown == 0 && TryPounce(5)) {
            DestroyBarrel(index);
            AddScore(100);
            NewActor(ACT_SCORE_EFFECT_100, act->x, act->y);
            return true;
        }

        return false;
```

This responds to actors having the {{< lookup/cref name="SPR" text="SPR_BASKET" >}} or {{< lookup/cref name="SPR" text="SPR_BARREL" >}} sprite types. If the barrel has a `hurtcooldown` of zero, it is eligible to be pounced and {{< lookup/cref TryPounce >}} tests to see if the player is appropriately positioned to be pouncing on it at this time. A recoil value of 5 is imparted to the player if the pounce succeeds, then the `if`'s body runs.

When a barrel is pounced, {{< lookup/cref DestroyBarrel >}} is called with `index` (as passed into {{< lookup/cref InteractPlayer >}}) as the argument to destroy the barrel and spawn its contents into the game world. {{< lookup/cref AddScore >}} gives the player 100 points and {{< lookup/cref NewActor >}} spawns a {{< lookup/actor type=177 strip=true >}} ({{< lookup/cref name="ACT" text="ACT_SCORE_EFFECT_100" >}}) at the barrel's final `x`/`y` position to call attention to this.

{{< lookup/cref InteractPlayer >}}'s convention is to return `true` in cases where the actor should not be drawn for this tick (here because it has been destroyed) and `false` in the common case where nothing has changed with the actor's state.

{{< boilerplate/function-cref ActBarrel >}}

{{< lookup/cref ActBarrel >}} is the tick function for every barrel and basket actor. It takes the `index` of the current actor in the actors array.

```c
void ActBarrel(word index)
{
    Actor *act = actors + index;
```

The passed `index` is added to the {{< lookup/cref actors >}} array, locating the {{< lookup/cref Actor >}} structure for the barrel being processed. `act` is the pointer to this actor.

```c
    if (IsNearExplosion(SPR_BARREL, 0, act->x, act->y)) {
        DestroyBarrel(index);
        AddScore(1600);
        NewActor(ACT_SCORE_EFFECT_1600, act->x, act->y);
    }
}
```

Barrels can be destroyed by explosions, and {{< lookup/cref IsNearExplosion >}} will return true if one is currently nearby. For the purposes of this test, the actual barrel/basket type is temporarily ignored and the intersection is tested as if every actor was showing frame zero of {{< lookup/cref name="SPR" text="SPR_BARREL" >}}. This is not a problem in the horizontal direction because barrel and basket sprites are both four tiles wide. Vertically, the barrels are one tile taller than the baskets -- this could cause an explosion to register a hit to the top of a basket even though it visually misses it by one tile.

If an explosion is touching the barrel, {{< lookup/cref DestroyBarrel >}} is called with `index` as the argument to destroy the barrel and spawn its contents into the game world. {{< lookup/cref AddScore >}} gives the player 1,600 points and {{< lookup/cref NewActor >}} spawns a {{< lookup/actor type=181 strip=true >}} ({{< lookup/cref name="ACT" text="ACT_SCORE_EFFECT_1600" >}}) at the barrel's final `x`/`y` position to call attention to this.

{{< boilerplate/function-cref DestroyBarrel >}}

The {{< lookup/cref DestroyBarrel >}} function handles the animation, sound effects, and lifecycle management at the instant a barrel or basket is destroyed.

```c
void DestroyBarrel(word index)
{
    Actor *act = actors + index;

    act->dead = true;
```

The passed `index` is added to the {{< lookup/cref actors >}} array, locating the {{< lookup/cref Actor >}} structure for the barrel being processed. `act` is the pointer to this actor.

Setting the barrel's `dead` to true effectively removes it from the map and from all subsequent processing. Its life has now ended.

```c
    NewShard(act->data2, 0, act->x - 1, act->y);
    NewShard(act->data2, 1, act->x + 1, act->y - 1);
    NewShard(act->data2, 2, act->x + 3, act->y);
    NewShard(act->data2, 3, act->x + 2, act->y + 2);
```

Four shards are released around the barrel's final `x`/`y` position with {{< lookup/cref NewShard >}}, using the value in `data2` to select between barrel or basket shards as appropriate for the actor type. Frames 0&ndash;4 of these sprite types contain different "strips" of debris rather than anything that could be considered an animation.

```c
    if (GameRand() % 2 != 0) {
        StartSound(SND_BARREL_DESTROY_1);
    } else {
        StartSound(SND_BARREL_DESTROY_2);
    }
```

There are two sound effects, {{< lookup/cref name="SND" text="SND_BARREL_DESTROY_1" >}} and {{< lookup/cref name="SND" text="SND_BARREL_DESTROY_2" >}}, selected with 50/50 probability based on the {{< lookup/cref GameRand >}} result. Whichever sound effect is chosen is queued for playback with {{< lookup/cref StartSound >}}.

```c
    NewSpawner(act->data1, act->x + 1, act->y);
```

`data1` is the actor type of the object that the barrel releases. {{< lookup/cref NewSpawner >}} begins spawning it into existence starting at the barrel's final `y` position and one tile to the right of `x`. This perfectly centers any sprites that happen to be two tiles wide.

```c
    if (numBarrels == 1) {
        NewActor(ACT_SPEECH_WOW_50K, playerX - 1, playerY - 5);
    }
    numBarrels--;
}
```

In the case where {{< lookup/cref numBarrels >}} equals 1, this was the last remaining barrel and/or basket on the map. This is worthy of a score bonus, which is granted indirectly by inserting a "{{< lookup/actor 246 >}}" ({{< lookup/cref name="ACT" text="ACT_SPEECH_WOW_50K" >}}) actor via {{< lookup/cref NewActor >}}. This new actor is centered relative to the _player_, since this is a speech bubble coming out of them.

In all cases, {{< lookup/cref numBarrels >}} is decremented to keep the count accurate to the remaining barrel population.
