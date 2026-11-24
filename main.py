from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    try:
        return {"Hello": "World"}
    except Exception as e:
        return {"error": str(e)}
    

@app.get("/health")
async def health_check():
    try:
        # Perform health check logic here (e.g., database connection, external service check)
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}