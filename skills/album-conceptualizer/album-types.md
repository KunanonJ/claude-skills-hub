# Album Types Reference

Detailed planning approaches for each album category.

---

## 1. True Crime / Documentary

**Definition**: Real events, real people, factual storytelling

**Planning Questions**:
- What's the central event/story?
- Who are the key players?
- What's the timeline?
- What sources exist? (Court docs, news, press releases)
- What's the angle? (Not just "what happened" but "why does it matter")
- How many tracks needed to tell story completely?

**Structure Approaches**:
- **Chronological**: Track 1 = beginning, final track = resolution
- **Thematic**: Group by themes, not timeline
- **Character-focused**: Each track follows a different person
- **Event-focused**: Each track = a critical moment

**Example**: Album about the Great Molasses Flood (Dark Tide)
- Tracks 1-4: The Monster (the neighborhood, the tank, warnings ignored)
- Tracks 5-8: The Wave (the disaster, chaos, death, heroism)
- Tracks 9-11: The Reckoning (the lies, the trial, the verdict)

---

## 2. Storytelling / Narrative

**Definition**: Fictional or dramatized story told across tracks

**Planning Questions**:
- Who is the protagonist?
- What do they want?
- What's preventing them from getting it?
- How does it resolve?
- What's the emotional arc?

**Structure Approaches**:
- **Three-act**: Setup (tracks 1-3), Conflict (4-8), Resolution (9-12)
- **Character journey**: Each track = stage of character development
- **Multiple perspectives**: Different characters tell same story
- **Non-linear**: Fragments that connect by end

**Example**: Concept album about addiction recovery
- Tracks 1-3: Descent (hitting bottom)
- Tracks 4-6: Recognition (realizing need for change)
- Tracks 7-9: Struggle (recovery process)
- Tracks 10-12: Emergence (new life, looking back)

---

## 3. Thematic Concept

**Definition**: United by theme, mood, or idea (not plot)

**Planning Questions**:
- What's the central theme?
- What are the sub-themes or facets?
- What emotions should each track evoke?
- How do tracks connect without being narrative?
- What's the sonic throughline?

**Structure Approaches**:
- **Exploration**: Each track examines theme from different angle
- **Emotional arc**: Journey through related feelings
- **Contrasts**: Light/dark, hope/despair, past/future
- **Mosaic**: Pieces that form larger picture

**Example**: Album about "Surrender"
- Tracks explore different meanings: giving up, letting go, acceptance, trust, defeat, peace
- Not a story, but emotional progression from resistance to release

---

## 4. Character Study

**Definition**: Deep dive into a person (real or fictional)

**Planning Questions**:
- Who is this person?
- What aspects of them will you explore?
- What time period(s)?
- What's the through-line?
- What makes them compelling?

**Structure Approaches**:
- **Life stages**: Childhood → youth → adulthood → legacy
- **Facets**: Different roles (father, CEO, addict, visionary)
- **Defining moments**: Tracks = pivotal events in their life
- **Internal/external**: Alternate between inner thoughts and outer actions

**Example**: Album about Edward Snowden
- Tracks explore: childhood, NSA career, discovery of surveillance, decision to leak, Hong Kong escape, exile, legacy

---

## 5. Collection

**Definition**: Standalone songs with loose connection

**Planning Questions**:
- What's the unifying element? (Even if loose)
- Genre consistency or variety?
- Is there an intentional flow, or is variety the point?
- Any narrative throughline, or purely thematic?

**Structure Approaches**:
- **Best foot forward**: Strongest track first
- **Energy arc**: High → low → high, or gradual build
- **Palette cleanser**: Vary styles to prevent fatigue
- **Bookends**: Strong opener and closer, looser middle

**Example**: Collection of Linux distro songs
- Unified by subject (Linux), each track standalone
- Arranged chronologically by distro release date
- Creates accidental narrative of Linux history

---

## 6. OST (Original Soundtrack)

**Definition**: Music evoking a fictional media property — a video game, film, TV series, anime, or other narrative world

**Planning Questions**:
- What is the media type? (Video game, film, TV series, anime, theater, podcast)
- What is the world/setting? (Fantasy kingdom, sci-fi station, noir city, school campus)
- What scenes or moments map to tracks? (Levels, chase scenes, episodes, boss fights, quiet moments, title/credits)
- Are there recurring musical themes/leitmotifs across tracks?
- What mix of vocal vs. instrumental tracks?
- What genre palette spans the album? (Orchestral, electronic, chiptune, ambient, jazz, metal)
- What emotional journey does the audience experience? (Discovery, escalation, climax, resolution)

**Structure Approaches**:
- **Scene-Based**: Each track = a key scene or moment, energy follows narrative tension
- **Act-Based**: Three-act narrative structure (setup → conflict → resolution)
- **World-Based**: Each track = a distinct location or environment with its own genre/mood
- **Episode-Based**: Each track = a chapter, episode, or level with escalating stakes
- **Gameplay-Loop** (games): Tracks follow player experience cycle (title → explore → combat → boss → victory → rest)

**Duration Strategy** (variable — OST tracks vary widely by scene function):

| Scene Function | Target Duration | Suno Section Strategy |
|---------------|-----------------|----------------------|
| Title/Opening | ~1:30 | `[Intro]` → `[Main Theme]` → `[End]` |
| Quiet Moment / Menu | ~2:00–3:00 | `[Intro]` → `[Theme]` → `[Variation]` → `[Outro]` |
| Exploration / Dialogue | ~3:00–4:00 | Standard structure, 2–3 sections |
| Action / Boss Fight | ~4:00–5:00+ | Multiple builds/drops, `"extended"` in style prompt |
| Cutscene / Flashback | ~1:30–2:30 | `[Intro]` → `[Theme]` → `[Outro]` → `[End]` |
| Credits / Ending | ~3:00–4:00 | Reprise sections with theme callbacks |

*Fewer section tags = shorter tracks. `[End]` is the strongest stop signal. Expect 2–3 generations to hit target length — trim in post.*

**Example 1**: OST for a retro sci-fi platformer (video game)
- Track 01: Title Screen (~1:30, chiptune, nostalgic, sets the tone)
- Tracks 02-04: Early Levels (~3:00, upbeat electronic, escalating tempo)
- Track 05: First Boss (~4:30, heavy synth-metal, intense)
- Track 06: Hub World (~2:30, ambient, peaceful respite)
- Tracks 07-09: Late Levels (~3:30, orchestral-electronic hybrid, darker)
- Track 10: Final Boss (~5:00, full orchestral + electronic, peak intensity)
- Track 11: Credits/Ending (~3:30, piano reprise of title theme, resolving leitmotifs)

**Example 2**: OST for a noir detective film
- Track 01: Opening Titles (~1:30, smoky jazz, saxophone, sets mood)
- Track 02: The Case (~3:30, tension building, brushed drums, muted trumpet)
- Track 03: Late Night Stakeout (~4:00, ambient noir, rain sounds, piano)
- Track 04: The Chase (~3:00, uptempo jazz, driving drums, brass stabs)
- Track 05: Betrayal (~2:30, slow strings, dissonant piano, emotional gut-punch)
- Track 06: Showdown (~4:30, full orchestra + jazz ensemble, peak intensity)
- Track 07: Closing Credits (~3:30, reprise of opening theme, bittersweet resolution)

---

## Common Mistakes

### 1. Too Much Setup
**Problem**: Tracks 1-3 all "introduction," real story doesn't start until track 4
**Fix**: Start in the middle, fill in backstory as needed

### 2. Flat Arc
**Problem**: Every track same energy, no dynamics
**Fix**: Intentional peaks and valleys

### 3. No Payoff
**Problem**: Build build build... then ends abruptly
**Fix**: Closing track must deliver emotional resolution

### 4. Burying the Hit
**Problem**: Best track is hidden at track 9
**Fix**: Front-load quality, especially tracks 1 and 3

### 5. Concept Overwhelms Music
**Problem**: Clever concept, but songs aren't compelling
**Fix**: Concept serves music, not vice versa

### 6. Too Much Explanation
**Problem**: Liner notes required to understand album
**Fix**: Music should stand on its own

---

## Length & Format

### EP (4-6 tracks)
**Best for**:
- Testing new direction
- Single concept explored deeply
- Introduction to new artist
- Tightly focused themes

**Structure**: Intro → Development → Climax → Resolution

### Standard Album (8-12 tracks)
**Best for**:
- Complete statements
- Narrative albums
- Established artist projects
- Traditional distribution

**Structure**: Three-act or thematic sections

### Double Album (15+ tracks)
**Best for**:
- Epic stories requiring space
- Comprehensive documentaries
- Sprawling concepts
- Career-defining statements

**Structure**: Movements, sections, or discs with distinct identities

**Challenge**: Maintaining listener attention - must justify length
