# Week 22

## Configure

1. Install [Python](https://www.python.org/downloads/).
1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Run venv\Scripts\activate on Windows.
   ```
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Run

1. Run `uvicorn main:app --host 0.0.0.0 --port 8000 --reload` in a terminal window.
1. Run `curl -X POST http://localhost:8000/v1/predict -H "Content-Type: application/json" --data @payload.json` in another terminal window.
1. Make changes to the app and `uvicorn` will auto-reload.

Here is an example `payload.json` file.
```
{
  "features": [5.1, 3.5, 1.4, 0.2]
}
```

## Docker

1. Run `docker build -t iris-api .` to build the Docker image.
1. Run `docker run -p 8000:8000 iris-api` to run it.
1. Test it by running step 2 above.
