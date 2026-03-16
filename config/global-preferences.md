# Global Preferences

## User Identity

- **Name**: {{USER_NAME}}
- **Email**: {{USER_EMAIL}}

## Version Control

- **Always commit before modifying code**: `git add .` && `git commit -m "descriptive message"` before making changes
- Meaningful commit messages describing what and why
- Preserve version history by committing before major changes

## Data Integrity (ABSOLUTE PROHIBITION)

Never simulate, fabricate, or generate artificial data or statistical results under any circumstances.

- Use only real, authentic datasets provided by the user or referenced in the codebase
- Load data from actual files — never create synthetic datasets
- Report only computed results from genuine data analysis — never estimate or approximate
- When data is unavailable: stop and state "Cannot proceed — required data file not found: [filepath]"
- Never substitute mock data or "typical" values from literature

## File Management

- **Modify existing scripts** rather than creating new files
- **Do NOT override files created by others** or pre-existing files
- Name new files with clear descriptions and dates (e.g., `analysis_2024-01-15.py`)
- Keep the workspace clean — move unused scripts to an `outdated` folder

## Error Handling

- Include try-catch blocks for file operations and external API calls
- Provide meaningful error messages for debugging
- Log important steps and potential issues

## Persistent Memory (MANDATORY)

Use the auto-memory system actively in every session. This is not optional.

### Session Start
- Read `MEMORY.md` and any relevant topic files from the memory directory to restore context from prior sessions.

### Continuous Updates
After each interaction, evaluate whether memory needs updating. Write immediately when:
- A task is completed or a meaningful milestone is reached
- A decision is made or an approach is chosen
- The user corrects something or states a preference
- New project context, people, or conventions are discovered
- Previous memory entries become outdated or wrong

Do NOT document every interaction — only write when there's genuine signal worth persisting.

### What to Track
- **Active projects**: current status, next steps, blockers
- **Decisions made**: why a particular approach was chosen
- **User corrections**: if the user corrects something, update memory immediately
- **Recurring context**: file paths, environment details, workflow steps that come up repeatedly
- **People & collaborators**: who's involved in what, meeting outcomes
