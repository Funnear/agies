# Test execution

## Run tests with `Makefile`

```bash
# Run formatting, linting, and smoke tests (fast CI / pre-commit)
make smoke_test

# Run formatting, linting, smoke + performance tests
make performance
```

## Run specific tests

test decorator | argument | call
--- | --- | ---
`@pytest.mark.smoke` | smoke | tools/shell_scripts/run_tests.sh smoke
`@pytest.mark.performance` | performance | tools/shell_scripts/run_tests.sh performance

Several arguments can be called for one test run:

```bash
tools/shell_scripts/run_tests.sh smoke performance
```
