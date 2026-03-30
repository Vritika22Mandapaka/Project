from dataclasses import dataclass


@dataclass
class AgentDecision:
    agent_name: str
    recommendation: str
    risk_level: str


class SalesForecastAgent:
    def run(self, sku_id: str, region: str) -> AgentDecision:
        return AgentDecision(
            agent_name="SalesForecastAgent",
            recommendation=f"Forecast next-week demand for {sku_id} in {region}: 120 units",
            risk_level="low",
        )


class ProcurementAgent:
    def run(self, sku_id: str) -> AgentDecision:
        return AgentDecision(
            agent_name="ProcurementAgent",
            recommendation=f"Create PO for {sku_id}: 300 units from Supplier-A",
            risk_level="medium",
        )


class ManufacturingAgent:
    def run(self, sku_id: str) -> AgentDecision:
        return AgentDecision(
            agent_name="ManufacturingAgent",
            recommendation=f"Allocate Line-2 for {sku_id} on next available shift",
            risk_level="medium",
        )


class SupervisorAgent:
    def evaluate(self, decisions: list[AgentDecision]) -> dict:
        requires_human_approval = any(d.risk_level in {"high", "medium"} for d in decisions)
        return {
            "requires_human_approval": requires_human_approval,
            "decisions": decisions,
        }
