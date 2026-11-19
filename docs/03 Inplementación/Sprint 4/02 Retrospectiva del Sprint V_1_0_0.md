[← Volver al README principal](../../../README.md)

# Retrospectiva del sprint

**Nombre del Proyecto:** EcoLogística — Sistema de Optimización de Rutas Sostenibles

**Líder del Proyecto:** Zevallos Melendres, Yimer Edyson

**Sprint:** 4

**Fecha de la retrospectiva:** 2026-11-19

**Versión:** 1.0.0

La sesión de cierre la registró Zevallos Melendres, Yimer Edyson. El acta de constitución sigue nombrando al equipo Híbridos. Esta retrospectiva corresponde al trabajo de cierre del 2026-11-19.

## ¿Qué aprendimos?

La página y el servidor comparten un solo proceso en el puerto 8765 y una sola memoria. Correr Playwright con varios workers a la vez mezclaba sesiones, bloqueaba al operador tras tres claves malas y hacía fallar pruebas que, en serie, pasan. Con `workers: 1` la suite quedó en 21 de 21.

El atributo HTML `hidden` no basta si una regla propia fija `display`. `.app { display: grid }` dejaba visible el panel después de un ingreso fallido. La regla `[hidden] { display: none !important; }` devuelve el control al atributo.

Las métricas de pintura hay que tomarlas en el navegador que las emite. Chromium y Firefox informaron LCP. WebKit, en esta página y en esta corrida, no emitió la entrada. Publicar un LCP inventado para WebKit habría falseado el informe.

El cierre documental pide la carpeta `docs/03 Inplementación/Sprint 4/`, con esa grafía. Los sprints anteriores siguen en `docs/03 Implementación`. Las dos rutas conviven: una es el historial del proyecto y la otra es la ruta que pide esta consigna.

## ¿Qué estamos haciendo bien?

Las reglas de negocio siguen en `src/backend/ecologistica/servicio.py` y las pruebas de Python las cubren antes de la pantalla. La interfaz, en `src/frontend`, llama a la misma API.

Los informes usan los números del sistema: distritos El Tambo, Huancayo y Chilca, factor 0,21 kg CO₂/km, velocidad 28 km/h, y los tiempos medidos el 2026-11-19. Lo que falta se escribe como pendiente.

Git Flow se mantiene con `main` y `develop`, sin reescribir la historia y sin `push --force`. El commit `8f23fbf` dejó la operación en pantalla y el `82d5c25` dejó la ayuda.

`.gitignore` deja fuera `node_modules/`, `.env`, `dist/`, `build/`, `playwright-report/`, `test-results/` y `blob-report/`. El candado de npm (`frontend/package-lock.json`) sí entra al repositorio para que `npm ci` pueda correr en Actions.

## ¿Qué podemos hacer mejor?

### Personas

El cierre del 2026-11-19 recayó en una sola persona. La carga de pruebas, documentación y subida quedó concentrada. Para el mantenimiento, cada historia nueva necesita un responsable nombrado antes de abrir la rama.

### Relaciones

El cliente y el servidor están separados (`src/frontend` y `src/backend`), y la suite E2E vive en `frontend/` porque ahí está Playwright. Quien revise el repositorio tiene que ver las tres carpetas juntas: la página, la API y las pruebas. La coordinación con el curso sigue siendo el cronograma del NRC 30142. Esta retrospectiva no inventa una hora de sustentación.

### Procesos

Las primeras pruebas E2E se lanzaron en paralelo contra el mismo servidor y el resultado no servía para informar. El proceso queda así: una prueba a la vez, cuenta inexistente para el caso de clave mala, y lectura del mensaje real de reoptimización. Las estimaciones del Sprint 4 cubrieron la pantalla y dejaron fuera el hospedaje, porque no hay cuenta ni secreto.

### Herramientas

Playwright 1.49.1, Python 3.12 y GitHub Actions cubren compilación, sintaxis del cliente, pruebas y el paquete de versión. Falta un hospedaje con secreto. El flujo de producción empaqueta el código y lo sube como artefacto. No publica una URL.

### Acciones a realizar

| Acción | Responsable | Seguimiento |
|---|---|---|
| Mantener `workers: 1` mientras el servidor use un solo proceso y el puerto 8765. | Zevallos Melendres, Yimer Edyson | La suite local sigue en 21 superadas. |
| Aplicar la ficha SUS de la evaluación de usabilidad a una muestra real antes de publicar un puntaje. | Zevallos Melendres, Yimer Edyson | El informe de usabilidad pasa de n = 0 a un n contado, con puntaje calculado desde esas respuestas. |
| Exportar el CSV según el filtro de estado y agregar filtro a la auditoría. | Zevallos Melendres, Yimer Edyson | US-013 y US-014 cierran su segundo criterio. |
| Crear el secreto de hospedaje cuando exista una cuenta y conectar `deploy-production.yml` a esa URL. | Zevallos Melendres, Yimer Edyson | El flujo publica una dirección comprobable. |

## Historial de versiones

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0.0 | 2026-11-19 | Retrospectiva del Sprint 4. |
