import structlog
from typing import List, Dict, Any
from pydantic import BaseModel

logger = structlog.get_logger(__name__)

class CategoryDefinition(BaseModel):
    category_name: str
    narrative: str
    vocabulary: List[str]
    competitor_framing: str

class CategoryCreationSystem:
    """
    Module 2: Category Creation System.
    Generates names, narratives, and unique vocabulary to define new markets.
    """
    def __init__(self, llm_engine: Any = None):
        self.llm = llm_engine

    def generate_category_name(self, idea_title: str) -> str:
        """
        Names the SPACE, not the product.
        """
        logger.info("CategoryCreation: Naming the new category", base_idea=idea_title)
        return f"Autonomous {idea_title.split()[0]} Orchestration"

    def write_narrative(self, category_name: str) -> str:
        """
        Writes the founding story: Why the old way is broken, why now is the moment.
        """
        return f"The era of manual {category_name} has ended. Static tools are the bottleneck..."

    def generate_vocabulary(self, category_name: str) -> List[str]:
        """
        Generates unique terms to own the mental real estate.
        """
        return ["Cognitive Sync", "Morphic Scaling", "Direct Revenue Path"]

    def define_new_category(self, idea_title: str) -> CategoryDefinition:
        """
        Full category definition cycle.
        """
        name = self.generate_category_name(idea_title)
        narrative = self.write_narrative(name)
        vocab = self.generate_vocabulary(name)

        framing = f"Competitors focus on features; {name} focuses on outcomes through {vocab[0]}."

        logger.info("CategoryCreation: New category DEFINED", name=name)

        return CategoryDefinition(
            category_name=name,
            narrative=narrative,
            vocabulary=vocab,
            competitor_framing=framing
        )
