# Manual técnico del sistema

**Nombre del sistema:** EcoLogística  
**Versión demostrable:** incremento del núcleo operativo, Sprint 2  
**Autores:** Zevallos Melendres, Yimer Edyson; Pomachagua Yapias, Bryan Antony; Cajamalqui Dávila, Josemaría Piero  
**Fecha:** 2026-11-05  
**Objetivo:** permitir que otro programador entienda, ejecute y continúe el sistema de rutas para El Tambo, Huancayo y Chilca

[Volver al README principal](../../README.md)

Este manual sigue el orden del esquema técnico del curso. Las tecnologías son las de EcoLogística. El esquema de C#, SQL Server y DevExpress no corresponde a este repositorio.

## 1. Presentación

EcoLogística registra operadores, vehículos, puntos de entrega y pedidos. Rechaza carga prohibida y puntos fuera de los tres distritos. Todavía no calcula ni dibuja la ruta.

## 2. Tecnologías utilizadas

| Pieza | Tecnología en este incremento | Tecnología decidida y aún no ejecutada |
|---|---|---|
| Interfaz | HTML, CSS y JavaScript en `src/frontend` | React |
| API | Python, biblioteca estándar, en `src/backend` | FastAPI |
| Datos | Memoria del proceso | PostgreSQL |
| Pruebas | `unittest` | Se mantienen |

Git, Docker y Mermaid no forman parte del producto. Son herramientas de trabajo.

## 3. Arquitectura

La página llama a la API por HTTP. La API aplica las reglas y guarda en memoria.

```text
Navegador
    |
Página en src/frontend
    |
API en src/backend/ecologistica/servidor.py
    |
Casos de uso en servicio.py
    |
Reglas en reglas.py
    |
Memoria del proceso
```

## 4. Estructura del proyecto

| Carpeta | Equivale a | Contenido |
|---|---|---|
| `src/frontend` | Presentación | `index.html`, `css/estilos.css`, `js/app.js` |
| `src/backend/ecologistica/reglas.py` | Reglas de negocio | Contador de sesión, distritos y carga prohibida |
| `src/backend/ecologistica/servicio.py` | Casos de uso | Sesión, vehículos, puntos y pedidos |
| `src/backend/ecologistica/servidor.py` | Acceso por HTTP | Rutas `/api/sesion`, `/api/vehiculos`, `/api/puntos`, `/api/pedidos` |
| `docs/01 Inicio/11. Base de datos V_1_0_0.md` | Modelo de datos | Script SQL previsto para PostgreSQL |

## 5. Instalación y ejecución

1. Tener Python 3 instalado.
2. Abrir una terminal en `src/backend`.
3. Ejecutar `python -m unittest tests.test_reglas tests.test_e2e`.
4. Ejecutar `python -m ecologistica`.
5. Abrir http://127.0.0.1:8765.
6. Entrar con `operador@ecologistica.test` y `operador123`.

No hay cadena de conexión que configurar: los datos viven en memoria y se pierden al cerrar el proceso.

## 6. Base de datos

El modelo lógico, en tercera forma normal, está en el documento de base de datos del inicio. Las entidades del incremento en ejecución son usuario, vehículo, punto de entrega y pedido. La clave del punto es el par latitud/longitud más el distrito. El pedido solo persiste si `tipo_carga` es general.

## 7. Módulos

| Módulo | Función | Regla |
|---|---|---|
| Sesión | Abrir acceso del operador | El contador se evalúa al iniciar. Al tercer fallo, bloquea 15 minutos |
| Vehículo | Guardar placa y capacidad | La placa no se repite. La capacidad es mayor que cero |
| Punto | Guardar destino | Solo El Tambo, Huancayo o Chilca, en coordenadas WGS84 |
| Pedido | Guardar la carga | General queda PENDIENTE. Explosivo y residuo peligroso se rechazan |

## 8. Interfaces

La página tiene cuatro bloques, en este orden: inicio de sesión, vehículo, punto de entrega y pedido. Cada alta muestra un mensaje bajo el formulario y agrega el registro a su lista. No hay controles de una librería de escritorio ni captura obligatoria dentro de este manual.

## 9. Seguridad

Hay un usuario de demostración, rol operador. Las rutas de vehículos, puntos y pedidos exigen el token que devuelve el inicio de sesión. No hay todavía pantalla de administración de usuarios ni de permisos por rol. Eso corresponde a US-002.

## 10. Reglas de negocio

| Código | Regla |
|---|---|
| RN-001 | Al iniciar la sesión, si el bloqueo venció, el contador vuelve a cero. Tres fallos bloquean 15 minutos |
| RN-016 | No se guarda un pedido de producto peligroso o prohibido |
| C-04 | La única geolocalización admitida es WGS84 dentro de los tres distritos |

## 11. Problemas comunes

| Problema | Qué ocurre | Qué hacer |
|---|---|---|
| `127.0.0.1 rechazó la conexión` | El proceso no está encendido | En `src/backend`, ejecutar `python -m ecologistica` y recargar |
| La lista de puntos del pedido está vacía | Todavía no hay un punto guardado | Registrar primero el punto de entrega |
| El pedido explosivo no aparece | La regla lo rechazó | Usar tipo General para un pedido válido |
| Los datos desaparecen | El almacén es memoria | Volver a registrarlos después de reiniciar |

## 12. Mejoras futuras

Usuarios y roles, generación de rutas con capacidad y ventana, mapa del recorrido, reoptimización, FastAPI y PostgreSQL.

## 13. Recomendación

Mantener este manual técnico separado de la exposición oral y de los diagramas que ya están en el modelo C4 y en la base de datos del inicio.
