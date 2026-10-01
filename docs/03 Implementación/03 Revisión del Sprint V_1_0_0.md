# Revisión del sprint

[← Volver al README Principal](../../README.md)

**Nombre del Proyecto:** EcoLogística – Sistema de Optimización de Rutas Sostenibles

**Líder del Proyecto:** ZEVALLOS MELENDRES YIMER EDYSON

**Sprint:** 2

**Fecha de la revisión:** 01/10/2026

**Asistentes:** ZEVALLOS MELENDRES YIMER EDYSON, POMACHAGUA YAPIAS BRYAN ANTONY, CAJAMALQUI DAVILA JOSEMARIA PIERO. El docente sigue el incremento por el repositorio. El rol de contratante se representó con el guion de consulta, sin una cuenta propia todavía.

## Historias de Usuario completadas en este Sprint

| ID | Como | Resultado demostrado |
|---|---|---|
| US-001 | Operador | Con `operador@ecologistica.test` y la clave de prueba, la sesión se abre. Una clave incorrecta no abre la sesión. Si el bloqueo de 15 minutos ya venció, el contador vuelve a cero al iniciar el intento, antes de validar la clave. |
| US-003 | Operador | Se registra la placa y la capacidad en kilogramos. Una placa repetida se rechaza. |
| US-004 | Operador | Se registra un punto con latitud y longitud. El método guardado es WGS84. Un distrito distinto de El Tambo, Huancayo o Chilca se rechaza. |
| US-005 | Operador | Un pedido de carga general queda en estado PENDIENTE. Un pedido marcado como explosivo o residuo peligroso no se guarda. |

## Demostración del trabajo completado

La demostración se hizo sobre http://127.0.0.1:8765, con el código de `src/frontend` y `src/backend`.

1. Inicio de sesión del operador.
2. Alta del vehículo de prueba.
3. Alta del punto en Huancayo, coordenada -12.07, -75.21, método WGS84.
4. Intento de pedido con tipo explosivo: el sistema muestra el rechazo de RN-016 y la lista de pedidos no crece.
5. Alta de un pedido general: aparece en estado PENDIENTE.

Los interesados de operación y el contratante no operaron la herramienta en esta revisión. El equipo de desarrollo acompañó el recorrido y dejó el guion anterior para la siguiente demostración con ellos.

## Pendientes

- US-002 Gestión de usuarios, incluida la cuenta del contratante.
- US-006 Generación de rutas con capacidad y ventana.
- US-007 Mapa de la ruta.
- US-008 Reoptimización.
- US-009 a US-015 Entregas, indicadores, exportación, auditoría y parámetros.
- Pasar la API de este incremento, hoy en la biblioteca estándar de Python, a FastAPI, que sigue siendo el stack elegido.
- Sustituir el almacén en memoria por PostgreSQL, según el modelo lógico ya corregido.

## Control de cambios

| Versión | Fecha | Descripción | Responsable |
|---|---|---|---|
| 1.0.0 | 01/10/2026 | Revisión del Sprint 2. | ZEVALLOS MELENDRES YIMER EDYSON |
