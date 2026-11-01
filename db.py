import sqlite3
from pathlib import Path
from app.config import DATABASE_PATH

SCHEMA = '''
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS teams (
 id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS matches (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 provider TEXT, event_number TEXT, ticket_number TEXT,
 match_date TEXT, kickoff_time TEXT,
 home_team_id INTEGER NOT NULL REFERENCES teams(id),
 away_team_id INTEGER NOT NULL REFERENCES teams(id),
 ht_home INTEGER, ht_away INTEGER, ft_home INTEGER, ft_away INTEGER,
 status TEXT NOT NULL DEFAULT 'incomplete',
 source_note TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP,
 CHECK(home_team_id <> away_team_id),
 CHECK(status IN ('complete','incomplete','annulled'))
);
CREATE INDEX IF NOT EXISTS idx_match_pair_date
 ON matches(home_team_id, away_team_id, match_date, kickoff_time);
CREATE TABLE IF NOT EXISTS odds_snapshots (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 match_id INTEGER NOT NULL REFERENCES matches(id),
 market TEXT NOT NULL, selection TEXT NOT NULL,
 odds REAL NOT NULL CHECK(odds > 1.0),
 captured_at TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS predictions (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 match_id INTEGER REFERENCES matches(id), model_version TEXT NOT NULL,
 one_x_two TEXT, main_ht TEXT, main_ft TEXT,
 alternative_ht TEXT, alternative_ft TEXT,
 surprise_ht TEXT, surprise_ft TEXT, confidence TEXT,
 explanation TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS prediction_evaluations (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 prediction_id INTEGER NOT NULL REFERENCES predictions(id),
 actual_ht TEXT, actual_ft TEXT, outcome_1x2 TEXT,
 evaluated_at TEXT DEFAULT CURRENT_TIMESTAMP
);
'''

def init_db():
 Path(DATABASE_PATH).parent.mkdir(parents=True, exist_ok=True)
 with sqlite3.connect(DATABASE_PATH) as con:
  con.executescript(SCHEMA)

def find_exact_order_history(home, away):
 with sqlite3.connect(DATABASE_PATH) as con:
  con.row_factory = sqlite3.Row
  return con.execute('''
   SELECT m.match_date, m.kickoff_time, h.name AS home, a.name AS away,
          m.ht_home, m.ht_away, m.ft_home, m.ft_away, m.event_number
   FROM matches m JOIN teams h ON h.id=m.home_team_id
   JOIN teams a ON a.id=m.away_team_id
   WHERE h.name=? AND a.name=? AND m.status='complete'
   ORDER BY m.match_date, m.kickoff_time
  ''', (home, away)).fetchall()
