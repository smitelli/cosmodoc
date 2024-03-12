+++
title = "Map Database"
linkTitle = "Maps"
description = "A table containing the parsed header data from each map file of the game."
weight = 630
+++

# Map Database

This page contains extracted header data from every map included in the game.

All maps contain exactly one {{< lookup/special-actor 0 >}}, and exactly 65,528 bytes of tile data. The {{< lookup/special-actor 0 >}}, {{< lookup/special-actor 1 >}}, {{< lookup/special-actor type=2 strip=true >}}, and {{< lookup/special-actor type=7 strip=true >}} actor types are included in the "Actors" column counts but are not included in the in-game Memory Usage "Total Actors" count.

The "Actors" count for map A8 includes two invalid entries that the game silently ignores.

{{< data-table/map >}}
