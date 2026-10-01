let token = "";

async function api(ruta, opciones = {}) {
  const encabezados = { "Content-Type": "application/json" };
  if (token) encabezados.Authorization = `Bearer ${token}`;
  const respuesta = await fetch(ruta, { ...opciones, headers: encabezados });
  return respuesta.json();
}

function texto(id, valor) {
  document.getElementById(id).textContent = valor;
}

function pintar(id, items, formato) {
  const lista = document.getElementById(id);
  lista.innerHTML = "";
  items.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = formato(item);
    lista.appendChild(li);
  });
}

async function recargar() {
  const vehiculos = await api("/api/vehiculos");
  const puntos = await api("/api/puntos");
  const pedidos = await api("/api/pedidos");
  pintar("lista-vehiculos", vehiculos.vehiculos || [], (v) => `${v.placa} · ${v.capacidad_kg} kg · ${v.estado}`);
  pintar("lista-puntos", puntos.puntos || [], (p) => `${p.nombre} · ${p.distrito} · ${p.latitud}, ${p.longitud} (${p.metodo_geolocalizacion})`);
  pintar("lista-pedidos", pedidos.pedidos || [], (p) => `Pedido ${p.pedido_id} · ${p.tipo_carga} · ${p.peso_kg} kg · ${p.estado}`);
  const select = document.getElementById("select-punto");
  select.innerHTML = "";
  (puntos.puntos || []).forEach((p) => {
    const opcion = document.createElement("option");
    opcion.value = p.punto_id;
    opcion.textContent = `${p.nombre} (${p.distrito})`;
    select.appendChild(opcion);
  });
}

document.getElementById("form-sesion").addEventListener("submit", async (evento) => {
  evento.preventDefault();
  const datos = new FormData(evento.target);
  const resultado = await api("/api/sesion", {
    method: "POST",
    body: JSON.stringify({ email: datos.get("email"), password: datos.get("password") }),
  });
  texto("mensaje-sesion", resultado.mensaje || `Sesión de ${resultado.nombre} (${resultado.rol}).`);
  if (!resultado.ok) return;
  token = resultado.token;
  document.getElementById("acceso").hidden = true;
  document.getElementById("operacion").hidden = false;
  texto("sesion-activa", `${resultado.nombre} · ${resultado.rol}`);
  await recargar();
});

document.getElementById("salir").addEventListener("click", () => {
  token = "";
  document.getElementById("operacion").hidden = true;
  document.getElementById("acceso").hidden = false;
  texto("mensaje-sesion", "Sesión cerrada.");
});

document.getElementById("form-vehiculo").addEventListener("submit", async (evento) => {
  evento.preventDefault();
  const datos = new FormData(evento.target);
  const resultado = await api("/api/vehiculos", {
    method: "POST",
    body: JSON.stringify({ placa: datos.get("placa"), capacidad_kg: Number(datos.get("capacidad_kg")) }),
  });
  texto("mensaje-op", resultado.mensaje || "Vehículo registrado.");
  if (resultado.ok) {
    evento.target.reset();
    await recargar();
  }
});

document.getElementById("form-punto").addEventListener("submit", async (evento) => {
  evento.preventDefault();
  const datos = new FormData(evento.target);
  const resultado = await api("/api/puntos", {
    method: "POST",
    body: JSON.stringify({
      nombre: datos.get("nombre"),
      direccion: datos.get("direccion"),
      distrito: datos.get("distrito"),
      latitud: Number(datos.get("latitud")),
      longitud: Number(datos.get("longitud")),
    }),
  });
  texto("mensaje-op", resultado.mensaje || "Punto registrado con geolocalización WGS84.");
  if (resultado.ok) await recargar();
});

document.getElementById("form-pedido").addEventListener("submit", async (evento) => {
  evento.preventDefault();
  const datos = new FormData(evento.target);
  const resultado = await api("/api/pedidos", {
    method: "POST",
    body: JSON.stringify({
      punto_id: Number(datos.get("punto_id")),
      peso_kg: Number(datos.get("peso_kg")),
      tipo_carga: datos.get("tipo_carga"),
    }),
  });
  texto("mensaje-op", resultado.mensaje || "Pedido registrado en estado PENDIENTE.");
  if (resultado.ok) await recargar();
});
