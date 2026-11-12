# Informe de reducción del impacto ambiental

**Proyecto:** EcoLogística — Sistema de Optimización de Rutas Sostenibles  
**Equipo:** Híbridos — Zevallos Melendres, Yimer Edyson; Pomachagua Yapias, Bryan Antony; Cajamalqui Dávila, Josemaría Piero  
**Curso:** Taller de Proyectos 2 — NRC 30142  
**Versión del informe:** 1.2.0  
**Fecha de medición:** 2026-11-12  
**Stack medido:** Python de biblioteca estándar, página HTML, CSS y JavaScript del navegador  

[Volver al README principal](../../../README.md)

| Sección | Contenido |
|---|---|
| 1.1 a 1.3 | Propósito, alcance y las dos fórmulas |
| 1.4 a 1.6 | Haversine, datos de demostración y los tres escenarios kilómetro a kilómetro |
| 1.7 a 1.8 | Ocho decisiones y el CO₂e de la página |
| 1.9 a 1.11 | Cómo leer la pantalla, límites y cifras orales |
| 1.12 a 1.15 | Cupo insuficiente, sensibilidad del factor, entregas y periodo |
| 1.16 a 1.18 | Procedimiento de los bytes, interpretación y conclusiones |

## 1.1 Introducción y propósito

EcoLogística planifica entregas de carga general en El Tambo, Huancayo y Chilca. El impacto ambiental de ese trabajo tiene dos partes, y este informe las mide por separado.

La primera parte es operativa. Un vehículo que sale de la base, visita un solo punto y regresa, y luego repite el viaje por cada pedido, recorre más kilómetros que un vehículo que sale una vez y visita las paradas en un solo recorrido. Cada kilómetro de más se convierte en kilogramos de CO₂ con el factor que el sistema guarda.

La segunda parte es digital. La página que usa el operador también consume energía: el navegador descarga HTML, CSS y JavaScript, y el equipo del usuario los interpreta. Esa emisión se calcula con el modelo Sustainable Web Design (SWDM) a partir del peso real de los archivos, no a partir de un puntaje de otra aplicación.

El propósito de este informe es:

1. Dejar escrita la fórmula de cada impacto y la unidad en la que se expresa.
2. Recorrer la ruta de demostración tramo por tramo, con la distancia de cada pierna.
3. Comparar tres escenarios de la misma carga: tres idas y vueltas, una ruta con regreso a la base, y la cifra que muestra la página.
4. Documentar las ocho decisiones de diseño que reducen kilómetros o bytes.
5. Mostrar el cálculo digital byte por byte, desde el tamaño del archivo hasta los gramos de CO₂e.
6. Decir con precisión qué cifra puede leerse en la pantalla y cuál exige el regreso a la base para ser comparable.

La plantilla de referencia del curso describe un sistema MongoDB, Express, React y Node, con una auditoría Lighthouse de 38/100 a 96/100, un peso de 8.4 MB y una proyección de 500,000 visitas. EcoLogística no usa ese stack y no ejecutó Lighthouse. Esas cifras no se copian. Las tablas de este informe salen del código que está en `src/backend` y del peso de `src/frontend` medido el 2026-11-12.

## 1.2 Alcance de la medición

| Elemento | Qué entra en este informe |
|---|---|
| Territorio | El Tambo, Huancayo y Chilca. Coordenadas WGS84 dentro de la caja latitud -12.20 a -11.90 y longitud -75.40 a -75.00 (RN-014). |
| Carga | Solo carga `GENERAL`. El explosivo y el residuo peligroso se rechazan y no generan kilómetros (RN-016). |
| Vehículo de la demostración | ECO-101, capacidad 800 kg, conductor `conductor@ecologistica.test`. ECO-202 queda disponible y no se usa porque los 52 kg caben en el primero. |
| Base de salida | -12.068, -75.210. Es el origen fijo de `_km` en `servicio.py`. No es un punto registrado por el usuario. |
| Unidad operativa | Kilómetros de la propuesta y kilogramos de CO₂ estimados. |
| Unidad digital | Gramos de CO₂e de una carga de la página (los tres archivos estáticos). |
| Fecha | 2026-11-12. Los bytes se leyeron del disco en esa fecha. |

Queda fuera de la medición, y por eso no aparece como resultado:

- El tubo de escape real del vehículo. El factor 0.21 kg CO₂/km es un parámetro, no una sonda.
- El regreso a la base dentro del número que pinta la página. La función `_km` suma la base y las paradas, y se detiene en la última parada.
- PostgreSQL, FastAPI, teselas de mapa, fotografías y un empaquetador de JavaScript. No están en ejecución, así que no tienen peso que medir.
- Una proyección anual de visitas. El equipo no tiene un contador de tráfico de producción. Inventar 500,000 visitas produciría un kilogramo anual que este repositorio no puede sostener.
- Puntajes Lighthouse (FCP, LCP, TBT, CLS). No se corrió esa auditoría.

## 1.3 Dos impactos y sus fórmulas

### Impacto operativo

```
CO₂ (kg) = kilómetros de las rutas activas × factor_emision_kg_por_km
```

El factor de fábrica es **0.21 kg CO₂/km**. Vive en `parametros` del servicio. El administrador puede cambiarlo desde la pantalla Parámetros. El sistema rechaza un factor menor o igual a cero. El indicador solo suma rutas con estado `ACTIVA` que ya traen el campo `km`. Si el periodo viene vacío, o si no hay pedidos ni rutas en el periodo, la respuesta es «No existen datos para realizar el cálculo.» Esa es la regla RN-013: no se calcula con datos insuficientes.

### Impacto digital

El modelo SWDM usado por la plantilla del curso es:

```
gramos CO₂e = gigabytes transferidos × 0.815 kWh/GB × 442 g CO₂e/kWh
```

| Constante | Valor | Qué representa |
|---|---:|---|
| Intensidad energética de la red | 0.815 kWh/GB | Energía atribuida a mover un gigabyte (dato centro, red y dispositivo, según el modelo de la plantilla). |
| Intensidad de carbono de la electricidad | 442 g CO₂e/kWh | Gramos por cada kilovatio-hora. Es el factor de la plantilla, aplicado aquí al peso medido. |
| Conversión a GB | byte / 1,073,741,824 | 1 GB = 1024³ bytes. |

La página no mezcla estas dos fórmulas. Los 2.46 kg de la ruta y los 0.011 g de la visita responden preguntas distintas. Sumarlos ocultaría que el recorrido del vehículo pesa varios órdenes de magnitud más que la descarga de la página.

## 1.4 Cómo se obtiene cada kilómetro

La distancia entre dos coordenadas es la fórmula de haversine, con radio terrestre de 6,371 km. Está en `_distancia_km`:

```
a = sen²(Δlat/2) + cos(lat1) × cos(lat2) × sen²(Δlon/2)
distancia = 2 × 6371 × arcsen(√a)
```

Las latitudes y longitudes entran en radianes. El resultado de cada pierna es un número sin redondear. `_km` suma las piernas y redondea el total a dos decimales. `indicadores` vuelve a redondear la suma de kilómetros y el CO₂ a dos decimales. Por eso una cuenta hecha a mano con más decimales puede diferir en la centésima: la cifra que vale en la sustentación es la que redondea el sistema.

La ruta de la página se arma así:

1. Se toman solo vehículos `DISPONIBLE` y pedidos `PENDIENTE`.
2. Las paradas se ordenan de norte a sur: latitud de mayor a menor (menos negativa primero), y a igual latitud por longitud y por identificador.
3. Cada pedido entra al primer vehículo cuyo cupo restante alcanza el peso. Si ninguno alcanza, el pedido queda en `sin_cupo` y sigue `PENDIENTE`.
4. Los kilómetros salen de la base, en el orden ya decidido, hasta la última parada. El tramo de vuelta a la base no se suma.

## 1.5 Datos de la demostración

El botón **Preparar datos de El Tambo, Huancayo y Chilca** llama a `cargar_ejemplo`. Si ECO-101 ya existe, no duplica los datos.

| Pieza | Valor |
|---|---|
| Vehículo usado | ECO-101, 800 kg, estado inicial DISPONIBLE |
| Vehículo que no sale | ECO-202, 450 kg. El primer vehículo todavía tiene cupo, así que el algoritmo no lo abre. |
| Pedido El Tambo | 18 kg, GENERAL, Parque Constitución |
| Pedido Huancayo | 12 kg, GENERAL, Mercado Modelo |
| Pedido Chilca | 22 kg, GENERAL, Plaza de Chilca |
| Peso total | 52 kg. Cabe en ECO-101 (800 − 52 = 748 kg libres). |
| Carga que no entra en la cuenta | Un pedido explosivo o de residuo peligroso. RN-016 lo rechaza antes de persistirlo. |

| Orden de visita | Parada | Distrito | Latitud | Longitud | Peso |
|---:|---|---|---:|---:|---:|
| 0 | Base de salida | Huancayo | -12.068 | -75.210 | — |
| 1 | Parque Constitución | El Tambo | -12.050 | -75.230 | 18 kg |
| 2 | Mercado Modelo | Huancayo | -12.070 | -75.210 | 12 kg |
| 3 | Plaza de Chilca | Chilca | -12.120 | -75.200 | 22 kg |

El Tambo queda al norte (-12.050), el Mercado Modelo en el medio (-12.070) y Chilca al sur (-12.120). Ese es el orden norte-sur. Después de generar, los tres pedidos y el vehículo pasan a `EN_RUTA` y la ruta queda `ACTIVA`.

## 1.6 Distancias tramo a tramo

Distancias haversine sin redondear, calculadas con el mismo radio de 6,371 km:

| Tramo | Kilómetros |
|---|---:|
| Base → Parque Constitución | 2.9557 |
| Parque Constitución → Mercado Modelo | 3.1106 |
| Mercado Modelo → Plaza de Chilca | 5.6651 |
| Plaza de Chilca → Base | 5.8835 |
| Base → Mercado Modelo (viaje directo) | 0.2224 |
| Base → Plaza de Chilca (viaje directo) | 5.8835 |

El Mercado Modelo está a 222 metros de la base. Por eso un viaje dedicado a ese punto casi no pesa, y cualquier desvío hacia El Tambo se nota en la suma.

### Escenario A. Tres viajes de ida y vuelta

Cada pedido sale de la base y el vehículo regresa antes del siguiente pedido.

| Viaje | Ida y vuelta | CO₂ a 0.21 kg/km |
|---|---:|---:|
| Base ↔ Parque Constitución | 2 × 2.9557 = 5.9114 km | 1.241 kg |
| Base ↔ Mercado Modelo | 2 × 0.2224 = 0.4448 km | 0.093 kg |
| Base ↔ Plaza de Chilca | 2 × 5.8835 = 11.7670 km | 2.471 kg |
| **Suma sin redondear** | **18.1232 km** | **3.806 kg** |
| **Cifra de trabajo (km redondeados × 0.21)** | **18.12 km** | **3.81 kg** |

18.12 × 0.21 = 3.8052, que el redondeo a dos decimales deja en **3.81 kg**.

### Escenario B. Una ruta con regreso a la base

Es la comparación justa: el vehículo también vuelve al patio.

| Tramo | Kilómetros |
|---|---:|
| Base → Parque Constitución | 2.9557 |
| Parque Constitución → Mercado Modelo | 3.1106 |
| Mercado Modelo → Plaza de Chilca | 5.6651 |
| Plaza de Chilca → Base | 5.8835 |
| **Suma sin redondear** | **17.6149 km** |
| **Cifra de trabajo** | **17.61 km → 3.70 kg** |

17.61 × 0.21 = 3.6981, que redondea a **3.70 kg**.

Ahorro del escenario B frente al A:

```
18.12 − 17.61 = 0.51 km
3.81 − 3.70 = 0.11 kg de CO₂
```

El ahorro es pequeño y hay que poder explicarlo. Consolidar evita dos regresos (el de El Tambo y el del Mercado). Al mismo tiempo, el orden norte-sur obliga a subir primero a El Tambo y después bajar al Mercado, un tramo de 3.11 km, cuando el Mercado por sí solo está a 0.22 km de la base. El desvío se come casi todo el ahorro de los regresos. En esta demostración la consolidación sigue siendo menor, pero no es un recorte grande. Decir que se ahorran varios kilogramos con estos tres puntos sería falso.

### Escenario C. Lo que muestra la página

`_km` no suma la vuelta. La página y el indicador usan este recorrido:

| Tramo | Kilómetros |
|---|---:|
| Base → Parque Constitución | 2.9557 |
| Parque Constitución → Mercado Modelo | 3.1106 |
| Mercado Modelo → Plaza de Chilca | 5.6651 |
| **Suma sin redondear** | **11.7314 km** |
| **Cifra en pantalla** | **11.73 km → 2.46 kg** |

11.73 × 0.21 = 2.4633, que redondea a **2.46 kg**.

Esa cifra es correcta como longitud de la propuesta. No es correcta como ahorro frente a los tres viajes, porque los tres viajes sí incluyen la vuelta y la pantalla no. Si en la sustentación se compara 2.46 kg contra 3.81 kg, hay que decir en la misma frase que faltan los 5.88 km de Chilca a la base. La comparación cerrada es 3.70 kg contra 3.81 kg.

### Tabla de los tres escenarios

| Escenario | Qué incluye | km | CO₂ (kg) |
|---|---|---:|---:|
| A. Tres idas y vueltas | Ida y regreso de cada parada | 18.12 | 3.81 |
| B. Una ruta y regreso a la base | Las tres paradas y la vuelta desde Chilca | 17.61 | 3.70 |
| C. Lectura de la página | Las tres paradas, sin la vuelta | 11.73 | 2.46 |
| Ahorro comparable (A − B) | Misma condición de regreso | 0.51 | 0.11 |

## 1.7 Las ocho decisiones y su efecto

Cada decisión está en el código de este repositorio. El efecto se expresa en kilómetros, en bytes o en datos que dejan de viajar. No se inventa un porcentaje de Lighthouse.

### 1. Un vehículo para los pedidos que caben

**Situación de partida.** Sin propuesta, cada pedido pendiente es un motivo para sacar un vehículo.

**Qué hace el sistema.** `propuesta_de_ruta` recorre los pedidos ya ordenados y los asigna al primer vehículo `DISPONIBLE` con cupo. En la demostración, 18 + 12 + 22 = 52 kg entran en ECO-101. ECO-202 no se mueve. Los pedidos asignados pasan a `EN_RUTA`.

**Efecto.** Se evita abrir un segundo vehículo para 52 kg. Si un pedido no cabe, no se parte ni se fuerza: queda en `sin_cupo`, sigue `PENDIENTE` y el mensaje es «Propuesta generada. No hubo capacidad para todos los pedidos.»

### 2. Paradas de norte a sur

**Situación de partida.** Un orden al azar puede cruzar el valle dos veces.

**Qué hace el sistema.** La clave de orden es la latitud descendente, luego la longitud y el identificador. En la demostración el orden queda El Tambo, Mercado Modelo, Chilca.

**Efecto.** El recorrido de la pantalla mide 11.73 km en ese orden. El informe no afirma que ese orden sea el óptimo matemático del viajante. Afirma el orden que el código produce y los kilómetros que ese orden mide. La reoptimización solo corre si ya existe una ruta `ACTIVA` y hubo un cambio operativo; si no, se niega y no se recalcula en vacío.

### 3. El CO₂ solo cuando la ruta ya tiene kilómetros

**Situación de partida.** Un indicador calculado sin recorrido mostraría un cero que parece una medición.

**Qué hace el sistema.** `indicadores` suma `km` de las rutas `ACTIVA`. El CO₂ es esa suma por el factor. El periodo `vacio` responde que no existen datos. El contratante recibe sus pedidos y una lista de rutas vacía: no ve el CO₂ de la flota.

**Efecto.** Se cumple RN-013. La pantalla de Indicadores, con periodo **Todo el registro**, muestra 11.73 km y 2.46 kg después de generar la ruta de demostración.

### 4. La carga peligrosa no entra en el recorrido

**Situación de partida.** Un pedido explosivo o de residuo peligroso, si se guardara, sumaría kilómetros y CO₂ de un traslado que la regla prohíbe.

**Qué hace el sistema.** `carga_prohibida` acepta solo el texto `general`. Cualquier otro tipo se rechaza y no se persiste. El pedido no nace, no pasa a `PENDIENTE` y no puede entrar en `propuesta_de_ruta`.

**Efecto.** RN-016 saca de la cuenta ambiental una operación que no debe existir. Los 2.46 kg de la demostración son solo de los tres pedidos GENERAL.

### 5. El mapa es un dibujo en la misma página

**Situación de partida.** Un mapa de teselas descarga decenas de imágenes PNG por cada movimiento del usuario. Cada imagen es una petición HTTP y un peso que el modelo SWDM convierte en gramos.

**Qué hace el sistema.** La vista de rutas dibuja un SVG. La proyección es lineal sobre la caja de los tres distritos: la longitud -75.40 a -75.00 se reparte en 1,000 unidades y la latitud -11.90 a -12.20 se reparte en 640. No hay Leaflet, no hay teselas y no hay clave de un proveedor de mapas.

**Efecto.** El mapa no añade un archivo al peso de 33,488 bytes. La primera carga sigue siendo tres peticiones: `index.html`, `css/estilos.css` y `js/app.js`.

### 6. Una sola página y tres archivos

**Situación de partida.** Una aplicación con una pantalla por archivo, o con un paquete distinto por rol, transfiere código que el usuario de ese momento no va a ejecutar.

**Qué hace el sistema.** Hay un `index.html`. Los paneles (inicio, usuarios, vehículos, puntos, pedidos, rutas, entregas, indicadores, parámetros, auditoría) están en esa página y se muestran según el rol. La tipografía es Palatino y Segoe UI, ya instaladas en el equipo. No hay descarga de fuentes web.

**Efecto.** Peso medido el 2026-11-12:

| Archivo | Bytes | Parte del total |
|---|---:|---:|
| `src/frontend/index.html` | 10,045 | 30.0 % |
| `src/frontend/css/estilos.css` | 5,892 | 17.6 % |
| `src/frontend/js/app.js` | 17,551 | 52.4 % |
| **Total** | **33,488** | **100 %** |

33,488 bytes son 0.032 MB.

### 7. Biblioteca estándar, sin dependencias de terceros

**Situación de partida.** Un empaquetador y una carpeta `node_modules` añaden librerías al artefacto que el navegador termina descargando, aunque la pantalla use una función.

**Qué hace el sistema.** El servidor es `ThreadingHTTPServer` de la biblioteca estándar. El cálculo, la sesión y las reglas están en `reglas.py`, `servicio.py` y `servidor.py`. El navegador ejecuta el JavaScript de `app.js` sin React, sin moment y sin lodash. En `src/frontend` no hay archivos PNG, JPEG, WEBP ni AVIF.

**Efecto.** No existe un bundle que medir aparte de los 17,551 bytes de `app.js`. La instalación del proyecto no descarga un árbol de paquetes para levantar la página.

### 8. Cada rol recibe solo la lista que le corresponde

**Situación de partida.** Devolver todos los pedidos, todas las rutas y el hash de la clave en cada consulta transfiere bytes y datos personales que la pantalla no pinta.

**Qué hace el sistema.** `_publico` devuelve correo, nombre, rol y estado. El hash de la clave no sale en esa lista. El contratante solo recibe pedidos con su correo. El conductor solo recibe las rutas donde su correo figura como conductor, y los pedidos de esas rutas. Quien no tiene sesión recibe 401. Quien no tiene el rol recibe 403.

**Efecto.** La lista de usuarios de la demostración viaja sin el campo `password_hash`. El indicador de flota no viaja al contratante. El filtro es la forma de paginación que este incremento sí tiene: se recorta por permiso, no por un parámetro `page` que el código no implementa.

## 1.8 Cálculo digital, paso a paso

Peso medido: **33,488 bytes**.

```
GB = 33,488 / 1,073,741,824 = 0.000031188 GB
kWh = 0.000031188 × 0.815 = 0.000025418 kWh
g CO₂e = 0.000025418 × 442 = 0.0112 g CO₂e
```

Redondeado a milésimas de gramo: **0.011 g CO₂e por carga de la página**.

Esa carga es la primera visita, cuando el navegador pide los tres archivos. Una recarga posterior puede usar la caché del propio navegador. El servidor de este incremento no envía `Cache-Control` ni comprime con Brotli, así que este informe cuenta la visita como si los 33,488 bytes viajaran completos. Es el caso más alto, no el más optimista.

Para situar el orden de magnitud frente al recorrido:

| Fuente | Emisión de la demostración | Relación |
|---|---:|---|
| Página, una visita | 0.011 g CO₂e | 1 |
| Ruta en pantalla (11.73 km) | 2,460 g (2.46 kg) | unas 220,000 visitas de la página |
| Ruta con regreso (17.61 km) | 3,700 g (3.70 kg) | unas 330,000 visitas de la página |

En este producto, el kilómetro del vehículo domina la huella. Adelgazar la página es la parte digital del estándar. La parte que mueve decenas de gramos, y no milésimas, es dejar de repetir la salida de la base.

## 1.9 Lectura en la pantalla

Para obtener los 11.73 km y los 2.46 kg:

1. Arrancar el servidor desde `src/backend` con `python -m ecologistica`.
2. Abrir `http://127.0.0.1:8765`.
3. Entrar como operador (`operador@ecologistica.test`).
4. En Inicio, pulsar **Preparar datos de El Tambo, Huancayo y Chilca**.
5. Abrir **Rutas** y pulsar **Generar ruta**. La ruta queda ACTIVA, con 52 kg de 800 y 11.73 km.
6. Abrir **Indicadores**, periodo **Todo el registro**, y pulsar **Calcular**.
7. Leer **Recorrido (km)** = 11.73 y **CO₂ (kg)** = 2.46. El factor mostrado es 0.21.

El contratante no ve ese CO₂ de flota. Un pedido de tipo explosivo, intentado antes de generar, no aumenta ni los kilómetros ni los kilogramos.

## 1.10 Límites que la sustentación debe decir

1. **11.73 km no incluye el regreso.** La comparación con tres idas y vueltas usa 17.61 km y 3.70 kg, y el ahorro es 0.51 km y 0.11 kg.
2. **0.21 no es una medición de escape.** Es el parámetro del sistema. Si el administrador lo cambia, el CO₂ de la pantalla cambia con él y los kilómetros no.
3. **0.011 g es la página, no la flota.** Sale de 33,488 bytes y de las dos constantes de la plantilla.
4. **No hay puntaje Lighthouse.** No se publican 38/100, 96/100, 8.4 MB, 2.15 g por visita, 500,000 visitas ni 935 kg al año. Esos números pertenecen a la plantilla MERN.
5. **El mapa no es el GPS del vehículo.** Es un esquema de los tres distritos. No hay posición en tiempo real.
6. **La persistencia de esta versión es memoria del proceso.** Al cerrar el servidor, la ruta de demostración se pierde. La medición se repite cargando de nuevo el ejemplo.

## 1.11 Cifras para decir en voz alta

- Tres viajes separados: **18.12 km** y **3.81 kg** de CO₂.
- La misma carga en una ruta, contando la vuelta a la base: **17.61 km** y **3.70 kg**.
- Ahorro con la vuelta incluida: **0.51 km** y **0.11 kg**.
- Lo que enseña Indicadores: **11.73 km** y **2.46 kg**, sin la vuelta.
- La página pesa **33,488 bytes**, unos **0.011 g CO₂e** por visita.
- La carga que no es general no entra en ninguna de esas cuentas.

## 1.12 Segundo caso: el pedido que no cabe no suma kilómetros

La prueba `test_la_propuesta_ordena_paradas_y_respeta_la_capacidad` arma un caso distinto al de la demostración. Hay un solo vehículo, ABC-123, con 40 kg. Hay dos pedidos GENERAL:

| Pedido | Punto | Coordenada | Peso | Qué hace la propuesta |
|---|---|---|---:|---|
| Norte | Tambo, El Tambo | -12.00, -75.22 | 20 kg | Entra. El Tambo está más al norte y 20 kg caben en 40 kg. |
| Sur | Chilca, Chilca | -12.15, -75.20 | 30 kg | No entra. Después de descontar 20 kg quedan 20 kg, y 30 no caben. Sigue PENDIENTE y aparece en `sin_cupo`. |

La ruta que se guarda tiene una sola parada. Con la misma base (-12.068, -75.210) y la misma fórmula:

| Recorrido de este caso | km | CO₂ a 0.21 |
|---|---:|---:|
| Lo que guarda la página: base → El Tambo | 7.64 | 1.60 kg |
| Esa parada más el regreso a la base | 15.28 | 3.21 kg |

7.64 × 0.21 = 1.6044, que redondea a **1.60 kg**. El pedido de Chilca (30 kg) no aporta kilómetros a esta ruta. Eso no significa que su entrega haya desaparecido: queda pendiente para un vehículo que sí tenga cupo. El ahorro ambiental de este caso es no sacar ABC-123 con sobrecarga y no inventar un tramo hasta Chilca dentro de una ruta que no puede cumplirlo. Cuando ese pedido se planifique en otra ruta, sus kilómetros entrarán en el indicador de esa ruta, no en esta.

Si los dos pesos hubieran cabido en un vehículo mayor, el orden norte-sur habría sido El Tambo y después Chilca. Ese recorrido hipotético, calculado con las mismas coordenadas y sin estar guardado por el sistema, mediría 24.46 km sin regreso (5.14 kg) y 33.64 km con regreso a la base (7.06 kg). Se anota solo para mostrar el tamaño del tramo que la capacidad dejó fuera. La pantalla, con ABC-123 de 40 kg, muestra el recorrido de la única parada asignada.

## 1.13 Sensibilidad del factor de emisión

Los kilómetros no dependen del factor. El CO₂ sí. El administrador puede cambiar `factor_emision_kg_por_km` en Parámetros. El sistema rechaza un factor menor o igual a cero. La tabla usa los kilómetros ya redondeados de la demostración y tres factores. El 0.21 es el valor de fábrica. El 0.12 y el 0.30 son variaciones de este informe para la sustentación. La pantalla no los trae cargados.

| Factor (kg CO₂/km) | Pantalla, 11.73 km | Ruta con regreso, 17.61 km | Tres idas y vueltas, 18.12 km |
|---:|---:|---:|---:|
| 0.12 | 1.41 kg | 2.11 kg | 2.17 kg |
| 0.21 | 2.46 kg | 3.70 kg | 3.81 kg |
| 0.30 | 3.52 kg | 5.28 kg | 5.44 kg |

El ahorro comparable (tres viajes menos la ruta con regreso) también escala con el factor: 0.51 km × 0.21 = 0.11 kg. Con 0.12 sería 0.06 kg. Con 0.30 sería 0.15 kg. Cambiar el factor no cambia el recorrido. Cambia la lectura en kilogramos. En la exposición, el factor que vale es el que esté guardado en Parámetros en ese momento. El de fábrica, y el de todas las tablas anteriores, es 0.21.

El otro parámetro del sistema es `velocidad_kmh`, de fábrica 28. El panel Indicadores no muestra minutos. Con ese parámetro, 11.73 km equivalen a 25.1 minutos de recorrido (11.73 / 28 × 60) y 17.61 km, ya con el regreso, equivalen a 37.7 minutos. Es una cuenta de este informe a partir del parámetro. No es una cifra de la pantalla de CO₂.

## 1.14 Qué hace el indicador cuando la ruta cambia de estado

`indicadores` suma kilómetros solo de rutas con estado `ACTIVA` y con campo `km`. De eso salen tres consecuencias que se pueden mostrar.

**Generar.** `generar_ruta` escribe `estado = ACTIVA`, la fecha y el `km` antes de guardar la ruta. Los pedidos de esa ruta pasan a `EN_RUTA`. A partir de ese momento el indicador los cuenta.

**Registrar entrega.** Marcar un pedido como `ENTREGADO` o `INCIDENCIA` cambia el pedido. No cambia el estado de la ruta ni borra sus kilómetros. El CO₂ de ese recorrido sigue en el indicador. La entrega confirma que el viaje se usó. No lo descuenta, porque el kilómetro ya se recorrió en la estimación.

**Reoptimizar.** Solo procede si existe una ruta `ACTIVA` y hubo un cambio operativo. Las rutas activas pasan a `REEMPLAZADA`. Esas dejan de entrar en la suma. Los pedidos que estaban `EN_RUTA` vuelven a `PENDIENTE`, los vehículos vuelven a `DISPONIBLE` y se genera una ruta nueva. El indicador queda con los kilómetros de la ruta nueva, no con la suma de la vieja más la nueva. No hay doble contabilidad.

**Periodo vacío.** La llamada con periodo `vacio` responde «No existen datos para realizar el cálculo.» y no devuelve un CO₂ en cero. Cumple RN-013.

## 1.15 Periodo de hoy y periodo de todo el registro

La fecha de la ruta es la fecha del momento en que se genera, con precisión de minutos. El periodo `hoy` conserva pedidos y rutas cuya fecha empieza por la fecha del día. El periodo de todo el registro no filtra por día.

En una misma sesión de demostración, generar la ruta y calcular con **Hoy** o con **Todo el registro** muestra los mismos 11.73 km y 2.46 kg, porque esa ruta acaba de nacer hoy y es la única activa. La diferencia aparece cuando hay rutas de otro día. Este incremento guarda los datos en la memoria del proceso: al cerrar el servidor no queda un histórico de días anteriores contra el cual contrastar el filtro. La regla del filtro está en el código. El histórico de varios días se verá cuando la persistencia guarde las fechas entre ejecuciones.

El contratante, en cualquiera de los dos periodos, recibe sus pedidos y una lista de rutas vacía. Su respuesta de indicadores no trae el CO₂ de la flota.

## 1.16 Procedimiento con el que se midieron los bytes

La medición digital no usa una extensión del navegador. Usa el tamaño de los archivos en disco el 2026-11-12, porque el servidor los envía enteros y sin compresión.

| Paso | Qué se hizo | Resultado |
|---|---|---|
| 1 | Ubicar los estáticos que el servidor lee desde `src/frontend`. | Tres archivos: HTML, CSS y JavaScript. |
| 2 | Leer el tamaño de cada archivo. | 10,045 + 5,892 + 17,551. |
| 3 | Sumar. | 33,488 bytes. |
| 4 | Buscar PNG, JPEG, WEBP, AVIF, fuentes web y mapas de teselas en esa carpeta. | No hay. El total no tiene un cuarto archivo. |
| 5 | Convertir con el modelo SWDM de la sección 1.8. | 0.011 g CO₂e por visita. |

Las llamadas `/api/rutas` o `/api/indicadores` no están dentro de esos 33,488 bytes. Salen después, cuando la persona pulsa Generar ruta o Calcular. Su tamaño depende de cuántos pedidos haya en memoria. En la demostración son tres paradas, y el informe no las presenta como si pesaran lo mismo que una fotografía.

## 1.17 Interpretación

La reducción que este incremento puede defender con números tiene tres capas.

La primera es operativa y pequeña en la demostración. Juntar tres entregas de 52 kg en ECO-101, y contar también el regreso, ahorra 0.51 km y 0.11 kg frente a tres idas y vueltas. El ahorro es corto porque el Mercado Modelo está a 0.22 km de la base y el orden norte-sur desvía el vehículo hasta El Tambo antes de volver a bajar. El resultado sigue siendo menor, y la sustentación gana si se dice esa causa en lugar de redondearla a un ahorro grande.

La segunda es de contención. RN-016 impide que una carga peligrosa exista como pedido. El cupo impide que un peso que no cabe se meta en la ruta y le invente kilómetros. El indicador impide publicar un CO₂ cuando no hay kilómetros. Esas tres reglas reducen impacto al no dejar pasar una operación que no debe contarse.

La tercera es digital. La herramienta que calcula lo anterior pesa 33,488 bytes y emite 0.011 g CO₂e por visita. Al lado de los 2.46 kg del recorrido en pantalla, la página es la fracción pequeña. Sigue siendo la parte del estándar que el equipo controla en el código: no agregar imágenes, no agregar un mapa de teselas y no agregar un framework para pintar una tabla que `app.js` ya pinta.

## 1.18 Conclusiones

1. La cifra de la pantalla para la demostración de los tres distritos es **11.73 km** y **2.46 kg de CO₂**, con factor 0.21, sin el regreso a la base.
2. La comparación que sí incluye el regreso es **17.61 km** y **3.70 kg** contra **18.12 km** y **3.81 kg** de tres viajes separados. El ahorro es **0.51 km** y **0.11 kg**.
3. Un pedido que no cabe, como los 30 kg de Chilca frente a un vehículo de 40 kg que ya lleva 20 kg, no entra en ese total. Queda pendiente.
4. Entregar un pedido no borra el CO₂ de su ruta. Reoptimizar sí reemplaza la ruta activa, y el indicador se queda con la ruta nueva.
5. La página mide **33,488 bytes** y **0.011 g CO₂e** por visita. Lighthouse no se ejecutó. Las cifras de la plantilla MERN no forman parte de este resultado.

## Historial de versiones

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0.0 | 2026-11-12 | Primera medición de la ruta de demostración y del peso de la página. |
| 1.1.0 | 2026-11-12 | Se desarrolla el cálculo tramo a tramo, los tres escenarios, las ocho decisiones y el paso a paso del modelo SWDM. |
| 1.2.0 | 2026-11-12 | Se agregan el caso de cupo insuficiente, la sensibilidad del factor, el efecto de entregar y reoptimizar, el periodo y el procedimiento de medición de los bytes. |
