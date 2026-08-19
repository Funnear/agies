# Music Industry Behavioral Patterns Report

> **Dataset**: AGIES Music Industry Knowledge Graph (50 Entities, 87 Relations)  
> **Generated**: 2026-08-19

---

## 1. Executive Summary & Graph Topology

| Metric | Value |
| :--- | :--- |
| **Total Entity Nodes** | 50 |
| **Total Relationship Edges** | 87 |
| **Artist Nodes** | 18 |
| **Record Labels** | 10 (Major & Indie) |
| **Talent & Management Agencies** | 6 (WME, CAA, UTA, Roc Nation, Red Light, Primary) |
| **Recording Studios** | 6 (Abbey Road, Electric Lady, Sunset Sound, Metropolis, Conway, RAK) |
| **Producers / Production Houses** | 10 (Max Martin, Jack Antonoff, Rick Rubin, Brian Eno, Metro Boomin, Finneas) |

---

## 2. Power Broker & Gatekeeper Analysis

### Top Power Brokers (PageRank)
1. **WME (William Morris Endeavor)** (Agency) — `0.0442` (8 core client connections)
2. **Drake** (Artist) — `0.0383` (Major collaboration hub & multi-label influence)
3. **Kendrick Lamar** (Artist) — `0.0351` (High cross-genre bridge centrality)
4. **Future** (Artist) — `0.0345` (Prolific collaborative density)
5. **Taylor Swift** (Artist) — `0.0327` (Elite agency-label-producer power triad)

### Key Takeaway:
**Talent Agencies** (WME, CAA) and **Super-Producers** (Jack Antonoff, Max Martin, Rick Rubin) act as the primary structural power brokers, anchoring entire clusters of multi-genre artists.

---

## 3. Creative Ecosystems & Production Cliques

Modularity clustering (Louvain algorithm) uncovered **6 distinct creative sub-communities**:

1. **Indie & Pop Power Circle (11 members)**:
   - *Members*: Taylor Swift, Phoebe Bridgers, Clairo, Bleachers Sound Labs, Jack Antonoff, Electric Lady Studios, WME, Republic Records.
   - *Dominant Genres*: Indie Pop, Pop, Alternative.
2. **UK & European Electronic Ecosystem (11 members)**:
   - *Members*: Aphex Twin, Four Tet, Bonobo, BICEP, Brian Eno, Warp Records, Ninja Tune, Abbey Road Studios, Metropolis Studios.
   - *Dominant Genres*: Electronic, IDM, Ambient, Breakbeat.
3. **Hip-Hop & Sonic Architecture Hub (7 members)**:
   - *Members*: Kendrick Lamar, Flying Lotus, Rick Rubin, Shangri-La Creative, Conway Studios, Interscope.
   - *Dominant Genres*: Hip-Hop, Jazz Rap, Experimental.
4. **Mainstream Pop & Hit-Making Factory (7 members)**:
   - *Members*: The Weeknd, Dua Lipa, Max Martin, MXM Music Productions, CAA, RAK Studios, Atlantic Records.
   - *Dominant Genres*: Pop, Dance, Disco, Synthwave.

---

## 4. Behavioral Pattern 1: Label Mobility & Churn

- **Overall Industry Migration Rate**: `22.2%`
- **Loyal / Single-Label Artists (`77.8%`)**: 14 artists (e.g. Billie Eilish, Radiohead, BICEP, Bonobo, Aphex Twin).
- **Migrated / Multi-Label Artists (`22.2%`)**: 4 artists:
  - **Taylor Swift**: Big Machine Records / Sub Pop -> Republic Records.
  - **Drake**: Def Jam Recordings -> Republic Records.
  - **Kendrick Lamar**: Def Jam / Top Dawg -> Interscope Records.
  - **Clairo**: 4AD / Fader -> Republic Records.

---

## 5. Behavioral Pattern 2: Studio & Producer Reliance Index (SPRI)

- **High Studio/Producer Concentration (`72.2%`)**: 13 out of 18 artists have tight, signature reliance on a single primary studio and executive producer (e.g. Billie Eilish + Finneas + Sunset Sound, Phoebe Bridgers + Jack Antonoff + Electric Lady).
- **Flexible / Modular Sound Architects (`27.8%`)**: 5 artists rotate recording spaces and self-produce without single-studio lock-in.

---

## 6. Behavioral Pattern 3: Agency Collaboration Dynamics

- **Total Track Collaborations Analyzed**: 13
- **Intra-Agency Collaborations**: 6 (`46.2%`)
- **Inter-Agency Collaborations**: 7 (`53.8%`)
- **Behavior Interpretation**: **Balanced Cross-Agency Collaboration**.
  - While mega-agencies like WME facilitate intra-roster features (e.g. Drake + Future, Taylor Swift + Phoebe Bridgers), top artists actively bridge across rival agencies for high-profile musical releases.
