+++
title = "Actor Sprite Database"
linkTitle = "Actor Sprites"
description = "A table containing information about each actor sprite set in the game."
weight = 730
+++

# Actor Sprite Database

Actor sprite graphics are also used in decorations, spawners, and shards. Each actor sprite set contains between one and fifteen frames. Each frame can have a different size if needed.

"Unused" sprite sets are those that are never directly mentioned in the game, and which hold references to graphics data that is used in different sprites' sets. These references do not occupy space in the game files themselves (aside from the 10-122 bytes each entry occupies in ACTRINFO.MNI).

A few sprites are noted as containing "identical data," which is an instance where two different sprite frames point to two different offsets in ACTORS.MNI but both read the same data. The redundant graphics data could have been removed, and the offsets fixed up, without visibly affecting anything other than group file size.

{{< data-table/actor-sprite >}}
