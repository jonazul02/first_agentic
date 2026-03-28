# first_agentic

Sistema agentico evolutivo con 3 roles principales:

- Orchestrator
- Coder
- Reviewer

Este proyecto se construye por etapas, empezando por un esqueleto minimo y robusteciendolo de forma incremental.

## Objetivo

Crear un flujo controlado para evolucionar codigo con:

- Roles bien definidos
- Permisos por alcance
- Estados de tarea claros
- Revision automatizada
- Aprobacion humana obligatoria

## Etapas

1. Protocolo (entradas, salidas, permisos, estados)
2. Tareas falsas para validar flujo
3. Integracion con repo sandbox
4. Revision automatizada
5. Aprobacion humana

## Estructura actual

- `docs/`: decisiones y protocolo
- `src/first_agentic/agents/`: agentes orquestador, coder y reviewer
- `src/first_agentic/core/`: tareas dummy y runner de demostracion
- `src/first_agentic/domain/`: modelos y enums base
- `src/first_agentic/orchestration/`: motor de estados
- `tests/unit/`: pruebas unitarias

## Demo Etapa 2

```bash
PYTHONPATH=src python3 -m first_agentic.core.demo_runner
```

## Tooling base

- `Poetry` como gestor principal de dependencias
- `requirements.txt` y `requirements-dev.txt` para compatibilidad con flujos `pip`

### Instalacion con Poetry

```bash
poetry install
poetry run pytest -q
```

### Instalacion con pip

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m pytest -q
```

## Trabajo por ramas

Todo cambio se hace en ramas `feature/*` antes de integrarse a `main`.
