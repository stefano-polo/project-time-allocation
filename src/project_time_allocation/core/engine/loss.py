import numpy as np

from project_time_allocation.core.engine.simplex_builder import (
    InequalityMatrixConstraint,
    InequalityVectorConstraint,
    LinearCoefficients,
)


class NegLossFunction:
    def __init__(self, lin_coeff: LinearCoefficients) -> None:
        self._lin_coeff = lin_coeff

    def value(self, strategy: np.ndarray) -> float:
        return -self._lin_coeff.value @ strategy


class ConstraintValues:
    def __init__(self, constr_matrix: InequalityMatrixConstraint) -> None:
        self._constr_matrix = constr_matrix

    def value(self, strategy: np.ndarray) -> np.ndarray:
        return self._constr_matrix.value @ strategy


class ConstraintChecker:
    def __init__(
        self, constr_value: ConstraintValues, constr_target: InequalityVectorConstraint
    ) -> None:
        self._contr_value = constr_value
        self._constr_target = constr_target

    def value(self, strategy: np.ndarray) -> bool:
        return (
            np.sum(self._contr_value.value(strategy) > self._constr_target.value)
        ) == 0
