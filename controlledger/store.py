from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict
from pathlib import Path

from .models import Evidence, UseCase


class Registry:
    def __init__(self, path: str | Path = ":memory:"):
        self.db = sqlite3.connect(str(path))
        self.db.execute("CREATE TABLE IF NOT EXISTS systems(system_id TEXT, version INTEGER, payload TEXT, PRIMARY KEY(system_id,version))")
        self.db.execute("CREATE TABLE IF NOT EXISTS evidence(system_id TEXT, control_id TEXT, payload TEXT, PRIMARY KEY(system_id,control_id))")

    def save_system(self, system: UseCase) -> None:
        self.db.execute("INSERT INTO systems VALUES(?,?,?)", (system.system_id, system.version, json.dumps(asdict(system), sort_keys=True)))
        self.db.commit()

    def systems(self) -> list[UseCase]:
        rows = self.db.execute("SELECT payload FROM systems ORDER BY system_id,version").fetchall()
        return [UseCase(**{**(data := json.loads(row[0])), "users": tuple(data["users"]), "data_categories": tuple(data["data_categories"])}) for row in rows]

    def save_evidence(self, item: Evidence) -> None:
        self.db.execute("INSERT OR REPLACE INTO evidence VALUES(?,?,?)", (item.system_id, item.control_id, json.dumps(asdict(item), sort_keys=True)))
        self.db.commit()

    def evidence(self, system_id: str) -> list[Evidence]:
        return [Evidence(**json.loads(row[0])) for row in self.db.execute("SELECT payload FROM evidence WHERE system_id=?", (system_id,))]
