class QueryDefinition:
    query: str
    """The raw string of the query definition, which is an M query."""

    def __init__(self, query: str) -> None:
        self.query = query

    def add_statement(self, statement: str) -> None:
        print(statement, self.query)
        breakpoint()

    def __str__(self) -> str:
        return self.query
