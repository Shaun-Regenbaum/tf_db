# Run the File:
### locally:
uvicorn main:app --reload

### on railway:
uvicorn main:app --host 0.0.0.0 --port $PORT

# install requirements:
pip install -r requirements.txt -U

Use pip3 if your environment is setup that way.

The API is available at:
[tfdb-production.up.railway.app](tfdb-production.up.railway.app)

The temporariry front-end is available at [402](402.app/tf)
