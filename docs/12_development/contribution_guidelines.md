# Contribution guidelines

## Summary

* Do not ignore [./docs/12_development/documentation_guidelines.md]
* Apply SOLID principles
* Always use logging instead of print()
* Always use try / except / raise blocks even if the code is draft to reduce effort on debugging

## SOLID Principles — Short Summary

### S — Single Responsibility

* A module/class/function must have exactly one reason to use.
* Do one thing. Do it well.

### O — Open/Closed

* Code should be open for extension but closed for modification.
* Extend behavior without rewriting existing code.

### L — Liskov Substitution

* Subclasses/implementations must be replaceable without breaking correctness.
* If a class promises an interface, derived classes must honor it.

### I — Interface Segregation

* Prefer many small, focused interfaces over one large “fat” interface.
* Clients should not depend on methods they don't use.

### D — Dependency Inversion

* High-level modules should depend on abstractions, not concrete implementations.
* Use clear ports/interfaces; inject dependencies rather than constructing them internally.

## Lint tests

### Auto-fix

```python
ruff check src/damn_ape/config/llm_settings.py --fix
```

## Logging

### log message templates

```python
# INFO – normal operations, milestones
logger.info("Successfully %s", action)
logger.info("Starting %s", process_name)
logger.info("Completed %s in %.2f seconds", task_name, duration)

# DEBUG – internal state, config, progress
logger.debug("Entering %s with args=%s kwargs=%s", function_name, args, kwargs)
logger.debug("Loaded configuration: %s", config_dict)
logger.debug("Using model=%s device=%s dtype=%s", model_id, device, dtype)
logger.debug("[%d/%d] Processing %s", index, total, item_name)

# WARNING – degraded mode, unexpected but non-fatal
logger.warning("Missing optional field '%s', using default", field_name)
logger.warning("Retrying operation '%s' (attempt %d)", operation, attempt)

# ERROR – failures that trigger raise
logger.error("Failed to %s: %s", action, exc)
logger.error("Could not load resource '%s': %s", resource_name, exc)
logger.error("Invalid configuration in '%s': %s", config_path, exc)

# CRITICAL – unrecoverable failures
logger.critical("Fatal error in %s: %s", subsystem, exc)
logger.critical("Unrecoverable failure, shutting down")
```

### In Jupyter notebook reduce output when building plots

```python
# downgrade logging level
logging.getLogger().setLevel(logging.ERROR)

# code that builds plots is here

# reset logging level
logging.getLogger().setLevel(logging.DEBUG)
```

### to run apps in debug mode

[macOS, linux]

```bash
export PYTHONPATH=src; \
export LOG_LEVEL=DEBUG; \
export TRANSFORMERS_VERBOSITY=info; \
python -m damn_ape.app.sandbox.demo_cli
```

### Namespace control

```python
import logging
logger = logging.getLogger("project_src_dir.subdir.subdir")
```

## Error Handling Pattern

All code must follow a strict **try / except / raise** structure to guarantee:

* Early termination on failure  
* Clear diagnostics in logs  
* Predictable behavior in all layers (nexus, app, infra)

### General Pattern

```python
try:
    result = dangerous_operation()
    return result
except SpecificError as exc:
    logger.error("Failed to %s: %s", "dangerous_operation", exc)
    raise
except Exception as exc:
    logger.critical("Unexpected failure in %s: %s", function_name, exc)
    raise
```

### Rules

#### Never swallow exceptions

##### Bad

```python
try:
    do_something()
except Exception:
    pass   # hides the problem
```

##### Correct

```python
try:
    do_something()
except Exception as exc:
    logger.error("Failed to %s: %s", "do_something", exc)
    raise
```

#### Validate inputs early

```python
if config is None:
    logger.error("Configuration object is missing.")
    raise ValueError("Missing configuration")
```

#### Always include context in log messages

```python
logger.error("Failed to load model '%s': %s", model_id, exc)
```

#### Never reformat exceptions—re-raise them

```python
except Exception as exc:
    logger.error("Fatal error in %s: %s", step_name, exc)
    raise
```

#### Infra layer must NEVER crash silently

Because infra problems are the most difficult to debug.

#### Nexus layer may catch and re-raise with semantic meaning

```python
try:
    vector = embedder.encode(text)
except Exception as exc:
    logger.error("Embedding failed for text length=%d: %s", len(text), exc)
    raise RuntimeError("Embedding failed") from exc
```

#### Application layer is where errors become user-facing

But still never hide stack traces during development.

## Lorem ipsum

```python

```

```bash

```
