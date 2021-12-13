#!/usr/bin/env python3.7

import math
import struct
import wave

# Don't read this; this is single-use crap.

CLOCK_FREQ = 44100
TWO_PI = 2 * math.pi

G3 = 195.9977
A3 = 220.0000
B3 = 246.9417
C4 = 261.6256
D4 = 293.6648
E4 = 329.6276
F4 = 349.2282
G4 = 391.9954
A4 = 440.0
B4 = 493.8833
C5 = 523.2511
D5 = 587.3295
Ds5 = 622.2540
E5 = 659.2551
F5 = 698.4565
G5 = 783.9909
Gs5 = 830.6094
A5 = 880.0
C6 = 1046.502


class Oscillator:
    def __init__(self):
        self.set_clock_freq(CLOCK_FREQ)
        self.output_freq = C4
        self.phase = 0

    def set_clock_freq(self, freq):
        self.clock_freq = freq
        self.hz_to_rad = freq / TWO_PI

    def tick(self, modulation=0):
        self.phase += self.output_freq / self.hz_to_rad
        return math.sin(self.phase + modulation)


def sine(filename):
    osc = Oscillator()

    with wave.open(filename, 'wb') as out_wav:
        out_wav.setframerate(CLOCK_FREQ)
        out_wav.setnchannels(1)
        out_wav.setsampwidth(2)

        for _ in range(CLOCK_FREQ):
            sample = int(osc.tick() * 16384)
            out_wav.writeframesraw(struct.pack('<h', sample))


def sine_song(filename):
    tempo_period = CLOCK_FREQ / 6.333
    notes = [
        (C5, 0), (E5, 2), (G5, 4), (F5, 5), (E5, 6), (D5, 7), (C5, 8), (G5, 10), (C6, 11)]

    osc = Oscillator()

    with wave.open(filename, 'wb') as out_wav:
        out_wav.setframerate(CLOCK_FREQ)
        out_wav.setnchannels(1)
        out_wav.setsampwidth(2)

        for tick in range(int(12 * tempo_period)):
            for freq, start in notes:
                if int(tick / tempo_period) == start:
                    osc.output_freq = freq
                    break
            sample = int(osc.tick() * 16384)
            out_wav.writeframesraw(struct.pack('<h', sample))


def slide_song(filename):
    tempo_period = CLOCK_FREQ / 12.667
    notes = [
        (A4, 0), (A4, 11), (A5, 12), (A5, 17), (E5, 18), (E5, 23), (D5, 24),
        (D5, 25), (E5, 26), (E5, 27), (D5, 28), (D5, 29), (C5, 30), (C5, 39),
        (B4, 40), (B4, 41), (C5, 42), (C5, 43), (B4, 44), (B4, 45), (G4, 46),
        (G4, 47), (A4, 48), (A4, 64)]

    osc = Oscillator()

    with wave.open(filename, 'wb') as out_wav:
        out_wav.setframerate(CLOCK_FREQ)
        out_wav.setnchannels(1)
        out_wav.setsampwidth(2)

        for tick in range(int(64 * tempo_period)):
            prev_freq = None
            next_freq = None
            prev_dist = 9999
            next_dist = 9999
            tickpos = tick / tempo_period
            for freq, start in notes:
                if start <= tickpos and tickpos - start < prev_dist:
                    prev_dist = tickpos - start
                    prev_freq = freq
                if start >= tickpos and start - tickpos < next_dist:
                    next_dist = start - tickpos
                    next_freq = freq

            if next_dist < 1:
                osc.output_freq = (prev_freq * next_dist) + (next_freq * (1 - next_dist))
            else:
                osc.output_freq = prev_freq

            sample = int(osc.tick() * 16384)
            out_wav.writeframesraw(struct.pack('<h', sample))


def pop_song(filename):
    amp1 = 32767
    amp2 = 16384
    amp3 = 1024
    tempo_period = CLOCK_FREQ / 30
    pattern = [
        (amp1, 0), (amp3, 4), (amp3, 8), (amp2, 12), (amp3, 16), (amp2, 20), (amp3, 24),
        (amp2, 28), (amp3, 32), (amp3, 36), (amp2, 40), (amp3, 44), (amp1, 48)]

    osc = Oscillator()
    osc.output_freq = C5

    with wave.open(filename, 'wb') as out_wav:
        out_wav.setframerate(CLOCK_FREQ)
        out_wav.setnchannels(1)
        out_wav.setsampwidth(2)

        for tick in range(int(64 * tempo_period)):
            sample = 0
            for amp, start in pattern:
                if int(tick / tempo_period) == start:
                    sample = int(osc.tick() * amp)
                    break
            if sample == 0:
                osc.phase = 0
            out_wav.writeframesraw(struct.pack('<h', sample))


def zarathustra(filename):
    tempo_period = CLOCK_FREQ / 8
    notes = [(C4, 0), (G4, 16), (C5, 32), (E5, 62), (Ds5, 64)]
    amps = [(256, 0), (4096, 62), (32767, 62.05), (8192, 74), (28670, 85), (0, 104)]

    osc = Oscillator()

    with wave.open(filename, 'wb') as out_wav:
        out_wav.setframerate(CLOCK_FREQ)
        out_wav.setnchannels(1)
        out_wav.setsampwidth(2)

        for tick in range(int(105 * tempo_period)):
            tickpos = tick / tempo_period

            for freq, start in notes:
                if int(tickpos) == start:
                    osc.output_freq = freq
                    break

            prev_amp = prev_pos = 0
            next_amp = next_pos = 0
            prev_dist = 9999
            next_dist = 9999
            for amp, start in amps:
                if start <= tickpos and tickpos - start < prev_dist:
                    prev_dist = tickpos - start
                    prev_amp = amp
                    prev_pos = start
                if start > tickpos and start - tickpos < next_dist:
                    next_dist = start - tickpos
                    next_amp = amp
                    next_pos = start

            ratio = (tickpos - prev_pos) / (next_pos - prev_pos)
            multiplier = (prev_amp * (1 - ratio)) + (next_amp * ratio)
            out_wav.writeframesraw(struct.pack('<h', int(osc.tick() * multiplier)))


def vibrato(filename):
    modulator = Oscillator()
    modulator.output_freq = (49716 / 1024) / 8

    carrier = Oscillator()

    vib_depth = 0.14 * (A5 - Gs5)  # 14 cents-ish

    with wave.open(filename, 'wb') as out_wav:
        out_wav.setframerate(CLOCK_FREQ)
        out_wav.setnchannels(1)
        out_wav.setsampwidth(2)

        for _ in range(CLOCK_FREQ):
            msamp = modulator.tick()
            carrier.output_freq = A5 + (msamp * vib_depth)
            csamp = carrier.tick()

            sample = int(csamp * 16384)
            out_wav.writeframesraw(struct.pack('<h', sample))


def tremolo(filename):
    modulator = Oscillator()
    modulator.output_freq = (49716 / 64) / 210

    carrier = Oscillator()
    carrier.output_freq = A4

    amp_delta = 3467
    amp_min = 12917

    with wave.open(filename, 'wb') as out_wav:
        out_wav.setframerate(CLOCK_FREQ)
        out_wav.setnchannels(1)
        out_wav.setsampwidth(2)

        for _ in range(CLOCK_FREQ):
            msamp = modulator.tick()
            csamp = carrier.tick()

            sample = int(csamp * ((msamp * amp_delta) + amp_min))
            out_wav.writeframesraw(struct.pack('<h', sample))


def modulate_up(filename):
    modulator = Oscillator()

    carrier = Oscillator()
    carrier.output_freq = C4

    multipliers = [0.5, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15]

    with wave.open(filename, 'wb') as out_wav:
        out_wav.setframerate(CLOCK_FREQ)
        out_wav.setnchannels(1)
        out_wav.setsampwidth(2)

        for mult in multipliers:
            modulator.output_freq = carrier.output_freq * mult
            modulator.phase = 0
            carrier.phase = 0
            for tick in range(CLOCK_FREQ):
                amplitude = 1 - (tick / CLOCK_FREQ)
                msamp = modulator.tick() * amplitude
                csamp = carrier.tick(modulation=msamp * 8 * math.pi)
                out_wav.writeframesraw(struct.pack('<h', int(csamp * 16384)))


def modulate_down(filename):
    modulator = Oscillator()

    carrier = Oscillator()
    carrier.output_freq = C4

    multipliers = [0.5, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15]

    with wave.open(filename, 'wb') as out_wav:
        out_wav.setframerate(CLOCK_FREQ)
        out_wav.setnchannels(1)
        out_wav.setsampwidth(2)

        for mult in multipliers:
            modulator.output_freq = carrier.output_freq / mult
            modulator.phase = 0
            carrier.phase = 0
            for tick in range(CLOCK_FREQ):
                amplitude = 1 - (tick / CLOCK_FREQ)
                msamp = modulator.tick() * amplitude
                csamp = carrier.tick(modulation=msamp * 8 * math.pi)
                out_wav.writeframesraw(struct.pack('<h', int(csamp * 16384)))


def feedback(filename):
    osc = Oscillator()
    osc.output_freq = D4

    fb_shifts = [0, 256, 128, 64, 32, 16, 8, 4]

    with wave.open(filename, 'wb') as out_wav:
        out_wav.setframerate(CLOCK_FREQ)
        out_wav.setnchannels(1)
        out_wav.setsampwidth(2)

        for fb in fb_shifts:
            osc.phase = 0
            out = 0
            prev_out = 0

            for tick in range(CLOCK_FREQ):
                amplitude = 1 - (tick / CLOCK_FREQ)

                fval = 0
                if fb > 0:
                    fval = int((out * 8 * math.pi) + (prev_out * 8 * math.pi)) / fb

                out = osc.tick(modulation=fval) * amplitude
                out_wav.writeframesraw(struct.pack('<h', int(out * 16384)))

                prev_out = out


if __name__ == '__main__':
    sine('sine-wave.wav')
    sine_song('sine-song.wav')
    slide_song('sine-portamento-song.wav')
    pop_song('amplitude-song.wav')
    zarathustra('zarathustra.wav')
    vibrato('vibrato.wav')
    tremolo('tremolo.wav')
    modulate_up('mod-up.wav')
    modulate_down('mod-down.wav')
    feedback('feedback.wav')
