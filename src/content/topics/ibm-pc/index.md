+++
title = "The IBM PC"
description = "To fully understand the game, one must understand the system it was designed to run on."
weight = 50
+++

# The IBM PC

The original IBM Personal Computer Model 5150 (**IBM PC**) was released in September 1981. In many respects, the PC was cobbled together from common off-the-shelf components: a processor and chipset from Intel, various memory and glue chips (sourced from Advanced Micro Devices, Motorola, Texas Instruments, Fairchild Semiconductor, etc.), and a smattering of run-of-the-mill support parts from whichever manufacturers had adequate supply at a good price. The design specifications were thorough and, somewhat surprisingly, open to anybody who cared to request them.

If you wired the correct components together in the correct way, you'd end up with a machine that could run the same software, in the same way, as a real IBM PC. The PC's BIOS software was built to an open specification as well, making it feasible and even practical to build such a machine and get it to run useful programs. (This is what led to the explosion in the "PC clone" industry that followed.) Since the design of the hardware and the BIOS had such a profound impact on the way the machine behaved and the way software needed to be written to run on it, the techniques, idioms, limitations and quirks became ingrained in the minds of anybody who programmed for the platform.

Practically speaking, some of the components and their long-term ramifications were:

* **The Intel 8088 Microprocessor:** Selected the instruction set, 16-bit machine word size, and the rather unfortunate segmented memory model and addressing limitations. Conceptually identical to the 8086, but cheaper and slower to move data in and out.
* **The Intel 8259 Programmable Interrupt Controller:** Defined the various interrupt requests (IRQs) and the protocols for how they should be handled.
* **The Intel 8237 Programmable DMA Controller:** Specified the number of DMA channels, the protocol for interacting with them, and the assignment of physical devices to channel numbers.
* **The Intel 8253 Programmable Interval Timer:** Set the original 18.2 Hz system timer rate, as well as the methods to configure it. Due to an interesting case of dual-purposing a component, also established the method for playing beeps through the internal speaker.

These hardware decisions influenced the design of the BIOS, memory and I/O maps and, eventually, the operating systems and software that ran on top of it all.

The IBM PC went through further evolutionary stages, first with the **XT** in 1983 and then with the **AT** in 1984. Each revision brought new features and improved performance, but maintained complete compatibility with the machines that came before. To this day, personal computers support some degree of backwards compatibility with the original design decisions of the PC.

Cosmo's Cosmic Adventure required an IBM AT computer primarily due to its reliance on some processor instructions that were introduced to the PC with the Intel 80286,[^80186] as well as its raw speed. This page (and the bulk of this site) in written from the perspective of an IBM AT computer, but most of the information is applicable to the original PC, as well as personal computers many generations newer.

## The Intel 80286

When Intel released the 80286 in 1982, and IBM first shipped one in the AT in 1984, one of the most significant changes over its predecessors was the addition of what was called **protected mode**. DOS didn't use it, nor did a lot of software of the era. Without protected mode and the capabilities it brought, the 80286 was really nothing more than a faster 8088 that supported a couple of shorthand notations for code that had numbers in it. (Yes, it also bumped the maximum amount of physical memory from 1 MiB to 16 MiB, but not in a particularly pleasant way.) All the processors models that end in -86 are similar enough that they're often collectively referred to as the **x86** family, and an x86 processor running in non-protected mode is said to be running in **real mode**.

The 80286 was a 16-bit processor, exactly like the 8086 and 8088 that came before it. What this means is that the native size of the data units that the processor operates on is sixteen binary digits -- sixteen of those little ones and zeros that all digital circuits breathe. If you take sixteen digits, each of which can be either 0 or 1, there is a total of 2<sup>16</sup> -- or 65,536 -- different numbers that you can express. If you don't care about negative numbers, the number range is 0 to 65,535. If you do care about negative numbers, the range shifts from -32,768 to +32,767.

In general, any number that a 16-bit processor touches has to fit inside the ranges above. Obviously this presents a problem if you're trying to compute astronomical distances, or the population of most countries, or the purchase price of a well-equipped Mercedes. To compute numbers at that scale, the program (not the processor) has to split the computation up into pieces which each individually fit inside a 16-bit storage slot (called a **register** in processor parlance) and work on the problem piecewise.[^mul] It's not as simple or as fast as working on a single value with a single instruction, but it does allow arbitrarily large numbers to be computed.

The x86 memory model is byte-addressable, meaning each individual memory byte (which is a grouping of eight bits) has a distinct numeric address and can be manipulated in isolation. This, paired with the 16-bit nature of the processor, means that only 65,536 bytes -- 64 KiB! -- of memory can be addressed in total. 64 KiB isn't a whole heck of a lot, and solving that issue is a bit more convoluted.

## The 16-Bit Memory Model

Even in the early 1980s, it was not uncommon for computers to have hundreds of kilobytes of memory installed. Limiting the amount of usable memory in the system to only 64 KiB was simply unconscionable.

To work around the problem (and to flummox programmers for decades afterwards), x86 processors running in real mode use **memory segmentation**. Rather than have a single 16-bit numeric address which refers directly to a specific byte in the computer's memory, there are two values, a **segment** and an **offset**, that must be taken together to determine the true physical address in memory. Since the segment is 16 bits, and the offset is 16 bits, one might assume the number of addressable memory bytes would be 2<sup>(16 + 16)</sup> -- hey, four gigabytes! But no, that's not quite how it works.

The 8086 and 8088 have a 20-bit address bus, meaning there are 20 separate pins on the chip and 20 separate vias that connect the processor to the memory circuitry. This means the chip can't physically differentiate any more than 2<sup>20</sup> bytes -- 1 MiB -- of memory. 20 is a weird number, too large to fit into 16 bits but too small to effectively fill 32, so there is waste. Rather than requiring the highest 12 bits to be zero and only assigning significance to the lower 20, the designers arranged it so that every bit meant something in the calculation.

A segment is a contiguous block of sixteen bytes. An offset is a number of bytes to add to the result. Memory addresses are usually written as _segment:offset_ using hexadecimal numbers. To compute the physical address of `1234:5678` the procedure is:

     Segment       Offset  Physical Address
     |             |       |
     V             V       V
    (1234h * 16) + 5678h = 179B8h

or 96,696 bytes in decimal. It's a relatively straightforward concept until it becomes apparent that `179B:0008` works out to:

    (179Bh * 16) + 0008h = 179B8h

or 96,696 again. The lower 12 bits of the segment affect the same things that the upper 12 bits of the offset do. For every byte of physically addressable memory in the system, there are up to 4,096 different segment:offset pairs that will refer to it.

To further complicate things, it's entirely possible to construct an address that won't fit in the 20-bit address space. Consider `FF00:1000`:

    (FF00h * 16) + 1000h = 100000h

That's a problem. 10 000h requires 21 bits to express, but there are only 20 address lines. The processor's solution is elegant and brutal: strip off the 21st bit, leaving 0000h. `FF00:1000` "wraps around" to point to the very first byte of memory.

When the 80286 came around and increased the number of address lines from 20 to 24, it granted the system the ability to address 16 MiB (2<sup>24</sup>) of memory in total. On these systems, the physical address 10 000h could actually point to a real spot in high memory without wrapping back around to zero. But since a significant amount of software existed in the wild that relied on the wraparound behavior being present, this couldn't be enabled by default. This gave rise to a number of familiar user-installable options in the DOS world, including HIMEM.SYS, the A20 handler, and the `DOS=HIGH` CONFIG.SYS directive, all of which enable use of this extra space and allow moving DOS itself to reside there to free up conventional memory for programs.

Past `FFFF:FFFF`, or just about 1,088 KiB of memory, there is no way to construct a valid 16-bit segment:offset pair. For addresses that high, software must negotiate with the operating system and/or motherboard hardware to perform bank-switching, where blocks of inaccessible memory are mapped onto lower addresses that can be accessed. There were several competing methods to do this, but luckily the game didn't use any of them. That relieves us of the responsibility of needing to discuss or understand them.

## Input/Output

It's great to have a processor that can execute programs and memory that can store programs and data, but they don't amount to much if there's no way to get any of that in and out of the system. The PC supported two general techniques to perform programmed input and output (**I/O**), plus a third sort of "hybrid" technique that bypassed the CPU almost entirely.

### Memory-Mapped I/O

This was the most straightforward technique from the perspective of a program. Within the 1 MiB of memory address space the processor supported, IBM's specifications set aside certain address ranges for communication with external devices. When data was read or written at these addresses, circuitry outside the processor would redirect the request to some other piece of hardware instead of the system's memory.

The memory layout of the PC reserved the addresses from `A000:0000` to `FFFF:000F` (a region totaling 384 KiB) for this memory-mapped I/O. This range included a mix of read-only BIOS code, writable video memory, and space to communicate with whatever additional hardware happened to be installed in the machine. The processor could read and write data here as if it were regular memory, but the system's hardware could do things in response.

As a consequence of the reserved area, addresses within its range could not be used to address any system memory, meaning the usable range for programs and data was `0000:0000` to `9FFF:000F` -- 640 KiB. DOS called this **conventional memory**, and it was always in short supply.[^640k]

### Port-Mapped I/O

x86 processors support a pair of instructions called `OUT` and `IN` which move data to/from a **port**.[^port] There are 65,536 ports available, and they are usually written as hexadecimal numbers from 0000h to FFFFh. Port numbers work like memory addresses, and even share the same physical address lines that memory addressing operations use. The processor differentiates port addresses from memory addresses by signaling on a separate status pin; this informs the other components on the motherboard that communication should happen over the I/O bus instead of the memory bus.

Using I/O ports, it is possible to transmit either a single byte or a single 16-bit word between a processor register and an external device. Since the throughput is not very high, such communication is usually used for small, relatively infrequent events -- reading a single keystroke from the keyboard, joystick polling, activating the PC speaker, sending a musical note to the AdLib...

### Direct Memory Access

This is a high-performance hybrid of the two previous approaches, designed to offload the effort required to simply copy large chunks of data from one place to another.

In a regular memory- or port-mapped I/O scenario, the act of moving a large block of data from system memory to mapped memory (or an I/O port) involves having the processor read a small piece of the system memory into a 16-bit register, write the contents of the register to the mapped memory (or I/O port), and then repeat those steps until the entire block is copied. The processor is perfectly capable of doing the job, but there is a great deal of overhead to perform such a menial task.

Direct Memory Access (DMA) involves a separate dedicated mini-processor whose sole job is to control memory and copy data to/from it. To copy the same data using DMA, the processor emits a few setup commands to the DMA controller's I/O port, relinquishes control of the memory address and data lines, and the DMA controller takes control of the memory to copy the data -- up to 64 KiB in a single shot. Since a dedicated piece of hardware is doing the work, it can be performed much faster.

DMA is usually used for high-bandwidth data copy operations, like reading from a disk drive or sending digital sound effects to a Sound Blaster or equivalent. The implementation in the PC was a bit of an ugly hack, and the game doesn't directly use DMA, so it won't be discussed in further detail.

## Interrupts

Our basic journey through the PC's low-level architecture is almost complete, except for one small detail: When the user presses a key on the keyboard, how does the program know to respond to that event?

We can take educated guesses about what happens in that situation. Perhaps the keyboard controller flips a byte in a memory-mapped area somewhere? Maybe it stores the keypress in a temporary buffer and makes it available on an I/O port whenever the program is ready to receive it?

The problem with these so-called **polling** approaches is that they require active participation from every program at all times. No matter what a program is doing, it must remember to occasionally stop, communicate with the keyboard hardware to see if any keypresses have come in, and react to them if so. If the program gets busy or forgets to check, the keyboard goes unserviced. And that's just one piece of hardware. Add to that the system timer, real time clock, mouse movement, disk drives and peripheral ports... the list of things that need to be checked grows out of control. To make matters worse, there can be occasions when these checks are downright useless if the hardware has nothing new to report since the last time it was polled.

The solution is **interrupts**. At the processor level, an interrupt is a special event that causes the flow of program execution to be suspended, followed by an unconditional jump to a different section of code called an **interrupt service routine**. The service routine does whatever it needs to do to adequately respond to the event, and then it signals a **return**. The return causes execution to jump right back to where it was before the interrupt was received, and the original program continues as if nothing had happened. To the interrupted program, there is no direct evidence that any interrupts occurred -- that is, assuming the service routine was well-behaved and cleaned up after itself.

Real-mode x86 supports 256 different **interrupt vectors**. The very first 1,024 bytes of system memory hold the **interrupt vector table**, which is a list of **pointers** to service routine addresses in segment:offset form that the processor should jump to when it receives each interrupt vector. (The pointer for interrupt vector 0 is at memory location `0000:0000`, interrupt 1 is at `0000:0004`, interrupt 2 is at `0000:0008`, and so on up to interrupt vector 255.) This table can be modified by software running on the machine to change which code is executed in response to different interrupt vectors.

Interrupts can occur as a result of internal software events (such as a program intentionally executing an `INT` instruction or performing some illegal computation such as dividing a number by zero), or from external signals received by the processor on its interrupt pins. External interrupts are all routed through a pair of Intel 8259A interrupt controllers, with each controller having eight input pins: one for each interrupt request, or **IRQ**, line. The first interrupt controller handles IRQ0 through IRQ7 (which are presented to the processor as interrupt vectors 08h through 0Fh) and the second interrupt controller handles IRQ8 through IRQ15 (presented to the processor as interrupt vectors 70h through 77h).[^pics] It's technically possible to reprogram the interrupt controllers to transmit different interrupt vectors to the processor for a given IRQ signal, but there doesn't seem to be many legitimate reasons to try to do that.

It's important to remember that interrupt vectors and IRQs are tightly related to one another, but not exactly the same thing.

When an interrupt controller receives a signal on one of its IRQ lines, it applies a signal to the processor's "interrupt" line. The processor stops, signals back to the interrupt controller on the "interrupt acknowledge" line, and the interrupt controller places the appropriate interrupt vector number onto the system's data bus. The processor, reading that number from the bus, looks up the corresponding entry in the interrupt vector table and starts executing the interrupt service routine code that it points to. Before returning, the service routine must issue a signal to the interrupt controller's I/O port that the event was handled, otherwise that IRQ will not trigger correctly next time.

The processor interrupt vectors 0-7 were defined by Intel, and IRQs 0-15 (and their corresponding interrupt vectors) were defined by the IBM PC specification, to refer to very specific events. Service routines needed to be carefully written to perform the correct actions to fully service whatever caused the interrupt, _without_ destabilizing whatever the machine was doing before the interrupt occurred.

Most of the remaining processor interrupt vectors were either reserved for future use, or used to define the application programming interface (**API**) for programs to communicate with BIOS and the operating system.

## BIOS

The IBM PC's Basic Input/Output System (**BIOS**) is a relatively small (on the order of tens of kilobytes) block of code and data that was permanently "burned" into a read-only chip on the motherboard. This chip's contents are exposed in the upper memory area, usually somewhere in the address range `F000:0000` to `FFFF:000F`. When the PC is first powered on from a cold state, the processor unconditionally starts executing whatever it finds at memory address `FFFF:0000` -- sixteen bytes before the very end of the BIOS area. The processor doesn't know or care what is actually at that address; it just has to execute correctly. Most BIOS code has an "unconditional jump" instruction at that address, which moves execution somewhere else in the BIOS area with a little more room to work.

The BIOS in the IBM PC was _primitive_. There was no "Press F2 to run SETUP"-type prompt, nor any built-in utilities to configure or test the machine. To configure the battery-backed CMOS settings for the BIOS, the system needed to boot from a special IBM diagnostics floppy disk.

{{< aside >}}
**Think about that.**

The fact that the IBM PC, with a dead CMOS battery and default BIOS settings, could boot from a floppy disk and run an interactive setup program was a testament to just how little variation there was in the core hardware of these systems. The BIOS could simply assume that there was a floppy disk drive at a certain I/O address, a keyboard over there, and a usable display adapter at this hard-coded location, and it all _just worked_.
{{< /aside >}}

The primary job of the BIOS is to configure all of the system's hardware into a baseline usable state. Most of the chips on the motherboard are named "Programmable Something-or-Other," and the BIOS is responsible for actually programming them to behave in a PC-like way. The BIOS is also responsible for interrogating the hardware to determine what options the specific computer has -- anyone who has watched one of these start up is well aware that the BIOS counts all of the installed memory each time it boots, so it can provide an accurate number to any programs that may ask for it.

The BIOS' final start-up job is to read the boot sector into memory from the most appropriate disk it can find, and unconditionally jump into it. From there, the operating system on the disk takes over.

Once the computer is under the operating system's control, the BIOS lays mostly dormant. However, many interrupt vectors point into BIOS functions, meaning that any number of software- and hardware-generated interrupts can cause BIOS code to execute and perform some system-level function. (Things like reconfiguring the video hardware, maintaining the time of day, interacting with disk drives, etc.)

## DOS

While not strictly part of the IBM PC's architecture, Microsoft's Disk Operating System (**MS-DOS** or simply **DOS**) is entrenched enough to warrant a brief discussion. Most IBM PCs doing any sort of useful work ran DOS. (Some other operating systems were available, and the PC could also run the BASIC programming language from a built-in ROM chip without an operating system present.) IBM tended to ship a version of DOS called "IBM PC DOS" that was for the most part just MS-DOS with the names and copyright messages changed.

{{< aside class="fun-fact" >}}
**Live long and prosper.**

Development of MS-DOS and PC DOS eventually diverged, with the two products competing with one another for a time. MS-DOS survived until version 8.0 in September 2000, while PC DOS version 7.1 saw minor incremental updates until the end of 2003.
{{< /aside >}}

From a user's direct interactions with DOS, it was straightforward to see it as a platform to install and execute programs, manage files, and control the computer's hardware on a high level. When some people referred to the PC or "PC compatible" systems, what they actually meant was "something that ran DOS and DOS-based programs correctly."

The programs that ran on the computer utilized DOS too, but in a much different way. DOS exposed an API that programs could use to access services such as memory allocation, input/output for the keyboard/screen/printer, listing/manipulating files, interacting with the real-time clock, and many other esoteric things. The original DOS API was based on (and designed to be compatible with) the API for an operating system from the 1970s called CP/M. Later revisions of the DOS API incorporated some ideas from the Unix world.

Programs invoked the DOS API by issuing an interrupt with a vector between 20h and 2Fh. The majority of the DOS API is housed within interrupt 21h, with about 100 different subfunctions available as of DOS version 4.0. The program would select the subfunction by writing the subfunction number into the processor's AH register (possibly alongside other arguments in different registers) immediately before issuing interrupt 21h. DOS would store the results, whatever they may be, in various registers before its interrupt service routine returned.

It was not strictly necessary to use the DOS API to accomplish some tasks, because the same thing could be accomplished (sometimes a little more efficiently) by going around DOS' back and calling the BIOS API directly. Sometimes it was necessary for a program to directly issue I/O requests and bypass the DOS/BIOS APIs completely, either because no API function existed to perform the task, or because performance was critical. Games did this a lot, and it produced some truly magical stuff.

DOS had a huge impact on the PC, and a permanent one at that. Many idioms and limitations of DOS survive well into this millennium. (For example: using `C:` as the primary hard drive letter, backslash as a path separator, and the inability to name files using "special" names/characters like `NUL`, `CON` and `?`.)

[^80186]: Technically, the necessary instructions were added in the Intel 80186, but that processor never shipped in an IBM PC.

[^mul]: A select few instructions, like `MUL`, could operate on two 16-bit operands and produce a 32-bit result which was stored across two 16-bit registers. These instructions were relatively rare (and slow)!

[^640k]: There is a quote, often attributed to Bill Gates, that goes "640 K ought to be enough for anybody." In all likelihood he never actually said that; the quote was probably the invention of some wisenheimer on Usenet.

[^port]: The word "port" is a very overloaded term in the computing world. These I/O ports have absolutely nothing to do with networking protocols like TCP or UDP, and they have no direct correlation with the physical ports on the back of the machine (although, confusingly, sending data to a port on the back of the machine usually involves communication over an I/O port to get the data moving).

[^pics]: This is an intentional simplification. In reality the two interrupt controllers in the IBM AT are chained in a rather unfortunately named master-slave configuration, with all interrupts from the slave arriving as IRQ2 on the master. To maintain compatibility with the original IBM PC and XT, where IRQ2 was not cascaded in this way, the system uses IRQ9 to emulate the original behavior.
