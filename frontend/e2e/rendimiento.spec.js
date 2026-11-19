const { test, expect } = require("@playwright/test");

test("la primera carga mide TTFB y FCP", async ({ page }) => {
  await page.addInitScript(() => {
    window.__lcp = null;
    new PerformanceObserver((lista) => {
      const ultima = lista.getEntries().at(-1);
      if (ultima) window.__lcp = ultima.startTime;
    }).observe({ type: "largest-contentful-paint", buffered: true });
  });
  await page.goto("/", { waitUntil: "load" });
  await page.waitForTimeout(300);
  const metricas = await page.evaluate(() => {
    const nav = performance.getEntriesByType("navigation")[0];
    const fcp = performance.getEntriesByType("paint").find((marca) => marca.name === "first-contentful-paint");
    return {
      ttfb: Math.round(nav.responseStart - nav.requestStart),
      fcp: fcp ? Math.round(fcp.startTime) : null,
      lcp: window.__lcp === null ? null : Math.round(window.__lcp),
      carga: Math.round(nav.loadEventEnd),
    };
  });
  expect(metricas.ttfb).toBeGreaterThanOrEqual(0);
  expect(metricas.fcp).not.toBeNull();
  console.log(JSON.stringify({ navegador: test.info().project.name, ...metricas }));
});

test("la API de sesión responde en la misma página", async ({ page }) => {
  await page.goto("/");
  const duracion = await page.evaluate(async () => {
    const inicio = performance.now();
    const respuesta = await fetch("/api/sesion", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: "operador@ecologistica.test", password: "clave-mala" }),
    });
    const fin = performance.now();
    return { estado: respuesta.status, ms: Math.round(fin - inicio) };
  });
  expect(duracion.estado).toBe(200);
  expect(duracion.ms).toBeLessThan(500);
  console.log(JSON.stringify({ navegador: test.info().project.name, apiSesionMs: duracion.ms }));
});
