# Etapa 2 - Arquitectura de 3 agentes

## Roles

- `orchestrator`: interfaz principal con el usuario, planifica, asigna permisos y decide estados.
- `coder`: implementa cambios de codigo dentro de rutas y comandos autorizados.
- `reviewer`: valida calidad (lint/tests/practicas), clasifica hallazgos y recomienda avanzar o no.

## Flujo base

1. Usuario envia solicitud al `orchestrator`.
2. `orchestrator` crea tarea (`created`) y plan (`planned`).
3. `orchestrator` delega al `coder` (`coding`) con permisos acotados.
4. `reviewer` analiza cambios (`reviewing`) y emite veredicto.
5. Si hay hallazgos: `needs_changes` y vuelve a `coder`.
6. Si falta decision humana: `awaiting_user`.
7. Usuario aprueba/rechaza: `approved` o `rejected`.

## Permisos por agente (version inicial)

- `orchestrator`
  - Puede cambiar estados.
  - Puede otorgar/revocar permisos temporales.
  - No modifica codigo directamente.
- `coder`
  - Puede editar solo `target_paths` autorizadas.
  - Puede ejecutar comandos permitidos (`pytest`, `ruff`, etc.).
  - Limite de archivos por tarea.
- `reviewer`
  - Solo lectura de repo + ejecucion de verificaciones.
  - No hace merge.
  - Puede proponer refactor, no aplicarlo sin aprobacion del orquestador.

## Reglas anti-riesgo

- Maximo 3 rondas `needs_changes -> coding`.
- Hallazgos por severidad: `critical`, `important`, `suggestion`.
- Aprobacion humana obligatoria antes de cerrar en `approved`.
