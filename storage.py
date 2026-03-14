import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "syllabi.json"


def load_all() -> dict:
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return {}


def save_all(data: dict):
    DATA_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))


def get_syllabus(course_code: str) -> dict | None:
    return load_all().get(course_code)


def save_syllabus(course_code: str, syllabus: dict):
    data = load_all()
    data[course_code] = syllabus
    save_all(data)


def delete_syllabus(course_code: str) -> bool:
    data = load_all()
    if course_code in data:
        del data[course_code]
        save_all(data)
        return True
    return False


def list_courses() -> list[str]:
    return list(load_all().keys())
