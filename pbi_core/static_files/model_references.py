from pbi_core.pydantic.main import BaseValidation


class ModelColumnReference(BaseValidation):
    column: str
    table: str

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ModelColumnReference):
            return False
        return (self.column == other.column) and (self.table == other.table)

    def __hash__(self) -> int:
        return hash((self.column, self.table))


class ModelTableReference(BaseValidation):
    table: str

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ModelTableReference):
            return False
        return self.table == other.table

    def __hash__(self) -> int:
        return hash(self.table)


class ModelMeasureReference(BaseValidation):
    measure: str
    table: str

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ModelMeasureReference):
            return False
        return (self.measure == other.measure) and (self.table == other.table)

    def __hash__(self) -> int:
        return hash((self.measure, self.table))
