# Test execution

## Run tests with `Makefile`

```bash
# Run formatting, linting, and smoke tests (fast CI / pre-commit)
make smoke_test

# Run formatting, linting, and unit tests
make test_units

# Run formatting, linting, and component tests
make test_components

# Run formatting, linting, and integration tests
make test_integration

# Run formatting, linting, and performance tests
make performance
```

## Run specific tests

| Test decorator | Marker argument | Direct shell call |
| --- | --- | --- |
| `@pytest.mark.unit` | `unit` | `tools/shell_scripts/run_tests.sh unit` |
| `@pytest.mark.component` | `component` | `tools/shell_scripts/run_tests.sh component` |
| `@pytest.mark.integration` | `integration` | `tools/shell_scripts/run_tests.sh integration` |
| `@pytest.mark.smoke` | `smoke` | `tools/shell_scripts/run_tests.sh smoke` |
| `@pytest.mark.performance` | `performance` | `tools/shell_scripts/run_tests.sh performance` |

Several arguments can be called for one test run:

```bash
tools/shell_scripts/run_tests.sh unit component
```
