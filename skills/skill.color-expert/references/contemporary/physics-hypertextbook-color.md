# Color — The Physics Hypertextbook (Glenn Elert)

A clean, citable, textbook-grade overview of the **physics of color**: light → eye → models →
digital encoding. Good canonical reference for the fundamentals, and unusually strong on the
*encoding/standards* side (bit depths, TV color systems) that most color resources skip.

- **Author:** Glenn Elert — *The Physics Hypertextbook*
- **Section:** Waves & Optics → Physical Optics (between "Thin-film interference" and "Reflection")
- **URL:** <https://physics.info/color/>

## Framing: color is perception, not a property

> "Objects don't *have* a color, they give off light that *appears to be* a color."

Spectral power distributions are physical; **color exists only in the observer**. (Same stance as
the [philosophy-of-color](colour-subjectivisms-philosophy.md) and
[Briggs](briggs-what-is-a-colour.md) references.)

Elert frames the visible band in **frequency** (≈400–790 THz) rather than only wavelength — a
useful reminder that frequency is the invariant (it doesn't change across media; wavelength does).

## Cone peaks

| Cone | Common label | Peak sensitivity |
| ---- | ------------ | ---------------- |
| **L** | long / "red"   | ~580 nm |
| **M** | medium / "green" | ~540 nm |
| **S** | short / "blue"  | ~440 nm |

Combined cone response peaks ~**560 nm** (yellow-green) — why luminance/luminous-efficiency curves
center there, and why warning/safety colors lean yellow-green.

## Additive vs. subtractive

**Additive (light) — primaries R, G, B**
- R+G = Yellow · G+B = Cyan · B+R = Magenta · R+G+B = White · none = Black
- Secondaries sit at hue **60° (yellow), 180° (cyan), 300° (magenta)** — each the complement of a
  primary.

**Subtractive (pigment/print) — primaries C, M, Y**
- C+M = Blue · M+Y = Red · Y+C = Green · C+M+Y = (≈)Black · none = White (paper)

> The traditional **RYB painter's wheel is historically inaccurate** for human vision; **CMY has
> the superior chromatic range.** (Aligns with the skill's RYB-is-bad-theory thread — see
> [RYB vs CMY](../historical/ryb-vs-cmy-color-wheels.md), [Moses Harris](../historical/moses-harris-1769-color-wheel.md).)

## Spectral wavelength bands (approximate, continuous not discrete)

| Color  | nm       |
| ------ | -------- |
| Red    | 620–750  |
| Orange | 590–620  |
| Yellow | 560–590  |
| Green  | 495–570  |
| Blue   | 450–495  |
| Violet | 400–450  |

Boundaries vary by source; the spectrum is continuous. (Note green/yellow overlap in the listed
ranges — different conventions disagree at the edges.)

## Six ways color is produced

Emission (incandescence, fluorescence, phosphorescence, lasers) · Reflection (paints, inks, dyes,
biological pigments) · Transmission (stained glass, filters) · Scattering (sky blue, colloids) ·
Dispersion (rainbows, chromatic aberration) · Interference (thin films, iridescence, nacre,
peacock). This is a condensed cousin of Nassau's framework — see the fuller
[Causes of Color / 15 causes](webexhibits-causes-of-color.md).

## Digital & broadcast encoding (the genuinely distinctive part)

**RGB bit depth**

| Bits | Colors        | Marketing name |
| ---- | ------------- | -------------- |
| 8    | 256           | —              |
| 16   | 65,536        | Thousands      |
| 24   | 16,777,216    | Millions       |
| 32   | 4,294,967,296 | Billions       |

**Broadcast / video luma-chroma systems** (all separate luminance from chrominance, enabling
chroma subsampling — see [JPEG/chroma subsampling](computerphile-jpeg-color.md)):

| System | Used by |
| ------ | ------- |
| **YIQ** (NTSC) | US, Canada, Japan |
| **YUV** (PAL) | Western Europe, Australia |
| **YDbDr** (SECAM) | France, Eastern Bloc |
| **YPbPr** | analog component video |
| **YCbCr** | digital video |

**Print:** CMY, CMYK, CMYK + spot colors, **Hexachrome** (CMYK + orange + green).

## Etymology & history (nice color-naming color)

- **Old English** color words: *reád* (red), *geolu* (yellow), *grēne* (green), *hǽwen* (blue).
- **1066 Norman Conquest** brought French loanwords — "blue" displaced *hǽwen*, "violet" appeared.
- **Newton's seven colors** (incl. indigo) is critiqued as numerology/mysticism-driven; **John
  Leslie (1838)** already attacked the seven-color scheme. Indigo called practically
  insignificant — see [What Happened to Indigo?](../historical/what-happened-to-indigo.md).
- Cited theorists: Newton (~1666), **Thomas Young** (1802 Bakerian Lecture, trichromacy), **Goethe**
  (*Theory of Colors*, 1810). Standards: **CIE**, **ISO 21348:2007**. Etymologies from the OED.

## Why It Matters

- **Best single-page primer** when someone needs the physics fundamentals (cone peaks, additive vs
  subtractive, wavelength bands) with textbook authority and a citation.
- **The encoding tables are the unique value** — bit depths and the YIQ/YUV/YDbDr/YPbPr/YCbCr
  family aren't covered elsewhere in these references; they're the bridge from "physics of light"
  to "how color is actually stored and broadcast."

## Links

- **Page:** <https://physics.info/color/>
- **Site:** <https://physics.info> · <https://hypertextbook.com> · author <https://glennelert.us>
