# Informe de reducción del impacto ambiental

**Proyecto:** EcoLogística — Sistema de Optimización de Rutas Sostenibles  
**Equipo:** Híbridos — Zevallos Melendres, Yimer Edyson; Pomachagua Yapias, Bryan Antony; Cajamalqui Dávila, Josemaría Piero  
**Versión:** 1.0.0  
**Fecha:** 2026-11-12  
**Stack en ejecución:** Python (biblioteca estándar) y página HTML, CSS y JavaScript  

[Volver al README principal](../../../README.md)

La plantilla de referencia describe un sistema MERN con MongoDB, Express, React y Node. EcoLogística no usa ese stack. Este informe mide lo que el repositorio sí ejecuta: el CO₂ de las rutas en El Tambo, Huancayo y Chilca, y el peso de la página que se transfiere al navegador.

## 1.1 Propósito

1. Medir el CO₂ estimado de una ruta frente a tres viajes separados.
2. Medir el peso real de la página y su emisión digital por visita.
3. Dejar por escrito qué no se midió, para no presentar una cifra de otro sistema.

## 1.2 Dos impactos distintos

| Impacto | Qué mide | Fórmula de este proyecto |
|---|---|---|
| Operativo | El recorrido del vehículo | kilómetros × 0.21 kg CO₂/km |
| Digital | Lo que descarga el navegador | GB × 0.815 kWh/GB × 442 g CO₂e/kWh |

El factor 0.21 kg CO₂/km es un parámetro del sistema. El administrador puede cambiarlo. No es una medición del tubo de escape.

## 1.3 Ruta de demostración

Puntos cargados por el botón de demostración:

| Parada | Distrito | Coordenada WGS84 | Peso |
|---|---|---|---:|
| Base | Huancayo | -12.068, -75.210 | — |
| Parque Constitución | El Tambo | -12.05, -75.23 | 18 kg |
| Mercado Modelo | Huancayo | -12.07, -75.21 | 12 kg |
| Plaza de Chilca | Chilca | -12.12, -75.20 | 22 kg |

El vehículo ECO-101 tiene 800 kg. Los 52 kg caben en un solo viaje. La propuesta ordena las paradas de norte a sur.

| Escenario | Recorrido | CO₂ estimado |
|---|---:|---:|
| Tres viajes de ida y vuelta, uno por parada | 18.12 km | 3.81 kg |
| Una ruta que visita las tres paradas y regresa a la base | 17.61 km | 3.70 kg |
| Lo que muestra la página (la ruta, sin el regreso a la base) | 11.73 km | 2.46 kg |

La página muestra **11.73 km** y **2.46 kg de CO₂** porque la propuesta no suma el regreso. Si el vehículo también regresa, el ahorro frente a tres idas y vueltas es **0.51 km** y **0.11 kg de CO₂**.

Un pedido explosivo o de residuo peligroso no entra en esta cuenta: la regla RN-016 lo rechaza y no se guarda.

## 1.4 Peso de la página

Archivos medidos en `src/frontend` el 2026-11-12:

| Archivo | Bytes |
|---|---:|
| `index.html` | 10,045 |
| `css/estilos.css` | 5,892 |
| `js/app.js` | 17,551 |
| Total | 33,488 |

Eso es 0.032 MB. Con el modelo de la plantilla:

`33,488 bytes = 0.0000312 GB × 0.815 kWh/GB × 442 g CO₂e/kWh = 0.011 g CO₂e por carga de la página.`

La primera carga pide 3 archivos. El mapa es un SVG dentro de la página: no descarga teselas ni fotografías. No hay `node_modules` ni un bundle de React.

No se ejecutó Lighthouse. Este informe no copia los puntajes 38/100 ni 96/100 de la plantilla MERN, ni el peso de 8.4 MB, ni la proyección de 500,000 visitas.

## 1.5 Dónde se ve en la página

1. Entrar como operador.
2. Pulsar **Preparar datos de El Tambo, Huancayo y Chilca**.
3. Abrir **Rutas** y pulsar **Generar ruta**.
4. Abrir **Indicadores**, periodo **Todo el registro**, y pulsar **Calcular**.
5. Leer **Recorrido (km)** y **CO₂ (kg)**.

## Historial de versiones

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0.0 | 2026-11-12 | Informe con las cifras de EcoLogística. La plantilla MERN queda como formato, no como medición. |
