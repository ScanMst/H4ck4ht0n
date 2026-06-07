SELECT

  o.id_pedido,
  o.customer_id,
  o.pais,
  o.business_unit,
  o.cedis,
  o.fecha_pedido,
  o.status_final,
  o.valor_pedido,
  o.SubTotal,
  o.Total,

  d.linea_id,
  d.sku_solicitado,
  d.nombre_sku_solicitado,
  d.Quantity,
  d.Status

INTO PEDIDOS_MAESTRA

FROM Orders o

INNER JOIN OrderDetails3 d
ON o.id_pedido = d.id_pedido;

--VALIDAR 
SELECT COUNT(*)
FROM PEDIDOS_MAESTRA;

-- Pedidos distintos

SELECT COUNT(DISTINCT id_pedido)
FROM PEDIDOS_MAESTRA;

-- Clientes distintos

SELECT COUNT(DISTINCT customer_id)
FROM PEDIDOS_MAESTRA;

-- Productos distintos

SELECT COUNT(DISTINCT sku_solicitado)
FROM PEDIDOS_MAESTRA;

-- Revisar pedidos duplicados

SELECT
id_pedido,
COUNT() AS registros
FROM PEDIDOS_MAESTRA
GROUP BY id_pedido
HAVING COUNT() > 1
ORDER BY registros DESC;

-- Top clientes por número de pedidos

SELECT
customer_id,
COUNT(DISTINCT id_pedido) AS pedidos
FROM PEDIDOS_MAESTRA
GROUP BY customer_id
ORDER BY pedidos DESC;

-- Top clientes por variedad de productos

SELECT
customer_id,
COUNT(DISTINCT sku_solicitado) AS productos
FROM PEDIDOS_MAESTRA
GROUP BY customer_id
ORDER BY productos DESC;