from fastapi import FastAPI

from .agents import ManufacturingAgent, ProcurementAgent, SalesForecastAgent, SupervisorAgent
from .rag import SimpleRAGPipeline
from .schemas import (
    ForecastRequest,
    ForecastResponse,
    OpsQuestionRequest,
    OpsQuestionResponse,
)

app = FastAPI(title="SmartSupply AI Platform", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/forecast", response_model=ForecastResponse)
def forecast(req: ForecastRequest) -> ForecastResponse:
    # TODO: connect to trained forecasting model.
    return ForecastResponse(
        sku_id=req.sku_id,
        region=req.region,
        weekly_demand_prediction=120.0,
        confidence=0.82,
    )


@app.post("/ops/question", response_model=OpsQuestionResponse)
def ops_question(req: OpsQuestionRequest) -> OpsQuestionResponse:
    rag = SimpleRAGPipeline()
    chunks = rag.retrieve(req.question)
    answer, citations = rag.generate(req.question, chunks)
    return OpsQuestionResponse(answer=answer, citations=citations)


@app.post("/plan/{sku_id}/{region}")
def full_plan(sku_id: str, region: str) -> dict:
    sales = SalesForecastAgent().run(sku_id=sku_id, region=region)
    procurement = ProcurementAgent().run(sku_id=sku_id)
    manufacturing = ManufacturingAgent().run(sku_id=sku_id)

    supervisor_output = SupervisorAgent().evaluate([sales, procurement, manufacturing])
    return {
        "workflow": "sales -> procurement -> manufacturing",
        "supervisor": {
            "requires_human_approval": supervisor_output["requires_human_approval"],
        },
        "decisions": [d.__dict__ for d in supervisor_output["decisions"]],
    }
