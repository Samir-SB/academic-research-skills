# AGENTS.md - PhD Thesis: A2C-Based Moving IoT Service Composition

## Project Context

**Main Thesis**: A2C-Based Proactive Composition for Moving IoT Services (IEEE Transactions on Services Computing)

**Research Focus** (from Notion):
- Selection and deployment of IoT services in dynamic environments
- Moving IoT services = services from mobile devices (location + availability change over time)
- Spatio-temporal properties: where + when service is available
- Core challenge: maintain QoS under device mobility

## Directory Structure

```
reference-paper/
├── main_paper/           # Your PhD thesis (A2C-Moving-IoT-Service-Composition-v4.*)
├── 01-17/                # Reference papers for literature review
├── analysis/             # Cross-paper analysis
├── peer_reviews/         # Consolidated peer reviews
└── surveys_summaries/    # Survey summaries

experiments-codesource/   # Experiment code (DQN, A2C, baselines)
├── claude_a2c_online.py # Main A2C implementation
├── dqn.py                # DQN baseline
├── configs/              # Experiment configs
└── data/                 # Experiment data
```

## Critical Workflows

### 1. Reference Paper Analysis

When analyzing papers in `reference-paper/XX/`:
1. **Confirm title first** — filename may differ from actual paper title
2. Read PDF with `read` tool (not OCR - use PDF directly)
3. Create: `XX/peer-review-analysis.md` (30 Q&A in 5 sections)
4. Update: `reference-paper/main_paper/summary-table.md` (add row + update stats)
5. **Commit** with git

**Common pitfalls**:
- Don't assume filename = title
- Papers are `01/`, `02/`, not sorted by year
- Always update summary-table.md when adding new paper

### 2. Main Paper Development

- Main paper: `reference-paper/main_paper/A2C-Moving-IoT-Service-Composition-v4.*`
- LaTeX source: `reference-paper/main_paper/main.tex` + sections `01_abstract.tex` - `12_source_code.tex`
- Bibliography: `A2C-Moving-IoT-Service-Composition-v4.bib`

### 3. Running Experiments

**Using Stable Baselines3** instead of custom implementations:
- A2C: `sb3.A2C` (`stable_baselines3.A2C`)
- DQN: `sb3.DQN` (`stable_baselines3.DQN`)

```bash
# Install stable-baselines3
pip install stable-baselines3

# Training
cd experiments-codesource
python train.py

# Run experiments batch
./run_experiments.sh
```

## Key Research Context

**Moving IoT Services** differ from static services:
- Location changes over time
- Availability is time-dependent
- Require spatio-temporal querying ("available here and now?")
- QoS degrades under mobility (link quality → latency → reliability)

**Core Problem**: Select, compose, maintain IoT services where services are mobile and spatio-temporal properties evolve, without QoS degradation.

---

*For academic pipeline skills (deep-research, paper writing), see `.claude/CLAUDE.md`*