from fastapi import FastAPI

app = FastAPI(title="urob.to")

@app.get("/health")
def health_check():
    return {"status": "ok"}