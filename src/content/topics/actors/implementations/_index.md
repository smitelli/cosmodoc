+++
title = "Actor Implementations"
linkTitle = "Implementations"
description = "Contains a list of all actor implementations, along with the common player/actor touch code shared by all actor types."
weight = 490

[sitemap]
priority = 1
+++

# Actor Implementations

Each actor's unique movement behavior is contained in its **tick function**, which has a name like `Act...()`. When an actor and the player touch each other (either because the actor is damaging the player or the player is pouncing on the actor) a specific case in the shared {{< lookup/cref InteractPlayer >}} handles the interaction. Each sub-page in this section describes one of the actor tick functions and the relevant portions of {{< lookup/cref InteractPlayer >}}.

{{< table-of-contents >}}

{{< boilerplate/function-cref InteractPlayer >}}

The {{< lookup/cref InteractPlayer >}} function tests for a potential interaction between an actor located at position `index` in the actors array and the player. The actor's `sprite_type`, `frame`, `x`, and `y` must all be passed, and should agree with the values currently held in the actor's memory structure. Returns true if the actor should not be drawn due to being hidden, destroyed, or picked up.

The bulk of this function is _not_ described here; see the relevant sub-page to find the code that handles a particular actor type. Only the common code is on this page.

```c
bool InteractPlayer(
    word index, word sprite_type, word frame, word x, word y
) {
    Actor *act = actors + index;
    register word height;
    word width;
    register word offset;

    if (!IsSpriteVisible(sprite_type, frame, x, y)) return true;
```

The passed `index` is added to the {{< lookup/cref actors >}} array, locating the {{< lookup/cref Actor >}} structure for the actor being examined. `act` is the pointer to this actor.

The {{< lookup/cref IsSpriteVisible >}} test makes sure that the actor is actually visible on the screen somewhere, at least partially. The player cannot interact with anything that can't be seen, and an early `return` for this case prevents any further action from taking place.

```c
    offset = *(actorInfoData + sprite_type) + (frame * 4);
    height = *(actorInfoData + offset);
    width = *(actorInfoData + offset + 1);
```

To support upcoming tests for player pounce alignment, the width and height of the actor need to be determined. This is stored in the [tile info data]({{< relref "tile-info-format" >}}) memory that {{< lookup/cref actorInfoData >}} points to. Adding `sprite_type` to the pointer finds the offset of frame zero for this sprite type, and adding `frame * 4` to the result locates the specific frame being tested. This becomes the `offset` to the sprite frame's data.

The {{< lookup/cref actorInfoData >}} field located at `offset` is the sprite's `height` in tiles. The field at `offset + 1` is the `width`.

```c
    isPounceReady = false;
    if (sprite_type == SPR_BOSS) {
        height = 7;

        if (
            (y - height) + 5 >= playerY && y - height <= playerY &&
            playerX + 2 >= x && x + width - 1 >= playerX
        ) {
            isPounceReady = true;
        }
    } else if (
        (playerFallTime > 3 ? 1 : 0) + (y - height) + 1 >= playerY &&
        y - height <= playerY &&
        playerX + 2 >= x && x + width - 1 >= playerX &&
        scooterMounted == 0
    ) {
        isPounceReady = true;
    }
```

The entire purpose of this is to figure out if {{< lookup/cref isPounceReady >}} should be true or false. In the most basic terms, the player is considered to be in pouncing position when their feet are over this actor's head. There's more to it than that, but the relative alignment is all that this function is concerned with. We'll start with the more typical case, which is the `else if` in the lower half.

In the vertical direction, a pounce is considered "ready" if the top row of the actor's sprite (`(y - height) + 1`) is at or below the bottom row of the player's sprite ({{< lookup/cref playerY >}}), and the row directly above the actor's sprite (`y - height`) is at or above the bottom row of the player's sprite. The player needs to either be positioned immediately above the actor, or overlapping the topmost row of the actor's tiles.

There is an additional adjustment: When {{< lookup/cref playerFallTime >}} is greater than three, the player is effectively falling at double speed and the test needs to be loosened to permit the player to enter the top _two_ tile rows of the actor's sprite and still register a pounce. This is not strictly required because the height of the pounce band is already wide enough to catch the player falling at any practical speed. This is either one of those imperceptible tweaks whose need became apparent during playtesting, or it's some kind of cruft.

Horizontally, the player's right edge ({{< lookup/cref playerX >}}` + 2`) must be on or to the right of the actor's left edge (`x`), and the player's left edge ({{< lookup/cref playerX >}}) must be on or to the left of the actor's right edge (`x + width - 1`). Between those two extents, some part of the player is falling on top of some part of the actor.

In addition to all of that, the player must also be on foot -- not riding a {{< lookup/actor 114 >}}. {{< lookup/cref scooterMounted >}} is zero in those cases. If all of the aforementioned tests pass, the player is in the correct position to be pouncing on the actor. This is memorialized by setting the {{< lookup/cref isPounceReady >}} flag to true.

Back to the primary `if` test: That creates special case for the game's {{< lookup/actor 102 >}} ({{< lookup/cref name="SPR" text="SPR_BOSS" >}}). The boss sprite is drawn in multiple passes for a combined display height of seven tiles, even though none of the component sprite frames are that tall individually. The `height` value is fudged to compensate for this.

The actual intersection tests are the same as in the non-boss branch, except the first comparison is significantly looser: If {{< lookup/cref playerY >}} is inside any of the top five tiles of the full-size boss sprite, the pounce is valid. (Also, there is no test for the scooter, since none of the boss maps in the unmodified game have one available for the player's use.)

If any of the above tests fail, the player is not in the correct location to be pouncing on this actor and {{< lookup/cref isPounceReady >}} is set to false.

```c
    switch (sprite_type) {
        /* Pounce cases */
    }

    if (!IsTouchingPlayer(sprite_type, frame, x, y)) return false;

    switch (sprite_type) {
        /* Prize pickup and injury cases */
    }

    return false;
}
```

It may not look like much here, but this is the bulk of the function.

The first `switch` contains the unconditional tests for `sprite_type`. These cases always run as long as the associated actor is visible on the screen, and this is where potential pounces are tested and handled.

The {{< lookup/cref IsTouchingPlayer >}} call determines if the current actor and the player are touching each other. If they are not, an early `return` prevents the second `switch` from running.

{{% note %}}It's important to remember that the player can _pounce_ on an actor without necessarily _touching_ it.{{% /note %}}

The second `switch` contains the cases that determine what happens when an actor touches the player (or vice versa, depending on your perspective). This is where actions like picking up prizes occur, and also where things cause injury to the player.

Most of the switch cases will return true or false themselves depending on what the result of the interaction was. Some actors do not have any implementations in this function and match no cases, in which case the default `false` value is returned. To the caller, this means "proceed with drawing this actor as usual."

## List of Implementations
