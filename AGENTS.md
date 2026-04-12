# AGENTS.md - PhD Thesis: A2C-Based Moving IoT Service Composition

## Project Context

**Main Thesis**: A2C-Based Proactive Composition for Moving IoT Services (IEEE Transactions on Services Computing)

## Current Paper Location

```
main_paper/
├── A2C-Moving-IoT-Service-Composition-merged.tex   # Main paper (13 pages)
├── A2C-Moving-IoT-Service-Composition-merged.pdf
└── peer-review-comprehensive.md                # Peer review analysis
```

## Directory Structure

```
reference-paper/
├── XX/                     # Reference papers 01-25 with PDFs
├── summary-table.md         # Paper analysis summary
└── literature-review-synthesis.md

experiments-codesource/     # Experiment code (DQN, A2C baselines)

thesis_chapters/
├── 02_literature_review/                    
└───├── 02_literature_review.tex
    ├── 02_literature_review.pdf
    ├── references.bib
    └── README.md  
```

## Key Commands

```bash
# Compile paper
cd main_paper
pdflatex A2C-Moving-IoT-Service-Composition-merged.tex

# Clean build artifacts
rm -f *.aux *.log *.out *.bak*
```

## Research Context

**Problem**: Select, compose, maintain IoT services where services are mobile (location + availability change over time).

**Approach**: A2C (Advantage Actor-Critic) with STR (Signal Transmission Reward) model.

**Datasets**: ATC Shopping Center (Osaka), Illinois Commute

## Common Pitfalls

- Paper path is `main_paper/`, not `reference-paper/main_paper/`
- LaTeX compiles with pdflatex, not xelatex (font handling differs)
- IEEE Transactions uses `natbib` with `numbers` option