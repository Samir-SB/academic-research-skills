# AGENTS.md - Academic Research Skills

## Reference Paper Analysis Workflow

When analyzing new research papers in `reference-paper/XX/` folders:

### Critical Steps

1. **Confirm paper title before reading** - Use `question` tool to verify the exact title, as filename may differ from actual paper title

2. **Read the PDF first** - Use `read` tool on the PDF file to get full content

3. **Create peer review files** - After reading:
   - `XX/peer-review-analysis.md` - Full peer review with 30 Q&A
   - `XX/research-summary.md` - Concise summary

4. **Update summary table** - Edit `reference-paper/summary-table.md`:
   - Add new row with title, year, algorithm, paper type
   - Update statistics section

5. **Commit changes** - Use git to track new analysis

### Summary Table Format

| # | Title | Year | Algorithm Used | Paper Type |
|---|-------|------|----------------|------------|

Update these stats after each new paper:
- Total Papers
- Systematic Reviews / Original Research counts
- Algorithm distribution

### Common Issues to Avoid

- **Don't assume filename = title** - Always confirm with user before proceeding
- **Check folder structure** - Papers are in `reference-paper/01/`, `02/`, etc.
- **Keep table updated** - Always update summary-table.md when adding new paper

---

*For full academic pipeline skills, see `.claude/CLAUDE.md`*
