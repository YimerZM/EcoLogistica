# Retrospectiva del sprint — Sprint 2

**Nombre del Proyecto:** EcoLogística — Sistema de Optimización de Rutas Sostenibles

**Líder del Proyecto:** ZEVALLOS MELENDRES YIMER EDYSON

**Sprint:** 2 — Incremento ejecutable del núcleo operativo

**Inicio:** 2026-09-25. **Cierre informado:** 2026-10-08.

**Versión:** 1.0.0. **Fecha de actualización documental:** 2026-10-08.

[Volver al README principal](../../../README.md)

## ¿Qué aprendimos?

La retroalimentación pedía el dato que faltaba, no más páginas: marco del enfoque, radar, objetivos medibles, tipo de geolocalización y la diferencia entre seguridad vial y datos personales. Registrar un pedido tampoco equivale a tener el motor de rutas.

## ¿Qué estamos haciendo bien?

El núcleo ya se puede ejecutar: sesión, vehículo, punto WGS84 y pedido con rechazo de carga prohibida. El tope de USD 10,175.20 coincide en el acta y en el presupuesto.

## ¿Qué podemos hacer mejor?

### Personas

Yimer concentró la integración. Bryan y Josemaria deben revisar su bloque antes del commit, no después de la observación del docente.

### Relaciones

La demostración fue del equipo. Falta el recorrido con el contratante, limitado a la consulta de sus pedidos.

### Procesos

Antes de cada commit documental hay que marcar la consigna. El radar, las claves alternas y el nivel de código del C4 aparecieron recién con la retroalimentación.

### Herramientas

Los documentos quedaron separados por sprint. Falta pegar en el repositorio las capturas recortadas de Jira y usar la clave de la historia en el mensaje de commit.

### Acciones a realizar

| ID | Acción | Responsable | Momento objetivo | Estado | Evidencia de cierre |
|---|---|---|---|---|---|
| S2-ACT-01 | Revisar la consigna antes de cada commit documental | CAJAMALQUI DAVILA JOSEMARIA PIERO | Desde el 2026-10-09 | Pendiente | Mensaje de commit con el ítem cubierto |
| S2-ACT-02 | Ejecutar las pruebas antes de dar por hecha una historia | POMACHAGUA YAPIAS BRYAN ANTONY | En cada incremento | En curso | `python -m unittest tests.test_reglas` |
| S2-ACT-03 | Pegar las cinco capturas recortadas de Jira | ZEVALLOS MELENDRES YIMER EDYSON | Revisión académica | Pendiente | Imágenes solo del panel |
| S2-ACT-04 | Demostrar al contratante la consulta de sus pedidos | ZEVALLOS MELENDRES YIMER EDYSON | 2026-10-15 | Pendiente | Guion de la revisión del Sprint 3 |

## Historial de versiones

| Versión | Fecha de edición | Cambio |
|---|---|---|
| 1.0.0 | 2026-10-08 | Retrospectiva del Sprint 2 con el formato mostrado en clase. |
