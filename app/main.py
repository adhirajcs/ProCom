from fastapi import FastAPI

app = FastAPI(
    title="ProCom API",
    description="Product Commerce platform API",
    version="0.1.0",
)


@app.get("/health/live", tags=["Health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok", "application": "ProCom"}
