# Failure Simulations

## Failure Simulation 1 &mdash; Invalid Input (schema validation failure)

This simulates a client sending malformed data.

###  Missing required field

```
curl -X POST http://localhost:8000/v1/predict \
  -H "Content-Type: application/json" \
  -d '{}'
```

###  Wrong type

```
curl -X POST http://localhost:8000/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"features": "not-a-list"}'
```

###  Wrong length

```
curl -X POST http://localhost:8000/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1,2]}'
```

### What happens

- FastAPI returns `422 Unprocessable Entity`
- The middleware logs the request
- Prometheus increments:
  - `request_count{endpoint="/v1/predict",method="POST"}`
  - `error_count{...}` **does NOT increment** (because validation errors happen before your handler)

## Failure Simulation 2 &mdash; Force a model failure

This simulates the model itself crashing during prediction.

### Option A &mdash; Send NaNs (scikit-learn will reject them)

```
curl -X POST http://localhost:8000/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [NaN, NaN, NaN, NaN]}'
```

### Option B &mdash; Send extremely large values

```
curl -X POST http://localhost:8000/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1e309, 1e309, 1e309, 1e309]}'
```

### Option C &mdash; Temporarily break the model (for testing)

Add this inside the `predict` function:
```
if payload.features[0] == -999:
    raise RuntimeError("Simulated model failure")
```

Then call:
```
curl -X POST http://localhost:8000/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [-999, 0, 0, 0]}'
```

### What happens

- The middleware catches the exception
- `error_count{endpoint="/v1/predict"}` increments
- `request_latency_seconds` records the latency
- Logs show something like:
```
ERROR | path=/v1/predict | latency_ms=2.14 | error=Simulated model failure
```

## What Prometheus shows

Query these:
- `request_count`
- `error_count`
- `rate(request_count[1m])`
- `rate(error_count[1m])`
- `histogram_quantile(0.95, sum(rate(request_latency_seconds_bucket[5m])) by (le))`

This shows spikes corresponding to the failure tests.

## What Grafana shows

Include panels for:
- **Total Requests** -> `sum(request_count)`
- **Errors per minute** -> `rate(error_count[1m])`
- **P95 Latency** -> `histogram_quantile(0.95, sum(rate(request_latency_seconds_bucket[5m])) by (le))`

The failure simulations will show up immediately.
