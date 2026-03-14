# SBU Syllabus MCP

An MCP server that transforms course syllabi into structured, queryable data — accessible directly from Claude.ai.

## Problem

Students manually dig through multiple syllabi every semester to track exams, deadlines, and policies. This is repetitive and doesn't integrate with AI tools.

## Solution

Upload a syllabus PDF to Claude.ai → Claude parses it → stores structured data in MCP server → query anytime with natural language.

```
┌──────────┐     ┌───────────┐     ┌────────────┐
│  Upload  │────▶│ Claude.ai │────▶│ MCP Server │
│   PDF    │     │ (parses)  │     │ (stores)   │
└──────────┘     └───────────┘     └────────────┘
                       │
                       ▼
              "When's my exam?"
                       │
                       ▼
              "May 15, 2:15 PM"
```

## Tech Stack

- **Protocol**: Model Context Protocol (MCP)
- **Server**: FastMCP + Starlette + SSE
- **Storage**: JSON
- **Hosting**: Railway
- **Runtime**: Python 3.10+ / uv

## Usage

### 1. Connect

Add to Claude.ai → Settings → Integrations:
```
https://sbu-syllabus-mcp-production.up.railway.app/sse
```

### 2. Upload

Attach PDF and say:
> "Parse and upload this syllabus"

### 3. Query

> "When are my CSE 351 exams?"  
> "How is LIN 200 graded?"  
> "What's the late policy for CSE 300?"

## Features

- **Syllabus Parsing**: Extracts course info, exams, grading, policies, and weekly schedule
- **Natural Language Queries**: Ask questions about any stored course
- **Multi-Course Support**: Store and query multiple syllabi
- **Zero API Cost**: Claude.ai handles parsing — no additional API keys needed
- **Persistent Storage**: Data persists across sessions

## Architecture

```
server.py      # MCP server + tools
storage.py     # JSON persistence
schema.py      # Pydantic models
```

### Data Schema

```
Syllabus
├── course: { code, title, credits, semester, modality }
├── instructors: [{ name, email, office_hours }]
├── meetings: [{ days, start_time, end_time, location }]
├── grading: [{ name, weight, details }]
├── grade_scale: [{ letter, min_percent, max_percent }]
├── exams: [{ name, date, time, location }]
├── policies: { late_work, attendance, academic_integrity, makeup_exam }
├── schedule: [{ week, topic, due }]
└── textbook
```

### Tools

| Tool | Description |
|------|-------------|
| `upload_syllabus` | Store parsed syllabus data |
| `get_syllabus` | Get full syllabus |
| `get_exam_dates` | Get exam dates |
| `get_grading_breakdown` | Get grading weights |
| `get_policies` | Get course policies |
| `get_schedule` | Get weekly schedule |
| `list_courses` | List stored courses |

## Why MCP?

- Native Claude.ai integration — no custom UI needed
- Standardized tool protocol
- SSE streaming built-in
- Works with Claude Desktop too

## Local Development

```bash
git clone https://github.com/mkjun2016/sbu-syllabus-mcp
cd sbu-syllabus-mcp
uv sync
uv run python server.py
```

### Claude Desktop Config

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "sbu-syllabus": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/sbu-syllabus-mcp", "python", "server.py"],
      "cwd": "/path/to/sbu-syllabus-mcp"
    }
  }
}
```

## Deployment

Deployed on Railway with automatic GitHub integration.

```
# Procfile
web: python server.py
```

## Roadmap

- [x] MCP server setup + schema design
- [x] SSE transport for remote access
- [x] Railway deployment
- [x] Claude.ai integration
- [x] Structured syllabus upload
- [x] Query tools (exams, grading, policies, schedule)
- [ ] Calendar export (ICS)
- [ ] Cross-course conflict detection
- [ ] Deadline reminders

## License

MIT