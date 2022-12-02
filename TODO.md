* Keep page title at the top of nav scroll
* Eventually will be more than semi-complete
* Word count
* Finish describing the bugs
* Appendix/glossary
* Unused tiles and masktile

=============================================================================

* status bar
    * mention format of status.mni
    * PlayerScore: defines position, UpdateStatusScore: GIVES POINTS. for each display page, place score line at XY.
    * PlayerStars: defines position, UpdateStatusStars: for each display page, place stars line at XY.
    * PlayerBombs: defines position, UpdateStatusBombs: for each display page, draw a font char, then place bombs line at XY.
    * PlayerHealth: calls IPH for each display page, InnerPlayerHealth: defines position, UpdateStatusHealth: draw health bars, two lines high.
    * InitializeGameWindow: calls DGW for each display page, DrawGameWindow: clear screen, draw status bar BG, call score/stars/bombs/health.

* game setup
    * GameRand: predictable PRNG
    * GameKeysAndMenu: does something goofy with the pages and calls ReadGameKeys
    * NextLevel: determine next level to play, optionally with star bonus tally.
    * GameLoop: runs once per frame.
    * LoadLevel: given level number, open groupent file. read flags. init player. load BD, map data. "now entering level." init game. so on and so forth.
    * InitializeGameState: reset player-specific game stuff for brand new game.
    * GiveScore: given an actor type, add a certain amount to player's score.
* map management
    * SetMapBlockRepeat: SetMapBlock to one value, repeated arbitrarily many times.
    * SetMapBlock4: set 4 consecutive map blocks to 4 different values.
    * GetMapBlock: get one map block.
    * SetMapBlock: set one map block.
    * AddMapActor: handle player start, platforms, fountains, lights. if none of those, dispatch to CreateActorAtIndex.
    * LoadMapData: given a level number, open the groupent file containing the map, set the width, add actors, and fill the map data block. initialize the platform saved blocks, and finally set current level and height.
    * MAP_BLOCK_ADDR: XY to linear address.
    * TILEATTR_BlockSouth
    * TILEATTR_BlockNorth
    * TILEATTR_BlockWest
    * TILEATTR_BlockEast
    * TILEATTR_Slippery
    * TILEATTR_InFront
    * TILEATTR_Sloped
    * TILEATTR_CanCling
* level display
    * DrawBackdropLayer: does more than you think!
    * DrawRandomEffects: make slippery tiles sparkle sometimes. spawn raindrops if warranted.
* player move
    * ReadGameKeys: handle the large majority of the game's input/cheats.
    * InitializePlayerState: reset more esoteric player vars, mostly to zero.
    * ResetPlayerHeadShake: stop player's head from shaking.
    * TestPlayerMove: determine if the player can move in a given direction, and set a bunch of global vars in the process.
    * HurtPlayer: ouch bubble, decrement health, maybe kill the player.
    * ResetPush: reset push-related vars.
    * SetPush: set up a push.
    * PushPlayer: handle one tick of player push movement.
    * MovePlayer: handle one tick of basically all player input.
    * MovePlayerScooter: handle one tick of player movement on the scooter.
    * ShakePlayerHead: handle landing on the ground and maybe shaking head.
* player display
    * DrawPlayerSprite: player sprite control, with some checks for the various ways to die.
* player/actor
    * TestPlayerHit: return true if actor type/frame/XY is touching the player
    * PounceHelper: imparts the springiness into actor pounces.
    * PlayerActorTouch: perform actions when a player and an actor touch. this goes both ways (player hurts actor, actor hurts player.)

* backdrop
    * InitializeBackdropTable: i have no earthly idea.
    * LoadBackdrop: open groupent by name, install to video memory via scratch space. calls other functions i don't yet understand.
    * InstallBackdropVert: i have no earthly idea.
    * InstallBackdropHoriz: i have no earthly idea.
    * IsBackdropChanged: did any pertinent info regarding the backdrop change?

* platforms/fountains
    * ProcessAllPlatforms: for all platforms -- remove platform from map, conditionally call PPT, move platform, reinsert platform into map
    * PlayerPlatformTouch: handle player riding platform, including scrolling the screen.
    * ProcessAllFountains: for all fountains -- sleep, change direction if needed. remove fountain head from map. conditionally call PPT. change height. reinsert fountain head into map.
    * DrawFountains: for all fountains -- draw fountain head. for each unit of height, draw fountain stream. if player is touching any part of the stream, hurt them.
* lights
    * DrawLights: for each light: draw correct shape for topmost tile. cast down from there, drawing solid light. stop after hitting a solid block, or max distance reached. do not draw off screen.
* shards
    * ResetShards: deactivate every shard in the array.
    * InsertShard: assign shard number 0-4, then insert into next free spot in array.
    * ProcessAllShards: move/bounce each shard, playing sounds, and drawing them.
* explosions
    * ResetExplosions: deactivate every explosion in the array.
    * InsertExplosion: insert explosion into next free spot in array. play sound.
    * ProcessAllExplosions: for each explosion -- if ep3, conditionally animate the palette. draw sparkle on first frame. place the explosion frame, hurt the player if too close. once animation has run, emit smoke and make that slot go idle.
    * IsExplosionTouchingActor: returns true if any explosion is close to the specified actor type/frame/XY.
    * ActorExplosionTouch: given actor type/frame/XY, handles explosion damage. Usually gives points/shards, or is a no-op. hint globes and eye plants have special code here. returns true if the explosion had an effect.
* spawners
    * ResetSpawners: deactivate every spawner in the array.
    * InsertSpawner: insert spawner into next free spot in array.
    * ProcessAllSpawners: for all spawners -- move up. if recently spawned, move up faster. if something is hit, or spawner ages out, go inactive and spawn a real actor at that position. otherwise draw spawning sprite.
* decorations
    * ResetDecorations: deactivate every decoration in the array.
    * InsertDecoration: insert decoration into next free spot in array.
    * ProcessAllDecorations: for each decoration -- draw at XY (sparkles are always in-front, rain moves faster and with randomness). move decoration according to given dir. handle cycling animation, and loop limit. once it's looped enough, go inactive.
    * PounceDecoration: insert six decoration spores in all directions.
* actors
    * CreateActor: set all members of actor slot specified by actorIndexCursor. does not change cursor in any way.
    * CreateActorAtIndex: sets actorIndexCursor, calls CA based on actor type.
    * InsertActor: looks for dead actor slot, then calls CAAI to install new actor there. if no dead actors in used area, call CAAI at the first free slot.
    * SetMovementState: fudge actor XY based on planned move direction. set word10/12 to indicate available space to move to.
    * ProcessAllActors: for each actor -- call PA. also clears global hint globe/question mark state.
    * ProcessActor: one actor -- handle falling off the map. decrement pounce cooldown. determine if actor is onscreen/should activate. if affected by gravity, apply it. think. if hit by explosion, die. unless something special occurred, call draw fn.
    * AreActorsTouching: given two actor defs, determine if they are touching.
    * IsActorVisible: given one actor def, determine if it is in the screen area.
    * TestActorMove: can an actor def move in the requested direction?
    * thinkers
        * ActFootSwitch: used for 4 real switches. all other references are no-op.
        * ActHorizontalMover: big saw blade, robotic spike
        * ActFloorSpring: floor/ceiling spring
        * ActArrowPiston: E/W variants
        * ActFireBallLauncher: E/W variants
        * ActHeadSwitch, ActHeadSwitchInner, ActDoor: 4 colors
        * ActCartSpring
        * ActRetractingSpikes: in ground or W wall
        * ActVerticalMover: big saw blade
        * ActArmedBomb
        * ActBarrel, DestroyBarrel: barrels and baskets, different type depending on contents
        * ActCabbageBall: 2 types, be careful!
        * ActCeilingSpear
        * ActDrips: leaking/dripping red/green acid
        * ActHailSprite
        * ActTwoTons
        * ActJumpingBullet
        * ActStoneHead
        * ActPyramidSpike: falling ceiling or fixed floor. (fixed ceiling is different!)
        * ActGhost
        * ActFloatingMoon
        * ActRedHeartPlant
        * ActBomb
        * ActQuestionMark
        * ActBabyGhost
        * ActFlashingProjectile: 5 types, depending on direction
        * ActTreasureWorm
        * ActPipeDirection, ActPipeEnd: four directions, two ends
        * ActBabyGhostEgg: two types
        * ActCeilingRobot
        * ActClamPlant: floor/ceiling variants
        * ActBlueBall
        * ActVerticalArcRobot
        * ActSplittingPlatform
        * ActSpark
        * ActEyePlant: floor/ceiling variants
        * ActRedJumper
        * ActBoss
        * ActSuctionCupWalker, SuctionCupWalkerCanFlip
        * ActTransporter: three types
        * ActSpittingWallPlant: E/W variants
        * ActSpittingTurret
        * ActScooter
        * ActRedChomper
        * ActForceField: H/V variants
        * ActPinkWorm, ActPinkWormGoo
        * ActHintGlobe: 26 of them
        * ActPusherRobot
        * ActSecurityRobot
        * ActDragonfly
        * ActPinkWormBox
        * ActSatellite
        * ActIvyPlant
        * ActExitJaws, ActExitLineVertical, ActExitLineHorizontal, ActEpisode1EndTrigger, ActExitFlytrap: horiz exit has two variants
        * ActSmallFlame
        * ActPrize: 21 of these
        * ActBearTrap
        * ActFallingFloor
        * ActFloatingScore: 8 of these
        * ActBlueBird
        * ActRocket
        * ActPedestal: 3 of these
        * ActInvincibilityShield
        * ActMonument
        * ActSpittingTulip
        * ActFrozenDN
        * ActPulsingFlame: E/W variants
        * ActSpeechBubble: 4 variants
        * ActSmokeEmitter: 2 variants
