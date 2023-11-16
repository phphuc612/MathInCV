from pathlib import Path
from typing import Any, List, Union

from pydantic import BaseModel, validator
from yaml import safe_load

from src.utils.validation_helpers import ALLOWED_NAMES, is_evaluable


class FractalTransformation(BaseModel):
    """
    A class representing a fractal transformation.

    Attributes:
    -----------
    probability : float
        The probability of the transformation being applied.
        Value must be positive but not obliged to be less than 1.
    transformation : str
        The string representation of the transformation.
    """

    probability: float
    transformation: str

    def transform(self, **kwargs) -> Any:
        """
        Applies the fractal transformation to the given input.

        Args:
            **kwargs: Keyword arguments representing the input values.

        Returns:
            The result of applying the fractal transformation to the input.
        """
        ALLOWED_NAMES.update(kwargs)
        return eval(self.transformation, {"__builtins__": {}}, ALLOWED_NAMES)

    @validator("probability", allow_reuse=True)
    def validate_probability(cls, v):
        if v <= 0:
            raise ValueError(f"Probability must be positive. Received {v}")
        return v

    @validator("transformation", allow_reuse=True)
    def validate_transformation(cls, v):
        if v == "":
            raise ValueError("Transformation cannot be empty.")
        if not is_evaluable(v):
            raise ValueError("Transformation is not evaluable.")
        return v

    @classmethod
    def get_sum_raw_prob(cls, transformations: List["FractalTransformation"]) -> float:
        """
        Returns the sum of the RAW probabilities of the given transformations.
        """
        return sum([transformation.probability for transformation in transformations])

    @classmethod
    def get_probs(cls, transformations: List["FractalTransformation"]) -> List[float]:
        """
        Returns list of true probabilities (<= 1) of each transformation.
        """

        sum = cls.get_sum_raw_prob(transformations)
        return [transformation.probability / sum for transformation in transformations]

    @classmethod
    def load_transformations(
        cls, file_path: Union[str, Path]
    ) -> List["FractalTransformation"]:
        """
        Load a list of FractalTransformation objects from a JSON file.
        """
        with open(file_path, "r") as f:
            data = safe_load(f)
        return [FractalTransformation.parse_obj(obj) for obj in data]
