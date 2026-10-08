# Informe de estado del proyecto — Sprint 1

**Nombre del Proyecto:** EcoLogística — Sistema de Optimización de Rutas Sostenibles

**Líder del Proyecto:** ZEVALLOS MELENDRES YIMER EDYSON

**Sprint:** 1 — Núcleo operativo de registros

**Inicio:** 2026-09-11. **Cierre informado:** 2026-09-24.

**Versión:** 1.0.0. **Fecha de actualización documental:** 2026-10-08.

[Volver al README principal](../../../README.md)

## Historias de Usuario completadas en este Sprint

El Sprint 1 cerró el 24 de septiembre de 2026 con las cuatro historias del núcleo aceptadas en el backlog y con sus criterios de aceptación. El incremento ejecutable de esas historias no estaba en el repositorio al cierre; se construyó en el Sprint 2.

| Historia | Backlog | Funcionalidad comprometida | Estado al cierre |
|---|---|---|---|
| US-001 | EP-01 | Iniciar sesión, con el contador de intentos evaluado al comenzar | Comprometida. Código en el Sprint 2 |
| US-003 | EP-02 | Registrar vehículos | Comprometida. Código en el Sprint 2 |
| US-004 | EP-02 | Registrar puntos de entrega con coordenadas WGS84 | Comprometida. Código en el Sprint 2 |
| US-005 | EP-02 | Registrar pedidos y rechazar carga prohibida | Comprometida. Código en el Sprint 2 |

Avance de código al 24 de septiembre: 0 de 4 historias en el repositorio. Avance de especificación: 4 de 4.

## Demostración del trabajo completado

En la revisión del 24 de septiembre se mostró la especificación, no una aplicación en ejecución.

| Bloque | Trabajo cerrado en el sprint | Recorrido de presentación | Evidencia |
|---|---|---|---|
| Acceso, US-001 | Criterio de inicio de sesión y regla de intentos | Lectura del requisito y de RN-001 | `docs/01 Inicio/06. Requisitos funcionales V_1_0_0.md` |
| Vehículos, US-003 | Campos de placa, capacidad y estado | Lectura de la historia en el backlog | `docs/02 Planificación/01 Transformando a ágil V_1_0_0.md` |
| Puntos, US-004 | Geolocalización solo por coordenadas WGS84 en El Tambo, Huancayo y Chilca | Lectura de A-02 y C-04 | `docs/01 Inicio/04. Registro de supuestos y restricciones V_1_0_0.md` |
| Pedidos, US-005 | Pedido en estado PENDIENTE y rechazo de carga prohibida | Lectura de RN-016 | `docs/01 Inicio/09. Reglas de negocio V_1_0_0.md` |

## Pendientes

1. Publicar el frontend y el backend de US-001, US-003, US-004 y US-005.
2. Demostrar el rechazo de una clave incorrecta, de un distrito fuera del ámbito y de una carga prohibida.
3. Adjuntar la captura de Jira del Sprint 1, recortada al tablero.

## Historial de versiones

| Versión | Fecha de edición | Cambio |
|---|---|---|
| 1.0.0 | 2026-10-08 | Informe del Sprint 1 con el formato mostrado en clase. |
