import pandas as pd
import numpy as np

# ============================
# Step 2.1: Load the Data
# ============================
shipments = pd.read_csv('shipments_large.csv')
fuel = pd.read_csv('fuel_price_index_large.csv')

# ============================
# Step 2.2: Check for Missing or Invalid Values
# ============================
print("Missing values in shipments:\n", shipments.isnull().sum())
print("\nMissing values in fuel:\n", fuel.isnull().sum())

# Fill missing numeric columns with median
numeric_cols = ['Distance_km', 'Weight_tons', 'BaseCost', 'FuelCost', 'OtherCost']
for col in numeric_cols:
    if shipments[col].isnull().sum() > 0:
        shipments[col].fillna(shipments[col].median(), inplace=True)

# Fill missing categorical columns with mode
categorical_cols = ['Origin', 'Destination', 'Route', 'Mode', 'Carrier']
for col in categorical_cols:
    if shipments[col].isnull().sum() > 0:
        shipments[col].fillna(shipments[col].mode()[0], inplace=True)

# ============================
# Step 2.3: Validate Data Types
# ============================
shipments['ShipDate'] = pd.to_datetime(shipments['ShipDate'], errors='coerce')
fuel['Date'] = pd.to_datetime(fuel['Date'], errors='coerce')

# Drop rows where ShipDate is invalid
shipments.dropna(subset=['ShipDate'], inplace=True)

# ============================
# Step 2.4: Remove Duplicates
# ============================
shipments.drop_duplicates(subset=['ShipmentID'], inplace=True)

# ============================
# Step 2.5: Add Derived Columns (KPIs)
# ============================
# Total Cost
shipments['TotalCost'] = shipments['BaseCost'] + shipments['FuelCost'] + shipments['OtherCost']

# Cost per Ton-Km
shipments['Cost_per_TonKm'] = shipments['TotalCost'] / (shipments['Distance_km'] * shipments['Weight_tons'])

# Fuel Percentage
shipments['Fuel_Percentage'] = (shipments['FuelCost'] / shipments['TotalCost']) * 100

# ============================
# Step 2.6: Handle Outliers
# ============================
# Remove shipments with zero or negative distance/weight
shipments = shipments[(shipments['Distance_km'] > 0) & (shipments['Weight_tons'] > 0)]

# Optional: Remove extreme outliers for TotalCost
q_low = shipments['TotalCost'].quantile(0.01)
q_high = shipments['TotalCost'].quantile(0.99)
shipments = shipments[(shipments['TotalCost'] >= q_low) & (shipments['TotalCost'] <= q_high)]

# ============================
# Step 2.7: Merge with Fuel Data
# ============================
# Sort both datasets by date for merge_asof
shipments = shipments.sort_values('ShipDate')
fuel = fuel.sort_values('Date')

# Merge to get FuelPrice for each shipment based on ShipDate
shipments = pd.merge_asof(shipments, fuel, left_on='ShipDate', right_on='Date')

# Drop the extra Date column (from fuel)
shipments.drop(columns=['Date'], inplace=True)

# ============================
# Step 2.8: Save Cleaned Data
# ============================
shipments.to_csv('cleaned_shipments.csv', index=False)

print("\n✅ Phase 2 Completed: Cleaned dataset saved as 'cleaned_shipments.csv'")
print(shipments.head(10))
