# Retrospectiva del sprint — Sprint 3

**Nombre del Proyecto:** EcoLogística — Sistema de Optimización de Rutas Sostenibles

**Líder del Proyecto:** ZEVALLOS MELENDRES YIMER EDYSON

**Sprint:** 3 — Usuarios y propuesta de ruta

**Inicio:** 2026-10-09. **Cierre informado:** 2026-11-05.

**Versión:** 1.0.0. **Fecha de actualización documental:** 2026-11-05.

[Volver al README principal](../../../README.md)

## ¿Qué aprendimos?

Una propuesta de ruta no es un mapa. Cerrar US-006 con una lista deja US-007 explícitamente pendiente y evita presentar una pantalla que el repositorio no tiene.

## ¿Qué estamos haciendo bien?

El administrador, el operador y el contratante ya no comparten la misma pantalla. La propuesta rechaza el caso sin vehículo y deja fuera el pedido que no cabe.

## ¿Qué podemos hacer mejor?

### Personas

El cierre del 22 de octubre se movió al 5 de noviembre. La integración no puede quedar en una sola persona el último día.

### Relaciones

El contratante ya ve sus pedidos. Falta sentar con él el filtro que pide US-009.

### Procesos

La historia se da por hecha cuando la prueba pasa, no cuando el formulario aparece.

### Herramientas

El almacén sigue en memoria. Una ruta generada se pierde al reiniciar el proceso. PostgreSQL queda para el siguiente incremento, junto con el mapa.

### Acciones a realizar

| ID | Acción | Responsable | Momento objetivo | Estado | Evidencia de cierre |
|---|---|---|---|---|---|
| S3-ACT-01 | Dibujar la ruta en el mapa, US-007 | POMACHAGUA YAPIAS BRYAN ANTONY | 2026-12-03 | Pendiente | Pantalla con el recorrido |
| S3-ACT-02 | Filtrar pedidos del contratante, US-009 | CAJAMALQUI DAVILA JOSEMARIA PIERO | 2026-11-19 | Pendiente | Listado filtrado por estado |
| S3-ACT-03 | Mantener la prueba de ruta en el commit de la historia | POMACHAGUA YAPIAS BRYAN ANTONY | En cada incremento | En curso | `python -m unittest tests.test_reglas tests.test_e2e` |
| S3-ACT-04 | Pegar las cinco capturas recortadas de Jira | ZEVALLOS MELENDRES YIMER EDYSON | Revisión académica | Pendiente | Imágenes solo del panel |

## Historial de versiones

| Versión | Fecha de edición | Cambio |
|---|---|---|
| 1.0.0 | 2026-11-05 | Retrospectiva del Sprint 3. |
