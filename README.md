# SBU Syllabus MCP

An MCP server that converts Stony Brook University syllabi into structured data, queryable directly from Claude Desktop.

## What It Does

```
[Student] → [Claude Desktop] → [MCP Server] → [Structured Syllabus Data]
            "When's my CSE 351 exam?"    ↓
                                    { exams: [...] }
```

Upload a syllabus PDF and it automatically parses:
- Exam dates
- Grading breakdown
- Assignment deadlines
- Attendance/late policies
- Weekly schedule

All stored as structured JSON. Query with natural language in Claude Desktop and get accurate info via MCP tools.

## Installation

```bash
git clone https://github.com/your-username/sbu-syllabus-mcp
cd sbu-syllabus-mcp
uv sync
```

## Connect to Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "sbu-syllabus": {
      "command": "/Users/YOUR_USERNAME/.local/bin/uv",
      "args": ["run", "--directory", "/path/to/sbu-syllabus-mcp", "python", "server.py"],
      "cwd": "/path/to/sbu-syllabus-mcp"
    }
  }
}
```

Restart Claude Desktop.

## Usage

In Claude Desktop:

```
# Upload syllabus
[Attach PDF] "Upload this as CSE 351"

# Check exam dates
"When are my CSE 351 exams?"

# Grading breakdown
"How is CSE 351 graded?"

# Policy check
"What's the late policy for CSE 351?"

# List stored courses
"What courses do I have stored?"
```

## MCP Tools

| Tool | Description |
|------|-------------|
| `ping` | Connection test |
| `list_courses` | List stored course codes |
| `upload_syllabus` | Upload and parse syllabus text |
| `get_syllabus` | Full syllabus data |
| `get_exam_dates` | Exam dates only |
| `get_grading_breakdown` | Grading weights only |
| `get_policies` | Attendance/late/makeup policies |
| `get_schedule` | Weekly topics |

## Project Structure

```
sbu-syllabus-mcp/
├── server.py      # MCP server + tool definitions
├── storage.py     # JSON file storage
├── schema.py      # Pydantic schemas
├── syllabi.json   # Stored syllabus data
└── pyproject.toml
```

## Roadmap

- [x] Week 1: MCP server setup + schema design
- [ ] Week 2: Claude API integration for PDF → structured JSON parsing
- [ ] Week 3: Query tools refinement + edge case handling
- [ ] Week 4: Parsing accuracy tuning
- [ ] Week 5: Beta testing
- [ ] Week 6: Feedback integration
- [ ] Week 7: Documentation + deployment

## License

MIT