````md id="xqk812"
# SOURCES.md — Data Source Research

---

# 1. SAP Data (Fuel & Procurement)

## What I Researched

SAP data is commonly exported as CSV files using SE16 or custom reports. These exports usually contain:
- plant code
- material name
- quantity
- unit
- posting date

I chose CSV exports because they are the most practical and commonly used format during client onboarding.

More advanced SAP integrations like IDoc or OData were avoided since they require additional setup, middleware, and IT support.

---

## Sample Data

```csv
plant_code,material,quantity,unit,date
PL01,Diesel,5000,L,2024-01-15
PL02,Petrol,3200,L,2024-02-01
PL01,Diesel,150000,L,2024-03-10
````

The values are realistic for industrial fuel usage.
The large 150,000L entry was intentionally added to test anomaly detection.

---

## Real-World Limitations

* Some SAP systems use German column names like `Menge` instead of `quantity`
* Unsupported units like `GAL` or `M3` may produce incorrect calculations
* Plant codes need a lookup table to map them to actual facilities
* Different date formats may require preprocessing

---

# 2. Utility Data (Electricity)

## What I Researched

Utility companies usually provide electricity usage data through:

* PDF bills
* CSV/Excel exports
* customer portals

CSV exports are the easiest and most consistent format across providers.

Typical exports include:

* meter ID
* billing period
* electricity usage (kWh)
* tariff type

---

## Sample Data

```csv
meter_id,billing_period,kwh,tariff
METER001,Jan-2024,15000,standard
METER002,Feb-2024,22000,standard
METER003,Mar-2024,8500,off-peak
```

The numbers represent realistic electricity consumption for medium-sized commercial buildings.

---

## Real-World Limitations

* Billing periods may overlap across months
* Large clients may have dozens of meters
* Some utility exports include non-energy charges that should not count toward emissions
* Grid emission factors vary across regions

---

# 3. Corporate Travel Data

## What I Researched

Corporate travel tools like Concur and Navan usually export trip data as CSV files.

Typical fields include:

* origin
* destination
* travel mode
* traveler name
* travel date

Distance is often missing and normally needs to be calculated separately using airport or city coordinates.

---

## Sample Data

```csv
origin,destination,distance_km,mode,traveler
DEL,LHR,6700,flight,Amit Shah
BOM,DXB,1930,flight,Priya Nair
DEL,MUM,1400,train,Rahul Gupta
```

The travel distances are realistic and were pre-calculated for simplicity.

---

## Real-World Limitations

* Some exports may not include distances
* Long-haul and short-haul flights should use different emission factors
* Business-class flights produce higher emissions but are not handled separately
* Hotel stay emissions are not included in the current model

```
```
