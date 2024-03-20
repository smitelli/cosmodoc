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
    * TryPounce: imparts the springiness into actor pounces.
* actor tick functions
    * 39 ActFootSwitch: no-op
    * 26 ActHintGlobe
    * 21 ActPrize
    * 8 ActScoreEffect
    * 5 ActProjectile: depending on direction
    * 4 ActFootSwitch: real
    * 4x2! ActHeadSwitch, ActDoor, UpdateDoors: 4 colors
    * 4 ActRedGreenSlime: leaking/dripping red/green acid
    * 4+2 ActPipeCorner, ActPipeEnd
    * 4 ActSpeechBubble
    * 3 ActTransporter
    * 3-in-1 ActEpisode1End
    * 3 ActPedestal
    * 2 ActHorizontalMover: big saw blade, robotic spike
    * 2 ActJumpPad: floor/ceiling spring
    * 2 ActArrowPiston: E/W variants
    * 2 ActFireball: E/W variants
    * 2 ActReciprocatingSpikes: in ground or W wall
    * 2 ActCabbage
    * 2 ActPyramid: falling ceiling or fixed floor. (fixed ceiling is different!)
    * 2 ActBabyGhostEgg
    * 2 ActClamPlant: floor/ceiling variants
    * 2 ActEyePlant: floor/ceiling variants
    * 2 ActSpittingWallPlant: E/W variants
    * 2 ActForceField: H/V variants
    * 2 ActExitLineHorizontal
    * 2 ActFlamePulse: E/W variants
    * 2 ActSmokeEmitter
    * 1+1 ActPinkWorm, ActPinkWormSlime
    * 1! ActSuctionWalker, SuctionCupWalkerCanFlip
    * 1 ActJumpPadRobot
    * 1 ActVerticalMover: big saw blade
    * 1 ActBombArmed
    * 1 ActReciprocatingSpear
    * 1 ActFlyingWisp
    * 1 ActTwoTonsCrusher
    * 1 ActJumpingBullet
    * 1 ActStoneHeadCrusher
    * 1 ActGhost
    * 1 ActMoon
    * 1 ActHeartPlant
    * 1 ActBombIdle
    * 1 ActMysteryWall
    * 1 ActBabyGhost
    * 1 ActRoamerSlug
    * 1 ActSharpRobot
    * 1 ActParachuteBall
    * 1 ActBeamRobot
    * 1 ActSplittingPlatform
    * 1 ActSpark
    * 1 ActRedJumper
    * 1 ActBoss
    * 1 ActSpittingTurret
    * 1 ActScooter
    * 1 ActRedChomper
    * 1 ActPusherRobot
    * 1 ActSentryRobot
    * 1 ActDragonfly
    * 1 ActWormCrate
    * 1 ActSatellite
    * 1 ActIvyPlant
    * 1 ActExitMonsterWest
    * 1 ActExitLineVertical
    * 1 ActExitPlant
    * 1 ActSmallFlame
    * 1 ActBearTrap
    * 1 ActFallingFloor
    * 1 ActBird
    * 1 ActRocket
    * 1 ActInvincibilityBubble
    * 1 ActMonument
    * 1 ActTulipLauncher
    * 1 ActFrozenDN
