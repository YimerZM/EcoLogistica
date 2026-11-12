# Estándares de ingeniería de software y desarrollo verde

**Proyecto:** EcoLogística — Sistema de Optimización de Rutas Sostenibles  
**Equipo:** Híbridos — Zevallos Melendres, Yimer Edyson; Pomachagua Yapias, Bryan Antony; Cajamalqui Dávila, Josemaría Piero  
**Curso:** Taller de Proyectos 2 — NRC 30142  
**Versión:** 1.1.0  
**Fecha:** 2026-11-12  

[Volver al README principal](../../../README.md)

Este documento relaciona el incremento que está en `src/backend` y `src/frontend` con tres marcos: ISO/IEC 25010, los principios de la Green Software Foundation y las Web Sustainability Guidelines del W3C. Cada fila de la matriz apunta a una decisión que el repositorio ya ejecuta. Al final se listan las prácticas de la plantilla que este incremento todavía no tiene, para no presentarlas como hechas.

Las cifras de kilómetros, kilogramos y bytes están desarrolladas en el informe de reducción del impacto ambiental de esta misma carpeta. Aquí se usan como evidencia del estándar, no se vuelven a derivar tramo a tramo.

## 2.1 Para qué se aplican estos estándares

EcoLogística tiene dos productos medibles: la propuesta de ruta y la página que la opera. Un estándar de calidad de software, solo, diría si la ruta responde bien y si el código se puede mantener. Un estándar de software verde, solo, diría si esa respuesta gasta de más. Los tres marcos juntos obligan a las dos preguntas:

1. ¿La función hace lo que la regla de negocio pide? RN-013 no calcula CO₂ sin kilómetros. RN-016 no planifica carga peligrosa. RN-014 no acepta un punto fuera de los tres distritos.
2. ¿Esa función evita trabajo inútil? Un segundo vehículo para 52 kg, un mapa de teselas, un hash de clave dentro de un listado y una librería que la pantalla no usa son trabajo que consume energía sin cambiar la entrega.

La plantilla del curso escribe las mismas preguntas sobre MongoDB, Express y React. El equipo Híbridos las responde sobre Python de biblioteca estándar y sobre una página HTML. El nombre del estándar se conserva. El ejemplo de código de la plantilla no se copia, porque ese código no está en el repositorio.

## 2.2 ISO/IEC 25010 aplicado al incremento

ISO/IEC 25010 describe la calidad del producto de software en ocho características. Esta sección dice cómo se ve cada una en el código actual.

### Adecuación funcional

La función de indicadores cumple RN-013: solo entran rutas `ACTIVA` que ya tienen `km`. Si el periodo es `vacio`, o si el filtro deja la lista sin pedidos y sin rutas, la respuesta es que no existen datos. No se devuelve un CO₂ en cero disfrazado de resultado.

La función de pedidos cumple RN-016: `carga_prohibida` compara el tipo contra `general`. El explosivo, el residuo peligroso y cualquier otro texto se rechazan y no se guardan. Una ruta posterior no puede incluirlos porque no existen como pedidos.

La función de puntos cumple RN-014: el distrito tiene que ser El Tambo, Huancayo o Chilca, y la coordenada tiene que caer en la caja WGS84 del valle. Un punto de Lima no se persiste y no puede alargar una ruta.

### Eficiencia de desempeño

En este incremento la eficiencia se observa en dos sitios.

En el cliente, la primera carga son tres archivos y 33,488 bytes. No hay un paquete por pantalla. El mapa SVG se dibuja con los datos que la ruta ya trajo. No se abre una conexión a un servidor de teselas.

En el servidor, la propuesta no recorre vehículos que no están `DISPONIBLE` ni pedidos que no están `PENDIENTE`. El cupo se descuenta en memoria, pedido por pedido. Si ningún vehículo alcanza el peso, la función termina con un mensaje y no crea una ruta vacía. El indicador del contratante no arma la lista de rutas de la flota.

No se publica un tiempo de respuesta en milisegundos. No se cronometró la API con una herramienta externa. Decir «65 ms» sería copiar la plantilla.

### Compatibilidad

La página habla con el servidor por JSON sobre HTTP, en el mismo origen `127.0.0.1`. No depende de un runtime de navegador distinto del JavaScript que ya trae el navegador, ni de una extensión. Las coordenadas viajan como latitud y longitud WGS84, que es el sistema que la regla geográfica ya fijó.

### Usabilidad

Hay una página y un menú que cambia con el rol. El operador ve la operación. El planificador ve la planificación. El conductor ve sus rutas y el registro de entrega. El contratante ve sus pedidos. El auditor ve la auditoría y los indicadores. El administrador ve los parámetros y los usuarios. Quien no puede escribir no ve el formulario de alta. La tarea de «ver el CO₂» es un panel, no una exportación que el usuario tenga que calcular fuera.

### Fiabilidad

La propuesta falla de forma explícita en cuatro casos, y en los cuatro no deja datos a medias:

| Condición | Mensaje | Qué no ocurre |
|---|---|---|
| No hay vehículo disponible | No es posible generar la ruta: no hay vehículos disponibles. | No se crea ruta. |
| No hay pedido pendiente | No hay pedidos pendientes para planificar. | No se crea ruta. |
| Ningún peso cabe | Ningún vehículo tiene capacidad para los pedidos pendientes. | No se crea ruta. |
| Reoptimizar sin cambio operativo o sin ruta activa | La operación se niega. | No se reemplaza la ruta vigente. |

El inicio de sesión evalúa el bloqueo al comenzar. Tres fallos seguidos bloquean 15 minutos. Un usuario inactivo no entra. Esas reglas no son una métrica de carbono. Evitan repetición de trabajo y dejan el fallo registrado en la auditoría.

### Seguridad

`_publico` arma la ficha que viaja al navegador con correo, nombre, rol y estado. El campo `password_hash` se queda en el servidor. La clave nueva exige al menos 8 caracteres y se guarda como hash SHA-256. Un rol desconocido se rechaza con «El rol no corresponde a un perfil del sistema.» No se puede dejar inactivo al último administrador activo. Sin token la respuesta es 401. Con token de un rol que no corresponde, la respuesta es 403 y el texto «No tiene autorización para esta operación.»

Menos campos en la respuesta es, a la vez, menos exposición de credenciales y menos bytes en la red. El estándar de seguridad y el de transferencia apuntan a la misma función.

### Mantenibilidad

El incremento está partido en tres módulos:

| Módulo | Responsabilidad | Qué no hace |
|---|---|---|
| `reglas.py` | Validar distrito, coordenada, rol, carga y armar la propuesta. | No abre sockets ni guarda sesiones. |
| `servicio.py` | Casos de uso, estados, kilómetros, indicadores, auditoría. | No conoce HTTP. |
| `servidor.py` | Rutas HTTP, códigos 200, 201, 400, 401, 403 y 404, archivos estáticos. | No decide el orden de las paradas. |
| `src/frontend` | Pintar paneles y llamar a la API. | No recalcula el haversine. |

Una regla de carbono o de capacidad se cambia en `reglas.py` o en `_km` sin reescribir la página. Las pruebas de `tests/test_reglas.py` y `tests/test_e2e.py` fijan el comportamiento que este informe describe: la capacidad, el rechazo de la carga y el recorrido hasta generar la ruta.

### Portabilidad

El servidor usa la biblioteca estándar de Python. Levantar la página no exige instalar Node, un motor de base de datos ni un compilador de frontend. El mismo `python -m ecologistica` sirve los tres archivos estáticos. Esa sobriedad de plataforma es la forma concreta de no atar el producto a un toolchain que habría que descargar, actualizar y ejecutar en cada máquina del equipo.

## 2.3 Principios de la Green Software Foundation

La Green Software Foundation ordena el trabajo en reducir la intensidad de carbono del software. Cuatro principios se pueden mostrar con este incremento. Uno queda declarado como límite.

### Eficiencia de carbono

Emitir menos para el mismo trabajo. El trabajo de la demostración es entregar 18 kg en El Tambo, 12 kg en el Mercado Modelo y 22 kg en Chilca.

| Forma de hacer el mismo trabajo | Emisión estimada |
|---|---:|
| Tres salidas, cada una con ida y vuelta | 3.81 kg CO₂ |
| Una salida, tres paradas y regreso a la base | 3.70 kg CO₂ |
| Diferencia | 0.11 kg CO₂ |

El principio se cumple en la dirección correcta. La magnitud es la que dan estos tres puntos, no una magnitud de plantilla. El detalle del desvío hacia El Tambo, que explica por qué el ahorro no es mayor, está en el informe de reducción.

### Eficiencia energética

Hacer el mismo trabajo con menos energía en el software. La visita a la página transfiere 33,488 bytes. Con las constantes del modelo SWDM de la plantilla:

```
33,488 / 1,073,741,824 × 0.815 kWh/GB = 0.000025418 kWh por visita
```

No hay imágenes que decodificar, no hay un framework que hidratar y no hay una fuente web que bajar. El costo energético digital de abrir la herramienta es el de interpretar esos tres archivos.

### Conciencia de carbono

Elegir cuándo y dónde ejecutar según la intensidad de la red eléctrica. Este incremento no desplaza cómputo a una hora de menor intensidad. El factor 0.21 y el factor 442 son constantes de cálculo, no una señal en vivo de la red de Huancayo. Declararlo evita presentar un balance horario que el código no consulta.

Lo que sí está bajo control del administrador es el factor de emisión del vehículo. Si ese dato se actualiza, `indicadores` usa el valor nuevo en el siguiente cálculo. Los kilómetros guardados en la ruta no se reescriben solos.

### Eficiencia de hardware

Pedir menos máquina alarga la vida útil del equipo y evita un servidor sobredimensionado. La página corre en el navegador que el estudiante ya tiene. El proceso es un solo `python -m ecologistica`, con los datos en memoria. No se levanta un clúster, un contenedor de base de datos ni un empaquetador vigilando archivos. Para el volumen de la demostración, esa es la máquina proporcional al problema.

### Intensidad de carbono del software (SCI)

La Green Software Foundation expresa la intensidad así:

```
SCI = (E × I) / R
```

| Símbolo | Significado | En este informe |
|---|---|---|
| E | Energía que el software hace consumir | Para la página, los kWh del modelo SWDM. |
| I | Gramos de CO₂e por kWh | 442, constante de la plantilla. |
| R | Unidad funcional | Una visita a la página, o una propuesta de ruta. |

Aplicado a **una visita**:

```
E = 0.000025418 kWh
I = 442 g/kWh
R = 1 visita
SCI = 0.011 g CO₂e por visita
```

Aplicado a **una propuesta de la demostración**, la unidad funcional es «planificar los tres pedidos». La energía aquí no es la del CPU: es la emisión que el software decide atribuir al recorrido, porque el factor ya está en kilogramos de CO₂ por kilómetro. Con la vuelta incluida, R = 1 propuesta y el resultado es **3.70 kg CO₂ por propuesta**. Sin la vuelta, que es lo que persiste la ruta, el resultado es **2.46 kg CO₂ por propuesta**.

Estas dos intensidades no se suman en un solo SCI. Una mide la herramienta. La otra mide el recorrido que la herramienta recomienda. El informe de reducción las deja en tablas distintas por esa razón.

## 2.4 Web Sustainability Guidelines (W3C)

Las WSG piden que el sitio pese lo necesario para la tarea, que los medios estén justificados y que la arquitectura no descargue de más. Así se leen en EcoLogística.

### Medios y presentación

No hay fotografías de banner, no hay iconos en archivos aparte y no hay video. El único gráfico es el SVG del valle, construido en el documento. Las fuentes son de sistema, así que no se pide un CSS de terceros ni un archivo de tipografía. El color de la interfaz no añade bytes de imagen.

La pauta de la plantilla habla de convertir PNG a WebP o AVIF. En este proyecto el paso equivalente ya está dado de otra forma: no se sube el PNG. No hay un antes de 5.2 MB en imágenes porque esa carpeta no existe.

### Arquitectura de la página

Una sola página contiene los paneles. El menú muestra el panel del rol y oculta el resto. No hay una ruta de frontend por cada historia de usuario ni una librería de enrutado. El JavaScript de `app.js` (17,551 bytes) es el único programa del cliente.

### Red y datos

Cada respuesta lleva los campos de la pantalla. La ficha pública del usuario tiene cuatro campos. El pedido viaja con su punto, su peso, su estado y su tipo, que son los datos con los que se arma la parada. El contratante no recibe la flota. El conductor no recibe las rutas de otros conductores.

La compresión Brotli y la cabecera `Cache-Control` que pide la plantilla no están configuradas en `servidor.py`. La reducción de red que sí está medida es el tamaño de origen: 33,488 bytes y tres peticiones en la primera carga. Las peticiones posteriores (`/api/rutas`, `/api/indicadores`, `/api/pedidos`) ocurren cuando el usuario pulsa una acción, no al abrir el documento.

### Tarea del usuario

La WSG trata como desperdicio hacer que la persona recorra pasos que el sistema puede cerrar. Generar la ruta, ver los kilómetros y ver el CO₂ son tres acciones en dos paneles. El usuario no exporta coordenadas a una hoja para multiplicar por 0.21. El sistema ya guardó el factor y ya sumó las piernas.

## 2.5 Guía de desarrollo verde de este equipo

La guía de la plantilla está escrita para Node, Express, MongoDB y React. El equipo la traduce a normas que el código de EcoLogística puede cumplir hoy. Una norma que el repositorio no cumple se escribe en la sección 2.7, no aquí.

### Normas del servidor

1. Una consulta de listado devuelve la ficha pública. El hash de la clave, el contador de intentos y la fecha de bloqueo no salen en `GET /api/usuarios`.
2. El listado se filtra por rol antes de serializar. El contratante y el conductor no reciben el universo de la operación.
3. No se crea una ruta si no hay vehículo disponible, si no hay pedido pendiente o si ningún peso cabe. Una ruta vacía sería cómputo y una fila sin entrega.
4. El CO₂ se calcula al leer indicadores, con el factor vigente y los kilómetros ya guardados. No se inventa un kilómetro cuando el campo no está.
5. La carga distinta de `general` se rechaza en la regla, antes de asignarle identificador.
6. El distrito y la caja WGS84 se validan al crear el punto. Un punto fuera del valle no queda disponible para una parada.
7. La distancia usa una sola función, `_distancia_km`, con radio 6,371 km. La página no tiene otra fórmula paralela que pueda divergir.

### Normas de la página

1. No se agregan archivos PNG, JPEG, WEBP ni AVIF a `src/frontend` para decorar. Un gráfico nuevo entra como SVG en el documento que ya se descarga.
2. No se agregan librerías de terceros al navegador para una función que el lenguaje ya trae. Fechas, listas y dibujo se resuelven en `app.js`.
3. No se pide un mapa de teselas. El esquema del valle se proyecta con la caja latitud -12.20 a -11.90 y longitud -75.40 a -75.00.
4. No se descarga una fuente web. La hoja de estilo usa la pila ya instalada en el equipo.
5. El panel que el rol no usa no se ofrece como acción. Menos formularios visibles, menos envíos inútiles.
6. El indicador se pide cuando la persona pulsa Calcular, con el periodo elegido. No se dispara un cálculo de flota al pintar el login.

### Qué debe conservar el siguiente incremento

El siguiente trabajo de historia de usuario sale de `develop`. Puede añadir persistencia o una cartografía externa. Si lo hace, este estándar le pone tres condiciones medibles:

1. El peso de la primera carga se vuelve a contar y se anota en el informe. Si se suma un proveedor de mapas, sus teselas entran en la cuenta de bytes y de peticiones.
2. El CO₂ de flota sigue sin mostrarse al contratante, y sigue sin calcularse cuando no hay kilómetros.
3. RN-016 sigue impidiendo que la carga peligrosa exista como pedido. Una base de datos nueva no es motivo para guardarla «por si acaso».

## 2.6 Matriz de mapeo

| # | Decisión ya aplicada en EcoLogística | ISO/IEC 25010 | Green Software Foundation | W3C WSG |
|---|---|---|---|---|
| 1 | Un vehículo absorbe los pedidos que caben. El que no cabe sigue pendiente y se lista en `sin_cupo`. | Adecuación funcional y eficiencia. La capacidad es parte del resultado correcto. | Eficiencia de carbono. 3.70 kg con regreso frente a 3.81 kg en tres viajes. | La tarea del usuario termina en una propuesta, no en tres salidas manuales. |
| 2 | Las paradas se ordenan de norte a sur y los kilómetros salen de esa secuencia. | Adecuación funcional. El orden es determinista y se puede probar. | Eficiencia de carbono. El recorrido queda escrito y no se recalcula en vacío. | El usuario ve el orden y el kilómetro en el mismo panel. |
| 3 | El indicador usa rutas activas con `km`. El periodo vacío no calcula. | Adecuación funcional (RN-013) y fiabilidad. No hay un cero falso. | Medición. El SCI de la propuesta tiene unidad y datos de entrada. | Los datos que se muestran alcanzan para la cuenta. |
| 4 | La carga que no es `general` no se guarda (RN-016). | Adecuación funcional y seguridad de la operación. | Eficiencia de carbono. Ese traslado no suma kilómetros. | No se ofrece una tarea que el dominio prohíbe. |
| 5 | El mapa es SVG en la página. No hay teselas ni proveedor externo. | Eficiencia de desempeño. | Eficiencia energética y de hardware. Cero imágenes de mapa. | Medios: el gráfico existe y no añade un archivo. |
| 6 | Una página, tres archivos, 33,488 bytes, fuentes de sistema. | Eficiencia de desempeño y usabilidad. | Eficiencia energética. 0.000025418 kWh por visita. | Arquitectura y red: tres peticiones en la primera carga. |
| 7 | Python de biblioteca estándar y JavaScript del navegador. Sin `node_modules`. | Mantenibilidad y portabilidad. | Eficiencia de hardware. No hay toolchain que ejecutar para abrir la página. | Librerías: no se descarga código de terceros. |
| 8 | La ficha pública no lleva el hash. Cada rol recibe su lista. El contratante no ve el CO₂ de la flota. | Seguridad y eficiencia de capacidad. | Menos datos transferidos por consulta. | Red: la respuesta se recorta a la tarea de ese rol. |

## 2.7 Prácticas de la plantilla que este incremento no ejecuta

La guía MERN cierra con compresión, caché y una auditoría automática. Esas tres prácticas se nombran aquí para que la sustentación no las dé por hechas.

| Práctica de la plantilla | Estado en EcoLogística el 2026-11-12 |
|---|---|
| Compresión Brotli o Gzip en el servidor | No está. `servidor.py` envía el cuerpo sin ese middleware. El peso de 33,488 bytes es el peso sin comprimir, que es el que usa el cálculo. |
| Cabecera `Cache-Control` y ETag | No están. El navegador puede cachear por su cuenta. El informe no descuenta una segunda visita. |
| Paginación `page` y `limit` | No está. El recorte que sí existe es por rol y por estado del pedido. |
| Lighthouse en GitHub Actions | No hay un workflow de esa auditoría. No se publican FCP, LCP, TBT ni CLS. |
| Conversión de imágenes a WebP o AVIF | No aplica como conversión: `src/frontend` no contiene imágenes de mapa de bits. |
| Índices y `.lean()` de MongoDB | No aplica. Este incremento no tiene MongoDB en ejecución. |

Cuando una de esas prácticas entre al repositorio, el informe de reducción se actualiza con el peso nuevo y con la evidencia del cambio. Hasta entonces, la evidencia verde del equipo es la tabla de la sección 2.6.

## 2.8 Trazabilidad con las reglas del proyecto

| Regla | Dónde se cumple | Qué protege en este informe |
|---|---|---|
| RN-013 | `indicadores` exige rutas con kilómetros y se niega si no hay datos. | El CO₂ publicado es calculable. |
| RN-014 | `coordenada_valida` y la lista `DISTRITOS`. | El kilómetro corresponde al valle, no a un punto fuera de alcance. |
| RN-015 | Códigos 401 y 403, y el menú por rol. | Cada persona descarga la operación que le pertenece. |
| RN-016 | `carga_prohibida`. | La carga peligrosa no infla la huella. |
| RF-012 | Panel Indicadores, periodo hoy o todo el registro. | La persona lee km y kg sin rehacer la fórmula. |

## 2.9 Glosario breve

| Término | Uso en EcoLogística |
|---|---|
| Factor de emisión | 0.21 kg CO₂ por kilómetro, parámetro editable por el administrador. |
| Haversine | Fórmula de `_distancia_km`, radio 6,371 km. |
| Propuesta | Lista de paradas de una ruta, orden norte-sur, limitada por la capacidad. |
| Escenario comparable | Tres idas y vueltas contra una ruta que también regresa a la base. |
| SCI | Intensidad de carbono por unidad funcional. En la página, una visita. En la operación, una propuesta. |
| SWDM | Modelo de la plantilla: GB × 0.815 kWh/GB × 442 g CO₂e/kWh. |
| Primera carga | `index.html` + `estilos.css` + `app.js` = 33,488 bytes = 0.011 g CO₂e. |

## Historial de versiones

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0.0 | 2026-11-12 | Primera relación de los tres estándares con el incremento Python. |
| 1.1.0 | 2026-11-12 | Se desarrolla cada característica de ISO/IEC 25010, los principios GSF con la fórmula SCI, las pautas W3C, la guía del equipo y la lista de prácticas todavía no implementadas. |
