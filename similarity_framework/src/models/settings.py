from pydantic import Field, BaseModel, AliasChoices
from pydantic_settings import BaseSettings, SettingsConfigDict


class WeightSettings(BaseModel):
    column_embeddings: int = Field(1, description="Weight for column embeddings")
    column_name_embeddings: int = Field(1, description="Weight for column name embeddings")
    kinds: int = Field(1, description="Weight for kinds")
    size: int = Field(1, description="Weight for size")
    incomplete_columns: int = Field(1, description="Weight for incomplete columns")
    exact_names: int = Field(1, description="Weight for exact names")
    type: int = Field(1, description="Weight for types")


class AnalysisSettings(BaseSettings):
    weights: WeightSettings = Field(default_factory=WeightSettings)

    column_embeddings: bool = Field(default=False, description="Use column embeddings for comparison")
    column_name_embeddings: bool = Field(default=False, description="Use column name embeddings for comparison")
    correlation: bool = Field(default=False, description="Use correlation for comparison")
    type_advanced: bool = Field(default=False, description="Use advanced type comparison")
    type_structural: bool = Field(default=False, description="Use structural type comparison")
    type_basic: bool = Field(default=False, description="Use basic type comparison")
    kinds: bool = Field(default=False, description="Use kinds for comparison")

    ## only for comparator
    size: bool = Field(default=False, description="Use size for comparison")
    incomplete_columns: bool = Field(default=False, description="Use incomplete columns for comparison")
    exact_names: bool = Field(default=False, description="Use exact names for comparison")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    analysis_settings: AnalysisSettings = Field(default_factory=AnalysisSettings)
    comparator: str = Field(default="by_type")
    metadata_creator: str = Field(validation_alias=AliasChoices("type"), default="type")

    @staticmethod
    def load(filepath: str):
        return Settings(_env_file=filepath)
