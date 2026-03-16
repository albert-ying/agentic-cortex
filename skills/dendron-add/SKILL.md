# Dendron Add (Smart Router)

**Universal entry point for adding ANY information to a Dendron vault with automatic classification and routing.**

## When to Use

Invoke when the user wants to add information to their vault: meeting notes, paper references, project updates, person profiles, science concepts, daily journal entries, or any unstructured content that needs categorization.

## What It Does

1. **Analyzes** content to determine type (meeting, paper, project, person, science, daily)
2. **Extracts** entities (people, dates, topics, citations)
3. **Routes** to correct hierarchy (`meet.*`, `user.*`, `proj.*`, `sci.*`, `daily.*`, `scratch.*`)
4. **Creates** note with rich frontmatter, **updates** indexes, **commits** changes

## Usage

```
@dendron-add [content | file path | URL or DOI]
```

Options: `--batch [folder]`, `--force-category=meeting`, `--dry-run`

---

## Classification Logic

Score content against each category; highest wins. If confidence < 80%, route to `scratch.*`.

```python
scores = {cat: count_indicators(content, cat) for cat in CATEGORIES}
category = max(scores, key=scores.get)
confidence = scores[category] / sum(scores.values())
if confidence < 0.8:
    category = 'scratch'
```

### Indicator Keywords by Category

| Category | Route | Indicators |
|----------|-------|------------|
| Meeting | `meet.YYYY.MM.DD.md` | Date patterns, "with @name", "attendees:", "discussed", "met with", "call with", "TODO", "follow up" |
| Paper | `user.authorYYYY.md` | DOI `10.xxxx/xxxxx`, arXiv IDs, "et al.", "Abstract:", journal names, "published in" |
| Project | `proj.YYYY.name.md` | "active/paused/completed", "milestone", "Update:", "Status:", "Phase 1", "deadline" |
| Person | `user.first-last.md` | Email/phone, university names, "Professor/Dr./PhD student", "PI/collaborator/postdoc" |
| Science | `sci.domain.topic.md` | Domain keywords (below), equations, "Protocol:", "Methods:", tool names |
| Daily | `daily.journal.YYYY.MM.DD.md` | "Today I...", personal reflections, diary-like language |
| Ambiguous | `scratch.YYYY.MM.DD.HHMMSS.md` | Confidence < 80%; flagged for manual review |

### Domain Classification (for `sci.*` notes)

```yaml
biology: [protein, gene, cell, DNA, RNA, expression, genetic, biological, organism]
math: [equation, theorem, proof, statistics, probability, calculus, derivative]
physics: [force, energy, quantum, thermodynamics, entropy, particle]
ml: [neural, network, training, model, algorithm, deep learning, transformer]
disease: [cancer, alzheimer, diabetes, pathology, therapeutic, disease]
protein-design: [structure, folding, alphafold, rosetta, design, binder, computational]
tools: [software, pipeline, workflow, CLI, API, install, package]
protocol: [method, procedure, assay, protocol, experimental, laboratory]
review: [review, summary, meta-analysis, literature, survey]
ideas: [hypothesis, idea, proposal, brainstorm, concept, theory]
```

Prefer the most specific domain (e.g., "protein-design" over "biology"). Default to "ideas" if scientific but unclear.

---

## Workflow

### Step 1: Accept Input
Read content from string, file path, or URL (handle DOI redirect, arXiv, PDF).

### Step 2: Classify
Score against indicator lists; route to scratch if ambiguous.

### Step 3: Extract Entities

- **People**: Regex `\b[A-Z][a-z]+ [A-Z][a-z]+\b`, cross-check existing profiles:
  ```sql
  SELECT fname FROM Note n JOIN Vault v ON n.vaultId=v.id
  WHERE v.fsPath='.' AND fname LIKE 'user.%';
  ```
- **Dates**: Parse "Jan 20, 2026", "2026-01-20", "today" -> convert to `YYYY.MM.DD`
- **Citations**: DOI `10\.\d{4,}/[\S]+`, arXiv `arXiv:\d{4}\.\d{4,}`, "Author et al. (YYYY)"
- **Projects**: Cross-reference existing `proj.*` files
- **Topics**: Map noun phrases to existing `tags.*` entries

### Step 4: Generate Filename & Check Duplicates

```sql
SELECT fname FROM Note n JOIN Vault v ON n.vaultId=v.id
WHERE v.fsPath='.' AND fname='proposed.note.id';
```

### Step 5: Create Note with Frontmatter

**Required Dendron fields** (all notes):
- `id`: 23-char lowercase alphanumeric (`random.choices(string.ascii_lowercase + string.digits, k=23)`)
- `title`, `desc`, `updated` (ms timestamp), `created` (ms timestamp)

**Category-specific fields**:

| Category | Extra Fields |
|----------|-------------|
| Meeting | `date`, `attendees` (list of `user.*`), `projects` (list of `proj.*`), `topics` |
| Paper | `authors`, `year`, `journal`, `doi`, `domains`, `topics`, `related_projects` |
| Project | `status`, `start_date`, `people` (list of `user.*`), `topics`, `related_science` |
| Science | `domain`, `subdomain`, `related_papers`, `related_projects` |

**Example** (meeting):
```yaml
---
id: a1b2c3d4e5f6g7h8i9j0k1l
title: Lab meeting — binder screening results
desc: 'Discussed screening data with Sarah and David'
updated: 1710100000000
created: 1710100000000
date: 2026.03.10
attendees: [user.sarah-kim, user.david-lee]
projects: [proj.2026.protein-design]
topics: [yeast-display, binding-affinity]
---
```

### Step 6: Update Indexes

Diff-based edits (not full rewrites) to:
1. **Main index**: `meet.md`, `user.md`, `proj.md`, etc. — add one-line entry
2. **Year/month indexes**: `meet.YYYY.md`, `proj.YYYY.md` (if applicable)
3. **Cross-references**: `_index.by-person.md`, `_index.by-project.md`, `_index.by-topic.md`

### Step 7: Preview & Confirm

```
Classification: Meeting Note (92%)
Route: meet.2026.03.10.md
Attendees: Sarah Kim, David Lee
Projects: proj.2026.protein-design
Topics: yeast-display, binding-affinity
Indexes to update: meet.md, meet.2026.md, _index.by-person.md, _index.by-project.md
Proceed? (Y/n)
```

### Step 8: Commit

```bash
git add notes/meet.2026.03.10.md notes/meet.md notes/meet.2026.md notes/_index.*
git commit -m "Add: meeting — Lab meeting on binder screening results"
```

---

## Safety & Validation

### Before Creating
1. **Check for duplicates** via SQLite (Step 4)
2. **Validate date format**: must be `YYYY.MM.DD`
3. **Confirm ambiguous classifications**: prompt user if confidence < 80%

### Never Do
- Overwrite existing notes without user confirmation
- Create filenames with spaces or special characters
- Skip frontmatter metadata
- Forget to update indexes
- Use placeholder text — every field must be populated or omitted
