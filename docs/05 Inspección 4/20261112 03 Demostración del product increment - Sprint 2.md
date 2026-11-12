# Demostración del product increment — Sprint 2

**Proyecto:** EcoLogística  
**Equipo:** Híbridos  
**Fecha de esta guía:** 2026-11-12  
**Incremento:** US-001, US-003, US-004 y US-005, ejecutables desde el Sprint 2

[Volver al README principal](../../README.md)

El Sprint 2 cerró el núcleo que el Sprint 1 había dejado en especificación. Esta demostración muestra solo esas cuatro historias. La página también tiene usuarios y ruta; eso se dice como trabajo posterior, no como parte de este incremento.

## 1. Encender la aplicación

Desde `src/backend`:

```text
python -m ecologistica
```

Abrir http://127.0.0.1:8765. En las cuentas de demostración, pulsar **Operador** y luego **Iniciar sesión**.

Cuenta: `operador@ecologistica.test` / `operador123`.

## 2. Recorrido del Sprint 2

| Paso | Qué hacer | Qué decir | Resultado |
|---|---|---|---|
| 1 | Poner una clave incorrecta y pulsar Iniciar sesión | US-001. El contador se evalúa al comenzar | No abre la sesión |
| 2 | Volver a la clave `operador123` y entrar | La clave válida abre el núcleo | Aparece Operador logístico y el menú |
| 3 | En Vehículos, registrar placa `ABC-123` y capacidad `800` | US-003 | El vehículo queda DISPONIBLE |
| 4 | En Puntos, intentar Lima | US-004. Solo El Tambo, Huancayo y Chilca | El punto se rechaza |
| 5 | Registrar Mercado, Jr. Real, Huancayo, `-12.07`, `-75.21` | La geolocalización es WGS84, no GPS del vehículo | El punto queda en el valle |
| 6 | En Pedidos, elegir ese punto, peso `10` y tipo Explosivo | RN-016 | El pedido no se guarda |
| 7 | Repetir con tipo General | US-005 | El pedido queda PENDIENTE |

## 3. Cierre

El incremento del Sprint 2 es sesión, vehículo, punto y pedido. Si el docente pide ver la ruta, se aclara que esa pantalla es el incremento siguiente: menú Rutas, después de preparar los datos del valle.
