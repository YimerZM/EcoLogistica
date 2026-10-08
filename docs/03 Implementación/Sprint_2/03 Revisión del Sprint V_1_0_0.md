# Revisión del sprint — Sprint 2

**Nombre del Proyecto:** EcoLogística — Sistema de Optimización de Rutas Sostenibles

**Líder del Proyecto:** ZEVALLOS MELENDRES YIMER EDYSON

**Sprint:** 2 — Incremento ejecutable del núcleo operativo

**Inicio:** 2026-09-25. **Cierre informado:** 2026-10-08.

**Versión:** 1.0.0. **Fecha de actualización documental:** 2026-10-08.

[Volver al README principal](../../../README.md)

## Historias de Usuario completadas en este Sprint

Se cerraron las cuatro historias del núcleo. La generación de rutas no entra en este cierre.

| Historia | Backlog | Funcionalidad completada | Estado |
|---|---|---|---|
| US-001 | EP-01 | Iniciar sesión. El contador se evalúa al comenzar el intento | Finalizada |
| US-003 | EP-02 | Registrar vehículos con placa y capacidad | Finalizada |
| US-004 | EP-02 | Registrar puntos WGS84 en El Tambo, Huancayo o Chilca | Finalizada |
| US-005 | EP-02 | Registrar pedidos generales y rechazar carga prohibida | Finalizada |

## Demostración del trabajo completado

Participaron ZEVALLOS MELENDRES YIMER EDYSON, POMACHAGUA YAPIAS BRYAN ANTONY y CAJAMALQUI DAVILA JOSEMARIA PIERO. El contratante no operó la herramienta; el equipo recorrió su guion de consulta como pendiente.

| Historia | Funcionalidad terminada | Recorrido de presentación | Evidencia |
|---|---|---|---|
| US-001 | Inicio de sesión | Clave inválida rechazada. Clave válida aceptada | Pruebas de `tests.test_reglas` |
| US-003 | Vehículo | Alta de placa ABC-123 y 800 kg | API `/api/vehiculos` |
| US-004 | Punto | Huancayo, -12.07, -75.21, método WGS84. Lima rechazada | API `/api/puntos` |
| US-005 | Pedido | Explosivo rechazado por RN-016. Carga general en PENDIENTE | API `/api/pedidos` |

## Pendientes

1. **US-002:** gestión de usuarios y cuenta del contratante.
2. **US-006, US-007 y US-008:** generar, visualizar y reoptimizar rutas.
3. Sustituir el almacén en memoria por PostgreSQL y la API actual por FastAPI.
4. Adjuntar capturas recortadas del tablero de Jira y la observación de la revisión académica.

## Historial de versiones

| Versión | Fecha de edición | Cambio |
|---|---|---|
| 1.0.0 | 2026-10-08 | Revisión del Sprint 2 con el formato mostrado en clase. |
