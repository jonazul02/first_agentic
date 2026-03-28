# Etapa 3 - Integracion con Repo Sandbox

Esta etapa conecta el flujo agentico con un repositorio real de pruebas bajo controles estrictos.

## Capacidades implementadas

- Lectura y escritura de archivos solo en rutas permitidas (`allowed_paths`).
- Creacion de branch temporal por tarea (`sandbox/<task>-<timestamp>`).
- Ejecucion de comandos solo si estan en `allowed_commands`.
- Limite maximo de archivos modificados por tarea.
- Generacion de diff real con `git diff`.

## Componentes

- `RepoAdapter`: capa de acceso al repo y enforcement de permisos.
- `SandboxOrchestratorAgent`: coordina estados y ejecucion sobre repo real.
- `SandboxCoderAgent`: aplica cambios controlados.
- `SandboxReviewerAgent`: valida pruebas en sandbox.

## Ejecutar demo sandbox

```bash
poetry run python -m first_agentic.core.sandbox_runner
```

## Guardrails activos

- Sin permisos de ruta no hay escritura.
- Sin permisos de comando no hay ejecucion.
- Si supera limite de archivos cambiados, la tarea se rechaza.
