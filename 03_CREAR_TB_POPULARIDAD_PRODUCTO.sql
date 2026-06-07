IF OBJECT_ID('TB_POPULARIDAD_PRODUCTO','U') IS NOT NULL
DROP TABLE TB_POPULARIDAD_PRODUCTO;

WITH Popularidad AS
(
    SELECT
        cedis,
        pais,
        sku_solicitado,
        nombre_sku_solicitado,

        COUNT(DISTINCT customer_id) AS clientes_distintos,

        SUM(TRY_CAST(Quantity AS DECIMAL(18,2))) AS piezas_vendidas

    FROM PEDIDOS_MAESTRA

    GROUP BY
        pais,
        cedis,
        sku_solicitado,
        nombre_sku_solicitado
)

SELECT
    *,

    DENSE_RANK() OVER
    (
        PARTITION BY pais, cedis
        ORDER BY
            clientes_distintos DESC,
            piezas_vendidas DESC
    ) AS ranking_popularidad

INTO TB_POPULARIDAD_PRODUCTO

FROM Popularidad;


/*
=====================================================

VALIDACIONES

=====================================================
*/

-- Revisar tabla generada

SELECT TOP 20 *
FROM TB_POPULARIDAD_PRODUCTO;


-- Validar ranking de popularidad para CEDIS demo

SELECT TOP 20
    cedis,
    pais,
    sku_solicitado,
    nombre_sku_solicitado,
    clientes_distintos,
    piezas_vendidas,
    ranking_popularidad
FROM TB_POPULARIDAD_PRODUCTO
WHERE cedis = '3804'
ORDER BY ranking_popularidad ASC;


-- Ver rango de rankings

SELECT
    MIN(ranking_popularidad) AS ranking_minimo,
    MAX(ranking_popularidad) AS ranking_maximo
FROM TB_POPULARIDAD_PRODUCTO;


-- Productos más populares por país y CEDIS

SELECT TOP 50
    pais,
    cedis,
    nombre_sku_solicitado,
    clientes_distintos,
    piezas_vendidas,
    ranking_popularidad
FROM TB_POPULARIDAD_PRODUCTO
ORDER BY
    pais,
    cedis,
    ranking_popularidad;


-- Validar productos más populares de México

SELECT TOP 20
    pais,
    cedis,
    nombre_sku_solicitado,
    clientes_distintos,
    piezas_vendidas,
    ranking_popularidad
FROM TB_POPULARIDAD_PRODUCTO
WHERE pais LIKE '%xico%'
ORDER BY
    ranking_popularidad ASC;