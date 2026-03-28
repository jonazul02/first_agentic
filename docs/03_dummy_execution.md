# Etapa 2 - Ejecucion con tareas falsas

Esta etapa valida el flujo de 3 agentes con tareas simuladas antes de conectar un repo real.

## Casos incluidos

- `agrega funcion suma`
- `corrige bug de login`
- `anade test`

## Objetivo

Validar que:

- el orquestador mueve estados correctamente
- coder y reviewer colaboran con rondas controladas
- el sistema produce una salida estructurada confiable

## Ejecutar demo

```bash
python3 -m first_agentic.core.demo_runner
```

## Resultado esperado

- Cada tarea termina en `awaiting_user` tras pasar por plan, coding y review.
- Hallazgos iniciales generan `needs_changes` y vuelta a `coding` cuando aplica.
- Se respeta el limite maximo de rondas de revision.

## Evolucion posterior (casos reales)

Este runner se mantendra y se alimentara luego con tareas reales desde archivos de configuracion por repo para poder medir `pass/fail` real sobre proyectos concretos.
