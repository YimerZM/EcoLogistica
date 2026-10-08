# Informe de estado del proyecto — Sprint 2

**Nombre del Proyecto:** EcoLogística — Sistema de Optimización de Rutas Sostenibles

**Líder del Proyecto:** ZEVALLOS MELENDRES YIMER EDYSON

**Sprint:** 2 — Incremento ejecutable del núcleo operativo

**Inicio:** 2026-09-25. **Cierre informado:** 2026-10-08.

**Versión:** 1.0.0. **Fecha de actualización documental:** 2026-10-08.

[Volver al README principal](../../../README.md)

## Historias de Usuario completadas en este Sprint

Se cerraron las cuatro historias que el Sprint 1 había dejado solo en el backlog. Avance de código: 4 de 4 historias del núcleo. La generación de rutas sigue pendiente.

| Historia | Backlog | Funcionalidad completada | Estado |
|---|---|---|---|
| US-001 | EP-01 | Iniciar sesión. Al comenzar, si el bloqueo de 15 minutos venció, el contador vuelve a cero antes de validar la clave | Finalizada |
| US-003 | EP-02 | Registrar vehículos con placa y capacidad | Finalizada |
| US-004 | EP-02 | Registrar puntos solo con coordenadas WGS84 en El Tambo, Huancayo o Chilca | Finalizada |
| US-005 | EP-02 | Registrar pedidos en estado PENDIENTE y rechazar carga prohibida | Finalizada |

## Demostración del trabajo completado

La demostración del 1 de octubre de 2026 se hizo en local, en http://127.0.0.1:8765, con el operador `operador@ecologistica.test`.

| Historia | Funcionalidad terminada | Recorrido de presentación | Evidencia |
|---|---|---|---|
| US-001 | Inicio de sesión y contador al comenzar | Clave incorrecta no abre sesión. Clave válida sí la abre | `src/backend/ecologistica/reglas.py` y pruebas unitarias |
| US-003 | Alta de vehículo | Registrar placa y capacidad. Una placa repetida se rechaza | `src/frontend` y API `/api/vehiculos` |
| US-004 | Punto georreferenciado | Alta en Huancayo, -12.07, -75.21, método WGS84. Lima se rechaza | API `/api/puntos` |
| US-005 | Pedido y RN-016 | La carga explosiva no se guarda. La carga general queda PENDIENTE | API `/api/pedidos` |

## Pendientes

1. **US-002:** gestionar usuarios, incluida la cuenta del contratante.
2. **US-006:** generar rutas con capacidad y ventana de tiempo.
3. **US-007:** visualizar la ruta en el mapa.
4. **US-008:** reoptimizar una ruta ante un cambio operativo.
5. Pasar la API de la biblioteca estándar de Python a FastAPI y el almacén en memoria a PostgreSQL.
6. Adjuntar las capturas recortadas de Jira: roadmap, backlog, sprint, tablero y release.

## Historial de versiones

| Versión | Fecha de edición | Cambio |
|---|---|---|
| 1.0.0 | 2026-10-08 | Informe del Sprint 2 con el formato mostrado en clase. |
