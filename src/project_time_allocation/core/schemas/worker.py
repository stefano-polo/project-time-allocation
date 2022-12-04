from pydantic import BaseModel, Field


class WorkerSchema(BaseModel):
    worker_id: str = Field(..., alias="worker_id")
    worker_division: str = Field(..., alias="worker_division")
    worker_numbers: int = Field(..., alias="worker_numbers")
    number_hour_per_workers_per_year: int = Field(
        ..., alias="number_hour_per_workers_per_year"
    )
    costs_per_worker_per_hour: float = Field(..., alias="costs_per_worker_per_hour")
