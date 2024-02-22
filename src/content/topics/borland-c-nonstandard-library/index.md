+++
title = "The Borland C Nonstandard Library"
description = "Documentation for every nonstandard Borland Turbo C library function used in the game."
weight = 580
+++

# The Borland C Nonstandard Library

Version 2.0 of Borland Turbo C was released in 1988, around the same time that the ANSI C standard was being finalized. Most of Turbo C's language features were influenced by the earlier specifications by Brian W. Kernighan and Dennis M. Ritchie ("K&R C"), but early ANSI draft standards no doubt played a part as well. While most of the functions provided by Borland's standard library ended up matching the final ANSI standard closely, many functions were vendor-specific and never appeared in any published standard. Most of these functions are specific to either the IBM PC hardware, the DOS API, or both. The game uses {{< index/num-borland-functions >}} of these functions throughout its code.

This page collects information and examples on these obsolete and/or nonstandard library functions (and their associated enums and structs) directly from the Borland manuals. Functions with standard behavior, and details that still apply to modern C implementations or POSIX-compliant environments, have been omitted.

{{< table-of-contents >}}

{{< boilerplate/global-cref COLORS >}}

These color values are accepted in text mode to control both the foreground and background colors of text. These values control foreground color; shifting the value 4 bits to the left will control the background color. Generally graphics palette indexes follow the same ordering and naming style. Adding the numeric value of `BLINK` to any value will cause the text to flash.

Symbolic Constant | Value
------------------|------
`BLACK`           | 0
`BLUE`            | 1
`GREEN`           | 2
`CYAN`            | 3
`RED`             | 4
`MAGENTA`         | 5
`BROWN`           | 6
`LIGHTGRAY`       | 7
`DARKGRAY`        | 8
`LIGHTBLUE`       | 9
`LIGHTGREEN`      | 10
`LIGHTCYAN`       | 11
`LIGHTRED`        | 12
`LIGHTMAGENTA`    | 13
`YELLOW`          | 14
`WHITE`           | 15
`BLINK`           | 128

### Defined In

 `conio.h`

{{< boilerplate/global-cref coreleft >}}

It gives a different measurement value, depending on whether the memory model is of the small data group or the large data group.

### Prototype In

 `alloc.h`

### Syntax

In the tiny, small, and medium models:

```c
unsigned coreleft(void);
```

In the compact, large, and huge models:

```c
unsigned long coreleft(void);
```

### Return Value

In the large data models, `coreleft()` returns the amount of unused memory between the heap and the stack.

In the small data memory models, `coreleft()` returns the amount of unused memory between the stack and the data segment minus 256 bytes.

### Notes

This function is unique to DOS.

{{< boilerplate/global-cref disable >}}

`disable()` is designed to provide a programmer with flexible hardware interrupt control. Only the NMI interrupt will still be allowed from any external device.

### Prototype In

`dos.h`

### Return Value

None.

### Notes

This macro is unique to the 8086 family of processors.

{{< boilerplate/global-cref enable >}}

`enable()` is designed to provide a programmer with flexible hardware interrupt control.

### Prototype In

`dos.h`

### Return Value

None.

### Notes

This macro is unique to the 8086 family of processors.

{{< boilerplate/global-cref farmalloc >}}

For allocating from the far heap, note that:

* All available RAM can be allocated.
* Blocks larger than 64K can be allocated.
* Far pointers are used to access the allocated blocks.

In the compact, large, and huge memory models, `farmalloc()` is similar, though not identical, to {{< lookup/cref malloc >}}. `farmalloc()` takes unsigned long parameters, while malloc takes unsigned parameters.

A tiny model program cannot make use of `farmalloc()` if it is to be converted to a .COM file.

### Prototype In

`alloc.h`

### Return Value

`farmalloc()` returns a pointer to the newly allocated block, or `NULL` if not enough space exists for the new block.

### Notes

`farmalloc()` is unique to DOS.

### Example

```c
/*
Far Memory Management
farcoreleft - gets the amount of core memory left
farmalloc - allocates space on the far heap
farrealloc - adjusts allocated block in far heap
farfree - frees far heap
*/

#include <stdio.h>
#include <alloc.h>

main()
{
    char far *block;
    long size = 65000;

    /* Find out what's out there */
    printf("%lu bytes free\n", farcoreleft());

    /* Get a piece of it */
    block = farmalloc(size);
    if (block == NULL) {
        printf("failed to allocate\n");
        exit(1);
    }
    printf("%lu bytes allocated, ", size);
    printf("%lu bytes free\n", farcoreleft());

    /* Shrink the block */
    size /= 2;
    block = farrealloc(block, size);
    printf("Block now reallocated to %lu bytes, ", size);
    printf("%lu bytes free\n", farcoreleft());

    /* Let it go entirely */
    printf("Free the block\n");
    farfree(block);
    printf ("Block now freed, ");
    printf("%lu bytes free\n", farcoreleft());
}  /* End of main */
```

Program output:

```plaintext
359616 bytes free
65000 bytes allocated, 294608 bytes free
Block now reallocated to 32500 bytes, 262100 bytes free
Free the block
Block now freed, 359616 bytes free
```

{{< boilerplate/global-cref filelength >}}

### Prototype In

`io.h`

### Return Value

On success, `filelength()` returns a long value, the file length in bytes. On error, it returns -1, and `errno` is set to `EBADF` ("bad file number").

{{< boilerplate/global-cref fileno >}}

If `stream` has more than one handle, `fileno()` returns the handle assigned to the stream when it was first opened.

### Prototype In

`stdio.h`

### Return Value

`fileno()` returns the integer file handle associated with `stream`.

{{% note label="Note from the 21st century" %}}The `stream` argument to this function should be a pointer to a `FILE` stream. In the definition of the `FILE` struct, `fd` is a char. If we're being pedantic, the return type of `fileno()` is actually char.{{% /note %}}

{{< boilerplate/global-cref getch >}}

`getch()` uses `stdin`.

### Prototype In

`conio.h`

### Return Value

`getch()` returns the character read from the keyboard.

### Notes

This function is unique to DOS.

{{< boilerplate/global-cref getvect >}}

Every processor of the 8086 family includes a set of interrupt vectors, numbered 0 to 255. The 4-byte value in each vector is actually an address, which is the location of an interrupt function ("interrupt service routine"). The value of `interruptno` can be from 0 to 255.

### Prototype In

`dos.h`

### Return Value

`getvect()` returns the current 4-byte value stored in the interrupt vector named by `interruptno`.

### Notes

This function is unique to DOS.

### Example

```c
#include <stdio.h>
#include <dos.h>

/* getvect example */

void interrupt (*oldfunc)();
int looping = 1;

/* get_out - this is our new interrupt routine */
void interrupt get_out()
{
    /* restore to original interrupt routine */
    setvect(5, oldfunc);
    looping = 0;
}

/* capture_prtscr - installs a new interrupt for <Shift><PrtSc> */
/* arguments: func -- new interrupt function pointer */
void capture_prtscr(void interrupt (*func)())
{
    /* save the old interrupt */
    oldfunc = getvect(5);
    /* install our interrupt handler */
    setvect(5, func);
}

void main()
{
    puts("Press <Shift><PrtSc> to terminate");
    /* capture the print screen interrupt */
    capture_prtscr(get_out);

    /* do nothing */
    while (looping);

    puts ("Success");
}
```

{{< boilerplate/global-cref getw >}}

`getw()` should not be used when the stream is opened in text mode.

### Prototype In

`stdio.h`

### Return Value

`getw()` returns the next integer on the input stream. On end-of-file or error, `getw()` returns `EOF`. Because `EOF` is a legitimate value for `getw()` to return, {{< lookup/cref feof >}} or {{< lookup/cref ferror >}} should be used to detect end-of-file or error.

{{< boilerplate/global-cref inportb >}}

If `inportb()` is called when `dos.h` has been included, it will be treated as a macro that expands to inline code.

If you don't include `dos.h`, or if you do include `dos.h` and `#undef` the macro `inportb`, you will get the `inportb()` function.

### Prototype In

`dos.h`

### Return Value

`inportb()` returns the value read.

### Notes

`inportb()` is unique to the 8086 family of processors.

{{< boilerplate/global-cref int86 >}}

Before executing the software interrupt, it copies register values from {{< lookup/cref REGS >}} `inregs` into the registers.

After the software interrupt returns, `int86()` copies the current register values to {{< lookup/cref REGS >}} `outregs`, copies the status of the carry flag to the `x.cflag` field in `outregs`, and copies the value of the 8086 flags register to the `x.flags` field in `outregs`. If the carry flag is set, it usually indicates that an error has occurred.

Note that `inregs` can point to the same structure that `outregs` points to.

### Prototype In

`dos.h`

### Return Value

`int86()` returns the value of AX after completion of the software interrupt. If the carry flag is set (`outregs->x.cflag != 0`), indicating an error, this function sets `_doserrno` to the error code.

### Notes

This function is unique to the 8086 family of processors.

### Example

```c
#include <dos.h>

#define VIDEO 0x10

/* gotoxy - positions cursor at line y, column x */
void gotoxy(int x, int y)
{
    union REGS regs;

    regs.h.ah = 2;  /* set cursor position */
    regs.h.dh = y;
    regs.h.dl = x;
    regs.h.bh = 0;  /* video page 0 */

    int86(VIDEO, &regs, &regs);
}
```

{{< boilerplate/global-cref MK_FP >}}

### Prototype In

`dos.h`

### Return Value

`MK_FP()` returns a far pointer.

{{< boilerplate/global-cref movmem >}}

Even if the source and destination blocks overlap, the copy direction is chosen so that the data is always copied correctly.

### Prototype In

`mem.h`

### Return Value

None.

### Notes

This function operates in essentially the same way as {{< lookup/cref memmove >}} from `string.h`, except `src` and `dest` are swapped.

{{< boilerplate/global-cref outport >}}

### Prototype In

`dos.h`

### Return Value

None.

### Notes

This function is unique to the 8086 family of processors.

{{< boilerplate/global-cref outportb >}}

If `outportb()` is called when `dos.h` has been included, it will be treated as a macro that expands to inline code.

If you don't include `dos.h`, or if you do include `dos.h` and `#undef` the macro `outportb`, you will get the `outportb()` function.

### Prototype In

`dos.h`

### Return Value

None.

### Notes

`outportb()` is unique to the 8086 family of processors.

{{< boilerplate/global-cref putw >}}

`putw()` neither expects nor causes special alignment in the file.

### Prototype In

`stdio.h`

### Return Value

On success, `putw()` returns the integer `w`. On error, `putw()` returns `EOF`.

Since `EOF` is a legitimate integer, {{< lookup/cref ferror >}} should be used to detect errors with `putw()`.

{{< boilerplate/global-cref random >}}

`random(num)` is a macro defined as `(`{{< lookup/cref rand >}}` % (num))`. Both `num` and the random number returned are integers.

### Prototype In

`stdlib.h`

### Return Value

`random()` returns a number between 0 and (`num` - 1).

### Example

```c
#include <stdlib.h>
#include <time.h>

/* prints a random number (1-20) of random numbers in the range 0-99 */

main()
{
    int n;
    randomize();
    /* selects a random number between 1 and 20 */
    n = random(20) + 1;
    while (n-- > 0)
        printf("%d ", random(100));
    printf ("\n");
}
```

{{< boilerplate/global-cref REGS >}}

All 16-bit word registers are available in `x`. The half-word views into AX, BX, CX, and DX are available in `h`. The definitions of these structs are as follows:

```c
struct WORDREGS {
    unsigned int ax, bx, cx, dx, si, di, cflag, flags;
};

struct BYTEREGS {
    unsigned char al, ah, bl, bh, cl, ch, dl, dh;
};
```

### Defined In

`dos.h`

{{< boilerplate/global-cref setvect >}}

The address of a C routine can only be passed to `isr` if that routine is declared to be an `interrupt` routine.

Every processor of the 8086 family includes a set of interrupt vectors, numbered 0 to 255. The 4-byte value in each vector is actually an address, which is the location of an interrupt function ("interrupt service routine").

### Prototype In

`dos.h`

### Return Value

None.

### Notes

If you use the prototypes declared in `dos.h`, you can simply pass the address of an interrupt function to `setvect()` in any memory model.

This function is unique to the 8086 family of processors.

{{< boilerplate/global-cref strupr >}}

### Prototype In

`string.h`

### Return Value

`strupr()` returns `s`.

{{< boilerplate/global-cref text_modes >}}

The `text_modes` type constants, their numeric values, and the modes they specify are given in the following table:

Symbolic Constant | Value | Text Mode
------------------|-------|----------
`LASTMODE`        | -1    | Previous text mode.
`BW40`            | 0     | Black and white, 40 columns.
`C40`             | 1     | Color, 40 columns.
`BW80`            | 2     | Black and white, 80 columns.
`C80`             | 3     | Color, 80 columns.
`MONO`            | 7     | Monochrome, 80 columns.

### Defined In

`conio.h`

{{< boilerplate/global-cref textmode >}}

You can give the text mode (the argument `newmode`) by using a symbolic constant from the {{< lookup/cref text_modes >}} type. To use these constants, you must include `conio.h`.

When `textmode()` is called, the current window is reset to the entire screen, and the current text attributes are reset to normal, corresponding to a call to `normvideo()`.

Specifying {{< lookup/cref name="text_modes" text="LASTMODE" >}} to `textmode()` causes the most recently selected text mode to be reselected. This feature is really only useful when you want to return to text mode after using a graphics mode.

`textmode()` should be used only when the screen is in the text mode (presumably to change to a different text mode). This is the only context in which `textmode()` should be used. When the screen is in graphics mode, you should use `restorecrtmode()` instead to escape temporarily to text mode.

### Prototype In

`conio.h`

### Return Value

None.

### Notes

`textmode()` works with IBM PCs and compatibles only.

{{< boilerplate/global-cref ultoa >}}

`value` is an unsigned long.

`radix` specifies the base to be used in converting `value`; it must be between 2 and 36, inclusive. `ultoa()` performs no overflow-checking, and if `value` is negative and `radix` equals 10, it does not set the minus sign.

### Prototype In

`stdlib.h`

### Return Value

`ultoa()` returns `string`. There is no error return.

### Notes

The space allocated for `string` must be large enough to hold the returned string, including the terminating null character (`\0`). `ultoa()` can return up to 33 bytes.
