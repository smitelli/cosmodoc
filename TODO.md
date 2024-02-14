* Eventually will be more than semi-complete
* Word count
* Important overall concepts/appendix
* Unused tiles and masktile
* Design and add a proper definition system
* Game ticks and timer ticks are two different things
* canPlayerCling in the debug bar probably only works for east

=============================================================================

* player move
    * MovePlayer: handle one tick of basically all player input.
    * PounceHelper: imparts the springiness into actor pounces.
    * SetPlayerPush: set up a push.
    * ClearPlayerPush: reset push-related vars.
    * MovePlayerPush: handle one tick of player push movement.
    * MovePlayerScooter: handle one tick of player movement on the scooter.
* player/actor
    * TouchPlayer: perform actions when a player and an actor touch. this goes both ways (player hurts actor, actor hurts player.)
* actors
    * NewActor: looks for dead actor slot, then calls NewActorAtIndex to install new actor there. if no dead actors in used area, call CAAI at the first free slot.
    * NewMapActorAtIndex: handle player start, platforms, fountains, lights. if none of those, dispatch to NewActorAtIndex.
    * NewActorAtIndex: sets actorIndexCursor, calls ConstructActor based on actor type.
    * ConstructActor: set all members of actor slot specified by actorIndexCursor. does not change cursor in any way.
    * TestSpriteMove: can an actor def move in the requested direction?
    * AdjustActorMove: fudge actor XY based on planned move direction. set word10/12 to indicate available space to move to.
    * MoveAndDrawActors: for each actor -- call PA. also clears global hint globe/question mark state.
    * ProcessActor: one actor -- handle falling off the map. decrement pounce cooldown. determine if actor is onscreen/should activate. if affected by gravity, apply it. think. if hit by explosion, die. unless something special occurred, call draw fn.
    * thinkers
        * ActFootSwitch: used for 4 real switches. all other references are no-op.
        * ActHorizontalMover: big saw blade, robotic spike
        * ActFloorSpring: floor/ceiling spring
        * ActArrowPiston: E/W variants
        * ActFireBallLauncher: E/W variants
        * ! ActHeadSwitch, ActDoor, UpdateDoors: 4 colors
        * ActCartSpring
        * ActRetractingSpikes: in ground or W wall
        * ActVerticalMover: big saw blade
        * ActArmedBomb
        * ! ActBarrel, DestroyBarrel: barrels and baskets, different type depending on contents
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
        * ! ActSuctionCupWalker, SuctionCupWalkerCanFlip
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
