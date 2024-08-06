+++
title = "Game Logic Functions"
description = "Describes the miscellaneous functions responsible for enforcing the game's interactivity, scoring, and rules."
weight = 450
+++

# Game Logic Functions

Some time ago I heard a quote that went something like: "In game development, all concerns are cross-cutting." I've long since lost the exact quote and have no way of tracking down the source, but it's a statement that's stuck with me. This game has a number of functions that don't fit neatly into a particular subsystem, and don't implement a specific enough functionality to be an entire topic of examination. Rather, this page contains a jumble of functions that I couldn't think of a better home for.

{{< table-of-contents >}}

{{< boilerplate/function-cref GameRand >}}

The {{< lookup/cref GameRand >}} function returns a pseudorandom number based on a fixed table of randomness combined with influence from the player and scrolling game window positions. The output sequence from this function is deterministic for a given sequence of player and scroll positions. This is necessary for consistency during demo playback -- without a reproducible sequence of random values the actors would desynchronize from the recorded player movements.

{{< lookup/cref randStepCount >}} is reset to zero each time a level is (re)started (see {{< lookup/cref InitializeMapGlobals >}}), which provides the basis of this predictable output assuming the player follows the exact same path through the map each time.

Functionality that does not affect demo synchronization should ideally use the standard {{< lookup/cref rand >}} function or the Borland-specific {{< lookup/cref random >}} macro, but not everything does. (e.g. sprite drawing in {{< lookup/cref ActTransporter >}}, sound effect choice in {{< lookup/cref DestroyBarrel >}}).

```c
word GameRand(void)
{
    static word randtable[] = {
        31,  12,  17,  233, 99,  8,   64,  12,  199, 49,  5,   6,
        143, 1,   35,  46,  52,  5,   8,   21,  44,  8,   3,   77,
        2,   103, 34,  23,  78,  2,   67,  2,   79,  46,  1,   98
    };

    randStepCount++;
    if (randStepCount > 35) randStepCount = 0;

    return randtable[randStepCount] + scrollX + scrollY + randStepCount +
        playerX + playerY;
}
```

`randtable[]` is a 36-element array of random-ish numbers of unknown origin. On each call, the global {{< lookup/cref randStepCount >}} is incremented to select the next element of the table. The very first call skips over index zero, but after that all elements from index zero to 35 are rotated through.

The return value is the sum of:

* `randtable[`{{< lookup/cref randStepCount >}}`]` plus {{< lookup/cref randStepCount >}}
* {{< lookup/cref scrollX >}} plus {{< lookup/cref scrollY >}}
* {{< lookup/cref playerX >}} plus {{< lookup/cref playerY >}}

I sat for a while and analyzed this function to try to determine what its range of outputs was. The highest value would occur on a 1,024 &times; 32 map with both the player (1,021, 31) and scroll position (986, 14) as far to the bottom right as possible. The maximum random table value is "233" at index three, so the sum of everything is 2,288. That's the maximum plausible value.

The minimum is not really dependent on the map dimensions, and occurs when the player (0, 4) and scroll position (0, 0) are both at the top left. The minimum random table value isn't actually relevant, as it's the sum of the table value and its index within the table that is used. The smallest combination from the table is the value "12" at index one. This places the minimum plausible value at 16.

This function is cryptographically laughable, but even for the purposes of gameplay it's not terribly robust. It's quite easy for the player to stand still for a moment and observe actors that seem to be "stuck" in one branch of their decision-making. By nudging the player (or the view) one or two tiles, the actors will regain their senses and start behaving in a more interesting way. That's caused by this random number generator producing repetitive output which is being consumed by the same group of actors in sequence.

{{< boilerplate/function-cref IsTouchingPlayer >}}

The {{< lookup/cref IsTouchingPlayer >}} function returns true if the passed `sprite_type` and `frame` located at `x_origin` and `y_origin` is touching any part of the player sprite at its current position. This function is very similar to {{< lookup/cref IsIntersecting >}}, but this function only accepts one sprite; the other sprite is implicitly the player at {{< lookup/cref playerX >}} and {{< lookup/cref playerY >}}.

```c
bool IsTouchingPlayer(
    word sprite_type, word frame, word x_origin, word y_origin
) {
    register word height, width;
    word offset;

    if (playerDeadTime != 0) return false;
```

If the player has died but their sprite is still on the map (e.g. during the angel death animation) they are incapable of touching anything. Nonzero {{< lookup/cref playerDeadTime >}} represents this, which causes an early false return.

```c
    offset = *(actorInfoData + sprite_type) + (frame * 4);
    height = *(actorInfoData + offset);
    width = *(actorInfoData + offset + 1);
```

The caller passed a `sprite_type` and a `frame`, but what is actually needed is the `width` and `height` of that sprite. This needs to be looked up in the [tile info data]({{< relref "tile-info-format" >}}) for the actor sprites.

All tile info in memory begins with a lookup table, which contains one 16-bit value per sprite type. The value read from this position is an offset to the tile info for frame zero for that sprite type. Frame zero, and all subsequent frames beyond, contain a four-word structure of height, width, image data offset, and image data segment. Arbitrary frames can be selected by stepping past frame zero in four-word increments.

The assignment to `offset` uses the above addressing math to produce an offset, in words, where the {{< lookup/cref actorInfoData >}} record for `frame` of `sprite_type` can be found. By adding this offset to the {{< lookup/cref actorInfoData >}} pointer and dereferencing it, the `height` of the sprite is found. `width` is calculated similarly, adding one to the offset to address the next field in the structure.

```c
    if (
        x_origin > mapWidth && x_origin <= WORD_MAX &&
        sprite_type == SPR_EXPLOSION
    ) {
        width = x_origin + width;
        x_origin = 0;
    }
```

When the `sprite_type` is {{< lookup/cref name="SPR" text="SPR_EXPLOSION" >}}, we might have to deal with an edge condition (literally). Some explosion origins can occur off the left edge of the screen, having a conceptually negative X that looks like a large positive number in the unsigned math the game uses. There is identical code (and a more satisfying explanation) in {{< lookup/cref IsIntersecting >}}.

```c
    if ((
        (playerX <= x_origin && playerX + 3 > x_origin) ||
        (playerX >= x_origin && x_origin + width > playerX)
    ) && (
        (y_origin - height < playerY && playerY <= y_origin) ||
        (playerY - 4 <= y_origin && y_origin <= playerY)
    )) return true;

    return false;
}
```

The intersection is a large set of nested expressions, with horizontal tests first followed by vertical tests.

Horizontally, when the player's left column is to the left of (or aligned with) the sprite's left column, intersection happens if the empty space to the right of the player ({{< lookup/cref playerX >}}` + 3`) is to the right of the sprite's left column. In the opposite order, when the player's left column is to the right of (or aligned with!) the sprite's left column, intersection could also happen if the player's left column is to the left of the empty space to the right of the sprite (`x_origin + width`).

Vertically, when the player's bottom row is higher than (or aligned with) the sprite's bottom row, intersection happens if the player's bottom row is lower than the empty space above the sprite (`y_origin - height`). In the opposite order, when the player's bottom row is below (or aligned with!) the sprite's bottom row, intersection could also happen if the top row of tiles for the player ({{< lookup/cref playerY >}}` - 4`) is higher than (or aligned with) the sprite's bottom row.

If at least one horizontal _and_ one vertical test passes, the return value is `true`. Otherwise `false` is returned.

{{< boilerplate/function-cref HurtPlayer >}}

The {{< lookup/cref HurtPlayer >}} function deducts a bar of health from the player, and kills them if they have lost enough health. This function unconditionally causes the player to release any active cling, and may show an "Ouch!" speech bubble or the pounce hint if either of those things has not happened before.

Each time this function is called, a 44-tick cooldown interval starts in which the player cannot be hurt again.

```c
void HurtPlayer(void)
{
    if (
        playerDeadTime != 0 ||
        isGodMode ||
        blockActionCmds ||
        activeTransporter != 0 ||
        isPlayerInvincible ||
        isPlayerInPipe ||
        playerHurtCooldown != 0
    ) return;
```

There are a whole bunch of things that could occur in the game that make the player momentarily invincible:

* When {{< lookup/cref playerDeadTime >}} is nonzero, the player has already lost enough health to kill them, and they are now experiencing the death animation sequence before the level restarts. There is no reason to hurt a player that's already dead.
* A true value in {{< lookup/cref isGodMode >}} means the user has enabled the <kbd>F10</kbd> + <kbd>G</kbd> debug key to enable "god mode." This shields the player from all injury except for falling off the map, which is not something this function deals with.
* {{< lookup/cref blockActionCmds >}} is enabled while the player is inside a creature like the {{< lookup/actor 152 >}}. They effectively no longer exist on the map while this is true.
* {{< lookup/cref activeTransporter >}} is nonzero when the player has entered one {{< lookup/actor type=107 strip=true >}} and is waiting to come out of the other one. The player should not be able to take damage during this time.
* The {{< lookup/cref isPlayerInvincible >}} flag is true as long as the player has an {{< lookup/actor 201 >}} protecting them. The flag becomes false once the bubble expires.
* The {{< lookup/cref isPlayerInPipe >}} flag is true while the player is inside of a pipe system. They should be protected from outside injury while moving across the map.
* {{< lookup/cref playerHurtCooldown >}} is nonzero for a short time after a previous call to this function. The player sprite flashes during this time, and when it returns to zero the player is able to be injured again.

Each of these conditions disqualifies the player from taking damage, so an early `return` bypasses the rest of this function.

```c
    playerClingDir = DIR4_NONE;
```

When the player is injured, clings are unconditionally released by setting {{< lookup/cref playerClingDir >}} to {{< lookup/cref name="DIR4" text="DIR4_NONE" >}}.

```c
    if (!sawHurtBubble) {
        sawHurtBubble = true;

        NewActor(ACT_SPEECH_OUCH, playerX - 1, playerY - 5);

        if (pounceHintState == POUNCE_HINT_UNSEEN) {
            pounceHintState = POUNCE_HINT_QUEUED;
        }
    }
```

If this is the first time the player has been injured since the level started, the {{< lookup/cref sawHurtBubble >}} flag will be false and this block executes. The flag is then set to prevent this from occurring again.

{{< lookup/cref NewActor >}} inserts a "{{< lookup/actor 235 >}}" ({{< lookup/cref name="ACT" text="ACT_SPEECH_OUCH" >}}) at the player's position. The bubble is five tiles wide, relative to the player's three, so the X position is adjusted by -1 to center it. The Y position is five tiles above the player's feet.

The {{< lookup/cref pounceHintState >}} system is a little convoluted, but it holds the value {{< lookup/cref name="POUNCE_HINT" text="POUNCE_HINT_UNSEEN" >}} when the episode begins. If it's still in that state when the player is hurt, it's updated to {{< lookup/cref name="POUNCE_HINT" text="POUNCE_HINT_QUEUED" >}} which (eventually, in {{< lookup/cref GameLoop >}}) shows the one-time "pounce hint" dialog. This never happens again over the course of an episode, even going so far as to be stored as a field in the [saved games]({{< relref "save-file-format" >}}).

```c
    playerHealth--;

    if (playerHealth == 0) {
        playerDeadTime = 1;
        scooterMounted = 0;
    } else {
        UpdateHealth();
        playerHurtCooldown = 44;
        StartSound(SND_PLAYER_HURT);
    }
}
```

One point is deducted from {{< lookup/cref playerHealth >}}, then the updated value is tested to see if that has killed the player.

If {{< lookup/cref playerHealth >}} became zero, the player died and {{< lookup/cref playerDeadTime >}} is set to one, beginning the death animation. The player is force-removed from any scooter they may be riding on by setting {{< lookup/cref scooterMounted >}} to zero.

Otherwise, the damage was not fatal, and {{< lookup/cref UpdateHealth >}} is called to redraw the health area in the status bar with the new health count. {{< lookup/cref playerHurtCooldown >}} is set to 44, giving the player some time to retreat from the danger before getting hurt again. {{< lookup/cref StartSound >}} also occurs here, queuing the {{< lookup/cref name="SND" text="SND_PLAYER_HURT" >}} warning.

{{< boilerplate/function-cref ProcessAndDrawPlayer >}}

The {{< lookup/cref ProcessAndDrawPlayer >}} function determines the player's reaction to pain or death and draws the player sprite accordingly. This function is also responsible for determining if the player has fallen to their death in a bottomless pit. If the player has died and completed the relevant death animation sequence, this function reloads the game state to the way it was when the level was last started and returns true. If the level has not been restarted, this function returns false.

The player can die in two distinct ways:

* When touching a dangerous object, {{< lookup/cref HurtPlayer >}} deducts one unit of health. Once all the available health has been depleted, {{< lookup/cref HurtPlayer >}} sets {{< lookup/cref playerDeadTime >}} to 1. This marks the player as "dead" and changes the player sprite into an angel that no longer responds to user input or objects on the map. After a short delay the angel rises off the top of the screen and the level restarts.
* If the player falls into a bottomless pit, the {{< lookup/cref playerY >}} value will leave the bottom of the [map data]({{< relref "map-format" >}}) and enter [undefined and buggy space]({{< relref "player-movement-functions#dancing=on-the-ceiling" >}}). Once they fall sufficiently far, this function sets both {{< lookup/cref playerDeadTime >}} and {{< lookup/cref playerFallDeadTime >}} to 1. The player falls completely off the bottom edge of the screen, a speech bubble rises up from the point where they fell from, and the level restarts.

This function is conceptually a wrapper around {{< lookup/cref DrawPlayer >}} and makes the final decision about which sprite frame to show at any given time. Once the player dies, this function becomes responsible for controlling the position -- regular keyboard/joystick input and movement rules no longer apply.

```c
bbool ProcessAndDrawPlayer(void)
{
    static byte speechframe = 0;
```

`speechframe` is a function-local variable that maintains its value across calls for the lifetime of the program's execution. This variable is used to rotate through five possible frames of a speech bubble sprite that appear when the player falls into a bottomless pit.

```c
    if (maxScrollY + SCROLLH + 3 < playerY && playerDeadTime == 0) {
        playerFallDeadTime = 1;
        playerDeadTime = 1;

        if (maxScrollY + SCROLLH + 4 == playerY) {
            playerY++;
        }

        speechframe++;
        if (speechframe == 5) speechframe = 0;
    }
```

{{< lookup/cref playerDeadTime >}} must be zero for this block to execute at all, which prevents an already-dead player from suffering the indignity of falling out of the map and dying again.

{{< lookup/cref maxScrollY >}} represents the row of map tiles that is drawn at the top of the screen when the view is scrolled down to the lowest visible area of the map. Adding {{< lookup/cref SCROLLH >}} yields the first row after the end of the visible map data, effectively the first row of map tiles that the status bar covers. Adding three to that running total covers four -- but not all five -- of the tiles of height the player sprite has. {{< lookup/cref playerY >}} becomes _greater_ than this as soon as the top row of player sprite tiles falls behind the status bar.

Once the player has fallen completely out of view, they are dead. {{< lookup/cref playerFallDeadTime >}} is set to 1 to begin the falling death animation, and {{< lookup/cref playerDeadTime >}} is also set to 1 to inform the rest of the game's functions that they no longer need to test for the player interacting with any surfaces or objects.

The off-screen math is repeated with a strict equality check instead of an inequality, this time against four. The intention is for there to be a one-tile gap between the bottom of the visible map area and the top of the player sprite. If the player was falling at a slow speed, the only way to obtain a sufficient gap is to increase {{< lookup/cref playerY >}} again.

Once {{< lookup/cref playerY >}} reaches this point off the screen, it no longer increases. There is no need for the player to continue falling if nothing can see them anyway.

`speechframe` is incremented to select the next speech bubble message out of a rotation of five available frames.

```c
    if (playerFallDeadTime != 0) {
        playerFallDeadTime++;

        if (playerFallDeadTime == 2) {
            StartSound(SND_PLAYER_HURT);
        }

        for (; playerFallDeadTime < 12; playerFallDeadTime++) {
            WaitHard(2);
        }
```

The previous `if` ends and a new one begins. This one handles the animation sequence of the player falling into the bottomless pit.

In the case where the player was just found to have fallen out of the map, {{< lookup/cref playerFallDeadTime >}} will be 1 which then immediately increments to 2 upon entry here. That, in turn, passes the next `if` and {{< lookup/cref StartSound >}} plays {{< lookup/cref name="SND" text="SND_PLAYER_HURT" >}}. It also passes the condition in the `for` loop, which takes {{< lookup/cref playerFallDeadTime >}} up to 12 after all iterations finish. Each iteration calls {{< lookup/cref WaitHard >}} for an inescapable 2 timer ticks producing a total delay of 1 &frasl; 7 of a second. This pauses _everything_ in the game -- the [game loop]({{< relref "game-loop-functions" >}}) stops cold while this delay is running -- causing a noticeable "hitch" as the player falls.

It's also important to remember that this is occurring during the same game tick where the player first moved off the map. _The video frame for this tick isn't done yet,_ and the screen is still showing the previous frame where the top of the player's head is still in view.

{{% aside class="speculation" %}}
**I liked it better the other way.**

This looks like maybe it was a late addition to speed up the animation. Removing the `for` loop removes the delay hitch and lets the player fall for a little under a second before the speech bubble comes. It actually feels pretty nice that way; I don't know why they hacked it shorter this way.
{{% /aside %}}

Once {{< lookup/cref playerFallDeadTime >}} reaches 12 nothing else in here runs until this function is called on the next game tick.

```c
        if (playerFallDeadTime == 13) {
            StartSound(SND_PLAYER_DEATH);
        }

        if (playerFallDeadTime > 12 && playerFallDeadTime < 19) {
            DrawSprite(
                SPR_SPEECH_MULTI, speechframe,
                playerX - 1, (playerY - playerFallDeadTime) + 13,
                DRAW_MODE_IN_FRONT
            );
        }
```

Once {{< lookup/cref playerFallDeadTime >}} reaches 13, {{< lookup/cref StartSound >}} plays the {{< lookup/cref name="SND" text="SND_PLAYER_DEATH" >}} effect.

The `for` loop begins as well, and runs over the next six game ticks. During each one, {{< lookup/cref DrawSprite >}} places the speech bubble {{< lookup/cref name="SPR" text="SPR_SPEECH_MULTI" >}} sprite using `speechframe` to select the message contained within. This is drawn centered against the last known {{< lookup/cref playerX >}} and rising up from {{< lookup/cref playerY >}} into the bottom of the visible screen. {{< lookup/cref name="DRAW_MODE" text="DRAW_MODE_IN_FRONT" >}} ensures that nothing on the map will cover up the bubble.

```c
        if (playerFallDeadTime > 18) {
            DrawSprite(
                SPR_SPEECH_MULTI, speechframe,
                playerX - 1, playerY - 6, DRAW_MODE_IN_FRONT
            );
        }
```

When {{< lookup/cref playerFallDeadTime >}} exceeds 18, the speech bubble stops rising and becomes fixed at a point six tiles above {{< lookup/cref playerY >}}. Given that the player is five tiles tall and the code earlier in this function ensured a one-tile gap between the bottom row of visible map tiles and the top of the player sprite, this speech bubble should be fixed at the bottom of the game window now. It will be drawn here during every subsequent game tick until the level restarts.

```c
        if (playerFallDeadTime > 30) {
            LoadGameState('T');
            InitializeLevel(levelNum);
            playerFallDeadTime = 0;
            return true;
        }
```

When {{< lookup/cref playerFallDeadTime >}} exceeds 30, the animation is over and the level should be restarted. {{< lookup/cref LoadGameState >}} reloads the game state from the temporary [save file]({{< relref "save-file-format" >}}) in the `'T'` slot, {{< lookup/cref InitializeLevel >}} reloads and resets all of the map state to play {{< lookup/cref levelNum >}}, and {{< lookup/cref playerFallDeadTime >}} is reset to zero (gratuitously; {{< lookup/cref InitializeLevel >}} called {{< lookup/cref InitializeMapGlobals >}} which did that already).

With the map reloaded, this function needs to `return true` to inform its caller ({{< lookup/cref GameLoop >}}) that there is a discontinuity in the game state and it should not continue trying to draw the frame it had been working on -- it needs to start all over.

```c
    } else if (playerDeadTime == 0) {
        if (playerHurtCooldown == 44) {
            DrawPlayer(
                playerBaseFrame + PLAYER_PAIN, playerX, playerY,
                DRAW_MODE_WHITE
            );
        } else if (playerHurtCooldown > 40) {
            DrawPlayer(
                playerBaseFrame + PLAYER_PAIN, playerX, playerY,
                DRAW_MODE_NORMAL
            );
        }

        if (playerHurtCooldown != 0) playerHurtCooldown--;

        if (playerHurtCooldown < 41) {
            if (!isPlayerPushed) {
                DrawPlayer(
                    playerBaseFrame + playerFrame, playerX, playerY,
                    DRAW_MODE_NORMAL
                );
            } else {
                DrawPlayer(
                    playerPushForceFrame, playerX, playerY, DRAW_MODE_NORMAL
                );
            }
        }
```

This `else if` body runs whenever {{< lookup/cref playerDeadTime >}} is zero, and represents the "happy path" of player sprite drawing: The player is not falling off the map, and they are not dead. They may, however, be experiencing pain _or_ an involuntary push in some direction, which selects one of a few {{< lookup/cref DrawPlayer >}} calls according to this table:

{{< lookup/cref playerHurtCooldown >}} | {{< lookup/cref isPlayerPushed >}} | `DRAW_MODE_`...                                    | Sprite Frame
---------------------------------------|------------------------------------|----------------------------------------------------|-------------
0--40                                  | `false`                            | {{< lookup/cref name="DRAW_MODE" text="NORMAL" >}} | {{< lookup/cref playerBaseFrame >}} + {{< lookup/cref playerFrame >}}
0--40                                  | `true`                             | {{< lookup/cref name="DRAW_MODE" text="NORMAL" >}} | {{< lookup/cref playerPushForceFrame >}}
41--43                                 | ---                                | {{< lookup/cref name="DRAW_MODE" text="NORMAL" >}} | {{< lookup/cref playerBaseFrame >}} + {{< lookup/cref name="PLAYER" text="PLAYER_PAIN" >}}
44                                     | ---                                | {{< lookup/cref name="DRAW_MODE" text="WHITE" >}}  | {{< lookup/cref playerBaseFrame >}} + {{< lookup/cref name="PLAYER" text="PLAYER_PAIN" >}}

Each path draws the player at {{< lookup/cref playerX >}} and {{< lookup/cref playerY >}} without modification. Any non-zero value in {{< lookup/cref playerHurtCooldown >}} decrements in the process.

{{% note %}}
The {{< lookup/cref DrawPlayer >}} code considers {{< lookup/cref playerHurtCooldown >}} as a means to flash the player's sprite. The player is only drawn if {{< lookup/cref playerHurtCooldown >}} is even. This means that the non-white {{< lookup/cref name="PLAYER" text="PLAYER_PAIN" >}} frame is only visible for a single game tick, which makes it very easy to miss.

{{< lookup/cref playerHurtCooldown >}} also decrements _in between_ the blocks that check for pain versus regular sprite drawing, which effectively jumps from the visible pain state in "{{< lookup/cref playerHurtCooldown >}} = 42" to the visible normal state in "{{< lookup/cref playerHurtCooldown >}} = 40."
{{% /note %}}

```c
    } else if (playerDeadTime < 10) {
        if (playerDeadTime == 1) {
            StartSound(SND_PLAYER_HURT);
        }

        playerDeadTime++;
        DrawPlayer(
            PLAYER_DEAD_1 + (playerDeadTime % 2), playerX - 1, playerY,
            DRAW_MODE_IN_FRONT
        );
```

This `else if` handles the early (but still nonzero) counts of {{< lookup/cref playerDeadTime >}}. Values from 1 to 9 are handled here. The player is recently dead, and should be drawn as a stationary angel in the spot where the fatal hit occurred.

On the first trip through the body here, {{< lookup/cref playerDeadTime >}} will be 1 and {{< lookup/cref StartSound >}} queues the {{< lookup/cref name="SND" text="SND_PLAYER_HURT" >}} sound effect for playback. This is necessary because the {{< lookup/cref HurtPlayer >}} call that killed the player chose not to play its own sound effect.

{{< lookup/cref playerDeadTime >}} increments during each game tick, and {{< lookup/cref DrawPlayer >}} uses that value modulo 2 to select between two player sprite frames: {{< lookup/cref name="PLAYER" text="PLAYER_DEAD_1" >}} and {{< lookup/cref name="PLAYER" text="PLAYER_DEAD_2" >}}. These two frames show the player dressed as an angel with flapping wings, with {{< lookup/cref name="DRAW_MODE" text="DRAW_MODE_IN_FRONT" >}} requesting that nothing cover it. The {{< lookup/cref playerX >}} value needs to be adjusted by one because the angel sprite frames are two tiles wider than the regular sprite, and this keeps them centered relative to where the player had been. {{< lookup/cref playerY >}} needs no correction, since the angel's height is the same as the rest of the frames.

```c
    } else if (playerDeadTime > 9) {
        if (scrollY > 0 && playerDeadTime < 12) {
            scrollY--;
        }

        if (playerDeadTime == 10) {
            StartSound(SND_PLAYER_DEATH);
        }

        playerY--;
        playerDeadTime++;
        DrawPlayer(
            PLAYER_DEAD_1 + (playerDeadTime % 2), playerX - 1, playerY,
            DRAW_MODE_IN_FRONT
        );
```

Once {{< lookup/cref playerDeadTime >}} reaches 10, the previous branch stops occurring and this one takes over. The player is still dead and still drawn as an angel but now it should rise up off the top of the screen.

When {{< lookup/cref playerDeadTime >}} has values of either 10 or 11 (and assuming {{< lookup/cref scrollY >}} is sufficiently high to support this) the scroll position is adjusted to show additional area at the top of the map. This scrolls everything down on the screen by two tiles, giving the angel a bit more vertical space to rise through before leaving the screen. During the first step, when {{< lookup/cref playerDeadTime >}} is 10, {{< lookup/cref StartSound >}} queues the {{< lookup/cref name="SND" text="SND_PLAYER_DEATH" >}} effect.

During every tick, from here until the level restarts, {{< lookup/cref playerY >}} decrements (moving the angel one tile higher on the screen) and {{< lookup/cref playerDeadTime >}} increments. {{< lookup/cref DrawPlayer >}} draws the sprite exactly how it did in the previous branch when the angel was stationary.

```c
        if (playerDeadTime > 36) {
            LoadGameState('T');
            InitializeLevel(levelNum);
            return true;
        }
```

Once {{< lookup/cref playerDeadTime >}} exceeds 36, the player sprite is almost certainly off the screen and the level should be restarted. {{< lookup/cref LoadGameState >}} reloads the game state from the temporary [save file]({{< relref "save-file-format" >}}) in the `'T'` slot and {{< lookup/cref InitializeLevel >}} reloads and resets all of the map state to play {{< lookup/cref levelNum >}}.

With the map reloaded, this function needs to `return true` to inform its caller ({{< lookup/cref GameLoop >}}) that there is a discontinuity in the game state and it should not continue trying to draw the frame it had been working on -- it needs to start all over.

```c
    }

    return false;
}
```

In the majority of cases, no path through this function restarts the level and the game loop should continue working on the current frame. `false` is returned as an indication that everything is normal and nothing in here interfered with the state of the world.

{{< boilerplate/function-cref SET_PLAYER_DIZZY >}}

The {{< lookup/cref SET_PLAYER_DIZZY >}} macro puts the player into a "dizzy" state, which will begin to take effect the next time they are standing on solid ground. This is structured as a macro to provide a counterpart to the {{< lookup/cref ClearPlayerDizzy >}} function.

```c
#define SET_PLAYER_DIZZY() { queuePlayerDizzy = true; }
```

{{< lookup/cref queuePlayerDizzy >}} marks the player as needing to enter the dizzy state, but does not directly place them into such a state. For the player's dizziness to take effect, they must be standing on the ground. Typically this function will be called while the player is free-falling, and they need to land before queued dizziness becomes actual dizziness.

{{< boilerplate/function-cref ProcessPlayerDizzy >}}

The {{< lookup/cref ProcessPlayerDizzy >}} function determines when a queued bout of dizziness should become effective, and handles the cases where dizziness wears off naturally or is abruptly canceled.

Dizziness is queued by setting {{< lookup/cref queuePlayerDizzy >}} to true, but other parts of the game respond to the dizzy condition (e.g. by immobilizing the player) by reading {{< lookup/cref playerDizzyLeft >}}. This function bridges the two variables together and manages their lifecycles.

```c
void ProcessPlayerDizzy(void)
{
    static word shakeframes[] = {
        PLAYER_SHAKE_1, PLAYER_SHAKE_2, PLAYER_SHAKE_3, PLAYER_SHAKE_2,
        PLAYER_SHAKE_1, PLAYER_SHAKE_2, PLAYER_SHAKE_3, PLAYER_SHAKE_2,
        PLAYER_SHAKE_1
    };
```

Dizziness is visualized as a three frame animation sequence of the player's sprite shaking its head back and forth. The graphics are such that these frames can be looped in a "ping-pong" sequence and look convincing. The `shakeframes[]` that form the animation are {{< lookup/cref name="PLAYER" text="PLAYER_SHAKE_1..3" >}}. Also worth noting, these array elements are played in _reverse_ order.

```c
    if (playerClingDir != DIR4_NONE) {
        queuePlayerDizzy = false;
        playerDizzyLeft = 0;
    }
```

If a pounce is queued while the player is in midair, and they push into a wall to initiate a cling, {{< lookup/cref playerClingDir >}} will take a value that is not {{< lookup/cref name="DIR4" text="DIR4_NONE" >}}. This cancels the queued dizzy spell in the same way {{< lookup/cref ClearPlayerDizzy >}} would -- that function's body is repeated in this `if` body.

```c
    if (
        queuePlayerDizzy &&
        TestPlayerMove(DIR4_SOUTH, playerX, playerY + 1) != MOVE_FREE
    ) {
        queuePlayerDizzy = false;
        playerDizzyLeft = 8;
        StartSound(SND_PLAYER_LAND);
    }
```

If {{< lookup/cref queuePlayerDizzy >}} is true, it's necessary to determine if the player is standing on the ground. (The player can't experience dizziness while jumping or falling, only standing.) {{< lookup/cref TestPlayerMove >}} evaluates the map blocks below the player's feet at {{< lookup/cref playerX >}} and {{< lookup/cref playerY >}} plus one -- the player stands _on_ the tiles, not _in_ them -- to see if a move is permitted into them in the {{< lookup/cref name="DIR4" text="DIR4_SOUTH" >}} direction. If {{< lookup/cref name="MOVE" text="MOVE_FREE" >}} is returned, there is air below the player and they can't be dizzy here.

Otherwise, they are on the ground and the `if` body runs. {{< lookup/cref queuePlayerDizzy >}} is set to false and {{< lookup/cref playerDizzyLeft >}} becomes eight. Queued dizziness has become actual dizziness.

With a nonzero {{< lookup/cref playerDizzyLeft >}}, the regular {{< lookup/cref MovePlayer >}} function becomes a no-op and is no longer available to play the landing sound effect. So that is done here, with {{< lookup/cref StartSound >}} queuing {{< lookup/cref name="SND" text="SND_PLAYER_LAND" >}}.

```c
    if (playerDizzyLeft != 0) {
        playerFrame = shakeframes[playerDizzyLeft];
        playerDizzyLeft--;
        isPlayerFalling = false;

        if (playerDizzyLeft > 8) {
            ClearPlayerDizzy();
        }
    }
}
```

Whenever {{< lookup/cref playerDizzyLeft >}} is nonzero, the player is dizzy and this state needs to be managed. Visually, the dizzy effect is produced by forcing {{< lookup/cref playerFrame >}} to one of the `shakeframes[]` values, as selected by {{< lookup/cref playerDizzyLeft >}}. It starts at eight, picking the last element in the array.

{{< lookup/cref playerDizzyLeft >}} is decremented, moving one step closer to having the dizziness wear off.

{{< lookup/cref isPlayerFalling >}} is also cleared here, which is probably a workaround for {{< lookup/cref MovePlayer >}} being disabled and missing the landing event.

The test for {{< lookup/cref playerDizzyLeft >}} greater than eight is most likely cruft. I do not see any way for this condition to ever be true. It looks like the original implementation was built around an incrementing counter, which would call {{< lookup/cref ClearPlayerDizzy >}} once it incremented to the target maximum.

{{< boilerplate/function-cref ClearPlayerDizzy >}}

The {{< lookup/cref ClearPlayerDizzy >}} function resets all the global variables related to the player's "dizziness" immobilization, immediately returning the player to normal state.

```c
void ClearPlayerDizzy(void)
{
    queuePlayerDizzy = false;
    playerDizzyLeft = 0;
}
```

Normally only one of these variables will need to be reset -- {{< lookup/cref queuePlayerDizzy >}} is true when the player is waiting for dizziness to kick in, while {{< lookup/cref playerDizzyLeft >}} is nonzero while the dizziness is actively affecting the player. Nevertheless, both are reset here to immediately cure the dizziness, or to prevent its onset if it has been queued.

{{< boilerplate/function-cref AddScoreForSprite >}}

The {{< lookup/cref AddScoreForSprite >}} function determines how many points should be added to the player's score for defeating an actor of a given `sprite_type`, and adds that amount. The status bar is updated to reflect the new score.

This function does not spawn any floating score effects or other rewards. Its only concern is incrementing the score in the status bar.

```c
void AddScoreForSprite(word sprite_type)
{
    switch (sprite_type) {
    case SPR_JUMPING_BULLET:
        AddScore(800);
        break;

    case SPR_GHOST:
    case SPR_MOON:
    case SPR_SHARP_ROBOT_FLOOR:
    case SPR_SHARP_ROBOT_CEIL:
        AddScore(400);
        break;
```

The entire function follows this pattern. `sprite_type` is tested in a large `switch`, and the matching `case` is the one that calls {{< lookup/cref AddScore >}} with the hard-coded number of points. {{< lookup/cref name="SPR" text="SPR_JUMPING_BULLET" >}} gives 800 points, while each {{< lookup/cref name="SPR" text="SPR_GHOST" >}}, {{< lookup/cref name="SPR" text="SPR_MOON" >}}, {{< lookup/cref name="SPR" text="SPR_SHARP_ROBOT_FLOOR" >}}, and so on grants only 400.

Once the points are added, `break` exits the `switch`, which also ends the function.

```c
    case SPR_SAW_BLADE:
        AddScore(3200);
        break;

    case SPR_SPEAR:
    case SPR_STONE_HEAD_CRUSHER:
    case SPR_PARACHUTE_BALL:
        AddScore(1600);
        break;

    case SPR_SPARK:
    case SPR_RED_JUMPER:
        AddScore(6400);
        break;

    case SPR_SPIKES_FLOOR:
    case SPR_SPIKES_FLOOR_RECIP:
    case SPR_SPIKES_E:
    case SPR_SPIKES_W:
        AddScore(250);
        break;

    case SPR_SUCTION_WALKER:
    case SPR_SPITTING_TURRET:
        AddScore(1000);
        break;

    case SPR_ROAMER_SLUG:
    case SPR_HINT_GLOBE:
        AddScore(12800);
        break;

    case SPR_PUSHER_ROBOT:
        AddScore(2000);
        break;

    case SPR_ARROW_PISTON_W:
    case SPR_ARROW_PISTON_E:
    case SPR_SPIKES_E_RECIP:
    case SPR_SPIT_WALL_PLANT_E:
    case SPR_SPIT_WALL_PLANT_W:
    case SPR_RED_CHOMPER:
    case SPR_SENTRY_ROBOT:
        AddScore(500);
        break;

    case SPR_DRAGONFLY:
        AddScore(50000L);
        break;

    case SPR_74:
    case SPR_BABY_GHOST_EGG:
    case SPR_EYE_PLANT:
    case SPR_96:
    case SPR_PINK_WORM_SLIME:
    case SPR_BIRD:
        AddScore(100);
        break;
```

The two odd sprites {{< lookup/cref name="SPR" text="SPR_74" >}} and {{< lookup/cref name="SPR" text="SPR_96" >}} are cases that get tested, but never happen. There are no actors in the game that use these sprite types. There are _actor_ types with these numbers (specifically, variants of the {{< lookup/actor type=74 strip=true >}} and {{< lookup/actor type=96 strip=true >}}), but they use sprite types that are already covered by other cases here.

```c
    case SPR_STAR:
    case SPR_CABBAGE:
    case SPR_HEART_PLANT:
    case SPR_BABY_GHOST:
    case SPR_CLAM_PLANT:
    case SPR_84:
    case SPR_PINK_WORM:
    case SPR_ROCKET:
        AddScore(200);
        break;
    }
}
```

Similarly, {{< lookup/cref name="SPR" text="SPR_84" >}} is a variant of {{< lookup/actor type=84 strip=true >}} that is already handled by another case.

As this `switch` has no default case, any unhandled `sprite_type` passed to this function will be ignored, leaving the score unchanged.
