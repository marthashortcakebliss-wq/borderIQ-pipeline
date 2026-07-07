CREATE TABLE IF NOT EXISTS countries (
    country_code CHAR(2) PRIMARY KEY,
    country_name VARCHAR(100) NOT NULL,
    region VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS hs_codes (
    hs_code VARCHAR(10) PRIMARY KEY,
    description TEXT NOT NULL,
    category VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS tariffs (
    tariff_id SERIAL PRIMARY KEY,
    hs_code VARCHAR(10) REFERENCES hs_codes(hs_code),
    origin_country CHAR(2) REFERENCES countries(country_code),
    destination_country CHAR(2) REFERENCES countries(country_code),
    duty_rate NUMERIC(6,3) NOT NULL,
    vat_rate NUMERIC(6,3),
    excise_rate NUMERIC(6,3),
    effective_date DATE NOT NULL,
    source VARCHAR(100),
    ingested_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS freight_routes (
    route_id SERIAL PRIMARY KEY,
    origin_port VARCHAR(100) NOT NULL,
    destination_city VARCHAR(100) NOT NULL,
    mode VARCHAR(20) NOT NULL,
    distance_km NUMERIC(8,2)
);

CREATE TABLE IF NOT EXISTS freight_rates (
    rate_id SERIAL PRIMARY KEY,
    route_id INT REFERENCES freight_routes(route_id),
    carrier VARCHAR(100),
    rate_usd_per_ton NUMERIC(10,2) NOT NULL,
    transit_days NUMERIC(4,1),
    quote_date DATE NOT NULL,
    source VARCHAR(100),
    ingested_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS disruption_events (
    event_id SERIAL PRIMARY KEY,
    corridor VARCHAR(150) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20),
    description TEXT,
    reported_date DATE NOT NULL,
    resolved_date DATE,
    source VARCHAR(100),
    ingested_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_tariffs_lookup ON tariffs(hs_code, origin_country, destination_country);
CREATE INDEX IF NOT EXISTS idx_freight_route ON freight_rates(route_id, quote_date);
CREATE INDEX IF NOT EXISTS idx_disruption_corridor ON disruption_events(corridor, reported_date);
