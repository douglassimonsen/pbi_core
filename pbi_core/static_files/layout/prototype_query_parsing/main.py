from typing import TYPE_CHECKING

import jinja2

from ..condition import Condition, Expression, QueryConditionType

if TYPE_CHECKING:
    from ..filters import From, PrototypeQuery

test = {
    "Version": 2,
    "From": [{"Entity": "DataTable", "Name": "k", "Type": 0}, {"Entity": "Table", "Name": "t", "Type": 0}],
    "Select": [
        {
            "Column": {"Expression": {"SourceRef": {"Source": "k"}}, "Property": "a"},
            "Name": "DataTable.a",
            "NativeReferenceName": "a",
        },
        {
            "Aggregation": {
                "Expression": {"Column": {"Expression": {"SourceRef": {"Source": "t"}}, "Property": "a"}},
                "Function": 5,
            },
            "Name": "CountNonNull(Table.a)",
            "NativeReferenceName": "Count of a",
        },
        {"Measure": {"Expression": {"SourceRef": {"Source": "k"}}, "Property": "title"}, "Name": "DataTable.title"},
    ],
    "Where": [
        {
            "Condition": {
                "Comparison": {
                    "ComparisonKind": 0,
                    "Left": {
                        "Aggregation": {
                            "Expression": {"Column": {"Expression": {"SourceRef": {"Source": "k"}}, "Property": "b"}},
                            "Function": 0,
                        }
                    },
                    "Right": {"Literal": {"Value": "1L"}},
                }
            },
            "Target": [{"Column": {"Expression": {"SourceRef": {"Source": "k"}}, "Property": "a"}}],
        },
        {
            "Condition": {
                "In": {
                    "Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "k"}}, "Property": "a"}}],
                    "Values": [[{"Literal": {"Value": "3L"}}]],
                }
            }
        },
        {
            "Condition": {
                "Not": {
                    "Expression": {
                        "In": {
                            "Expressions": [
                                {"Column": {"Expression": {"SourceRef": {"Source": "k"}}, "Property": "a"}}
                            ],
                            "Values": [[{"Literal": {"Value": "3L"}}]],
                        }
                    }
                }
            }
        },
        {
            "Condition": {
                "Contains": {
                    "Left": {"Column": {"Expression": {"SourceRef": {"Source": "t"}}, "Property": "a"}},
                    "Right": {"Literal": {"Value": "'A'"}},
                }
            }
        },
        {
            "Condition": {
                "Not": {
                    "Expression": {
                        "Contains": {
                            "Left": {"Column": {"Expression": {"SourceRef": {"Source": "t"}}, "Property": "a"}},
                            "Right": {"Literal": {"Value": "'A'"}},
                        }
                    }
                }
            }
        },
        {
            "Condition": {
                "Comparison": {
                    "ComparisonKind": 1,
                    "Left": {"Column": {"Expression": {"SourceRef": {"Source": "k"}}, "Property": "a"}},
                    "Right": {"Literal": {"Value": "1L"}},
                }
            }
        },
        {
            "Condition": {
                "And": {
                    "Left": {
                        "Comparison": {
                            "ComparisonKind": 3,
                            "Left": {"Column": {"Expression": {"SourceRef": {"Source": "k"}}, "Property": "a"}},
                            "Right": {"Literal": {"Value": "2L"}},
                        }
                    },
                    "Right": {
                        "Comparison": {
                            "ComparisonKind": 3,
                            "Left": {"Column": {"Expression": {"SourceRef": {"Source": "k"}}, "Property": "a"}},
                            "Right": {"Literal": {"Value": "1L"}},
                        }
                    },
                }
            }
        },
        {
            "Condition": {
                "Not": {
                    "Expression": {
                        "Comparison": {
                            "ComparisonKind": 0,
                            "Left": {"Column": {"Expression": {"SourceRef": {"Source": "k"}}, "Property": "a"}},
                            "Right": {"Literal": {"Value": "null"}},
                        }
                    }
                }
            }
        },
        {
            "Condition": {
                "Or": {
                    "Left": {
                        "Comparison": {
                            "ComparisonKind": 0,
                            "Left": {"Column": {"Expression": {"SourceRef": {"Source": "k"}}, "Property": "a"}},
                            "Right": {"Literal": {"Value": "1L"}},
                        }
                    },
                    "Right": {
                        "Not": {
                            "Expression": {
                                "Comparison": {
                                    "ComparisonKind": 0,
                                    "Left": {"Column": {"Expression": {"SourceRef": {"Source": "k"}}, "Property": "a"}},
                                    "Right": {"Literal": {"Value": "1L"}},
                                }
                            }
                        }
                    },
                }
            }
        },
    ],
}


DAX_TEMPLATE = jinja2.Template("""
// DAX Query
DEFINE
  {{table_definitions}}
{{order_by}}
""")


def generate_filter_table(group_name: str, filters: list[Condition], tables: dict[str, "From"]):
    filter_info: list[Expression] = []
    for f in filters:
        x = f.to_query_text(tables)
        if isinstance(x, tuple):
            filter_info.extend(x)
        else:
            filter_info.append(x)
    for x in filter_info:
        print(x.to_text())
    exit()
    return """
VAR __DS0FilterTable =
    FILTER
"""


def generate_filters(filters: list["Condition"], tables: dict[str, "From"]):
    filter_types: dict[QueryConditionType, list[Condition]] = {e: [] for e in QueryConditionType}
    for f in filters:
        filter_types[f.get_prototype_query_type()].append(f)
    for i, (filter_group, filters) in enumerate(filter_types.items()):
        generate_filter_table(filter_group, filters, tables)


def parse_prototype_query(prototype_query: "PrototypeQuery"):
    assert prototype_query.Where is not None
    assert all(table.Name is not None for table in prototype_query.From)
    table_mapping: dict[str, From] = {table.Name: table for table in prototype_query.From}

    generate_filters(prototype_query.Where, table_mapping)
