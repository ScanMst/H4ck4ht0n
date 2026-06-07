IF OBJECT_ID('TB_METRICAS_CLIENTE_PRODUCTO','U') IS NOT NULL
DROP TABLE TB_METRICAS_CLIENTE_PRODUCTO;

SELECT

    customer_id,
    pais,
    business_unit,
    cedis,

    sku_solicitado,
    nombre_sku_solicitado,

    COUNT(DISTINCT id_pedido) AS veces_comprado,

    SUM(TRY_CAST(Quantity AS DECIMAL(18,2))) AS cantidad_total,

    ROUND(AVG(TRY_CAST(Quantity AS DECIMAL(18,2))),2) AS promedio_piezas,

    MIN(fecha_pedido) AS primera_compra,

    MAX(fecha_pedido) AS ultima_compra,

    DATEDIFF(DAY, MAX(fecha_pedido), GETDATE()) AS dias_desde_ultima

INTO TB_METRICAS_CLIENTE_PRODUCTO

FROM PEDIDOS_MAESTRA

GROUP BY
    customer_id,
    pais,
    business_unit,
    cedis,
    sku_solicitado,
    nombre_sku_solicitado;


/*
=====================================================

AGREGAR FRECUENCIA PROMEDIO

La frecuencia promedio calcula cada cuántos días
un cliente vuelve a comprar el mismo producto.

Se utiliza LAG() para comparar una compra contra
la compra anterior del mismo cliente y SKU.

=====================================================
*/

ALTER TABLE TB_METRICAS_CLIENTE_PRODUCTO
ADD frecuencia_promedio DECIMAL(10,2);


WITH Compras AS
(
    SELECT DISTINCT
        customer_id,
        sku_solicitado,
        fecha_pedido
    FROM PEDIDOS_MAESTRA
),

Frecuencia AS
(
    SELECT
        customer_id,
        sku_solicitado,
        fecha_pedido,

        LAG(fecha_pedido) OVER
        (
            PARTITION BY customer_id, sku_solicitado
            ORDER BY fecha_pedido
        ) AS fecha_anterior

    FROM Compras
),

FrecuenciaPromedio AS
(
    SELECT
        customer_id,
        sku_solicitado,

        AVG
        (
            DATEDIFF
            (
                DAY,
                fecha_anterior,
                fecha_pedido
            )
        ) AS frecuencia_promedio

    FROM Frecuencia

    WHERE fecha_anterior IS NOT NULL

    GROUP BY
        customer_id,
        sku_solicitado
)

UPDATE M
SET frecuencia_promedio = F.frecuencia_promedio
FROM TB_METRICAS_CLIENTE_PRODUCTO M
INNER JOIN FrecuenciaPromedio F
    ON M.customer_id = F.customer_id
   AND M.sku_solicitado = F.sku_solicitado;


/*
=====================================================

AGREGAR BANDERA DE RECOMPRA

Regla:
Si los días desde la última compra son mayores
o iguales a la frecuencia promedio, entonces
el producto puede recomendarse para reabastecimiento.

=====================================================
*/

ALTER TABLE TB_METRICAS_CLIENTE_PRODUCTO
ADD recomendar_recompra BIT;

UPDATE TB_METRICAS_CLIENTE_PRODUCTO
SET recomendar_recompra =
CASE
    WHEN frecuencia_promedio IS NOT NULL
         AND dias_desde_ultima >= frecuencia_promedio
    THEN 1
    ELSE 0
END;


/*
=====================================================

AGREGAR INDICADOR DE HISTORIAL

Sirve para identificar si el cliente tiene compras
repetidas suficientes para calcular frecuencia.

=====================================================
*/

ALTER TABLE TB_METRICAS_CLIENTE_PRODUCTO
ADD tiene_historial BIT;

UPDATE TB_METRICAS_CLIENTE_PRODUCTO
SET tiene_historial =
CASE
    WHEN frecuencia_promedio IS NULL THEN 0
    ELSE 1
END;


/*
=====================================================

RANKING DE PRODUCTOS FAVORITOS

Se ordenan los productos por cliente según:
1. Veces comprado
2. Cantidad total
3. Última compra

=====================================================
*/

ALTER TABLE TB_METRICAS_CLIENTE_PRODUCTO
ADD ranking_cliente INT;

WITH Ranking AS
(
    SELECT
        customer_id,
        sku_solicitado,

        ROW_NUMBER() OVER
        (
            PARTITION BY customer_id
            ORDER BY
                veces_comprado DESC,
                cantidad_total DESC,
                ultima_compra DESC
        ) AS ranking_cliente

    FROM TB_METRICAS_CLIENTE_PRODUCTO
)

UPDATE M
SET ranking_cliente = R.ranking_cliente
FROM TB_METRICAS_CLIENTE_PRODUCTO M
INNER JOIN Ranking R
    ON M.customer_id = R.customer_id
   AND M.sku_solicitado = R.sku_solicitado;


/*
=====================================================

BANDERA DE FAVORITOS

Se considera favorito si está dentro del Top 3
de productos más relevantes para el cliente.

=====================================================
*/

ALTER TABLE TB_METRICAS_CLIENTE_PRODUCTO
ADD es_favorito BIT;

UPDATE TB_METRICAS_CLIENTE_PRODUCTO
SET es_favorito =
CASE
    WHEN ranking_cliente <= 3 THEN 1
    ELSE 0
END;


/*
=====================================================

VALIDACIONES

=====================================================
*/

-- Revisar estructura generada

SELECT TOP 20 *
FROM TB_METRICAS_CLIENTE_PRODUCTO;


-- Validar cliente demo principal

SELECT
    customer_id,
    nombre_sku_solicitado,
    veces_comprado,
    cantidad_total,
    promedio_piezas,
    primera_compra,
    ultima_compra,
    dias_desde_ultima,
    frecuencia_promedio,
    recomendar_recompra,
    ranking_cliente,
    es_favorito
FROM TB_METRICAS_CLIENTE_PRODUCTO
WHERE customer_id = '518361000000000000'
ORDER BY ranking_cliente;


-- Productos recomendados para recompra del cliente demo

SELECT
    nombre_sku_solicitado,
    dias_desde_ultima,
    frecuencia_promedio,
    recomendar_recompra
FROM TB_METRICAS_CLIENTE_PRODUCTO
WHERE customer_id = '518361000000000000'
  AND recomendar_recompra = 1
ORDER BY dias_desde_ultima DESC;


-- Top favoritos del cliente demo

SELECT
    nombre_sku_solicitado,
    veces_comprado,
    cantidad_total,
    ranking_cliente
FROM TB_METRICAS_CLIENTE_PRODUCTO
WHERE customer_id = '518361000000000000'
  AND es_favorito = 1
ORDER BY ranking_cliente;


-- Clientes con más productos con historial suficiente

SELECT
    customer_id,
    COUNT(*) AS productos_con_historial
FROM TB_METRICAS_CLIENTE_PRODUCTO
WHERE tiene_historial = 1
GROUP BY customer_id
ORDER BY productos_con_historial DESC;


-- Clientes con más recomendaciones de recompra

SELECT
    customer_id,
    COUNT(*) AS productos_recompra
FROM TB_METRICAS_CLIENTE_PRODUCTO
WHERE recomendar_recompra = 1
GROUP BY customer_id
ORDER BY productos_recompra DESC;