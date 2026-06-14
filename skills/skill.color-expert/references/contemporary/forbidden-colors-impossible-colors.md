# Forbidden Colors — Reddish-Green & Yellowish-Blue

"Forbidden colors" (a.k.a. **chimerical** or **impossible colors**) are hues the
**opponent-process** model says you should never be able to see: a color that is *simultaneously*
reddish **and** greenish, or yellowish **and** bluish, in the same spot at the same time. Under
the right lab conditions, some observers report seeing them anyway.

> ⚠️ Don't confuse this with "impossible colors" in the *gamut* sense (a chroma/hue that a display
> or color space can't reproduce, e.g. out-of-gamut OKLCH). Those are reproduction limits; these
> are perceptual/neural limits. See [HSLuv](../techniques/hsluv-better-than-hsl.md) for the gamut
> usage.

- **Primary source:** Natalie Wolchover, *"Red-Green & Blue-Yellow: The Stunning Colors You Can't
  See,"* LiveScience, 2012-01-17 —
  <https://www.livescience.com/17948-red-green-blue-yellow-stunning-colors.html>

## Why They're "Forbidden" — Opponent Process

Color vision past the cones is encoded on two **opponent axes** (Hering; the basis of CIELAB's
`a*/b*` and OKLAB). See [opponent-process model](opponent-process-color-blindness.md).

- **Red ↔ Green** axis: red excites the opponent neuron, green inhibits it.
- **Yellow ↔ Blue** axis: yellow excites, blue inhibits.

Because the two ends of an axis drive the *same* neuron in opposite directions, "reddish-green"
or "yellowish-blue" would require that neuron to be excited and inhibited at once — so the model
predicts those percepts are impossible. (You *can* see reddish-yellow = orange, or bluish-green =
teal, because those mix *across* the two axes, not within one.)

## The 1983 Crane & Piantanida Experiment

**Hewitt Crane & Thomas Piantanida**, *"On Seeing Reddish Green and Yellowish Blue,"* **Science**,
1983.

- **Method:** showed red/green (and yellow/blue) adjacent stripes, then used an **eye tracker to
  stabilize the image on the retina** so each retinal cell was held on one fixed color (defeating
  the micro-eye-movements that normally refresh the stimulus).
- **Result:** the stripe borders dissolved — "the colors seem to flood into each other" — and some
  observers reported a genuinely novel color they couldn't name, neither a mix nor a third hue:
  a reddish-green or yellowish-blue.
- **Paper PDF (mirror):** `philosci40.unibe.ch/lehre/winter99/farbenlehre/crane.PDF`

## The Debate Since

- **Hsieh & Tse (2006)** — argued the effect is **illusory color mixing / filling-in**, producing
  an *intermediate* color (e.g. a muddy brown or a color along the line between the two), **not** a
  true forbidden color. I.e. the percept is explicable without breaking opponency.
- **Billock & Tsou (2010, and earlier work)** — found that under **equiluminant** conditions (the
  two colors matched in brightness, removing the luminance edge), some observers *do* report
  stable forbidden colors that resist being described as a mixture — supporting the original
  claim. Suggests the result is real but condition-dependent and varies between observers.

**Takeaway:** the existence of "forbidden colors" is genuinely contested. The safe statement is:
under retinal stabilization (and especially equiluminance), the opponent-process prediction *can*
break down for some people, but whether what they see is a true novel hue or an intermediate
filled-in color is unresolved.

## Why It Matters

- **Opponent process is a model, not an absolute wall.** It's the right default for explaining hue
  relationships, color blindness, and the `a*/b*` axes — but it's a neural encoding, not a hard
  perceptual law, and stabilized/equiluminant stimuli can push past it.
- **Three different "impossible" colors — keep them straight:**
  1. **Forbidden/chimerical** — violate opponency (this file).
  2. **Out-of-gamut** — real to the eye, unreproducible by a device/space (clamp with Culori
     `clampChroma` in OKLCH).
  3. **Imaginary/non-physical** — e.g. CIE XYZ coordinates outside the spectral locus, or hyper-
     saturated afterimage colors, that no light spectrum can produce.
- Related curiosity: [OLO](olo-newly-discovered-color.md) — a hyper-saturated green from stimulating
  only M-cones with a laser; another "color you can't get from natural light," but via a *different*
  mechanism (cone isolation, not opponency override).

## Links

- **LiveScience article:** <https://www.livescience.com/17948-red-green-blue-yellow-stunning-colors.html>
- **Crane & Piantanida 1983 PDF (mirror):** <http://philosci40.unibe.ch/lehre/winter99/farbenlehre/crane.PDF>
