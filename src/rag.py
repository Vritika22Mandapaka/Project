from dataclasses import dataclass


@dataclass
class RetrievedChunk:
    source: str
    text: str


class SimpleRAGPipeline:
    """A lightweight placeholder RAG pipeline for project scaffolding."""

    def retrieve(self, question: str) -> list[RetrievedChunk]:
        # TODO: replace with vector DB lookup and embeddings.
        return [
            RetrievedChunk(
                source="SOP_Procurement_v1.pdf",
                text="Reorder point should consider lead time and safety stock.",
            )
        ]

    def generate(self, question: str, chunks: list[RetrievedChunk]) -> tuple[str, list[str]]:
        context = " ".join(chunk.text for chunk in chunks)
        answer = (
            f"Based on available SOP context: {context} "
            "Use forecasted demand, supplier lead time, and safety stock to decide order quantity."
        )
        return answer, [chunk.source for chunk in chunks]
