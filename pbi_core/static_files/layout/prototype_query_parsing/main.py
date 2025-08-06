from typing import TYPE_CHECKING

import jinja2

from ..condition import Condition, Expression, QueryConditionType

if TYPE_CHECKING:
    from ..filters import From, PrototypeQuery


DAX_TEMPLATE = jinja2.Template("""
// DAX Query
DEFINE
{%- for simple_filter in simple_filters %}
{{simple_filter}}
{%- endfor %} 
""")

BASIC_FILTER_TEMPLATE = jinja2.Template("""
    VAR __DS0FilterTable{{index}} =
        FILTER(
            KEEPFILTERS(VALUES({{source}})),
            {{filters}}
        )
""")


def generate_simple_filter_tables(filters: list[Condition], tables: dict[str, "From"]) -> list[str]:
    filter_info: dict[str, list[Expression]] = {}
    for f in filters:
        x = f.to_query_text(tables)
        if not isinstance(x, tuple):
            x = (x,)
        for y in x:
            filter_info.setdefault(y.source, []).append(y)

    ret: list[str] = []
    for i, (field, processed_filters) in enumerate(filter_info.items()):
        filter_str = processed_filters.pop(0).to_text()
        for f in processed_filters:
            filter_str = f"AND({filter_str}, {f.to_text()})"

        ret.append(
            BASIC_FILTER_TEMPLATE.render(
                index=str(i + 1) if i > 0 else "",
                source=field,
                filters=filter_str,
            )
        )
        return ret


def generate_filters(filters: list["Condition"], tables: dict[str, "From"]):
    filter_types: dict[QueryConditionType, list[Condition]] = {e: [] for e in QueryConditionType}
    for f in filters:
        filter_types[f.get_prototype_query_type()].append(f)
    simple_filter_tables = generate_simple_filter_tables(filter_types[QueryConditionType.STANDARD], tables)
    ret = DAX_TEMPLATE.render(simple_filters=simple_filter_tables)
    print(ret)
    exit()


def parse_prototype_query(prototype_query: "PrototypeQuery"):
    assert prototype_query.Where is not None
    assert all(table.Name is not None for table in prototype_query.From)
    table_mapping: dict[str, From] = {table.Name: table for table in prototype_query.From}

    generate_filters(prototype_query.Where, table_mapping)
