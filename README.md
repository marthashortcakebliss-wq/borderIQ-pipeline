# BorderIQ

Trade intelligence pipeline for East African corridors — customs tariff calculation, freight rate comparison, and disruption tracking.

## What this does

Pulls real East African Community Gazette data (tariff decisions, customs duty rates) and runs it through a working pipeline: extract → transform → load → Postgres. Includes a calculator that computes landed shipment cost (duty + VAT + excise) from real, currently-in-force tariff rates.

## Proven working

Parsed 15 real, currently-in-force tariff decisions directly from a published EAC Gazette legal notice, then ran them through the landed cost calculator — e.g. an $8,000 mobile phone shipment into Uganda lands at $8,800 under the real 10% rate Uganda currently applies.
