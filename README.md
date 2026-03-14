# SBU Syllabus MCP

Stony Brook University 실라버스를 structured data로 변환하고, Claude Desktop에서 바로 조회할 수 있게 해주는 MCP 서버.

## 뭘 하는 건가

```
[학생] → [Claude Desktop] → [MCP Server] → [Structured Syllabus Data]
         "CSE 351 시험 언제야?"     ↓
                              { exams: [...] }
```

실라버스 PDF를 업로드하면 자동으로 파싱해서:
- 시험 날짜
- 성적 비중
- 과제 마감일
- 출석/지각 정책
- 주차별 스케줄

등을 structured JSON으로 저장. 이후 Claude Desktop에서 자연어로 질문하면 MCP tool을 통해 정확한 정보 제공.

## 설치

```bash
git clone https://github.com/mkjun2016/sbu-syllabus-mcp
cd sbu-syllabus-mcp
uv sync
```

## Claude Desktop 연결

`~/Library/Application Support/Claude/claude_desktop_config.json`:

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

Claude Desktop 재시작 후 사용 가능.

## 사용법

Claude Desktop에서:

```
# 실라버스 업로드
[PDF 첨부] "이 실라버스 CSE 351로 업로드해줘"

# 시험 일정 조회
"CSE 351 시험 언제야?"

# 성적 비중 확인
"CSE 351 성적 어떻게 매겨?"

# 정책 확인  
"CSE 351 지각하면 어떻게 돼?"

# 저장된 수업 목록
"저장된 수업 뭐있어?"
```

## MCP Tools

| Tool | 설명 |
|------|------|
| `ping` | 연결 테스트 |
| `list_courses` | 저장된 수업 코드 목록 |
| `upload_syllabus` | 실라버스 텍스트 업로드 및 파싱 |
| `get_syllabus` | 전체 실라버스 데이터 |
| `get_exam_dates` | 시험 날짜만 |
| `get_grading_breakdown` | 성적 비중만 |
| `get_policies` | 출석/지각/과제 정책 |
| `get_schedule` | 주차별 스케줄 |

## 프로젝트 구조

```
sbu-syllabus-mcp/
├── server.py      # MCP 서버 + tool 정의
├── storage.py     # JSON 파일 기반 저장소
├── schema.py      # Pydantic 스키마
├── syllabi.json   # 저장된 실라버스 데이터
└── pyproject.toml
```

## 개발 로드맵

- [x] Week 1: MCP 서버 세팅 + 스키마 설계
- [ ] Week 2: Claude API로 PDF → structured JSON 파싱
- [ ] Week 3: Query tools 고도화 + edge case 처리  
- [ ] Week 4: 파싱 정확도 튜닝
- [ ] Week 5: 베타 테스트
- [ ] Week 6: 피드백 반영
- [ ] Week 7: 문서화 + 배포

## License

MIT