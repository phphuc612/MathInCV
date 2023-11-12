import pydantic
from typing import Any

from pydantic import BaseModel
from pydantic import *

from src.utils.validation_helpers import is_evaluable


class FractalTransformation(BaseModel):
    """
    A class representing a fractal transformation.

    Attributes:
    -----------
    _probability : float
        The probability of the transformation being applied.
    _str_transformation : str
        The string representation of the transformation.
    """

    _probability: PrivateAttr[float]
    _str_transformation: PrivateAttr[str]

    class FractalTransformation:
        def __init__(self, str_transformation: str):
            self._str_transformation = str_transformation

        def transform(self, **kwargs) -> Any:
            """
            Applies the fractal transformation to the given input.

            Args:
                **kwargs: Keyword arguments representing the input values.

            Returns:
                The result of applying the fractal transformation to the input.
            """
            return eval(self._str_transformation, kwargs)

    @validator('_probability')
    def validate_probability(cls, v):
        if v <= 0:
            raise ValueError(f'Probability must be positive. Received {v}')
        return v
    
    @validator('_str_transformation')
    def validate_str_transformation(cls, v):
        if v == '':
            raise ValueError(f'Transformation cannot be empty.')
        if not is_evaluable(v):
            raise ValueError(f'Transformation is not evaluable.')
        return v