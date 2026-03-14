import os
from mcp.server.fastmcp import FastMCP
import storage

RAILWAY_HOST = os.environ.get(
    "RAILWAY_PUBLIC_DOMAIN", "sbu-syllabus-mcp-production.up.railway.app"
)

mcp = FastMCP("sbu-syllabus", host=RAILWAY_HOST)


@mcp.tool()
async def ping() -> str:
    """Test connection"""
    return "pong"


@mcp.tool()
async def list_courses() -> list[str]:
    """List all stored course codes"""
    courses = storage.list_courses()
    if not courses:
        return ["No courses stored yet"]
    return courses


@mcp.tool()
async def get_syllabus(course_code: str) -> dict | str:
    """Get full syllabus data for a course"""
    syllabus = storage.get_syllabus(course_code)
    if not syllabus:
        return f"No syllabus found for {course_code}"
    return syllabus


@mcp.tool()
async def get_exam_dates(course_code: str) -> list[dict] | str:
    """Get exam dates for a course"""
    syllabus = storage.get_syllabus(course_code)
    if not syllabus:
        return f"No syllabus found for {course_code}"
    return syllabus.get("exams", [])


@mcp.tool()
async def get_grading_breakdown(course_code: str) -> list[dict] | str:
    """Get grading policy breakdown for a course"""
    syllabus = storage.get_syllabus(course_code)
    if not syllabus:
        return f"No syllabus found for {course_code}"
    return syllabus.get("grading", [])


@mcp.tool()
async def get_policies(course_code: str) -> dict | str:
    """Get course policies (late work, attendance, etc.)"""
    syllabus = storage.get_syllabus(course_code)
    if not syllabus:
        return f"No syllabus found for {course_code}"
    return syllabus.get("policies", {})


@mcp.tool()
async def get_schedule(course_code: str) -> list[dict] | str:
    """Get weekly schedule/topics for a course"""
    syllabus = storage.get_syllabus(course_code)
    if not syllabus:
        return f"No syllabus found for {course_code}"
    return syllabus.get("schedule", [])


@mcp.tool()
async def upload_syllabus(
    course_code: str,
    title: str,
    credits: int,
    semester: str,
    modality: str,
    instructors: list[dict],
    meetings: list[dict],
    grading: list[dict],
    grade_scale: list[dict],
    exams: list[dict],
    policies: dict,
    schedule: list[dict],
    textbook: str | None = None,
) -> str:
    """
    Upload structured syllabus data.

    Claude should parse the syllabus PDF and extract all fields before calling this tool.

    Args:
        course_code: Course code like "CSE 351"
        title: Course title like "Introduction to Data Science"
        credits: Number of credits
        semester: Semester like "Spring 2026"
        modality: "in-person", "online-async", or "hybrid"
        instructors: List of instructors, each with "name", "email" (optional), "office_hours" (optional)
        meetings: List of meetings, each with "days" (list), "start_time", "end_time", "location" (optional). Empty list for online courses.
        grading: List of grading components, each with "name", "weight" (as decimal, e.g., 0.25 for 25%), "details" (optional)
        grade_scale: List of grade cutoffs, each with "letter", "min_percent", "max_percent" (optional)
        exams: List of exams, each with "name", "date", "time" (optional), "location" (optional)
        policies: Dict with keys "late_work", "attendance", "academic_integrity", "makeup_exam" (all optional)
        schedule: List of weekly topics, each with "week" (int), "topic", "due" (optional)
        textbook: Required textbook (optional)

    Returns:
        Confirmation message
    """
    syllabus_data = {
        "course": {
            "code": course_code,
            "title": title,
            "credits": credits,
            "semester": semester,
            "modality": modality,
        },
        "instructors": instructors,
        "meetings": meetings,
        "grading": grading,
        "grade_scale": grade_scale,
        "exams": exams,
        "policies": policies,
        "schedule": schedule,
        "textbook": textbook,
    }

    storage.save_syllabus(course_code, syllabus_data)

    return f"Successfully stored syllabus for {course_code}: {title} ({semester}). {len(exams)} exams, {len(grading)} grading components, {len(schedule)} weeks."


if __name__ == "__main__":
    import uvicorn
    from starlette.middleware.cors import CORSMiddleware

    app = mcp.sse_app()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
