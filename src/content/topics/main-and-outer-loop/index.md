+++
title = "main() and Outer Loop"
description = "An exploration of the outermost main functions of the game."
weight = 200
+++

# `main()` and Outer Loop

{{< table-of-contents >}}

The first programmer-defined function that runs in any C program is named {{< lookup/cref main >}}. It is called by the C runtime and takes two parameters: `argc` (the number of command-line arguments the program was run with) and `argv` (the values of each of these arguments).

This is where everything begins.

{{< boilerplate/function-cref main >}}

Cosmo's Cosmic Adventure requires an 80286 processor due to the way it was compiled (and because it moves an objectively large amount of graphics data with every frame it draws). First and foremost, the CPU needs to be tested to ensure it meets this requirement, with a graceful fallback message if the system is not powerful enough. The {{< lookup/cref main >}} function is responsible for this check, and it is small enough to speak for itself:

```c
void main(int argc, char *argv[])
{
    int cputype = GetProcessorType();

    if (cputype < CPUTYPE_80188) {
        byte response;

        /* Grammatical errors preserved faithfully */
        printf("You're computer appears to be an 8088/8086 XT system.\n\n");
        printf("Cosmo REQUIRES an AT class (80286) or better to run due "
            "to\n");
        printf("it's high-speed animated graphics.\n\n");
        printf("Note:  This game will crash on XT systems.\n");
        printf("Do you wish to continue if you really have an AT system or "
            "better (Y/N)?");

        response = getch();
        if (response == 'Y' || response == 'y') {
            InnerMain(argc, argv);
        }

        exit(EXIT_SUCCESS);
    } else {
        InnerMain(argc, argv);
    }
}
```

{{< lookup/cref main >}} does not share its compilation unit with any other functions -- this is basically all that is present in the file. This is the only C function in the game that is compiled in 8086/88 compatibility mode, and for good reason: If the user runs the program on an original IBM PC or XT with the 8088 processor, a 286-optimized main function would not execute correctly and the prompt would never show.

The actual CPU detection routine in {{< lookup/cref GetProcessorType >}} and its return values are covered in detail [elsewhere]({{< relref "processor-detection" >}}).

The happy path through this function is that the user has a 286 (technically, anything equal to or better than a {{< lookup/cref name="CPUTYPE" text="CPUTYPE_80188" >}}). In this case, execution is passed to {{< lookup/cref InnerMain >}} along with the values for `argc` and `argv`.

If the user appears to have a processor that is incapable of running the game (an 8086/88 or an NEC V20/30), a text warning and prompt are displayed via {{< lookup/cref printf >}}. {{< lookup/cref getch >}} reads the user's response to the prompt without echoing it to the screen. If the user enters <kbd>Y</kbd> or <kbd>y</kbd>, it attempts to call {{< lookup/cref InnerMain >}} as above. Otherwise {{< lookup/cref exit >}} is called to return to DOS with an {{< lookup/cref EXIT_SUCCESS >}} status code.

{{< lookup/cref InnerMain >}} never returns, so control never comes back here.

{{< boilerplate/function-cref InnerMain >}}

The {{< lookup/cref InnerMain >}} function accepts the same arguments as {{< lookup/cref main >}} and receives the same values in each. The function parses the command line arguments first:

```c
void InnerMain(int argc, char *argv[])
{
    if (argc == 2) {
        writePath = argv[1];
    } else {
        writePath = "\0";
    }
```

If there was exactly one command-line argument provided (`argc == 2`),[^argc] that argument is used as the [write path]({{< relref "#write-path" >}}). Otherwise the {{< lookup/cref writePath >}} is empty, which means "use the current working directory."

The startup function is called next:

```c
    Startup();
```

{{< lookup/cref Startup >}} performs quite a bit of hardware detection, memory allocation and file loading. Once initialization is complete, the [outer loop]({{< relref "#outer-loop" >}}) is entered.

{{< aside class="speculation" >}}
**How'd it get two {{< lookup/cref main >}}s?**

At one point, {{< lookup/cref InnerMain >}} was probably the actual main function. Once it was determined that the game would require a 286 to run, it was probably more straightforward to do the CPU detection in a separate outer function that wrapped the old main function than to try to refactor the existing code to work on an 8088.
{{< /aside >}}

### Write Path

Most users run the game by typing `COSMOx` at the DOS prompt without providing any arguments. This is not the only way.

{{< lookup/cref InnerMain >}} supports exactly one optional command line argument. This is interpreted as either an absolute or relative directory name, and the value is used as the game's **write path**. If unspecified (i.e. there were no additional command line arguments, or too many of them) the write path defaults to the current working directory. (Under DOS, this is the directory the user `CD`'d into before running the game.) Some example invocations:

* `COSMO1 C:\MYDIR`: Uses C:\MYDIR as the write path.
* `COSMO1 SUBDIR`: Uses the directory SUBDIR inside of the current working directory.
* `COSMO1 DEEPER\SUBDIR`: Uses the directory SUBDIR inside of the directory DEEPER inside of the current working directory.
* `COSMO1`: Uses the current working directory (default, since there was not an argument provided).
* `COSMO1 EXAMPLE DOESNOTWORK`: Uses the current working directory (default, since there were too many arguments provided).

In all cases, these are the files written to the write path:

* [Configuration file]({{< relref "configuration-file-format" >}}) (COSMOx.CFG)
* [Save files]({{< relref "save-file-format" >}}) (COSMOx.SV?)

It appears as though the intent of this feature was to provide a way for the user to play the game from a read-only working directory, but still save data in a different location that is writable. This would allow the game to be run directly from a read-only "game disk" with save files stored separately on the hard drive or a secondary "save disk." (The game is far too large to fit on a single 1,440 KiB floppy disk, but who knows exactly which formats the creators may have had in mind.)

For this to work as intended, the specified directory must exist and be writable -- no attempt is made to create the directory or verify its usability. If an invalid or unwritable path is provided, any attempts to load or save these files will fail -- in many cases silently. This produces [odd behavior that some have interpreted as a special cheat mode]({{< relref "apogee-parameter" >}}).

### Outer Loop

{{< lookup/cref InnerMain >}} continues with the outer loop of the game, which has no termination condition. The only way out of it is to use the {{< lookup/cref ExitClean >}} function (which ultimately asks DOS to terminate execution of the program).

```c
    for (;;) {
        demoState = TitleLoop();
```

{{< lookup/cref TitleLoop >}} handles showing the title screen graphics, main menu, and most of the sub-menus contained within. {{< lookup/cref TitleLoop >}} doesn't return until the point where gameplay needs to start -- either under direct player control or by playing back a previously recorded demo. {{< lookup/cref demoState >}} is a global variable to track this state. {{< lookup/cref TitleLoop >}} also performs _some_ initialization of game state -- the most relevant effect is initializing {{< lookup/cref levelNum >}} to 0.

```c
        InitializeLevel(levelNum);
        LoadMaskedTileData("MASKTILE.MNI");

        if (demoState == DEMOSTATE_PLAY) {
            LoadDemoData();
        }
```

{{< lookup/cref InitializeLevel >}} handles loading and setup of the global variables needed to play the level specified by {{< lookup/cref levelNum >}}.

The call to {{< lookup/cref LoadMaskedTileData >}} is interesting. All it does is load the contents of the map's [masked tile image data]({{< relref "tile-image-format#masked-tiles" >}}) into memory. The reason why this needs to happen here is because its memory block (pointed to by {{< lookup/cref maskedTileData >}}) is _also_ used to hold the AdLib music that plays during the title loop and main menu. When the program switches between the main menu and gameplay mode, this memory must be rewritten with the data required for that context.

If {{< lookup/cref demoState >}} indicates a demo is being played back, {{< lookup/cref LoadDemoData >}} is called to read the [demo data]({{< relref "demo-format" >}}) into memory and initialize playback variables.

```c
        isInGame = true;
        GameLoop(demoState);
        isInGame = false;
```

Next comes {{< lookup/cref GameLoop >}}, framed by a toggle of the {{< lookup/cref isInGame >}} flag. This function does not return until the player wins the game or quits, or until the demo ends if running in that mode.

```c
        StopMusic();

        if (demoState != DEMOSTATE_PLAY && demoState != DEMOSTATE_RECORD) {
            CheckHighScoreAndShow();
        }

        if (demoState == DEMOSTATE_RECORD) {
            SaveDemoData();
        }
    }
}
```

At this point, gameplay has stopped and we are handling the transition back into the title loop and main menu.

{{< lookup/cref StopMusic >}} ensures that there is no music or "ringing" notes still playing.

If {{< lookup/cref demoState >}} indicates no demo is being played back or recorded, {{< lookup/cref CheckHighScoreAndShow >}} is called to see if the player's score qualifies for entry into the high score table. This also displays the high score table before returning.

Finally, if a demo _is_ being recorded, {{< lookup/cref SaveDemoData >}} is called to flush the recorded [demo data]({{< relref "demo-format" >}}) to disk.

The loop then repeats with the title screen. The infinite nature of this outer loop is plainly visible within the program: From the main menu, start a new game... Play for a bit... Quit... Enter your name into the high score table... Return to the main menu. This cycle can be repeated ad nauseam. In order to truly quit back to the DOS prompt, something within the loop must ultimately call {{< lookup/cref exit >}} to request program termination from the DOS API -- there is no other provision to break out of the outer loop.

[^argc]: Yup, `argc` is 2 when there is one command line argument provided. The argument list always contains at least one element; `argv[0]` is the name of the program that was invoked, in this case something like `C:\PATH\TO\COSMOx.EXE`.
