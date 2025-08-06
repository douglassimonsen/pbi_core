class QueryDefinition:
    query: str

    def __init__(self, query: str) -> None:
        self.query = query

    def add_statement(self, statement: str) -> None:
        breakpoint()

    def __str__(self) -> str:
        return self.query
