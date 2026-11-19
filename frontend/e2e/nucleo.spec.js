const { test, expect } = require("@playwright/test");

async function entrarComoOperador(page) {
  await page.goto("/");
  await page.getByRole("button", { name: "Operador" }).click();
  await page.getByRole("button", { name: "Iniciar sesión" }).click();
  await expect(page.getByRole("button", { name: "Cerrar sesión" })).toBeVisible();
}

test("la clave incorrecta no abre la sesión", async ({ page }) => {
  await page.goto("/");
  await page.locator("#form-sesion input[name='email']").fill("nadie@ecologistica.test");
  await page.locator("#form-sesion input[name='password']").fill("clave-mala");
  await page.getByRole("button", { name: "Iniciar sesión" }).click();
  await expect(page.locator("#mensaje-sesion")).not.toHaveText("");
  await expect(page.locator("#aplicacion")).toBeHidden();
});

test("el operador prepara los tres distritos y genera la ruta", async ({ page }) => {
  await entrarComoOperador(page);
  await page.getByRole("button", { name: "Preparar datos de El Tambo, Huancayo y Chilca" }).click();
  await page.locator("#menu").getByRole("button", { name: "Rutas" }).click();
  await page.getByRole("button", { name: "Generar ruta" }).click();
  await expect(page.locator("#detalle-ruta")).toContainText("El Tambo");
  await expect(page.locator("#detalle-ruta")).toContainText("Chilca");
});

test("reoptimizar responde con una de sus tres reglas", async ({ page }) => {
  await entrarComoOperador(page);
  await page.locator("#menu").getByRole("button", { name: "Rutas" }).click();
  await page.getByRole("button", { name: "Reoptimizar" }).click();
  await expect(page.locator("#mensaje-op")).toContainText(/reoptimiz|ruta activa|cambio operativo/i);
});

test("el pedido explosivo no se guarda", async ({ page }) => {
  await entrarComoOperador(page);
  await page.locator("#menu").getByRole("button", { name: "Puntos" }).click();
  await page.locator("#form-punto input[name='nombre']").fill("Mercado");
  await page.locator("#form-punto input[name='direccion']").fill("Jr. Real");
  await page.locator("#form-punto input[name='latitud']").fill("-12.07");
  await page.locator("#form-punto input[name='longitud']").fill("-75.21");
  await page.locator("#form-punto button[type='submit']").click();
  await page.locator("#menu").getByRole("button", { name: "Pedidos" }).click();
  await page.locator("#form-pedido select[name='tipo_carga']").selectOption("explosivo");
  await page.locator("#form-pedido input[name='peso_kg']").fill("10");
  await page.locator("#form-pedido button[type='submit']").click();
  await expect(page.locator("#mensaje-op")).toContainText("RN-016");
});

test("la ayuda y el ingreso responden 200", async ({ request }) => {
  const inicio = await request.get("/");
  const ayuda = await request.get("/ayuda.html");
  expect(inicio.status()).toBe(200);
  expect(ayuda.status()).toBe(200);
  const ausente = await request.get("/no-existe.html");
  expect(ausente.status()).toBe(404);
});
