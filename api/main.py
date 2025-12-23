from source.game_search_system_final.game_search import GameSearchSystem
from data_models.SearchRequest import SearchRequest
from data_models.SearchResponse import SearchResponse
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AIGameSearch",
    description="API для поиска игр с помощью ИИ"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

game_search_system = GameSearchSystem()


@app.post("/search", response_model=SearchResponse)
async def search_games(request: SearchRequest):
    try:
        results = game_search_system.search(request.query, top_k=request.top_k)

        return SearchResponse(
            query=request.query,
            results=results,
            total=len(results)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка поиска: {str(e)}")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": "loaded"}


@app.get("/")
async def root():
    return {"message": "Game Search API"}
