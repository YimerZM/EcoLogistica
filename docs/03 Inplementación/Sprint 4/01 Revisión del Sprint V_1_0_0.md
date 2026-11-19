[← Volver al README principal](../../../README.md)

# Revisión del sprint

**Nombre del Proyecto:** EcoLogística — Sistema de Optimización de Rutas Sostenibles

**Líder del Proyecto:** Zevallos Melendres, Yimer Edyson

**Sprint:** 4 — Cierre del incremento, pruebas E2E y operación en pantalla

**Fecha de la revisión:** 2026-11-19

**Versión:** 1.0.0

## Historias de Usuario completadas en este Sprint

El comportamiento de estas historias está en la página desde el commit `8f23fbf` (`feat: presenta la operacion completa en una pagina con mapa, roles e indicadores`). La ayuda y la edición de vehículos, puntos y pedidos pendientes quedaron en el commit `82d5c25`. La suite de Playwright, los tres flujos de GitHub Actions y estos informes cierran en el commit `b5d956c`. No hay pull request: el trabajo se integró por commit en `develop` y `main`.

| Historia | Criterio verificado | Evidencia |
|---|---|---|
| US-008 Reoptimizar rutas | Con una ruta activa y un cambio operativo, el sistema arma una propuesta nueva. Sin ruta activa, o sin cambio operativo, la operación se niega y la ruta vigente se conserva. | `POST /api/rutas/reoptimizar`. Playwright: «reoptimizar responde con una de sus tres reglas». Commit `8f23fbf`. |
| US-009 Consultar pedidos | El listado muestra los pedidos y su estado. El filtro por estado deja solo los que cumplen el criterio. | `GET /api/pedidos?estado=`. Control `#filtro-estado`. Commit `8f23fbf`. |
| US-010 Registrar entregas | Un pedido en ruta se registra como entregado o con incidencia. El kilómetro de la ruta se conserva. | `POST /api/entregas`. Commit `8f23fbf`. |
| US-011 Consultar indicadores | Con datos, el panel muestra pendientes, en ruta, entregados, incidencias, kilogramos, kilómetros, CO₂ y minutos. Sin kilómetros en el periodo, informa que no hay datos. | `GET /api/indicadores`. Commit `8f23fbf` y minutos en `82d5c25`. |
| US-012 Consultar indicadores ambientales | El mismo panel consulta un periodo y muestra el CO₂ con el factor vigente (0,21 kg/km, editable y mayor que cero). | Selector de periodo. Commit `8f23fbf`. |
| US-013 Exportar información | La exportación genera un CSV con los pedidos. | `GET /api/exportar/pedidos`. Commit `8f23fbf`. El CSV filtrado queda en Pendientes. |
| US-014 Consultar auditoría | El administrador y el auditor ven las acciones registradas. | `GET /api/auditoria`. Commit `8f23fbf`. El filtro de auditoría queda en Pendientes. |
| US-015 Configurar parámetros | Un factor de emisión mayor que cero se guarda. Un valor no permitido se rechaza con mensaje. | `PUT /api/parametros`. Commit `8f23fbf`. |

También quedó cerrado en este incremento el archivo de ayuda (`src/frontend/ayuda.html`, commit `82d5c25`) y la corrección de pantalla del 2026-11-19: la regla `[hidden] { display: none !important; }` en `src/frontend/css/estilos.css` mantiene oculto el panel de la aplicación cuando el ingreso falla.

## Demostración del trabajo completado

La demostración del 2026-11-19 la ejecutó Zevallos Melendres, Yimer Edyson en el entorno local. La página se abre con `python -m ecologistica` desde `src/backend` y queda en http://127.0.0.1:8765. Ese proceso es la aplicación en primer plano. No hay entorno de staging ni URL de producción.

Recorrido exhibido:

1. Ingreso con la ficha Operador. Una cuenta inexistente (`nadie@ecologistica.test`) recibe el mensaje de credenciales y el panel de la aplicación permanece oculto.
2. Preparar los datos de El Tambo, Huancayo y Chilca y generar la ruta. El detalle nombra El Tambo y Chilca.
3. Pulsar Reoptimizar. El mensaje es uno de los tres de la regla: ruta reoptimizada, sin ruta activa, o sin cambio operativo.
4. Intentar un pedido de carga explosiva. El sistema responde RN-016 y no lo deja pendiente.
5. Abrir el archivo de ayuda. `GET /` y `GET /ayuda.html` responden 200. Un archivo ausente responde 404.

La suite automática repitió ese recorrido en Chromium, Firefox y WebKit: 21 pruebas, 21 superadas, 20,2 segundos, un solo worker, el 2026-11-19 en la máquina local. El detalle de tiempos está en [03 Analisis PlayWrigth V_1_0_0](03%20Analisis%20PlayWrigth%20V_1_0_0.md).

La retroalimentación de esta revisión es la del propio cierre: la pantalla de ingreso mostraba la aplicación porque `.app { display: grid }` tapaba el atributo `hidden`. Esa falla ya está corregida y la prueba de clave incorrecta la vigila.

## Pendientes

1. US-013, segundo criterio: el CSV exporta el listado completo de pedidos. Todavía no exporta solo el resultado del filtro de estado.
2. US-014, segundo criterio: la auditoría se lista completa. Todavía no tiene filtro en pantalla.
3. FastAPI, PostgreSQL, teselas de mapa externas y capturas de Jira siguen fuera de este incremento. El servidor es la biblioteca estándar de Python y los datos viven en memoria.
4. No hay secreto de hospedaje ni URL pública. El flujo `deploy-production.yml` comprueba la compilación y publica el paquete como artefacto de GitHub Actions. No despliega en Vercel, Render, Railway ni AWS.
5. La escala SUS está redactada en [04 Usabilidad V_1_0_0](04%20Usabilidad%20V_1_0_0.md). Ningún participante la respondió, así que no hay puntaje promedio.
6. WebKit no emitió una entrada de Largest Contentful Paint en la medición local. Chromium y Firefox sí.

## Historial de versiones

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0.0 | 2026-11-19 | Revisión del Sprint 4. Historias en `8f23fbf` y `82d5c25`. Suite, flujos e informes en `b5d956c`. |
