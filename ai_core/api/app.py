from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter
from api.routers.ai_scenario import router as ai_scenario_router
from api.routers.chatting import router as chatting_router
from api.routers.rag import router as rag_router

load_dotenv()


# app = FastAPI()
app = APIRouter() # APIRouter для выноса наружу через .include_router(), так как mount для объекта FastAPI() усложнит структуру docs
app.include_router(ai_scenario_router)
app.include_router(chatting_router)
app.include_router(rag_router)
