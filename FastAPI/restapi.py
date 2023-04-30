#pip install pydantic
from fastapi import FastAPI
#wsgi server =  Unicorn
#uvicorn restapi:app --reload
#curl http://127.0.0.1:8000
#curl http://127.0.0.1:8000 -X POST


app = FastAPI()

@app.get('/')
def hello():
    return {"Hello": "World"}

@app.post('/')
def hello_post():
    return {"sucesso":"deu tudo certo"}

@app.get('/something')
def something():
    return {"Alguma coisa": "something"}

# @app.get('/')
# def hello():
#     return {"Hello": "World"}
#
# @app.get('/')
# def hello():
#     return {"Hello": "World"}