+++
title = "Processor Detection"
description = "A deep dive on CPU quirks of the early 1980s and how to use them to detect different processor models."
weight = 210
+++

# Processor Detection

By early 1992, there were a few different PC processors available on the market. The original IBM PC and its successor, the IBM PC/XT, shipped with an Intel 8088 processor. The later IBM PC/AT and compatible clones had an 80286, and newer computers with 386 and 486 processors were also available at substantial cost.

The Intel 286 was a big improvement over the 8088, and not just due to clock speed increases. It had a 24-bit address bus, supporting 16 MiB of memory instead of the previous limit of 1 MiB. Additions to the instruction encodings were particularly important to compilers of the era: `enter`, `leave`, and support for immediate operands on `imul`, `push`, and bit shifts were all put to frequent use. The game was compiled with the expectation that these instruction encodings would be available, making it unable to run on an 8088.

{{< aside class="fun-fact" >}}
**If we're being pedantic...**

These instructions were actually added in the Intel 80186, which never shipped in any IBM PC or mainstream compatible computer.

The 286's other big selling point was the addition of **protected mode** (to replace the **real mode** used by DOS programs), which didn't see much adoption before it was improved for the 386.
{{< /aside >}}

At the time, there was no formal interface a program could use to query the CPU type installed in a system. The conventional way to do it was to try "unusual stuff" and see how the processor responded -- different models handled these cases in different ways.

By combining tests, it was possible to reliably discern between an 8088, 8086, NEC V20, V30, 188, 186, 286, and 386. That's what the game did.

{{< boilerplate/function-cref GetProcessorType >}}

The {{< lookup/cref GetProcessorType >}} function is written in Turbo Assembler (TASM) assembly, using only 8086-compatible instruction encodings, and takes no arguments. It's designed to run correctly on any conceivable PC processor.

The procedure begins with the usual housekeeping:

```tasm
; Since this code might be testing an 8086/88, don't emit any instruction
; encodings that these CPUs did not support.
P8086

PROC _GetProcessorType FAR
        PUBLIC _GetProcessorType
        push  bp
        mov   bp,sp
        push  ds
        push  si
        push  di
        pushf
```

This sets up a stack frame and saves the values of the DS, SI, DI, and FLAGS registers on the stack. Each of these values will be restored before the procedure returns. The stack is not used for any local variable addressing, but the base pointer is available nonetheless.

Next comes the most important test for our purposes: determining if the CPU is a 286 (or better).

### 286 Test

The first test bisects the search into "286 or better" and "less than a 286."

```tasm
        ; Push a zero value to the stack, then immediately pop that zero
        ; value into the FLAGS register. Depending on the CPU, some bits will
        ; refuse this change and remain on.
        xor   ax,ax
        push  ax
        popf

        ; Push the current state of FLAGS to the stack, then immediately pop
        ; the flag state into AX for further analysis.
        pushf
        pop   ax
```

The x86 instruction set does not generally support direct fiddling with bits in the FLAGS register, but it does support pushing the flags onto the stack and popping a stack value into the flags. The CPU doesn't keep track of where any of the stack values came from, so it's possible to write any value to the flags register through use of the stack.

The setup for this test puts the value 0 into AX, pushes AX's value onto the stack, then pops the stack value into FLAGS. This rather circuitous path simply sets FLAGS to zero... or attempts to, anyway. This is the essence of the test: Some CPUs will reject a zero bit in some positions, and others will permit it. By seeing whether FLAGS took a zero or some other value, it is possible to narrow down the CPU type.

As soon as the zero is written to FLAGS, the flag state is pushed onto the stack and popped back into AX. This saves a snapshot of the flag state in a place where it can be analyzed.

```tasm
        ; Consider only flag bits 12..15, and see if they all remained on.
        and   ax,0f000h
        cmp   ax,0f000h
        je    @@less_than_286  ; Jump if all of these bits are on.

        ; DL stores the work-in-progress return value.
        mov   dl,CPUTYPE_80286
```

Prior to the 286, bits 12&ndash;15 of the FLAGS register were undefined and conventionally always held a 1 value. Even after explicitly popping a zero value into the flags, these bits will still hold 1.

If the high four bits of the flags are all 1 (F000h) after being explicitly zeroed, the CPU cannot be a 286 or a 386, so jump to the [tests for lesser processors]({{< relref "#18688-test" >}}). Otherwise, update the DL register with the current status of the test -- the CPU is at least a 286. Fall through to see if it might be a 386.

### 386 Test

If the 286 test passed, the CPU could potentially be a 386.

```tasm
        ; Same as before, but try to set NT = 1b and IOPL = 11b.
        mov   ax,7000h
        push  ax
        popf

        ; Save for analysis.
        pushf
        pop   ax
```

The mechanics of this test are the same as the 286 test, but the value and its interpretation are different. On a 286 or 386, a FLAGS value of 7000h is defined as having Nested Task (NT) = 1 and I/O Privilege Level (IOPL) = 11b. The result of the attempt is copied to AX to see how the CPU reacted.

```tasm
        ; Consider only flag bits 12..14, and see if they all remained off.
        and   ax,7000h
        jz    @@done    ; Jump if all of these bits are off.

        ; Here, at least one of the relevant flag bits turned on, so the CPU
        ; must be a 386.
        inc   dl        ; Return value becomes CPUTYPE_80386.
        jmp   @@done
```

The 286 CPU, running in real mode, keeps both NT and IOPL at zero values and will not accept changes from normal code. If all three of the bits we tried to turn on stayed off, the CPU is a 286. The verdict written to DL in the previous test becomes final, and control jumps to the [procedure return code at `@@done`]({{< relref "#cleanup" >}}).

If, on the other hand, any of the three bits took a 1 value, the CPU must be a 386 which permits such changes. Increment DL, which has the effect of taking the next value in the enumeration-like {{< lookup/cref CPUTYPE >}} group: `CPUTYPE_80386`. This test ends with an unconditional jump to the [procedure return code]({{< relref "#cleanup" >}}).

### 186/88 Test

Once execution reaches this point, the CPU cannot be a 286 or a 386. The next lower possibility is a 186 or 188.

```tasm
@@less_than_286:
        ; Now we know that the CPU is less than a 286.
        mov   dl,CPUTYPE_80188

        ; Perform "FFh >> 33" then check for a zero or nonzero result.
        mov   al,0ffh
        mov   cl,21h
        shr   al,cl
        jnz   @@cpu_class_known  ; Jump if result in AL is not zero.
```

The meat of this test is `AL = FFh >> 33`, written in the constraints of assembly language. Everything is an integer here, so AL should be zero. In fact, it should've been zero after a shift of eight -- why do we need 33?

The designers of the 186 likely had the same thought. These CPUs required a variable number of clock cycles to execute bit shift instructions -- up to four cycles per bit count in the worst case. That means a program could ask for a shift by 255, tying up the CPU for (255 &times; 4) 1,020 clock cycles to perform an operation that was pointless after the first 16 shifts. As a quick fix, the 186 modified its handling of these instructions to zero the highest three bits in CL before shifting. This permitted shifts of 16 (actually, up to 31) without allowing the most absurd of the shift values.

In this instance, zeroing the high three bits of 33 leaves 1, which will leave a nonzero value in AL on a 186. Older CPUs will shift by the insane value 33, leaving zero in AL.

Passing this test means the value held in DL is appropriate -- the CPU is a 186 or 188, so jump to the [`@@cpu_class_known` label]({{< relref "#data-bus-width-detection" >}}) to differentiate between the two.

Otherwise the CPU is worse than a 186. The next lower candidate is the NEC V20, so fall through and test for that.

### V20 Test

The NEC V20 was a drop-in replacement for the Intel 8088 released in the mid 1980s. It was a more complex design than Intel's, supporting several extensions to the original 8086/88 instruction set. It was subjectively faster than similarly-clocked 8088 chips for many common use cases. It also corrected some defects and oversights in the 8088's interrupt handling, which can be exploited to detect this processor family.

```tasm
        ; Now we know that the CPU is less than an 186/188.
        mov   dl,CPUTYPE_V20

        ; Ensure interrupts are enabled, then save SI's value on the stack.
        ; The `push` (and the `pop` below) aren't strictly required since the
        ; SI value is already being saved/restored at the beginning/end of
        ; the procedure.
        sti
        push  si

        ; Here, ES is pointing to some unspecified place in memory. Below is
        ; a busy loop that reads 64 KiB of memory from ES:SI, loading each
        ; byte into AL and doing nothing further with it. After each
        ; iteration, SI is incremented and CX is decremented. The loop ends
        ; when CX reaches zero. Or does it?
        mov   si,0
        mov   cx,0ffffh
        rep lods [BYTE PTR es:si]

        ; Pop the saved value from the stack and restore it to SI.
        pop   si
```

This test starts with some housekeeping of its own. First it ensures that hardware interrupts are enabled. (They should be, but it's good to be explicit because the test relies on it.) The value of SI is also saved, since it gets destroyed next.

`lods` is a so-called "string instruction" that packs a lot of operations into a tiny encoding. Each `lods` copies the byte held in memory at ES:SI into AL, increments the pointer in the SI register, and decrements the value in the CX register. This is meant to be used as a block read operation -- "read CX bytes, starting at ES:SI, one byte at a time and write it into AL."

Prefixing `lods` with `rep` has the effect of repeating the instruction until CX reaches zero. This construction wouldn't normally appear in typical code, as there is no room to actually do anything with the value in AL before a subsequent iteration overwrites it. As written, this is purely a busy loop. This is supported by the fact that the code never sets ES to anything specific, so who knows what part of the memory it's actually reading.

Turns out it doesn't matter, as that's not the part we're interested in. The line with `rep lods` assembles to F3h (`rep`) 26h (`es`) ACh (`lodsb`), which is a single-byte instruction with two single-byte prefixes. The original 8086/88 had a bug related to this condition: If a hardware interrupt occurs while executing an instruction with both a repeat prefix and a segment override prefix, the earlier prefix will be dropped when the interrupt returns. The `lodsb` instruction would then lose its `rep` prefix and cease repeating, and CX would not reach zero as expected. The V20 did not suffer from this defect, and completes the loop fully in all cases.

This code relies on the fact that, in its default configuration, the system timer generates an interrupt approximately once every 55 ms. `rep lods` on an 8086/88 is documented as needing 13 cycles for each iteration, bringing the total length of the operation to at least (13 &times; 65,535) 851,955 cycles, which would be about 85 ms at the chip's maximum clock rate of 10 MHz. The timer would be expected to fire at least once during the whole operation, interrupting the `rep` midway.

Finally, SI is restored to the value it held previously.

With the setup out of the way, the actual interpretation of the test result is trivial:

```tasm
        ; See if the value in CX made it all the way to zero. If it did, the
        ; CPU is a V30 or V20.
        or    cx,cx
        jz    @@cpu_class_known  ; Jump if CX is zero.

        ; Now we know that the CPU is a bottom-rung 8086 or 8088.
        mov   dl,CPUTYPE_8088
```

DL contains the return value for a V20 here. If the entire memory block was read successfully, CX will be zero and that determination will be correct; jump to the [`@@cpu_class_known` label]({{< relref "#data-bus-width-detection" >}}).

Otherwise it's a buggy little processor -- the Intel 8086/8088. Update DL to reflect this and fall through to the [`@@cpu_class_known` label]({{< relref "#data-bus-width-detection" >}}).

### Data Bus Width Detection

This is the target of all the `@@cpu_class_known` jumps. Execution could arrive here with a 186/188, V30/V20, or 8086/8088. The difference between each of these pairs is the **data bus** width -- model numbers ending in "6" have a 16-bit data bus width, and numbers ending in "8" have an 8-bit data bus width. (The V20 was 8-bit, and the V30 was 16-bit.) Aside from the data bus interface, each pair was almost identical internally.

_Almost._ Each CPU contains a **prefetch queue** that reads memory positions ahead of the current execution position to optimize bus usage. Each 16-bit bus CPU prefetches six bytes of memory, while the 8-bit bus CPUs only prefetch four bytes. With a little cleverness, this difference can be measured.

First, some setup:

```tasm
@@cpu_class_known:
        ; Set ES to point to CS, the segment where this code resides, and
        ; turn DF on.
        push  cs
        pop   es
        std

        ; Load DI with the offset part (relative to CS) of the memory address
        ; at the end of the prefetch queue test sequence below.
        mov   di,OFFSET @@qEnd

        ; Set up AL and CX. FBh is the encoding for an `sti` instruction.
        mov   al,0fbh
        mov   cx,3
```

There is a label defined a little later in the code named `@@qEnd` to mark the end of the prefetch queue's reach. As this is part of the currently-executing code, it resides within the segment that CS points to. Therefore ES:DI is set up to point to the labeled `@@qEnd` byte in memory. The **direction flag** (DF) is turned on, which causes string instructions to run in reverse -- decrementing DI toward zero on each iteration. AL and CX get the values FBh and 3, respectively.

The test runs next:

```tasm
        ; Ensure interrupts are disabled, because any deviation in execution
        ; flow will reset the queue and invalidate the test. Write the `sti`
        ; byte three times, starting at `@@qEnd` and working backwards.
        cli
        rep stosb

        ; The `cld` instruction, which turns the Direction Flag back off, is
        ; probably not critical because DF gets restored by `popf` later.
        cld
        nop
        nop
        nop
        inc   dx  ; Increment the running test result value in DX/DL
        nop
@@qEnd: sti
```

This is self-modifying code, which can be a little tricky to reason about. The interplay with the prefetch queue only complicates things.

The first two instructions are simple enough: disable interrupts and run the string copy that was just set up. Turning off the interrupts is critically important, because anything that changes the execution flow of the CPU will clear the prefetch queue and taint the results of the test. `rep stosb` means "until CX reaches zero, copy a byte from AL to ES:DI, decrement DI, and decrement CX." The effective result is that FBh is written to the memory location labeled `@@qEnd` and the two bytes that precede it. Each instruction around `@@qEnd` is a single byte long, so this overwrites `sti`, the last `nop`, and most importantly, `inc dx`. The value written is interpreted as `sti`, so the end result is:

```tasm
        ; ...
        rep stosb  ; Current execution point
        cld        ; Prefetch byte 1
        nop        ; Prefetch byte 2
        nop        ; Prefetch byte 3
        nop        ; Prefetch byte 4; farthest byte queued on 8-bit bus CPUs
        sti        ; Prefetch byte 5
        sti        ; Prefetch byte 6; farthest byte queued on 16-bit bus CPUs
@@qEnd: sti
```

This is what things look like _in memory._ Remember that the CPU has already stored some of these bytes in its prefetch queue, and it's not aware that it has rewritten code it's about to execute.

At the point of the `rep stosb`, 16-bit bus processors have read the next six bytes and 8-bit bus processors have read four. The 16-bits have queued the `inc dx`, and the 8-bits have not. By the time the 8-bit bus processors are able to prefetch the rest of the sequence, `inc dx` has been replaced with `sti` and no increment occurs. 16-bit bus processors run the queued code that contains `inc dx`, unaware that the instructions had changed in memory.

The increment instruction, if it runs, changes the {{< lookup/cref CPUTYPE >}} value in DX (which also affects DL in the same way) from `CPUTYPE_8088` to `CPUTYPE_8086`, from `CPUTYPE_V20` to `CPUTYPE_V30`, or from `CPUTYPE_80188` to `CPUTYPE_80186` depending on what the value already was. The `nop` instructions are no-ops used for padding, `cld` restores the direction flag setting, and any number of `sti` instructions turn interrupts back on.

The CPU type has been uniquely determined. From here, execution falls through to the cleanup and return code.

### Cleanup

The job is almost done now.

```tasm
@@done:
        ; Restore the FLAGS register back to the state it was in when the
        ; procedure was first entered.
        popf

        ; Zero the high byte of DX, then copy the result into AX. This is the
        ; procedure's final return value.
        xor   dh,dh
        mov   ax,dx

        pop   di
        pop   si
        pop   ds
        pop   bp
        ret
ENDP
```

No matter which processor was detected, execution enters this section of the code. `popf` restores the FLAGS register to the state it was in when the procedure was first entered. This renders earlier efforts to restore things like the direction flag and the interrupt flag moot -- all of those are restored by this instruction.

Next, the running value in DL/DX is prepared for return. The code treats DL a little loosely, sometimes referring to it specifically and other times changing it through DX. The `xor dh,dh` zeros out the high bits in DX, leaving the low bits intact. The resulting value is copied into AX, which is where the C calling convention requires integer return values to be placed.

Finally, the values for DI, SI, DS, and BP are restored. This unwinds the local stack frame in the reverse order from how it was created at the beginning of the procedure. Control returns to the caller via `ret`.

### Return Value

See {{< lookup/cref name="CPUTYPE" text="CPUTYPE_*" >}}.

## Authorship

The tests documented here are clever, and no doubt the result of countless hours of research on the part of the original authors. Testing such code requires access to a wide variety of different PCs, which was not a cheap undertaking in the 1980s. It's worth trying to properly attribute the source of these tests.

* Certain ideas and descriptions of formal behaviors came directly from the Intel Programmer's Reference manuals.

* A great deal of research was done by **Bob Smith**, in an article titled "Chips in Transition" in PC Tech Journal.[^smith]

* **Robert de Bath** contributed some novel extensions to the basic ideas presented here in a utility script[^debath] provided with the Dev86 project.

* A different form of the 286/386 tests was released by an unknown author, in an assembly code fragment titled "Chips",[^chips] where another author named **Clif Purkiser** is mentioned as creating some techniques.

* A 386/not 386 test is credited in passing to **Juan Jimenez** in files JABHACK.ASM and WL_ASM.ASM from both the Wolfenstein 3D[^wolf3d] and Catacomb 3-D[^catacomb3d] source releases. The code was likely adapted, based solely on the initials "JAB", by **Jason Blochowiak**.

This code, however, directly matches the structure and implementation choices used in PROCCA.ASM from a book titled "PC System Programming for Developers" by **Michael Tischer**, chapter 15. Regardless of who discovered each test, this implementation was taken verbatim from Tischer's book.

[^smith]: "Chips in Transition" by Bob Smith, PC Tech Journal Vol. 4 No. 4, April 1986. https://archive.org/details/PC_Tech_Journal_vol04_n04/page/n57/mode/2up
[^debath]: https://github.com/jbruchon/dev86/blob/master/libc/misc/cputype.c
[^chips]: https://code.michu-it.com/michael/programming-examples/src/branch/master/assembly/Chips.asm
[^wolf3d]: https://github.com/id-Software/wolf3d
[^catacomb3d]: https://github.com/CatacombGames/Catacomb3D
