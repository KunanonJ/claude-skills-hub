# Spectrimage — Color Spectrum & Palette from an Image

**Spectrimage** (Amanda Hinton) is a client-side tool with two complementary views of an image's
color, computed in the same pass:

1. **The spectrum** — a 2D distribution chart (hue → x, lightness stacked, frequency → height).
2. **The palette** — a 5-color extraction via K-means clustering.

The author's own framing of why both exist:

> "My goal is for the spectrum to show the **'fact'** of the color in the image and for the
> palette to show the **'feeling'**."

i.e. the spectrum is the honest full distribution; the palette is the curated few-color read.

- **Author:** Amanda Hinton — [GitHub](https://github.com/amandahinton) ·
  [LinkedIn](https://www.linkedin.com/in/amandahinton/) ·
  [Instagram](http://instagram.com/amandadanghinton)
- **Built at:** Recurse Center "Impossible Stuff Day"
- **Spectrum write-up:** 2026-04-14 — <https://amandahinton.com/blog/generating-a-color-spectrum-for-an-image>
- **Palette write-up:** 2026-05-01 — <https://amandahinton.com/blog/creating-a-color-palette-from-an-image>
- **Contact:** hello@amandahinton.com

---

# Part 1 — The Spectrum (the "fact")

A visualization technique for showing the *color composition* of an image as a 2D spectrum: hue
along the horizontal axis, lightness stacked vertically, frequency as column height. Distinct
from palette extraction — instead of reducing an image to N swatches, it shows the full
distribution of hue × lightness × frequency in one chart.

## The Core Idea (Iteration 7 — the breakthrough)

The hard part of "spectrum from an image" is that color is 3D (hue, lightness, chroma) but
a spectrum strip is 1D. Early attempts all tried to **sort** pixels into a single line
(median-cut quantization, hue histograms, pixel-level sorting, lightness sub-sorts) and all
produced banding, striping, or discontinuities — the one-dimensional sorting problem.

The breakthrough was to go 2D: **each hue gets a vertical column, painted as a linear
gradient — tint at top, pure hue at center, shade at bottom.** This displays hue, frequency,
and tonal range simultaneously instead of forcing everything onto one axis.

Within a hue column, the tonal endpoints are derived by slicing that hue's pixels by lightness:

> "The darkest 20% are averaged to produce the shade color. The middle 20% produce the pure
> color. The lightest 20% produce the tint. Using 20% slices reduces outlier noise."

## Reading the Final Spectrum

| Visual property        | Encodes                                              |
| ---------------------- | ---------------------------------------------------- |
| Horizontal position    | Hue (walks the wheel)                                |
| Column height          | Frequency, relative to the most-populous hue         |
| Stacked bands (top→bot)| Lightness distribution: tints up, shades down        |
| Asymmetry about center | Tonal character — dark-dominant vs light-dominant    |

The pure-hue band straddles the horizontal axis; tints stack upward, shades downward, so a
column that bulges upward is a light-leaning hue and one that bulges down is dark-leaning.

## OKLCH Refactor (Iteration 11)

The tool started in HSL and was rebuilt in **OKLCH**, which fixed saturation-perception and
perceptual-uniformity problems:

> "In OKLCH, L is lightness that matches the eye. C is chroma, independent of lightness, so a
> near-white off-white reports near-zero. And H is hue that walks the wheel evenly."

This is the standard argument for OKLCH over HSL: HSL's L is a math average (so equal-L colors
look unequally bright), its S doesn't track perceived saturation, and its hue spacing is
non-uniform. OKLCH's chroma being lightness-independent is what makes the chromatic/achromatic
split (below) clean — an off-white reports near-zero chroma instead of HSL's misleadingly high
saturation.

## Binning Parameters (final implementation)

| Parameter              | Value                                              |
| ---------------------- | -------------------------------------------------- |
| Color space            | OKLCH                                               |
| Chromatic threshold    | chroma **C ≥ 0.02** (below → treated as achromatic)|
| Hue bins               | **180 bins, 2° each**, wrap point at 15°            |
| Achromatic bins        | **60 lightness bins** (greys handled separately)   |
| Lightness bands/column | **11 bands**, ~0.091 L units each; band 5 = pure   |

Black-and-white / near-grey images get special handling: pixels under the chroma threshold are
routed to a separate achromatic (lightness-only) track instead of being forced into a hue column.

## Performance / Architecture

- **Fully client-side** — runs in the browser, no server beyond the Canvas API.
- Images **downsampled to 300px on the longest dimension** before binning.
- **Under 1 second** to process a 4000×3000 photo.

---

# Part 2 — The Palette (the "feeling")

A 5-color palette extractor for the same image, via **K-means++ clustering in OKLab**. The
write-up documents four iterations — a good case study in the failure modes of naïve extraction.

### Iteration 1 — RGB median-cut + ROYGBIV (abandoned)

Median-cut quantization in RGB with hand-drawn ROYGBIV region partitioning. It collapsed under its
own special-casing — *"thirteen named constants"* and *"six rules for what counts as gray"* — so
the author scrapped it: *"move everything to OKLCH, start with a clean K-means algorithm."* The
lesson: ad-hoc rules in RGB don't generalize; pick a perceptual space and a principled algorithm.

### Iteration 2 — K-means++ in OKLCH

- **Space:** OKLCH, chosen because *"OKLCH C is a distance from the achromatic axis"* rather than
  HSL's saturation ratio that *"blows up near black."*
- **K = 10**, overshooting the 5 final colors. **K-means++** seeding, made **deterministic** via a
  hash of the input pixels (same image → same palette).
- **Merge:** closest-pair merge of clusters within **0.07** of each other until ≤5 remain; a
  **rescue pass** re-adds missed regions at **≥0.1% pixel density**.
- **Swatch pick:** highest-chroma pixel within the cluster's typical radius.

### Iteration 3 — hue-weighted distance, K = 14

- **K raised to 14** (best over 12 benchmark images).
- **Anisotropic distance:** the **chromatic plane (hue + chroma) weighted 2× vs. the lightness
  axis** — *"Two reds at different lightnesses feel like reds to a human, but two distinct hues at
  similar lightness feel like different colors."* (A nice perceptual-clustering insight: don't
  treat OKLab's three axes as equally important for *grouping*.)

### Iteration 4 — phantom guard, mass allocation, centroid-aware selection

- **Phantom guard:** drop any cluster with pixel weight < **2.5%** *and* centroid chroma < **0.05**
  (kills faint ghost colors from anti-aliasing/JPEG).
- **Mass-based slot allocation:** achromatic pixels counted proportionally; greys bucketed into
  dark/mid/light bands; same-band pairs collapsed (so a photo doesn't spend 3 of 5 slots on greys).
- **Centroid-aware representative:**
  - centroid chroma **≥ 0.03** → pick the **highest-chroma** pixel (vivid, representative).
  - centroid chroma **< 0.03** → pick the pixel **closest to the centroid** (prevents a near-grey
    cluster from being represented by an off-color outlier — *"sepia or mauve or sage green"*).

### Final pipeline

Up to **90,000 sampled pixels** → **K-means++ at K = 14 in OKLab**, deterministic seed → merge /
guard / allocate down to 5 → **sorted by hue, achromatics last by lightness**, using the same
**chroma threshold 0.02** as the spectrum. Runs in the **same client-side pass** as the spectrum.

### Palette-extraction takeaways

- **Overshoot then merge.** Cluster to more centroids than you want (K=14→5) and merge by perceptual
  distance — more robust than asking K-means for exactly N.
- **Weight the axes for grouping.** Equal-weight OKLab distance over-splits on lightness; doubling
  the chromatic plane matches how people group colors.
- **Representative pixel ≠ centroid.** For chromatic clusters show the *vivid* member; for near-grey
  clusters show the *central* one. Picking the centroid color itself tends to look muddy.
- **Guard against phantoms.** Low-mass + low-chroma clusters are almost always compression/edge
  artifacts — drop them before they eat a palette slot.

## Why It Matters (technique takeaways)

- **Don't sort 3D color onto 1D.** Give one perceptual axis to position (hue → x) and let the
  others map to height/stacking. Generalizable to any "summarize a color field" problem.
- **Percentile slices (20%) beat min/max** for deriving tint/pure/shade — they reject outlier
  pixels (specular highlights, JPEG noise) that a true-min or true-max would latch onto.
- **A chroma threshold is the right achromatic gate** — in OKLCH, near-greys honestly report
  near-zero chroma, so `C ≥ 0.02` cleanly separates "has a hue" from "is grey." This is exactly
  the kind of thing HSL gets wrong (a dark saturated-looking blue and a near-grey can both show
  high S).
- **Frequency-as-height + asymmetry-as-tone** packs three dimensions into a static chart that's
  readable at a glance.
- **Fact vs. feeling.** Two views of the same data answer different questions — full distribution
  (spectrum) vs. curated few-color read (palette). Worth offering both when summarizing image color.

## Related

- [Image Color Extraction Tools](image-color-extraction-tools.md) — peer palette extractors
  (img-colors.com's 7 clustering algorithms, okpalette.color.pizza's OKLCH extraction, colorgram-js,
  Art Palette). Spectrimage's palette is another K-means-in-OKLab extractor; its spectrum view is
  the distinct part.
- OKLCH rationale: [HSLuv better than HSL](hsluv-better-than-hsl.md), [Culori](culori-color-spaces-api.md).

## Links

- **Spectrum article:** <https://amandahinton.com/blog/generating-a-color-spectrum-for-an-image>
- **Palette article:** <https://amandahinton.com/blog/creating-a-color-palette-from-an-image>
- **Author site:** <https://amandahinton.com>
- **Recurse Center:** <https://www.recurse.com>
