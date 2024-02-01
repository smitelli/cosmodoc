+++
title = "Welcome to Cosmodoc!"
weight = 10

[sitemap]
priority = 1
+++

# Welcome to Cosmodoc!

_Cosmo's Cosmic Adventure_ is a DOS video game published by Apogee Software Productions in March 1992. It was programmed by Todd J. Replogle with art by Stephen A. Hornback.

My name is Scott, and I wrote roughly 207,000 words (and counting) about how this game worked.

The pages of this website cover all aspects of the game, from data files to drawing routines and everything in between, with occasional forays into the computer hardware and software contemporary to the era. The information presented here is the result of months of research and reverse-engineering effort. I hope you find it enlightening, or at the very least somewhat interesting.

The [Topics]({{< relref "topics" >}}) page contains the master index of all the pages. The navigation menu on each page contains the same links for easy access. If you're looking for suggestions, check out a few of the pages I'm proudest of:

* **Hardware:** [AdLib]({{< relref "adlib-functions" >}}), [EGA]({{< relref "ega-functions" >}}), [Keyboard]({{< relref "keyboard-functions" >}}), [Joystick]({{< relref "joystick-functions" >}}), [PC Speaker/Timer]({{< relref "pc-speaker-and-timing-functions" >}}).
* **System programming:** [The IBM PC]({{< relref "ibm-pc" >}}), [B800 Text Display]({{< relref "b800-text-format" >}}), [LZEXE]({{< relref "lzexe" >}}), [Low-Level Drawing]({{< relref "assembly-drawing-functions" >}}), [Processor Detection]({{< relref "processor-detection" >}}).

The code fragments in these pages is based on my reconstruction of the game's source code, [**Cosmore**](https://github.com/smitelli/cosmore). The Cosmore project can be built using Borland Turbo C and Turbo Assembler to create an almost-identical executable file for all three episodes of the game, in the same way the original creators likely did it.
