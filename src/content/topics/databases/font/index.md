+++
title = "Font Database"
linkTitle = "Font"
description = "A table listing every glyph in the game font."
weight = 580
+++

# Font Database

The game font consists of 100 **glyphs**, which are tile images that visually represent letters or other symbols. The font codes bear some semblance to the standard ASCII table with a few sections removed and rearranged. The `/` glyph was replaced with the symbol for the pound sterling (&pound;) to facilitate displaying the game's price in the "Foreign Orders" screens.

For each row in the table, an equivalent C character is shown that can produce each glyph on the screen. Most of the printable ones match (the character entered in code is the character that displays), but symbols and custom elements have differences from standard ASCII/CP437 encodings.

The status health bars are also stored here, with each bar comprised of two glyphs (one for the upper half, and one for the lower).

{{< data-table/font >}}
