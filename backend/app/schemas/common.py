from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Base schema for all API request and response models."""

    model_config = ConfigDict(
        from_attributes=True,
    )