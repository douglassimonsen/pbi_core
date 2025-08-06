from dataclasses import dataclass
from typing import TYPE_CHECKING

import jsondiff

if TYPE_CHECKING:
    from collections.abc import Iterable

    from pbi_core.main import LocalReport
    from pbi_core.ssas.server.tabular_model import SsasTable
    from pbi_core.static_files.layout.layout import Layout


@dataclass
class SsasDifference:
    deleted: list["SsasTable"]
    updated: list[tuple["SsasTable", "SsasTable", list[str]]]
    inserted: list["SsasTable"]

    def __bool__(self) -> bool:
        return len(self.deleted) > 0 or len(self.updated) > 0 or len(self.inserted) > 0


def ssas_diff(
    parent_table: "Iterable[SsasTable]",
    child_table: "Iterable[SsasTable]",
    bad_cols: tuple[str, ...],
) -> SsasDifference:
    parent_items = {obj.id: obj for obj in parent_table}
    child_items = {obj.id: obj for obj in child_table}
    parent_keys = set(parent_items.keys())
    child_keys = set(child_items.keys())
    deleted_items = parent_keys - child_keys
    new_items = child_keys - parent_keys
    same_items = parent_keys & child_keys

    updated: list[tuple[SsasTable, SsasTable, list[str]]] = []
    for key in same_items:
        old_record = parent_items[key]
        new_record = child_items[key]
        old_json = old_record.model_dump(exclude=set(bad_cols))
        new_json = new_record.model_dump(exclude=set(bad_cols))
        affected_fields: list[str] = list(jsondiff.diff(old_json, new_json).keys())
        if affected_fields:
            updated.append((old_record, new_record, affected_fields))

    return SsasDifference(
        deleted=[parent_items[k] for k in deleted_items],
        updated=updated,
        inserted=[child_items[k] for k in new_items],
    )


def layout_diff(parent: "Layout", child: "Layout") -> None:
    print(parent, child)
    breakpoint()


def diff(parent: "LocalReport", child: "LocalReport") -> None:
    x = layout_diff(parent.static_files.layout, child.static_files.layout)
    for ssas_table in parent.ssas.TABULAR_FIELDS():
        x = ssas_diff(
            getattr(parent.ssas, ssas_table),
            getattr(child.ssas, ssas_table),
            ("tabular_model", "modified_time", "refreshed_time"),
        )
        if x:
            print(ssas_table)
            if x.deleted:
                print("\tdeleted")
                for d in x.deleted:
                    print("\t\t", d)
            if x.updated:
                print("\tupdated")
                for a, b, updated_fields in x.updated:
                    old_fields = {k: v for k, v in a.model_dump().items() if k in updated_fields}
                    new_fields = {k: v for k, v in b.model_dump().items() if k in updated_fields}
                    print("\t\t", old_fields)
                    print("\t\t", new_fields, "\n")

            if x.inserted:
                print("\tinserted")
                for d in x.inserted:
                    print("\t\t", d)
