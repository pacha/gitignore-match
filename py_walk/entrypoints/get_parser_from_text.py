from typing import Union
from pathlib import Path

from py_walk.models import Parser
from .get_parser_from_list import get_parser_from_list
from .pattern_text_to_pattern_list import pattern_text_to_pattern_list


def get_parser_from_text(text: str, base_dir: Union[Path, str]) -> Parser:
    """Create a Parser object from a multiline text."""

    # normalize base_dir to Path
    if isinstance(base_dir, str):
        base_dir = Path(base_dir)

    patterns = pattern_text_to_pattern_list(text)
    return get_parser_from_list(patterns, base_dir=base_dir)
