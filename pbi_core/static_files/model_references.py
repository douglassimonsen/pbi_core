from pydantic import BaseModel


class ModelColumnReference(BaseModel):
    column: str
    table: str

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ModelColumnReference):
            return False
        return (self.column == other.column) and (self.table == other.table)

    def __hash__(self) -> int:
        return hash((self.column, self.table))


class ModelTableReference(BaseModel):
    table: str

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ModelTableReference):
            return False
        return self.table == other.table

    def __hash__(self) -> int:
        return hash(self.table)


class ModelMeasureReference(BaseModel):
    measure: str
    table: str

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ModelMeasureReference):
            return False
        return (self.measure == other.measure) and (self.table == other.table)

    def __hash__(self) -> int:
        return hash((self.measure, self.table))
