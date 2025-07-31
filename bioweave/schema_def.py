
import pandera as pa
from pandera.typing import Series

class AssaySchema(pa.SchemaModel):
    USUBJID: Series[str]
    VISIT: Series[str]  # or int, but str covers both
    ANALYTE: Series[str]
    CONC: Series[float]
    UNIT: Series[str]

    class Config:
        coerce = True

class QikPropSchema(pa.SchemaModel):
    ACDxDNAS: Series[float]
    CIQlogS: Series[float]
    PSA: Series[float]
    QPPCaco: Series[float]
    QPPMDCK: Series[float]
    QPlogPo_w: Series[float]

    class Config:
        coerce = True
