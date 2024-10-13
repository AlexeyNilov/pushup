""" Fitness tests/standards collection"""

from typing import Tuple


AGE_GROUPS = [
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


def get_pushup_range(age: int) -> Tuple[int, int]:
    """U.S. Army Standards, push-ups are performed within a two-minute period"""

    if age < 17:
        raise ValueError("Age must be at least 17")

    # Determine the age group based on the age
    for min_age, max_age, age_group in AGE_GROUPS:
        if min_age <= age <= max_age:
            return US_ARMY_AGE_RANGE[age_group]

    raise ValueError("Age group not found")  # Fallback, should not reach here
