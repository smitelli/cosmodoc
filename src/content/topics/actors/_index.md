+++
title = "Actors"
description = "Moving objects on the map that the player can pick up, damage, or otherwise interact with."
weight = 460

[sitemap]
priority = 1
+++

# Actors

The game's **actors** are fully independent objects inhabiting the map that can exhibit any kind of movement and player interaction. Compared to [entities]({{< relref "entities" >}}), which have very constrained and specific behavior, actors can be implemented to do anything the game requires. Everything the player needs to pick up or destroy is an actor, and most of the injuries the player can suffer result from interaction with actors.

From the standpoint of function counts, there are between 60 and 70 different actors in the game. When considering the different actor subtypes that share common implementations, there are over 240 of them.
