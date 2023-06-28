import numpy as np
from scipy.optimize import linprog

from project_time_allocation.core.engine.simplex_builder import (
    InequalityMatrixConstraint,
    InequalityVectorConstraint,
    LinearCoefficients,
)


class Optimizer:
    def __init__(
        self,
        linear_coefficients: LinearCoefficients,
        inequality_matrix_constraint: InequalityMatrixConstraint,
        inequality_vector_constraint: InequalityVectorConstraint,
    ) -> None:
        self._linear_coefficients = linear_coefficients
        self._ineq_matrix_constr = inequality_matrix_constraint
        self._ineq_vec_constr = inequality_vector_constraint
        bounds = []
        for i in range(len(self._linear_coefficients.value)):
            bounds.append((0, None))
        self._bounds = tuple(bounds)

    def run(self) -> np.ndarray:
        res = linprog(
            self._linear_coefficients.value,
            A_ub=self._ineq_matrix_constr.value,
            b_ub=self._ineq_vec_constr.value,
            bounds=self._bounds,
            method="highs",
            options=None,
            integrality=np.ones(len(self._linear_coefficients.value)),
        )
        if not res.success:
            print("The provided solution is not optimal")
        return res.x
