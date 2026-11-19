# Informe completo — Consolidado 2

**Proyecto:** EcoLogística — Sistema de Optimización de Rutas Sostenibles  
**Estudiante que publica este cierre:** Zevallos Melendres, Yimer Edyson  
**Equipo del proyecto:** Híbridos — Zevallos Melendres, Yimer Edyson; Pomachagua Yapias, Bryan Antony; Cajamalqui Dávila, Josemaría Piero  
**NRC:** 30142 — Taller de Proyectos 2  
**Fecha:** 2026-11-19  
**Repositorio:** https://github.com/YimerZM/EcoLogistica

[Volver al README principal](../../README.md)

## 1. Qué es el sistema

EcoLogística planifica entregas de carga general en El Tambo, Huancayo y Chilca. El operador registra vehículos, puntos WGS84 y pedidos. El administrador registra usuarios. El planificador genera una ruta que ordena las paradas de norte a sur y respeta la capacidad del vehículo. El indicador convierte los kilómetros en CO₂ con el factor 0.21 kg por kilómetro.

## 2. Cómo se enciende

Desde `src/backend`:

```text
python -m ecologistica
```

La página queda en http://127.0.0.1:8765. El archivo de ayuda queda en http://127.0.0.1:8765/ayuda.html y en el menú Ayuda. Si la terminal se cierra, la página se apaga. Los datos viven en la memoria de ese proceso.

Cuentas de demostración: administrador `admin123`, operador `operador123`, planificador `plan12345`, conductor `conductor1`, responsable `responsable1`, auditor `auditor123`. El dominio de todas es `@ecologistica.test`. El contratante lo crea el administrador.

## 3. Requisitos que la página ejecuta

| Requisito | Dónde se ve |
|---|---|
| RF-001 Autenticación | Ingreso. Tres fallos bloquean 15 minutos. Si el bloqueo ya venció, el contador vuelve a cero al empezar. |
| RF-002 Usuarios | Alta, consulta y modificación. La lista no trae la clave. |
| RF-003 Vehículos | Alta y modificación de capacidad, estado y conductor. |
| RF-004 Puntos | Solo El Tambo, Huancayo y Chilca, dentro de la caja WGS84. |
| RF-005 Pedidos | Carga general queda PENDIENTE. Explosivo y residuo peligroso se rechazan. |
| RF-006 Rutas | Una propuesta por capacidad, de norte a sur. |
| RF-007 Visualización | Esquema SVG del valle. La línea de una ruta activa sale de la base. |
| RF-008 Reoptimización | Solo si hay una ruta activa y un cambio operativo. |
| RF-009 Seguimiento | Filtro por estado del pedido. |
| RF-010 Entrega | ENTREGADO, o INCIDENCIA con motivo, solo si el pedido está EN_RUTA. |
| RF-011 Indicadores logísticos | Pendientes, en ruta, entregados, incidencias, kilogramos, kilómetros y minutos estimados. |
| RF-012 Indicadores ambientales | Kilómetros por el factor. De fábrica, 0.21. El contratante no ve el CO₂ de la flota. |
| RF-013 Exportación | CSV de pedidos para administrador, operador, planificador, responsable y auditor. |
| RF-014 Auditoría | Ingresos y operaciones, visibles para administrador y auditor. |
| RF-015 Parámetros | Factor de emisión y velocidad, editables por el administrador. |

## 4. Cifras de la demostración

Con el botón de datos de los tres distritos y Generar ruta, la pantalla muestra **11.73 km** y **2.46 kg de CO₂**. Esa distancia no incluye el regreso a la base. Tres viajes separados suman **18.12 km** y **3.81 kg**. Una ruta con regreso suma **17.61 km** y **3.70 kg**. El ahorro comparable es **0.51 km** y **0.11 kg**. El desarrollo de esas cuentas está en el informe de reducción del impacto ambiental.

## 5. Pruebas

Desde `src/backend`:

```text
python -m unittest tests.test_reglas tests.test_e2e -v
```

Son 10 pruebas de sistema y 1 de extremo a extremo. El resultado esperado es `Ran 11 tests` y `OK`. No hace falta tener la página encendida.

## 6. Lo que este informe no declara como hecho

- FastAPI no está en ejecución. La API es Python de la biblioteca estándar.
- PostgreSQL no está en ejecución. El almacén es la memoria del proceso.
- No hay Lighthouse ni las cifras de la plantilla MERN.
- No hay capturas de Jira fabricadas. El espacio para pegarlas sigue en el documento de planificación.
- El mapa no es el GPS del vehículo.

## 7. Dónde está cada entrega

| Entrega | Carpeta |
|---|---|
| Inicio y planificación | `docs/01 Inicio`, `docs/02 Planificación` |
| Sprints 1, 2 y 3 | `docs/03 Implementación` |
| Impacto ambiental | `docs/03 Implementación/reduccion del impacto ambiental` |
| Inspección 3 | `docs/04 Inspección 3` |
| Inspección 4 | `docs/05 Inspección 4` |
| Inspección 5 | `docs/06 Inspección 5` |
| Este informe | `docs/07 Consolidado 2` |
| Ayuda del software | `src/frontend/ayuda.html` |
