"""Pydantic schemas for Project object"""

from csv import QUOTE_ALL, Dialect

from pydantic import BaseModel, Field


class ProjectReturnSchema(BaseModel):
    project_id: str = Field(..., alias="project_id")
    project_name: str = Field(..., alias="project_name")
    project_return: float = Field(..., alias="project_return")


class ProjectHourSchema(BaseModel):
    project_id: str = Field(..., alias="project_id")
    worker_id: str = Field(..., alias="worker_id")
    worker_division: str = Field(..., alias="worker_division")
    number_hours: int = Field(..., alias="number_hours")


class ProjectReturnDialect(Dialect):
    """
    Dialect for importing the file with counterparty record
    """

    delimiter = ","
    quotechar = '"'
    lineterminator = "\n"
    doublequote = True
    quoting = QUOTE_ALL
