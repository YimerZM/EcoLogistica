# Elevator pitch

**Proyecto:** EcoLogística  
**Equipo:** Híbridos  
**Fecha:** 2026-11-12  
**Duración:** 30 segundos y 90 segundos

[Volver al README principal](../../README.md)

## 30 segundos

En El Tambo, Huancayo y Chilca un operador reparte pedidos con pocos vehículos y sin un mapa claro de lo que sí puede cargar. EcoLogística le deja registrar el vehículo, el punto con coordenadas WGS84 y el pedido, y le arma una ruta que cabe en la capacidad. Si la carga es peligrosa o el punto sale de esos tres distritos, el pedido no entra.

## 90 segundos

Un operador de Huancayo arma la ruta del día con la memoria y con mensajes. Se le pasa un pedido que no cabe, o un destino que ya no está en el valle, y el camión recorre de más.

EcoLogística es el sistema de rutas sostenibles para El Tambo, Huancayo y Chilca. El operador entra con su cuenta. El sistema revisa el contador de intentos al comenzar, no después. Luego registra la placa y los kilos del vehículo, el punto de entrega con latitud y longitud WGS84, y el pedido. La carga general queda pendiente. Un explosivo o un residuo peligroso se rechaza y no se guarda.

Cuando hay vehículo disponible, el sistema propone la ruta de norte a sur y muestra las paradas sobre el esquema del valle. Si no hay vehículo, o el pedido no cabe, lo dice y no lo asigna. El administrador crea las cuentas. El contratante solo consulta sus pedidos.

El resultado es una distribución local que se puede demostrar hoy en http://127.0.0.1:8765, con las reglas del proyecto y sin salir de los tres distritos.

## Qué no se dice en el pitch

No se dice que el sistema ya usa PostgreSQL ni FastAPI. No se dice que el vehículo trae GPS. La geolocalización de esta versión es la coordenada WGS84 del punto de entrega.
