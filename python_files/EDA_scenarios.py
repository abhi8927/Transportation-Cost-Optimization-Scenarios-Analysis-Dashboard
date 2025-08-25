import pandas as pd
import matplotlib.pyplot as plt

# -------------------------
# 1. Load dataset
# -------------------------
df = pd.read_csv("cleaned_shipments.csv")

print("Columns available:", df.columns.tolist())

# -------------------------
# 2. Required columns check
# -------------------------
required_cols = ['Origin', 'Destination', 'TotalCost', 'FuelCost', 'Mode', 'Carrier', 'Weight_tons', 'Distance_km']
missing = [col for col in required_cols if col not in df.columns]
if missing:
    raise KeyError(f"Missing columns in dataset: {missing}")

# -------------------------
# SCENARIO 1: Fuel Price Increase (10%)
# -------------------------
fuel_increase = 0.10
df['New_Fuel_Cost'] = df['FuelCost'] * (1 + fuel_increase)
df['Scenario1_TotalCost'] = df['TotalCost'] - df['FuelCost'] + df['New_Fuel_Cost']

# -------------------------
# SCENARIO 2: Shipment Consolidation (90% of combined cost)
# -------------------------
consolidated = df.groupby(['Origin', 'Destination'], as_index=False).agg({
    'TotalCost': 'sum',
    'FuelCost': 'sum',
    'Scenario1_TotalCost': 'sum',
    'Weight_tons': 'sum',
    'Distance_km': 'mean'
})
consolidated['Scenario2_TotalCost'] = consolidated['Scenario1_TotalCost'] * 0.90

# -------------------------
# SCENARIO 3: Mode Shift (10% Air → Rail, Rail 30% cheaper)
# -------------------------
df['Scenario3_TotalCost'] = df['Scenario1_TotalCost']
air_mask = df['Mode'].str.lower() == 'air'
df.loc[air_mask, 'Scenario3_TotalCost'] *= (0.90 + (0.10 * 0.70))

# -------------------------
# SCENARIO 4: Carrier Optimization (70% to cheapest)
# -------------------------
carrier_min = df.groupby(['Origin', 'Destination'])['Scenario3_TotalCost'].transform('min')
df['Scenario4_TotalCost'] = (df['Scenario3_TotalCost'] * 0.30) + (carrier_min * 0.70)

# -------------------------
# 5. Add CPTK (Cost per Ton-Km)
# -------------------------
df['Ton_Km'] = df['Weight_tons'] * df['Distance_km']

df['CPTK_Original'] = df['TotalCost'] / df['Ton_Km']
df['CPTK_Scenario1'] = df['Scenario1_TotalCost'] / df['Ton_Km']
df['CPTK_Scenario3'] = df['Scenario3_TotalCost'] / df['Ton_Km']
df['CPTK_Scenario4'] = df['Scenario4_TotalCost'] / df['Ton_Km']

# -------------------------
# 6. Save outputs as CSV
# -------------------------
df.to_csv("scenario_full_data_with_cptk.csv", index=False)
consolidated.to_csv("scenario2_consolidation.csv", index=False)

# Summary Table
summary = pd.DataFrame({
    'Scenario': ['Original', 'Fuel +10%', 'Consolidation', 'Mode Shift', 'Carrier Optimization'],
    'Total Cost': [
        df['TotalCost'].sum(),
        df['Scenario1_TotalCost'].sum(),
        consolidated['Scenario2_TotalCost'].sum(),
        df['Scenario3_TotalCost'].sum(),
        df['Scenario4_TotalCost'].sum()
    ],
    'Avg CPTK': [
        df['CPTK_Original'].mean(),
        df['CPTK_Scenario1'].mean(),
        consolidated['Scenario2_TotalCost'].sum() / (consolidated['Weight_tons'].sum() * consolidated['Distance_km'].mean()),
        df['CPTK_Scenario3'].mean(),
        df['CPTK_Scenario4'].mean()
    ]
})
summary['Cost Reduction %'] = ((summary['Total Cost'][0] - summary['Total Cost']) / summary['Total Cost'][0]) * 100
summary.to_csv("scenario_summary_with_cptk.csv", index=False)

print("\n✅ All scenario data and summary saved as CSVs.")
print(summary)

# -------------------------
# 7. Visualizations
# -------------------------

# Scenario Comparison
plt.figure(figsize=(8, 5))
plt.bar(summary['Scenario'], summary['Total Cost'], color=['#4e79a7', '#f28e2b', '#e15759', '#76b7b2', '#59a14f'])
plt.title("Scenario Comparison - Total Costs")
plt.ylabel("Total Cost")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig("scenario_comparison.png")
plt.close()

# Top 10 Costly Routes (Original)
top_routes = df.groupby(['Origin', 'Destination'])['TotalCost'].sum().nlargest(10)
plt.figure(figsize=(8, 5))
top_routes.plot(kind='bar', color='#f28e2b')
plt.title("Top 10 Costly Routes (Original)")
plt.ylabel("Cost")
plt.tight_layout()
plt.savefig("top_10_routes.png")
plt.close()

# Carrier Comparison (Scenario 4)
carrier_costs = df.groupby('Carrier')['Scenario4_TotalCost'].sum().sort_values(ascending=False)
plt.figure(figsize=(8, 5))
carrier_costs.plot(kind='bar', color='#59a14f')
plt.title("Carrier Comparison after Optimization (Scenario 4)")
plt.ylabel("Cost")
plt.tight_layout()
plt.savefig("carrier_comparison.png")
plt.close()

# Top 10 Routes by CPTK (Original)
top_cptk = df.groupby(['Origin', 'Destination'])['CPTK_Original'].mean().nlargest(10)
plt.figure(figsize=(8, 5))
top_cptk.plot(kind='bar', color='#4e79a7')
plt.title("Top 10 Routes by Cost per Ton-Km")
plt.ylabel("CPTK")
plt.tight_layout()
plt.savefig("top_10_cptk_routes.png")
plt.close()

print("✅ Visualizations saved: scenario_comparison.png, top_10_routes.png, carrier_comparison.png, top_10_cptk_routes.png")

# -------------------------
# 8. Weight Impact Analysis
# -------------------------

# Define weight categories
bins = [0, 5, 10, 20, 30, 50, 100]  # in tons
labels = ['0-5', '5-10', '10-20', '20-30', '30-50', '50+']
df['Weight_Category'] = pd.cut(df['Weight_tons'], bins=bins, labels=labels[:-1], right=False)
df['Weight_Category'] = df['Weight_Category'].cat.add_categories('50+')
df.loc[df['Weight_tons'] >= 50, 'Weight_Category'] = '50+'

# Group by weight category
weight_impact = df.groupby('Weight_Category').agg({
    'TotalCost': 'sum',
    'Scenario4_TotalCost': 'sum',
    'Weight_tons': 'sum'
}).reset_index()

weight_impact['Cost_Contribution_%'] = (weight_impact['TotalCost'] / df['TotalCost'].sum()) * 100
weight_impact.to_csv("weight_impact_analysis.csv", index=False)

# Visualization: Cost by Weight Category (Original)
plt.figure(figsize=(8, 5))
plt.bar(weight_impact['Weight_Category'], weight_impact['TotalCost'], color='#e15759')
plt.title("Cost Distribution by Weight Category (Original)")
plt.ylabel("Total Cost")
plt.xlabel("Weight Category (tons)")
plt.tight_layout()
plt.savefig("weight_impact_original.png")
plt.close()

# Visualization: Cost Comparison by Weight Category (Original vs Scenario 4)
weight_impact.set_index('Weight_Category')[['TotalCost', 'Scenario4_TotalCost']].plot(kind='bar', figsize=(8, 5))
plt.title("Weight Impact: Original vs Scenario 4")
plt.ylabel("Total Cost")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("weight_impact_comparison.png")
plt.close()

print("✅ Weight Impact Analysis complete. Charts saved: weight_impact_original.png, weight_impact_comparison.png")
