from typing import Dict, List

class ColorNotFoundException(Exception):
    """Raise when color wasn't found, just in case"""
    pass

def find_color_name(color_value: str, color_type: str, data: List[Dict[str, str]]) -> str:
    # O(N*M) - complexity N - main loop M - lowercasing of strings
    for i in data:
        if i[color_type].lower() == color_value:
            return i["name"]
    raise ColorNotFoundException
