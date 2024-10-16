""" Fitness tests/standards collection"""

from typing import List, Tuple, Dict, Any
from service.repo import get_profile


AGE_GROUPS_ARMY = [
    (17, 22, "17-22"),
    (23, 26, "22-26"),
    (27, 31, "27-31"),
    (32, 36, "32-36"),
    (37, 41, "37-41"),
    (42, 46, "42-46"),
    (47, 51, "47-51"),
    (52, 56, "52-56"),
    (57, 61, "57-61"),
    (62, float("inf"), "62+"),
]

US_ARMY_AGE_RANGE = {
    "17-22": (42, 71),
    "22-26": (40, 75),
    "27-31": (39, 77),
    "32-36": (36, 75),
    "37-41": (34, 73),
    "42-46": (31, 66),
    "47-51": (25, 59),
    "52-56": (20, 56),
    "57-61": (18, 54),
    "62+": (16, 50),
}


def get_army_pushup_range(age: int) -> Tuple[int, int]:
    """U.S. Army Standards, push-ups are performed within a two-minute period"""

    if age < 17:
        raise ValueError("Age must be at least 17")

    result = next(
        (
            US_ARMY_AGE_RANGE[age_group]
            for min_age, max_age, age_group in AGE_GROUPS_ARMY
            if min_age <= age <= max_age
        ),
        None,
    )
    if result is None:
        raise ValueError(f"No pushup range found for age {age}")
    return result


# Define age ranges and corresponding group names
AGE_GROUPS: List[Tuple[int, Any, str]] = [
    (0, 29, "Under 30"),
    (30, 39, "30-39"),
    (40, 49, "40-49"),
    (50, 59, "50-59"),
    (60, float("inf"), "60+"),
]

# Define rating thresholds for each age group
RATINGS: Dict[str, Dict[str, Tuple[int, Any]]] = {
    "Under 30": {
        "Excellent": (51, float("inf")),
        "Very good": (41, 50),
        "Good": (31, 40),
        "Average": (21, 30),
        "Poor": (0, 20),
    },
    "30-39": {
        "Excellent": (47, float("inf")),
        "Very good": (37, 46),
        "Good": (27, 36),
        "Average": (17, 26),
        "Poor": (0, 16),
    },
    "40-49": {
        "Excellent": (40, float("inf")),
        "Very good": (31, 39),
        "Good": (22, 30),
        "Average": (13, 21),
        "Poor": (0, 12),
    },
    "50-59": {
        "Excellent": (33, float("inf")),
        "Very good": (25, 32),
        "Good": (17, 24),
        "Average": (9, 16),
        "Poor": (0, 8),
    },
    "60+": {
        "Excellent": (28, float("inf")),
        "Very good": (21, 27),
        "Good": (13, 20),
        "Average": (5, 12),
        "Poor": (0, 4),
    },
}


def get_age_group(age: int) -> str:
    """Determine the age group based on the given age."""
    return next(
        (group for min_age, max_age, group in AGE_GROUPS if min_age <= age <= max_age),
        "Unknown",
    )


def get_pushup_rating(age: int, pushup_count: int) -> str:
    """Returns the push-up performance rating based on age and count."""
    age_group = get_age_group(age)  # Get the correct age group
    if not age_group:
        raise ValueError("Invalid age")

    return next(
        (
            rating
            for rating, (min_count, max_count) in RATINGS[age_group].items()
            if min_count <= pushup_count <= max_count
        ),
        "Unknown rating",
    )


def get_rating(user_id: int) -> Tuple[str, str]:
    """Returns the overall performance rating based on age and push-up count."""
    p = get_profile(user_id)
    army_min, _ = get_army_pushup_range(p.age)
    if p.max_set >= army_min:
        army_rating = "You are fit!"
    else:
        army_rating = "You better hit the ground and train harder, soldier!"
    civil_rating = get_pushup_rating(age=p.age, pushup_count=p.max_set).lower()
    return army_rating, civil_rating
