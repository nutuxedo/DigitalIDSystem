# test for sheets.py
# pytest assert
from sheets import _find_columns, _normalize_column_name


def test_student_id():
    actual = _normalize_column_name("Student_ID")
    expected = "student id"
    assert actual == expected


def test_name():
    actual = _normalize_column_name("            Name")
    expected = "name"
    assert actual == expected


def test_first_name():
    actual = _normalize_column_name("FIRST   NAMe")
    expected = "first name"
    assert actual == expected


def test_find_columns():
    headers = [
        "id",
        "surname",
        "given name",
        "position",
        "sub-role",
        "headshot",
        "band",
        "approval status",
        "date and time",
        "email add",
    ]
    actual = _find_columns(headers)
    expected = {
        "id": "id",
        "lastname": "surname",
        "firstname": "given name",
        "role": "position",
        "subrole": "sub-role",
        "headshot": "headshot",
        "bandname": "band",
        "status": "approval status",
        "timestamp": "date and time",
        "email": "email add",
    }
    assert actual == expected
