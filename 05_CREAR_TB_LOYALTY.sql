IF OBJECT_ID('TB_LOYALTY','U') IS NOT NULL
DROP TABLE TB_LOYALTY;

SELECT

    customer_id,

    SUM(Total) AS total_comprado,

    FLOOR(SUM(Total) / 20.0) AS puntos

INTO TB_LOYALTY

FROM PEDIDOS_MAESTRA

GROUP BY customer_id;


/*
=====================================================

VALIDACIONES

=====================================================
*/

-- Revisar tabla generada

SELECT TOP 20 *
FROM TB_LOYALTY
ORDER BY puntos DESC;


-- Validar cliente demo principal

SELECT *
FROM TB_LOYALTY
WHERE customer_id = '518361000000000000';


-- Recalcular puntos para validar contra tabla final

SELECT
    customer_id,
    SUM(Total) AS total_comprado_validacion,
    FLOOR(SUM(Total) / 20.0) AS puntos_validacion
FROM PEDIDOS_MAESTRA
WHERE customer_id = '518361000000000000'
GROUP BY customer_id;


-- Validar diferencias entre TB_LOYALTY y cálculo directo

SELECT
    L.customer_id,
    L.total_comprado,
    L.puntos,
    V.total_comprado_validacion,
    V.puntos_validacion
FROM TB_LOYALTY L
INNER JOIN
(
    SELECT
        customer_id,
        SUM(Total) AS total_comprado_validacion,
        FLOOR(SUM(Total) / 20.0) AS puntos_validacion
    FROM PEDIDOS_MAESTRA
    GROUP BY customer_id
) V
    ON L.customer_id = V.customer_id
WHERE
    L.puntos <> V.puntos_validacion
    OR L.total_comprado <> V.total_comprado_validacion;


-- Clientes con más puntos

SELECT TOP 20
    customer_id,
    total_comprado,
    puntos
FROM TB_LOYALTY
ORDER BY puntos DESC;