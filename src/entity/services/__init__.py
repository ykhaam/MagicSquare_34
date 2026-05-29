"""Entity services for magic-square logic."""

from entity.services.blank_locator import find_blank_coords
from entity.services.magic_validator import is_magic_square
from entity.services.missing_number_finder import find_not_exist_nums

__all__ = ["find_blank_coords", "find_not_exist_nums", "is_magic_square"]
