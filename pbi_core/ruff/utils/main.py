from typing import Any

from ...static_files.layout.condition import Expression

MAX_FONTS = 2


def get_config_values(config: Any) -> dict[tuple[str, str], Expression]:
    if config is None:
        return {}

    ret = {}
    for category in config.model_fields:
        category_data = getattr(config, category)
        if category_data is None:
            continue

        for field in category_data[0].properties.model_fields:
            field_data = getattr(category_data[0].properties, field)
            ret[category, field] = field_data
    return ret
