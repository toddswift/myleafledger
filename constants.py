DATABASE_NAME = "cigars.db"

CREATE_QUERY = """ CREATE TABLE IF NOT EXISTS 
    cigar_reviews(
    id            INTEGER PRIMARY KEY,
    brand         TEXT    NOT NULL,                     -- e.g., "Padron"
    line          TEXT,                                 -- e.g., "1964 Anniversary"
    vitola        TEXT,                                 -- e.g., "Toro"
    ring_gauge    INTEGER,                              -- e.g., 50 in mm
    country       TEXT,                                 -- e.g., "Nicaragua"
    wrapper       TEXT,                                 -- optional
    binder        TEXT,                                 -- optional
    filler        TEXT,                                 -- optional

    date_smoked   TEXT    NOT NULL,                     -- ISO 8601: "YYYY-MM-DD"
    rating        INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    notes         TEXT,                                 -- freeform notes
    price_cents   INTEGER,                              -- store money as integer cents
    humidor       TEXT,                                 -- location label
    tags          TEXT,                                 -- CSV, e.g. "maduro,box-press"

    created_at    TEXT    NOT NULL DEFAULT (datetime('now')),
    updated_at    TEXT    NOT NULL DEFAULT (datetime('now'))
    )
    """