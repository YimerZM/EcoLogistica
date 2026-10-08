# Informe de estado del proyecto

La versión vigente de los sprints está en [Sprint 1](Sprint_1/01%20Informe%20de%20estado%20del%20proyecto%20V_1_0_0.md) y [Sprint 2](Sprint_2/01%20Informe%20de%20estado%20del%20proyecto%20V_1_0_0.md).

[← Volver al README Principal](../../README.md)

**Nombre del Proyecto:** EcoLogística – Sistema de Optimización de Rutas Sostenibles

**Líder del Proyecto:** ZEVALLOS MELENDRES YIMER EDYSON

**Sprint:** 2

**Periodo:** 25/09/2026 al 08/10/2026

**Estado al 01/10/2026:** el sprint está en curso. La línea base documental quedó corregida según la retroalimentación y el incremento de código del núcleo operativo ya se ejecuta en local.

## Historias de Usuario completadas en este Sprint

| ID | Historia | Evidencia en el repositorio |
|---|---|---|
| US-001 | Iniciar sesión | `src/backend/ecologistica/reglas.py` evalúa y restablece el contador al comenzar la sesión. |
| US-003 | Registrar vehículos | Alta de placa y capacidad desde `src/frontend`. |
| US-004 | Registrar puntos de entrega | Solo coordenadas WGS84 en El Tambo, Huancayo o Chilca. |
| US-005 | Registrar pedidos | El pedido nace en PENDIENTE y la carga prohibida se rechaza (RN-016). |

Estas cuatro historias eran la meta del Sprint 1 y no tenían código en el repositorio. El Sprint 2 las implementó ya con las correcciones del docente.

## Demostración del trabajo completado

El 01/10/2026 el equipo ejecutó la aplicación en local y recorrió, con el rol de operador, el inicio de sesión, el alta de un vehículo, el alta de un punto en Huancayo y el rechazo de un pedido con carga explosiva. El contratante queda como rol de consulta de sus pedidos; esa consulta aún no está en este incremento.

## Pendientes

| ID | Pendiente | Sprint previsto |
|---|---|---|
| US-002 | Gestionar usuarios | Sprint 3 |
| US-006 | Generar rutas | Sprint 3 |
| US-007 | Visualizar rutas | Sprint 3 |
| US-008 | Reoptimizar rutas | Sprint 4 |
| US-009 a US-015 | Entregas, indicadores, auditoría y parámetros | Sprints 3 y 4 |

El algoritmo de rutas, el mapa y el dashboard no forman parte del estado de este sprint.

## Control de cambios

| Versión | Fecha | Descripción | Responsable |
|---|---|---|---|
| 1.0.0 | 01/10/2026 | Informe del Sprint 2. | ZEVALLOS MELENDRES YIMER EDYSON |
