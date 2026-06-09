from fastapi import FastAPI

app = FastAPI(
    title="SynapseOS API",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "SynapseOS API Running"
    }