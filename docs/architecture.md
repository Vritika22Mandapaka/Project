# Architecture: SmartSupply AI Platform

## 1. Data Layer

### Structured Tables

- `sales_orders` (order_date, sku_id, qty, channel, region)
- `inventory_levels` (sku_id, warehouse_id, on_hand, safety_stock)
- `supplier_lead_times` (supplier_id, sku_id, avg_days, reliability)
- `delivery_events` (shipment_id, promised_date, delivered_date, delay_reason)
- `manufacturing_capacity` (plant_id, line_id, shift_date, available_hours)

### Document Corpus for RAG

- SOPs (production, procurement, returns)
- Supplier contracts / SLAs
- Product specs and BOM notes
- Incident and quality reports

## 2. AI Components

### A) Forecast Model

Input: historical sales + promotions + seasonality + macro events

Output: `demand_forecast(sku, location, week, prediction, confidence_interval)`

### B) Procurement Optimizer

Uses forecast + lead times + safety stock + MOQ to recommend:

- reorder point
- order quantity
- supplier ranking

### C) Delivery Prioritizer

Uses shipment risk score (weather, route delay history, carrier performance).

### D) Manufacturing Planner

Maps demand into production slots considering:

- machine/line capacity
- changeover costs
- labor shifts
- material availability

### E) RAG Q&A

1. Chunk and embed operational docs
2. Retrieve top-k chunks
3. LLM generates grounded answer with citations

## 3. Multi-Agent Workflow

1. `SalesForecastAgent` predicts demand
2. `ProcurementAgent` proposes purchase plan
3. `ManufacturingAgent` builds production schedule
4. `DeliveryAgent` prioritizes shipments
5. `SupervisorAgent` enforces rules and asks for human approval on high-risk actions

## 4. Guardrails

- Rule-based checks for budget, capacity, and compliance
- Confidence thresholds before auto-action
- Human approval for critical procurement and production changes
- Prompt injection and data leakage protections

## 5. Evaluation

- Forecasting: MAPE, WAPE, bias by SKU class
- RAG: retrieval precision@k, groundedness, answer correctness
- Agent workflow: task success rate, override rate, cycle time
- Business outcomes: stockouts, OTIF, inventory turns

## 6. Deployment Pattern

- FastAPI microservice for inference and orchestration
- Batch jobs for nightly forecasting + weekly planning
- Event-driven updates for urgent disruptions (supplier delay, machine failure)
