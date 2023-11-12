import pydantic

from pydantic import BaseModel
from pydantic import *


class FractalTransformation(BaseModel):
    _probability: PrivateAttr[float]
    _str_transformation: PrivateAttr[str]


    @validator('_probability')
    def validate_probability(cls, v):
        if v <= 0:
            raise ValueError(f'Probability must be positive. Received {v}')
        return v
    
    @validator('_str_transformation')
    def validate_str_transformation(cls, v):
        if v == '':
            raise ValueError(f'Transformation cannot be empty.')
        return v