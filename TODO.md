* Eventually will be more than semi-complete; remove "and counting" then
* Important overall concepts/appendix
    * Map format page really needs an explainer on how sloped tiles are laid out
* Unused tiles and masktile
* Design and add a proper definition system
    * (timer/music/game/???) ticks and frames are really overloaded terms
* update descriptions on actors that don't match the code/text
* look for all maps where the E2M6 bug can happen -- E3M6 is one

=============================================================================

* really unpleasant functions
    * MovePlayer: handle one game tick of basically all player input.
    * MovePlayerScooter: handle one game tick of player movement on the scooter.
    * PounceHelper: imparts the springiness into actor pounces.
    * TouchPlayer: perform actions when a player and an actor touch. this goes both ways (player hurts actor, actor hurts player.)
* actor tick functions
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
