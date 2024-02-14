+++
title = "Decoration Functions"
description = "Describes the functions that create and process decorations that are emitted from many actors."
weight = 500
+++

# Decoration Functions

A **decoration** is a sequence of sprite frames that can be set to play at an arbitrary map position. Decorations may play once or loop a fixed number of times. They may also be drawn fixed at one position on the map or move in a straight line in any one of eight directions. Decorations disappear once they have looped the necessary number of times, or when they have completely left the area visible on the screen.

Most of the decorations in the game are some form of sparkle or rising smoke, although there are many other inventive uses for them.

{{< table-of-contents >}}

## The Decoration Interface

To create a decoration, the caller must provide several pieces of information. The most important things to provide are the **sprite type** and the total number of **frames** the sprite has -- the game does have a way to determine the number of frames available to each sprite type dynamically. The decoration will start on frame zero and increment up to the maximum, at which point the loop is complete and the frame is reset to zero. Separately there is a **repetition** argument that controls how many times the sprite loop will play from frame zero up to the maximum. Once the sprite frame sequence has repeated that many times, the decoration is removed.

Each decoration has an X and Y position on the map, and a direction argument that takes one of the {{< lookup/cref DIR8 >}} values. {{< lookup/cref name="DIR8" text="DIR8_NONE" >}} produces a decoration that is fixed in one position; any other value will move one tile in the specified direction during each **tick** of gameplay. Decorations are not aware of the map contents; they do not stop or interact with any map tiles aside from the ["in-front" tile attribute]({{< relref "tile-attributes-format#in-front" >}}) occlusion that most sprites experience.

All decorations are removed once they move/scroll completely off the screen. It is possible to create an endlessly-looping decoration by setting the repetition count to zero, but the decoration will still be removed once it scrolls out of view.

## Special Cases

More than typical [entities]({{< relref "entities" >}}), decorations have special behavior depending on the sprite type being displayed. These behaviors exist to support map-wide effects inserted by {{< lookup/cref DrawRandomEffects >}}:

* Throughout the game, various map tiles are marked as "[slippery]({{< relref "tile-attributes-format#slippery" >}})" in the tile attributes data and will randomly glisten with a {{< lookup/cref name="SPR" text="SPR_SPARKLE_SLIPPERY" >}} decoration. These sprites are drawn with the {{< lookup/cref name="DRAW_MODE" text="DRAW_MODE_IN_FRONT" >}} option to ensure that no part of the map (or any other sprite, typically) can cover up the sparkle. Any other decorations could be obscured by map tiles with the "[in-front]({{< relref "tile-attributes-format#in-front" >}})" attribute set.
* Maps that enable the [rain flag]({{< relref "map-format#map-variables-word" >}}) generate {{< lookup/cref name="SPR" text="SPR_RAINDROP" >}} decorations moving in the {{< lookup/cref name="DIR8" text="DIR8_SOUTHWEST" >}} direction. When these decorations are processed during each tick, the horizontal position is adjusted one additional tile to the west, and the vertical position is adjusted randomly between zero and two additional tiles to the south. This makes each raindrop move faster, with some variance in the fall speed.

{{< boilerplate/function-cref InitializeDecorations >}}

The {{< lookup/cref InitializeDecorations >}} function clears all of the memory slots used to store decoration state, immediately terminating all incomplete decoration animations and making each slot available for use.

```c
void InitializeDecorations(void)
{
    word i;

    for (i = 0; i < numDecorations; i++) {
        decorations[i].alive = false;
    }
}
```

The {{< lookup/cref numDecorations >}} variable always holds the value from the constant {{< lookup/cref MAX_DECORATIONS >}}, which is 10 regardless of the episode, level, or state of the current map. In the outermost `for` loop, `i` increments from zero to nine, covering every decoration slot.

The {{< lookup/cref decorations >}} array maintains a list of {{< lookup/cref Decoration >}} structures, each one having an `alive` member variable. Each decoration is marked "alive" at creation time, and this flag is cleared again once the animation has run to the end. Since none of the decorations here should be running, `alive` is set to false.

When this function returns, all decorations will be reset to their idle state, ready to be activated at some future time.

{{< boilerplate/function-cref NewDecoration >}}

The {{< lookup/cref NewDecoration >}} function creates a new decoration at `x_origin` and `y_origin` consisting of the passed `sprite_type` with an animation duration of `num_frames`. `dir` controls the straight-line direction the decoration will move in, and `num_times` controls how many times the animation sequence will play before ending.

{{< note >}}If there is no room in the {{< lookup/cref decorations >}} array (due to too many decorations already running) this function does nothing.{{< /note >}}

`dir` should be a {{< lookup/cref DIR8 >}} value. It is possible to set `num_times` to zero for a decoration that persists for as long as it can be seen on the screen. The maximum possible lifetime of the decoration is `num_frames` &times; `num_times`, in ticks. The decoration may end earlier if it totally leaves the scrolling game window.

```c
void NewDecoration(
    word sprite_type, word num_frames, word x_origin, word y_origin,
    word dir, word num_times
) {
    word i;

    for (i = 0; i < numDecorations; i++) {
        Decoration *dec = decorations + i;
```

The outermost `for` loop runs once for each decoration slot, up to {{< lookup/cref numDecorations >}}. Within the loop, `dec` points to the {{< lookup/cref Decoration >}} structure from the {{< lookup/cref decorations >}} array that's currently being processed.

```c
        if (dec->alive) continue;
```

Each decoration uses the `alive` member variable to mark whether or not it is active. If a decoration's `alive` flag is true, it indicates that the current slot holds a decoration that is still progressing and should not be overwritten. In this case, the loop `continue`s onto the next slot, hopefully eventually finding one with an inactive decoration.

```c
        dec->alive = true;
        dec->sprite = sprite_type;
        dec->numframes = num_frames;
        dec->x = x_origin;
        dec->y = y_origin;
        dec->dir = dir;
        dec->numtimes = num_times;
```

With a suitable decoration slot located, the `alive` flag is enabled and the six arguments from the caller are stored in the {{< lookup/cref Decoration >}} structure.

```c
        decorationFrame[i] = 0;
```

The motivation behind this aspect of the design is utterly unknown. In terms of storage requirements, each {{< lookup/cref Decoration >}} structure needs to keep track of the sprite frame that's currently being displayed so it can be incremented and tested against the `numframes` maximum. When the animation is set to repeat, this frame number needs to reset to zero and increment toward `numframes` again. It would make perfect sense for {{< lookup/cref Decoration >}} to have an additional member variable here named "frame" or somesuch, but it has none.

Instead, a separate {{< lookup/cref decorationFrame >}} array serves this purpose, totally detached from the {{< lookup/cref Decoration >}} structure. I can't (and won't) even hazard a guess as to why it was set up this way.

Here the {{< lookup/cref decorationFrame >}} array is indexed by `i`, same as its sibling {{< lookup/cref decorations >}}, and the frame number is set to zero. This prepares the sprite's animation to play from the beginning.

```c
        break;
    }
}
```

The last thing done here is a `break` to terminate the outer `for` loop, since we no longer need to check for any more free decoration slots -- we just found and used one up. With this `break` (or with the `for` loop running to exhaustion without finding a suitable decoration slot), the function returns.

{{< boilerplate/function-cref NewPounceDecoration >}}

The {{< lookup/cref NewPounceDecoration >}} function inserts six decorations representing pieces of pounce debris into the game world, radiating away from the origin point specified in `x` and `y`.

```c
void NewPounceDecoration(word x, word y)
{
    NewDecoration(SPR_POUNCE_DEBRIS, 6, x + 1, y,     DIR8_SOUTHWEST, 2);
    NewDecoration(SPR_POUNCE_DEBRIS, 6, x + 3, y,     DIR8_SOUTHEAST, 2);
    NewDecoration(SPR_POUNCE_DEBRIS, 6, x + 4, y - 2, DIR8_EAST,      2);
    NewDecoration(SPR_POUNCE_DEBRIS, 6, x + 3, y - 4, DIR8_NORTHEAST, 2);
    NewDecoration(SPR_POUNCE_DEBRIS, 6, x + 1, y - 4, DIR8_NORTHWEST, 2);
    NewDecoration(SPR_POUNCE_DEBRIS, 6, x,     y - 2, DIR8_WEST,      2);
}
```

Each call to {{< lookup/cref NewDecoration >}} creates a decoration using the {{< lookup/cref name="SPR" text="SPR_POUNCE_DEBRIS" >}} sprite type, which consists of a six-frame animation cycle. Each decoration is set to play all the way through twice.

The `x`, `y`, and {{< lookup/cref DIR8 >}} constants set up a radial pattern:

{{< image src="pounce-decoration-2052x.png"
    alt="Diagram of the origin and initial position of each element of the pounce decoration."
    1x="pounce-decoration-684x.png"
    2x="pounce-decoration-1368x.png"
    3x="pounce-decoration-2052x.png" >}}

The origin is conceptually the bottom-left tile of a 5 &times; 5 circle, so the `x`/`y` positions should be compensated if it's necessary to center the decorations against an actor that is significantly smaller or larger.

{{< boilerplate/function-cref MoveAndDrawDecorations >}}

The {{< lookup/cref MoveAndDrawDecorations >}} function draws, advances the animation step, and moves each decoration currently running, and handles looping and ending conditions.

```c
void MoveAndDrawDecorations(void)
{
    int i;

    for (i = 0; i < (int)numDecorations; i++) {
        Decoration *dec = decorations + i;
```

The outermost `for` loop runs once for each decoration slot, up to {{< lookup/cref numDecorations >}}. Within the loop, `dec` points to the {{< lookup/cref Decoration >}} structure from the {{< lookup/cref decorations >}} array that's currently being processed. (The cast to `int` is necessary to match the way the original game was compiled.)

```c
        if (!dec->alive) continue;
```
Each decoration uses the `alive` member variable to track whether or not it is currently active. If a decoration's `alive` flag is false, it indicates that the current slot holds a decoration that is not currently active and should not be processed. In this case, the loop `continue`s onto the next slot, looking for a decoration that's ready.

```c
        if (IsSpriteVisible(dec->sprite, dec->numframes, dec->x, dec->y)) {
```

Here we have an active decoration. The outermost `if` uses {{< lookup/cref IsSpriteVisible >}} to determine if the decoration sprite `dec->sprite` is still in view at position `dec->x` and `dec->y`.

**There is a bug here.** The second argument to {{< lookup/cref IsSpriteVisible >}} should be {{< lookup/cref name="decorationFrame" text="decorationFrame[i]" >}}, not `dec->numframes`. This oversight is investigated in more detail [below](#sprite-visibility-bug).

When the sprite is visible, the bulk of this code executes. Otherwise we jump to the furthest `else` branch (which unsets the `alive` flag).

```c
            if (dec->sprite != SPR_SPARKLE_SLIPPERY) {
                DrawSprite(
                    dec->sprite, decorationFrame[i], dec->x, dec->y,
                    DRAW_MODE_NORMAL
                );
            } else {
                DrawSprite(
                    dec->sprite, decorationFrame[i], dec->x, dec->y,
                    DRAW_MODE_IN_FRONT
                );
            }
```
The pattern used in this function is to draw the sprite first, then move it in preparation for a future frame. {{< lookup/cref DrawSprite >}} draws the active `dec->sprite` type using the frame number from {{< lookup/cref name="decorationFrame" text="decorationFrame[i]" >}} at the current `dec->x` and `dec->y` positions. There are two almost-identical calls here -- the one with {{< lookup/cref name="DRAW_MODE" text="DRAW_MODE_NORMAL" >}} is used in the typical case, while {{< lookup/cref name="DRAW_MODE" text="DRAW_MODE_IN_FRONT" >}} is used for any sprite having the {{< lookup/cref name="SPR" text="SPR_SPARKLE_SLIPPERY" >}} type.

```c
            if (dec->sprite == SPR_RAINDROP) {
                dec->x--;
                dec->y += random(3);
            }

            dec->x += dir8X[dec->dir];
            dec->y += dir8Y[dec->dir];
```

This handles movement, starting with the special case code for the {{< lookup/cref name="SPR" text="SPR_RAINDROP" >}} sprite type. Raindrops here are moved left on the screen by one tile position, and down by a {{< lookup/cref random >}} value between zero and two tiles. This adjustment is _in addition to_ the regular movement that all decorations have.

`dec->dir` contains a {{< lookup/cref DIR8 >}} value describing how this decoration should move, and that is used as an index into the {{< lookup/cref dir8X >}} and {{< lookup/cref dir8Y >}} arrays to determine how to adjust `dec->x` and `dec->y` to move the decoration. The component in each dimension gets -1, 0, or 1 added to it to perform the movement.

```c
            decorationFrame[i]++;
            if (decorationFrame[i] == dec->numframes) {
                decorationFrame[i] = 0;
                if (dec->numtimes != 0) {
                    dec->numtimes--;
                    if (dec->numtimes == 0) {
                        dec->alive = false;
                    }
                }
            }
```

This is the animation and looping code. At each step, {{< lookup/cref name="decorationFrame" text="decorationFrame[i]" >}} is incremented to select the next frame of animation. If `dec->numframes` is reached, there are no more sprite frames and {{< lookup/cref name="decorationFrame" text="decorationFrame[i]" >}} resets to zero for (potentially) another loop.

Each time the animation frame resets to zero, `dec->numtimes` is tested then decremented. Once `dec->numtimes` decrements to zero, the decoration has no more loops to show and `dec->alive` is set to false to remove it. In the case where `dec->numtimes` is _already_ zero, the nested `if`s never run and the animation loops an unlimited number of times.

```c
        } else {
            dec->alive = false;
        }
    }
}
```

This `else` branch is taken when the earlier sprite visibility check fails. This occurs when the sprite has moved/scrolled completely off the screen and no part of it is still visible. In this case, `dec->alive` is set to false to remove the decoration.

The outer `for` loop continues running until all decoration slots have been handled, and then the function returns.

### Sprite Visibility Bug

{{< lookup/cref MoveAndDrawDecorations >}} determines the visibility of each sprite using the following test:

```c
if (IsSpriteVisible(dec->sprite, dec->numframes, dec->x, dec->y)) { ... }
```

Nominally, the second argument to {{< lookup/cref IsSpriteVisible >}} is the frame number within the sprite type to test against. This is needed because some sprite types change size during the course of their animation, and we're interested in the visibility of the sprite frame using its currently-shown dimensions. In actuality, `dec->numframes` is passed. This is not the currently displayed frame, and in fact is not _any_ frame for the sprite. (A sprite with `numframes = 4` should only have frame numbers 0&ndash;3. Frame four is out of bounds.)

The structure of the [tile info data]({{< relref "tile-info-format" >}}) is such that reading past the last frame of one sprite type begins reading into the starting frames of the subsequent sprite type. Essentially the arguments `dec->sprite, dec->numframes` behave as if they were `dec->sprite + 1, 0`. This only becomes a serious memory access violation when the highest sprite type in the game is used (which doesn't occur); instead we simply get the wrong answer to the question.

When the game reads tile info for a larger sprite than necessary, the decoration continues being drawn some distance off the edge of the screen even though it should've expired. When it reads a smaller sprite, the potential exists for a decoration that's partially off the left or bottom edges of the screen to be removed while still in view.

Of all the sprite types used by the decoration system, the following are immediately succeeded in the tile info data by sprites that have smaller dimensions:

* {{< lookup/cref name="SPR" text="SPR_DOOR_YELLOW" >}} (3 &times; 5) followed by {{< lookup/cref name="SPR" text="SPR_SPARKLE_SHORT" >}} (3 &times; 3)
* {{< lookup/cref name="SPR" text="SPR_SPARKLE_SHORT" >}} (3 &times; 3) followed by {{< lookup/cref name="SPR" text="SPR_JUMP_PAD_ROBOT" >}} (4 &times; 2)
* {{< lookup/cref name="SPR" text="SPR_SMOKE_LARGE" >}} (4 &times; 3) followed by {{< lookup/cref name="SPR" text="SPR_SPARKLE_SLIPPERY" >}} (2 &times; 2)

Each of these sprite types is capable of disappearing prematurely when partially off the left or bottom screen edges. It is very difficult to see this effect, but it is possible. In my own testing, I had the best luck using watching {{< lookup/cref name="SPR" text="SPR_SMOKE_LARGE" >}} as released by the {{< lookup/actor type=249 plural=true >}} on E1M7, for instance. Make the player walk to the right while watching smoke scroll off the left edge of the screen, and eventually you'll catch a moment where the smoke abruptly disappears before it really should.
