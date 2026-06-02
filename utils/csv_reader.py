
import csv
import os
from config.logger import logger


def read_csv(filename: str) -> list:
    filepath = os.path.join("test_data", filename)

    if not os.path.exists(filepath):
        logger.error(f"קובץ לא נמצא: {filepath}")
        return []

    data = []
    with open(filepath, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(dict(row))

    logger.info(f"נטענו {len(data)} שורות מ־{filename}")
    return data


def get_parametrize_data(filename: str, *keys) -> list:
    rows = read_csv(filename)
    result = []

    for row in rows:
        values = tuple(row[key] for key in keys)
        result.append(values)

    return result