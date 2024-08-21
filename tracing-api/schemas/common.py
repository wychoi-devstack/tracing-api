from pydantic import BaseModel, Field


class Message(BaseModel):
    message: str = Field(..., description="Message")
    code: int = Field(200, description="Code")
    title: str = Field("OK", description="Title")


class ErrorMessageBase(BaseModel):
    detail: str = Field(..., description="Detail message")


class BadRequestMessage(ErrorMessageBase):
    """"""


class UnauthorizedMessage(ErrorMessageBase):
    """"""


class ForbiddenMessage(ErrorMessageBase):
    """"""


class NotFoundMessage(ErrorMessageBase):
    """"""


class InternalServerErrorMessage(ErrorMessageBase):
    """"""
