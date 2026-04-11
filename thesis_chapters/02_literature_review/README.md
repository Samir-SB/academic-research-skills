# Thesis Chapters - Chapter 2: Literature Review

## Files

- `02_literature_review.tex` - Main LaTeX chapter file (~5,500 words)
- `references.bib` - BibTeX references for the chapter

## Chapter Structure

| Section | Subsection | Content |
|---------|------------|---------|
| 2.1 | Introduction | Scope, objectives, organization |
| 2.2 | Fundamentals | Problem definition, NP-hard, QoS models |
| 2.3 | Traditional Approaches | GA, PSO, ACO heuristics |
| 2.4 | Mobile/Moving IoT | EaaS, DaaS evolution |
| 2.5 | ML & RL | Q-learning → DQN → A2C |
| 2.6 | Publishing Pattern | **Key insight** - Algorithm change pattern |
| 2.7 | Research Gap | What this thesis addresses |
| 2.8 | Summary | Key findings |

## Key Content

### Publishing Pattern (Section 2.6)

The chapter presents a novel analysis of the publishing pattern in IoT service composition research:

- **Energy-as-a-Service (EaaS)**: Papers E1-E9 demonstrate the "add one feature per paper" pattern
- **Drone-as-a-Service (DaaS)**: Papers D1-D7 follow the same pattern
- **Moving IoT**: Paper 17 (Neiat 2021) represents the DQN-based approach

### Your Contribution

- A2C (Actor-Critic) vs. Double DQN (Value-based)
- Polar coordinate state representation (r, cosθ, sinθ) vs. trajectory prediction
- Real pedestrian datasets (ATC indoor, Illinois outdoor) vs. synthetic data

## Usage

This chapter is designed to be included in your main thesis document:

```latex
\input{thesis_chapters/02_literature_review/02_literature_review}
```

Or compile independently:

```bash
cd thesis_chapters/02_literature_review
pdflatex 02_literature_review
bibtex 02_literature_review
pdflatex 02_literature_review
pdflatex 02_literature_review
```

## Word Count

Approximately 5,500 words (excluding references)

## References

~40+ citations covering:
- Fundamental works (Yu & Lin 2007)
- Surveys (Papers 01, 05, 11)
- EaaS papers (E1-E9)
- DaaS papers (D1-D7)
- Moving IoT (Paper 17)
- RL methods (A2C, DQN)