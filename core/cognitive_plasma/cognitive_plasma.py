import numpy as np
from typing import Dict, List, Optional, Tuple, Any
import structlog
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import torch

logger = structlog.get_logger(__name__)

class CognitivePlasma:
    """
    The shared embedding space that merged agents think in.
    Implements state fusion via random projections into high-dimensional latent space.
    """
    def __init__(
        self,
        base_dim: int = 1536,
        plasma_dim: int = 4096,
        device: str = "cpu"
    ):
        self.base_dim = base_dim
        self.plasma_dim = plasma_dim
        self.device = device

        # Consistent random projection matrix for stable latent space
        rng = np.random.default_rng(42)
        proj = rng.standard_normal((base_dim, plasma_dim)) / np.sqrt(plasma_dim)
        self.projection_matrix = torch.from_numpy(proj).to(dtype=torch.float32, device=device)

        # Load local encoder
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2", device=device)
        logger.info("CognitivePlasma: Latent Space Initialized", base_dim=base_dim, plasma_dim=plasma_dim)

    def project(self, embedding: np.ndarray) -> torch.Tensor:
        """Move embedding from base space to high-dimensional plasma."""
        with torch.no_grad():
            t_emb = torch.from_numpy(embedding).to(dtype=torch.float32, device=self.device)
            return torch.matmul(t_emb, self.projection_matrix)

    def deproject(self, plasma_tensor: torch.Tensor) -> np.ndarray:
        """Approximate recovery of base embedding using pseudoinverse."""
        pinv = torch.linalg.pinv(self.projection_matrix)
        with torch.no_grad():
            return torch.matmul(plasma_tensor, pinv).cpu().numpy()

    async def merge(
        self,
        state_a: np.ndarray,
        state_b: np.ndarray,
        context_task: str
    ) -> torch.Tensor:
        """
        Fused merger of two agent cognitive states.
        Uses attention weights derived from the task context.
        """
        # Encode task context
        task_emb = self.encoder.encode(context_task)
        t_plasma = self.project(task_emb)

        # Project parent states
        a_plasma = self.project(state_a)
        b_plasma = self.project(state_b)

        # Compute cosine similarity for attention
        sim_a = torch.nn.functional.cosine_similarity(a_plasma.unsqueeze(0), t_plasma.unsqueeze(0))
        sim_b = torch.nn.functional.cosine_similarity(b_plasma.unsqueeze(0), t_plasma.unsqueeze(0))

        # Softmax weights
        weights = torch.softmax(torch.stack([sim_a, sim_b]), dim=0)

        # Fused state (weighted average in plasma space)
        merged = weights[0] * a_plasma + weights[1] * b_plasma

        logger.debug("CognitivePlasma: State Merger",
                     weight_a=float(weights[0]), weight_b=float(weights[1]))

        return merged

    def compute_gradient(self, plasma_state: torch.Tensor, target_goal: str) -> np.ndarray:
        """Directional vector in plasma space toward a strategic goal."""
        goal_emb = self.encoder.encode(target_goal)
        goal_plasma = self.project(goal_emb)

        gradient = goal_plasma - plasma_state
        return gradient.cpu().numpy()
