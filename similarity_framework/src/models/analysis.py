from dataclasses import dataclass

@dataclass
class WeightSettings:
    column_embeddings: int = 1
    column_name_embeddings: int = 1
    kinds: int = 1
    size: int = 1
    incomplete_columns: int = 1
    exact_names: int = 1

@dataclass
class AnalysisSettings:
    column_embeddings: bool = False,
    column_name_embeddings: bool = False,
    correlation: bool = False,
    type_advanced: bool = False,
    type_structural: bool = False,
    type_basic: bool = False,
    kinds: bool = False,

    ## only for comparator
    size: bool = False,
    incomplete_columns: bool = False,
    exact_names: bool = False

    weights: WeightSettings = WeightSettings()
