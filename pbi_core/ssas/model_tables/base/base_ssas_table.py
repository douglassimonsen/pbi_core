from structlog import get_logger

from pbi_core.attrs import define
from pbi_core.ssas.model_tables._group import IdBase

from .helpers import HelperMixin
from .lineage import LineageMixin
from .ssas import SsasMixin
from .tabular import TabularMixin

logger = get_logger()


@define()
class SsasTable(IdBase, TabularMixin, HelperMixin, SsasMixin, LineageMixin):
    pass
