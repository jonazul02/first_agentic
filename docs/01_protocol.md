# Etapa 1 - Protocolo base

## 1) Que entra

La entrada principal es una `TaskRequest` con:

- `title`: titulo corto de la tarea
- `description`: detalle de lo solicitado
- `task_type`: `feature`, `bugfix`, `test`, `refactor`, `docs`
- `requested_by`: identificador de quien solicita
- `target_paths`: rutas candidatas a modificar

## 2) Que sale

La salida principal es un `TaskResult` con:

- `task_id`
- `final_status`
- `summary`
- `changed_files`
- `test_status`
- `risk_level`
- `recommendation`

## 3) Permisos

Permisos iniciales por rol:

- `orchestrator`: planificar, mover estado, pedir aprobacion humana
- `coder`: editar rutas permitidas, ejecutar comandos de build/test autorizados
- `reviewer`: leer diff, ejecutar lint/tests, emitir observaciones

En esta etapa no hay integracion git real; solo contrato de permisos.

## 4) Estados de tarea

Estados iniciales:

- `created`
- `planned`
- `coding`
- `reviewing`
- `needs_changes`
- `approved`
- `rejected`
- `awaiting_user`

## 5) Reglas de transicion

Flujo base propuesto:

- `created -> planned`
- `planned -> coding`
- `coding -> reviewing`
- `reviewing -> needs_changes | approved | rejected | awaiting_user`
- `needs_changes -> coding`
- `awaiting_user -> approved | rejected | needs_changes`

Cierre:

- `approved` y `rejected` son estados terminales.

## 6) Guardrails iniciales

- Maximo de rondas coder-reviewer: 3
- Coder no puede modificar mas de N archivos (configurable)
- Siempre debe existir recomendacion final del reviewer
- Aprobacion humana requerida antes de merge en etapas posteriores
