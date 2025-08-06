from pbi_core.ssas.server.tabular_model import SsasTable


class RelatedColumnDetail(SsasTable):
    @classmethod
    def _db_type_name(cls) -> str:
        return "RelatedColumnDetails"
