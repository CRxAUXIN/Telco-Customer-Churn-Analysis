
-- Churn rate overall
SELECT AVG(churned) AS overall_churn_rate FROM churn;

-- Churn by contract type
SELECT c.contract_type, AVG(ch.churned) AS churn_rate
FROM customers c
JOIN churn ch ON c.customer_id = ch.customer_id
GROUP BY c.contract_type
ORDER BY churn_rate DESC;

-- High risk customers (top 100 by churn probability)
SELECT ch.customer_id, ch.churn_probability, s.monthly_charges, u.num_complaints_last_year, b.num_late_payments
FROM churn ch
JOIN services s ON ch.customer_id = s.customer_id
JOIN usage u ON ch.customer_id = u.customer_id
JOIN billing b ON ch.customer_id = b.customer_id
ORDER BY ch.churn_probability DESC
LIMIT 100;

-- Revenue lost (approx)
SELECT SUM(s.monthly_charges) * 6 AS estimated_6_month_revenue_lost
FROM services s
JOIN churn ch ON s.customer_id = ch.customer_id
WHERE ch.churned = 1;
