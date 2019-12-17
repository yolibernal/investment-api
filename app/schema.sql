DROP TABLE IF EXISTS company;
DROP TABLE IF EXISTS investor;
DROP TABLE IF EXISTS investment_round;
DROP TABLE IF EXISTS investment;

CREATE TABLE company (
  name TEXT NOT NULL,
  city TEXT NOT NULL,
  PRIMARY KEY (name, city)
);

CREATE TABLE investor (
  name TEXT NOT NULL,
  city TEXT NOT NULL,
  PRIMARY KEY (name, city)
);

CREATE TABLE investment_round (
  id TEXT PRIMARY KEY,
  company TEXT REFERENCES company(name),
  investment_stage CHECK( investment_stage IN ('Seed', 'Seed+', 'Series A', 'Series B', 'Series C') ) NOT NULL,
  round_size REAL NOT NULL,
  date TEXT NOT NULL
);

CREATE TABLE investment (
  investment_round_id TEXT REFERENCES investment_round(id),
  investor TEXT REFERENCES investor(name)
);
