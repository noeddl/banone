from pathlib import Path

import yaml


def load_test_data(keys):
    """Load test data from a YAML file."""
    data = []
    with Path("tests/data/de.yaml").open(encoding="utf-8") as f:
        entries = yaml.safe_load(f)
        for compound, doc in entries.items():
            doc["compound"] = compound
            d = [doc.get(k) for k in keys]
            data.append(d)
    return data
