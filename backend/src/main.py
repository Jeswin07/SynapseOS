from fastapi import FastAPI

from src.core.storage.storage_service import StorageService
from src.modules.auth.admin_routes import (
    router as admin_router,
)
from src.modules.auth.router import router as auth_router
from src.modules.data.router import (
    router as data_router,
)
from src.modules.forecast.router import (
    router as forecast_router,
)
from src.modules.ml.router import (
    router as ml_router,
)
from src.modules.risk.router import (
    router as risk_router,
)
from src.modules.tenants.router import (
    router as tenant_router,
)
from src.modules.users.router import (
    router as users_router,
)
from src.modules.knowledge.router import (
    router as knowledge_router,
)


app = FastAPI(title="SynapseOS API", version="1.0.0")


@app.get("/")
def root():
    return {"message": "SynapseOS API Running"}

storage = StorageService()
storage.ensure_bucket_exists()

app.include_router(auth_router)
app.include_router(tenant_router)
app.include_router(users_router)
app.include_router(data_router)
app.include_router(ml_router)
app.include_router(admin_router)
app.include_router(forecast_router)
app.include_router(risk_router)
app.include_router(knowledge_router)
