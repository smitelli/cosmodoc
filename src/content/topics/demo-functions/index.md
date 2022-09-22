+++
title = "Demo File Functions"
description = "Describes the functions that read, write, and interpret the demo data."
weight = 240
+++

# Demo File Functions

{{< table-of-contents >}}

The **demo data** is a stream of bytes that represent the state of the keyboard during each frame of a gameplay session. This data can then be replayed, simulating keypresses in lieu of actually reading the hardware, to play the game automatically.

[Demo data]({{< relref "demo-format" >}}) is stored in a file named PREVDEMO.MNI. Each episode ships with a factory-default demo inside the VOL [group file]({{< relref "group-file-format" >}}), but user demos can also be recorded and saved to disk. By removing the factory demo, user demos could be played back in their place.

The principal demo functions consist of {{< lookup/cref LoadDemoData >}}/{{< lookup/cref SaveDemoData >}} (which are responsible for moving data from the disk to memory and back) and {{< lookup/cref ReadDemoFrame >}}/{{< lookup/cref WriteDemoFrame >}} (which translate between the in-memory demo format and a sequence of keyboard states).

{{< boilerplate/function-cref LoadDemoData >}}

The {{< lookup/cref LoadDemoData >}} function copies the data from the PREVDEMO.MNI [group file]({{< relref "group-file-format" >}}) entry into system memory. It is called immediately before the game loop starts, but only if the game is in demo playback mode.

```c
void LoadDemoData(void)
{
    FILE *fp = GroupEntryFp("PREVDEMO.MNI");
    miscDataContents = IMAGE_DEMO;

    if (fp == NULL) {
        demoDataLength = 0;
        demoDataPos = 0;
    } else {
        demoDataLength = getw(fp);
        fread(miscData, demoDataLength, 1, fp);
    }

    fclose(fp);
}
```

The function begins with a call to {{< lookup/cref GroupEntryFp >}} to create a file stream pointer to PREVDEMO.MNI. {{< lookup/cref miscDataContents >}} is then set to {{< lookup/cref name="IMAGE" text="IMAGE_DEMO" >}} as a status flag -- this serves as an indicator that {{< lookup/cref miscData >}} is being rewritten with demo data.

Next is a null pointer check. If `fp` is null, the demo file did not exist. Set both {{< lookup/cref demoDataLength >}} and {{< lookup/cref demoDataPos >}} to zero in response. These would actually already be zero from an earlier call to {{< lookup/cref InitializeGame >}}, but it's explicitly restated here.

Otherwise, `fp` was opened successfully and the data can be read. The first 16-bit word in the [demo data contents]({{< relref "demo-format#file-contents" >}}) is the length of the data, in bytes. Read that into {{< lookup/cref demoDataLength >}}. Next an {{< lookup/cref fread >}} is issued to read that much data into the {{< lookup/cref miscData >}} memory block.

Finally, {{< lookup/cref fclose >}} cleans up the file pointer. Note that it's entirely possible for `fp` to be null here, and `fclose(NULL)` is undefined behavior, so, uh... try not to let that situation occur, I guess.

{{< boilerplate/function-cref SaveDemoData >}}

The {{< lookup/cref SaveDemoData >}} function flushes all of the in-memory demo data to the PREVDEMO.MNI file _on disk_ -- it does not modify any [group file]({{< relref "group-file-format" >}}) contents. This is the complement of the {{< lookup/cref LoadDemoData >}} function.

This function is called at the conclusion of a gameplay session where demo data was being captured. The demo data is held in the {{< lookup/cref miscData >}} memory block, and has a length of {{< lookup/cref demoDataLength >}}.

```c
void SaveDemoData(void)
{
    FILE *fp = fopen("PREVDEMO.MNI", "wb");
    miscDataContents = IMAGE_DEMO;

    putw(demoDataLength, fp);
    fwrite(miscData, demoDataLength, 1, fp);

    fclose(fp);
}
```

The function starts with a call to {{< lookup/cref fopen >}} the PREVDEMO.MNI file. This does **not** consider the [write path]({{< relref "main-and-outer-loop#write-path" >}}), so the file will always be created in the current working directory. This also does not check the return value of {{< lookup/cref fopen >}}, so it is possible for bad things to happen if the current working directory is not writable or some other failure occurs.

{{< lookup/cref miscDataContents >}} is then set to {{< lookup/cref name="IMAGE" text="IMAGE_DEMO" >}} -- this is arguably not the best place to be doing that; it should probably have been set while {{< lookup/cref miscData >}} was being written and then _checked_ here as a guard.

The [demo data contents]({{< relref "demo-format#file-contents" >}}) are written next -- a call to {{< lookup/cref putw >}} to write the 16-bit length header, followed by an {{< lookup/cref fwrite >}} to flush the demo data held in the {{< lookup/cref miscData >}} block to disk.

{{< lookup/cref fclose >}} cleans up the file pointer, and the function returns.

{{< boilerplate/function-cref ReadDemoFrame >}}

The {{< lookup/cref ReadDemoFrame >}} function reads the next byte from the [demo data]({{< relref "demo-format" >}}) and updates the global input command state. If a demo is being played back, the keyboard handler calls this function during each frame of gameplay in lieu of reading from the keyboard hardware.

If this function returns true, the end of the demo has been reached and the caller must prepare to stop gameplay mode.

```c
bbool ReadDemoFrame(void)
{
    cmdWest  = (bbool)(*(miscData + demoDataPos) & 0x01);
    cmdEast  = (bbool)(*(miscData + demoDataPos) & 0x02);
    cmdNorth = (bbool)(*(miscData + demoDataPos) & 0x04);
    cmdSouth = (bbool)(*(miscData + demoDataPos) & 0x08);
    cmdJump  = (bbool)(*(miscData + demoDataPos) & 0x10);
    cmdBomb  = (bbool)(*(miscData + demoDataPos) & 0x20);
    winLevel =  (bool)(*(miscData + demoDataPos) & 0x40);

    demoDataPos++;
    if (demoDataPos > demoDataLength) return true;

    return false;
}
```

The [demo data contents]({{< relref "demo-format#file-contents" >}}) use a sequence of bytes to represent keyboard input over time. Each byte of the data represents a frame of gameplay, and the low six bits in each byte represent the pressed/unpressed state of each of the six input keys. Each bit is isolated using a mask, and stored in its corresponding input command variable.

The bit in position 6 is written to the {{< lookup/cref winLevel >}} variable, permitting demo playback to advance to the next level at any arbitrary point. This function runs early enough in each iteration of the game loop that this assignment does not interfere with the functionality of any of the usual level exits, which can be used to advance the demo levels if desired.

Once the input has been parsed, the read position indicated by {{< lookup/cref demoDataPos >}} is advanced. If the position overruns the end of the data as measured by {{< lookup/cref demoDataLength >}}, return true to indicate to the caller the demo mode must end.

Otherwise, return false to let the caller know that gameplay may continue.

{{< boilerplate/function-cref WriteDemoFrame >}}

The {{< lookup/cref WriteDemoFrame >}} function captures a snapshot of the global input command state (from the keyboard or joystick) and encodes it into a stream of [demo data]({{< relref "demo-format" >}}) bytes. If a demo is being recorded, the keyboard handler calls this function during each frame of gameplay after interpreting the user's input commands.

Normally this function returns false, indicating that the demo is being recorded correctly. If the demo runs long and runs out of storage space in memory, this function returns true to inform the caller that it must stop gameplay.

```c
bbool WriteDemoFrame(void)
{
    if (demoDataLength > 4998) return true;

    winLevel = isKeyDown[SCANCODE_X];

    *(miscData + demoDataPos) = cmdWest | (cmdEast  << 1) |
        (cmdNorth << 2) | (cmdSouth << 3) |
        (cmdJump  << 4) | (cmdBomb  << 5) | (winLevel << 6);

    demoDataPos++;
    demoDataLength++;

    return false;
}
```

The function starts with a check that the offset of the demo data captured so far (tracked in {{< lookup/cref demoDataLength >}}) is 4,998 bytes or less. This results in a maximum allowable demo data size of _4,999_ bytes. Once the data reaches this size, the function returns true to indicate to the caller that it must stop the game -- no more demo data can be stored.

Otherwise, the function proceeds. The base state of the global {{< lookup/cref winLevel >}} is set to match the state of the <kbd>X</kbd> key on the keyboard. If the user presses this key, the level unconditionally ends and the next level in the progression starts. This function runs early enough in each iteration of the game loop that this assignment does not interfere with the functionality of any of the usual level exits, which can be used to advance the demo levels if desired.

The state of the six global input command variables is packed into a byte, with each bit position mapped to a specific input as defined by the [demo data format]({{< relref "demo-format#file-contents" >}}). The {{< lookup/cref winLevel >}} flag is also packed into the bit in position 6. The resulting demo data byte is written to the {{< lookup/cref miscData >}} data block at the position indicated by {{< lookup/cref demoDataPos >}}.

Finally, {{< lookup/cref demoDataPos >}} and {{< lookup/cref demoDataLength >}} are incremented in tandem, preparing this function for its upcoming call during the next frame. A false value is returned, informing the caller that it may proceed with gameplay.
