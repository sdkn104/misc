import argparse
import configparser
import os
import re
from pathlib import Path
from typing import Dict

import mysql.connector
import pandas as pd
import numpy as np


def sanitize_col(name: str) -> str:
    name = name.strip()
    name = re.sub(r"\s+", "_", name)
    name = re.sub(r"[^0-9A-Za-z_]+", "", name)
    if name == "":
        name = "col"
    return name


def dtype_to_sql(dtype) -> str:
    if pd.api.types.is_integer_dtype(dtype):
        return "BIGINT"
    if pd.api.types.is_float_dtype(dtype):
        return "DOUBLE"
    if pd.api.types.is_bool_dtype(dtype):
        return "TINYINT(1)"
    if pd.api.types.is_datetime64_any_dtype(dtype):
        return "DATETIME"
    return "TEXT"


def create_table(cursor, table_name: str, df: pd.DataFrame):
    cols = []
    for col in df.columns:
        colname = sanitize_col(col)
        sqltype = dtype_to_sql(df[col].dtype)
        cols.append(f"`{colname}` {sqltype}")
    cols_sql = ", ".join(cols)
    sql = f"CREATE TABLE IF NOT EXISTS `{table_name}` ({cols_sql}) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
    cursor.execute(sql)


def insert_dataframe(cursor, table_name: str, df: pd.DataFrame, batch: int = 500):
    cols = [sanitize_col(c) for c in df.columns]
    placeholders = ",".join(["%s"] * len(cols))
    col_list = ",".join([f"`{c}`" for c in cols])
    sql = f"INSERT INTO `{table_name}` ({col_list}) VALUES ({placeholders})"

    def _convert_value(v):
        # convert pandas / numpy NA to Python None, and numpy scalar types to native Python types
        if pd.isna(v):
            return None
        if isinstance(v, (np.integer,)):
            return int(v)
        if isinstance(v, (np.floating,)):
            return float(v)
        if isinstance(v, (np.bool_,)):
            return bool(v)
        if isinstance(v, (np.datetime64, pd.Timestamp)):
            try:
                return pd.to_datetime(v).to_pydatetime()
            except Exception:
                return str(v)
        return v

    records = df.values.tolist()
    converted_records = [tuple(_convert_value(v) for v in row) for row in records]
    for i in range(0, len(converted_records), batch):
        batch_records = converted_records[i : i + batch]
        cursor.executemany(sql, batch_records)


def process_file(conn, filepath: Path, table_prefix: str = ""):
    print(f"Processing: {filepath}")
    df = pd.read_csv(filepath)
    table_name = table_prefix + sanitize_col(filepath.stem)
    with conn.cursor() as cursor:
        create_table(cursor, table_name, df)
        if not df.empty:
            insert_dataframe(cursor, table_name, df)
    conn.commit()
    print(f"Finished: {filepath} -> table `{table_name}`")


def main():
    parser = argparse.ArgumentParser(description="Load CSVs into MySQL database")
    parser.add_argument("--config", default="config.ini", help="path to config file")
    parser.add_argument("--folder", default="store-sales-time-series-forecasting", help="folder with CSV files")
    args = parser.parse_args()

    cfg = configparser.ConfigParser()
    if not os.path.exists(args.config):
        raise SystemExit(f"Config file not found: {args.config}")
    cfg.read(args.config)

    if "mysql" not in cfg:
        raise SystemExit("[mysql] section missing in config file")

    db = cfg["mysql"]
    conn = mysql.connector.connect(
        host=db.get("host", "127.0.0.1"),
        port=int(db.get("port", 3306)),
        user=db.get("user"),
        password=db.get("password"),
        database=db.get("database"),
        charset=db.get("charset", "utf8mb4"),
        autocommit=False,
    )

    folder = Path(args.folder)
    if not folder.exists():
        raise SystemExit(f"CSV folder not found: {folder}")

    csv_files = sorted(folder.glob("*.csv"))
    if not csv_files:
        print("No CSV files found in folder.")
        return

    for f in csv_files:
        process_file(conn, f, table_prefix=db.get("table_prefix", ""))

    conn.close()


if __name__ == "__main__":
    main()
