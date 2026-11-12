# Estándares de ingeniería de software y desarrollo verde

**Proyecto:** EcoLogística — Sistema de Optimización de Rutas Sostenibles  
**Equipo:** Híbridos  
**Versión:** 1.0.0  
**Fecha:** 2026-11-12  

[Volver al README principal](../../../README.md)

Estos estándares se aplican al código que está en `src/backend` y `src/frontend`. No describen MongoDB, Express ni React, porque ese stack no está en ejecución.

## 2.1 Estándares usados

### ISO/IEC 25010

La eficiencia de desempeño, en este incremento, es el tiempo de responder en local y el tamaño de lo que viaja al navegador. La mantenibilidad es separar reglas (`reglas.py`), casos de uso (`servicio.py`) y la página.

### Green Software Foundation

Se reduce el cómputo por visita: una página de 33 KB, sin imágenes y sin librerías de terceros. El CO₂ operativo se calcula solo cuando la ruta tiene kilómetros. Si no hay datos, el sistema lo dice y no inventa el indicador.

### W3C Web Sustainability Guidelines

La interfaz no pide fotografías. El mapa va dibujado en la misma página. Cada lista de la API trae los campos que la pantalla muestra, y la clave no sale en esa lista.

## 2.2 Ocho decisiones ya aplicadas

| # | Decisión en EcoLogística | Efecto |
|---|---|---|
| 1 | La lista de usuarios no incluye el hash de la clave | Menos datos personales y menos bytes |
| 2 | El contratante solo recibe sus pedidos y el conductor solo sus rutas | El listado no descarga toda la operación |
| 3 | El mapa es SVG, no un servicio de teselas | Cero imágenes de mapa |
| 4 | Una sola página HTML, paneles ocultos según el rol | No hay un bundle por pantalla |
| 5 | Python de biblioteca estándar y JavaScript del navegador | No hay `node_modules` |
| 6 | No hay archivos PNG ni JPEG en `src/frontend` | La primera carga son 3 archivos |
| 7 | El CO₂ usa solo rutas activas que ya tienen kilómetros | Cumple RN-013 |
| 8 | Tres entregas que caben en un vehículo salen en una ruta | Se evita repetir la salida de la base |

## 2.3 Mapeo

| # | Decisión | ISO/IEC 25010 | Green Software | W3C WSG |
|---|---|---|---|---|
| 1 | Campos públicos del usuario | Seguridad y eficiencia | Menos datos transferidos | Red |
| 2 | Filtro por rol | Eficiencia de capacidad | Energía por consulta | Eficiencia de la interfaz |
| 3 | Mapa SVG | Comportamiento temporal | Carbono de red | Medios |
| 4 | Una página | Mantenibilidad | Hardware del cliente | Arquitectura |
| 5 | Sin dependencias npm | Analizabilidad | Energía del toolchain | Librerías |
| 6 | Sin imágenes | Comportamiento temporal | Carbono | Medios |
| 7 | CO₂ solo con recorrido | Correctitud funcional | Intensidad de carbono medible | Datos |
| 8 | Una ruta para tres paradas | Eficiencia | Carbono operativo | Tarea del usuario |

## 2.4 Lo que esta versión no afirma

No hay compresión Brotli, no hay cabecera `Cache-Control` y no hay un workflow de Lighthouse en GitHub Actions. Esas prácticas quedan como siguiente paso, no como trabajo ya medido.

## Historial de versiones

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0.0 | 2026-11-12 | Estándares aplicados al incremento Python de EcoLogística. |
