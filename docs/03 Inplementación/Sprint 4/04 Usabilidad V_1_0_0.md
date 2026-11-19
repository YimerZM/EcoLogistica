[← Volver al README principal](../../../README.md)

# Evaluación de usabilidad

**Nombre del Proyecto:** EcoLogística — Sistema de Optimización de Rutas Sostenibles

**Líder del Proyecto:** Zevallos Melendres, Yimer Edyson

**Instrumento:** System Usability Scale (SUS), Brooke, 1996

**Fecha de la ficha:** 2026-11-19

**Versión:** 1.0.0

## Ficha técnica de la evaluación

| Dato | Valor |
|---|---|
| Instrumento | SUS, diez enunciados alternados entre tono positivo y tono negativo |
| Escala | Likert de 1 a 5. 1 = totalmente en desacuerdo. 5 = totalmente de acuerdo. |
| Tamaño de la muestra | n = 0 |
| Perfil pedido | Operador logístico, planificador o responsable que use la pantalla de rutas de El Tambo, Huancayo y Chilca |
| Entorno previsto | http://127.0.0.1:8765 con `python -m ecologistica` |
| Puntaje promedio | No se calcula. No hay respuestas. |
| Umbral de lectura | 68 o más se toma como aceptable cuando exista muestra |

La ficha está lista para aplicarse. El 2026-11-19 ningún participante la respondió. Por eso este informe no publica puntajes brutos, ni un promedio, ni un grado A–F del producto. Inventar cinco filas de Likert dejaría de ser una medición.

### Tareas que la persona completa antes de marcar la escala

1. Abrir http://127.0.0.1:8765 e ingresar con la ficha Operador.
2. Preparar los datos de El Tambo, Huancayo y Chilca.
3. Generar la ruta y leer el detalle.
4. Abrir Pedidos, filtrar por un estado y volver a ver el listado.
5. Abrir el archivo de ayuda desde el menú Ayuda.
6. Cerrar la sesión.
7. Recién entonces marcar los diez enunciados.

### Enunciados

Cada enunciado se responde de 1 a 5.

1. Creo que me gustaría usar este sistema con frecuencia.
2. Encontré el sistema innecesariamente complejo.
3. Me pareció que el sistema era fácil de usar.
4. Creo que necesitaría apoyo de una persona técnica para poder usar este sistema.
5. Encontré que las funciones del sistema estaban bien integradas.
6. Pensé que había demasiada inconsistencia en este sistema.
7. Imagino que la mayoría de las personas aprendería a usar este sistema rápidamente.
8. Encontré el sistema muy incómodo de usar.
9. Me sentí muy seguro usando el sistema.
10. Necesité aprender muchas cosas antes de poder manejarme con el sistema.

Los enunciados 1, 3, 5, 7 y 9 van en tono positivo. Los enunciados 2, 4, 6, 8 y 10 van en tono negativo.

## Resultados cuantitativos

### Tabla de puntuaciones brutas

| Participante | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9 | P10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| — | — | — | — | — | — | — | — | — | — | — |

La fila está vacía porque n = 0. Cuando alguien responda, esa fila lleva el identificador de la persona y los diez enteros de 1 a 5.

### Cálculo de un puntaje individual

Para una persona, con respuestas R1…R10:

1. En cada enunciado positivo (1, 3, 5, 7, 9) el aporte es `Ri - 1`. El rango de cada aporte queda entre 0 y 4.
2. En cada enunciado negativo (2, 4, 6, 8, 10) el aporte es `5 - Ri`. El rango de cada aporte queda entre 0 y 4.
3. Se suman los diez aportes. La suma queda entre 0 y 40.
4. El SUS individual es esa suma multiplicada por 2,5. El resultado queda entre 0 y 100.

Ejemplo de la fórmula, con letras y sin datos de una persona real:

- Aportes positivos: `(R1 - 1) + (R3 - 1) + (R5 - 1) + (R7 - 1) + (R9 - 1)`
- Aportes negativos: `(5 - R2) + (5 - R4) + (5 - R6) + (5 - R8) + (5 - R10)`
- `SUS = 2,5 × (positivos + negativos)`

### Cálculo del promedio

Con n personas y puntajes S1…Sn:

`promedio = (S1 + S2 + … + Sn) / n`

Hoy n = 0, la suma no existe y el promedio no se publica.

## Análisis e interpretación

El umbral de lectura de esta ficha es 68. Un promedio de 68 o más se leería como aceptable. La tabla de adjetivos que se usará cuando haya muestra es esta:

| Puntaje SUS | Grado | Lectura |
|---|---|---|
| 84,1 a 100 | A | Excelente |
| 80,8 a 84,0 | B | Bueno |
| 71,1 a 80,7 | C | Aceptable, por encima del umbral |
| 68,0 a 71,0 | D | En el límite aceptable |
| 51,0 a 67,9 | E | Bajo el umbral |
| 0 a 50,9 | F | Deficiente |

EcoLogística no recibe grado en esta versión. El promedio no existe.

### Hallazgos de interfaz observados al construir y correr las pruebas

Estos hallazgos salen de la construcción de la suite y de la corrida del 2026-11-19. Son observaciones del equipo, no respuestas SUS.

1. El panel de la aplicación seguía visible después de un ingreso fallido, porque `.app { display: grid }` tapaba el atributo `hidden`. La corrección está en `src/frontend/css/estilos.css` y la prueba de clave incorrecta lo vigila.
2. La página tiene tres campos de correo (ingreso, alta de usuario y edición). Una prueba que buscaba cualquier `input[name="email"]` encontraba tres. El ingreso quedó acotado a `#form-sesion`.
3. Reoptimizar tiene tres mensajes distintos. La pantalla los muestra en `#mensaje-op`. Quien opera necesita leer ese aviso: sin un cambio operativo la ruta no se recalcula.
4. WebKit no informó LCP en la carga medida. La primera pintura sí ocurrió (FCP 83 ms en esa corrida).

### Mejoras propuestas para cuando se aplique la muestra

1. Sentar al menos a cinco personas del perfil de la ficha, con las seis tareas, y cargar la tabla de brutos.
2. Calcular cada SUS con los cuatro pasos de arriba y el promedio con la división por n.
3. Comparar ese promedio con 68 y asignar el grado de la tabla.
4. Si el promedio queda bajo 68, revisar primero el aviso de reoptimización y el texto del ingreso fallido, que son los dos puntos donde la corrida automática ya encontró ambigüedad.

## Historial de versiones

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0.0 | 2026-11-19 | Ficha SUS lista. Muestra n = 0. Sin puntaje publicado. |
