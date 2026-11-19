[← Volver al README principal](../../../README.md)

# Análisis Playwright

**Nombre del Proyecto:** EcoLogística — Sistema de Optimización de Rutas Sostenibles

**Líder del Proyecto:** Zevallos Melendres, Yimer Edyson

**Fecha de la medición:** 2026-11-19

**Herramienta:** Playwright 1.49.1

**Versión:** 1.0.0

## Configuración del entorno de pruebas

La suite vive en `frontend/` y la aplicación sigue en `src/frontend` y `src/backend`.

```text
frontend/
├── package.json
├── package-lock.json
├── playwright.config.js
└── e2e/
    ├── nucleo.spec.js
    └── rendimiento.spec.js
```

`playwright.config.js` define:

- `testDir`: `./e2e`
- tiempo de prueba: 30 segundos; tiempo de expectativa: 8 segundos
- `fullyParallel: false` y `workers: 1`, porque todas las pruebas hablan con un solo proceso en memoria
- un reintento solo cuando existe la variable `CI`
- reporteros `list` y `html` con `open: "never"`
- `baseURL`: http://127.0.0.1:8765
- `webServer`: `python -m ecologistica` con directorio de trabajo `../src/backend`
- `reuseExistingServer` activo fuera de CI y apagado en CI, para que Actions levante su propio proceso
- proyectos: Chromium (Desktop Chrome), Firefox (Desktop Firefox) y WebKit (Desktop Safari)

El paquete es privado (`ecologistica-e2e`). El script `test:e2e` ejecuta `playwright test`. La dependencia de desarrollo es `@playwright/test` 1.49.1.

## Pruebas de extremo a extremo

Cada caso corre en los tres navegadores. Son siete casos por navegador, 21 en total.

| Caso | Qué comprueba |
|---|---|
| La clave incorrecta no abre la sesión | Llena `#form-sesion` con `nadie@ecologistica.test` y una clave que no existe. El mensaje de sesión trae texto y `#aplicacion` permanece oculto. |
| El operador prepara los tres distritos y genera la ruta | Entra con la ficha Operador, prepara El Tambo, Huancayo y Chilca, y el detalle de la ruta nombra El Tambo y Chilca. |
| Reoptimizar responde con una de sus tres reglas | El mensaje contiene «reoptimiz», «ruta activa» o «cambio operativo». |
| El pedido explosivo no se guarda | El formulario de pedido con carga explosiva muestra RN-016. |
| La ayuda y el ingreso responden 200 | `GET /` y `GET /ayuda.html` responden 200. `GET /no-existe.html` responde 404. |
| La primera carga mide TTFB y FCP | Lee la navegación y la pintura, y exige FCP. |
| La API de sesión responde en la misma página | `POST /api/sesion` con clave incorrecta responde HTTP 200 en menos de 500 ms. El cuerpo lleva `ok: false`. |

El ingreso del operador usa el botón de la ficha que ya está en la pantalla. La clave mala del primer caso usa un correo que no existe, así el contador del operador no llega a tres y las pruebas siguientes pueden entrar.

Resultado de la corrida local del 2026-11-19, después de corregir el atributo `hidden`:

- 21 pruebas ejecutadas
- 21 superadas
- 0 fallidas
- duración 20,2 segundos
- 1 worker

Comando, desde `frontend`:

```text
npx playwright test
```

El reporte HTML queda en `frontend/playwright-report/`. Esa carpeta está en `.gitignore`. En GitHub Actions el flujo `tests.yml` la sube como artefacto `playwright-report` aunque la suite falle (`if: always()`).

## Monitoreo de rendimiento

Medición local del 2026-11-19, primera carga de http://127.0.0.1:8765, cabeza sin ventana. TTFB es `responseStart - requestStart`. FCP sale de `first-contentful-paint`. LCP sale de un `PerformanceObserver` de tipo `largest-contentful-paint` instalado antes de la navegación. El tiempo de API es `POST /api/sesion` con clave incorrecta, medido con `performance.now()` en la misma página.

| Navegador | TTFB (ms) | FCP (ms) | LCP (ms) | Carga (ms) | API de sesión (ms) |
|---|---:|---:|---:|---:|---:|
| Chromium | 3 | 68 | 68 | 63 | 3 |
| Firefox | 2 | 83 | 83 | 82 | 11 |
| WebKit | 1 | 83 | sin entrada | 150 | 96 |

WebKit completó la prueba de carga porque FCP sí existió. No emitió LCP en esa corrida, así que la celda queda vacía de número a propósito. Los cuatro tiempos de API quedaron bajo el tope de 500 ms que afirma la prueba. Son tiempos de la máquina local contra un servidor en el mismo equipo. No son tiempos de un servidor público.

## Disponibilidad y resiliencia

| Petición | Código | Lectura |
|---|---|---|
| `GET /` | 200 | La página de ingreso se entrega. |
| `GET /ayuda.html` | 200 | El archivo de ayuda se entrega. |
| `GET /no-existe.html` | 404 | Un archivo estático ausente responde «No encontrado.» |
| `POST /api/sesion` con clave incorrecta | 200 | La API responde. El cuerpo indica `ok: false` y el mensaje «Credenciales no válidas.» cuando el correo no existe. |
| Ruta de API desconocida | 404 | El servidor responde «Ruta no encontrada.» |

La suite no midió un tiempo de disponibilidad de producción. No hay URL desplegada. El servidor local permaneció en pie durante los 20,2 segundos de la corrida. Si el puerto 8765 no tiene proceso, el navegador informa conexión rechazada y Playwright no puede abrir la página: el flujo de Actions levanta el proceso antes de las pruebas y, fuera de CI, reutiliza uno que ya esté escuchando.

El reporte HTML de esta corrida se genera al terminar `npx playwright test`. Para abrirlo en la máquina local:

```text
npx playwright show-report
```

## Historial de versiones

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0.0 | 2026-11-19 | Primera medición Playwright: 21 de 21 en Chromium, Firefox y WebKit. |
