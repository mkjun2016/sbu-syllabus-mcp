from mcp.server.fastmcp import FastMCP
import storage

mcp = FastMCP("sbu-syllabus")


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
async def upload_syllabus(course_code: str, syllabus_text: str) -> str:
    """
    Upload and parse syllabus from text content.

    Args:
        course_code: Course code like "CSE 351"
        syllabus_text: Full text content of the syllabus PDF

    Returns:
        Confirmation message with parsed data summary
    """
    # TODO: Week 2 - Implement structured extraction with Claude API
    # For now, only raw text is stored
    storage.save_syllabus(course_code, {"raw_text": syllabus_text, "parsed": False})
    return f"Stored raw syllabus for {course_code} ({len(syllabus_text)} chars). Parsing not yet implemented."


if __name__ == "__main__":
    mcp.run()
