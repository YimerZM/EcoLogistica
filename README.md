# EcoLogistica

Proyecto final. Sistema de optimización de rutas sostenibles para El Tambo, Huancayo y Chilca.

Equipo: ZEVALLOS MELENDRES YIMER EDYSON (director), POMACHAGUA YAPIAS BRYAN ANTONY y CAJAMALQUI DAVILA JOSEMARIA PIERO.

## Fase 01: Inicio

1. [01. Selección del enfoque del proyecto V_1_0_0](docs/01%20Inicio/01.%20Selección%20del%20enfoque%20del%20proyecto%20V_1_0_0.md)
2. [02. Acta de constitución V_1_0_0](docs/01%20Inicio/02.%20Acta%20de%20constitución%20V_1_0_0.md)
3. [03. Declaración de la visión V_1_0_0](docs/01%20Inicio/03.%20Declaración%20de%20la%20visión%20V_1_0_0.md)
4. [04. Registro de supuestos y restricciones V_1_0_0](docs/01%20Inicio/04.%20Registro%20de%20supuestos%20y%20restricciones%20V_1_0_0.md)
5. [05. Registro de interesados V_1_0_0](docs/01%20Inicio/05.%20Registro%20de%20interesados%20V_1_0_0.md)
6. [06. Requisitos funcionales V_1_0_0](docs/01%20Inicio/06.%20Requisitos%20funcionales%20V_1_0_0.md)
7. [07. Requisitos no funcionales V_1_0_0](docs/01%20Inicio/07.%20Requisitos%20no%20funcionales%20V_1_0_0.md)
8. [08. Usuarios V_1_0_0](docs/01%20Inicio/08.%20Usuarios%20V_1_0_0.md)
9. [09. Reglas de negocio V_1_0_0](docs/01%20Inicio/09.%20Reglas%20de%20negocio%20V_1_0_0.md)
10. [10. Stack tecnológico V_1_0_0](docs/01%20Inicio/10.%20Stack%20tecnológico%20V_1_0_0.md)
11. [11. Base de datos V_1_0_0](docs/01%20Inicio/11.%20Base%20de%20datos%20V_1_0_0.md)
12. [12. Modelo C4 V_1_0_0](docs/01%20Inicio/12.%20Modelo%20C4%20V_1_0_0.md)
13. [13. Restricciones V_1_0_0](docs/01%20Inicio/13.%20Restricciones%20V_1_0_0.md)

## Fase 02: Planificación del Proyecto

1. [01 Transformando a ágil V_1_0_0](docs/02%20Planificación/01%20Transformando%20a%20ágil%20V_1_0_0.md)
2. [02 Artefactos Jira V_1_0_0](docs/02%20Planificación/02%20Artefactos%20Jira%20V_1_0_0.md)
3. [03 Registro de riesgos V_1_0_0](docs/02%20Planificación/03%20Registro%20de%20riesgos%20V_1_0_0.md)
4. [04 Presupuesto del proyecto V_1_0_0](docs/02%20Planificación/04%20Presupuesto%20del%20proyecto%20V_1_0_0.md)

## Fase 03: Implementación

Sprint 2. Los documentos están en `docs/03 Implementación`.

1. [01 Informe de estado del proyecto V_1_0_0](docs/03%20Implementación/01%20Informe%20de%20estado%20del%20proyecto%20V_1_0_0.md)
2. [02 Registro de Impedimentos V_1_0_0](docs/03%20Implementación/02%20Registro%20de%20Impedimentos%20V_1_0_0.md)
3. [03 Revisión del Sprint V_1_0_0](docs/03%20Implementación/03%20Revisión%20del%20Sprint%20V_1_0_0.md)
4. [04 Retrospectiva del Sprint V_1_0_0](docs/03%20Implementación/04%20Retrospectiva%20del%20Sprint%20V_1_0_0.md)

## Código

- `src/frontend`: interfaz del incremento.
- `src/backend`: reglas, casos de uso y API.

Desde `src/backend`:

```text
python -m unittest tests.test_reglas
python -m ecologistica
```

La aplicación queda en http://127.0.0.1:8765. Usuario de prueba del operador: `operador@ecologistica.test` / `operador123`.
