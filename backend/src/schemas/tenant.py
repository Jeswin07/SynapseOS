from pydantic import BaseModel


class TenantCreate(BaseModel):
    company_name: str
    industry: str


class TenantResponse(BaseModel):
    id: str
    company_name: str
    industry: str