from pydantic import BaseModel


class CourseInfo(BaseModel):
    code: str  # "CSE 351", "LIN 200"
    title: str
    credits: int
    semester: str  # "Spring 2026"
    modality: str  # "in-person", "online-async", "hybrid"


class Instructor(BaseModel):
    name: str
    email: str | None = None
    office_hours: str | None = None  # "Mon/Wed 12-1:30pm NCS 202"


class Meeting(BaseModel):
    days: list[str]  # ["Mon", "Wed"]
    start_time: str  # "2:00 PM"
    end_time: str  # "3:20 PM"
    location: str | None = None  # "Harriman Hall 137"


class GradingComponent(BaseModel):
    name: str  # "Midterm", "Final", "Homework"
    weight: float  # 0.25 = 25%
    details: str | None = None  # "Midterm1 20% + Midterm2 20%"


class ExamInfo(BaseModel):
    name: str  # "Midterm 1", "Final"
    date: str  # "3/4" or "May 15"
    time: str | None = None  # "2:00 PM - 3:20 PM"
    location: str | None = None


class GradeScale(BaseModel):
    letter: str  # "A", "A-", "B+"
    min_percent: float  # 93.0
    max_percent: float | None = None  # 100.0


class Policies(BaseModel):
    late_work: str | None = None
    attendance: str | None = None  # "4+ absences = F"
    academic_integrity: str | None = None
    makeup_exam: str | None = None


class WeeklyTopic(BaseModel):
    week: int
    topic: str
    due: str | None = None  # what's due that week


class Syllabus(BaseModel):
    course: CourseInfo
    instructors: list[Instructor]
    meetings: list[Meeting]  # empty list for online courses
    grading: list[GradingComponent]
    grade_scale: list[GradeScale]
    exams: list[ExamInfo]
    policies: Policies
    schedule: list[WeeklyTopic]
    textbook: str | None = None
