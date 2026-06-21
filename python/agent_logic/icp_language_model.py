import structlog
from typing import List, Dict, Counter
import re

logger = structlog.get_logger(__name__)

class ICPLanguageModel:
    """
    Layer 9: ICP Language Model.
    Analyzes raw text from market perception to learn 'buyer language'.
    """
    def __init__(self):
        self.pain_phrase_bank: Counter = Counter()
        self.stop_words = {"the", "a", "is", "and", "or", "but", "i", "to", "of", "it"}

    def ingest_market_data(self, raw_texts: List[str]):
        """
        Extracts key phrases from raw forum/review texts.
        Looks for common patterns describing pain points.
        """
        logger.info("ICP_LM: Ingesting market data", count=len(raw_texts))

        for text in raw_texts:
            # Simple extraction of phrases following "problem with", "hate it when", etc.
            patterns = [
                r"problem with ([\w\s]+)",
                r"hate it when ([\w\s]+)",
                r"wish i could ([\w\s]+)",
                r"hard to ([\w\s]+)",
                r"annoying ([\w\s]+)"
            ]

            for pattern in patterns:
                matches = re.findall(pattern, text.lower())
                for match in matches:
                    # Clean up and count
                    phrase = match.strip()
                    if len(phrase.split()) > 1: # Want meaningful phrases
                        self.pain_phrase_bank[phrase] += 1

    def get_conversion_phrases(self, limit: int = 10) -> List[str]:
        """
        Returns the most common buyer phrases for use in content generation.
        """
        return [phrase for phrase, _ in self.pain_phrase_bank.most_common(limit)]

    def score_content_alignment(self, content: str) -> float:
        """
        Scores how well a piece of marketing content aligns with learned buyer language.
        """
        content_lower = content.lower()
        score = 0.0
        total_weight = sum(self.pain_phrase_bank.values())

        if total_weight == 0:
            return 0.0

        for phrase, count in self.pain_phrase_bank.items():
            if phrase in content_lower:
                score += (count / total_weight)

        return min(1.0, score * 10) # Scaling for demo

class ContentPersonalizer:
    """
    Uses ICPLanguageModel to transform generic marketing speak into high-converting buyer language.
    """
    def __init__(self, language_model: ICPLanguageModel):
        self.lm = language_model

    def personalize(self, generic_copy: str) -> str:
        """
        Injects real buyer phrases into the copy.
        In production, this would be an LLM call with the LM phrases as context.
        """
        phrases = self.lm.get_conversion_phrases(3)
        if not phrases:
            return generic_copy

        logger.info("ContentPersonalizer: Injecting buyer language", phrases=phrases)
        # Mocking the injection logic
        return f"{generic_copy}\n\n(Optimized for: {', '.join(phrases)})"
