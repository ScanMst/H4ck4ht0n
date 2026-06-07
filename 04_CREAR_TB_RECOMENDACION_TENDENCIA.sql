IF OBJECT_ID('TB_RECOMENDACION_TENDENCIA','U') IS NOT NULL
DROP TABLE TB_RECOMENDACION_TENDENCIA;

WITH ClienteContexto AS
(
SELECT
customer_id,
pais,
cedis,
MAX(fecha_pedido) AS ultima_fecha

```
FROM PEDIDOS_MAESTRA

GROUP BY
    customer_id,
    pais,
    cedis
```

),

Clientes AS
(
SELECT *,

```
    ROW_NUMBER() OVER
    (
        PARTITION BY customer_id
        ORDER BY ultima_fecha DESC
    ) AS rn

FROM ClienteContexto
```

),
--SE REALIZA LO SIGUIENTE POR QUE SI NO HAY MUCHIS DUPLUCADOS POR SKU

Popularidad AS
(
SELECT *,

```
    CASE

        WHEN UPPER(nombre_sku_solicitado)
            LIKE '%COCA%'
            THEN 'COCA-COLA'

        WHEN UPPER(nombre_sku_solicitado)
            LIKE '%CIEL%'
            THEN 'CIEL'

        WHEN UPPER(nombre_sku_solicitado)
            LIKE '%FUZE%'
            THEN 'FUZE TEA'

        WHEN UPPER(nombre_sku_solicitado)
            LIKE '%DEL VALLE%'
            THEN 'DEL VALLE'

        WHEN UPPER(nombre_sku_solicitado)
            LIKE '%MONSTER%'
            THEN 'MONSTER'

        WHEN UPPER(nombre_sku_solicitado)
            LIKE '%TOPO CHICO%'
            THEN 'TOPO CHICO'

        ELSE UPPER(nombre_sku_solicitado)

    END AS familia_producto

FROM TB_POPULARIDAD_PRODUCTO
```

),

HistorialCliente AS
(
SELECT DISTINCT

```
    customer_id,
    sku_solicitado,

    CASE

        WHEN UPPER(nombre_sku_solicitado)
            LIKE '%COCA%'
            THEN 'COCA-COLA'

        WHEN UPPER(nombre_sku_solicitado)
            LIKE '%CIEL%'
            THEN 'CIEL'

        WHEN UPPER(nombre_sku_solicitado)
            LIKE '%FUZE%'
            THEN 'FUZE TEA'

        WHEN UPPER(nombre_sku_solicitado)
            LIKE '%DEL VALLE%'
            THEN 'DEL VALLE'

        WHEN UPPER(nombre_sku_solicitado)
            LIKE '%MONSTER%'
            THEN 'MONSTER'

        WHEN UPPER(nombre_sku_solicitado)
            LIKE '%TOPO CHICO%'
            THEN 'TOPO CHICO'

        ELSE UPPER(nombre_sku_solicitado)

    END AS familia_producto

FROM TB_METRICAS_CLIENTE_PRODUCTO
```

),

# /*


GENERAR RECOMENDACIONES

*/

Candidatos AS
(
SELECT

```
    C.customer_id,
    C.pais,
    C.cedis,

    P.sku_solicitado,
    P.nombre_sku_solicitado,

    P.clientes_distintos,
    P.piezas_vendidas,

    P.ranking_popularidad,

    ROW_NUMBER() OVER
    (
        PARTITION BY C.customer_id
        ORDER BY P.ranking_popularidad ASC
    ) AS ranking_recomendacion

FROM Clientes C

INNER JOIN Popularidad P

    ON C.pais = P.pais
   AND C.cedis = P.cedis

WHERE C.rn = 1

  AND P.ranking_popularidad <= 50

  AND NOT EXISTS
  (
      SELECT 1

      FROM HistorialCliente H

      WHERE H.customer_id = C.customer_id

      AND
      (
          H.sku_solicitado = P.sku_solicitado

          OR

          H.familia_producto =
          P.familia_producto
      )
  )
```

)

SELECT *

INTO TB_RECOMENDACION_TENDENCIA

FROM Candidatos

WHERE ranking_recomendacion <= 3;

# /*

VALIDACIONES

=====================================================
*/

-- Revisar estructura

SELECT TOP 20 *
FROM TB_RECOMENDACION_TENDENCIA;

-- Cliente demo principal

SELECT *
FROM TB_RECOMENDACION_TENDENCIA
WHERE customer_id='518361000000000000'
ORDER BY ranking_recomendacion;

-- Número de recomendaciones por cliente

SELECT
customer_id,
COUNT(*) AS recomendaciones
FROM TB_RECOMENDACION_TENDENCIA
GROUP BY customer_id
ORDER BY recomendaciones DESC;

-- Productos más recomendados

SELECT
nombre_sku_solicitado,
COUNT(*) AS veces_recomendado
FROM TB_RECOMENDACION_TENDENCIA
GROUP BY nombre_sku_solicitado
ORDER BY veces_recomendado DESC;

```
```
