+++
title = "Group File Functions"
description = "Describes the functions that read data from the game's .STN and .VOL files."
weight = 230
+++

# Group File Functions

{{< table-of-contents >}}

All of the data assets for the game are stored in two **[group files]({{< relref "group-file-format" >}})** named COSMOx.STN and COSMOx.VOL. The STN file holds all of the data that is common to all three episodes of the game while the VOL holds the elements that are specific to an episode. Both of the files use the same internal data format.

Each group file contains multiple **entries**, which are named blocks of data with varying lengths. The game loads each entry as a unit directly into memory, either when the game first starts ({{< lookup/cref Startup >}}) or when the level changes ({{< lookup/cref InitializeLevel >}}).

The functions described here handle the loading of generic data from the group files. A few entry-specific functions are also documented here; these functions typically follow the generic loading patterns but contain one-off behaviors that are specific to the entry they operate on.

{{< boilerplate/function-cref GroupEntryFp >}}

The {{< lookup/cref GroupEntryFp >}} function returns a file stream pointer to the data that a [group file's]({{< relref "group-file-format" >}}) `entry_name` refers to. The entry data could be in the STN or VOL file, or it could also be a standalone file in the current working directory. The value in {{< lookup/cref lastGroupEntryLength >}} is updated with the size of the entry data.

The entries in the group file are indexed by all-uppercase names, so an uppercase copy of `entry_name` must be made first:

```c
FILE *GroupEntryFp(char *entry_name)
{
    char header[1000];
    char name[20];
    FILE *fp;
    dword offset;
    int i;
    bool found;

    /* Make an uppercased copy of `entry_name`, saved in `name` */
    for (i = 0; i < 19; i++) {
        name[i] = *(entry_name + i);
    }
    name[19] = '\0';
    strupr(name);
```

This code is not exactly great. Group file entries are indexed by a [**header** structure]({{< relref "group-file-format#header" >}}) that uses 12 bytes for the entry name. These names use the DOS "eight dot three" file naming convention, although this is not a requirement of the group file format. Even though an entry name cannot be more than 12 bytes long, This code copies 19 bytes from `entry_name` into `name`. The actual end of `entry_name`, indicated by a null terminator byte, is completely disregarded -- 19 bytes are copied unconditionally, which always causes a read out of bounds and the inclusion of unrelated memory data.

As a "safety" measure, the final byte of `name` is set to a null terminator. This would protect things in the case where `entry_name` was _longer_ than 19 bytes, which never happens. The actual `entry_name` is always shorter than 19 bytes, and already contains a null terminator, so now the string contains "entry name, null byte, garbage data, null byte." This ends up working correctly because all the functions that operate on `name` stop reading once they reach the first null terminator byte. The garbage data doesn't faze them.

The {{< lookup/cref strupr >}} call changes any `a-z` characters to `A-Z` without changing anything else.

With a usable entry name in hand, the first place to search for the data is within the STN file:

```c
    fp = fopen(stnGroupFilename, "rb");
    found = false;
    fread(header, 1, 960, fp);

    for (i = 0; i < 980; i += 20) {
        if (header[i] == '\0') break;  /* no more entries */

        if (strncmp(header + i, name, 11) == 0) {
            offset = i + 12;
            found = true;
        }
    }
```

Take note of this code; you'll see it again. The file named by {{< lookup/cref stnGroupFilename >}}, which takes the form COSMOx.STN, is {{< lookup/cref fopen >}}'d and the first 960 bytes of the file are copied via {{< lookup/cref fread >}} into the `header` buffer. `found` is a boolean flag that starts false, but flips to true if the desired entry is found.

All searching is done via the `header` buffer, which now contains a repeating sequence of 20-byte entries. Due to the fact that _960_ bytes of header data has been read, only the first (960 &frasl; 20) 48 entries can be searched from this file. The `for` loop iterates over over _49_ header entries, meaning that the last iteration, should it ever get that far, would operate on garbage data from the stack.

The entry name is at offset 0 in each header entry. If the first byte of a header entry name is null, the end of the header has been reached and the loop needs to stop. Otherwise {{< lookup/cref strncmp >}} is employed to compare the first _11_ bytes of the header entry name with the value being searched for. Since the comparison is only checking 11 bytes on a 12-byte field, the last character on a name like "LONGNAME.MNI" will not be considered.

{{% note %}}The sequence of [header entries]({{< relref "group-file-format#header" >}}) in the group file is terminated with an ASCII digit sequence (e.g. "21") in the name field immediately following the last valid entry. The check for a null header entry name will not match this, meaning it is possible to "find" a phantom group entry named "21" with an undefined offset/length in the file.{{% /note %}}

If the header entry name matches the desired value, {{< lookup/cref strncmp >}} returns zero and the `offset` variable is updated to point to the first byte of the offset field in the matching header entry, then `found` is set true. Otherwise the loop continues.

Once the loop stops, either by finding a value or exhausting the available header entries, the search moves on.

```c
    if (!found) {
        fclose(fp);

        fp = fopen(volGroupFilename, "rb");
        fread(header, 1, 960, fp);

        for (i = 0; i < 980; i += 20) {
            if (header[i] == '\0') break;  /* no more entries */

            if (strncmp(header + i, name, 11) == 0) {
                offset = i + 12;
                found = true;
            }
        }
```

If `found` is false, the STN file did not contain the desired entry. {{< lookup/cref fclose >}} the STN file stream, and repeat the same exact steps using the file named by {{< lookup/cref volGroupFilename >}}: COSMOx.VOL.

```c
        if (!found) {
            fclose(fp);

            fp = fopen(entry_name, "rb");
            i = fileno(fp);
            lastGroupEntryLength = filelength(i);

            return fp;
        }  /* if (!found), VOL file*/
    }  /* if (!found), STN file*/
```

If the entry _still_ was not found, neither the STN nor the VOL file contained a candidate. {{< lookup/cref fclose >}} the VOL file stream. As a last-ditch effort (and perhaps as a development aid while the game was being actively worked on), check the current working directory for a normal file with that name.

This code makes a pretty strong assumption that, if this point is reached, the file is going to exist on disk. {{< lookup/cref fopen >}} could very well return a null pointer if the file was not present, which is a condition that's never tested for.

{{< lookup/cref fileno >}} and {{< lookup/cref filelength >}} are used in tandem to get the size of the file for storage in {{< lookup/cref lastGroupEntryLength >}}.

When a file is opened in this way, the stream pointer is set to the beginning of the file data. This is the state the game expects the pointer to be in, so `fp` is returned directly.

If, on the other hand, `found` was set true from either the STN or VOL files, we end up here:

```c
    /* Here `offset` points to the entry's header data */
    fseek(fp, offset, SEEK_SET);
    fread(&offset, 4, 1, fp);
    fread(&lastGroupEntryLength, 4, 1, fp);

    /* Now `offset` points to the first byte of the entry's data */
    fseek(fp, offset, SEEK_SET);

    return fp;
}  /* GroupEntryFp() */
```

At this point, the value in `offset` is a byte offset (not a pointer!) in the currently-open `fp`. This location is inside of the header entry we need to parse, 12 bytes into the structure. The 4-byte value at this position is the offset at which the actual data starts, and the next 4-byte value is the length of that data.

{{< lookup/cref fseek >}} advances the file pointer to the location of the header offset value, and two successive calls to {{< lookup/cref fread >}} update `offset` with the byte position of the data and set the value in {{< lookup/cref lastGroupEntryLength >}} to its size.

{{< lookup/cref fseek >}} is called once again, this time to update the file stream to point to the first byte of the data. The file stream is returned to the caller in this state, ready to be read from.

{{< boilerplate/function-cref GroupEntryLength >}}

The {{< lookup/cref GroupEntryLength >}} function locates a [group file]({{< relref "group-file-format" >}}) `entry_name` and returns the size of its data in bytes.

```c
dword GroupEntryLength(char *entry_name)
{
    fclose(GroupEntryFp(entry_name));

    return lastGroupEntryLength;
}
```

This opens a file stream via {{< lookup/cref GroupEntryFp >}}, then immediately closes it with {{< lookup/cref fclose >}}. This seemingly pointless action actually has an important side-effect: As {{< lookup/cref GroupEntryFp >}} locates the data and sets up the file pointer, it also updates the value in the global {{< lookup/cref lastGroupEntryLength >}} variable to contain the size of the data that was found.

This function returns the value held in the freshly-updated {{< lookup/cref lastGroupEntryLength >}} variable.

{{< boilerplate/function-cref LoadGroupEntryData >}}

The {{< lookup/cref LoadGroupEntryData >}} function is a general-purpose utility that reads data from an `entry_name` inside a [group file]({{< relref "group-file-format" >}}) and stores it in the memory block pointed to by `dest`. Like many such functions in C, a `length` argument is required to control how much data is copied.

```c
void LoadGroupEntryData(char *entry_name, byte *dest, word length)
{
    FILE *fp = GroupEntryFp(entry_name);

    fread(dest, length, 1, fp);
    fclose(fp);
}
```

The implementation is straightforward. {{< lookup/cref GroupEntryFp >}} opens and returns a stream pointing at the file data that `entry_name` refers to. {{< lookup/cref fread >}} copies `length` bytes from the file to `dest`, and {{< lookup/cref fclose >}} closes the stream.

{{% aside class="speculation" %}}
**Making more work for ourselves**

This function relies on the caller to provide `length` instead of leveraging {{< lookup/cref GroupEntryLength >}} or {{< lookup/cref lastGroupEntryLength >}} to dynamically determine the size of the data. This suggests that maybe the length calculation functions were a late addition to the code.
{{% /aside %}}

Despite the general usefulness of this function, it is not used in as many places as it could have been. Several load functions instead opt to duplicate the behavior shown here.

{{< boilerplate/function-cref LoadInfoData >}}

{{< lookup/cref LoadInfoData >}} is almost a carbon-copy of {{< lookup/cref LoadGroupEntryData >}}. In fact, the only difference between the two is in the parameter list -- this function takes a word pointer for `dest`, while {{< lookup/cref LoadGroupEntryData >}} takes a byte pointer. This avoids a cast operation in the calling code, at the expense of brevity.

```c
void LoadInfoData(char *entry_name, word *dest, word length)
{
    FILE *fp = GroupEntryFp(entry_name);

    fread(dest, length, 1, fp);
    fclose(fp);
}
```

This function is used to load word-aligned [tile info data]({{< relref "tile-info-format" >}}) stored in *INFO.MNI entries.

{{< boilerplate/function-cref LoadActorTileData >}}

The {{< lookup/cref LoadActorTileData >}} function reads data from the provided `entry_name` and fills the {{< lookup/cref actorTileData >}} memory blocks. `entry_name` is always `ACTORS.MNI`, and this function is hard-coded with some strong assumptions about the file's name and size -- it will not behave correctly on any other file.

```c
void LoadActorTileData(char *entry_name)
{
    FILE *fp = GroupEntryFp(entry_name);

    fread(actorTileData[0], WORD_MAX, 1, fp);
    fread(actorTileData[1], WORD_MAX, 1, fp);
    /* Could've/should've used `entry_name` instead of hard-coding ACTORS */
    fread(actorTileData[2], (word)GroupEntryLength("ACTORS.MNI") + 2, 1, fp);
    fclose(fp);
}
```

{{< lookup/cref GroupEntryFp >}} opens a stream pointing at the beginning of the [group file data]({{< relref "group-file-format" >}}) for ACTORS.MNI.

The first two {{< lookup/cref actorTileData >}} array elements point to large blocks of memory -- each is 65,535 bytes, the largest allocation that {{< lookup/cref malloc >}} can provide. The first two {{< lookup/cref fread >}} calls fill them both with as much data as they will hold.

The third {{< lookup/cref fread >}} reads the remainder of the data into {{< lookup/cref name="actorTileData" text="actorTileData[2]" >}}. This block is not as large as the first two, so the length of the read is some amount less than 65,535 bytes. Similarly to how it was handled in {{< lookup/cref Startup >}}, the remainder is calculated by truncating the doubleword size of the file data to 16 bits, then adding 2 to correct for the off-by-one error introduced when reading each previous full block. (Truncation to 16 bits is akin to taking the value modulo 65,536 while the previous reads were each 65,535 bytes.)

The file stream is closed with {{< lookup/cref fclose >}}, and the function returns.

To be crystal clear, the only reason this function works correctly is because it is always called with `ACTORS.MNI` as its argument, and because this file contains between (65,536 &times; 2) 131,072 and (65,535 &times; 3) 196,605 bytes of data.

{{< boilerplate/function-cref LoadCartoonData >}}

The {{< lookup/cref LoadCartoonData >}} function is designed to load the [masked tile image data]({{< relref "tile-image-format#masked-tiles" >}}) from the CARTOON.MNI [group file]({{< relref "group-file-format" >}}) entry. It generally mirrors the behavior of {{< lookup/cref LoadGroupEntryData >}}, but hard-codes the destination pointer and dynamically computes the length of the data.

```c
void LoadCartoonData(char *entry_name)
{
    FILE *fp = GroupEntryFp(entry_name);

    fread(mapData.b, (word)GroupEntryLength(entry_name), 1, fp);
    fclose(fp);
}
```

The usage of {{< lookup/cref GroupEntryLength >}} permits the function to dynamically adjust the read size based on the actual size of the file data. The destination pointer here is the byte-aligned member of {{< lookup/cref mapData >}}.

This function is always called outside of gameplay due to the fact that it clobbers the game map memory.

{{< boilerplate/function-cref LoadFontTileData >}}

The {{< lookup/cref LoadFontTileData >}} function is designed to load and fix up the data for the game's font.

```c
void LoadFontTileData(char *entry_name, byte *dest, word length)
{
    int i;
    FILE *fp = GroupEntryFp(entry_name);

    fread(dest, length, 1, fp);
    fclose(fp);

    /* Ideally should be `length`, not a literal 4000. */
    for (i = 0; i < 4000; i += 5) {
        *(dest + i) = ~*(dest + i);
    }
}
```

The function starts with a clone of the code from {{< lookup/cref LoadGroupEntryData >}}. Once the data is loaded and the file stream is closed, the in-memory data is altered.

{{< lookup/cref LoadFontTileData >}} is designed to operate on the FONTS.MNI entry, which is 4,000 bytes long and contains [masked tile image data]({{< relref "tile-image-format#masked-tiles" >}}). Tile image data is stored in a byte-planar format using mask-blue-green-red-intensity order. In this arrangement, offsets 0, 5, 10, 15... all refer to transparency mask bytes.

For whatever reason, the font tiles were constructed with a transparency mask that is inverted relative to every other masked tile in the game. Rather than using a special function to handle this condition at draw time, the mask bits are simply flipped here. The `for` loop iterates through every 5th byte in the entire font and inverts the transparency bits using a bitwise NOT. This normalizes the font mask format in memory.

If not for the literal 4,000 in the code, this could be made into a general-purpose function for almost any masked tile data. The usefulness of such a general-purpose function is pretty much nil.

{{< boilerplate/function-cref LoadMaskedTileData >}}

The {{< lookup/cref LoadMaskedTileData >}} function loads data from the [group file]({{< relref "group-file-format" >}}) entry named `entry_name` and stores it in {{< lookup/cref maskedTileData >}}. The implementation is quite similar to {{< lookup/cref LoadGroupEntryData >}}.

```c
void LoadMaskedTileData(char *entry_name)
{
    FILE *fp = GroupEntryFp(entry_name);

    fread(maskedTileData, 40000U, 1, fp);
    fclose(fp);
}
```

Due to the hard-coded destination and literal length of 40,000 in the {{< lookup/cref fread >}}, this function is only appropriate for loading the MASKTILE.MNI group file entry.

{{< boilerplate/function-cref LoadTileAttributeData >}}

The {{< lookup/cref LoadTileAttributeData >}} function loads data from the [group file]({{< relref "group-file-format" >}}) entry named `entry_name` and stores it in {{< lookup/cref tileAttributeData >}}. The implementation is essentially a modified copy of {{< lookup/cref LoadMaskedTileData >}}.

```c
void LoadTileAttributeData(char *entry_name)
{
    FILE *fp = GroupEntryFp(entry_name);

    fread(tileAttributeData, 7000, 1, fp);
    fclose(fp);
}
```

Due to the hard-coded destination and literal length of 7,000 in the {{< lookup/cref fread >}}, this function is only appropriate for loading the TILEATTR.MNI group file entry.

{{< boilerplate/function-cref LoadSoundData >}}

The {{< lookup/cref LoadSoundData >}} function reads data from the [group file]({{< relref "group-file-format" >}}) entry named by `entry_name` and stores it in the `dest` memory block along with index structures.

The `skip` value is used to linearize the indexes across multiple calls. Since the numbering of sound effects starts at zero in each new file, the number from the file can't be used directly as it would overwrite indexes from earlier files. The `skip` value is added to each sound effect number to ensure it doesn't interfere with any sounds that have already been loaded.

This function is designed to work only on SOUNDSx.MNI entries, and expects to find 23 entries during each call.

The function begins with a variant of {{< lookup/cref LoadGroupEntryData >}}:

```c
void LoadSoundData(char *entry_name, word *dest, int skip)
{
    int i;
    FILE *fp = GroupEntryFp(entry_name);

    fread(dest, (word)GroupEntryLength(entry_name), 1, fp);
    fclose(fp);
```

The only difference between this and {{< lookup/cref LoadGroupEntryData >}} is the use of {{< lookup/cref GroupEntryLength >}} to dynamically determine the size of the data loaded by {{< lookup/cref fread >}}.

`dest` is a pointer to a block of memory large enough to hold the full contents of the file. At this point, nothing has been parsed or indexed -- the memory at `dest` contains an opaque blob of [sound file headers and data]({{< relref "pc-speaker-sound-format" >}}).

The indexes are constructed next:

```c
    for (i = 0; i < 23; i++) {
        soundDataPtr[i + skip] = dest + (*(dest + (i * 8) + 8) >> 1);
        soundPriority[i + skip + 1] = (byte)*(dest + (i * 8) + 9);
    }
}
```

As best as I can determine, this is actually the way the original C code was written. It's a bit of a head-scratcher, so I'll step through it.

The sound file starts with a 16-byte [file header]({{< relref "pc-speaker-sound-format#file-header" >}}) that is completely unused. Following that, there is a [sound effect table]({{< relref "pc-speaker-sound-format#sound-effect-table" >}}) that consists of a 16-byte structure that repeats 23 times, once for each sound effect. Within each structure, the word at offset 0h is the offset of that sound effect's data in the file, and the byte at offset 2h is the **priority** of that sound effect.

The first piece of computation is `*(dest + (i * 8) + 8) >> 1`. Because `dest` is a pointer to a word value, each unit of pointer arithmetic moves the memory position by two bytes. `i * 8` positions the offset on a 16-byte boundary, and `+ 8` skips over the 16-byte file header. The net result points to offset 0h in the `i`th sound effect table entry in `dest`. The pointer is then dereferenced, yielding the offset of this sound effect's data _in bytes_. `dest` is a word pointer, so the value must be halved to refer to the correct offset in words. The one-bit right shift (`>> 1`) accomplishes this.

By adding the computed sound offset to the `dest` pointer again, we end up with the memory address where the `i`th sound effect's data begins. This value is stored in the {{< lookup/cref soundDataPtr >}} array, indexed by `i` plus the value in `skip`.

The second computation is `*(dest + (i * 8) + 9)`, which is not terribly different from the first. As before, this positions the offset on a 16-byte boundary, and `+ 9` not only skips over the 16-byte header, but also skips over the first two bytes of the structure. The net result points to offset 2h in the `i`th sound effect table entry in `dest`. The pointer is then dereferenced, resulting in a _word_ value containing the sound effect's priority number in the low byte, and junk data from the file in the high byte.

The word value is truncated to a byte, discarding the junk data and leaving the priority. This value is stored in the {{< lookup/cref soundPriority >}} array, indexed by `i`, plus the value in `skip`, plus a constant 1 -- for unknown reasons, the sound priority array is one-based while the pointer array uses zero.

This loop runs a total of 23 times, and creates the pointer and priority indexes for all the sound effects in the file.

{{< boilerplate/function-cref LoadMusicData >}}

The {{< lookup/cref LoadMusicData >}} function opens music data from a group file entry (expressed by passing one of the available {{< lookup/cref MUSIC >}} values in `music_num`), loads the data into the {{< lookup/cref Music >}} structure pointed to by `dest`, and prepares the AdLib service to receive new music data. Returns a pointer to `dest`.

```c
Music *LoadMusicData(word music_num, Music *dest)
{
    FILE *fp;
    Music *localdest = dest;

    miscDataContents = IMAGE_NONE;
```

This function begins by making a local copy of the _pointer_ to `dest`, which really serves no purpose other than to create an additional name (`localdest`) that points to the same structure.

{{< lookup/cref miscDataContents >}} is set to {{< lookup/cref name="IMAGE" text="IMAGE_NONE" >}} as a flag for other parts of the program that {{< lookup/cref miscData >}} (which **might** be providing the memory that `dest` points to) could soon contain non-image data. Compare {{< lookup/cref StartGameMusic >}} and {{< lookup/cref StartMenuMusic >}} for more information about how `dest` is provided to this function.

```c
    fp = GroupEntryFp(musicNames[music_num]);
    fread(&dest->datahead, 1, (word)lastGroupEntryLength + 2, fp);
    localdest->length = (word)lastGroupEntryLength;
```

{{< lookup/cref musicNames >}} is an array which maps the numerical `music_num` (0--18) to a group file entry name. This name is passed to {{< lookup/cref GroupEntryFp >}} which returns a file stream pointer to the located music data to `fp`.

{{< lookup/cref fread >}} loads the music data from `fp` into memory, with the write position starting at the address of `dest->datahead`. The memory block that `dest` maps to is much larger than the {{< lookup/cref Music >}} structure, so this read simply overruns the end of the defined structure members and fills up as much memory as {{< lookup/cref name="lastGroupEntryLength" text="lastGroupEntryLength + 2" >}} says it should. The addition of two, by the way, is _absolutely baffling_ and I can't fathom why it is needed or if it is even correct to do.

```c
    SetMusicState(true);

    fclose(fp);

    return localdest;
}
```

{{< lookup/cref name="SetMusicState" text="SetMusicState(true)" >}} ensures the AdLib service is enabled and the system timer is running at the correct rate to support it. It also temporarily pauses the actual output functions of the AdLib service, since the music is currently in a not-fully-configured state. (New music has been loaded into memory, but the pointers and statuses used by the AdLib service are not yet set up to point to the beginning of it, among other things.)

`fp` is closed with {{< lookup/cref fclose >}}, freeing its resources. Finally, the `localdest` is returned to the caller. This is identical to `dest`, which the caller provided and presumably still has, but that's how this was written.
