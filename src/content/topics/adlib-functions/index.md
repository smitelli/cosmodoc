+++
title = "AdLib Functions"
description = "Describes the hardware and functions responsible for music playback via the AdLib card."
weight = 300
+++

# AdLib Functions

Many players have experienced the music output of the game through a Sound Blaster or other compatible expansion card, but some might not be aware that the programming interface for music playback was originally introduced by a product called the **AdLib Music Synthesizer Card** in 1987. By most accounts, the AdLib was the first mainstream sound card available for the IBM PC platform. Although the AdLib is capable of producing rich audio that puts the [PC speaker]({{< relref "pc-speaker-and-timing-functions" >}}) to shame, it was only designed to produce music and music-like output; there is no hardware to handle arbitrary waveforms for sound effects. Within a year or two, Creative Labs introduced their competing product, the **Sound Blaster**, which boasted perfect compatibility with the AdLib's programming interface. It also included analog waveform recording/playback and an integrated [game port]({{< relref "joystick-functions" >}}) -- at a very attractive price -- making it an absolute smash hit with the gaming public. AdLib (both the product and the company that created it) soon faded away, but its interface lived on for years.

The AdLib card is really nothing more than a bundle of off-the-shelf components stitched together to function with the PC's bus interface. At the heart of the unit is a **Yamaha YM3812** music synthesis chip, which Yamaha called the **FM Operator Type-L&#8545;** or **OPL2**. The AdLib's interface is exactly the same as the OPL2's, and any programming techniques that work on the OPL2 will work on the AdLib (or any AdLib compatible hardware) with suitable I/O address translation.

{{< table-of-contents >}}

## Making Waves

In order to understand what the OPL2 chip does and what causes its characteristic sound, it's necessary to get a bit into the weeds and explore the math behind sound and music. The building blocks of synthesis are simple -- the same output could be produced on a graphing calculator with little effort -- but artful tuning of the input parameters produces effects that are pleasing to the ear.

All output of the OPL2 is built from a single building block: the **sine function**. Given a series of increasing input values, the output of the sine function starts at zero, drifts up to 1, changes direction and goes all the way down to -1, and then returns back to zero. This cycle repeats infinitely at regular intervals, producing a smooth and stable output wave with many useful properties and symmetries. The repetition behavior depends on the unit of measurement, but typically one **period** of the wave fits into 360 **degrees** or 2&pi; **radians** of input:

{{< image src="sine-function-2052x.png"
    alt="Diagram of the basic sine function and its typical X and Y units."
    1x="sine-function-684x.png"
    2x="sine-function-1368x.png"
    3x="sine-function-2052x.png" >}}

{{< aside class="fun-fact" >}}
**Round and Round**

The sine function can be described (albeit a bit imprecisely) by the following physical process:

Go out into a field or other open space, and draw a large circle on the ground. Draw a straight line that splits the circle exactly in half. Stand at the edge of the circle, and start walking around its perimeter. At regular intervals, measure how far you are from the closest point you can reach on the dividing line. Your position along the outside of the circle is the X axis of this chart, your distance from the dividing line at each point is proportional to the Y value, and the Y value's sign indicates which side of the dividing line you are standing on.

Eventually the measurements repeat, because you are walking in circles. Try not to do it for too long or the neighbors will start to wonder if you're okay.
{{< /aside >}}

This is interesting to look at and all, but some concrete connections must be made to produce audible output. In audio synthesis, the input to the sine function is derived from the passage of time. A counter value tracks the cumulative number of clock "ticks" that have occurred since a fixed point in time, which produces a value that increments at a linear rate. Feeding this counter value into the sine function causes the output to repeat (**oscillate**) at a constant and predicable rate. The function's output is connected to an electrical circuit that causes a speaker to physically move in lock-step with the sine wave as it cycles between -1 and 1. This vibration excites the air molecules in the surrounding area, which can be detected by structures in our ears as sound.

{{< audio "sine-wave" "Basic Sine Wave, Middle C" >}}

Most would call this a beep, which is not very interesting by itself, but it sets the stage for manipulation of the input and output parameters to explore the capabilities of this fundamental arrangement.

### Frequency and Pitch

In our abstract example, we glossed over the relationship between the passage of time and the repetition rate of the sine wave. But this is actually the most important relationship in terms of controlling the output. This rate is measured in **hertz** (Hz), which is the number of periods of wave repetition that occur in one second. This is ultimately governed by the rate of the system's clock ticks, which is constant, being divided by a **frequency** control value. This allows the repetition rate to be reduced, producing a lower **pitch**, or increased to produce a higher pitch:

{{< image src="sine-frequency-2052x.png"
    alt="Examples of different frequencies applied to the sine function."
    1x="sine-frequency-684x.png"
    2x="sine-frequency-1368x.png"
    3x="sine-frequency-2052x.png" >}}

The graphed frequencies are excessively low for the benefit of visual clarity -- the lowest frequency value that humans perceive as a **tone** (or **note**) is around 20 Hz. Below that, we sense rumbling, vibration, clicking, or rhythms. As frequencies increase, tones become whistles, then irritating/painful squeals, followed by hisses, then silence above about 15,000 or 20,000 Hz, depending on the age of the listener and the health of their ears. Musical frequencies are generally in the range of about 25 Hz (e.g. a contrabassoon) to 5,000 Hz (a piccolo), although practically all instruments produce additional frequencies outside of this range which add richness and complexity to their sound.

By taking the basic sine wave and altering its frequency, we get something like the following:

{{< audio "sine-song" "Discrete Sine Frequencies" >}}

Most casual listeners would still call this a beep, but by carefully manipulating the frequency value we are able to divide the constant clock rate into something distinctly musical. This example uses abrupt and discontinuous jumps in frequency, but it is also possible to smoothly "ramp" from one frequency to another over time:

{{< audio "sine-portamento-song" "Continuously Variable Sine Frequencies" >}}

This example uses fine changes in frequency, recomputed at each output point, to create a pitch bend (or **portamento**) over time instead of abrupt jumps between tones. Both techniques are appropriate for music synthesis, depending on the context and desired aesthetic.

### Amplitude and Loudness

In all of the previous examples, the output of the sine function stays within its original range of -1 to 1. This range of values is mapped to the absolute minimum and maximum movement range of the speaker, limited by its physical construction and the available supply of electrical power. Since it is not possible to make the output any louder, the only other remaining dimension of control we have is to make it quieter. By dividing the output of the sine function by a constant **amplitude** scaling factor, we are able to reduce the amount of travel the speaker takes, thus reducing the perceived **loudness** of the output. When graphed, it looks something like this:

{{< image src="sine-amplitude-2052x.png"
    alt="Examples of different amplitudes applied to the sine function."
    1x="sine-amplitude-684x.png"
    2x="sine-amplitude-1368x.png"
    3x="sine-amplitude-2052x.png" >}}

As an audible example, it sounds like this:

{{< audio "amplitude-song" "Rhythms from Varying Amplitudes" >}}

This example is a sine wave of constant (and otherwise irrelevant) frequency, scaled by a few different amplitude values. The spans of silence are produced by scaling the output to such a minuscule value that the speaker doesn't receive enough power to move in any direction.

Much like frequency, the amplitude can change over time to produce interesting entrances and exits of individual notes, as well as producing emotional expression over longer fragments of the music.

{{< audio "zarathustra" "Thus Beeped Zarathustra" >}}

### Phase

There is yet another parameter available to control the output of a sine wave function: **phase**. Compared to frequency, which is a measure of the number of repetitions of the wave in a given span of time, the phase value defines exactly where the starting point of that function was, and at which points in time all subsequent repetitions will occur. Phase can be thought of as adjusting the position of the sine wave in time, without changing the frequency it oscillates at.

With a pure sine function, phase adjustments can vary from -360 degrees (-2&pi; radians) to 360 degrees (2&pi; radians) -- this can also be thought of as an adjustment of &plusmn;1 period. Outside of that range, the result repeats as if smaller values had been used. Positive phase adjustments move the graph to the left, making the signal occur earlier in time, and negative adjustments are the opposite.

{{< image src="sine-phase-2052x.png"
    alt="Examples of different phase adjustments applied to sine functions."
    1x="sine-phase-684x.png"
    2x="sine-phase-1368x.png"
    3x="sine-phase-2052x.png" >}}

A few interesting properties exist: Adding or subtracting 180 degrees (or &pi; radians) perfectly negates the output of the function, flipping the wave upside-down compared to its unmodified version. Adding 90 degrees (&pi; radians) or subtracting 270 degrees (3&pi; &#x2215; 2 radians) turns the sine function into a cosine function.

For a single waveform, phase is entirely inaudible -- it is impossible for the human ear to detect the absolute position of an oscillating signal in time. When multiple signals are combined together, however, phase plays a significant role in determining how the individual waves interact to produce a cumulative output.

### Vibrato and Tremolo

The musical terms **vibrato** and **tremolo** refer to variations in frequency and amplitude, respectively, of a tone over time. By slightly adjusting the frequency and/or amplitude of an otherwise constant tone, different effects and emotions can be conveyed.

{{< image src="vibrato-and-tremolo-2052x.png"
    alt="Shows the different effects of vibrato and tremolo on frequency and amplitude."
    1x="vibrato-and-tremolo-684x.png"
    2x="vibrato-and-tremolo-1368x.png"
    3x="vibrato-and-tremolo-2052x.png" >}}

For vibrato, the base frequency of the sine wave is adjusted by a small and ever-changing amount, producing a sort of "quiver" in pitch over time. The added value varies continuously, sometimes positive and sometimes negative, but it is always centered around zero which keeps the output frequency anchored to its unmodified value. To be perceived as a true vibrato, the rate must be considerably slower than the frequency of the tone -- typical vibrato speeds are between 1 and 10 Hz.

{{< audio "vibrato" "Vibrato: Constant Amplitude with Varying Frequency" >}}

This example uses the same vibrato rate that the OPL2 chip uses: 6.07 Hz.

Tremolo functions similarly, except the scaling occurs at the output side of the sine wave, changing amplitude and producing more of a "flutter" in loudness. As implemented in the OPL2, tremolo can only _reduce_ the amplitude, so it has the net effect of making the overall loudness of a passage somewhat quieter. As with vibrato, the tremolo rate must be much slower than the frequency of the tone in order to be perceived as a true tremolo.

{{< audio "tremolo" "Tremolo: Constant Frequency with Varying Amplitude" >}}

This example also demonstrates the OPL2 tremolo rate: 3.70 Hz.

These are both actually special cases of more general signal manipulations. Vibrato is a form of **frequency modulation** (FM) and tremolo is a form of **amplitude modulation** (AM). FM is of particular importance in creating the characteristic sound of the OPL2.

### Frequency Modulation

The most common method of producing sound on the OPL2 chip is through FM synthesis. This requires the use of two discrete **oscillators**: the **modulator** which is located first in the signal chain, followed by the **carrier** that ultimately creates the audible signal. The output amplitude of the modulator is used to modify the phase of the carrier.

A constant phase shift would simply move the peaks and valleys of the carrier's output wave earlier or later in time, without affecting the way it sounds. A variable phase shift over time, however, creates the effect of the pitch raising or lowering (like in the earlier example of vibrato) without the carrier's frequency value changing. There can even be _discontinuous_ phase shifts, causing the output to jump wildly to produce noise or other outputs that no longer look or behave like sine waves.

FM is notoriously difficult to reason about because of the interactions between these two oscillators. The modulator's frequency _and_ amplitude can have a profound effect on the carrier, at times even completely masking the frequency the carrier is tuned to. Fortunately, most frequency combinations sound either non-musical or downright awful, so the OPL2 restricts the composer from choosing all but a few frequency ratios.

In the OPL2, the modulator and carrier frequencies are both locked to the frequency of the note being played and cannot be arbitrarily tuned. The only frequency control available is a **multiplier** in the range of 0.5x to 15x, which can be applied to the modulator and/or carrier frequencies independently. This allows for a few dozen frequency ratios to be produced while eliminating combinations that are not musically useful.

There is far more control available in the output amplitude of the modulator. This can be at full loudness (in which case the carrier's phase could be shifted by as much as &plusmn;8&pi;) all the way down to silence (where the carrier's phase would be unaffected).

Since one period of the modulator's sine function has the capability to phase-shift the carrier by up to four periods in either direction, it's possible to create a variety of different outputs. The effect of modulation adds **harmonics** or **overtones** to the base frequency of the carrier, which are additional frequencies that appear at regular intervals above or below the carrier frequency. The frequency of the modulator determines the spacing of these harmonics (higher modulation frequencies produce harmonics that are spaced farther apart) and the amplitude of the modulator controls how many harmonics are produced.

Using the available controls, the range of modulator settings sounds like the following example. You might want to turn down your volume as a precaution; this is not exactly easy listening.

{{< audio "modulation-up" "Middle C Carrier, 0.5x to 15x Ascending Modulator" >}}

Throughout the example, the carrier is playing a constant frequency and amplitude. The modulator steps through all of its available multiplication settings, from 0.5x to 15x, one per second. Within each multiplication setting, the modulator amplitude begins at full output and decays linearly to zero before switching to the next multiplication setting.

It's helpful to look at a **spectrogram** of what this audio looks like. The horizontal axis represents time, the vertical axis is frequency, and the intensity of the colors within the plot represents the amplitude of each frequency at that point in time:

{{< image src="modulation-up-2052x.png"
    alt="Spectrogram of the Ascending Modulator example audio."
    1x="modulation-up-684x.png"
    2x="modulation-up-1368x.png"
    3x="modulation-up-2052x.png" >}}

At lower multiplication levels, the harmonics are spaced evenly and decay from highest to lowest. Starting at 3.0 seconds, the harmonics begin to "reflect" on top of themselves on the frequency axis, appearing at more and more uneven intervals and decaying in less-than-simple to predict ways. Across the entire example, the fundamental middle C note at 262 Hz remains in place.

It's far less interesting to multiply the carrier frequency in isolation. However, a useful effect can be produced by artificially requesting a note to be played at a fraction of the intended frequency (which makes both the modulator and the carrier run at a lower frequency than intended) then setting the carrier's multiplication to bring the note frequency back to what was originally desired. This has the effect of running the modulator as if it were _divided_ by the carrier's multiplication factor, which can produce some interesting effects:

{{< audio "modulation-down" "Middle C Carrier, 2x to 1/15x Descending Modulator" >}}

And the spectrogram:

{{< image src="modulation-down-2052x.png"
    alt="Spectrogram of the Descending Modulator example audio."
    1x="modulation-down-684x.png"
    2x="modulation-down-1368x.png"
    3x="modulation-down-2052x.png" >}}

The rest of the parameters are the same as the previous example, and the behavior is the same from a mathematical standpoint. The harmonics become more densely packed as the ratios progress, resulting in lower and eventually sub-audible frequencies being produced. None of the generated harmonics reach a high enough frequency to cause the reflection behavior seen earlier, so the spacing remains consistent and the output is more musical. What's more interesting is the fact that, although the fundamental middle C note never disappears, it becomes so deeply buried in a sea of harmonics that the output stops sounding like middle C.

Our examples always left one of the two oscillators at 1x, but it's possible to use any desired multiplier combination between the modulator and the carrier. While it's true that the available options preclude choosing a ratio which is an irrational number -- which substantially limits the range of options -- there are still close to 80 ratios available for use. It's entirely up to the composer to decide which modulator settings work best for a given piece of music. If you're interested in the world of inharmonic ratios, look up a piece called _Stria_ by John Chowning, the creator of digital FM synthesis.

A few general rules of thumb can be summarized:

* The higher the modulator frequency (relative to the carrier), the larger the frequency spacing between harmonics.
* There is limited space available in the frequency spectrum. Once harmonics reach the end of the available space, they start repeating _at irregular spacing_ elsewhere in the spectrum.
* The higher the modulator amplitude, the more harmonics appear. Reducing the amplitude causes the highest-order harmonics to disappear first. If these harmonics have been reflected elsewhere in the frequency spectrum, they _may not_ be the highest frequency components in the sound.

Beyond that, it's all subjective. Low modulator ratios produce harmonics that are strictly multiples of the fundamental carrier frequency, which most listeners would describe as having a "musical" quality. Once the harmonics start appearing at non-multiples of the fundamental frequency, the output takes on a distinctly metallic sound -- this could be described as "bells" or "clanging" noise. Adding and removing harmonics over time is perceived as a sort of "wow" sound.

### Feedback

Some of the oscillators in the OPL2 are capable of **feedback**, where some fraction of an oscillator's output amplitude is fed back into its input as a phase shift. This works the same as modulation, but has a distinctly more chaotic result. The amount of phase shift is adjustable from zero to &plusmn;4&pi; at maximum. The OPL2 uses a mixture of the previous _two_ output values when calculating the feedback amount for the next value.

{{< audio "feedback" "Feedback Depth Examples" >}}

This example steps through the feedback levels from zero to 4&pi;, playing a note that decays in amplitude once per second. At moderate levels of feedback, the sine wave becomes lopsided like a sawtooth wave -- rising fast and falling slowly -- which adds both sharpness and brightness due to the many harmonics created. As the feedback level is set higher, louder outputs produce more random results, and at extreme levels the sound becomes distinctly percussive.

{{< note >}}
The noise produced through this technique is almost perfect **white noise**, which is random sound output with equal _power_ across the entire frequency spectrum. The OPL2's output has slightly higher frequency response at the low and high edges of the spectrum, making the result something between white noise and **gray noise**, which is equal _loudness_ across the spectrum.

The relationship between power and loudness is explored in a bit more detail later.
{{< /note >}}

Most instruments in common use have some amount of feedback to add distinctiveness to the sound. The exceptions tend to be tonal percussion elements like the bass drum and low tom-toms.

### Envelope

In order to more realistically approximate the behavior of real instruments, most synthesis techniques support amplitude control via **envelopes**. As each individual note goes through its lifecycle -- from initial onset all the way back to silence -- the oscillator goes through several distinct stages that affect output amplitude over time. These stages are **attack**, **decay**, **sustain**, and **release**.

The attack stage begins when a note-on event occurs. This could occur at any time, even if the envelope is already in another stage. During attack, the amplitude of the note begins at silence (or whatever level it was at when the previous envelope was interrupted) and increases at a configurable **rate** until the amplitude reaches the maximum possible level.

When the maximum attack amplitude is reached, the decay stage begins. During decay, the amplitude of the note decreases at a configurable rate until the amplitude reaches the sustain level.

When the sustain level is reached, all envelope processing is paused. The amplitude is held at the sustain level for as long as the composer holds the note on.

When a note-off event occurs, regardless of the stage the envelope is currently in, the release stage begins. The amplitude of the note decreases at a configurable rate until it becomes silent, at which point the envelope has completed its lifecycle and becomes idle again.

Higher rate values cause faster changes in amplitude, including instantaneous jumps at extreme settings. Lower rate values cause more gradual amplitude changes. Zero is a permissible rate, which has the effect of artificially holding the envelope in a stage that it wouldn't normally stay in, which can be used for interesting effects.

Visually, the interaction between note events (often called **Key On** and **Key Off** signals) and envelopes looks like the following:

{{< image src="key-on-and-envelope-2052x.png"
    alt="Diagram showing the interaction between the key-on signal and envelope lifecycle."
    1x="key-on-and-envelope-684x.png"
    2x="key-on-and-envelope-1368x.png"
    3x="key-on-and-envelope-2052x.png" >}}

The combination of envelope attack, decay, release, and sustain is commonly referred to as **ADSR**. It's important to bear in mind that attack/decay/release are _rates_ (amounts of change over time) while sustain is a _level_ (amplitude scaling value). Taken together and configured appropriately, envelopes can create surprisingly convincing simulations of real instrument behavior.

Envelopes are often used in conjunction with FM techniques to create more sophisticated sounds. Depending on the desired effect, the modulator could have very different ADSR settings than the carrier, allowing for the phase of the output to evolve independently of the overall sound level.

### Key Scaling

On the subject of simulating real instruments, the OPL2 also supports two slightly more arcane settings: key scaling of rate (KSR) and key scaling of level (KSL). As convoluted as the documentation tries to make it, the underlying concept is surprisingly straightforward: lower notes behave differently than higher notes do. These two settings aim to replicate this behavior with relatively few parameters.

**Key scaling of rate** adjusts the ADSR rate parameters according to the frequency of the note that is being played. The lowest notes use the original unmodified envelope values, while higher notes have their rates increased (causing their envelopes to progress faster). The higher the note frequency, the more the ADSR rates are sped up. KSR has two possible options: large or small (it is not possible to entirely disable it). In large mode, rates on the highest notes are increased by almost four units. In small mode, the maximum increase is just under one unit.

{{< image src="ksr-concepts-2052x.png"
    alt="Diagram showing the overall effect of \"Key Scaling of Rate\"."
    1x="ksr-concepts-684x.png"
    2x="ksr-concepts-1368x.png"
    3x="ksr-concepts-2052x.png" >}}

{{< note >}}The exact definition of a rate "unit" is... complicated. It's explained a little more precisely later on this page.{{< /note >}}

The piano keyboards in this diagram (and the one that follows) are illustrative and not necessarily to scale. It's possible to configure the OPL2 to span a much wider frequency spectrum than the piano is capable of, and the scaling graphs would follow that range accordingly.

**Key scaling of level** simulates the tendency of higher notes to play more quietly, and it does this by reducing the amplitude of notes as their frequencies get higher. KSL can be switched off if desired, or set to one of three levels.

{{< image src="ksl-concepts-2052x.png"
    alt="Diagram showing the overall effect of \"Key Scaling of Level\"."
    1x="ksl-concepts-684x.png"
    2x="ksl-concepts-1368x.png"
    3x="ksl-concepts-2052x.png" >}}

The unit "dB" is an abbreviation for **decibel**, which is described in detail a bit later. For the purposes of this concept, 0 dB is "no reduction in level" and -42 dB is roughly halfway between the loudest and quietest _perceived_ volume available.

### Waveforms

The OPL2 is only capable of producing sine waves, but it can do a few manipulations to the function's basic shape to produce other waveforms. In total, four waveforms can be produced:

{{< image src="waveforms-2052x.png"
    alt="The four sine-based waveforms available in the OPL2."
    1x="waveforms-684x.png"
    2x="waveforms-1368x.png"
    3x="waveforms-2052x.png" >}}

The first wave is the standard sine wave, unmodified. Silencing the negative portions of the wave produces a "half" sine. By instead taking the absolute value of the sine wave, a **rectified** sine is produced. Finally, by taking the rectified sine wave and silencing the areas with negative slope, a "half-rectified" sine is generated. Each of these has a harsher and more harmonically rich sound compared to the sine function they are derived from.

The modified waves do not contain any negative values, which has the effect of reducing the overall travel distance of the speaker and making them sound somewhat quieter than the pure sine wave. The added sonic character, which could be described as "brightness" or "harshness" by some, compensates for this loss.

### Frequencies and Amplitudes, Mathematically

Up until this point, we've been treating the units for frequency and amplitude a little loosely. As the description of the OPL2 becomes more concrete, it's going to be necessary to understand precisely the quantities being measured and how they relate to real sounds.

#### Frequency

As briefly mentioned earlier, frequency is measured in hertz (Hz) and it describes the number of times a signal repeats itself in one second. The inverse of frequency is the period, which is the amount of time required for one repetition of the signal. This is all pretty cut and dry, and everything makes good clear linear sense until the signal reaches our ears. Human ears are logarithmic.

The distance between the notes B and C on the lowest end of a piano keyboard is about 1.8 Hz. The human ear can detect that difference. On the high end of that same piano, the distance from B to C is almost 235 Hz. Even a well-trained ear would be unable to detect if one of those high keys was 1.8 Hz out of tune without comparing it to a reference frequency -- and even then it would be tough to do. Human hearing simply has better resolution at lower frequencies.

Hearing (and physical objects) are also highly responsive to **octaves**, each of which is a doubling of any frequency. So the first octave of 100 Hz is 200 Hz, followed by another doubling to 400, then 800, and up to 1,600 Hz and so on. Musically, all frequencies in a given octave series sound sort of "the same" -- if you've ever tried to sing along to a song that was too low for your vocal range, and you compensated by jumping up to a higher set of notes that you could sing comfortably, that's an octave.

Western musicians decided a long time ago that each octave should have 12 note divisions in it. The rules about how those 12 notes should be utilized came later, but the 12-note octave became the bedrock upon which everything else was built. The intervals between each note were chosen so that _every single note_ was double the frequency of the note 12 spaces to the left, and half the frequency of the note 12 spaces to the right. They accomplished that minor miracle with the following formula: **Frequency of note _n_ = (<sup>12</sup>&radic;2)<sup>_n_</sup> &times; 440 Hz**

The 12th root is because our octave is divided into 12 notes, and 440 Hz is the reference frequency of the A above middle C (sometimes called A4). The arrangement works correctly if a different frequency is used, but 440 Hz is the standard that musicians agreed on. The number _n_ is the distance (in note steps) away from the reference note -- positive when moving up the keyboard, and negative when moving down.

If we wanted to find the frequency of the note that was five steps below A4, we would calculate (<sup>12</sup>&radic;2)<sup>-5</sup> &times; 440 Hz &approx; 330 Hz. By the same rules, the frequency of the note seven steps above A4 is (<sup>12</sup>&radic;2)<sup>7</sup> &times; 440 Hz &approx; 660 Hz. It just so happens that "five steps below" plus "seven steps above" equals 12 steps, and the two calculated frequencies are one octave apart, give or take some rounding error.

The formula can be inverted: **Steps to note _n_ = 12 &times; log<sub>2</sub>(_f_ &divide; 440 Hz).** Here _f_ is some frequency in hertz, and _n_ is the note-step distance (again positive or negative) away from the A4 reference note.

#### Amplitude

We've been taking the output of the sine function, calling it "amplitude" or "level," and passing it directly to a speaker that moves proportionally by the same amount. This much is actually accurate, but once again it is not the way our ears perceive things. Human ears are able to detect surprisingly faint sounds, while at the same time tolerating (at least for brief periods) other sounds that are many orders of magnitude louder. As with frequency, the response can best be modeled as a logarithmic one.

Hearing roughly follows a power-of-ten logarithmic curve. This ratio is measured in units called **decibels** (dB), and every 10 dB represents a halving or a doubling of the perceived loudness of any sound. Absolute measurements of sound pressure in air range from about 5 dB (too quiet to be audible for most people) to about 190 dB (will literally rip your inner ear apart).

In electrical circuits, and computer applications that interact with them, decibels work a little differently. In this universe, 0 dB represents the absolute maximum amount of power (and loudness) that the hardware can faithfully and continually produce. To create lower volumes, the output is **attenuated** by some amount. In terms of voltage, waveform sample values, and speaker movement, every 6 dB of attenuation exactly halves the output voltage. A given output voltage can only be halved so many times before the level drops to the point where it is indistinguishable from background noise. This has some interesting relationships to digital audio as well -- a 16-bit sample value can only be halved 16 times (96 dB attenuation) before it becomes zero (silence).

In everything relating to the OPL2, the rule is that 6 dB of attenuation halves the output level, which also halves the voltage and speaker travel distance. How that is perceived by the listener in context, and how it should be utilized by the composer of the music, is more of a subjective choice than anything else.

You'll often see levels written like "-12 dB," which is a shorthand representing 12 decibels of attenuation (or, as we just learned, one-quarter of the maximum output level otherwise attainable at 0 dB of attenuation).

## Anyway, Here's the OPL2

Theory becomes practice now. The OPL2 is a real-time FM synthesis chip that is reprogrammed on the fly while playback occurs. It contains 18 **operators**, each consisting of a sine wave generator (oscillator), an envelope processor, and a level controller. Each operator is self-contained and functionally independent. The OPL2 is organized into nine **channels**, each managing two of the available operators. Each channel can control how its operators are connected to each other: either serially to produce FM sounds, or in parallel for additive synthesis. The output of all nine channels is summed together to produce a 13-bit floating-point sample value that an external digital-to-analog converter (like the Yamaha YM3014) decodes into an electrical signal for the speaker circuit.

{{< image src="opl2-block-diagram-2052x.png"
    alt="Block diagram showing two (of nine) channels available in the OPL2."
    1x="opl2-block-diagram-684x.png"
    2x="opl2-block-diagram-1368x.png"
    3x="opl2-block-diagram-2052x.png" >}}

The OPL2 has an 8-bit data bus that supports both reading and writing from the host system's CPU. When read, the OPL2 reports the state of its two internal timers. Writing is a two-step operation: the host must first write the address of the 8-bit register it wants to program, then it must write the 8-bit value that should be placed into that register. The updated value becomes audible immediately. There is no provision to read back the contents of arbitrary registers.

There are three kinds of registers: chip-wide registers, per-channel registers, and per-operator registers. The chip-wide registers each have a single address and modify a parameter that influences the behavior of the chip as a whole. Channel registers modify parameters that are channel specific, and each of these register types occupies nine positions in the address map -- one for each channel. Similarly, operator registers control parameters for a single operator, and there are 18 positions used in the address map for each of these register types.

### Chip-Wide Registers

The OPL2 contains 18 parameters that influence the behavior of the entire chip. Each of these register values either changes a sub-circuit that the chip only contains one instance of, or controls a setting that applies universally across all channels and/or operators.

Register Address | Bit Position | Acronym  | Range       | Function
-----------------|--------------|----------|-------------|----------
01h              | 5            | WSE      | Off/On      | "Waveform Selection" Enable
02h              | 7&ndash;0    | TIMER 1  | 0&ndash;255 | Timer 1 Preset Value
03h              | 7&ndash;0    | TIMER 2  | 0&ndash;255 | Timer 2 Preset Value
04h              | 7            | RST      | Off/On      | Interrupt Reset Command (must be sent in isolation)
04h              | 6            | T1 MASK  | Off/On      | Timer 1 Mask
04h              | 5            | T2 MASK  | Off/On      | Timer 2 Mask
04h              | 1            | T2 START | Off/On      | Timer 2 Enable
04h              | 0            | T1 START | Off/On      | Timer 1 Enable
08h              | 7            | CSM      | Off/On      | Composite Sine Wave Speech Modeling Enable
08h              | 6            | NOTE SEL | 0&ndash;1   | Note Select (Keyboard Split) Position
BDh              | 7            | AM DEP   | 0&ndash;1   | Amplitude Modulation (Tremolo) Depth
BDh              | 6            | VIB DEP  | 0&ndash;1   | Vibrato Depth
BDh              | 5            | R        | Off/On      | Rhythm (Percussion) Mode Enable
BDh              | 4            | BD       | Off/On      | Bass Drum Key-On
BDh              | 3            | SD       | Off/On      | Snare Drum Key-On
BDh              | 2            | TOM      | Off/On      | Tom-Tom Key-On
BDh              | 1            | TC       | Off/On      | Top Cymbal Key-On
BDh              | 0            | HH       | Off/On      | Hi-Hat Key-On

When a read command is issued to the OPL2, a status byte is returned. Since there is only one single readable register in the entire chip, it is not necessary (or possible) to request a specific register address to read from.

Bit Position | Acronym | Range  | Function
-------------|---------|--------|---------
7            | IRQ     | Off/On | Interrupt Requested
6            | T1 FLAG | Off/On | Timer 1 Overflow Occurred
5            | T2 FLAG | Off/On | Timer 2 Overflow Occurred

### Per-Channel Registers

The OPL2 contains nine instances of the following six parameters, one group for each channel in the chip. The values here either adjust both of the channel's operators in tandem, or influence the way the two operators are connected to each other.

Register Address | Bit Position | Acronym | Range       | Function
-----------------|--------------|---------|-------------|----------
A0h + _channel_  | 7&ndash;0    | F NUM L | 0&ndash;255 | Frequency Value (low byte)
B0h + _channel_  | 5            | KON     | Off/On      | Channel Key-On
B0h + _channel_  | 4&ndash;2    | BLOCK   | 0&ndash;7   | Octave (Block) Value
B0h + _channel_  | 1&ndash;0    | F NUM H | 0&ndash;3   | Frequency Value (high 2 bits)
C0h + _channel_  | 3&ndash;1    | FB      | 0&ndash;7   | Feedback Depth
C0h + _channel_  | 0            | C       | 0&ndash;1   | Connection Type

### Per-Operator Registers

The OPL2 contains 18 instances of the following 12 parameters, one group for each operator in the chip. These allow for independent control of each modulator, carrier, or additive oscillator (depending on how the chip and its channels have been configured).

Register Address | Bit Position | Acronym | Range      | Function
-----------------|--------------|---------|------------|----------
20h + _operator_ | 7            | AM      | Off/On     | Amplitude Modulation (Tremolo) Enable
20h + _operator_ | 6            | VIB     | Off/On     | Vibrato Enable
20h + _operator_ | 5            | EG TYPE | 0&ndash;1  | Envelope Generator Type
20h + _operator_ | 4            | KSR     | 0&ndash;1  | "Key Scaling of Rate" Value
20h + _operator_ | 3&ndash;0    | MULTI   | 0&ndash;15 | Frequency Multiplier Value
40h + _operator_ | 7&ndash;6    | KSL     | 0&ndash;3  | "Key Scaling of Level" Value
40h + _operator_ | 5&ndash;0    | TL      | 0&ndash;63 | Total Level Value
60h + _operator_ | 7&ndash;4    | AR      | 0&ndash;15 | Attack Rate
60h + _operator_ | 3&ndash;0    | DR      | 0&ndash;15 | Decay Rate
80h + _operator_ | 7&ndash;4    | SL      | 0&ndash;15 | Sustain Level Value
80h + _operator_ | 3&ndash;0    | RR      | 0&ndash;15 | Release Rate
E0h + _operator_ | 1&ndash;0    | WS      | 0&ndash;3  | Waveform Selection

The assignments between channels and operators, and between operators and their register offsets, is not contiguous and not straightforward to explain. The table below shows the modulator/carrier operator pairs for each channel, and the offsets used to address them in per-operator register writes:

{{< data-table/opl2-operator-map >}}

{{< note >}}Operator register offsets 6&ndash;7h, E&ndash;Fh, and anything &GreaterEqual; 16h are **undefined** and perform no function.{{< /note >}}

The arrangement of operators is a consequence of the OPL2's design. The chip only contains one physical instance of an operator circuit, which must be utilized 18 times to generate all of the values that comprise an output sample. The operator index arrangement is related to the order that this operator circuit processes the data internally.

### Clock and Timing

The OPL2 chip requires an external high-frequency oscillator to govern its operation and to serve as the master clock for all frequency-based calculations. As installed in the AdLib card, the master clock runs at approximately 3.58 MHz and the output sample rate is 49,716 Hz. Any conversions to/from a musical frequency must incorporate this sampling frequency to keep proper tuning.

{{< aside class="fun-fact" >}}
**The PC's clock strikes again.**

At first glance, 49,716 Hz seems like a pointlessly arbitrary number. But it's actually derived in a surprisingly straightforward way. As detailed on the [Programmable Interval Timer/PC speaker]({{< relref "pc-speaker-and-timing-functions" >}}) page, the PC's clock generator circuitry is based around a 315 &#x2215; 22 MHz (14.3 MHz) crystal, which was widely available and cheap due to its use in NTSC color television equipment. The AT bus uses this frequency, unmodified, as the "OSC" signal. The AdLib, lacking any timing circuitry of its own, cleverly passes this signal through a 74LS109 dual flip-flop that divides the frequency by four, yielding 315 &#x2215; 88 MHz (3.58 MHz).

The OPL2 chip requires 72 clock cycles to generate one sample of output data. This works out to ([315 &#x2215; 88 MHz] &div; 72) 49,715.{{< overline >}}90{{</ overline >}} Hz, which is rounded to 49,716 Hz in typical calculations.
{{< /aside >}}

The OPL2 chip requires a fixed amount of "recovery" time after a write operation. The host must wait for 12 master clock cycles after writing a register address before it can write data, and it must wait 84 cycles after writing a data byte before it can write anything else. At AdLib clock rates, these wait times are about 3.4 &micro;s and 23.5 &micro;s, respectively. If these delays are ignored, there's no guarantee that a write operation will have the intended effect.

### On-Board Timers

A fair number of the chip-wide writable registers (and the entirety of the readable registers) are there to support a pair of configurable **timers**. Timer 1 increments its counter once every 80 &micro;s and Timer 2 increments one-fourth as fast -- every 320 &micro;s. Each timer counter is eight bits wide, and whenever either of them overflows and wraps back to zero, a flag value is set to indicate the overflow and that timer's Preset Value is reloaded into the counter. Using this arrangement, Timer 1 could be configured to overflow at a rate anywhere between 49 Hz and 12.5 kHz, while Timer 2 could be configured for 12&ndash;3,125 Hz. When either timer overflows, an **interrupt request** is also raised at the hardware level. The AdLib doesn't listen to this signal, however, so there is no way for the host system to know about these timer events without resorting to polling.

The **Timer 1/2 Preset Value** registers control the counter value that is reloaded during each overflow, which influences the resulting overflow rate -- higher values produce more frequent overflows. The **Timer 1/2 Mask** settings control whether the chip raises an interrupt when that particular timer overflows. The **Timer 1/2 Enable** settings pause or unpause counting for that timer. If an interrupt has previously occurred, the **Interrupt Reset** command will acknowledge it and reset all flags in preparation for a subsequent interrupt request.

The host can read the **Timer 1/2 Overflow Occurred** flag bits to determine if one of the timers has overflowed since the last interrupt reset, and which timer it was. If the host doesn't care about the specific timer that triggered the interrupt, it can simply read the **Interrupt Requested** bit, which turns on if either of the timer flag bits have turned on.

In common operation, nothing is triggered by either of these timers and they do not influence the sound produced by the chip. They serve no outwardly apparent purpose, which is why many sources gloss over the fact that they exist. The most common use of these timers is actually to detect the AdLib in the first place, since this is the only means of bidirectional communication the programmer has to determine if an AdLib or AdLib-like piece of hardware is installed at a particular I/O address.

### Composite Sine Wave Speech Modeling

The OPL2 and the original OPL (YM3526) chips support a composite sine wave speech synthesis mode (CSM). Nobody, including your humble author, seems to really understand how this was supposed to work or what it may have sounded like. General consensus seems to be that it was hard to do and sounded bad in practical use, so take that as you will.

Apparently CSM required all channels to be configured in additive mode with no active key-on signals. Whenever Timer 1 overflowed, it would briefly strobe the Key-On signal for every channel. That's about all I was able to find in the original documentation. This feature was removed in the OPL3 (YMF262) and none of the software emulators I'm aware of have implemented it.

### Waveform Selection

Yamaha's OPL and OPL2 are actually identical for all practical purposes and can be interchanged without difficulty. The only thing differentiating the OPL2 is the ability to choose between four different sine waveform functions. The original OPL can only produce unmodified sine waves.

Changing the waveform involves two parameters: The **Waveform Selection** value on one of the operators, and the **"Waveform Selection" Enable** setting at the chip level. If "Waveform Selection" Enable is not turned on, changes to a Waveform Selection parameter are ignored and the OPL2 behaves identically to an OPL -- only using waveform 0.

The available waveforms for each operator are:

Waveform Selection | Description
-------------------|------------
0                  | Unmodified sine
1                  | Positive portions of sine
2                  | Absolute value of sine (aka "Rectified" Sine)
3                  | Rising portions of rectified sine

### Tremolo

The OPL2's tremolo effect is controlled by two parameters. The **AM/Tremolo Depth** parameter at the chip level changes the depth used chip-wide:

Tremolo Depth | Attenuation Range
--------------|------------------
0             | 0 &ndash; -1.1 dB
1             | 0 &ndash; -4.9 dB

The **AM/Tremolo Enable** parameter on each operator controls whether tremolo should be applied to that operator. Regardless of the depth setting, the tremolo effect runs at 3.7 Hz and every operator's tremolo phase is locked in sync.

### Vibrato

Vibrato works similarly to tremolo. The chip-wide **Vibrato Depth** parameter sets the amount of frequency adjustment applied. This is accomplished by adding or subtracting a certain number of **cents** to the frequency specified in the channel's "F NUM" value. (One cent is equal to 1/100th of a note step.)

Vibrato Depth | Frequency Range
--------------|----------------
0             | "F NUM" &plusmn;7 cents
1             | "F NUM" &plusmn;14 cents

The **Vibrato Enable** parameter on each operator controls whether vibrato is enabled there. The vibrato frequency is 6.07 Hz and the vibrato phase is locked in sync across all operators.

### Frequencies, Octaves, and Notes

To control the actual frequency and enablement of the notes played on a channel, four parameters are involved. The first, **Frequency Value** (or "F NUM") is a 10-bit quantity which is split between a full 8-bit register and two bits of another register. Taken together, the Frequency Value can be in the range of 0&ndash;1,023. Another channel parameter, **Octave** (or "BLOCK"), shifts the binary digits in the Frequency Value to the left by a certain number of positions. The Octave value can be any integer between 0 (meaning no shift occurs) up to 7 (shift to the left by seven binary digits). This has the effect of multiplying the Frequency Value by 2<sup>BLOCK</sup>, which also has the effect of moving the note frequency up by one musical octave for every one Octave Value.

To convert the Frequency and Octave Values into the frequency they represent, the formula **_f_ = _FNUM_ &times; 49,716 &div; 2<sup>20 - _BLOCK_</sup>** can be used. Here _f_ is the audible frequency that will be played (in hertz), _FNUM_ is the Frequency Value as programmed into the OPL2's registers, and _BLOCK_ is the Octave Value. The constant 49,716 is the sampling frequency of the AdLib's OPL2.

The inverse of this formula is more commonly seen in documentation for AdLib programming: **_FNUM_ = _f_ &times; 2<sup>20 - _BLOCK_</sup> &div; 49,716**. The programmer has to do a bit of work here -- not only is it necessary to translate musical note names into frequencies in hertz before even starting the conversion, but they also need to select a value for _BLOCK_ that won't cause _FNUM_ to overflow on high notes, while also providing enough resolution to get accurate tuning on low notes. It's a bit of a delicate trade-off.

{{< note >}}The value chosen for _FNUM_ also interacts with the Note Select (Keyboard Split) parameter, explained below. The programmer should consider how the chosen _FNUM_ value will propagate through this setting to influence the envelope rates.{{< /note >}}

Next, each operator has a **Frequency Multiplier Value** which can further manipulate the frequency being played. This is the only parameter that allows the two operators on a channel to run at different frequencies -- all other frequency-control parameters are set at the channel level and apply to both operators in unison.

Frequency Multiplier Value | Operator Frequency Multiplied By...
---------------------------|------------------------------------
0                          | 0.5x
1                          | 1x
2                          | 2x
3                          | 3x
4                          | 4x
5                          | 5x
6                          | 6x
7                          | 7x
8                          | 8x
9                          | 9x
10 or 11                   | 10x
12 or 13                   | 12x
14 or 15                   | 15x

The final piece of the puzzle is each channel's **Key-On** parameter. (The word "key" here is used in the sense of, say, a piano key.) When this is turned on, both operators on the channel begin voicing their output, each starting their ADSR envelopes at the beginning of the "attack" stage. As long as the Key-On parameter remains enabled, the envelopes will follow their pre-programmed rates and stages, controlling the output of the oscillators along the way. The oscillators will play for as long as the Key-On parameter remains on, provided their envelopes are not programmed to silence the sound prematurely.

When the Key-On parameter is turned off, the envelopes jump to their "release" stage and begin the process of silencing the oscillator outputs.

### Operator Connections and Feedback

Each channel contains a pair of closely-related parameters: **Connection Type** and **Feedback Depth**. These control how the channel's two operators are connected together. Connection Type can be one of the following:

Connection Type | Description
----------------|------------
0               | Frequency Modulation mode. Operator 1 is the modulator, whose instantaneous output amplitude is fed into operator 2 as a phase adjustment in the range &plusmn;8&pi;. Operator 2 is the carrier, whose output becomes the output for the channel as a whole.
1               | Additive mode. Operator 1 and operator 2 share no phase adjustments. The outputs of both operators are added together, and this sum becomes the output for the channel as a whole.

In both modes, operator 1 (and _only_ operator 1) supports an optional amount of **feedback**. Feedback is computed by taking the previous _two_ samples produced by operator 1, adding the samples' amplitudes together, and scaling the result based on the configurable Feedback Depth. The result -- which could be anywhere between zero and &plusmn;4&pi; depending on the amplitude of the previous samples and the amount of depth configured -- is added to the phase offset of operator 1 as its next sample is computed.

Feedback Depth | Phase Offset Range
---------------|-------------------
0              | 0 (feedback disabled)
1              | &plusmn;&pi;/16
2              | &plusmn;&pi;/8
3              | &plusmn;&pi;/4
4              | &plusmn;&pi;/2
5              | &plusmn;&pi;
6              | &plusmn;2&pi;
7              | &plusmn;4&pi;

### Rhythm Mode

**Rhythm Mode Enable** is a chip-wide setting that, when turned on, rewires channels 7&ndash;9 to function as five separate percussion instruments. Channel 7 uses FM mode, combining its two operators to produce a bass drum sound. Channels 8 and 9 both switch to additive mode to independently produce a snare drum, tom-tom, top cymbal, and hi-hat. Channels 1&ndash;6 continue to operate as usual.

Since there are five percussion instruments, but they're packed into just three channels, a different mechanism must be used to control their Key-On states. Five bits in register BDh, one per instrument, control the Key-On for each rhythm sound in this mode. The per-operator registers can still be used to tune the sound of each percussion instrument independently, allowing for some degree of customization.

Rhythm mode does not see much use in general, and it is never enabled at any point in any of this game's music. The reasoning for this varies, with some sources claiming that rhythm mode does not offer enough control over the sound of the drums to create the tones required for many compositions. Other creators (or perhaps the software tools they prefer to use) are simply more comfortable defining their sounds in the confines of FM synthesis alone.

### Amplitude Levels

There are two parameters on each operator that control the overall level of output produced. These are the **Total Level Value** and the **"Key Scaling of Level" Value**.

The Total Level value, as one could probably surmise, controls the total level of output produced by an operator. This is expressed as an attenuation, where zero means "no reduction" in output level and increasing values (up to the maximum of 63) represent progressively quieter outputs. The exact conversion is 0.75 dB of attenuation per Total Level step, for a range of 0 dB to 47.25 dB of attenuation.

Total Level is really the only avenue of control the programmer has over the absolute volume of notes in a musical phrase, so anything pertaining to volume or velocity (in the MIDI sense of the terms) gets wedged into a Total Level adjustment immediately before each Key-On event.

The "Key Scaling of Level" Value (KSL) manages an effect where higher notes are played back at quieter levels than lower notes. This provides for a more accurate simulation of some types of instruments. KSL values are as follows:

KSL Value | Attenuation
----------|------------
0         | 0 dB (KSL disabled)
1         | 3 dB/octave
2         | 1.5 dB/octave
3         | 6 dB/octave

{{< note >}}These values are defined in a weird order. What can you do.{{< /note >}}

Rather than go on a long-winded explanation of how the math works, suffice it to say that this setting does what it says it does: Each time the frequency (expressed by "BLOCK" and "F NUM") doubles, the effective output of the operator is reduced by the number of decibels in the table. At the highest frequencies and the strongest KSL setting, the amount of adjustment can reach -42 dB.

{{< image src="ksl-frequency-attenuation-2052x.png"
    alt="Graph showing the relationship between octave blocks, frequency values, and attenuation levels for a KSL setting of -6 dB/octave."
    1x="ksl-frequency-attenuation-684x.png"
    2x="ksl-frequency-attenuation-1368x.png"
    3x="ksl-frequency-attenuation-2052x.png" >}}

### Envelope Rates and Levels

The lifecycle of a note as it goes from Key-On to Key-Off, simply referred to as its "envelope," involves several rate and level parameters: **Attack Rate**, **Decay Rate**, **Sustain Level**, and **Release Rate**. Together these are sometimes called "ADSR." There are also a few other parameters that can scale the rates and influence the transitions between these four stages.

Each operator spends its idle time with its attenuation at the maximum value, producing silence. When a Key-On event occurs, the "attack" stage is entered and the attenuation level is reduced by a specific value (influenced by the attack rate) as each sample is computed. Eventually the attenuation level reaches zero, meaning full output level has been reached, and the "decay" stage begins. From here, the attenuation level is increased by a value influenced by the decay rate, causing the output level to decrease. As the output decays, it is continually compared to the sustain level and, once it matches, the "sustain" stage begins. During sustain, all levels are held at their current values for as long as the note is being held. Eventually, a Key-Off signal arrives, starting the "release" stage. The attenuation level is increased by a value influenced by the release rate, until it reaches the maximum attenuation value. Once the maximum level is reached, the output is silent and the operator becomes idle again.

While the decay and release stages use a linear change in decibel level, the attack is more logarithmic in nature -- beginning sharply but slowing down as it "eases" into its peak level. The calculations for the attack use tiny lookup tables and integer math to produce a rather low-resolution stair-step pattern that contributes to the distinctive character of the OPL2's sound.

{{< image src="adsr-attenuation-2052x.png"
    alt="Graph showing the attenuation characteristics of ADSR envelopes, and the relevant parameters."
    1x="adsr-attenuation-684x.png"
    2x="adsr-attenuation-1368x.png"
    3x="adsr-attenuation-2052x.png" >}}

The rate units for attack, decay, and release are measured relative to time on a logarithmic scale. A decay or release traveling from zero dB attenuation to max attenuation takes approximately 15 times as long as the attack stage takes to perform the same amount of change. Typically the decay and release stages only need to travel partway through the scale -- either from zero dB attenuation to the sustain level, or from the sustain level to maximum attenuation -- so many envelopes finish these stages more quickly than the computed graph would suggest.

{{< image src="adsr-rates-2052x.png"
    alt="Graph showing the timing behavior of attack/decay/release rates."
    1x="adsr-rates-684x.png"
    2x="adsr-rates-1368x.png"
    3x="adsr-rates-2052x.png" >}}

If any of the three rates are set to zero, the envelope will pause indefinitely in the corresponding stage with no change in output level. This would typically not be done for attacks, since it would result in a note that never became loud enough to hear. It would also be of limited utility for releases, since it would cause notes to stick in the "on" state until another Key-On event restarted the envelope. Similarly, a rate of 15 would produce an instantaneous or almost-instantaneous progression through that particular stage of the envelope.

The Sustain Level parameter is simply an attenuation value, encoded in 3 dB steps for a total range of 0 dB to -42 dB. There is a special case for the value 15, which is interpreted as -93 dB. The higher the Sustain Level value, the quieter the output will be during the sustain stage.

The envelope's behavior can be further customized by changing the **Envelope Generator Type** parameter. When this is set to type 1, the envelope functions as we have described it here. When changed to type 0, however, the behavior of the sustain stage changes slightly: Envelope type 0 uses the sustain level as an inflection point where the envelope skips from the decay mode directly to the release mode. Type 0 envelopes do not play sustained tones while the Key-On parameter is held, instead producing relatively short constant-length notes. Due to this behavior, type 0 envelopes are sometimes referred to as "rhythm" or "percussion" envelopes, but that's not strictly all they can be used for.

{{< image src="envelope-types-2052x.png"
    alt="Comparison of Type 1 (Sustain) and Type 0 (Rhythm) envelope generator types."
    1x="envelope-types-684x.png"
    2x="envelope-types-1368x.png"
    3x="envelope-types-2052x.png" >}}

The last bit of envelope control available is **Key Scaling of Rate** (KSR). This is used to speed up all of the rate values on higher-frequency notes to simulate the behavior of real instruments. This cannot be turned off, but it can be switched between producing small or large amounts of change.

The KSR adjustment is calculated by taking the operator's current Octave Value, shifting it to the left by one bit position (effectively doubling it) and adding the "selected bit" from the operator's current Frequency Value to the result. This produces an intermediate value between 0 and 15. In small mode (KSR is 0), the result is scaled down by a factor of four, limiting the result to an integer value between 0 and 3. The final result of these calculations is called the **key scale value** (KSV).

The OPL2 internally uses **(_RATE_ &times; 4) + _KSV_** during each stage of envelope processing to compute an effective rate between 0 and 60 (clamped to that range if any of the values are excessive). The programmer can't do anything directly with this knowledge, but it does help form an intuition of the relative effect between the programmed attack/decay/release rates and the KSV. Namely, the highest frequencies in large mode could add 3.75 units to the requested rate, while the same frequencies in small mode could add 0.75 units. (And the lowest frequencies, as one might guess, get nothing added in either mode.)

I glossed over the meaning of "selected bit" in the KSV calculation above. This is controlled by the chip's **Note Select (Keyboard Split) Position** value: When 0, the "selected bit" is the most significant bit (bit 9) of the Frequency Value. When 1, the "selected bit" is the second-most significant bit (bit 8). This is _apparently_ backwards in the official Yamaha documentation, or every emulator is getting the behavior wrong. Either way, it's not really something that creates a huge audible difference in the output, and the game never sets Note Select to anything but zero during any of its music.

## OPL2 Cheat Sheet

If you followed me this far, this should probably make some amount of sense:

{{< image src="opl2-cheat-sheet-2052x.png"
    alt="Quick reference chart of all relevant OPL2 parameters and their effect on a single operator."
    1x="opl2-cheat-sheet-684x.png"
    2x="opl2-cheat-sheet-1368x.png"
    3x="opl2-cheat-sheet-2052x.png" >}}

This shows the basic structure of one operator, along with all of the parameters available to configure it. Each parameter is grouped by the register area it is controlled by (chip-wide, per-channel, or per-operator) and which part of the signal chain it affects (sine generation, envelopes, levels, or more than one element.) For clarity, this does not show the parameters related to CSM or Rhythm modes, which are not typically seen in most applications anyway.

The OPL2 isn't exactly complicated, it just straddles a lot of technical disciplines. It offers a great deal of control over the sounds it produces, but it's not always friendly or intuitive. But as musicians in the 1980s and 90s showed us, it can do amazing things and make lasting impressions on listeners.

## The Anatomy of a Song

The OPL2 has nine channels, meaning it is capable of playing nine simultaneous notes, but the music in this game (like many games of the era) only uses eight of them. Channel 1 is reserved for _sound effect_ playback, which has a unique sort of aesthetic that can be heard in games like _Commander Keen_ episodes four through six, or on some of the bonus items in _Wolfenstein 3D_. It is unknown if channel 1 was reserved consciously by Bobby Prince (the game's composer) in anticipation of the possibility of including AdLib sound effects, or if this was a convention imposed by the tools he was using.

Whatever the reason, the relatively limited number of channels and the structural requirements of music tend to make the channel reservations follow certain patterns. There are typically three drum channels (bass drum, snare drum, and various cymbals) one bass channel, three harmony channels, and one lead channel. Some songs use a dual-channel lead and sacrifice one of the harmony channels to get it.

There are no apparent rules that dictate how channels and their instruments are ordered, other than that the assignments generally don't change mid-song.

{{< aside class="fun-fact" >}}
**&#8544;&#8544;&#8544;&#8544;, &#8547;&#8547;&#8544;&#8544;, &#8548;&#8547;&#8544;&#8544;.**

A great many Bobby Prince compositions follow a **twelve-bar blues** progression, built on three chords that change in a repeating pattern every twelve measures of the song. The textbook example of this is the title screen music, a rendition of "Tush" by ZZ Top. Once you train yourself to hear it, you'll find it all over his work from _Commander Keen_ to _Duke Nukem 3D_.
{{< /aside >}}

## The Id Engine Sound Manager

The credits of the game include "Music Routines by Id Software" near the bottom of the list, and Id was known for open-sourcing its game code after it was no longer cutting edge. Doing a bit of digging, I was able to trace the lineage of their AdLib code and determine that the version used in this game came from a library file called the "Sound Manager v1.1d1" from _Catacomb 3-D_, a predecessor to _Wolfenstein 3D_ that Id released in November 1991.

The AdLib code in _Cosmo_ is essentially identical to that in _Catacomb 3-D_, with only a few modifications and glue code to make it work in this game's context. Based on the way it was compiled into the final executable, it is almost certain that Todd Replogle had access to the C source and inserted it into the code he was writing. (Other techniques, like sharing a compiled OBJ file and linking it in later, would've added additional code segments and other tell-tale evidence which did not occur here.)

id's Sound Manager was written by Jason Blochowiak, who is also credited with creating the [IMF file format]({{< relref "adlib-music-format#music-file-format" >}}) the music is encoded in. It was expanded greatly by the time _Wolfenstein 3D_ was released, but as of _Catacomb 3-D_, the only output types implemented were the PC speaker sound effects (which _Cosmo_ did not use) and AdLib/Sound Blaster music. There was preliminary code to support the Disney Sound Source (a relatively primitive sound effect device) and structures for fine AdLib music control supporting features beyond "play this data blob" and "stop playing it," but it was not usable at the time of release.

In this document, I will try to straddle the line between how the Sound Manager code was written and how the functions in _Cosmo_ actually work.

{{< boilerplate/function-cref SetPIT0Value >}}

The {{< lookup/cref SetPIT0Value >}} function configures channel 0 of the system's Programmable Interval Timer (PIT) with the provided counter `value`. This counter value can be thought of as a divisor -- the larger the value, the longer the counter must run during each timing period, and the slower the resulting timer frequency. [The PIT channels count in descending order at a constant rate of 105 &#x2215; 88 MHz]({{< relref "pc-speaker-and-timing-functions#a-taste-of-the-programmable-interval-timer" >}}) or 1,193,181.{{< overline >}}81{{< /overline >}} Hz, firing one period of output each time the counter reaches zero, thus the resulting timer frequency for an arbitrary `value` can be determined by **f = 1,193,181.{{< overline >}}81{{< /overline >}} &divide; `value`**. Each time this timer fires, interrupt vector 8 (also known as IRQ 0) is raised to the processor.

This function is basically identical to `SDL_SetTimer0()`[^SDL_SetTimer0] from Id Software's Sound Manager as used in _Catacomb 3-D_.

```c
void SetPIT0Value(word value)
{
    outportb(0x0043, 0x36);
```

The function begins with a call to {{< lookup/cref outportb >}} to write a byte to I/O port 43h, which is the command register on the system's Programmable Interval Timer. The value written (36h) has the following interpretation:

Bit Pattern (= 36h) | Interpretation
--------------------|---------------
00xxxxxx            | Select timer channel 0
xx11xxxx            | Access Mode: "Low byte, followed by high byte"
xxxx011x            | Mode 3: Square wave generator
xxxxxxx0            | 16-bit binary counting mode

This sets timer channel 0 to a reasonable state: It will output a square wave having a 50/50 duty cycle while counting in binary. The "access mode" configures how the 16-bit counter value will be broken into 8-bit chunks when it is next rewritten.

```c
    outportb(0x0040, value);
    outportb(0x0040, value >> 8);

    pit0Value = value;
}
```

The {{< lookup/cref outportb >}} to I/O port 40h (timer channel 0's data port) programs the new counter value into the PIT, following the convention agreed on in the "access mode" above. The low byte of `value` is written first, followed by the high byte. Whenever timer channel 0's counter reaches zero, this becomes the value that will be reloaded into the counter.

Lastly, the configured counter `value` is stashed in {{< lookup/cref pit0Value >}} for later use.

{{< boilerplate/function-cref SetInterruptRate >}}

The {{< lookup/cref SetInterruptRate >}} function configures channel 0 of the system's Programmable Interval Timer (PIT) with an interrupts-per-second value specified by `ints_second`. This is essentially a wrapper around {{< lookup/cref SetPIT0Value >}} that abstracts the timer's count rate away from the calling code.

As a consequence of how the Programmable Interval Timer channels are wired to the Programmable Interrupt Controller on the IBM PC, the value in `ints_second` becomes the number of times interrupt vector 8 fires each second.

This function is basically identical to `SDL_SetIntsPerSec()`[^SDL_SetIntsPerSec] from Id Software's Sound Manager as used in _Catacomb 3-D_.

```c
void SetInterruptRate(word ints_second)
{
    SetPIT0Value((word)(1192030L / ints_second));
}
```

There's not much to explain here that wasn't already explained in {{< lookup/cref SetPIT0Value >}}. The only curiosity is the use of the long value 1,192,030 Hz as the dividend in the calculation. As long established, all of the PIT channels run at one-twelfth of the NTSC 315 &#x2215; 22 MHz rate, so the expected value here should be rounded to 1,193,182 Hz instead. The difference in rates is 966 parts per million (PPM), which is roughly the equivalent of drifting one second every 15 minutes. Compared to even the cheapest wall clocks available, this accuracy is dismal.

I don't know and can't explain why this value was used. Assuming the 14.3 MHz crystals are true to their markings, this value is simply wrong. Regardless, the value survived into _Wolfenstein 3-D_ and later games by Apogee Software and 3D Realms -- Jim Dos&eacute;'s `TS_SetTimer()` function in both _Rise of the Triad_[^rottclock] and _Duke Nukem 3D_[^dukeclock] have identical values in their equivalent functions. I'm thinking perhaps the value was published inaccurately in some seminal text on PC systems programming that these developers consulted -- if you have any insights on this, [please let me know!](mailto:scott@smitelli.com)

_Quake_[^quakeclock] was quite a bit better at this, but still about 15 PPM off.

{{< boilerplate/function-cref ProfileCPUService >}}

The {{< lookup/cref ProfileCPUService >}} function is a small interrupt service routine used to benchmark the timing characteristics of the CPU relative to the system's Programmable Interval Timer. It really only makes sense in the context of the {{< lookup/cref ProfileCPU >}} function that installs it.

This function is basically identical to `SDL_TimingService()`[^SDL_TimingService] from Id Software's Sound Manager as used in _Catacomb 3-D_.

```c
void interrupt ProfileCPUService(void)
{
    profCountCPU = _CX;
    profCountPIT++;

    outportb(0x0020, 0x20);
}
```

This is an interrupt handler function, designed to be attached to interrupt vector 8 (which is the PIT channel 0 interrupt), which is also known as IRQ 0. Each time the timer channel fires, the value of the CX register is stored in {{< lookup/cref profCountCPU >}} using a Borland-specific language extension, and the {{< lookup/cref profCountPIT >}} value is incremented. Once all the variables have been adjusted, {{< lookup/cref outportb >}} sends a nonspecific end-of-interrupt message (20h) to the system's Programmable Interrupt Controller via I/O port 20h. This acknowledges the IRQ and permits it to fire again later.

If the intent of this function is inscrutable, hopefully {{< lookup/cref ProfileCPU >}} will clear it up.

{{< boilerplate/function-cref ProfileCPU >}}

The {{< lookup/cref ProfileCPU >}} function measures the execution speed of the CPU relative to the system's Programmable Interval Timer, and records the number of busy loop iterations the CPU requires to generate various delay times. The computed delay values are stored in {{< lookup/cref wallclock10us >}}, {{< lookup/cref wallclock25us >}}, and {{< lookup/cref wallclock100us >}}. These values should be passed to {{< lookup/cref WaitWallclock >}} to produce a delay of (approximately) the required length.

This function is basically identical to `SDL_InitDelay()`[^SDL_InitDelay] from Id Software's Sound Manager as used in _Catacomb 3-D_.

```c
void ProfileCPU(void)
{
    int trial;
    word loops_ms;

    setvect(8, ProfileCPUService);
    SetInterruptRate(1000);
```

This function begins by setting interrupt vector 8 to a profiling function, {{< lookup/cref ProfileCPUService >}}. The original interrupt handler is not saved here -- that already happened in {{< lookup/cref StartAdLib >}} immediately before this function was called. {{< lookup/cref name="SetInterruptRate" text="SetInterruptRate(1000)" >}} sets the effective timer frequency to 1,000 Hz or one interrupt per millisecond.

From this point, the {{< lookup/cref ProfileCPUService >}} function runs asynchronously 1,000 times per second. Each time it runs, it sets {{< lookup/cref profCountCPU >}} to the current value held in the CX register and increments {{< lookup/cref profCountPIT >}}. The remaining code in this function relies on the external changes to these two variables.

```c
    for (trial = 0, loops_ms = 0; trial < 10; trial++) {
        _DX = 0;
        _CX = 0xffff;
        profCountPIT = _CX;

wait4zero:
        asm or    [profCountPIT],0
        asm jnz   wait4zero

wait4one:
        asm test  [profCountPIT],1
        asm jnz   done
        asm loop  wait4one
done:
        if (0xffff - profCountCPU > loops_ms) {
            loops_ms = 0xffff - profCountCPU;
        }
    }
```

This is the measurement loop. `trial` is the iteration control value that causes the loop to run ten times. `loops_ms` starts at 0, and eventually becomes the sole output of the loop. The main body of the loop contains a bunch of inline assembly and Borland register keywords.

The DX register is set to zero, which doesn't appear to be a significant assignment -- nothing reads this value and it does not influence the behavior of any of the subsequent instructions. CX is set to FFFFh, which should be interpreted as the value 65,535. {{< lookup/cref profCountPIT >}} is also set to the FFFFh value held in CX, but in this context it could be more naturally thought of as the number -1.

A busy loop is entered next. As long as {{< lookup/cref profCountPIT >}} is not 0, jump back to the `wait4zero:` label and try again. We just set {{< lookup/cref profCountPIT >}} to -1, so this loop will spin until the timer interrupt fires and increments {{< lookup/cref profCountPIT >}} to 0. As soon as that happens, execution moves onto the next test.

Another busy loop occurs. As long as {{< lookup/cref profCountPIT >}} is not 1, loop back to the `wait4one:` label and try again. We know that {{< lookup/cref profCountPIT >}} just became 0 in the previous loop; that's what permitted it to enter the current loop. The only way for it to become 1 is to wait until the timer ticks again. The use of `loop` is clever -- each time the `loop` instruction executes, it implicitly decrements the CX register. (If CX decrements to zero, `loop` will terminate, but if that happens here the CPU is running wicked fast and the whole profiling methodology becomes invalid.)

Once the timer ticks again and {{< lookup/cref profCountPIT >}} increments to 1, the jump to the `done:` label is taken and execution moves on. But something else has occurred: The timer interrupt handler copies the value in CX to {{< lookup/cref profCountCPU >}} each time it runs. Since CX holds an indication of how many times the busy loop ran, {{< lookup/cref profCountCPU >}} holds this value now too.

More concretely, the value FFFFh - {{< lookup/cref profCountCPU >}} is the number of times the second busy loop ran, and the second busy loop is tightly governed by two consecutive ticks of a 1,000 Hz clock. Therefore FFFFh - {{< lookup/cref profCountCPU >}} is the number of busy loop iterations that occurred in 1/1,000th of a second (one millisecond). If the most recently measured value is larger than `loops_ms`, that becomes its new value. The highest (i.e. fastest-performing) value for `loops_ms` after ten trials is the final result.

```c
    loops_ms += loops_ms / 2;
    wallclock10us  = loops_ms / (1000 / 10);
    wallclock25us  = loops_ms / (1000 / 25);
    wallclock100us = loops_ms / (1000 / 100);
```

More optimism occurs, and `loops_ms` is set to 150% of its observed value. From here, it is scaled into three timing variables: {{< lookup/cref wallclock10us >}} is the calculated number of busy loop iterations the CPU can perform in 10 microseconds (&micro;s). {{< lookup/cref wallclock25us >}} and {{< lookup/cref wallclock100us >}} follow the pattern, calculating values for 25 &micro;s and 100 &micro;s respectively.

```c
    SetPIT0Value(0);
    setvect(8, savedInt8);
}
```

The function ends with some cleanup. {{< lookup/cref name="SetPIT0Value" text="SetPIT0Value(0)" >}} sets the timer count value back to _65,536_, restoring the PC's default 18.2 Hz timer rate. {{< lookup/cref setvect >}} reinstalls the function saved in {{< lookup/cref savedInt8 >}} to interrupt vector 8, returning the timer to the same configuration it was in when this function was entered.

{{< boilerplate/function-cref WaitWallclock >}}

The {{< lookup/cref WaitWallclock >}} function creates an artificial delay using a CPU busy loop, controlled by the iteration count specified in `loops`.

This function is basically identical to `SDL_Delay()`[^SDL_Delay] from Id Software's Sound Manager as used in _Catacomb 3-D_.

```c
void WaitWallclock(word loops)
{
    if (loops == 0) return;

    _CX = loops;
```

The function begins with a quick sanity check: If the value requested in `loops` is zero, no delay is appropriate and the function should return immediately. (If allowed to run anyway, the 16-bit nature of the below `loop` instruction would actually run for 65,536 iterations, which is not desirable at all.)

The value in `loops` is copied into the CPU's CX register, which sets up the subsequent loop.

```c
wait:
    asm test  [profCountPIT],0
    asm jnz   done
    asm loop  wait
done:
    ;
}
```

This assembly code looks both strange and familiar; it _exactly_ matches the structure of a loop in the {{< lookup/cref ProfileCPU >}} function. This is the intent, as we need to make sure that the delay loop is running the exact same instructions and taking the same number of CPU cycles as the calibration loop did.

{{< lookup/cref profCountPIT >}} was abandoned after {{< lookup/cref ProfileCPU >}} finished executing. It holds some nonzero number, most likely 1, and it doesn't matter. A `test` instruction between anything and zero always returns zero, so the `jnz` jump never occurs.

The `loop` instruction is doing all the work here. Each time it runs, it decrements CX and, if CX is not zero, it jumps back to the `wait:` label. The end effect is that the busy loop runs the number of times the caller requested it to, performing no other useful work.

The rest of the function is simply syntactic ceremony to appease the compiler and maintain timing parity.

{{< boilerplate/function-cref SetAdLibRegister >}}

The {{< lookup/cref SetAdLibRegister >}} function writes one `data` byte to the AdLib register at address `addr`, assuming the hardware is present at the standard I/O ports.

This function is basically identical to `alOut()`[^alOut] from Id Software's Sound Manager as used in _Catacomb 3-D_.

```c
void SetAdLibRegister(byte addr, byte data)
{
    asm pushf

    disable();
```

This function performs some tight timing operations, so it's necessary to suspend interrupt processing while it runs. The assembly instruction `pushf` pushes the current state of the CPU's FLAGS register (most importantly the Interrupt Flag) onto the stack. {{< lookup/cref disable >}} then turns interrupts off. From this point forward, the code running here has exclusive control of the CPU.

```c
    asm mov   dx,0x0388
    asm mov   al,[addr]
    asm out   dx,al
    asm in    al,dx
    asm in    al,dx
    asm in    al,dx
    asm in    al,dx
    asm in    al,dx
    asm in    al,dx
```

The `out` instruction sends the value in `addr` to I/O port address 388h, which is the **address register** for the AdLib. The temporary involvement of the DX and AL registers is simply a constraint of the x86 instruction set.

The six `in` instructions repeatedly read the AdLib's **status register** at I/O port address 388h into the AL register. The actual value read is irrelevant; the OPL2 chip in the AdLib requires recovery time of about 3.4 &micro;s after writing to the address register before another write can occur, and these instructions provide that delay.

{{< aside class="armchair-engineer" >}}
**Cycle Pincher**

According to the OPL2 docs, the register address latches its value, meaning that if the programmer intends to perform multiple writes to the same register, it is not necessary to re-send the address byte. The AdLib's design doesn't include anything that would obviously prevent this from working, so it might have been possible to redesign things to save a few cycles if it was known ahead of time that multiple writes to the same register were planned.

Is the added complexity to do that worth it? Eh, maybe not.
{{< /aside >}}

```c
    asm mov   dx,0x0389
    asm mov   al,[data]
    asm out   dx,al

    asm popf
```

Another `out` instruction follows, this time sending the value in `data` to I/O port address 389h, which is the **data register** for the AdLib. The `popf` instruction pops the most recently pushed value off the stack and installs it into the CPU's FLAGS register. This restores the flags to the state they were in when `pushf` was executed earlier, which also has the effect of restoring the Interrupt Flag to the state it was in before.

```c
    asm mov   dx,0x0388
    asm in    al,dx
    asm in    al,dx
    asm in    al,dx
    asm in    al,dx
    asm in    al,dx
    asm in    al,dx
    asm in    al,dx
    asm in    al,dx
    asm in    al,dx
    asm in    al,dx
    asm in    al,dx
    asm in    al,dx
    asm in    al,dx
    asm in    al,dx
    asm in    al,dx
    asm in    al,dx
    asm in    al,dx
    asm in    al,dx
    asm in    al,dx
    asm in    al,dx
    asm in    al,dx
    asm in    al,dx
    asm in    al,dx
    asm in    al,dx
    asm in    al,dx
    asm in    al,dx
    asm in    al,dx
    asm in    al,dx
    asm in    al,dx
    asm in    al,dx
    asm in    al,dx
    asm in    al,dx
    asm in    al,dx
    asm in    al,dx
    asm in    al,dx
}
```

That's 35 `in`s from the AdLib status register at I/O port address 388h, with the returned values in AL being ignored, generating the 23.5 &micro;s recovery time required by the OPL2 chip. Interrupts are enabled here, so this code could very well take longer to execute due to those interruptions, but the OPL2 is guaranteed to have recovered from the data write by the time this function returns.

{{< aside class="armchair-engineer" >}}
**Math Hat**

It's not readily apparent how the value of 35 `in`s was selected to delay for 23.5 &micro;s, or how six `in`s earlier achieved 3.4 &micro;s. The speed of the `in` instruction is governed by the bus frequency, not the CPU frequency (although historically they both ran at the same speed until CPUs in PC clones became too fast). The highest frequency that any AT/ISA bus is _supposed_ to go is 8 MHz. My best guess is that these figures were based around an 8 MHz bus that takes 5 clock cycles to write each I/O byte.

The math suggests that it should actually need _38_ `in` instructions to generate the required delay instead of 35, but this code has been working for over thirty years and I'm in no position to second-guess it.
{{< /aside >}}

Based on some commented-out blocks in the original code,[^alOut] it appears the {{< lookup/cref wallclock10us >}} delay was originally intended to produce the address write delay, and {{< lookup/cref wallclock25us >}} was designed for the data write delay. Evidently that approach was abandoned in favor of just whacking the bus a fixed number of times.

{{< boilerplate/function-cref AdLibService >}}

The {{< lookup/cref AdLibService >}} function streams chunks of music data to the AdLib hardware at the appropriate time. This function is called by the {{< lookup/cref TimerInterruptService >}} function at a rate of 560 Hz if the AdLib hardware has been activated. Each execution of this function is called a music **tick**.

As documented in the [IMF file format]({{< relref "adlib-music-format#music-file-format" >}}) section, the music data contains a stream of raw AdLib register/data byte pairs interleaved with 16-bit delay values. The delay is measured in music ticks.

This function is basically identical to `SDL_ALService()`[^SDL_ALService] from Id Software's Sound Manager as used in _Catacomb 3-D_.

```c
void AdLibService(void)
{
    if (!enableAdLib) return;
```

{{< lookup/cref enableAdLib >}} is the "soft" control that enables or disables music playback. If it is false, this function should do nothing.

```c
    while (musicDataLeft != 0 && musicNextDue <= musicTickCount) {
        byte chunkaddr, chunkdata;
        word chunk = *musicDataPtr++;

        musicNextDue = musicTickCount + *musicDataPtr++;

        asm mov   dx,[chunk]
        asm mov   [chunkaddr],dl
        asm mov   [chunkdata],dh

        SetAdLibRegister(chunkaddr, chunkdata);

        musicDataLeft -= 4;
    }

    musicTickCount++;
```

This `while` loop operates on two conditions:

1. The decrementing value in {{< lookup/cref musicDataLeft >}} must be nonzero, indicating there is more music data to play.
2. The {{< lookup/cref musicNextDue >}} tick timestamp must be less than or equal to {{< lookup/cref musicTickCount >}}, indicating that the deadline for playing this chunk is either right now or in the past.

As long as both conditions are true, the AdLib address/data pair is read from {{< lookup/cref musicDataPtr >}} into the local `chunk` variable and the source pointer is advanced. Each of these is an 8-bit value, but they are read and handled as a 16-bit chunk here.

{{< lookup/cref musicDataPtr >}} is read and advanced again, this time to get the delay value that accompanies the music chunk that was just read. This is added to the current value of {{< lookup/cref musicTickCount >}} to determine the deadline tick timestamp for the next iteration of this loop: {{< lookup/cref musicNextDue >}}. The delay value is often zero, which will cause another iteration of this `while` loop before the current music tick completes.

Following this, a brief dabble of assembly splits the 16-bit `chunk` variable into its 8-bit components, `chunkaddr` and `chunkdata`. These are sent to the AdLib hardware by the call to {{< lookup/cref SetAdLibRegister >}}.

{{< lookup/cref musicDataLeft >}} is decremented by four to reflect the fact that the 16-bit {{< lookup/cref musicDataPtr >}} pointer has advanced twice, for a four-byte change in position. The `while` loop repeats as long as music data still remains and there are more chunks of data due to be sent during this tick.

When there are no more chunks to be sent in the current tick, {{< lookup/cref musicTickCount >}} is incremented to track the passage of time.

{{< aside class="fun-fact" >}}
**I'm Bored!**

Don't worry about {{< lookup/cref musicTickCount >}} or any related values overflowing. They're 32 bits wide, and would take something like 88 days of uninterrupted playback to wrap back to zero.
{{< /aside >}}

```c
    if (musicDataLeft == 0) {
        musicDataPtr = musicDataHead;
        musicDataLeft = musicDataLength;
        musicTickCount = musicNextDue = 0;
    }
}
```

The remainder of the function handles the task of repeating the music once the end of the data has been reached. This is indicated by {{< lookup/cref musicDataLeft >}} becoming zero.

Restarting the music is a simple matter of resetting {{< lookup/cref musicDataPtr >}} to point to the start of the music data (which {{< lookup/cref musicDataHead >}} always points to), and updating the {{< lookup/cref musicDataLeft >}} counter to show that the entire length of the music data ({{< lookup/cref musicDataLength >}}) is ready and waiting to be played.

{{< lookup/cref musicTickCount >}} and {{< lookup/cref musicNextDue >}} are both zeroed out as well, guaranteeing that the next music tick that calls this function will send _something_ to the AdLib without any delay. It should be noted that this essentially discards the final delay value in the music data, and substitutes zero in its place. Fortunately all of the music files that ship with the game already end with a zero, so this does not interfere with the looping behavior. But custom-made music should exercise caution here to ensure there are no skips or clicks when the loop occurs.

All these steps are essentially the same as what happens in {{< lookup/cref SwitchMusic >}} to start music playback.

{{< boilerplate/function-cref DetectAdLib >}}

The {{< lookup/cref DetectAdLib >}} function interrogates the default AdLib I/O address to check if one is installed, and initializes the hardware if it is there. If an AdLib card is installed in the system, this function returns true. In all other cases, false is returned.

The AdLib card, and the Yamaha OPL2 chip it's built around, are almost exclusively write-only devices. There are only three bits of information that the host system can read: **IRQ** (did either of the two [on-board timers](#on-board-timers) fire?), **T1**, and **T2 FLAG** (which timer was it?). The programmer can reset the timers, enable/disable them, and change the rate they fire at. By carefully manipulating the timers, the behavior can be observed to make a pretty good guess as to whether an OPL2 (or something that behaves like it) is present at the expected I/O port address.

This function is basically identical to `SDL_DetectAdLib()`[^SDL_DetectAdLib] from Id Software's Sound Manager as used in _Catacomb 3-D_. The detection methodology is identical to the one proposed by Tero T&ouml;tt&ouml; in the Ad Lib Music Synthesizer Card Programming Guide.[^almscpg]

```c
bool DetectAdLib(void)
{
    byte oplstatus1, oplstatus2;
    int addr;

    SetAdLibRegister(0x04, 0x60);
    SetAdLibRegister(0x04, 0x80);

    oplstatus1 = inportb(0x0388);
```

{{< lookup/cref SetAdLibRegister >}} directly manipulates the register contents of the AdLib's OPL2 chip. Register address 4h contains flags and options that control timer behavior. The interpretation of the two writes (60h followed by 80h) is as follows:

Bit Pattern (= 60h) | Interpretation
--------------------|---------------
x1xxxxxx            | Enable T1 MASK (prevent flag setting)
xx1xxxxx            | Enable T2 MASK
xxxxxx0x            | Disable T2 START
xxxxxxx0            | Disable T1 START

This prevents both timers from setting their respective flags, and prevents them from counting in the first place.

Bit Pattern (= 80h) | Interpretation
--------------------|---------------
1xxxxxxx            | Reset all timer/interrupt flags

This invokes a command which zeroes out all of the timer status flags. Due to a quirk of the OPL2's operation, the request to clear the flag state must be made in isolation -- these two writes _cannot_ be combined into a single write of the value C0h.

The net effect of these writes should be to pause the timers and reset their output flags. An OPL2 chip in this state would be expected to have all of its timer status bits clear, and they should not retrigger themselves at any point. The status is captured with an {{< lookup/cref inportb >}} from the AdLib status port at 388h, which is saved in `oplstatus1`.

```c
    SetAdLibRegister(0x02, 0xff);
    SetAdLibRegister(0x04, 0x21);

    WaitWallclock(wallclock100us);

    oplstatus2 = inportb(0x0388);
```

This is the second step of the detection process. AdLib register address 2h is the Timer 1 Preset Value, which is the byte value that is loaded into the incrementing counter within this timer each time it overflows and fires. {{< lookup/cref SetAdLibRegister >}} sets this to the fastest rate, FFh, specifying that the timer should fire every 80 &micro;s.

The next call to {{< lookup/cref name="SetAdLibRegister" text="SetAdLibRegister(0x04, ...)" >}} configures timer 1 to run, while leaving timer 2 disabled. The exact interpretation of the 21h byte is:

Bit Pattern (= 21h) | Interpretation
--------------------|---------------
x0xxxxxx            | Disable T1 MASK (permit flag setting)
xx1xxxxx            | Enable T2 MASK
xxxxxx0x            | Disable T2 START
xxxxxxx1            | Enable T1 START

{{< lookup/cref WaitWallclock >}} is called with the calculated {{< lookup/cref wallclock100us >}} value, producing a wait of at least 100 &micro;s regardless of the CPU speed of the current system. Since timer 1 has been configured to fire every 80 &micro;s, the expectation is that the timer will have fired and set its flag bits by the time {{< lookup/cref WaitWallclock >}} returns.

{{< lookup/cref inportb >}} captures the OPL2's timer status byte to `oplstatus2` so this assertion can be checked.

```c
    SetAdLibRegister(0x04, 0x60);
    SetAdLibRegister(0x04, 0x80);

    if ((oplstatus1 & 0xe0) == 0 && (oplstatus2 & 0xe0) == 0xc0) {
        /* AdLib is present; perform initialization steps */
        ...

        return true;
    }

    return false;
}
```

Before moving on, the timer configuration is brought back to its initial state. The same {{< lookup/cref SetAdLibRegister >}} writes from the start of this function are performed, causing the same result (deactivating both timers).

To actually determine the presence of an AdLib, the two sampled timer status bytes must be checked. All of the _defined_ status bits (bits 7&ndash;5) in `oplstatus1` are expected to be zero:

Bit Pattern (= 0h) | Interpretation
-------------------|---------------
0xxxxxxx           | IRQ has not occurred
x0xxxxxx           | Timer 1 has not overflowed
xx0xxxxx           | Timer 2 has not overflowed

If this looks good, `oplstatus2` should then have the following bits set:

Bit Position (= C0h) | Interpretation
---------------------|---------------
1xxxxxxx             | IRQ occurred
x1xxxxxx             | Timer 1 overflowed
xx0xxxxx             | Timer 2 has not overflowed

If both of these values match, it's a pretty good bet that there is an AdLib, or at least _something_ with OPL2-compatible timer functionality, at the expected I/O port address. Perform the initialization steps (detailed below) and return true to let the caller know that the hardware is present and ready to use.

Otherwise there is no AdLib present at the default I/O address. Return false to indicate this.

### AdLib Initialization

If an AdLib card is found, the detection function also resets it to a known base state to ensure no previous operations left undesirable parameters in the hardware's registers.

```c
        for (addr = 0x01; addr <= 0xf5; addr++) {
            SetAdLibRegister(addr, 0);
        }

        SetAdLibRegister(0x01, 0x20);
        SetAdLibRegister(0x08, 0);
```

The OPL2's register space spans from addresses 1h to F5h, with some gaps in a few spots. The `for` loop steamrolls over the entire range, calling {{< lookup/cref SetAdLibRegister >}} to set all parameter values to zero. Writing to nonexistent register addresses doesn't appear to cause any undesirable effects, but no useful function is performed during those iterations.

{{< lookup/cref name="SetAdLibRegister" text="SetAdLibRegister(0x01, 0x20)" >}} turns on the "Wave Select" Enable bit. This drops compatibility with the original OPL, and permits the OPL2 to access all four of its [sine wave variants](#waveform-selection). {{< lookup/cref name="SetAdLibRegister" text="SetAdLibRegister(0x08, 0)" >}} is slightly redundant, as this register was already cleared during the preceding `for` loop, but it turns off the [Composite Sine Wave Speech Modeling mode](#composite-sine-wave-speech-modeling) and sets the [Note Select position](#envelope-rates-and-levels) to zero. These parameters, when enabled, do nothing but make the output behave strangely, and none of the music files ever change these values to anything else.

{{< boilerplate/function-cref TimerInterruptService >}}

The {{< lookup/cref TimerInterruptService >}} function handles interrupts that occur on interrupt vector 8 (IRQ 0), which is wired to channel 0 of the system's Programmable Interval Timer. The timer channel ticks at a rate of 560 Hz (if the AdLib hardware is enabled) or 140 Hz (if the AdLib hardware is not enabled). Each time the timer ticks, this function is called to update the sounds being played by the PC speaker and/or the AdLib.

Interrupts enable a primitive form of multitasking. Regardless of what is happening elsewhere in the program -- even if execution is stuck in an infinite loop somewhere -- timer interrupts will still occur and this function will continue running periodically as requested.

This function is a heavily reworked variant of `SDL_t0Service()`[^SDL_t0Service] from Id Software's Sound Manager as used in _Catacomb 3-D_. Several operations on junk variables have been removed since they don't appear to pertain to any interesting unused functionality.

```c
void interrupt TimerInterruptService(void)
{
    static word count = 1;
```

The `interrupt` keyword tells the compiler to handle this function a little differently -- it must explicitly save every single CPU register on entry, restore them all before returning, and use the special "interrupt return" instruction to restore the CPU flags while returning to the interrupted code. It also needs to be very explicit when addressing the data or extra segments, because they are not guaranteed to be pointing anywhere useful.

`count` tracks the number of times this function has been called, retaining its value across calls through use of the `static` keyword.

```c
    if (isAdLibServiceRunning == true) {
        AdLibService();

        if (count % 4 == 0) {
            PCSpeakerService();
        }

        count++;
    } else {
        PCSpeakerService();

        count++;
    }
```

Execution takes one of two paths here. If {{< lookup/cref isAdLibServiceRunning >}} is true, we know we're running at the 560 Hz rate. {{< lookup/cref AdLibService >}} should be called every time, but {{< lookup/cref PCSpeakerService >}} should only be called every fourth time so PC speaker sound effects continue to play at the expected 140 Hz rate.

If {{< lookup/cref isAdLibServiceRunning >}} wasn't true, we know we're already running at the PC speaker's 140 Hz rate and the AdLib service should not be called at all. In that case, simply call {{< lookup/cref PCSpeakerService >}} unconditionally.

{{< note >}}{{< lookup/cref PCSpeakerService >}} is also responsible for maintaining the game tick counter, which governs the speed of the entire game.{{< /note >}}

Regardless of the path taken through this code, the `count` value is incremented. Because this is only 16 bits wide, it overflows back to zero every few minutes. This is not a problem in practice, because modulo division by four continues to work as expected in both cases (`65536 % 4 == 0 % 4`).

```c
    asm mov   ax,[WORD PTR timerTickCount]
    asm add   ax,[WORD PTR pit0Value]
    asm mov   [WORD PTR timerTickCount],ax
    asm jnc   acknowledge
    savedInt8();
    asm jmp   done
acknowledge:
    outportb(0x0020, 0x20);
done:
    ;
}
```

{{< note >}}Be careful with {{< lookup/cref timerTickCount >}} and {{< lookup/cref pit0Value >}} here; they are both declared as `dword`, but here they are explicitly accessed and treated as 16-bit values. They behave as `word`s in all contexts where they appear.{{< /note >}}

The remaining code drops into assembly for some fun with the CPU flags. {{< lookup/cref timerTickCount >}} and {{< lookup/cref pit0Value >}} are added together, and the result is written back to {{< lookup/cref timerTickCount >}}. This essentially inverts the operation of the PIT. Recall that PIT channel 0 starts at the configured {{< lookup/cref pit0Value >}}, decrements at a fixed reference rate until reaching zero, then this function is called. By adding {{< lookup/cref pit0Value >}} to an accumulator variable each time this function runs, the total number of fixed reference ticks over time can be obtained.

The reference rate of the PIT timers is 1.193{{< overline >}}18{{< /overline >}} MHz, and the storage space allocated for {{< lookup/cref timerTickCount >}} is 16 bits wide, meaning it overflows and wraps to zero before reaching 65,536. Dividing the former by the latter, we discover that this value overflows 18.2 times per second. This seems familiar.

It seems familiar because this is exactly how PIT channel 0 worked in its default configuration, before the game messed with it. The PC boots with a value of 0 in PIT channel 0, which means the reference clock has to tick 65,536 times for it to wrap around again and fire. This ends up occurring at a rate of 18.2 Hz, which is the default system timer rate the PC boots with. {{< lookup/cref timerTickCount >}} is a clever variable that always overflows at a rate of 18.2 Hz, no matter what rate the interrupt handler function is being called at.

The `jnc` instruction, meaning "jump if no carry," jumps to the `acknowledge:` label as long as the `add` instruction did not cause an overflow. Generally this will be the more common case. {{< lookup/cref outportb >}} is called to send a nonspecific end-of-interrupt signal (20h) to the Programmable Interrupt Controller at I/O port 20h, acknowledging the IRQ, and execution finds its way to the end of the function.

If the `add` _did_ overflow, the jump to `acknowledge:` is not taken and execution falls to the {{< lookup/cref savedInt8 >}} call. This invokes the handler for interrupt vector 8 that was present when the game was started. Typically this will point to BIOS code that performs housekeeping tasks. One of BIOS' more important timer-related jobs is maintaining the time-of-day clock. If {{< lookup/cref savedInt8 >}} were not called at the correct 18.2 Hz rate (or not called at all) the time and date reported by BIOS could drift badly. On this path, the saved interrupt handler can be trusted to acknowledge the IRQ before it returns, so `jmp` takes us directly to the `done:` label without further action.

{{< boilerplate/function-cref InitializeInterruptRate >}}

The {{< lookup/cref InitializeInterruptRate >}} function sets up the system timer interrupt rate depending on whether or not the AdLib hardware is enabled.

This function is basically identical to `SDL_SetTimerSpeed()`[^SDL_SetTimerSpeed] from Id Software's Sound Manager as used in _Catacomb 3-D_.

```c
void InitializeInterruptRate(void)
{
    word rate;

    if (isAdLibServiceRunning == true) {
        rate = 560;
    } else {
        rate = 140;
    }

    SetInterruptRate(rate);
}
```

Compared to most of the AdLib functions, this one is short and sweet. If {{< lookup/cref isAdLibServiceRunning >}} is true, the timer interrupt `rate` should be set to 560 Hz. Otherwise, the `rate` should be one-quarter that amount: 140 Hz. Once the appropriate value has been determined, it is passed to {{< lookup/cref SetInterruptRate >}} to become the active timer rate.

{{< boilerplate/function-cref SetMusicState >}}

The {{< lookup/cref SetMusicState >}} function enables or disables AdLib output based on the value of `state`. Calling this function with a true value will enable the AdLib if it is present, and calling it with a false value will disable it. In either case, any currently-playing music is stopped and the system timer interrupt rate is set appropriately.

This function is a stripped-down and reworked (to the point of almost nonsensical indirection) variant of `SD_SetMusicMode()`[^SD_SetMusicMode] from Id Software's Sound Manager as used in _Catacomb 3-D_. Several operations on junk variables have been removed since they don't appear to pertain to any interesting unused functionality.

```c
bool SetMusicState(bool state)
{
    bool found;

    FadeOutAdLibPlayback();

    switch (state) {
    case false:
        found = true;
        break;

    case true:
        if (isAdLibPresentPrivate) {
            found = true;
        }
        break;

    default:
        found = false;
        break;
    }

    if (found) {
        isAdLibServiceRunning = state;
    }
```

This sure is... something. The function begins innocently enough by calling {{< lookup/cref FadeOutAdLibPlayback >}}, a function that ostensibly fades out any music that is currently playing. This is actually a surprisingly difficult thing to do in the constraints of OPL2 programming, which is probably why the "fade" part was never implemented. This actually cuts the music off abruptly.

The `switch` construct decodes the `state` variable, which by convention is either true or false and shouldn't satisfy the `default:` case. The usage of `found` is just confusing, and it introduces a potential bug: In the case where `state` is true but {{< lookup/cref isAdLibPresentPrivate >}} is false, the `found` variable will contain uninitialized stack garbage.

This whole thing could be replaced with `isAdLibServiceRunning = isAdLibPresentPrivate ? state : false` while still getting essentially the same answer. The apparent reason for all of the extra code is because `state` was originally designed to be an enumeration type, supporting not just on/off values but different music playback hardware devices that could be selected through one interface. The use of a `switch` statement and the found/not found handling makes a little more sense in that light, but even the later modifications for _Wolfenstein 3D_ still only had two modes here: off and AdLib.

```c
    InitializeInterruptRate();

    return found;
}
```

Having (potentially) changed the value in {{< lookup/cref isAdLibServiceRunning >}}, the system timer interrupt rate may need to be adjusted. The call to {{< lookup/cref InitializeInterruptRate >}} accomplishes this.

Finally the value in `found` is returned to the caller. It's not really useful for any purpose, and none of the callers do anything with it, but it is there.

{{< boilerplate/function-cref StartAdLib >}}

The {{< lookup/cref StartAdLib >}} function detects and initializes the AdLib hardware if it is present, installs the interrupt handler necessary to run the AdLib and PC speaker services, and measures values for CPU-based time delays.

This function is a somewhat reduced and modified variant of `SD_Startup()`[^SD_Startup] from Id Software's Sound Manager as used in _Catacomb 3-D_. Several operations on junk variables have been removed since they don't appear to pertain to any interesting unused functionality.

```c
void StartAdLib(void)
{
    if (isAdLibStarted) return;

    skipDetectAdLib = false;
```

The function begins with a safety check: If {{< lookup/cref isAdLibStarted >}} is already true, there is no need to run this process again. Return early in this case.

Otherwise, set the global {{< lookup/cref skipDetectAdLib >}} variable to false. In the original code, this could be set to true sometime later in the function based on command-line parameters used to start the game, but that code was either removed or conditionally commented out. This skip is always false and never changes.

```c
    savedInt8 = getvect(8);

    ProfileCPU();

    setvect(8, TimerInterruptService);
```

No matter if an AdLib card is present or not, the system timer interrupt is replaced. Before this happens, the old interrupt service routine is read via {{< lookup/cref name="getvect" text="getvect(8)" >}} and stored in {{< lookup/cref savedInt8 >}} for safekeeping. This happens before the call to {{< lookup/cref ProfileCPU >}}, since the tests performed by that function replace the timer interrupt handler.

{{< lookup/cref ProfileCPU >}} sets up some timing measurements that will be required later during the AdLib detection stage.

{{< lookup/cref setvect >}} is used to install the game's {{< lookup/cref TimerInterruptService >}} into interrupt vector 8. Once this completes, the system timer will begin firing the game's interrupt service regularly and asynchronously.

```c
    musicTickCount = 0;

    SetMusicState(false);
```

{{< lookup/cref musicTickCount >}} is zeroed, as it is in many other places. {{< lookup/cref name="SetMusicState" text="SetMusicState(false)" >}} disables the AdLib output -- at least temporarily -- thus causing the system timer to run at the slower "PC speaker only" speed without attempting to play any music.

```c
    if (!skipDetectAdLib) {
        isAdLibPresentPrivate = DetectAdLib();
    }

    isAdLibStarted = true;

    isAdLibPresent = DetectAdLib();
}
```

If {{< lookup/cref skipDetectAdLib >}} is false, which is always the case, {{< lookup/cref DetectAdLib >}} is called to detect (and initialize, if appropriate) the AdLib hardware. {{< lookup/cref isAdLibPresentPrivate >}} receives the result of the detection: true if the card is present, and false if not. {{< lookup/cref isAdLibStarted >}} is then set to true to prevent this function from running again.

The function ends with a _Cosmo_-specific modification: {{< lookup/cref DetectAdLib >}} is called a _second_ time, and the result is stored in a _second_ variable named {{< lookup/cref isAdLibPresent >}}. This will (or should, anyway) hold the same value that {{< lookup/cref isAdLibPresentPrivate >}} does. The difference between the two is that the private variable has internal linkage, and thus isn't visible to anything outside of the C file where it is declared, and the non-private variable can be seen everywhere.

{{< aside class="speculation" >}}
**Whatever works.**

If I had to guess about why this code ended up with two AdLib detection calls saved in two variables... I'd say having the first call to {{< lookup/cref DetectAdLib >}} wrapped in a conditional either confused or scared the author, who didn't fully understand the different paths the code could take. I'm sure they knew they could just chop `static` off the variable declaration and call it a day, but they weren't sure that the detection (and thus the assignment) actually occurred in every circumstance.
{{< /aside >}}

{{< boilerplate/function-cref StopAdLib >}}

The {{< lookup/cref StopAdLib >}} function stops all playback from the AdLib card and restores the original system timer interrupt handler.

This function is a somewhat reduced variant of `SD_Shutdown()`[^SD_Shutdown] from Id Software's Sound Manager as used in _Catacomb 3-D_.

```c
void StopAdLib(void)
{
    if (!isAdLibStarted) return;

    StopAdLibPlayback();

    asm pushf

    disable();

    SetPIT0Value(0);
    setvect(8, savedInt8);

    asm popf

    isAdLibStarted = false;
}
```

The function begins with a safety check: If {{< lookup/cref isAdLibStarted >}} is false, the AdLib has either already been stopped or was never started in the first place, so the function should return without doing anything.

Otherwise, {{< lookup/cref StopAdLibPlayback >}} is called to silence any notes that may be actively playing through the AdLib's output.

The assembly `pushf` instruction pushes the current state of the CPU flags onto the stack. (Of particular importance is the Interrupt Flag.) Interrupts are disabled with the {{< lookup/cref disable >}} function, which prevents any timer ticks from interfering with the AdLib while we're trying to disarm it.

{{< lookup/cref name="SetPIT0Value" text="SetPIT0Value(0)" >}} writes the value 0 to the Programmable Interval Timer's channel 0, which has the effect of setting the value to _65,536_. This is the lowest frequency the timer can produce given the size of its counter register, and as explained [elsewhere on this page](#TimerInterruptService) the resulting tick rate is the PC's power-on default of 18.2 Hz.

{{< lookup/cref setvect >}} restores the interrupt vector 8 handler to {{< lookup/cref savedInt8 >}}, which reinstalls the timer interrupt handler that was present when {{< lookup/cref StartAdLib >}} last ran.

The assembly `popf` instruction pops the most recently pushed value off the stack and writes it into the CPU flags register. This restores, among other things, the previous value of the Interrupt Flag. If interrupts were enabled when this function was entered (and they really should have been) they will be re-enabled here.

Finally {{< lookup/cref isAdLibStarted >}} is set false to reflect the state the AdLib hardware is now in.

{{< boilerplate/function-cref StartAdLibPlayback >}}

The {{< lookup/cref StartAdLibPlayback >}} function sets the {{< lookup/cref enableAdLib >}} variable to true, permitting the AdLib service to play music.

This function is basically identical to `SD_MusicOn()`[^SD_MusicOn] from Id Software's Sound Manager as used in _Catacomb 3-D_.

```c
void StartAdLibPlayback(void)
{
    enableAdLib = true;
}
```

{{< boilerplate/function-cref StopAdLibPlayback >}}

The {{< lookup/cref StopAdLibPlayback >}} function clears all the AdLib parameter values that could produce note sounds.

This function is basically identical to `SD_MusicOff()`[^SD_MusicOff] from Id Software's Sound Manager as used in _Catacomb 3-D_. A junk variable has been removed which doesn't appear to pertain to any interesting unused functionality.

```c
void StopAdLibPlayback(void)
{
    word addr;

    switch (isAdLibServiceRunning) {
    case true:
        SetAdLibRegister(0xbd, 0);

        for (addr = 0; addr < 10; addr++) {
            SetAdLibRegister(addr + 0xb1, 0);
        }

        break;
    }

    enableAdLib = false;
}
```

This is an instance of {{< lookup/cref isAdLibServiceRunning >}} being treated like an enumeration instead of a boolean by using a `switch`. Setting that aside, the actual meat of this function is rather small.

First, {{< lookup/cref name="SetAdLibRegister" text="SetAdLibRegister(0xbd, 0)" >}} replaces the value in the AdLib's OPL register BDh with zero. This disables the [Key-On bits for the rhythm instruments](#rhythm-mode) (bass drum, snare drum, tom-tom, top cymbal, and hi-hat) in case they were in use. They never are, but that's beside the point. This also has the side effect of disabling [Rhythm Mode](#rhythm-mode) entirely, and setting both the [Vibrato](#vibrato) and [Tremolo Depth](#tremolo) values to 0. These changes are more collateral damage than intentional.

Next, a `for` loop calls {{< lookup/cref SetAdLibRegister >}} on registers B1h through BAh, setting all their values to zero. This loop starts on channel _2_ (which might be desired, as channel 1 is earmarked for sound effects) and ends with two nonexistent registers above channel 9.

OPL2 registers in the BXh range control Key-On, and _also_ control the coarse-grained Octave Value and the highest two bits of the Frequency Value. By setting all of these bits to zero, it's not immediately silencing the notes -- it's forcing each operator's [envelope](#envelope-rates-and-levels) to jump to its release stage while simultaneously setting the sine generator [frequencies](#frequencies-octaves-and-notes) to low -- but not necessarily zero -- values due to the bits still set in the AXh registers. The combined Frequency Value could still be as high as 255, which in this octave can produce a tone anywhere in the range of 0&ndash;12 Hz for as long as it takes the release stage of the envelope to complete. This is the reason why, on a lot of Id games, stopping the music or quitting the game would sometimes leave a low rumbling or almost flatulent tone playing for a brief time.

{{< aside class="armchair-engineer" >}}
**If you're gonna do it, do the hell out of it.**

To thoroughly silence the AdLib, in addition to the steps taken here, one would need to either zero out _all_ of the Frequency Value bits, or kick the Release Rate on all of the operators up to 15. Both of these would stop the output in very short order.
{{< /aside >}}

Finally, {{< lookup/cref enableAdLib >}} is set false to prevent the AdLib service from sending any additional music chunks to the hardware, thus preventing unwanted reactivation of any of the notes that were just turned off.

{{< boilerplate/function-cref SwitchMusic >}}

The {{< lookup/cref SwitchMusic >}} function stops any currently playing music and starts playing the music specified by `music`. The {{< lookup/cref Music >}} structure (note the capitalization) for each valid `music` value contains a blob of music data and the total length of that data.

This function is basically identical to `SD_StartMusic()`[^SD_StartMusic] from Id Software's Sound Manager as used in _Catacomb 3-D_.

```c
void SwitchMusic(Music *music)
{
    StopAdLibPlayback();

    asm pushf

    disable();

    if (isAdLibServiceRunning == true) {
        musicDataPtr = musicDataHead = &music->datahead;
        musicDataLength = musicDataLeft = music->length;

        musicNextDue = 0;
        musicTickCount = 0;

        StartAdLibPlayback();
    }

    asm popf
}
```

The function begins by silencing the active AdLib outputs, if any are generating sound, with {{< lookup/cref StopAdLibPlayback >}}. The assembly instruction `pushf` copies the current status of the CPU flags (particularly the Interrupt Flag) and pushes it onto the stack. The {{< lookup/cref disable >}} function then pauses interrupt handling, preventing the system timer from invoking the AdLib service and restarting any output while things are being reconfigured.

If {{< lookup/cref isAdLibServiceRunning >}} is true, an AdLib is present and music output is desired, so new music is prepared for playback. The {{< lookup/cref Music >}} structure contains two members: `length` is the size of the music in bytes, and `datahead` is the first byte of a memory block where music data has been loaded. The _memory address_ of the first byte of music data is loaded into {{< lookup/cref musicDataPtr >}} and {{< lookup/cref musicDataHead >}}. Following that, the length of the music data is copied to {{< lookup/cref musicDataLength >}} and {{< lookup/cref musicDataLeft >}}.

To ensure the scheduling logic in the AdLib service is in a pristine state, {{< lookup/cref musicNextDue >}} and {{< lookup/cref musicTickCount >}} are both set to zero. This ensures that something will be sent to the AdLib hardware the next time the timer interrupt occurs.

{{< lookup/cref StartAdLibPlayback >}} re-enables the flag that tells the AdLib service to play. This by itself does not restart the playback, as interrupts are still disabled and the AdLib service is not being called as a result.

Finally, the assembly instruction `popf` restores the CPU flags to the state they were in when the function was first entered. If the Interrupt Flag was enabled there, it is re-enabled here and the timer interrupts resume as before, playing the newly-configured music from the beginning.

{{< boilerplate/function-cref FadeOutAdLibPlayback >}}

The {{< lookup/cref FadeOutAdLibPlayback >}} function nominally fades any playing music to silence over a period of time, but as implemented it simply cuts the music off immediately.

This function is basically identical to `SD_FadeOutMusic()`[^SD_FadeOutMusic] from Id Software's Sound Manager as used in _Catacomb 3-D_. The original intent and name of this function was only apparent by consulting that source.

```c
void FadeOutAdLibPlayback(void)
{
    switch (isAdLibServiceRunning) {
    case true:
        StopAdLibPlayback();
        break;
    }
}
```

Structurally, this function mirrors many others by treating {{< lookup/cref isAdLibServiceRunning >}} as if it could be an enumeration, even though it never became one. This explains the presence of `switch`/`case`/`break` where it could have been written more succinctly.

This function simply calls {{< lookup/cref StopAdLibPlayback >}} if the AdLib is enabled. This silences the music abruptly, returning to the caller immediately.

According to the _Catacomb 3-D_ source code,[^SD_FadeOutMusic] this function was intended to fade the music out over a brief but perceptible period of time, blocking until silence was achieved. This is actually a very difficult thing to do. As implemented, the AdLib service relinquishes all control of the AdLib hardware to the music data as it was originally composed. It does not manipulate the data, nor does it keep track of what the data is asking the hardware to do.

The only real avenue of control the programmer has to "fade out" music is the Total Level register on each of the OPL2's operators. By ramping these values up to their maximum value, the outputs could be attenuated down to "pretty quiet" (but not silent) before cutting the notes off. This would require keeping track of the Total Level values that have been encountered in the music data and intercepting and scaling down the values as the fade progresses. Each Key-On event tends to come with its own Total Level value to reproduce MIDI velocity information, so any new notes that occur while the fade is progressing would also need to be scaled.

To further complicate this, the Total Level adjustment should only be applied to operators that are functioning as carriers, since modifying modulators would change the character of the output sound in potentially severe ways. The modulator/carrier role is determined by the position of each operator its channel, the channel's Connection mode, and the global setting of Rhythm Mode.

Taken together, this is a lot of effort and complexity for a small bit of polish that few really seemed to miss.

{{< boilerplate/function-cref IsAdLibAbsent >}}

The {{< lookup/cref IsAdLibAbsent >}} function returns _true_ if an AdLib or compatible card was _not_ detected in the system.

```c
bbool IsAdLibAbsent(void)
{
    return !isAdLibPresentPrivate;
}
```

Pretty self-explanatory. The opposite of {{< lookup/cref isAdLibPresentPrivate >}} is indeed the correct answer to the question, which is returned in a byte-sized boolean value.

{{< boilerplate/function-cref StartGameMusic >}}

The {{< lookup/cref StartGameMusic >}} function starts playing the music identified by the numeric `music_num` if the AdLib hardware is available. This function is only safe to use while gameplay is occurring. `music_num` should be one of the available {{< lookup/cref MUSIC >}} values.

```c
void StartGameMusic(word music_num)
{
    if (IsAdLibAbsent()) return;

    activeMusic = LoadMusicData(music_num, (Music *) (miscData + 5000));

    if (isMusicEnabled) {
        SwitchMusic(activeMusic);
    }
}
```

This function returns early if {{< lookup/cref IsAdLibAbsent >}} is true.

`music_num` is a numeric music identifier in the range of 0&ndash;18, which is passed to {{< lookup/cref LoadMusicData >}} to specify which piece of music should be read from disk. The music data will be loaded into a destination pointer, specified by the second argument to this function. Here it is the {{< lookup/cref miscData >}} memory block, 5,000 bytes from its start. This offset is needed because the first 5,000 bytes of {{< lookup/cref miscData >}} are used during gameplay to store any [demo data]({{< relref "demo-functions" >}}) that may be in use, leaving 30,000 bytes available for the {{< lookup/cref Music >}} structure used here.

Once the music data has been loaded into the destination memory, a {{< lookup/cref Music >}} pointer to the data is saved in {{< lookup/cref activeMusic >}}.

{{< lookup/cref isMusicEnabled >}} is the user-controllable preference indicating whether or not music is configured to play. If it is, {{< lookup/cref SwitchMusic >}} is called with {{< lookup/cref activeMusic >}} as its argument, setting the music up to play and enabling the AdLib service.

This function returns immediately, and the new music will begin playing from the beginning the next time the system timer ticks and runs the AdLib service.

{{< boilerplate/function-cref StartMenuMusic >}}

The {{< lookup/cref StartMenuMusic >}} function starts playing the music identified by the numeric `music_num` if the AdLib hardware is available. This function is only safe to use on the title screens, main menu, and its submenus. `music_num` should be one of the available {{< lookup/cref MUSIC >}} values.

```c
void StartMenuMusic(word music_num)
{
    if (IsAdLibAbsent()) return;

    activeMusic = LoadMusicData(music_num, (Music *) maskedTileData);

    if (isMusicEnabled) {
        SwitchMusic(activeMusic);
    }
}
```

The implementation is identical to {{< lookup/cref StartGameMusic >}}, so I won't repeat most of it. The important difference is the destination pointer on the {{< lookup/cref LoadMusicData >}} call: Here {{< lookup/cref maskedTileData >}} is used for storage of the music data, since the menu system has no need for any of the masked tile image data. This data area supports a {{< lookup/cref Music >}} structure up to 40,000 bytes in size.

{{< boilerplate/function-cref StopMusic >}}

The {{< lookup/cref StopMusic >}} function silences any active music and prevents the AdLib service from processing any new chunks of music.

```c
void StopMusic(void)
{
    if (IsAdLibAbsent()) return;

    StopAdLibPlayback();
}
```

This function returns early if {{< lookup/cref IsAdLibAbsent >}} is true. Otherwise, it calls {{< lookup/cref StopAdLibPlayback >}} to silence the music and disable output from the AdLib service.

[^almscpg]: [Ad Lib Music Synthesizer Card Programming Guide](http://www.vgmpf.com/Wiki/images/4/48/AdLib_-_Programming_Guide.pdf) (page 6)

[^rottclock]: `speed = 1192030L / TickBase`: https://github.com/videogamepreservation/rott/blob/master/audiolib/SOURCE/TASK_MAN.C#L230

[^dukeclock]: `speed = 1192030L / TickBase`: https://github.com/videogamepreservation/dukenukem3d/blob/master/audiolib/SOURCE/TASK_MAN.C#L230

[^quakeclock]: `ft = (double) (t+(65536-r)) / 1193200.0`: https://github.com/id-Software/Quake/blob/master/WinQuake/sys_dos.c#L711

[^SDL_SetTimer0]: `SDL_SetTimer0()`: https://github.com/CatacombGames/Catacomb3D/blob/master/ID_SD.C#L130

[^SDL_SetIntsPerSec]: `SDL_SetIntsPerSec()`: https://github.com/CatacombGames/Catacomb3D/blob/master/ID_SD.C#L149

[^SDL_TimingService]: `SDL_TimingService()`: https://github.com/CatacombGames/Catacomb3D/blob/master/ID_SD.C#L161

[^SDL_InitDelay]: `SDL_InitDelay()`: https://github.com/CatacombGames/Catacomb3D/blob/master/ID_SD.C#L175

[^SDL_Delay]: `SDL_Delay()`: https://github.com/CatacombGames/Catacomb3D/blob/master/ID_SD.C#L217

[^alOut]: `alOut()`: https://github.com/CatacombGames/Catacomb3D/blob/master/ID_SD.C#L362

[^SDL_ALService]: `SDL_ALService()`: https://github.com/CatacombGames/Catacomb3D/blob/master/ID_SD.C#L600

[^SDL_DetectAdLib]: `SDL_DetectAdLib()`: https://github.com/CatacombGames/Catacomb3D/blob/master/ID_SD.C#L686

[^SDL_t0Service]: `SDL_t0Service()`: https://github.com/CatacombGames/Catacomb3D/blob/master/ID_SD.C#L723

[^SDL_SetTimerSpeed]: `SDL_SetTimerSpeed()`: https://github.com/CatacombGames/Catacomb3D/blob/master/ID_SD.C#L855

[^SD_SetMusicMode]: `SD_SetMusicMode()`: https://github.com/CatacombGames/Catacomb3D/blob/master/ID_SD.C#L928

[^SD_Startup]: `SD_Startup()`: https://github.com/CatacombGames/Catacomb3D/blob/master/ID_SD.C#L969

[^SD_Shutdown]: `SD_Shutdown()`: https://github.com/CatacombGames/Catacomb3D/blob/master/ID_SD.C#L1069

[^SD_MusicOn]: `SD_MusicOn()`: https://github.com/CatacombGames/Catacomb3D/blob/master/ID_SD.C#L1203

[^SD_MusicOff]: `SD_MusicOff()`: https://github.com/CatacombGames/Catacomb3D/blob/master/ID_SD.C#L1214

[^SD_StartMusic]: `SD_StartMusic()`: https://github.com/CatacombGames/Catacomb3D/blob/master/ID_SD.C#L1237

[^SD_FadeOutMusic]: `SD_FadeOutMusic()`: https://github.com/CatacombGames/Catacomb3D/blob/master/ID_SD.C#L1262
