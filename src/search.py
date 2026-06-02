from rapidfuzz import fuzz

from src.case_service import list_cases


def build_search_text(case):
    parts = [
        case.get("title", ""),
        case.get("system", ""),
        case.get("category", ""),
        case.get("description", ""),
        case.get("symptoms", ""),
        case.get("attempted_steps", ""),
        case.get("cause", ""),
        case.get("resolution", ""),
        case.get("tags", ""),
    ]

    return " ".join([str(part) for part in parts if part])


def search_similar_cases(query, min_score=20, limit=5):
    cases = list_cases()
    results = []

    for case in cases:
        searchable_text = build_search_text(case)

        score = fuzz.token_set_ratio(query.lower(), searchable_text.lower())

        if score >= min_score:
            results.append(
                {
                    "score": score,
                    "case": case,
                }
            )

    results = sorted(results, key=lambda item: item["score"], reverse=True)

    return results[:limit]