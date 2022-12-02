+++
title = "Save File Functions"
description = "Describes functions that are responsible for saving and loading game state from disk."
weight = 260
+++

# Save File Functions

{{< table-of-contents >}}

The [save file format]({{< relref "save-file-format" >}}) of the game is relatively simple, and the functions that save and load games are accordingly straightforward. This simplicity is achieved because of a firm game design decision -- saved games are recorded at the beginning of a level, discarding any progress that has been made since the level started. By designing the save format in this way, the regular map loading and initialization code can accurately recreate the game state without needing to store details about the state of every global variable that could possibly affect the restoration of the game's state.

{{< boilerplate/function-cref LoadGameState >}}

The {{< lookup/cref LoadGameState >}} function reads the current state of the most important player variables from a file on disk, whose filename extension is influenced by the character provided in `slot_char`. If the file cannot be loaded, returns false. If the file's internal anti-tampering checksum does not match, an error message is displayed and the program exits. Otherwise, returns true.

Each save game slot is identified by a single-character `slot_char` byte, which could in principle be any character supported in a DOS "8.3" style file name. The MS-DOS 6 User's Guide says this about files and directory names:

> * Can be up to eight characters long. In addition, you can include an extension up to three characters long.
> * Are not case-sensitive. It does not matter whether you use uppercase or lowercase letters when you type them.
> * Can contain only the letters A through Z, the numbers 0 through 9, and the following special characters: underscore (\_), caret (^), dollar sign ($), tilde (~), exclamation point (!), number sign (#), percent sign (%), ampersand (&), hyphen (-), braces ({}), at sign (@), single quotation mark (\`), apostrophe ('), and parentheses (). No other special characters are acceptable.
> * Cannot contain spaces, commas, backslashes, or periods (except the period that separates the name from the extension).
> * Cannot be identical to the name of another file or subdirectory in the same directory.
>
> -- https://archive.org/details/microsoft-ms-dos-6/page/n25/mode/2up

In practice, the game uses digit characters `1` through `9` and the letter `T` as `slot_char` values.

```c
bbool LoadGameState(char slot_char)
{
    static char *filename = FILENAME_BASE ".SV ";
    FILE *fp;
    word checksum;

    *(filename + SAVE_SLOT_INDEX) = slot_char;
```

{{< lookup/cref FILENAME_BASE >}} is a constant based on the episode of the game being played, and holds a value like `"COSMO1"`. {{< lookup/cref SAVE_SLOT_INDEX >}} is a numeric index into the local `filename` string, and points to the location in that string where the `slot_char` should be placed. These two constants, combined with `slot_char`, produce the final filename that will be opened.

In a hypothetical example where `slot_char` was `'7'`, {{< lookup/cref FILENAME_BASE >}} was `"COSMO2"`, and {{< lookup/cref SAVE_SLOT_INDEX >}} was `9`, the initial value for `filename` would become `"COSMO2.SV "` -- note the trailing space. The ninth element of that string would be overwritten with `slot_char`, producing a final `filename` of `"COSMO2.SV7"`.

```c
    fp = fopen(JoinPath(writePath, filename), "rb");
    if (fp == NULL) {
        fclose(fp);

        return false;
    }
```

{{< lookup/cref JoinPath >}} combines the relative `filename` with the {{< lookup/cref writePath >}} from when the program started. In common use, {{< lookup/cref writePath >}} is an empty string and the resulting filename remains relative. This filename is passed to {{< lookup/cref fopen >}} which tries to open the file for reading in binary mode (`"rb"`). The file pointer is returned in `fp`.

If the file could not be opened (most likely because a save file with the specified `slot_char` does not exist), `fp` will hold a `NULL` value and loading cannot proceed. The `if` body responds to this by {{< lookup/cref fclose >}}ing the known-`NULL` pointer (which is an entirely meaningless and unsafe operation) and returning `false` to the caller. 

```c
    playerHealth = getw(fp);
    fread(&gameScore, 4, 1, fp);
    gameStars = getw(fp);
    levelNum = getw(fp);
    playerBombs = getw(fp);
    playerHealthCells = getw(fp);
    usedCheatCode = getw(fp);
    sawBombHint = getw(fp);
    pounceHintState = getw(fp);
    sawHealthHint = getw(fp);
```

Otherwise, `fp` holds a readable file and we can proceed with populating the global variables with the values read from the file.

The [save file format]({{< relref "save-file-format" >}}) defines the size and ordering of the fields here, which are (with one exception) 16-bit words stored in the CPU's native byte order. The {{< lookup/cref getw >}} library function reads such a word, and advances the read position in `fp` by two bytes to prepare for the next read. {{< lookup/cref fread >}} does a similar task, but using a configurable read size -- here reading one four-byte value into {{< lookup/cref gameScore >}}.

From `fp`, values are read into the global {{< lookup/cref playerHealth >}}, {{< lookup/cref gameScore >}}, {{< lookup/cref gameStars >}}, {{< lookup/cref levelNum >}}, {{< lookup/cref playerBombs >}}, {{< lookup/cref playerHealthCells >}}, {{< lookup/cref usedCheatCode >}}, {{< lookup/cref sawBombHint >}}, {{< lookup/cref pounceHintState >}}, and {{< lookup/cref sawHealthHint >}} variables.

```c
    checksum = playerHealth + (word)gameStars + levelNum + playerBombs +
        playerHealthCells;

    if (getw(fp) != checksum) {
        ShowAlteredFileError();
        ExitClean();
    }

    fclose(fp);

    return true;
}
```

The file concludes with a `checksum` word, which is the 16-bit sum of the player's health, available health cells, bombs, stars, and the current level number. If the last word in the save file, read via {{< lookup/cref getw >}}, does not match this `checksum`, the save file has been tampered with.

The game chooses to handle this condition sternly, by showing an error message ({{< lookup/cref ShowAlteredFileError >}}) followed by an unconditional exit to DOS with {{< lookup/cref ExitClean >}}.

If the checksum check succeeded, clean up `fp` with a call to {{< lookup/cref fclose >}} and return `true` to the caller to indicate that the load has completed successfully.

{{< boilerplate/function-cref SaveGameState >}}

The {{< lookup/cref SaveGameState >}} function writes the current state of the most important player variables to a file on disk, whose filename extension is influenced by the character provided in `slot_char`.

```c
void SaveGameState(char slot_char)
{
    static char *filename = FILENAME_BASE ".SV ";
    FILE *fp;
    word checksum;

    *(filename + SAVE_SLOT_INDEX) = slot_char;

    fp = fopen(JoinPath(writePath, filename), "wb");
```

The file name generation here works identically to {{< lookup/cref LoadGameState >}}. `slot_char` is injected into a file name template to produce a file pointer in `fp`.

```c
    putw(playerHealth, fp);
    fwrite(&gameScore, 4, 1, fp);
    putw((word)gameStars, fp);
    putw(levelNum, fp);
    putw(playerBombs, fp);
    putw(playerHealthCells, fp);
    putw(usedCheatCode, fp);
    putw(true, fp);  /* bomb hint */
    putw(POUNCE_HINT_SEEN, fp);
    putw(true, fp);  /* health hint */
```

This sequence of calls serializes the current game state into the [save file format]({{< relref "save-file-format" >}}). Most variables are 16-bit and written to `fp` with {{< lookup/cref putw >}}. {{< lookup/cref gameScore >}} is 32 bits wide, and instead uses {{< lookup/cref fwrite >}} to store a single four-byte value in `fp`.

Values are stored from {{< lookup/cref playerHealth >}}, {{< lookup/cref gameScore >}}, {{< lookup/cref gameStars >}}, {{< lookup/cref levelNum >}}, {{< lookup/cref playerBombs >}}, {{< lookup/cref playerHealthCells >}}, and {{< lookup/cref usedCheatCode >}}. Following these, the three hint variables (bomb, pounce, and power-up) are unconditionally written as their "seen" state -- _not_ the values currently held in memory. As a result of this decision, any subsequent {{< lookup/cref LoadGameState >}} call will load a state where these hints will not show, even if the player has not actually seen them yet.

{{< aside class="speculation" >}}
**Get a load of Mr. Know It All here...**

Perhaps the thinking was, if the user knows enough to be saving/loading the game before seeing these hints, they probably have played the game before and have seen how the essential mechanics work already.
{{< /aside >}}

```c
    checksum = playerHealth + (word)gameStars + levelNum + playerBombs +
        playerHealthCells;
    putw(checksum, fp);

    fclose(fp);
}
```

The last field written into the file is the `checksum`. This is the 16-bit sum of the player's health, available health cells, bombs, stars, and the current level number. This is written to `fp` with {{< lookup/cref putw >}}, then the file pointer is closed with {{< lookup/cref fclose >}}.

The checksum is used by {{< lookup/cref LoadGameState >}} as a simple check to verify that the content of the save file has not been manipulated by the user in an attempt to cheat.
