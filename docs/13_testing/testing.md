# Test execution

## Run tests with `Makefile`

```bash
# Run formatting, linting, and smoke tests (fast CI / pre-commit)
make test

# Run formatting, linting, smoke + performance tests
make performance
```

## Run specific tests

test decorator | argument | call
--- | --- | ---
`@pytest.mark.smoke` | smoke | ./tools/run_tests smoke
`@pytest.mark.performance` | performance | ./tools/run_tests performance

Several arguments can be called for one test run:

```bash
./tools/run_tests smoke performance
```
