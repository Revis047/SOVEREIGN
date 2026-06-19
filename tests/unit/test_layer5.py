import pytest
import numpy as np
from layers.l05_quantum_optimizer.qubo_decision import QUBODecisionEngine, DecisionSpace, Objective, Constraint

def test_qubo_sbm_decision():
    engine = QUBODecisionEngine(max_steps=500)
    space = DecisionSpace(
        variables=["marketing"],
        binary_variables=["twitter", "linkedin", "tiktok", "email"]
    )
    objectives = [Objective(name="reach", weight=1.0, target="max")]
    constraints = [Constraint(name="budget", penalty=5.0)]

    result = engine.make_decision(space, objectives, constraints)

    assert result.action in space.binary_variables
    assert len(result.solution_vector) == 4
    assert result.confidence > 0
