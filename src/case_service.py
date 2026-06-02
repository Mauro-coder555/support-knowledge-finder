from src.database import (
    insert_case,
    get_all_cases,
    get_case_by_id,
    update_case,
    delete_case,
)
from src.validators import validate_case


def create_case(case_data):
    errors = validate_case(case_data)

    if errors:
        return {
            "success": False,
            "errors": errors,
            "case_id": None,
        }

    case_id = insert_case(case_data)

    return {
        "success": True,
        "errors": [],
        "case_id": case_id,
    }


def list_cases():
    return get_all_cases()


def get_case(case_id):
    return get_case_by_id(case_id)


def edit_case(case_id, case_data):
    errors = validate_case(case_data)

    if errors:
        return {
            "success": False,
            "errors": errors,
        }

    update_case(case_id, case_data)

    return {
        "success": True,
        "errors": [],
    }


def remove_case(case_id):
    delete_case(case_id)

    return {
        "success": True,
    }


def is_case_resolved(case_data):
    return case_data.get("status") in ["Resuelto", "Verificado"]