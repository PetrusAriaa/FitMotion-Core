# FitMotion-Core
Built with [FastAPI](https://fastapi.tiangolo.com/). FitMotion-Core is main Backend of FitMotion App.
<hr />

## Initial Configuration
1. Create an environment. It is recommended using pipenv or virtualenv
```bash
# using virtualenv
vitualenv .venv

# For Linux
source .venv/bin/activate
# For Windows
.venv\Scripts\activate

# using  pipenv
pipenv shell
```
3. Install the dependencies
```bash
# using pipenv
pipenv install

# using pip
pip install -r requirements.txt
```
5. Create new `.env.development` file and add following variables: `PG_URL`, `SECRET`, `ALGORITHM`, `GOOGLE_APPLICATION_CREDENTIALS`, `CLOUD_BUCKET`. Your `.env.development` file should look like this.
```
# .env.development
PG_URL= <database connection string>
SECRET= <secret hex>
ALGORITHM=HS256
GOOGLE_APPLICATION_CREDENTIALS= <location of google cloud storage service account json key>
CLOUD_BUCKET= <bucket name>
```
6. Run the server. You can run the server using the pre-configured `Makefile` with command `make dev`. You can also start the server with uvicorn command.
```
# hot reload for development
uvicorn src.main:app --reload

# exposed to public for production
uvicorn src.main:app --host 0.0.0.0 --port 0.0.0.0
```
