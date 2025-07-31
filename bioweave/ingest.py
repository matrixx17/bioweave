
import os, uuid, datetime, logging, yaml
import pandas as pd

from .models import SessionLocal, Upload
from .schema_def import AssaySchema, QikPropSchema
from .benchling_client import push_to_benchling

MAPPING_PATH = os.path.join(os.path.dirname(__file__), "mapping.yml")

def load_mapping():
    with open(MAPPING_PATH, "r") as fh:
        raw = yaml.safe_load(fh)
    # flatten list of single‑item dicts into one dict
    mapping = {}
    for pair in raw:
        mapping.update(pair)
    return mapping

ALIAS_MAP = load_mapping()
CANONICAL_FIELDS = ["USUBJID", "VISIT", "ANALYTE", "CONC", "UNIT"]

def _standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns=lambda c: ALIAS_MAP.get(c.strip(), c.strip()))
    return df

# def _clean(df: pd.DataFrame) -> pd.DataFrame:
#     df = _standardize_columns(df)
#     # Keep canonical fields that are present
#     keep_cols = [c for c in CANONICAL_FIELDS if c in df.columns]
#     df = df[keep_cols]
#     AssaySchema.validate(df, lazy=True)
#     return df

def _clean(df: pd.DataFrame) -> pd.DataFrame:
    df = _standardize_columns(df)

    # Decide schema based on available fields
    if set(["ACxDNA^5/SA", "QPPCaco", "QPlogPo/w"]).issubset(df.columns):
        QikPropSchema.validate(df, lazy=True)
    else:
        AssaySchema.validate(df, lazy=True)

    return df

def handle_upload(file_path: str, out_dir: str = "processed") -> Upload:
    os.makedirs(out_dir, exist_ok=True)
    ext = os.path.splitext(file_path)[1].lower()
    if ext in (".xlsx", ".xls"):
        df = pd.read_excel(file_path)
    elif ext == ".csv":
        df = pd.read_csv(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    df_clean = _clean(df)
    out_file = os.path.join(out_dir, f"{uuid.uuid4()}.csv")
    df_clean.to_csv(out_file, index=False)

    # Push to Benchling (optional)
    pushed = push_to_benchling(out_file)

    # Persist metadata
    session = SessionLocal()
    upload = Upload(
        filename=os.path.basename(file_path),
        status="complete" if pushed else "stored",
        dataset_path=out_file,
        report={
            "rows": len(df_clean),
            "pushed_to_benchling": pushed,
            "generated_at": datetime.datetime.utcnow().isoformat(),
        },
    )
    session.add(upload)
    session.commit()
    session.refresh(upload)
    session.close()

    logging.info("Ingested %s rows from %s", len(df_clean), file_path)
    return upload
