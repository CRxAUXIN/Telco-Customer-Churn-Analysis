
# Telco Churn Analysis - Analysis script
# Author: Arnav Gajbe
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

customers = pd.read_csv('customers.csv')
services = pd.read_csv('services.csv')
usage = pd.read_csv('usage.csv')
billing = pd.read_csv('billing.csv')
churn = pd.read_csv('churn.csv')

df = customers.merge(services, on='customer_id').merge(usage, on='customer_id').merge(billing, on='customer_id').merge(churn, on='customer_id')

# Basic KPIs
total_customers = len(df)
churn_rate = df['churned'].mean()
avg_monthly_charges = df['monthly_charges'].mean()
avg_tenure = df['tenure_months'].mean()
revenue_lost = (df.loc[df['churned']==1, 'monthly_charges']).sum() * 6  # approx 6 months revenue lost

print("Total customers:", total_customers)
print("Churn rate:", round(churn_rate*100,2), "%")
print("Avg monthly charges:", round(avg_monthly_charges,2))
print("Avg tenure (months):", round(avg_tenure,1))
print("Estimated revenue lost (approx next 6 months from churned customers): ₹", int(revenue_lost))

# Churn by contract type
churn_by_contract = df.groupby('contract_type')['churned'].mean().reset_index().sort_values('churned', ascending=False)
print("\nChurn rate by contract type:\n", churn_by_contract)

# High risk customers (top by churn_probability)
high_risk = df.sort_values('churn_probability', ascending=False).head(200)
high_risk[['customer_id','churn_probability','monthly_charges','num_complaints_last_year','num_late_payments']].to_csv('high_risk_customers.csv', index=False)

# CLTV approximation (simple) = monthly_charges * (expected_months_remaining) 
# expected_months_remaining = (1 / churn_rate) for population average, but we estimate per user as (1 / churn_probability)
df['expected_months'] = np.clip(1/np.where(df['churn_probability']>0, df['churn_probability'], 0.01), 1, 120)
df['approx_CLTV'] = df['monthly_charges'] * df['expected_months']

top_ltv = df.sort_values('approx_CLTV', ascending=False).head(20)
top_ltv[['customer_id','approx_CLTV','monthly_charges','tenure_months']].to_csv('top_ltv_customers.csv', index=False)

# Save summary KPIs
kpis = {
    'total_customers': int(total_customers),
    'churn_rate': float(churn_rate),
    'avg_monthly_charges': float(avg_monthly_charges),
    'avg_tenure_months': float(avg_tenure)
}
import json
with open('kpis.json','w') as f:
    json.dump(kpis,f,indent=2)

# Save a churn by plan plot
plot = df.groupby('plan')['churned'].mean().sort_values(ascending=False)
plt.figure(figsize=(8,5))
plot.plot(kind='bar')
plt.title('Churn Rate by Plan')
plt.ylabel('Churn Rate')
plt.tight_layout()
plt.savefig('churn_by_plan.png')
print('\nSaved churn_by_plan.png, high_risk_customers.csv, top_ltv_customers.csv, kpis.json')
