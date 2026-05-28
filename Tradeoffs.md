```md
# TRADEOFFS.md — Known Tradeoffs

## 1. No User Authentication

The prototype does not include login, roles, or JWT authentication.

I skipped this because the main focus was building the ingestion pipeline and emissions workflow within limited time. Adding authentication would take extra time without improving the core product logic.

The system is already structured so authentication can be added later with minimal changes.

**Current limitation:**  
Anyone can approve or flag records, and there is no tracking of which user performed an action.

---

## 2. Limited Unit Conversion

The parser currently supports common units like `L` and `KG`.

Real SAP exports can contain many different unit formats such as gallons or cubic metres. A complete conversion system would require a larger mapping layer and database support.

I kept the implementation simple to focus on the ingestion flow and emissions calculation logic.

**Current limitation:**  
Some uncommon units may produce incorrect emission values.

---

## 3. No PDF Utility Bill Parsing

The system currently accepts CSV uploads instead of PDF bills.

PDF parsing was intentionally skipped because utility bill layouts vary heavily across providers, making reliable extraction difficult and time-consuming for a prototype.

Most utility portals already provide CSV or Excel exports, so using CSV is still realistic for real-world workflows.

**Current limitation:**  
Clients with only PDF bills would need manual data entry or CSV conversion before upload.
```
