+++
title = "Entities"
description = "Moving objects that inhabit the map, but are not implemented as actors."
weight = 440

[sitemap]
priority = 1
+++

# Entities

An **entity** is any object, moving or stationary, that inhabits the map but does not use the actor system. There are five kinds of entity in the game.

## Platforms and Mud Fountains

The [**platforms** and **mud fountains**]({{< relref "platform-functions" >}}) are moving surfaces that the player (and other actors) can stand on and use for transport around the map. Platforms (but not fountains) may need to be activated by using a {{< lookup/actor type=59 strip=true >}}.

These entities are inserted by a map author and follow rigidly defined paths.

## Explosions

An **explosion** (or series of explosions) are typically created when player-placed bombs explode. Explosions can damage map actors as well as the player.

In addition to bombs, explosions can occur from {{< lookup/actor type=50 strip=true plural=true >}}, {{< lookup/actor type=90 plural=true >}}, {{< lookup/actor type=130 plural=true >}}, and  {{< lookup/actor type=188 plural=true >}}.

## Spawners

A **spawner** is a precursor to an actor that is being spawned into existence. When the player destroys a barrel, for example, the barrel releases a spawner that flies up some distance into the air. Once the spawner reaches its maximum height, it is replaced by a full actor of the same type which falls back to the ground using the actor system's sense of gravity.

Both good things (like prizes from barrels) and bad things (like {{< lookup/actor type=86 plural=true >}} from {{< lookup/actor type=152 plural=true >}}) are added to the map using the spawner system.

## Decorations

**Decorations** are simple sprites or sprite sequences that appear either stationary or move in a fixed direction. Decorations do not test for intersection with map tiles -- they either run until their animations end or until they scroll off the edge of the screen.

The vast majority of decorations in the game are either sparkles or rising smoke plumes, but a few other activities generate decorations of different styles.

## Shards

Groups of **shards** are generated when certain actor types are destroyed. Each shard is either a complete sprite or a fragment of a sprite, which bounces away from the point of creation. After a limited number of bounces, each shard is absorbed into the floor before disappearing.
