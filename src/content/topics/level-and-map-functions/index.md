+++
title = "Level and Map Functions"
description = "Describes functions that select, load, and manage levels and the map data they refer to."
weight = 390
+++

# Level and Map Functions

There are two distinct, but closely related concepts related to the progression of gameplay: levels and maps. While superficially similar, and interchangeable in common parlance, they refer to different things and are not exactly the same. This page explains the differences in detail, and highlights the functions in the game's code that are responsible for loading and interacting with each.

{{< table-of-contents >}}

## Maps vs. Levels

**Maps** are data blobs that represent a two-dimensional grid of tiles. Each tile cell may contain nothing (i.e. it is "air" that the player can walk through), a solid piece of the environment that restricts movement, or a semi-transparent feature that may be walked through in certain directions/circumstances. Each episode of the game ships with either 10 or 11 regular maps, plus two bonus maps, for a grand total of 12 or 13 maps.

On disk, [map files]({{< relref "map-format" >}}) additionally contain a handful of **map variables** that control behavior of the game engine, plus a variable-length sequence of actors and their start positions. When loaded into memory, however, the map is only the tile grid; the map variables and actors are maintained in separate and unrelated areas of memory.

**Levels** are a more nuanced construction, and refer to the current position in the _sequence of maps_. The bonus maps are repeated as levels are progressed, which causes the level numbers to increase faster than map numbers. This sequence can be explained most succinctly with a table:

Level | Map    | Notes
------|--------|------
0     | A1     | First level played when a new game is started.
1     | A2     | If the player collected &lt;25 stars, skips to A3 upon completion.
2     | BONUS1 | Lesser bonus level, occurs after A2 if the player collected 25&ndash;49 stars. When completed, skips to A3.
3     | BONUS2 | Better bonus level, occurs after A2 if the player collected &ge;50 stars. When completed, proceeds to A3.
4     | A3     |
5     | A4     |
6     | BONUS1 | Works the same as level 2, but skips to A5 on completion.
7     | BONUS2 | Works the same as level 3, but proceeds to A5 on completion.
8     | A5     |
9     | A6     |
10    | BONUS1 | Works the same as level 2, but skips to A7 on completion.
11    | BONUS2 | Works the same as level 3, but proceeds to A7 on completion.
12    | A7     |
13    | A8     |
14    | BONUS1 | Works the same as level 2, but skips to A9 on completion.
15    | BONUS2 | Works the same as level 3, but proceeds to A9 on completion.
16    | A9     |
17    | A10    | Last level for episodes two and three; progression stops at the conclusion of this level.
18    | BONUS1 | Episode one only. Works the same as level 2, but skips to A11 on completion.
19    | BONUS2 | Episode one only. Works the same as level 3, but proceeds to A11 on completion.
20    | A11    | Episode one only.

{{< note >}}These are the map names for episode one. The other episodes use names like B*, C*, and BONUS3&ndash;6.{{< /note >}}

The key to understanding this is to remember that there is a "section" intermission after every two levels, which conditionally allows the player to proceed to one of the bonus levels. There are only two bonus maps in the whole game, but they may be played multiple times. The level concept allows the game to keep track of which occurrence of a bonus map has been reached, and to determine which regular map should come next.

{{< aside class="fun-fact" >}}
**See for yourself.**

An effect of this can be seen by using the {{< lookup/cref PromptLevelWarp >}} cheat. Choose one of the bonus levels and play it to completion, and you will find that the next level is always 4. This is because {{< lookup/cref PromptLevelWarp >}} uses levels 2 and 3 to access these maps, which is the first instance of the bonus maps in the level progression.
{{< /aside >}}

{{< boilerplate/function-cref NextLevel >}}

The {{< lookup/cref NextLevel >}} function selects the next level to be played in the progression. Depending on the number of stars collected, it conditionally takes the player to or from one of the bonus levels at regular intervals. If a demo is being recorded or played back, a fixed (and discontinuous) progression of levels is selected instead.

```c
void NextLevel(void)
{
    word stars = (word)gameStars;
```

This function maintains a local copy of the `stars` count from {{< lookup/cref gameStars >}}. This is necessary because the global star count will be zeroed during calls to {{< lookup/cref ShowSectionIntermission >}}, but subsequent logic needs to know the value that was held previously.

```c
    if (demoState != DEMO_STATE_NONE) {
        switch (levelNum) {
        case 0:
            levelNum = 13;
            break;
        case 13:
            levelNum = 5;
            break;
        case 5:
            levelNum = 9;
            break;
        case 9:
            levelNum = 16;
            break;
        }

        return;
    }
```

If a demo is being recorded or played back ({{< lookup/cref demoState >}} is anything other than {{< lookup/cref name="DEMO_STATE" text="DEMO_STATE_NONE" >}}), the level progression is much more constrained. There are only four expected values for {{< lookup/cref levelNum >}} to be in, and the `switch` statement leaves the level number in the next expected state. The final progression is level numbers 0, 13, 5, 9, and 16. Once the last level in the sequence has been reached, progression stops and the game is essentially "stuck" on that level until the demo ends.

The designer of each episode, and the person recording the demo, must be mindful of this hard-coded progression of levels and end the demo before the progression would require an additional level.

In this mode, the function does nothing else and simply `return`s.

```c
    switch (levelNum) {
    case 2:
    case 6:
    case 10:
    case 14:
    case 18:
    case 22:
    case 26:
        levelNum++;
```

In the typical case, a demo is neither being recorded nor played back, and the level progression follows the normal order expected by the player. This behavior is also handled by a `switch` statement. The cases here start at level 2 and cover every fourth level number possible. This handles instances where the player has finished one of the lesser bonus levels.

To cover this case, {{< lookup/cref levelNum >}} is simply incremented and then execution _falls through_ to the next case. This effectively discards this case, and fudges the progression into the state it would've been in had the player completed one of the better bonus levels instead.

```c
    case 3:
    case 7:
    case 11:
    case 15:
    case 19:
    case 23:
    case 27:
        ShowSectionIntermission("Bonus Level Completed!!", "Press ANY key.");
```

This case covers level 3 and every fourth level past it. These are all the "better" bonus levels. This is also where execution arrives after the fudging of lesser levels discussed previously. In practice, this is where _all_ bonus levels end. As such, it is appropriate to {{< lookup/cref ShowSectionIntermission >}} with a message stating the bonus level has been completed.

Once the intermission screen has been shown, execution falls through to the next case.

```c
    case 0:
    case 4:
    case 8:
    case 12:
    case 16:
    case 20:
    case 24:
        levelNum++;
        break;
```

This case covers level 0 (which is the first level in the game) and every fourth level past it. Execution also arrives here at the conclusion of any bonus level.

Nothing special is presented to the user here; there are no intermission screens between the two levels of each section, nor is there anything else to do upon returning from a bonus level. Simply move onto the next level in the progression by incrementing {{< lookup/cref levelNum >}} by one and `break` out.

```c
    case 1:
    case 5:
    case 9:
    case 13:
    case 17:
    case 21:
    case 25:
        ShowSectionIntermission("Section Completed!", "Press ANY key.");
```

This is the interesting case, covering level 1 and every fourth level past it. This is the demarcation point between sections, and the place where bonus levels _might_ be encountered. Each time one of these levels is completed, {{< lookup/cref ShowSectionIntermission >}} states this fact with section-specific message text.

This case needs to do one of three things, depending on the number of stars the player collected:

* 25&ndash;49 stars: Increment {{< lookup/cref levelNum >}} by one to advance to the lesser bonus level.
* &ge;50 stars: Increment {{< lookup/cref levelNum >}} by two to advance to the better bonus level.
* &lt;25 stars: Increment {{< lookup/cref levelNum >}} by three to skip both of the bonus levels and go directly to the next regular level in the progression.

This logic is a bit fragmented, but happens below.

```c
        if (stars > 24) {
            FadeOutCustom(0);
            ClearScreen();
            DrawFullscreenImage(IMAGE_BONUS);
            StartSound(SND_BONUS_STAGE);
```

Here we must use our local copy of `stars` because {{< lookup/cref ShowSectionIntermission >}} zeroed the global {{< lookup/cref gameStars >}} value while tallying the bonus points. If the player collected 25 or more stars, they earned the right to play a bonus level.

{{< lookup/cref FadeOutCustom >}} fades the screen to black with a quick delay setting of 0, and {{< lookup/cref ClearScreen >}} erases the display. Neither of these calls are strictly necessary because {{< lookup/cref DrawFullscreenImage >}} does its own fading and implicitly erases the screen while drawing. {{< lookup/cref name="IMAGE" text="IMAGE_BONUS" >}} is placed on the screen, and {{< lookup/cref StartSound >}} queues a short tune ({{< lookup/cref name="SND" text="SND_BONUS_STAGE" >}}) to accompany it.

```c
            if (stars > 49) {
                levelNum++;
            }
            levelNum++;
            WaitHard(150);
```

Since we know the player already collected enough stars to play _some_ bonus level, {{< lookup/cref levelNum >}} should always be incremented by at least one. If the player collected more than 49 stars, {{< lookup/cref levelNum >}} is incremented by one again to select the better bonus level.

In either case, {{< lookup/cref WaitHard >}} pauses for a bit while the {{< lookup/cref name="IMAGE" text="IMAGE_BONUS" >}} image is on-screen.

```c
        } else {
            levelNum += 3;
        }

        break;
    }
}
```

In the other branch of the `if` statement, the player collected fewer than 25 stars. In that case, increment {{< lookup/cref levelNum >}} by three to skip both bonus levels, and do not show or play anything pertaining to the bonus functionality.

Regardless of the path taken through this case, execution `break`s out of this function and returns to the caller.

{{< boilerplate/function-cref LoadMapData >}}

The {{< lookup/cref LoadMapData >}} function reads the map file associated with the passed `level_num` and initializes the global variables that are most affected by a map file's contents.

```c
void LoadMapData(word level_num)
{
    word i;
    word actorwords;
    word t;
    FILE *fp = GroupEntryFp(mapNames[level_num]);
```

There are a few local variables used here, some of which are a bit convoluted:

* `i` is a regular loop index variable.
* `actorwords` will hold the size of the variable-length actors data area in the map file. This is measured in 16-bit words.
* `t` serves multiple purposes depending on where it appears. In its first appearances, it holds an actor's "type" identifier. Later, it becomes a horizontal tile offset while initializing any {{< lookup/special-actor type=1 plural=true >}} the map may have.
* `fp` is a pointer to a file stream for the map file that is being loaded.

To start, the passed `level_num` is looked up in the {{< lookup/cref mapNames >}} array to produce a [group file entry]({{< relref "group-file-format" >}})'s name. This name is passed to {{< lookup/cref GroupEntryFp >}} which opens the file and seeks to the start of the data, returning the file stream pointer into `fp`.

```c
    isCartoonDataLoaded = false;

    getw(fp);
    mapWidth = getw(fp);
```

The memory arena used for holding the map's tile data ({{< lookup/cref mapData >}}) is used as scratch space in a few different places in the game. Most notably, it can hold [cartoon images]({{< relref "databases/cartoon-sprite" >}}) that are shown during some of the [dialogs]({{< relref "dialog-functions" >}}). The {{< lookup/cref isCartoonDataLoaded >}} flag tracks whether this memory currently holds cartoon image data, saving it from being reloaded unnecessarily if so. This function is going to overwrite {{< lookup/cref mapData >}} with map tile data, so {{< lookup/cref isCartoonDataLoaded >}} is set to false to indicate that the cartoon images are no longer there.

{{< lookup/cref getw >}} reads one 16-bit word from `fp` and discards it, advancing the read position in the process. This skips over the [map variables]({{< relref "map-format#map-variables-word" >}}), which are not handled in this function.

{{< lookup/cref getw >}} again reads a 16-bit word from `fp`, storing it into the global {{< lookup/cref mapWidth >}} variable. Only the width of the map is stored in the file; the height is implicitly known based on the property that all maps are 32,768 tiles&sup2; in size.

```c
    switch (mapWidth) {
    case 1 << 5:
        mapYPower = 5;
        break;
    case 1 << 6:
        mapYPower = 6;
        break;
    case 1 << 7:
        mapYPower = 7;
        break;
    case 1 << 8:
        mapYPower = 8;
        break;
    case 1 << 9:
        mapYPower = 9;
        break;
    case 1 << 10:
        mapYPower = 10;
        break;
    case 1 << 11:
        mapYPower = 11;
        break;
    }
```

The game doesn't actually care how high the map is in the majority of cases. What it _does_ care about is how to translate a two-dimensional X,Y pair of tile coordinates into a one-dimensional tile offset in memory, and how to compute that as quickly as possible. To do this, it uses a novel property of the map size: All the factors of 32,768 can be expressed as **2<sup>n</sup>**. To convert from X,Y coordinates to a tile offset, the calculation used by the game is **X + (Y &times; 2<sup>n</sup>)**, with **n = log<sub>2</sub>(mapWidth)**.

Some might ask what the point of all that hassle is when you could just as easily do **X + (Y &times; mapWidth)** and be done with it. The reason is due to a binary math trick: Any expression that can be written as **Y &times; 2<sup>n</sup>** can be implemented using the bitwise left-shift **Y \<\< n** instead. These operations are incredibly fast on CPUs, especially compared to the multiplications they replace, and the map widths used by this game ensure that these properties always work.

Here a `switch` block is employed to match a predefined list of {{< lookup/cref mapWidth >}} values with the appropriate {{< lookup/cref mapYPower >}} to use for this map. Subsequent operations that look up tiles in memory do so by bitwise-left-shifting Y by {{< lookup/cref mapYPower >}} and adding X to the result.

{{< note >}}{{< lookup/cref mapYPower >}} 5 is never used; such maps would be too narrow to cover the full width of the screen. Likewise, {{< lookup/cref mapYPower >}} 11 is never used because the map would not cover the screen's height.{{< /note >}}

```c
    actorwords = getw(fp);
    numActors = 0;
    numPlatforms = 0;
    numFountains = 0;
    numLights = 0;
    areLightsActive = true;
    hasLightSwitch = false;
```

{{< lookup/cref getw >}} reads the next word from the map file `fp`, which is the size of the actor data in _words_. This value is stored in the local `actorwords` variable for later use.

{{< lookup/cref numActors >}}, {{< lookup/cref numPlatforms >}}, {{< lookup/cref numFountains >}}, {{< lookup/cref numLights >}}, {{< lookup/cref areLightsActive >}}, and {{< lookup/cref hasLightSwitch >}} are all initialized to reasonable default values. By default, lights on each map are active until a relevant {{< lookup/actor type=120 strip=true >}} actor is added.

```c
    fread(mapData.w, actorwords, 2, fp);

    for (i = 0; i < actorwords; i += 3) {
        register word x, y;

        t = *(mapData.w + i);
        x = *(mapData.w + i + 1);
        y = *(mapData.w + i + 2);
        NewMapActorAtIndex(numActors, t, x, y);

        if (numActors > MAX_ACTORS - 1) break;
    }
```

{{< lookup/cref fread >}} copies a number of two-byte records from `fp` to a scratch area in {{< lookup/cref mapData >}}. The size of the data copied is governed by the value in `actorwords`. Because this value is measured in words, the **w**ord union member of {{< lookup/cref mapData >}} is used.

The `for` loop runs once for each actor defined in the map file. Each actor's map file data consists of three words, hence the increment by three. On each iteration, the actor's type is read from {{< lookup/cref mapData >}} into `t`, the X position into `x`, and Y position into `y`. (See the [map format]({{< relref "map-format#list-of-actors" >}}) for details on the structure of this data.) Each of these is passed to the {{< lookup/cref NewMapActorAtIndex >}} function which constructs the specified actor.

The involvement of {{< lookup/cref numActors >}} is a bit convoluted because of a mixture of pass-by-value and pass-by-global semantics. Essentially, {{< lookup/cref numActors >}} is a counter of the number of actors that have been created so far, and it can also be used during map construction as the position in the actors array where the next new actor should be created. Since this is a brand new map and none of the actors are dead yet, it is not necessary to scan the list of existing actors to look for a dead actor to overwrite -- we can simply create each actor at the {{< lookup/cref numActors >}} position and then increment that counter.

If {{< lookup/cref numActors >}} exceeds {{< lookup/cref name=MAX_ACTORS text="MAX_ACTORS - 1">}}, the actor list is full and no more data can be processed. `break` out of this loop and do not process any more actor data that might be present.

```c
    fread(mapData.b, WORD_MAX, 1, fp);
    fclose(fp);
```

Finally, the real map data is read into {{< lookup/cref mapData >}}. `fp`'s read position now points to the first byte of data past the end of the variable-length actor data, and should have {{< lookup/cref WORD_MAX >}} bytes of data left to read via {{< lookup/cref fread >}}. Here we are counting in byte units, which necessitates use of the **b**yte union member of {{< lookup/cref mapData >}}. Once the data has been read, {{< lookup/cref fclose >}} closes the group file and releases the resources that `fp` pointed to.

```c
    for (i = 0; i < numPlatforms; i++) {
        for (t = 2; t < 7; t++) {
            *((word *)(platforms + i) + t) = MAP_CELL_DATA_SHIFTED(
                platforms[i].x, platforms[i].y, t - 4
            );
        }
    }
```

A bit of special processing is necessary to handle {{< lookup/special-actor type=1 plural=true >}}. These are implemented as map tiles that move around. As each platform moves out of a tile position that it previously occupied, it must restore the original map tiles that were at that location before it arrived there. This set of loops handles the initial positioning for each platform, saving the map tiles that each platform is going to cover up once the first frame of gameplay runs.

The outer `for` loop is straightforward, it increments `i` from zero up to the last platform defined according to {{< lookup/cref numPlatforms >}}. The inner `for` loop is _heinous_.

The {{< lookup/cref Platform >}} structure contains an `x` word, a `y` word, and a five-word `mapstash[]` array. Each platform is five tiles wide, with its center tile at the X,Y position. The idea is that `mapstash[0]` should store the tile from `x - 2`, `mapstash[2]` should get the tile from `x`, and `mapstash[4]` should have `x + 2`, and so on for the other two elements.

Instead of writing anything remotely resembling that, the author chose to recast the {{< lookup/cref Platform >}} structure to a `word` array and hard-code offsets to the structure members (2 for `mapstash[0]`, 3 for `mapstash[1]`, etc.) instead. When `t` increments from 2 to 6, it is really incrementing from `mapstash[0]` to `mapstash[4]`.

{{< lookup/cref MAP_CELL_DATA_SHIFTED >}} is a macro that reads the tile data at a given X,Y position, plus an arbitrary expression to add to the X coordinate. During each read, the X position evaluates to `x + t - 4` which is a convoluted way of spanning `x - 2` to `x + 2`.

When all is said and done, each {{< lookup/cref Platform >}}'s `mapstash[]` array holds a copy of the five map tiles centered around the platform's starting X/Y position.

```c
    levelNum = level_num;
    maxScrollY = (word)(0x10000L / (mapWidth * 2)) - (SCROLLH + 1);
}
```

Before the function ends, the global {{< lookup/cref levelNum >}} is updated to the passed `level_num` value. {{< lookup/cref maxScrollY >}} is also computed to govern how far down the map is allowed to scroll before its movement is constrained.

Each map grid is nominally 10000h bytes (in practice, all the map grids that ship with the retail game are FFF8h bytes for reasons not entirely known). {{< lookup/cref mapWidth >}} is measured in tiles, and multiplying that by two yields bytes. Dividing the former by the latter gives the total height of the map in tiles. From this, we subtract the {{< lookup/cref SCROLLH >}} screen height constant plus one. The addition of one sets the maximum scrolling Y position (that is, the row of map tiles positioned at the top of the screen when the map is scrolled to its bottom-most position) such that the last row of map tiles can never be seen. Most maps contain garbage or incomplete constructions in this row which is not suitable for display.

{{< boilerplate/function-cref GetMapTile >}}

The {{< lookup/cref GetMapTile >}} function returns the data for a single map tile positioned at horizontal position `x` and vertical position `y`.

```c
word GetMapTile(word x, word y)
{
    return MAP_CELL_DATA(x, y);
}
```

This function simply wraps the {{< lookup/cref MAP_CELL_DATA >}} macro, which performs the actual offset calculation and reads the data from map memory.

{{< boilerplate/function-cref SetMapTile >}}

The {{< lookup/cref SetMapTile >}} function sets one map tile at horizontal position `x` and vertical position `y` to the value passed in `value`.

```c
void SetMapTile(word value, word x, word y)
{
    MAP_CELL_DATA(x, y) = value;
}
```

This function uses the {{< lookup/cref MAP_CELL_DATA >}} macro to convert `x` and `y` into an offset, which is then used to dereference a pointer in map memory. This memory location receives the tile value held in the `value` variable.

{{< boilerplate/function-cref SetMapTileRepeat >}}

The {{< lookup/cref SetMapTileRepeat >}} function sets a horizontal span of `count` map tiles, starting at horizontal position `x_origin` and vertical position `y_origin`, to the value passed in `value`.

If the `count` should run off the right edge of the map, the position "wraps around" to the leftmost tile on the next row down. This behavior should not occur in an unmodified copy of the game, however.

```c
void SetMapTileRepeat(word value, word count, word x_origin, word y_origin)
{
    word x;

    for (x = 0; x < count; x++) {
        SetMapTile(value, x_origin + x, y_origin);
    }
}
```

This function simply wraps a call to {{< lookup/cref SetMapTile >}} in a `for` loop that iterates `count` times, moving the horizontal `x` offset one tile to the right on each iteration while updating the selected tile to `value`.

{{< boilerplate/function-cref SetMapTile4 >}}

The {{< lookup/cref SetMapTile4 >}} function sets a horizontal span of four map tiles, starting at horizontal position `x_origin` and vertical position `y_origin`, to the values passed in `val1` through `val4`.

If the sequence of four tiles should run off the right edge of the map, the position "wraps around" to the leftmost tile on the next row down. This behavior should not occur in an unmodified copy of the game, however.

```c
void SetMapTile4(
    word val1, word val2, word val3, word val4, word x_origin, word y_origin
) {
    SetMapTile(val1, x_origin,     y_origin);
    SetMapTile(val2, x_origin + 1, y_origin);
    SetMapTile(val3, x_origin + 2, y_origin);
    SetMapTile(val4, x_origin + 3, y_origin);
}
```

This function calls {{< lookup/cref SetMapTile >}} four times, with each call using the next `val...` variable provided by the caller and an X position one tile to the right of the previous one.

{{< boilerplate/function-cref MAP_CELL_ADDR >}}

The {{< lookup/cref MAP_CELL_ADDR >}} macro converts an `x` and `y` position, measured in zero-based tiles, into a pointer to the map data in memory.

```c
#define MAP_CELL_ADDR(x, y) (mapData.w + ((y) << mapYPower) + x)
```

Whenever a map is loaded (during {{< lookup/cref LoadMapData >}}) the {{< lookup/cref mapYPower >}} variable is set such that **2<sup>mapYPower</sup>** equals the width of the map. Because of this property, **Y \<\< mapYPower** is equivalent to **Y &times; mapWidth**, only the former is much faster to compute. The passed `x` is added to the running total, producing a one-dimensional tile offset that still refers to the intended tile. This is added as an offset to the {{< lookup/cref mapData >}} union, here using its **w**ord member, evaluating to a pointer to the word of map memory that represents the passed `x`, `y` position.

{{< note >}}The `x` in this macro is not parenthesized (although ideally it should be) in order to preserve the order-of-operations in the original game's compiled machine code.{{< /note >}}

{{< boilerplate/function-cref MAP_CELL_DATA >}}

The {{< lookup/cref MAP_CELL_DATA >}} macro looks up the value of a tile at an `x` and `y` position, measured in zero-based tiles, from the map data in memory.

```c
#define MAP_CELL_DATA(x, y) (*(mapData.w + (x) + ((y) << mapYPower)))
```

Aside from differences in order-of-operations, this works identically to {{< lookup/cref MAP_CELL_ADDR >}}. Once the offset has been computed, the pointer is dereferenced to access the actual value held in this tile's position.

{{< boilerplate/function-cref MAP_CELL_DATA_SHIFTED >}}

The {{< lookup/cref MAP_CELL_DATA_SHIFTED >}} macro looks up the value of a tile at an `x` and `y` position plus an arbitrary shift expression `shift_expr`, all measured in zero-based tiles, from the map data in memory.

```c
#define MAP_CELL_DATA_SHIFTED(x, y, shift_expr) \
    (*(mapData.w + (x) + ((y) << mapYPower) + shift_expr))
```

This is identical to {{< lookup/cref MAP_CELL_DATA >}}, except the value in `shift_expr` is added to the pointer's offset before dereferencing occurs. This is essentially the same as using {{< lookup/cref MAP_CELL_DATA >}} with `shift_expr` added to `x` at the call site, but this macro exists to preserve the order-of-operations in the original game's compiled machine code. (This is also the reason why `shift_expr` is not parenthesized.)

{{< boilerplate/function-cref TILE_BLOCK_SOUTH >}}

The {{< lookup/cref TILE_BLOCK_SOUTH >}} macro evaluates to a nonzero value if the tile value passed in `val` has its "block south movement" attribute flag set.

```c
#define TILE_BLOCK_SOUTH(val) (*(tileAttributeData + ((val) / 8)) & 0x01)
```

The {{< lookup/cref tileAttributeData >}} pointer references a block of memory that stores one byte of attribute flag data for each tile value. Tile addresses are spaced (at minimum) eight bytes apart from each other, so `val` gets divided by eight to scale the values down to the spacing that the [tile attributes]({{< relref "tile-attributes-format" >}}) data expects.

With the pointer plus offset dereferenced, the resulting attribute is ANDed with 1h to isolate the least-significant bit of the data. This will result in a zero value if the attribute flag is unset, or a nonzero value if set. This is the value the macro ultimately evaluates to.

When a tile has a "block south" attribute, players and actors cannot fall through it; the tile can be stood upon.

{{< boilerplate/function-cref TILE_BLOCK_NORTH >}}

The {{< lookup/cref TILE_BLOCK_NORTH >}} macro evaluates to a nonzero value if the tile value passed in `val` has its "block north movement" attribute flag set.

```c
#define TILE_BLOCK_NORTH(val) (*(tileAttributeData + ((val) / 8)) & 0x02)
```

This works similarly to {{< lookup/cref TILE_BLOCK_SOUTH >}}, but with the AND using 2h as a mask.

When a tile has a "block north" attribute, players and actors cannot jump through it; they will "hit their head" on the tile.

{{< boilerplate/function-cref TILE_BLOCK_WEST >}}

The {{< lookup/cref TILE_BLOCK_WEST >}} macro evaluates to a nonzero value if the tile value passed in `val` has its "block west movement" attribute flag set.

```c
#define TILE_BLOCK_WEST(val) (*(tileAttributeData + ((val) / 8)) & 0x04)
```

This works similarly to {{< lookup/cref TILE_BLOCK_SOUTH >}}, but with the AND using 4h as a mask.

When a tile has a "block west" attribute, players and actors cannot pass through the tile by moving left on screen; the tile behaves as a solid wall.

{{< boilerplate/function-cref TILE_BLOCK_EAST >}}

The {{< lookup/cref TILE_BLOCK_EAST >}} macro evaluates to a nonzero value if the tile value passed in `val` has its "block east movement" attribute flag set.

```c
#define TILE_BLOCK_EAST(val) (*(tileAttributeData + ((val) / 8)) & 0x08)
```

This works similarly to {{< lookup/cref TILE_BLOCK_SOUTH >}}, but with the AND using 8h as a mask.

When a tile has a "block east" attribute, players and actors cannot pass through the tile by moving right on screen; the tile behaves as a solid wall.

{{< boilerplate/function-cref TILE_SLIPPERY >}}

The {{< lookup/cref TILE_SLIPPERY >}} macro evaluates to a nonzero value if the tile value passed in `val` has its "is slippery" attribute flag set.

```c
#define TILE_SLIPPERY(val) (*(tileAttributeData + ((val) / 8)) & 0x10)
```

This works similarly to {{< lookup/cref TILE_BLOCK_SOUTH >}}, but with the AND using 10h as a mask.

When a tile is "slippery," the player cannot stand or cling to it without being pulled down by gravity. Slippery tiles can also sparkle randomly while in view.

{{< boilerplate/function-cref TILE_IN_FRONT >}}

The {{< lookup/cref TILE_IN_FRONT >}} macro evaluates to a nonzero value if the tile value passed in `val` has its "draw in front" attribute flag set.

```c
#define TILE_IN_FRONT(val) (*(tileAttributeData + ((val) / 8)) & 0x20)
```

This works similarly to {{< lookup/cref TILE_BLOCK_SOUTH >}}, but with the AND using 20h as a mask.

The {{< lookup/cref DrawSprite >}} and {{< lookup/cref DrawPlayer >}} functions will avoid drawing on top of tiles that have their "draw in front" attribute flag set, which has the effect of the tile blocking the sprite from view or the tile being located _in front_ of the sprite. This flag may be disregarded if a sprite drawing function is called using the {{< lookup/cref name=DRAW_MODE text=DRAW_MODE_IN_FRONT >}} mode. (This is relatively uncommon.)

{{< boilerplate/function-cref TILE_SLOPED >}}

The {{< lookup/cref TILE_SLOPED >}} macro evaluates to a nonzero value if the tile value passed in `val` has its "is sloped" attribute flag set.

```c
#define TILE_SLOPED(val) (*(tileAttributeData + ((val) / 8)) & 0x40)
```

This works similarly to {{< lookup/cref TILE_BLOCK_SOUTH >}}, but with the AND using 40h as a mask.

When a tile is "sloped," an actor or the player may walk into it (assuming no other attributes prohibit that) but their vertical position is adjusted to allow them to climb "up" the slope. Similarly, if an actor or the player is near a sloped tile but walks onto empty space, their vertical position is adjusted to make them descend the slope without free-falling.

{{< boilerplate/function-cref TILE_CAN_CLING >}}

The {{< lookup/cref TILE_CAN_CLING >}} macro evaluates to a nonzero value if the tile value passed in `val` has its "player can cling" attribute flag set.

```c
#define TILE_CAN_CLING(val) (*(tileAttributeData + ((val) / 8)) & 0x80)
```

This works similarly to {{< lookup/cref TILE_BLOCK_SOUTH >}}, but with the AND using 80h as a mask.

When a tile is flagged as "clingable," it is part of a vertical wall that prohibits movement through the tile, but the player is able to cling to it from the side by using his suction cup hands. Such walls can be climbed over, provided there is a continuous span of clingable tiles and sufficient free space surrounding them for the player to move through.
