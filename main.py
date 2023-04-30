from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from routes.user_routes import user_router

app = FastAPI()
app.add_middleware(CORSMiddleware)

app.include_router(user_router, tags=["UserRoutes"], prefix="/api/v1")