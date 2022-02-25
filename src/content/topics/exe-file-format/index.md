+++
title = "EXE File Format"
description = "An analysis of the executable files of each episode of the game."
weight = 60
+++

# EXE File Format

{{< table-of-contents >}}

A reasonable place to start the discussion is with the game's executable files. A user would run  `COSMO1.EXE` if they wanted to play episode one, `COSMO2.EXE` for episode two, and `COSMO3.EXE` for episode three. Each executable contains a different variant of the base game, with enough substantial differences that the [group files]({{< relref "group-file-format" >}}) from different episodes cannot be interchanged and played. The file structure and naming conventions permit all three episodes to coexist in the same directory without conflict, although the installer programs seem to prefer to install each episode in its own directory.

There are a few obvious differences right off the bat. Take the file sizes, for instance:

File       | Version | Size (Bytes) | Date           | Hashes (MD5, SHA-1)
-----------|---------|--------------|----------------|--------------------
COSMO1.EXE | 1.20    | 62,081       | April 15, 1992 | `247ea7fc151a0a4f866ba7140800b54f`,<br>`132b18e2c66f1a96ce0893310e58308765e86e52`
COSMO2.EXE | 1.20    | 58,805       | April 15, 1992 | `8163e3e08850cd1455c8d6eb23ba33a1`,<br>`48559d041156f5368c2a70029bd1be74276bcede`
COSMO3.EXE | 1.20    | 119,078      | April 15, 1992 | `31c89929b4ebcb39416c7e71a3e0bf9e`,<br>`536eb77a6b819a4feee78011823105c49849d952`

The executable file for episode three is almost twice as large as the executable files for the other two episodes. Hex dumps of the EXE headers offer some insight as to why:

**COSMO1.EXE:**

```hexdump
00000000: 4d5a 8100 7a00 0000 0200 f814 ffff 361d  MZ..z.........6.
00000010: 8000 0000 0e00 b20e 1c00 0000 4c5a 3931  ............LZ91
```

**COSMO2.EXE:**

```hexdump
00000000: 4d5a b501 7300 0000 0200 1b14 ffff 941b  MZ..s...........
00000010: 8000 0000 0e00 ed0d 1c00 0000 4c5a 3931  ............LZ91
```

**COSMO3.EXE:**

```hexdump
00000000: 4d5a 2601 e900 1005 6001 6b06 ffff 0e22  MZ&.....`.k...."
00000010: e600 0000 0000 0000 2200 0000 0100 fb20  ........"...... 
```

COSMO1 and COSMO2 contain the signature `LZ91` in the EXE header, while COSMO3 does not. This is a pretty reliable indication that the executable files for the first two episodes were compressed using a utility called [LZEXE]({{< relref "lzexe" >}}), and the third episode was not.

{{< aside class="speculation" >}}
**Why is the third episode different?**

It's not clear why the third episode was left uncompressed. It's possible there was a bug or limitation in LZEXE that prevented that particular episode from being compressed. Perhaps there was a late change or bug fix in that episode and the compression step was overlooked during the rush.

Given that episode three has the smallest group files of the series, it could've been a simple case of the episode fitting on the installation disks without further compression, so it wasn't attempted in the first place.
{{< /aside >}}

After removing the LZEXE compression, the file sizes are:

* **COSMO1.EXE:** 123,126 bytes
* **COSMO2.EXE:** 116,040 bytes
* **COSMO3.EXE:** 119,078 bytes

In the rest of this document, I use the uncompressed EXE files. These were created by running UNLZEXE[^unlzexe] on the original EXE files.

## EXE Header

The main header of an MS-DOS executable file is stored in the first 28 bytes. These values are used by DOS to determine where in memory the program can fit, and what must be done to ensure that execution can be handed off to the program without any trouble.

All three episodes are substantially similar, but they are not identical.

Offset (Bytes) | Size  | COSMO1    | COSMO2    | COSMO3    | Description
---------------|-------|-----------|-----------|-----------|------------
00h            | word  | `MZ`      | `MZ`      | `MZ`      | EXE file signature. Always either `MZ` or `ZM`.[^mz]
02h            | word  | 00F6h     | 0148h     | 0126h     | Number of bytes used in the last 512-byte page of the executable.
04h            | word  | 00F1h     | 00E3h     | 00E9h     | Total number of 512-byte pages in the executable, including the last (partial) page.
06h            | word  | 0564h     | 04ECh     | 0510h     | Number of entries in the relocation table.
08h            | word  | 0160h     | 0140h     | 0160h     | Header size, in 16-byte paragraphs.
0Ah            | word  | 066Bh     | 066Bh     | 066Bh     | Minimum additional memory to allocate, in 16-byte paragraphs.
0Ch            | word  | FFFFh     | FFFFh     | FFFFh     | Maximum additional memory to allocate, in 16-byte paragraphs.
0Eh            | word  | 230Bh     | 2170h     | 220Eh     | Initial SS value, relative to the loaded executable's start address.
10h            | word  | 00E6h     | 00E6h     | 00E6h     | Initial SP value.
12h            | word  | 0000h     | 0000h     | 0000h     | Checksum, or 0 if not used.
14h            | dword | 0000:0000 | 0000:0000 | 0000:0000 | Initial CS:IP value, relative to the loaded executable's start address.
18h            | word  | 001Ch     | 001Ch     | 0022h     | Offset of relocation table, in bytes.
1Ah            | word  | 0000h     | 0000h     | 0000h     | Overlay number, or 0 if main program.

The differences between the three EXE headers are for predictable and benign reasons. The total number of pages, number of bytes in the last page, number of relocation table entries, header size, and SS value are all different because the executable files all have different amounts of code and data in them.

COSMO3 has a few extra header bytes that precede the relocation table. This appears to be data inserted by Borland TLINK. Since the LZEXE &rarr; UNLZEXE translation of COSMO1 and COSMO2 stripped these values out, they are almost certainly not important to the actual function of the program.

Offset (Bytes) | Size | COSMO3 | Description
---------------|------|--------|------------
1Ch            | word | 0001h  | Unknown purpose, apparently always 1.
1Eh            | byte | FBh    | Identifier, always FBh.
1Fh            | byte | 20h    | TLINK version, major component in the high nibble.
20h            | word | 6A72h  | Unknown purpose. Maybe `rj` in ASCII?

If you can provide any further information about the meaning of any of these fields, please let me know!

## Relocation Table

Normal program execution is linear, with each instruction directly following the one that came before. *Jump* and *call* instructions interrupt this flow and force the program to jump to arbitrary positions in the code.

The simpler method of accomplishing such movement is to use relative addressing, where the program says "jump *n* bytes ahead of where we otherwise would have ended up if we had proceeded sequentially." In relative addressing, it doesn't matter where the program is physically located in memory, "n bytes from wherever we are" means the same thing no matter where we currently are.

Relative addressing begins to fall apart in a program of any appreciable size, because adding or removing code anywhere requires the entire program to be reexamined and all the relative distances recomputed. This becomes a tedious chore (even for a computer), especially if the program is integrating with third-party library code. The CPU itself even has limits on how far it is willing to jump in this way.

The alternative to relative addressing is absolute addressing, where the program says "jump to this specific byte of the computer's memory." It doesn't matter if code moves around in absolute addressing, all that matters is that the memory being targeted has the value that's expected to be there.

Absolute addressing has its drawbacks. When an MS-DOS program is running, it has to coexist with DOS itself, device drivers, reserved areas, and any terminate-and-stay-resident programs that may be occupying space in memory. There are no guarantees about what memory address an executable file will be loaded into. It can and frequently does change from run to run.

To solve this problem, the EXE file format uses a relocation table. When the EXE file is created, all absolute addresses are calculated with the assumption that the program will be loaded at the absolute beginning of the computer's memory (at address 0000:0000). This never happens in practice; the first kilobyte of memory, for example, contains the CPU's interrupt vector table -- something that _definitely_ should not be overwritten by programs.

When DOS loads an executable into memory, it does so at some arbitrary address. The start address is chosen based on the size of the program, the additional memory requirements stated in its header, and the layout of free memory on the system. But it's never 0000:0000.

The relocation table holds a list of positions in the EXE file where such an absolute address appears. The DOS loader visits each position in the file, "fixes up" the address stored there by adding the real starting address to it, and saves the result in the executable's memory image. By patching the every absolute address in the EXE file, the entire program image can be installed at any memory address and still refer to positions within itself in a consistent and correct way.

{{< aside class="fun-fact" >}}
**EXE vs. COM**

Relocation is not a problem in the older, simpler COM file format. In that model, DOS picks a suitable segment address where the program is to be loaded, and both code and data get stored there without modification. Since the segment address never changes, the program doesn't need to worry about what it is actually set to, and "offset-only" absolute addressing works without any fixups.

All this has the rather unfortunate side effect that the program's code and data -- *combined* -- have to be smaller than 64 KiB.
{{< /aside >}}

The number of relocation entries is loosely correlated with the overall size of each executable:

* **COSMO1.EXE:** 1,380 relocation entries
* **COSMO2.EXE:** 1,260 relocation entries
* **COSMO3.EXE:** 1,296 relocation entries

Each relocation table entry is a 4-byte pointer containing an offset word and a segment word. The end of the relocation table is padded with null bytes until the start of the next 512-byte paragraph boundary. The "header size" field in the EXE header (word 08h) includes the space occupied by the relocation table and its end padding.

## Code

After the header and relocation table, the actual executable image begins. In all three episodes, the CPU starts execution at the very first instruction of this image (this is specified in the EXE headers, at dword 14h).

Cosmo's Cosmic Adventure, being a DOS game without extenders, is 16-bit real mode code. The majority of the instruction set used by the game was introduced with the original Intel 8086 CPU in 1979, and only a handful of real-mode 80286 instructions were used.

In 16-bit x86 machine code, each individual instruction is encoded as a variable-length sequence of bytes. Some common instructions are single bytes, others use as many as six bytes. As the CPU consumes each byte, it is able to unambiguously determine if it needs to consume more bytes to form a complete instruction.

The "important" code in the executable -- that is, code written specifically for the game without considering the C runtime and libraries -- consists of about 33,500 x86 instructions. The [hint sheet]({{< relref "hint-sheet" >}}) states that the game has 24,500 lines of code, but I estimate the true C+assembly line count to be closer to 14,000 if comments are sparse.

The code is partitioned into a few different sections, each of which came from a different source and serves a different sort of purpose:

* The Borland Turbo-C Runtime
* Assembly Routines
* ASM Global Variables
* Runtime/Library Routines
* Compiled Code
* Library Code

### The Borland Turbo-C Runtime

The code starts with some dense and very un-C-like procedures. This is C0.ASM, the startup code for the Borland Turbo-C runtime. This code is responsible for receiving control from DOS, setting up a reasonable environment for the program to run in, populating environment variables/`argc`/`argv`, calling the programmer-defined {{< lookup/cref main >}} function, and handling unexpected program termination.

C0.ASM is available in unassembled, commented form as part of the Turbo-C development toolchain. There are a number of conditional flags to control various behaviors of the runtime, including software emulation of floating-point hardware. The startup code can even be replaced entirely at the programmer's discretion, but that does not appear to have been done here. The only significant customization is the configuration of the memory model; as far as I can tell it was set to "large."

The startup code occupies 455 bytes of space in each executable file. Since it pertains mostly to things that happen before {{< lookup/cref main >}} starts (or after it returns) it's not important to decipher.

### Assembly Routines

Next in the executable code are the game's assembly language routines. There are instructions in this area that are not emitted anywhere else in the code, heavily unrolled loops, as well as some rather clever shortcuts that suggest these were all written by hand and not by a compiler.

These routines handle low-level setup and management of the video hardware, and there are about a half-dozen different draw functions that move 8x8 pixel images from tile memory to the visible screen area in different ways. Three functions brighten areas of the screen in response to lighted areas on some levels, and there is also a fascinating CPU feature detection routine.

The assembly-language code occupies 2,502 bytes of space in each executable file. In total there are fifteen procedures in this area.

### ASM Global Variables

Immediately after the Turbo-C runtime, there are three words of variable data. The first word is owned by the C runtime, and it holds the address of the data segment. The other two words are owned by the game's assembly routines, and they hold information about the current display page and base address for the video memory.

### Runtime/Library Routines

Next up are a few impenetrable assembly routines that are either part of the Turbo-C runtime itself or the C library functions. These are responsible for a variety of things, including initialization of `envp`, multiplication and division of 32-bit long integers, as well as copying static arrays from the data segment into the stack. I briefly tried figuring out how these worked and it just about drove me mad. For our purposes, it is enough to know what they do without knowing exactly how they do it.

These occupy 1,040 bytes of space in each executable file.

### Compiled Code

This is the true meat of the game, and where the majority of my attention was directed. There are about 270 functions (&plusmn;5 depending on the episode) in this area, all of which appear to have been compiled from C code. There is occasional evidence of inline assembly within a few of the functions, but it is exceedingly rare.

Conveniently enough, the very first function in this section is {{< lookup/cref main >}}.

The size of this section varies depending on the game. Different episodes have different stories and menu areas, and certain actor types are conditionally compiled to be omitted from certain episodes:

* **COSMO1.EXE:** 82,536 bytes of compiled code
* **COSMO2.EXE:** 79,689 bytes of compiled code
* **COSMO3.EXE:** 81,522 bytes of compiled code

Most of this site is devoted to explaining what the code in here does. With that in mind, enough has been said here.

### Library Code

The last part of the executable code houses the C library functions. These are included by the programmer and pulled in by the linker to perform low-level operations like file access and memory allocation.

No effort was made to investigate how any of these functions worked. As soon as I understood enough about each one to unambiguously associate it with a known C library function call, I moved on.

This code occupies 14,372 bytes in each executable file. The remaining space directly after the library code is padded with null bytes until the start of the next 16-byte paragraph/segment boundary.

## Data

The final section of the executable file is the static data segment. When the program begins executing, the CPU's DS register is set to point to this area and it does not change over the course of execution.

{{< note >}}
If we're being pedantic, the DS register *does* change sometimes during data movement operations and the like, but it is always set back to the static data area once the work is done.
{{< /note >}}

One of the first values in the data is an interesting string:

    Turbo-C - Copyright (c) 1988 Borland Intl.

While it doesn't specify exactly which version of C the game was compiled with, it certainly narrows it down. In 1988 the most recently released version of Turbo-C would have been 2.01. That version included TLINK 2.0, which is corroborated by the EXE header signature (byte 1Fh) found in COSMO3. The Turbo Assembler version is nowhere near as guessable, and could plausibly be anything from 1.0 to 3.0.

The actual game-specific data doesn't start until 148 bytes into the data segment (everything before that belongs to the runtime/startup code). Generally, the data stored here falls into one of the following categories:

* Static text strings, or pointers to them
* Pre-initialized, nonzero values for global or static variables
* Array/table members

The majority of the data in here is human-readable text for the menus and UI. The total size of the game-specific data for each episode is:

* **COSMO1:** 15,227 bytes
* **COSMO2:** 11,501 bytes
* **COSMO3:** 12,187 bytes

Following the game data, there is 1,191 bytes of static data for the C library functions whose purpose is opaque.

{{< aside class="fun-fact" >}}
Some of the more interesting string values in the C library include:

* `.$$$` (a temporary file extension?)
* `print scanf : floating point formats not linked`
* `(null)`
* `0123456789ABCDEF` (for {{< lookup/cref printf >}} with `%X`?)
* `COMPAQ`

I do not want to think about what it needs "COMPAQ" for.
{{< /aside >}}

## And Beyond

At this point, the executable file has ended and there is nothing more to read. Conceptually, though, there are a few additional structures implied by the EXE header.

Each episode's header states that it requires 66Bh 16-byte paragraphs, or 26,288 bytes, minimum additional memory (EXE header word 0Ah). DOS allocates this memory when it loads the program, and it arranges the memory so that this area begins right after the end of the static data. In a sense, the EXE file is almost 26 KiB longer than it is on disk, with the tail end filled with null bytes. To the program, this is space reserved for global variables that have no initial value defined. This is where uninitialized "BSS" data and the stack reside.

The EXE header defines values for both the stack segment and the stack pointer (words 0Eh and 10h, respectively), which together point to a memory location that resides near the end of this space. Initially there is only 230 bytes of stack space available before SP wraps around from 0000h back to FFFFh. Part of the runtime startup code does some negotiating with DOS to bring the amount of stack space up to 4,096 bytes, if I am reading C0.ASM correctly.

[^unlzexe]: unlzexe 0.9G2 by Anders Gavare (http://files.shikadi.net/malv/files/unlzexe.c)

[^mz]: The initials of Mark Zbikowski, the designer of the MS-DOS executable file format.
