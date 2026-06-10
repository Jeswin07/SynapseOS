from fastapi import FastAPI

from src.modules.auth.admin_routes import (
    router as admin_router,
)
from src.modules.auth.router import router as auth_router
from src.modules.tenants.router import (
    router as tenant_router,
)
from src.modules.users.router import (
    router as users_router,
)

app = FastAPI(title="SynapseOS API", version="1.0.0")


@app.get("/")
def root():
    return {"message": "SynapseOS API Running"}


app.include_router(auth_router)
app.include_router(tenant_router)
app.include_router(users_router)

app.include_router(admin_router)
