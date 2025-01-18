from app.model.survivor import Chat, Survivor
from fastapi import FastAPI, Body, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.templating import Jinja2Templates
from app.core import predict as cp
from app.core import chat as cc

app = FastAPI(
    title="Titanic Survive Predictor",
    description="App para determinar si una persona sobrevive o no al naufragio del titacnic.",
    version="0.1.0",
    license_info={
        "name": "MIT",
        "url": "https://github.com/krisskira/ml-handwritten-number-recognizar/blob/main/LICENCE",
        "file": "LICENSE",
        "type": "MIT"
    },
    contact={
        "name": "Crhistian David Vergara Goméz",
        "url": "https://www.linkedin.com/in/cristian-david-vergara-gomez/",
        "email": "krisskira@gmail.com"
    }
)

app.mount("/public", StaticFiles(directory="public"), name="public")
templates = Jinja2Templates(directory="templates", auto_reload=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={}
    )


@app.post("/api/v1/predict", response_class=JSONResponse)
async def predict(payload: Survivor = Body(None)):
    print(">>> Payload", payload)
    result = await cp.predict(payload)
    return {"result": result}


@app.post("/api/v1/chat", response_class=JSONResponse)
async def chat(payload: Chat = Body(None)):
    message = payload.message
    response = await cc.chatting(message)
    return {"message": response}
