SELECT distinct customers.customerNumber, customerName
FROM customers LEFT OUTER JOIN orders
ON customers.customerNumber = orders.customerNumber
GROUP BY customers.customerNumber
HAVING COUNT(orders.orderNumber) <= 1;
