from pydantic import BaseModel, Field


class ForecastRequest(BaseModel):
    sku_id: str
    region: str
    history_window_days: int = Field(default=180, ge=30, le=730)


class ForecastResponse(BaseModel):
    sku_id: str
    region: str
    weekly_demand_prediction: float
    confidence: float


class OpsQuestionRequest(BaseModel):
    question: str


class OpsQuestionResponse(BaseModel):
    answer: str
    citations: list[str]
