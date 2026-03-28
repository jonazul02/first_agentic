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
poetry run python -m first_agentic.core.demo_runner
```

## Tooling base

- `Poetry` como gestor principal de dependencias
- `requirements.txt` y `requirements-dev.txt` para compatibilidad con flujos `pip`

### Instalacion con Poetry

```bash
poetry config virtualenvs.in-project true
poetry install
poetry run pytest -q
```

### Instalacion con pip

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m pytest -q
```

## Poetry y entornos virtuales

### Que hace Poetry

Poetry resuelve 3 cosas en una sola herramienta:

- manejo de dependencias
- creacion y uso del entorno virtual
- empaquetado del proyecto Python

En lugar de depender solo de `requirements.txt`, Poetry usa `pyproject.toml` como fuente principal.

### Archivos clave

- `pyproject.toml`: dependencias declaradas y metadatos del proyecto
- `poetry.lock`: versiones exactas resueltas (se genera al instalar/actualizar)
- `.venv/`: entorno virtual local del proyecto (si activas `virtualenvs.in-project`)
- `requirements*.txt`: compatibilidad con flujos tradicionales de `pip`

### Flujo recomendado en este repo

1. Entrar al proyecto

```bash
cd /Users/MI20741/Documents/Cursos/first_agentic
```

2. Forzar venv dentro del repo

```bash
poetry config virtualenvs.in-project true
```

3. Instalar dependencias y crear entorno

```bash
poetry install
```

4. Ejecutar comandos dentro del entorno

```bash
poetry run pytest -q
poetry run python -m first_agentic.core.demo_runner
```

### Diferencia contra tu flujo con conda/pyenv

- Con `conda`: primero creas ambiente y luego `pip install -r requirements.txt`.
- Con `Poetry`: declaras en `pyproject.toml` y `poetry install` crea/usa el ambiente e instala todo.

Poetry ademas fija versiones resueltas en `poetry.lock`, lo que mejora reproducibilidad entre maquinas.

### Por que usar `poetry run` en vez de `python script.py`

`poetry run` garantiza que el comando use el Python y las dependencias del entorno del proyecto.

Puedes seguir usando Python normal, pero entonces debes activar el entorno primero:

```bash
source .venv/bin/activate
python -m first_agentic.core.demo_runner
deactivate
```

### Comandos utiles

```bash
poetry env info --path     # ruta del entorno virtual
poetry env list            # lista de entornos detectados
poetry add <paquete>       # agregar dependencia runtime
poetry add --group dev <paquete>  # agregar dependencia de desarrollo
poetry update              # actualizar lock y dependencias segun reglas
```

## Trabajo por ramas

Todo cambio se hace en ramas `feature/*` antes de integrarse a `main`.
