from uuid import UUID

from pydantic import BaseModel


class RiskRequest(BaseModel):

    dataset_id: UUID


class RiskResponse(BaseModel):

    analysis_id: UUID

    risk_score: float

    risk_level: str

    anomalies: int

    rows: int

    message: str

    summary: str