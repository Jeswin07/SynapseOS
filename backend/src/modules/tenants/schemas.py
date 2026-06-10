from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TenantCreate(BaseModel):
    company_name: str
    industry: str


class TenantResponse(BaseModel):
    id: UUID
    company_name: str
    industry: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
