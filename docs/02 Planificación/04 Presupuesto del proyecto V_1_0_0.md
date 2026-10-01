# Presupuesto del proyecto

[← Volver al README Principal](../../README.md)

## 1. Información general

| Campo        | Información                     |
| ------------ | ------------------------------- |
| Proyecto     | EcoLogística                    |
| Fase         | 02 - Planificación del Proyecto |
| Enfoque      | Híbrido                         |
| Moneda       | USD                             |
| Contingencia | 12 %                            |
| Ámbito       | El Tambo, Huancayo y Chilca     |
| Versión      | V_1_0_0                         |

---

# 2. Introducción

El presupuesto de EcoLogística considera los recursos humanos, herramientas de software, infraestructura cloud y otros servicios necesarios para desarrollar, probar y desplegar el sistema.

El presupuesto se divide en:

* CAPEX / inversión en desarrollo.
* Licencias y herramientas.
* OPEX / operación e infraestructura.
* Contingencia.

Los costos de recursos humanos se calculan utilizando:

```text
Costo = Horas × Tarifa por hora
```

Los valores presentados corresponden a una estimación académica para efectos de planificación del PFA.

---

# 3. CAPEX - Recursos humanos

## 3.1 Equipo estimado

| Rol                    |   Horas | Tarifa USD/h | Costo USD |
| ---------------------- | ------: | -----------: | --------: |
| Project Manager        |      80 |           18 |     1,440 |
| Software Architect     |      60 |           22 |     1,320 |
| Senior Developer       |     100 |           20 |     2,000 |
| Junior Developer       |     160 |           12 |     1,920 |
| QA Engineer            |      80 |           14 |     1,120 |
| UI/UX Designer         |      50 |           14 |       700 |
| **Total CAPEX RR.HH.** | **530** |            — | **8,500** |

### Justificación

El Project Manager se encarga de la coordinación, seguimiento del cronograma, riesgos, presupuesto y comunicación.

El Software Architect define la arquitectura, componentes, integración, seguridad y decisiones técnicas principales.

El Senior Developer participa en las funcionalidades de mayor complejidad, especialmente aquellas relacionadas con planificación y optimización de rutas.

El Junior Developer participa en funcionalidades de menor complejidad, mantenimiento y apoyo al desarrollo.

El QA Engineer se encarga de pruebas funcionales, integración, regresión y validación de criterios de aceptación.

El UI/UX Designer desarrolla y valida la experiencia e interfaz de usuario.

---

# 4. Licencias y herramientas

Se consideran herramientas necesarias para desarrollo, gestión, diseño, calidad y colaboración.

| Herramienta / Servicio             | Cantidad | Costo estimado USD | Tipo                     |
| ---------------------------------- | -------: | -----------------: | ------------------------ |
| IDE / herramientas de desarrollo   |        1 |                  0 | Gratuito                 |
| GitHub                             |        1 |                  0 | Gratuito / académico     |
| Jira                               |        1 |                  0 | Plan inicial / académico |
| Figma                              |        1 |                  0 | Plan inicial             |
| SonarQube                          |        1 |                  0 | Community / académico    |
| Herramientas de documentación      |        1 |                  0 | Gratuito                 |
| **Total licencias y herramientas** |          |              **0** |                          |

> Los costos pueden variar según el plan comercial, cantidad de usuarios y condiciones de contratación. Para el PFA se considera el uso de planes gratuitos, académicos o comunitarios cuando estén disponibles.

---

# 5. OPEX - Infraestructura cloud

Se considera una infraestructura inicial para ambientes de desarrollo, pruebas y despliegue.

| Servicio                    | Periodo estimado | Costo mensual USD | Costo estimado USD |
| --------------------------- | ---------------: | ----------------: | -----------------: |
| Servidor / aplicación cloud |          6 meses |                35 |                210 |
| Base de datos administrada  |          6 meses |                30 |                180 |
| Almacenamiento y respaldos  |          6 meses |                10 |                 60 |
| Dominio                     |            1 año |                15 |                 15 |
| SSL                         |            1 año |                 0 |                  0 |
| CI/CD                       |          6 meses |                10 |                 60 |
| Monitoreo y logs            |          6 meses |                10 |                 60 |
| **Total OPEX**              |                  |                   |            **585** |

---

# 6. Resumen financiero

| Categoría                      |     Costo USD |
| ------------------------------ | ------------: |
| CAPEX - Recursos humanos       |         8,500 |
| Licencias y herramientas       |             0 |
| OPEX - Cloud e infraestructura |           585 |
| **Subtotal**                   |     **9,085** |
| Contingencia 12 %              |  **1,090.20** |
| **TOTAL ESTIMADO**             | **10,175.20** |

---

# 7. Contingencia

Se establece una contingencia del **12 %** sobre el subtotal del proyecto.

```text
Subtotal = USD 9,085

Contingencia = 9,085 × 0.12

Contingencia = USD 1,090.20
```

Por lo tanto:

```text
Presupuesto total =
9,085 + 1,090.20

Presupuesto total =
USD 10,175.20
```

La contingencia permite cubrir variaciones no previstas relacionadas con:

* Incremento de horas de desarrollo.
* Corrección de defectos críticos.
* Incremento de infraestructura.
* Necesidad de herramientas adicionales.
* Cambios técnicos.
* Retrabajo.
* Problemas de integración.
* Actividades adicionales de pruebas.

---

# 8. Consolidación del presupuesto

El presupuesto se consolida considerando que el principal componente de inversión del proyecto corresponde al trabajo especializado del equipo.

Los recursos humanos representan la mayor parte del presupuesto debido a que EcoLogística requiere actividades de análisis, diseño, desarrollo, pruebas, arquitectura y gestión.

La infraestructura cloud representa un costo operativo menor durante la etapa inicial, pero deberá monitorearse para evitar incrementos inesperados.

El uso de herramientas gratuitas, comunitarias o académicas permite reducir los costos iniciales del proyecto sin eliminar las actividades de control de calidad, desarrollo y gestión.

---

# 9. Distribución porcentual

Tomando como referencia el subtotal de USD 9,085:

| Categoría        | Costo USD | Participación aproximada |
| ---------------- | --------: | -----------------------: |
| Recursos humanos |     8,500 |                  93.56 % |
| OPEX cloud       |       585 |                   6.44 % |
| Licencias        |         0 |                      0 % |
| **Total**        | **9,085** |                **100 %** |

Esto demuestra que el principal costo del proyecto está relacionado con el recurso humano especializado.

---

# 10. Relación con los riesgos

El presupuesto contempla una reserva de contingencia para responder a riesgos identificados en el Registro de Riesgos.

| Riesgo                        | Posible impacto presupuestario                                    |
| ----------------------------- | ----------------------------------------------------------------- |
| Retraso del desarrollo        | Incremento de horas de trabajo.                                   |
| Fallos en generación de rutas | Horas adicionales de desarrollo y pruebas.                        |
| Vulnerabilidades de seguridad | Trabajo adicional de corrección y auditoría.                      |
| Bajo rendimiento              | Optimización de infraestructura y código.                         |
| Problemas cloud               | Incremento de consumo o necesidad de infraestructura alternativa. |
| Cambios de alcance            | Horas adicionales de análisis y desarrollo.                       |

---

# 11. Control presupuestario

El presupuesto deberá revisarse periódicamente durante la ejecución del proyecto.

Se deberán controlar:

1. Horas planificadas frente a horas ejecutadas.
2. Costos de infraestructura.
3. Consumo de servicios cloud.
4. Herramientas utilizadas.
5. Variaciones respecto al presupuesto inicial.
6. Uso de la reserva de contingencia.

Cualquier incremento significativo deberá ser registrado y justificado dentro de la gestión del proyecto.

---

# 12. Conclusión

El presupuesto estimado para EcoLogística asciende a **USD 10,175.20**, incluyendo una contingencia del 12 %.

La mayor inversión corresponde al recurso humano, debido a la necesidad de contar con perfiles especializados para arquitectura, desarrollo, pruebas, diseño y gestión.

El presupuesto se encuentra alineado con el enfoque híbrido del proyecto, permitiendo controlar los costos mediante planificación inicial y realizar ajustes durante los ciclos iterativos de desarrollo.

La reserva de contingencia proporciona capacidad financiera para responder a riesgos técnicos, operativos y de gestión sin comprometer inmediatamente el presupuesto base.

## Control de cambios

| Versión | Fecha | Descripción | Responsable |
|---|---|---|---|
| 1.0.0 | 17/09/2026 | Presupuesto inicial de USD 10,175.20. | Equipo EcoLogística |
| 1.1.0 | 01/10/2026 | El acta de constitución usa este mismo tope. No hubo cambio de monto en el Sprint 2. | ZEVALLOS MELENDRES YIMER EDYSON |

[← Volver al README Principal](../../README.md)
