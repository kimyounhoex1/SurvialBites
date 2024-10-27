SELECT customerName, orderNumber, productName, orderDate
FROM customers NATURAL JOIN orders NATURAL JOIN orderdetails NATURAL JOIN products
WHERE products.productLine = 'Classic Cars' AND orders.status = 'Shipped'
ORDER BY orders.orderDate ASC;
