SELECT customerName, HighestPayment
FROM (SELECT customerName, sum(payments.amount)
      FROM customers NATURAL JOIN payments
      GROUP BY customerName)
      AS customer_higest(customerName, HighestPayment)
ORDER BY HighestPayment DESC
LIMIT 1;
