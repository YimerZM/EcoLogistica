# Plan de trabajo

**Proyecto:** EcoLogística — Sistema de Optimización de Rutas Sostenibles  
**Equipo:** Híbridos  
**NRC:** 30142 — Taller de Proyectos 2  
**Fecha:** 2026-11-19  
**Repositorio:** https://github.com/YimerZM/EcoLogistica

[Volver al README principal](../../README.md)

## 1. Base que se mantiene

| Entrega | Resultado que se mantiene |
|---|---|
| Sprint 1 | US-001, US-003, US-004 y US-005 especificadas. |
| Sprint 2 | Esas cuatro historias ejecutables: sesión, vehículo, punto WGS84 y pedido. |
| Sprint 3 | US-002 usuarios y US-006 propuesta de ruta. La página en ejecución también cubre RF-001 a RF-015. |
| Inspección 3 | Artefactos del 2026-11-05 en `docs/04 Inspección 3`. |
| Inspección 4 | Artefactos del 2026-11-12 en `docs/05 Inspección 4`. |
| Impacto ambiental | Informe y estándares en `docs/03 Implementación/reduccion del impacto ambiental`. |

La base publicada antes de esta inspección es el commit `eeaa96e`.

## 2. Trabajo de esta inspección

| Orden | Artefacto | Responsable | Fecha |
|---|---|---|---|
| 01 | Plan de trabajo | Zevallos Melendres, Yimer Edyson | 2026-11-19 |
| 02.1 | Flujo de trabajo GitFlow | Zevallos Melendres, Yimer Edyson | 2026-11-19 |
| 02.2 | Pruebas de sistema | Zevallos Melendres, Yimer Edyson | 2026-11-19 |
| 02.3 | Pruebas de extremo a extremo | Zevallos Melendres, Yimer Edyson | 2026-11-19 |
| 02.4 | Sincronización del repositorio remoto | Zevallos Melendres, Yimer Edyson | 2026-11-19 |
| 02.5 | Demostración del incremento — Sprint 3 | Zevallos Melendres, Yimer Edyson | 2026-11-19 |
| 03.1 | Minuta de reunión | Zevallos Melendres, Yimer Edyson | 2026-11-19 |
| 03.2 | Informe de estado del proyecto | Zevallos Melendres, Yimer Edyson | 2026-11-19 |
| 03.3 | Registro de impedimentos | Zevallos Melendres, Yimer Edyson | 2026-11-19 |
| 04.1 | Revisión del sprint | Zevallos Melendres, Yimer Edyson | 2026-11-19 |
| 04.2 | Retrospectiva del sprint | Zevallos Melendres, Yimer Edyson | 2026-11-19 |

## 3. Consolidado 2

Esta inspección acompaña el software completo y el informe completo.

| Pieza | Dónde está |
|---|---|
| Software | `src/frontend` y `src/backend`. Se enciende con `python -m ecologistica`. |
| Archivo de ayuda | `src/frontend/ayuda.html`. También se abre desde el ingreso y desde el menú Ayuda. |
| Informe completo | `docs/07 Consolidado 2/20261119 Informe completo.md`. |

## 4. Presentación

La fecha y la hora las marca el cronograma del NRC 30142. Este plan no las reemplaza.

## 5. Siguiente historia

La próxima historia sale de `develop` con `git flow feature start US-008`. No se escribe directo en `main` y no se usa `push --force`.
