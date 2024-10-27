SELECT productCode, productName
FROM products
WHERE productCode NOT IN 
  (SELECT productCode 
   FROM orderdetails);
