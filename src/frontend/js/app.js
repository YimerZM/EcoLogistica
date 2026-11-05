let token = "";
let rolActual = "";
let cache = { puntos: [], pedidos: [], rutas: [], vehiculos: [] };

const CUENTAS = [
  ["Administrador", "administrador@ecologistica.test", "admin123"],
  ["Operador", "operador@ecologistica.test", "operador123"],
  ["Planificador", "planificador@ecologistica.test", "plan12345"],
  ["Conductor", "conductor@ecologistica.test", "conductor1"],
  ["Responsable", "responsable@ecologistica.test", "responsable1"],
  ["Auditor", "auditor@ecologistica.test", "auditor123"],
];

const MENU = {
  Administrador: ["inicio", "usuarios", "vehiculos", "puntos", "pedidos", "rutas", "entregas", "indicadores", "parametros", "auditoria"],
  Operador: ["inicio", "vehiculos", "puntos", "pedidos", "rutas", "entregas", "indicadores"],
  Planificador: ["inicio", "pedidos", "rutas", "indicadores"],
  Conductor: ["inicio", "rutas", "entregas"],
  Responsable: ["inicio", "pedidos", "rutas", "indicadores"],
  Auditor: ["inicio", "usuarios", "vehiculos", "puntos", "pedidos", "rutas", "indicadores", "auditoria"],
  Contratante: ["inicio", "pedidos", "indicadores"],
};

const TITULOS = {
  inicio: "Panel",
  usuarios: "Usuarios",
  vehiculos: "Vehículos",
  puntos: "Puntos de entrega",
  pedidos: "Pedidos",
  rutas: "Rutas",
  entregas: "Entregas",
  indicadores: "Indicadores",
  parametros: "Parámetros",
  auditoria: "Auditoría",
};

const ESCRITURA = {
  usuarios: ["Administrador"],
  vehiculos: ["Administrador", "Operador"],
  puntos: ["Administrador", "Operador"],
  pedidos: ["Administrador", "Operador", "Contratante"],
  rutas: ["Administrador", "Operador", "Planificador"],
  entregas: ["Administrador", "Operador", "Conductor"],
  parametros: ["Administrador"],
  ejemplo: ["Administrador", "Operador"],
  exportar: ["Administrador", "Operador", "Planificador", "Responsable", "Auditor"],
};

function puede(clave) {
  return (ESCRITURA[clave] || []).includes(rolActual);
}

async function api(ruta, opciones = {}) {
  const encabezados = { "Content-Type": "application/json" };
  if (token) encabezados.Authorization = `Bearer ${token}`;
  const respuesta = await fetch(ruta, { ...opciones, headers: encabezados });
  return respuesta.json();
}

function aviso(valor, ok = false) {
  const nodo = document.getElementById("mensaje-op");
  nodo.textContent = valor || "";
  nodo.className = ok ? "aviso ok" : "aviso";
}

function estado(valor) {
  return `<span class="estado ${valor}">${valor}</span>`;
}

function tabla(id, columnas, filas, alElegir) {
  const nodo = document.getElementById(id);
  if (!filas.length) {
    nodo.innerHTML = `<tr><td class="vacio">No hay registros para mostrar.</td></tr>`;
    return;
  }
  const cabeza = `<tr>${columnas.map(([titulo]) => `<th>${titulo}</th>`).join("")}</tr>`;
  const cuerpo = filas.map((fila, indice) => {
    const celdas = columnas.map(([, formato]) => `<td>${formato(fila)}</td>`).join("");
    return `<tr data-i="${indice}">${celdas}</tr>`;
  }).join("");
  nodo.innerHTML = cabeza + cuerpo;
  if (!alElegir) return;
  nodo.querySelectorAll("tr[data-i]").forEach((tr) => {
    tr.addEventListener("click", () => {
      nodo.querySelectorAll("tr").forEach((otra) => otra.classList.remove("seleccionada"));
      tr.classList.add("seleccionada");
      alElegir(filas[Number(tr.dataset.i)]);
    });
  });
}

function xy(lat, lon) {
  const x = ((lon - (-75.4)) / 0.4) * 1000;
  const y = (((-11.9) - lat) / 0.3) * 640;
  return [x, y];
}

function mapaBase() {
  return `
    <rect width="1000" height="640" fill="#edf5ef"></rect>
    <path d="M80 90 C 240 40, 420 70, 620 50 C 780 36, 900 80, 940 140 L 900 560 C 760 600, 420 610, 120 560 Z" fill="#dcecde" stroke="#1f7a4d" stroke-width="3"></path>
    <text x="180" y="150" fill="#1a4334" font-size="28">El Tambo</text>
    <text x="430" y="300" fill="#1a4334" font-size="28">Huancayo</text>
    <text x="250" y="500" fill="#1a4334" font-size="28">Chilca</text>
    <text x="40" y="620" fill="#5d6b63" font-size="16">WGS84 · lat -12.20 a -11.90 · lon -75.40 a -75.00</text>`;
}

function dibujarPuntos(id, puntos, ruta) {
  const svg = document.getElementById(id);
  const marcas = puntos.map((p) => {
    const [x, y] = xy(p.latitud, p.longitud);
    return `<circle cx="${x}" cy="${y}" r="8" fill="#9a7433"></circle><text x="${x + 12}" y="${y + 4}" font-size="16" fill="#1b2420">${p.nombre}</text>`;
  }).join("");
  let linea = "";
  if (ruta) {
    const coords = ruta.paradas.map((p) => xy(p.latitud, p.longitud).join(" ")).join(" ");
    linea = `<polyline points="${coords}" fill="none" stroke="#10281f" stroke-width="4"></polyline>`;
  }
  svg.innerHTML = mapaBase() + linea + marcas;
}

async function recargar() {
  const [puntos, pedidos, rutas, vehiculos, indicadores] = await Promise.all([
    api("/api/puntos"),
    api(`/api/pedidos?estado=${document.getElementById("filtro-estado").value}`),
    api("/api/rutas"),
    api("/api/vehiculos"),
    api("/api/indicadores?periodo=todo"),
  ]);
  cache = {
    puntos: puntos.puntos || [],
    pedidos: pedidos.pedidos || [],
    rutas: rutas.rutas || [],
    vehiculos: vehiculos.vehiculos || [],
  };
  pintarMetricas(indicadores);
  pintarUsuarios();
  pintarVehiculos();
  pintarPuntos();
  pintarPedidos();
  pintarRutas();
  pintarEntregas();
  if (rolActual === "Administrador" || rolActual === "Auditor") {
    const auditoria = await api("/api/auditoria");
    tabla("tabla-auditoria", [
      ["Cuándo", (e) => e.fecha],
      ["Usuario", (e) => e.email],
      ["Operación", (e) => e.operacion],
      ["Resultado", (e) => estado(e.resultado)],
      ["Detalle", (e) => e.detalle],
    ], (auditoria.eventos || []).slice().reverse());
  }
}

function pintarMetricas(datos) {
  const items = datos.ok
    ? [
        ["Pedidos pendientes", datos.pendientes],
        ["En ruta", datos.en_ruta],
        ["Kilómetros", datos.km],
        ["CO₂ estimado (kg)", datos.co2_kg],
      ]
    : [["Operación", "—"], ["En ruta", "—"], ["Kilómetros", "—"], ["CO₂ estimado (kg)", "—"]];
  document.getElementById("metricas").innerHTML = items.map(([nombre, valor]) => `<article class="metrica"><span>${nombre}</span><strong>${valor}</strong></article>`).join("");
}

async function pintarUsuarios() {
  if (!MENU[rolActual].includes("usuarios")) return;
  const usuarios = await api("/api/usuarios");
  tabla("tabla-usuarios", [
    ["Correo", (u) => u.email],
    ["Nombre", (u) => u.nombre],
    ["Rol", (u) => u.rol],
    ["Estado", (u) => estado(u.estado)],
  ], usuarios.usuarios || []);
}

function pintarVehiculos() {
  tabla("tabla-vehiculos", [
    ["Placa", (v) => v.placa],
    ["Capacidad", (v) => `${v.capacidad_kg} kg`],
    ["Estado", (v) => estado(v.estado)],
    ["Conductor", (v) => v.conductor_email || "Sin asignar"],
  ], cache.vehiculos);
}

function pintarPuntos() {
  tabla("tabla-puntos", [
    ["Nombre", (p) => p.nombre],
    ["Distrito", (p) => p.distrito],
    ["Dirección", (p) => p.direccion],
    ["WGS84", (p) => `${p.latitud}, ${p.longitud}`],
  ], cache.puntos);
  dibujarPuntos("mapa-puntos", cache.puntos);
  const select = document.getElementById("select-punto");
  select.innerHTML = cache.puntos.map((p) => `<option value="${p.punto_id}">${p.nombre} (${p.distrito})</option>`).join("");
}

function pintarPedidos() {
  tabla("tabla-pedidos", [
    ["Pedido", (p) => p.pedido_id],
    ["Distrito", (p) => p.distrito],
    ["Peso", (p) => `${p.peso_kg} kg`],
    ["Estado", (p) => estado(p.estado)],
    ["Contratante", (p) => p.contratante_email || "—"],
  ], cache.pedidos);
}

function pintarRutas() {
  tabla("tabla-rutas", [
    ["Ruta", (r) => r.ruta_id],
    ["Placa", (r) => r.placa],
    ["Estado", (r) => estado(r.estado)],
    ["Km", (r) => r.km],
    ["Carga", (r) => `${r.peso_kg} / ${r.capacidad_kg} kg`],
  ], cache.rutas, (ruta) => {
    document.getElementById("titulo-ruta").textContent = `Ruta ${ruta.ruta_id} · ${ruta.placa}`;
    document.getElementById("detalle-ruta").textContent = ruta.paradas.map((p) => `${p.orden}. ${p.nombre} (${p.distrito})`).join(" → ");
    dibujarPuntos("mapa-ruta", ruta.paradas, ruta);
  });
  const activa = cache.rutas.find((r) => r.estado === "ACTIVA");
  if (activa) {
    document.getElementById("titulo-ruta").textContent = `Ruta ${activa.ruta_id} · ${activa.placa}`;
    document.getElementById("detalle-ruta").textContent = activa.paradas.map((p) => `${p.orden}. ${p.nombre} (${p.distrito})`).join(" → ");
    dibujarPuntos("mapa-ruta", activa.paradas, activa);
  } else {
    dibujarPuntos("mapa-ruta", cache.puntos);
  }
}

function pintarEntregas() {
  const asignados = cache.pedidos.filter((p) => p.estado === "EN_RUTA");
  document.getElementById("select-entrega").innerHTML = asignados.map((p) => `<option value="${p.pedido_id}">Pedido ${p.pedido_id} · ${p.distrito} · ${p.peso_kg} kg</option>`).join("");
}

function mostrar(panel) {
  Object.keys(TITULOS).forEach((nombre) => {
    document.getElementById(`panel-${nombre}`).hidden = nombre !== panel;
  });
  document.getElementById("titulo-panel").textContent = TITULOS[panel];
  document.querySelectorAll("#menu button[data-panel]").forEach((boton) => {
    boton.classList.toggle("activo", boton.dataset.panel === panel);
  });
}

function armarMenu() {
  const menu = document.getElementById("menu");
  menu.innerHTML = `<strong>EcoLogística</strong>` + MENU[rolActual].map((panel) => `<button type="button" data-panel="${panel}">${panel === "puntos" ? "Puntos" : TITULOS[panel]}</button>`).join("");
  menu.querySelectorAll("button").forEach((boton) => boton.addEventListener("click", () => mostrar(boton.dataset.panel)));
  ["form-usuario", "form-usuario-editar"].forEach((id) => { document.getElementById(id).hidden = !puede("usuarios"); });
  document.getElementById("form-vehiculo").hidden = !puede("vehiculos");
  document.getElementById("form-punto").hidden = !puede("puntos");
  document.getElementById("form-pedido").hidden = !puede("pedidos");
  document.getElementById("generar-ruta").hidden = !puede("rutas");
  document.getElementById("reoptimizar").hidden = !puede("rutas");
  document.getElementById("form-entrega").hidden = !puede("entregas");
  document.getElementById("form-parametros").hidden = !puede("parametros");
  document.getElementById("cargar-ejemplo").hidden = !puede("ejemplo");
  document.getElementById("exportar").hidden = !puede("exportar");
}

document.getElementById("cuentas").innerHTML = CUENTAS.map(([nombre]) => `<button type="button" data-cuenta="${nombre}">${nombre}</button>`).join("");
document.getElementById("cuentas").addEventListener("click", (evento) => {
  const cuenta = CUENTAS.find(([nombre]) => nombre === evento.target.dataset.cuenta);
  if (!cuenta) return;
  const formulario = document.getElementById("form-sesion");
  formulario.email.value = cuenta[1];
  formulario.password.value = cuenta[2];
});

document.getElementById("form-sesion").addEventListener("submit", async (evento) => {
  evento.preventDefault();
  const datos = new FormData(evento.target);
  const resultado = await api("/api/sesion", {
    method: "POST",
    body: JSON.stringify({ email: datos.get("email"), password: datos.get("password") }),
  });
  const mensaje = document.getElementById("mensaje-sesion");
  mensaje.textContent = resultado.ok ? "" : (resultado.mensaje || "Credenciales no válidas.");
  if (!resultado.ok) return;
  token = resultado.token;
  rolActual = resultado.rol;
  document.getElementById("acceso").hidden = true;
  document.getElementById("aplicacion").hidden = false;
  document.getElementById("sesion-activa").innerHTML = `${resultado.nombre} <span class="rol">${resultado.rol}</span>`;
  armarMenu();
  mostrar("inicio");
  await recargar();
});

document.getElementById("salir").addEventListener("click", () => {
  token = "";
  rolActual = "";
  document.getElementById("aplicacion").hidden = true;
  document.getElementById("acceso").hidden = false;
  document.getElementById("mensaje-sesion").textContent = "Sesión cerrada.";
});

document.getElementById("filtro-estado").addEventListener("change", recargar);

document.getElementById("form-usuario").addEventListener("submit", async (evento) => {
  evento.preventDefault();
  const datos = new FormData(evento.target);
  const resultado = await api("/api/usuarios", { method: "POST", body: JSON.stringify(Object.fromEntries(datos)) });
  aviso(resultado.mensaje || "Usuario registrado.", resultado.ok);
  if (resultado.ok) { evento.target.reset(); await recargar(); }
});

document.getElementById("form-usuario-editar").addEventListener("submit", async (evento) => {
  evento.preventDefault();
  const datos = new FormData(evento.target);
  const resultado = await api("/api/usuarios", { method: "PUT", body: JSON.stringify(Object.fromEntries(datos)) });
  aviso(resultado.mensaje || "Usuario actualizado.", resultado.ok);
  if (resultado.ok) await recargar();
});

document.getElementById("form-vehiculo").addEventListener("submit", async (evento) => {
  evento.preventDefault();
  const datos = new FormData(evento.target);
  const resultado = await api("/api/vehiculos", {
    method: "POST",
    body: JSON.stringify({ placa: datos.get("placa"), capacidad_kg: Number(datos.get("capacidad_kg")) }),
  });
  aviso(resultado.mensaje || "Vehículo registrado.", resultado.ok);
  if (resultado.ok) { evento.target.reset(); await recargar(); }
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
  aviso(resultado.mensaje || "Punto registrado con geolocalización WGS84.", resultado.ok);
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
      contratante_email: datos.get("contratante_email"),
    }),
  });
  aviso(resultado.mensaje || "Pedido registrado en estado PENDIENTE.", resultado.ok);
  if (resultado.ok) await recargar();
});

document.getElementById("generar-ruta").addEventListener("click", async () => {
  const resultado = await api("/api/rutas", { method: "POST", body: "{}" });
  aviso(resultado.mensaje, resultado.ok);
  await recargar();
  mostrar("rutas");
});

document.getElementById("reoptimizar").addEventListener("click", async () => {
  const resultado = await api("/api/rutas/reoptimizar", { method: "POST", body: "{}" });
  aviso(resultado.mensaje, resultado.ok);
  await recargar();
});

document.getElementById("form-entrega").addEventListener("submit", async (evento) => {
  evento.preventDefault();
  const datos = new FormData(evento.target);
  const resultado = await api("/api/entregas", {
    method: "POST",
    body: JSON.stringify({
      pedido_id: Number(datos.get("pedido_id")),
      resultado: datos.get("resultado"),
      motivo: datos.get("motivo"),
    }),
  });
  aviso(resultado.mensaje || "Entrega registrada.", resultado.ok);
  if (resultado.ok) await recargar();
});

document.getElementById("ver-indicadores").addEventListener("click", async () => {
  const periodo = document.getElementById("periodo").value;
  const datos = await api(`/api/indicadores?periodo=${periodo}`);
  if (!datos.ok) {
    document.getElementById("indicadores").innerHTML = "";
    aviso(datos.mensaje);
    return;
  }
  aviso(`Indicadores de ${datos.periodo}.`, true);
  document.getElementById("indicadores").innerHTML = [
    ["Pendientes", datos.pendientes],
    ["En ruta", datos.en_ruta],
    ["Entregados", datos.entregados],
    ["Incidencias", datos.incidencias],
    ["Carga (kg)", datos.kg],
    ["Recorrido (km)", datos.km],
    ["CO₂ (kg)", datos.co2_kg],
  ].map(([nombre, valor]) => `<article class="metrica"><span>${nombre}</span><strong>${valor}</strong></article>`).join("");
});

document.getElementById("form-parametros").addEventListener("submit", async (evento) => {
  evento.preventDefault();
  const datos = new FormData(evento.target);
  const resultado = await api("/api/parametros", {
    method: "PUT",
    body: JSON.stringify({
      factor_emision_kg_por_km: Number(datos.get("factor_emision_kg_por_km")),
      velocidad_kmh: Number(datos.get("velocidad_kmh")),
    }),
  });
  aviso(resultado.mensaje || "Parámetros actualizados.", resultado.ok);
});

document.getElementById("exportar").addEventListener("click", async () => {
  const resultado = await api("/api/exportar/pedidos");
  if (!resultado.ok) { aviso(resultado.mensaje); return; }
  const blob = new Blob([resultado.contenido], { type: "text/csv" });
  const enlace = document.createElement("a");
  enlace.href = URL.createObjectURL(blob);
  enlace.download = resultado.archivo;
  enlace.click();
  aviso("Archivo de pedidos generado.", true);
});

document.getElementById("cargar-ejemplo").addEventListener("click", async () => {
  const resultado = await api("/api/ejemplo", { method: "POST", body: "{}" });
  aviso(resultado.mensaje, resultado.ok);
  if (resultado.ok) await recargar();
});
