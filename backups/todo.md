# Missing Features vs Industry Standard — Implementation Plan

## Inventory Management

- [x] **Low-stock alerts / Reorder points** — `min_stock` field on Product; POS low-stock badge; product form fields
- [x] **Purchase Order management** — Create PO → receive against PO → auto-update stock; track ordered, received, pending quantities
- [x] **Vendor/Supplier management** — CRUD for suppliers; link products to vendors; vendor purchase history
- [x] **Stock adjustments with reason codes** — Log stock changes (damage, theft, count correction, write-off) with reason; audit trail
- [ ] **Inventory forecasting** — Basic reorder suggestions based on historical sales velocity
- [x] **Physical inventory counts** — Count sheet generation; count entry; variance reporting
- [ ] **Multi-location inventory** — Warehouse/store concept; separate stock per location
- [ ] **Stock transfers** — Move inventory between locations with workflow
- [ ] **Per-variant inventory** — Track stock per color+size SKU combination instead of product level
- [x] **Cost of goods / Margin tracking** — Track purchase cost; calculate COGS and margin per product/report
- [x] **Inventory valuation report** — Report stock value at cost and at retail
- [x] **Barcode label printing** — Generate & print barcode labels from product list
- [x] **Kit/Bundle management** — Define bundle products that sum component stock

## POS Transactions

- [x] **Discount at POS** — Per-transaction % or $ discount with reason code
- [x] **Order notes on POS** — Text memo field attached to transaction
- [ ] **Split tender** — Pay with multiple payment methods per transaction
- [ ] **Suspend / Recall transaction** — Park an order and resume later
- [ ] **Quick keys / Speed buttons** — Assign products to grid buttons for one-tap add
- [ ] **Gift cards** — Issue gift cards; redeem at POS
- [ ] **Loyalty points** — Earn points per purchase; redeem at POS
- [ ] **Offline mode** — Process sales during internet outage; sync when online
- [x] **Return with receipt lookup** — Look up original sale by receipt number or barcode

## Reporting & Analytics

- [x] **Sales reports** — Filterable: by product, category, cashier, date range; exportable
- [x] **End-of-day close / Shift management** — Shift model; expected vs actual cash; variance logging; closing entry
- [x] **Margin reports** — Profit margin per product, category, and overall
- [x] **Inventory aging** — Slow movers, dead stock, stock turnover rate
- [ ] **Tax summary report** — Sales tax collected by rate
- [ ] **Cashier performance** — Per-cashier sales totals, transaction count, void rate

## Customer Management

- [x] **Customer lifetime value** — CLV metric; total spend, order count, avg order value
- [x] **Customer groups/tiers** — Wholesale, VIP, etc. with custom pricing
- [ ] **Marketing automation** — Email/SMS based on purchase behavior or inactivity
