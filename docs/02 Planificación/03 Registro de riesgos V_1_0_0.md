# Registro de riesgos

[← Volver al README Principal](../../README.md)

## 1. Información general

| Campo       | Información                     |
| ----------- | ------------------------------- |
| Proyecto    | EcoLogística                    |
| Fase        | 02 - Planificación del Proyecto |
| Enfoque     | Híbrido                         |
| Ámbito      | El Tambo, Huancayo y Chilca     |
| Metodología | Scrum                           |
| Versión     | V_1_0_0                         |

---

# 2. Introducción

El registro de riesgos permite identificar, analizar y controlar eventos que podrían afectar el alcance, cronograma, presupuesto, calidad o funcionamiento del proyecto EcoLogística.

La evaluación utiliza una matriz cuantitativa basada en la probabilidad de ocurrencia y el impacto que tendría cada riesgo sobre el proyecto.

---

# 3. Metodología de evaluación

La severidad del riesgo se calcula mediante:

```text
Severidad = Probabilidad × Impacto
```

Ambas variables utilizan una escala de 1 a 5.

## 3.1 Probabilidad

| Valor | Nivel    | Descripción                                    |
| ----: | -------- | ---------------------------------------------- |
|     1 | Muy baja | Es poco probable que ocurra.                   |
|     2 | Baja     | Puede ocurrir ocasionalmente.                  |
|     3 | Media    | Existe una posibilidad moderada de ocurrencia. |
|     4 | Alta     | Es probable que ocurra.                        |
|     5 | Muy alta | Es altamente probable que ocurra.              |

## 3.2 Impacto

| Valor | Nivel          | Descripción                                           |
| ----: | -------------- | ----------------------------------------------------- |
|     1 | Insignificante | Efecto mínimo sobre el proyecto.                      |
|     2 | Menor          | Efecto reducido y fácilmente controlable.             |
|     3 | Moderado       | Puede generar retrasos o retrabajo.                   |
|     4 | Grave          | Puede afectar significativamente el proyecto.         |
|     5 | Catastrófico   | Puede comprometer objetivos importantes del proyecto. |

## 3.3 Severidad

| Puntaje | Nivel |
| ------: | ----- |
|   1 - 6 | Bajo  |
|  8 - 12 | Medio |
| 15 - 25 | Alto  |

---

# 4. Matriz de riesgos

| ID    | Descripción                                          | Categoría        | Prob. | Imp. |  Severidad | Mitigación preventiva                                                        | Contingencia reactiva                                                                                   | Responsable                     |
| ----- | ---------------------------------------------------- | ---------------- | ----: | ---: | ---------: | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- | ------------------------------- |
| R-001 | Retraso en el desarrollo de funcionalidades críticas | Cronograma       |     4 |    4 |  16 - Alto | Priorizar historias críticas y realizar seguimiento semanal del Sprint.      | Repriorizar backlog y reducir trabajo de menor prioridad.                                               | Project Manager                 |
| R-002 | Requisitos incompletos o ambiguos                    | Alcance          |     3 |    4 | 12 - Medio | Validar requisitos y criterios de aceptación antes del desarrollo.           | Realizar refinamiento y actualizar las Historias de Usuario.                                            | Product Owner                   |
| R-003 | Fallos en la generación de rutas                     | Técnico          |     3 |    5 |  15 - Alto | Realizar pruebas con diferentes escenarios y datos de operación.             | Desactivar temporalmente la optimización avanzada y utilizar una generación de ruta básica.             | Arquitecto de Software          |
| R-004 | Pérdida o corrupción de información                  | Datos            |     2 |    5 | 10 - Medio | Implementar respaldos y validaciones de integridad.                          | Restaurar información desde el último respaldo válido.                                                  | Desarrollador Backend           |
| R-005 | Vulnerabilidades de seguridad                        | Seguridad        |     3 |    5 |  15 - Alto | Aplicar autenticación, autorización, análisis estático y revisión de código. | Corregir inmediatamente la vulnerabilidad y limitar temporalmente la funcionalidad afectada.            | Arquitecto de Software          |
| R-006 | Baja adopción por parte de usuarios                  | Usuario          |     3 |    3 |  9 - Medio | Realizar pruebas de usabilidad y recoger retroalimentación.                  | Ajustar interfaz, flujos y documentación según los problemas identificados.                             | UI/UX Designer                  |
| R-007 | Bajo rendimiento con incremento de datos             | Técnico          |     3 |    4 | 12 - Medio | Optimizar consultas y ejecutar pruebas de carga.                             | Optimizar consultas críticas y limitar temporalmente operaciones de alto consumo.                       | Desarrollador Backend           |
| R-008 | Indisponibilidad del servicio cloud                  | Infraestructura  |     2 |    4 |  8 - Medio | Configurar monitoreo, respaldos y mecanismos de recuperación.                | Restaurar el servicio o utilizar una instancia alternativa disponible.                                  | DevOps                          |
| R-009 | Cambios frecuentes en el alcance                     | Gestión          |     4 |    3 | 12 - Medio | Utilizar backlog priorizado y control de cambios.                            | Repriorizar historias para mantener el objetivo del Sprint y del Release.                               | Project Manager / Product Owner |
| R-010 | Falta de disponibilidad del equipo                   | Recursos humanos |     3 |    4 | 12 - Medio | Distribuir responsabilidades y mantener documentación actualizada.           | Redistribuir tareas y ajustar el Sprint Backlog.                                                        | Project Manager                 |
| R-011 | Errores durante la integración de componentes        | Técnico          |     3 |    4 | 12 - Medio | Utilizar control de versiones, Pull Requests y pruebas automatizadas.        | Revertir cambios defectuosos y realizar una integración controlada.                                     | Desarrolladores                 |
| R-012 | Incremento inesperado de costos de infraestructura   | Financiero       |     2 |    4 |  8 - Medio | Establecer límites de consumo y monitorear costos cloud.                     | Reducir recursos no esenciales y ajustar la infraestructura.                                            | Project Manager                 |
| R-013 | Fallos en el registro de entregas                    | Operativo        |     3 |    4 | 12 - Medio | Validar flujos y ejecutar pruebas funcionales.                               | Registrar temporalmente la información mediante procedimiento alternativo y sincronizar posteriormente. | QA Engineer                     |
| R-014 | Problemas de compatibilidad entre navegadores        | Técnico          |     2 |    3 |   6 - Bajo | Probar el sistema en los navegadores definidos como compatibles.             | Corregir estilos o funcionalidades incompatibles antes del Release.                                     | Frontend Developer              |
| R-015 | Documentación técnica desactualizada                 | Calidad          |     3 |    3 |  9 - Medio | Incluir actualización documental dentro de la Definition of Done.            | Actualizar documentación antes del cierre del Release.                                                  | Equipo técnico                  |

---

# 5. Priorización de riesgos

Los riesgos de mayor atención son:

### R-001 - Retraso en funcionalidades críticas

Tiene una severidad de **16 - Alto** debido a la probabilidad elevada de retrasos y su impacto directo sobre el cronograma.

### R-003 - Fallos en la generación de rutas

Tiene una severidad de **15 - Alto**, debido a que la generación de rutas constituye una funcionalidad técnicamente compleja y de alto valor para EcoLogística.

### R-005 - Vulnerabilidades de seguridad

Tiene una severidad de **15 - Alto**, debido a que una vulnerabilidad podría comprometer información y funcionamiento del sistema.

---

# 6. Estrategia general de respuesta

Para los riesgos identificados se utilizarán cuatro estrategias:

| Estrategia | Aplicación                                                               |
| ---------- | ------------------------------------------------------------------------ |
| Mitigar    | Reducir la probabilidad o impacto mediante acciones preventivas.         |
| Evitar     | Modificar la planificación para eliminar la causa del riesgo.            |
| Transferir | Delegar parte del riesgo a un tercero o servicio especializado.          |
| Aceptar    | Reconocer el riesgo y establecer una contingencia en caso de ocurrencia. |

La estrategia predominante para EcoLogística será **mitigar**, especialmente en riesgos técnicos, de seguridad, cronograma y calidad.

---

# 7. Seguimiento

El registro de riesgos deberá revisarse durante la planificación y ejecución de cada Sprint.

Durante las reuniones de seguimiento se deberá verificar:

* Nuevos riesgos identificados.
* Cambios en la probabilidad.
* Cambios en el impacto.
* Efectividad de las medidas preventivas.
* Activación de contingencias.
* Riesgos cerrados.
* Riesgos que hayan incrementado su severidad.

---

# 8. Conclusión

La matriz de riesgos proporciona un mecanismo cuantitativo para priorizar las amenazas que pueden afectar el proyecto EcoLogística.

La utilización de Probabilidad × Impacto permite enfocar los recursos de gestión en los riesgos de mayor severidad, especialmente aquellos relacionados con retrasos, generación de rutas y seguridad.

El registro deberá mantenerse actualizado durante los Sprints para que forme parte del proceso de adaptación propio del enfoque híbrido.

## Control de cambios

| Versión | Fecha | Descripción | Responsable |
|---|---|---|---|
| 1.0.0 | 17/09/2026 | Matriz inicial de riesgos. | Equipo EcoLogística |
| 1.1.0 | 01/10/2026 | Se confirma el riesgo de carga prohibida y de geolocalización fuera de WGS84, ya tratados como RN-016 y como restricción C-04. | ZEVALLOS MELENDRES YIMER EDYSON |

[← Volver al README Principal](../../README.md)
