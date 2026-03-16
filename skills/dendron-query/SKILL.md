# Dendron Query

**Query the Dendron knowledge base using indexes and SQLite for efficient information retrieval.**

## When to Use

Invoke when the user wants to find information in their vault: people, project status, scientific topics, recent activity, keyword search, or meeting preparation.

## What It Does

1. **Parses** natural language query to determine intent
2. **Routes** to the appropriate entry point (by-person, by-project, by-topic, by-date, keyword)
3. **Traverses** note graph to collect related notes
4. **Reads** relevant notes in context
5. **Synthesizes** a structured response with source links

## Usage

```
@dendron-query [natural language query]
```

**Examples**:
- `@dendron-query Find everything about Sarah Kim`
- `@dendron-query What's the status of the protein design project?`
- `@dendron-query Show all papers on aging clocks`
- `@dendron-query What did I discuss in meetings last week?`

---

## Query Types & Routing

### Person Query -> `_index.by-person.md`

**Indicators**: "about [Person]", "related to [Person]", "with [Person]", "who is [Person]"

1. Read `_index.by-person.md` -> find person's section
2. Follow links to projects, meetings, papers, contact info
3. Read their `user.*` note for full context
4. Check recent mentions via SQLite:
   ```sql
   SELECT fname, title FROM Note n JOIN Vault v ON n.vaultId=v.id
   WHERE v.fsPath='.' AND raw LIKE '%person-name%'
   ORDER BY updated DESC LIMIT 10;
   ```
5. Synthesize overview with links to all related notes

### Project Query -> `_index.by-project.md`

**Indicators**: "project status", "about [Project]", "progress", "what's happening with"

1. Read `_index.by-project.md` -> find project section
2. Read main project file: `proj.YYYY.project-name.md`
3. Extract people, science, and meetings from frontmatter links
4. Check recent mentions via SQLite
5. Return status + context + next steps

### Topic Query -> `_index.by-topic.md`

**Indicators**: "papers on", "research about", "all notes on", "everything about [concept]"

1. Read `_index.by-topic.md` -> find topic section
2. Collect all linked notes (projects, science, papers)
3. Fall back to ripgrep content search if index is insufficient
4. Organize by type and return structured summary

### Date/Time Query -> SQLite

**Indicators**: "last week", "recent", "today", "yesterday", "meetings in January"

```sql
SELECT fname, title, date(updated/1000,'unixepoch') as modified
FROM Note n JOIN Vault v ON n.vaultId=v.id
WHERE v.fsPath='.'
AND (fname LIKE 'daily.journal.%' OR fname LIKE 'meet.%')
AND date(n.updated/1000,'unixepoch') >= date('now','-7 day')
ORDER BY fname DESC;
```

### Keyword Search -> ripgrep + SQLite

**Indicators**: "find notes with", "search for", "mentions of", or any unmatched query

```sql
SELECT fname, title FROM Note n JOIN Vault v ON n.vaultId=v.id
WHERE v.fsPath='.' AND raw LIKE '%keyword%'
ORDER BY updated DESC LIMIT 20;
```

Supplement with ripgrep when SQLite `raw` column is incomplete or for multi-word phrases.

---

## Common SQL Templates

```sql
-- Recent activity (last 7 days)
SELECT fname, title, date(updated/1000,'unixepoch') as modified
FROM Note n JOIN Vault v ON n.vaultId=v.id
WHERE v.fsPath='.' AND date(updated/1000,'unixepoch') >= date('now','-7 day')
ORDER BY updated DESC;

-- All meetings mentioning a person
SELECT fname, title FROM Note n JOIN Vault v ON n.vaultId=v.id
WHERE v.fsPath='.' AND fname LIKE 'meet.%' AND raw LIKE '%person-name%'
ORDER BY fname DESC;

-- Papers on a topic
SELECT fname, title, desc FROM Note n JOIN Vault v ON n.vaultId=v.id
WHERE v.fsPath='.' AND fname LIKE 'user.%'
AND (raw LIKE '%topic%' OR tags LIKE '%topic%');

-- Active projects
SELECT fname, title FROM Note n JOIN Vault v ON n.vaultId=v.id
WHERE v.fsPath='.' AND fname LIKE 'proj.%' AND raw LIKE '%status%active%';

-- All people (excluding paper references)
SELECT fname, title FROM Note n JOIN Vault v ON n.vaultId=v.id
WHERE v.fsPath='.' AND fname LIKE 'user.%' AND fname NOT LIKE 'user.%[0-9][0-9][0-9][0-9]'
ORDER BY fname;
```

---

## Response Format

Structure every response with:

1. **Summary** — 2-3 sentences, most important information first
2. **Details** — Organized by category or chronology
3. **Sources** — Dendron links: `[[title|note.id]]`
4. **Next Steps** — Follow-up queries or actions (when applicable)

**Example**:

```
## Summary
Sarah Kim is the PI of the aging biology lab at Westfield University.
She advises two active projects and was last seen in the March 10 lab meeting.

## Details
- **Profile**: Professor, Dept. of Biology, Westfield University
- **Projects**: [[Protein Binder Design|proj.2026.protein-design]], [[Foundation Model|proj.2026.foundation-model]]
- **Recent**: [[Lab meeting Mar 10|meet.2026.03.10]] — binder screening results

## Sources
[[user.sarah-kim]], [[proj.2026.protein-design]], [[proj.2026.foundation-model]], [[meet.2026.03.10]]

## Next Steps
- `@dendron-query meetings with Sarah Kim in 2026`
- `@dendron-query protein design project status`
```

---

## Advanced Features

- **Multi-Entity**: Find connections between two people or topics (shared meetings, overlapping projects)
- **Temporal**: Compare project state across time by reading notes from different date ranges
- **Aggregation**: List all active projects with summaries, or all people in a given project
- **Meeting Prep**: Combine person + project queries to build context before an upcoming meeting
