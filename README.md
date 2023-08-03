# Run the File:
### locally:
uvicorn main:app --reload

### on railway:
uvicorn main:app --host 0.0.0.0 --port $PORT

# install requirements:
pip install -r requirements.txt -U

Use pip3 if your environment is setup that way.

The API is available on [railway](https://tfdb-production.up.railway.app/).

The temporariry front-end is available at [402](https://www.402.app/tf).
