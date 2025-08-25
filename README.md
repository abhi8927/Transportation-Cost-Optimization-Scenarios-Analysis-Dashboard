# 🚛 Transportation Cost Analysis Dashboard – Supply Chain Optimization

This project delivers an **end-to-end interactive Power BI dashboard** designed to analyze and optimize **transportation costs**, **carrier performance**, and **logistics scenarios**. The dashboard enables businesses to monitor KPIs, assess performance by carriers and routes, and perform **What-If analysis** for cost-saving opportunities.

---

## 🎯 Project Objectives

- Track **transportation costs and shipment KPIs** in real time.
- Analyze **mode-wise and carrier-wise performance** to identify optimization opportunities.
- Simulate cost-saving strategies using **What-If Scenarios** (fuel price impact, carrier adoption, and mode changes).
- Provide actionable insights for **strategic supply chain decisions**.

---

## 🛠 Tools & Skills Used

- **Power BI** – Dashboard development and visualization
- **DAX** – Calculations for KPIs and scenario analysis
- **Power Query (M Language)** – Data cleaning and transformation
- **What-If Analysis** – Scenario planning with dynamic parameters
- **Data Modeling** – Relationships and measures for accurate analysis
- **Interactive Slicers & Filters** – Year, Month, Mode, Carrier, Origin, Destination

---

## 🗂 Dataset Overview

The dataset includes detailed transportation and logistics information:

- **Shipment details** (Shipment ID, Origin, Destination, Mode)
- **Carrier information** (Carrier Name, Mode of Transport)
- **Distance & Weight metrics** (Average Distance, Weight in tons)
- **Cost data** (Cost per Ton-Km, Total Shipment Cost)
- **Scenarios & Savings** (Consolidation, Cheapest Carrier adoption, Mode shift)

---

## 📌 Key KPIs Tracked

| KPI                            | Value       |
|--------------------------------|------------|
| Total Shipments               | 4,900      |
| Average Distance (KM)         | 1.40K      |
| Average Cost per Ton-Km       | 3.51       |
| Average Weight (Tons)         | 17.36      |
| Total Shipment Cost           | ₹405.87M   |

---

## 📊 Dashboard Pages & Visuals

### **1️⃣ Overview Page**  
![Overview](images/overview.png)

- Total Shipments & Cost Metrics
- **Cost Share by Mode** (Air, Road, Rail)
- **Shipments by Mode, Origin, and Carrier**
- Interactive filters for **Year, Month, Mode, Carrier**

---

### **2️⃣ Carrier Performance Page**  
![Carrier Performance](images/carrier_performance.png)

- **Total Shipment Cost by Carrier & Mode**
- **Cost per Ton-Km (CPTK) by Carrier**
- **Potential Savings by Carrier**
- **Average Distance by Carrier**

---

### **3️⃣ What-If Scenarios Page**  
![What-If Scenarios](images/what_if_scenarios.png)

- **Baseline vs Scenario vs Consolidation Cost**
- **Scenario Total Cost by Mode & Carrier**
- **Dynamic Parameters**:
    - Fuel Price Change (%)
    - Cheapest Carrier Adoption (%)
    - Air → Rail Mode Shift (%)
- **Consolidation Savings by Route**

---

## 📈 Insights Generated

- **Air Transport** accounts for the largest share of cost (over 50%) despite fewer shipments compared to road.
- **IndianRail and IndigoCargo** are major cost drivers; optimization here can unlock significant savings.
- **What-If Analysis** shows:
    - 0.3% fuel price reduction → significant cost savings.
    - Carrier consolidation & cheapest carrier adoption can save up to **₹30M+**.
- **Ahmedabad & Hyderabad** routes offer maximum savings through consolidation.

---

## 🚀 Key Features Implemented

- ✅ **Dynamic What-If Parameters** for real-time scenario modeling  
- ✅ **Mode-wise and Carrier-wise Performance Analysis**  
- ✅ **Interactive Filters & Drill-through** by Year, Month, Mode, Origin, Destination  
- ✅ Published on **Power BI Service** with secure sharing  

---

## 🗂 Data Files

- **Raw Data:** [shipments_large.csv](data/shipments_large.csv)  
- **Cleaned Data:** [cleaned_shipments.csv](data/cleaned_shipments.csv)  

---


## 🖼 Sample Dashboard Screenshots

- **Overview Page**  
![Overview](images/overview.png)

- **Carrier Performance**  
![Carrier Performance](images/carrier_performance.png)

- **What-If Scenarios**  
![What-If Scenarios](images/what_if_scenarios.png)

---



### ⭐ If you found this helpful, don’t forget to **star the repo**!


