# Retrospectiva del sprint

La versión vigente de los sprints está en [Sprint 1](Sprint_1/04%20Retrospectiva%20del%20Sprint%20V_1_0_0.md) y [Sprint 2](Sprint_2/04%20Retrospectiva%20del%20Sprint%20V_1_0_0.md).

[← Volver al README Principal](../../README.md)

**Nombre del Proyecto:** EcoLogística – Sistema de Optimización de Rutas Sostenibles

**Líder del Proyecto:** ZEVALLOS MELENDRES YIMER EDYSON

**Sprint:** 2

**Fecha:** 01/10/2026

## ¿Qué aprendimos?

La retroalimentación no pedía más páginas. Pedía el dato que faltaba: marco del enfoque, radar, objetivos medibles, tipo de geolocalización, rol del contratante y la diferencia entre seguridad vial y datos personales. Escribir de más ocultó esos huecos.

## ¿Qué estamos haciendo bien?

El equipo mantuvo un solo ámbito, El Tambo, Huancayo y Chilca, desde el acta hasta el rechazo de coordenadas fuera de esa zona. El presupuesto de USD 10,175.20 del acta y el de planificación coinciden.

## ¿Qué podemos hacer mejor?

### Personas

ZEVALLOS concentró la integración de los documentos. POMACHAGUA y CAJAMALQUI revisaron por bloques, pero la primera versión salió con campos vacíos porque nadie tenía la lista de cierre antes de entregar.

### Relaciones

La revisión se hizo entre el equipo. El contratante y el responsable de operaciones no estuvieron en la demostración. El registro de interesados ya dice que ellos participan según su interés y que el equipo los acompaña; en este sprint ese acompañamiento no ocurrió fuera del equipo.

### Procesos

No hubo una lista de verificación contra la consigna antes del commit. Por eso el radar, las claves alternas y el nivel de código del C4 aparecieron recién con la retroalimentación.

### Herramientas

El repositorio solo tenía Markdown. Sin carpetas de código ni `.gitignore`, el Sprint 2 no podía demostrar historias. Mermaid se usó tarde para el radar.

### Acciones a realizar

| Acción | Responsable | Fecha |
|---|---|---|
| Antes de cada commit documental, recorrer la consigna y marcar el ítem en el mensaje de commit. | CAJAMALQUI DAVILA JOSEMARIA PIERO | Desde el 02/10/2026 |
| Asignar dueño por documento: enfoque y stack a POMACHAGUA; interesados, usuarios y reglas a CAJAMALQUI; acta, visión y presupuesto a ZEVALLOS. | ZEVALLOS MELENDRES YIMER EDYSON | 03/10/2026 |
| Ejecutar `python -m unittest` en `src/backend` antes de dar por hecha una historia. | POMACHAGUA YAPIAS BRYAN ANTONY | En cada incremento |
| Agendar la revisión del Sprint 3 con un guion para el contratante, aunque sea representado, y mostrarle solo la consulta de sus pedidos. | ZEVALLOS MELENDRES YIMER EDYSON | 15/10/2026 |

## Control de cambios

| Versión | Fecha | Descripción | Responsable |
|---|---|---|---|
| 1.0.0 | 01/10/2026 | Retrospectiva del Sprint 2. | ZEVALLOS MELENDRES YIMER EDYSON |
