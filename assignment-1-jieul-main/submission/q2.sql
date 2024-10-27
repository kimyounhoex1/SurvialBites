SELECT distinct customers.customerNumber, customerName
FROM customers NATURAL JOIN orders;
