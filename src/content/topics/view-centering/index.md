+++
title = "View Centering"
description = "Describes the similarities and differences found in each instance of the screen scrolling/centering logic."
weight = 430
+++

# View Centering

For one reason or another, there is no centralized function responsible for centering the scrolling game window on the player's position. This behavior is handled in a couple of unrelated areas of the game code with both redundancies and differences in each. The descriptions here attempt to describe the implementation both succinctly and accurately.

View centering occurs, to various degrees, in each of the following functions:

* {{< lookup/cref ActTransporter >}}
* {{< lookup/cref MovePlayer >}}
* {{< lookup/cref MovePlayerPlatform >}}
* {{< lookup/cref MovePlayerPush >}}
* {{< lookup/cref MovePlayerScooter >}}
* {{< lookup/cref NewMapActorAtIndex >}}

In general, view centering tries to keep the player in the center third of the scrolling game window. In cases where the edge of the map is reached, scrolling stops and the player is permitted to move to the edges of the screen. Scrolling resumes once they return back to the center. Typically the window will scroll as fast as the player moves, keeping the player fixed on a location on the screen.

The user can usually press the <kbd>Up</kbd> or <kbd>Down</kbd> arrow keys to artificially move the scroll position up or down a bit, allowing for additional visibility into nearby areas. The look distance is constrained so that the player never leaves the view.

{{< table-of-contents >}}

## Player Emergence

There are two situations where the player can "appear" at an arbitrary location without moving to that place: the player is placed at a starting position when a new level begins, or they can take a ride in a transporter. Both events use similar logic with differences in the constants involved.

### Level Start

In the {{< lookup/cref NewMapActorAtIndex >}} function, in the code responsible for interpreting a {{< lookup/cref name="SPA" text="SPA_PLAYER_START" >}} actor from the map data, a pair of `x`/`y` coordinates is used to place the player. From these values, an appropriate value for {{< lookup/cref scrollX >}} and {{< lookup/cref scrollY >}} is chosen:

```c
if (x > mapWidth - 15) {
    scrollX = mapWidth - SCROLLW;
} else if (x - 15 >= 0 && mapYPower > 5) {
    scrollX = x - 15;
} else {
    scrollX = 0;
}

if (y - 10 >= 0) {
    scrollY = y - 10;
} else {
    scrollY = 0;
}
```

In the horizontal position, the intention is to set {{< lookup/cref scrollX >}} to the position 15 tiles left of the player start position in `x`. If the player is too close to the right edge of the map, {{< lookup/cref scrollX >}} is clamped to {{< lookup/cref mapWidth >}} minus {{< lookup/cref SCROLLW >}} to prevent panning off the right edge of the map. Similarly, negative values for {{< lookup/cref scrollX >}} are clamped to zero, preserving the left limit of the map.

{{% note %}}The test for {{< lookup/cref mapYPower >}} greater than five is always true. For the map to have a {{< lookup/cref mapYPower >}} of five or less, the map would need to be 32 or fewer tiles wide. This would not be wide enough to fill the width of the screen of this game, and none of the stock maps do this.{{% /note %}}

Vertical positioning is similar, setting {{< lookup/cref scrollY >}} to the position ten tiles above the player's feet. Clamping occurs at the top of the map, but _not_ at the bottom. A player start position in the bottom eight tiles of the map would initialize {{< lookup/cref scrollY >}} to a value that draws outside of map bounds, but this condition is corrected externally in {{< lookup/cref DrawMapRegion >}} before it can cause problems:

```c
if (scrollY > maxScrollY) scrollY = maxScrollY;
```

### Transporters

Transporters handle view centering in the {{< lookup/cref ActTransporter >}} function:

```c
if (playerX - 14 < 0) {
    scrollX = 0;
} else if (playerX - 14 > mapWidth - SCROLLW) {
    scrollX = mapWidth - SCROLLW;
} else {
    scrollX = playerX - 14;
}

if (playerY - 12 < 0) {
    scrollY = 0;
} else if (playerY - 12 > maxScrollY) {
    scrollY = maxScrollY;
} else {
    scrollY = playerY - 12;
}
```

This is the same idea as the player start position, but in this case the view is scrolled to the point 14 tiles left of and 12 tiles above the player's position in {{< lookup/cref playerX >}}/{{< lookup/cref playerY >}}. All four map edges are clamped here.

## Regular Player Movement

The {{< lookup/cref MovePlayer >}} function is responsible for handling all user-controlled movement of the player on foot.

If the player is standing on a surface that is both slippery and sloped, they will slide down and to the side. If the slope descends in the west direction, this code handles view centering:

```c
if (playerY - scrollY > SCROLLH - 4) {
    scrollY++;
}

if (playerX - scrollX < 12 && scrollX > 0) {
    scrollX--;
}
```

As the player is sliding down and to the left, {{< lookup/cref scrollY >}} is incremented and {{< lookup/cref scrollX >}} is decremented to match the corresponding changes in the player position (not shown here). This keeps the player sprite at the same position on the screen while scrolling the map around them.

The vertical scroll does not start until the player is at least 15 tiles ({{< lookup/cref SCROLLH >}}` - 4`) below the top of the scrolling window. Similarly the horizontal scroll requires the player to be closer than 12 tiles from the left edge of the window before scrolling will happen, and scrolling off the left edge of the map is not permitted.

Conversely, the player could slide east instead:

```c
if (playerY - scrollY > SCROLLH - 4) {
    scrollY++;
}

if (playerX - scrollX > SCROLLW - 15 && mapWidth - SCROLLW > scrollX) {
    scrollX++;
}
```

The vertical component code is identical. Horizontally, {{< lookup/cref scrollX >}} is incremented to follow the player's change in position so long as the player is 24 or more tiles ({{< lookup/cref SCROLLW >}}` - 15`) away from the left edge of the scrolling window (and as long as the scroll will not exceed the {{< lookup/cref mapWidth >}} constraint.)

When slippery surfaces are not involved, the regular view centering code occurs once per frame:

```c
if (playerY - scrollY > SCROLLH - 4) {
    scrollY++;
}

if (clingslip && playerY - scrollY > SCROLLH - 4) {
    scrollY++;
} else {
    if (playerMomentumNorth > 10 && playerY - scrollY < 7 && scrollY > 0) {
        scrollY--;
    }

    if (playerY - scrollY < 7 && scrollY > 0) {
        scrollY--;
    }
}

if (
    playerX - scrollX > SCROLLW - 15 && mapWidth - SCROLLW > scrollX &&
    mapYPower > 5
) {
    scrollX++;
} else if (playerX - scrollX < 12 && scrollX > 0) {
    scrollX--;
}
```

The vertical band is between 7 and 14 (a.k.a. {{< lookup/cref SCROLLH >}}` - 4`) tiles above the position of the player's feet. If the top edge of the scrolling window ({{< lookup/cref scrollY >}}) is within that range of tiles from {{< lookup/cref playerY >}}, no scrolling adjustment is done. Otherwise {{< lookup/cref scrollY >}} is incremented or decremented by one tile to bring the view closer to center. This may take several frames to resolve, which causes the "elastic" return of the view position once one of the "look up/down" keys is released. {{< lookup/cref scrollY >}} is never permitted to be less than zero, but it may become too high for the map and scroll off the bottom edge. As mentioned earlier, {{< lookup/cref DrawMapRegion >}} has code to protect against this condition.

The `clingslip` variable holds a true value when the player is clinging to a slippery tile and sliding down. In this case {{< lookup/cref scrollY >}} is incremented an additional tile down to allow the player to better see what they are falling towards. In the opposite direction, {{< lookup/cref playerMomentumNorth >}} stores a magnitude that relates to how fast the player is rising vertically -- when this value is greater than ten it indicates a very fast ascent and {{< lookup/cref scrollY >}} is decremented an additional tile to allow the player to better see where they are headed.

The horizontal centering occurs next, and follows substantially the same patterns as the earlier code for slippery slopes. The only difference here is a check that {{< lookup/cref mapYPower >}} is larger than five, which is always true for every map included with the game. (See the [Level Start](#level-start) section of this page for an explanation of why this assertion is true.) Taken together, this works to keep the player inside a 12--23 (a.k.a. {{< lookup/cref SCROLLW >}}` - 15`) tile band measured from the left edge of the screen.

There is one other scrolling adjustment in {{< lookup/cref MovePlayer >}}. This occurs when the player is falling, and looks like the following (heavily simplified) snippet:

```c
if (isPlayerFalling && ...) {
    playerY++;
    ...
    if (playerFallTime > 3) {
        playerY++;
        scrollY++;
        if (TestPlayerMove(DIR4_SOUTH, playerX, playerY) != MOVE_FREE) {
            ...
            playerY--;
            scrollY--;
            ...
        }
    }
    if (playerFallTime < 25) playerFallTime++;
}
```

When the player is falling, {{< lookup/cref isPlayerFalling >}} sensibly holds a true value and the outermost block executes. During each frame, {{< lookup/cref playerY >}} is incremented without an associated change in scroll position. This allows the player to fall short distances without necessarily re-centering the screen. The view may still be adjusted elsewhere if the player falls too close to a screen edge.

During each frame of falling, {{< lookup/cref playerFallTime >}} is incremented up to a maximum of 25. Any time {{< lookup/cref playerFallTime >}} is over three, the player falls an additional tile during every frame -- doubling the fall speed. Since the regular view centering can only move the screen one tile per frame, {{< lookup/cref scrollY >}} is incremented here to help the view keep up with the player's fall speed.

If the player falls inside the floor during this double-speed movement, they will need to be "ejected" one tile higher, canceling the second tile of movement in both {{< lookup/cref playerY >}} and {{< lookup/cref scrollY >}}. This allows the player to fall an even number of tiles while landing successfully on a surface an odd distance away.

## Scooter Movement

During times when the player is riding a scooter, the {{< lookup/cref MovePlayerScooter >}} function is responsible for moving the player around the map. The centering behavior here works the same as that in {{< lookup/cref MovePlayer >}}:

```c
if (playerY - scrollY > SCROLLH - 4) {
    scrollY++;
} else {
    if (playerMomentumNorth > 10 && playerY - scrollY < 7 && scrollY > 0) {
        scrollY--;
    }

    if (playerY - scrollY < 7 && scrollY > 0) {
        scrollY--;
    }
}

if (playerX - scrollX > SCROLLW - 15 && mapWidth - SCROLLW > scrollX) {
    scrollX++;
} else if (playerX - scrollX < 12 && scrollX > 0) {
    scrollX--;
}
```

This is effectively the same as the code in the regular {{< lookup/cref MovePlayer >}}, including the test against {{< lookup/cref playerMomentumNorth >}} which has no purpose here -- its value is forced to zero for the entire time the player is riding on the scooter.

## Platform Movement

During times when the player is riding one of the platforms (or mud fountains), the {{< lookup/cref MovePlayerPlatform >}} function moves the player in tandem with the platform. As part of this movement, the scroll position is adjusted to keep the player inside the scrolling game window.

```c
if ((cmdNorth || cmdSouth) && !cmdWest && !cmdEast) {
    if (cmdNorth && scrollY > 0 && playerY - scrollY < SCROLLH - 1) {
        scrollY--;
    }

    if (cmdSouth && (
        scrollY + 4 < playerY || (dir8Y[y_dir] == 1 && scrollY + 3 < playerY)
    )) {
        scrollY++;
    }
}
```

The first bit of the view code handles the look up/down behavior, usually mapped to the <kbd>Up</kbd> and <kbd>Down</kbd> arrow keys. When such movement is requested and permitted, {{< lookup/cref cmdNorth >}} or {{< lookup/cref cmdSouth >}} will be true to indicate the requested action.

The outer `if` prevents the <kbd>Up</kbd> and <kbd>Down</kbd> keys from being handled if <kbd>Left</kbd> or <kbd>Right</kbd> is simultaneously held ({{< lookup/cref cmdWest >}} and {{< lookup/cref cmdEast >}}). This prevents looking while walking at the same time.

When {{< lookup/cref cmdNorth >}} is held and {{< lookup/cref scrollY >}} is greater than zero, the player wants to look up and there is enough map data in that direction to avoid scrolling off the top edge. An additional check ensures that the player will not scroll off the bottom of the screen ({{< lookup/cref SCROLLH >}}` - 1`). If everything looks good, {{< lookup/cref scrollY >}} is decremented to shift the map down one tile on the screen.

{{< lookup/cref cmdSouth >}} follows a similar pattern to look down, which shifts the map up on the screen. This ensures that the player is not scrolled off the top edge of the screen. A secondary check serves as a bit of a hack: The local `y_dir` variable is looked up through {{< lookup/cref dir8Y >}} to extract the vertical movement component, and it's checked against the constant 1. If this condition is true, the player is riding a platform that is moving down on the screen and the test against {{< lookup/cref playerY >}} is repeated with a smaller constant. The idea is to allow the player to be able to look down one additional tile if they are moving downwards. As long as there is room for the scroll using either of the tests, {{< lookup/cref scrollY >}} is incremented to shift the map up on the screen.

```c
if (playerY - scrollY > SCROLLH - 1) {
    scrollY++;
} else if (playerY - scrollY < 3) {
    scrollY--;
}
```

This keeps the player inside the screen bounds vertically. Unlike many of the other centering functions, this allows the player to ride a platform all the way to the bottom edge of the screen before {{< lookup/cref scrollY >}} is incremented to accommodate them.

The opposite check is also lenient to an excessive degree. It will not begin decrementing {{< lookup/cref scrollY >}} until the top _two_ tiles of the player sprite are off the top edge of the screen. (The player is five tiles tall.) Even after correction, the player's head can be left cut off here.

```c
if (playerX - scrollX > SCROLLW - 15 && mapWidth - SCROLLW > scrollX) {
    scrollX++;
} else if (playerX - scrollX < 12 && scrollX > 0) {
    scrollX--;
}
```

In the horizontal direction, the scrolling behavior is reminiscent of other implementations found elsewhere in the game. {{< lookup/cref scrollX >}} is incremented when the player is within 15 tiles of the right edge of the screen, and {{< lookup/cref scrollX >}} is decremented when the player is within 12 tiles of the left edge, both constrained to the map data available to be displayed.

```c
if (dir8Y[y_dir] == 1 && playerY - scrollY > SCROLLH - 4) {
    scrollY++;
}

if (dir8Y[y_dir] == -1 && playerY - scrollY < 3) {
    scrollY--;
}
```

Particular to the platform view centering code, a bit of logic handles the vertical movement component of the platform the player is riding. `y_dir` is a local variable containing the movement direction, which is used as an index into {{< lookup/cref dir8Y >}} to produce a value of 0, 1 (player is moving down on the screen), or -1 (player is moving up).

Both of these `if` blocks repeat work that was already done. In the case of downward movement, the only difference here is a smaller value on the right side of the comparison that causes the screen to scroll before the player gets near the bottom of the screen. Upward, the test is identical to the earlier code and the decrement never occurs.

## Push

The {{< lookup/cref MovePlayerPush >}} function is responsible for involuntary changes to the player's position. This typically happens during interactions with a "pushy" actor, but the pipe systems also use this mechanism to transport the player.

```c
if (
    dir8X[playerPushDir] + scrollX > 0 &&
    dir8X[playerPushDir] + scrollX < mapWidth - (SCROLLW - 1)
) {
    scrollX += dir8X[playerPushDir];
}

if (dir8Y[playerPushDir] + scrollY > 2) {
    scrollY += dir8Y[playerPushDir];
}
```

The global {{< lookup/cref playerPushDir >}} variable holds a nonzero {{< lookup/cref DIR8 >}} value while the player is experiencing a push. The {{< lookup/cref dir8X >}} and {{< lookup/cref dir8Y >}} lookup tables decompose the direction into X and Y movement components, each having a value between -1 and 1 depending on direction. The X component is added to {{< lookup/cref scrollX >}} and, provided the movement wouldn't scroll off the edge of the map, {{< lookup/cref scrollX >}} is adjusted to keep the player in view.

{{< lookup/cref scrollY >}} is adjusted similarly, except the bounds checking only tests the top edge of the map. (The bottom edge is checked in {{< lookup/cref DrawMapRegion >}}), so any over-scroll here is quickly corrected before causing trouble.

```c
if (wallhit) {
    ...
    scrollX -= dir8X[playerPushDir];
    scrollY -= dir8Y[playerPushDir];
    ...
}
```

{{< lookup/cref MovePlayerPush >}} follows a philosophy of "beg forgiveness" as opposed to "ask permission." It moves the player first, _then_ checks to see if the player moved inside a wall or other impassible area of the map. `wallhit` will be true whenever this happens, and the move is unwound by subtracting all the movement components that had just been added. {{< lookup/cref scrollX >}} and {{< lookup/cref scrollY >}} are reverted as part of this process.
