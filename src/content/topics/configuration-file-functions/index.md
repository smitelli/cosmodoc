+++
title = "Configuration File Functions"
description = "Describes the functions that read and write the game's configuration files."
weight = 250
+++

# Configuration File Functions

{{< table-of-contents >}}

The game stores a few small pieces of configuration in a [configuration file]({{< relref "configuration-file-format" >}}) named COSMOx.CFG. This file holds the keyboard mapping preferences, the state of sound effect/music playback, and the high score table.

The configuration is loaded during the {{< lookup/cref Startup >}} process, and saved during {{< lookup/cref ExitClean >}}. If the configuration file does not exist, default values are loaded instead.

{{< boilerplate/function-cref LoadConfigurationData >}}

The {{< lookup/cref LoadConfigurationData >}} function loads and parses the contents of the [configuration file]({{< relref "configuration-file-format" >}}) named `filename` into several global variables. If the specified file does not exist, these variables are filled with default values.

The top-level structure of the function is:

```c
void LoadConfigurationData(char *filename)
{
    FILE *fp;
    char space;

    fp = fopen(filename, "rb");

    if (fp == NULL) {
        /* Config file is missing; fill in default values */
        ...
    } else {
        /* Config file is present; load its values */
        ...
    }
}
```

This is a straightforward A-or-B choice: {{< lookup/cref fopen >}} the file specified by `filename` and see if the return value is `NULL`. If it is, the configuration file was not present and there is nothing to load -- use the default values. Otherwise the file exists and can be read.

### Default Values

Here, `fp` is `NULL` so there is nothing else we can do with it -- the configuration file does not exist and the default settings must be loaded.

```c
        scancodeNorth = SCANCODE_KP_8;
        scancodeSouth = SCANCODE_KP_2;
        scancodeWest = SCANCODE_KP_4;
        scancodeEast = SCANCODE_KP_6;
        scancodeJump = SCANCODE_CTRL;
        scancodeBomb = SCANCODE_ALT;
        isMusicEnabled = true;
        isSoundEnabled = true;
```

The game implements six movement and action keys. They are configured according to their **scancodes**, where each key on the keyboard is numbered according to IBM specifications. The default keyboard configuration maps the four arrow keys to the four cardinal movement directions, the <kbd>Ctrl</kbd> key is used for "jump," and the <kbd>Alt</kbd> key is used for "bomb."

The scancode table is a bit limited in the fact that it doesn't actually have dedicated codes for the arrow keys, or the block of <kbd>Insert</kbd>/<kbd>Delete</kbd>/<kbd>Home</kbd>/<kbd>End</kbd>/<kbd>PgUp</kbd>/<kbd>PgDn</kbd> keys above them. This section of the keyboard was not present on the original IBM Model F keyboard,[^model-f] so codes weren't defined for them.

Instead, these functions were available through alternate functions on the numeric keypad. If the keyboard's Num Lock mode was _disabled_, the numeric keypad would perform these cursor control functions instead of typing numbers.

{{% aside class="fun-fact" %}}
**Hey, look down!**

Are you currently sitting in front of a full-size PC keyboard? Take a look at the numeric keypad. Does it have arrows and cursor movement keys? Turn Num Lock off and give 'em a whirl.

If your computer uses an OS that responds to <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>Del</kbd>, it should also respond the same way to <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>Num .</kbd> for similar reasons.
{{% /aside %}}

This is all a roundabout way of saying, if you want to read the arrow keys using the IBM scancode scheme, you have to read keys <kbd>8</kbd>/<kbd>2</kbd>/<kbd>4</kbd>/<kbd>6</kbd> on the numeric keypad to do it. That's what's being configured here.

{{< lookup/cref scancodeNorth >}} and {{< lookup/cref scancodeSouth >}} hold the "look up"/"look down" scancode values. {{< lookup/cref scancodeWest >}} and {{< lookup/cref scancodeEast >}} hold the "walk left"/"walk right" values and, conveniently enough, {{< lookup/cref scancodeJump >}} and {{< lookup/cref  scancodeBomb >}} hold the "jump"/"bomb" values.

{{< lookup/cref isMusicEnabled >}} and {{< lookup/cref isSoundEnabled >}} both default to true, enabling music and sound by default.

```c
        highScoreValues[0] = 1000000L;
        strcpy(highScoreNames[0], "BART");
        highScoreValues[1] = 900000L;
        strcpy(highScoreNames[1], "LISA");
        highScoreValues[2] = 800000L;
        strcpy(highScoreNames[2], "MARGE");
        highScoreValues[3] = 700000L;
        strcpy(highScoreNames[3], "ITCHY");
        highScoreValues[4] = 600000L;
        strcpy(highScoreNames[4], "SCRATCHY");
        highScoreValues[5] = 500000L;
        strcpy(highScoreNames[5], "MR. BURNS");
        highScoreValues[6] = 400000L;
        strcpy(highScoreNames[6], "MAGGIE");
        highScoreValues[7] = 300000L;
        strcpy(highScoreNames[7], "KRUSTY");
        highScoreValues[8] = 200000L;
        strcpy(highScoreNames[8], "HOMER");
```

The remainder of this branch of the function constructs the default high score table out of character names from _The Simpsons_. {{< lookup/cref highScoreValues >}} and {{< lookup/cref highScoreNames >}} are two parallel arrays that, taken together, represent the contents of this table. The scores can be initialized literally, but the names need to use {{< lookup/cref strcpy >}} for initialization.

{{% aside class="fun-fact" %}}
**"Marge, it takes two to lie... one to lie and one to listen."**

The March 1992 release date of the game coincides with the tail end of the third season of _The Simpsons_, right around the premiere of episode 20, "Colonel Homer."
{{% /aside %}}

With this branch of the code complete, the function returns.

### Load from Configuration File

On this branch of the function, the configuration file existed and `fp` refers to a readable file.

```c
        int i;

        scancodeNorth = fgetc(fp);
        scancodeSouth = fgetc(fp);
        scancodeWest = fgetc(fp);
        scancodeEast = fgetc(fp);
        scancodeJump = fgetc(fp);
        scancodeBomb = fgetc(fp);
        isMusicEnabled = fgetc(fp);
        isSoundEnabled = fgetc(fp);

        for (i = 0; i < 10; i++) {
            fscanf(fp, "%lu", &highScoreValues[i]);
            fscanf(fp, "%c", &space);
            fscanf(fp, "%[^\n]s", highScoreNames[i]);
        }

        fclose(fp);
```

The [configuration file format]({{< relref "configuration-file-format#format" >}}) encodes the six keyboard scancode mappings and two sound/music option flags as a series of eight byte values. These are read, one {{< lookup/cref fgetc >}} at a time, into their corresponding global configuration variables.

Following this data, the high score table is encoded as a consecutive series of packed values. The encoding scheme is "score, space, name, newline," and this occurs ten times in total.

For each table entry, the score component is read via {{< lookup/cref fscanf >}}, using a format specifier that consumes all digits `0`--`9` and interprets them as **l**ong **u**nsigned base 10 integers into an element of the {{< lookup/cref highScoreValues >}} array. Once the first non-digit character is reached, the score field is done.

The second {{< lookup/cref fscanf >}} consumes a single **c**haracter into a junk variable. This character is usually a space in a well-constructed configuration file, which is why the junk variable is named `space`.

The third {{< lookup/cref fscanf >}} contains what is called a "negated scanset," which consumes any number of characters until a newline (`\n`) is encountered. This reads the name component of the high score entry, for as many characters as it takes to reach a newline character. This is dangerous -- each element in {{< lookup/cref highScoreNames >}} is 16 bytes wide, and the last byte should be a null terminator. If any name field in the file is longer than 15 characters, this will read into adjacent high score table names and, quite possibly, unrelated memory.

The third format specifier (`"%[^\n]s"`) deserves a little more scrutiny. This is actually two separate things combined together. `%[^\n]` consumes and stores all characters until a newline (`\n`) is found. When that happens, the string is complete and `\n` remains on the input stream -- it will be the next character read. The `s` is a literal character; the programmer is saying "expect the next character read to be an `s` and throw it out." The next byte in the stream is not `s`, it's `\n`. Therefore the match fails and reading stops. The `\n` character remains on the input stream. On the _subsequent_ iteration of the `for` loop, the `"%lu"` specifier actually skips over whitespace characters that precede the digits, including `\n`, so this whole construction actually works correctly.

Once the high score table has been fully read, {{< lookup/cref fclose >}} cleans up the file pointer and the function returns.

{{< boilerplate/function-cref SaveConfigurationData >}}

The {{< lookup/cref SaveConfigurationData >}} function saves the state of the global game configuration variables to the configuration file named `filename`. Since all of the configuration variables are guaranteed to be in a good state while the program is running, there is no need for default handling here.

```c
void SaveConfigurationData(char *filename)
{
    FILE *fp;
    int i;

    fp = fopen(filename, "wb");

    fputc(scancodeNorth, fp);
    fputc(scancodeSouth, fp);
    fputc(scancodeWest, fp);
    fputc(scancodeEast, fp);
    fputc(scancodeJump, fp);
    fputc(scancodeBomb, fp);
    fputc(isMusicEnabled, fp);
    fputc(isSoundEnabled, fp);

    for (i = 0; i < 10; i++) {
        fprintf(fp, "%lu", highScoreValues[i]);
        fprintf(fp, " ");
        fprintf(fp, "%s\n", highScoreNames[i]);
    }

    fclose(fp);
}
```

This function is the complement of the [loading code]({{< relref "#load-from-configuration-file" >}}) in {{< lookup/cref LoadConfigurationData >}}. After opening the file for writing with {{< lookup/cref fopen >}}, the six keyboard scancode mappings are written to the file followed by the two music/sound option flags (see the [configuration file format]({{< relref "configuration-file-format#format" >}}) for more on the file structure).

Next the ten high score table entries are written sequentially to the file with multiple calls to {{< lookup/cref fprintf >}}, creating the "score, space, name, newline" format. Writing this data is considerably more straightforward than reading it.

Once the high score table has been fully written, {{< lookup/cref fclose >}} cleans up the file pointer and the function returns.

{{< boilerplate/function-cref JoinPath >}}

The {{< lookup/cref JoinPath >}} function combines a string `dir` with a string `file`, creating and returning an absolute pathname. Typically `dir` will be a directory on disk like "C:\MYDIR" while `file` will have the form "MYFILE.EXT." The final joined path would be "C:\MYDIR\MYFILE.EXT."

This function is used when loading and saving both [configuration files]({{< relref "configuration-file-format" >}}) and [save files]({{< relref "save-file-format" >}}), to combine the filename with the [write path]({{< relref "main-and-outer-loop#write-path" >}}).

```c
char *JoinPath(char *dir, char *file)
{
    int dstoff;
    word srcoff;

    if (*dir == '\0') return file;

    for (dstoff = 0; *(dir + dstoff) != '\0'; dstoff++) {
        *(joinPathBuffer + dstoff) = *(dir + dstoff);
    }

    *(joinPathBuffer + dstoff++) = '\\';

    for (srcoff = 0; *(file + srcoff) != '\0'; srcoff++) {
        *(joinPathBuffer + dstoff++) = *(file + srcoff);
    }

    return joinPathBuffer;
}
```

The first test handles an edge case: If `dir` is an empty string, the path is treated as a relative one, and `file` is returned unmodified.

A `for` loop copies bytes, one at a time, from `dir` into the global {{< lookup/cref joinPathBuffer >}}. The loop ends once the null byte at the end of `dir` is reached.

The `dstoff` variable now indicates the point in {{< lookup/cref joinPathBuffer >}} where the directory copy finished. A single backslash character is placed at that position and `dstoff` is incremented.

Another `for` loop again copies bytes, this time from `file`. The read position starts at the beginning of `file`, but the write position within {{< lookup/cref joinPathBuffer >}} starts after the backshash that was just inserted. As before, copying stops once the null byte in `file` is reached.

There is an insidious bug in this code: The copy from `file` to {{< lookup/cref joinPathBuffer >}} stops at `file`'s null terminator byte, but _it does not copy that terminator into the destination._ This leaves an improperly-terminated string in the destination, which would usually cause obvious misbehavior. The reason it works correctly here is due to a series of happy accidents. {{< lookup/cref joinPathBuffer >}} is in BSS, which is explicitly initialized to zero on startup, and all calls to {{< lookup/cref JoinPath >}} happen to have `dir` and `file` lengths of consistent size. The zero bytes in BSS end up accidentally (but correctly) terminating the string without any ghosts of longer values showing through.

A pointer to {{< lookup/cref joinPathBuffer >}} is returned, which contains the combination of the provided directory and file names.

[^model-f]: https://en.wikipedia.org/wiki/Model_F_keyboard
