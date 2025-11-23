from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from config import initialize_gemini_client, logger
from api.planner import router as planner_router
from db.database import connect_to_mongo, close_mongo_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Initializes the Gemini client and MongoDB connection on startup,
    and closes connections on shutdown.
    """
    gemini_client = initialize_gemini_client()
    app.state.aio = gemini_client.aio
    logger.info(
        "Gemini client initialized and async utility client stored in app.state."
    )

    await connect_to_mongo()

    try:

        yield
    finally:

        aio = app.state.aio
        if hasattr(aio, "close"):
            try:
                await aio.close()
                logger.info("Gemini async client closed successfully.")
            except Exception as e:
                logger.exception("Error closing Gemini aio client: %s", e)

        await close_mongo_connection()


app = FastAPI(
    title="Smart Task Planner API",
    description="System for breaking down user goals into actionable tasks using the Gemini LLM.",
    version="1.1.0",
    lifespan=lifespan,
)

origins =[
    "http://localhost:3000",
    "https://smart-task-planner-frontend-iota.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(planner_router, prefix="/api")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
