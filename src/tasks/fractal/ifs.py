#! /usr/bin/env python
# coding: utf-8

from __future__ import division

from typing import Generator, List, Tuple

from numpy import random
from PIL import Image, ImageDraw
from pydantic import TupleError

from src.schemas import FractalTransformation


def _scale_points(points: List[Tuple], lim_x: int, lim_y: int) -> List[Tuple]:
    # find out image limits determine scaling and translating
    min_x = min(points, key=lambda p: p[0])[0]
    max_x = max(points, key=lambda p: p[0])[0]
    min_y = min(points, key=lambda p: p[1])[1]
    max_y = max(points, key=lambda p: p[1])[1]
    p_width = max_x - min_x
    p_height = max_y - min_y

    width_scale = lim_x / p_width
    height_scale = lim_y / p_height
    scale = min(width_scale, height_scale)

    new_points: List[Tuple] = []
    for point in points:
        x = (point[0] - min_x) * scale
        y = (point[1] - min_y) * scale
        new_points.append((x, y))
    return new_points


def generate_points(
    transformations: List[FractalTransformation],
    lim_x: int,
    lim_y: int,
    initial_point: Tuple[float] = (0, 0),
    n_points=100000,
) -> List[Tuple]:
    n_transformation = len(transformations)
    probs = FractalTransformation.get_probs(transformations)
    choices = random.choice(n_transformation, n_points, replace=True, p=probs)

    point = initial_point
    points: List[Tuple] = [point]

    for choice in choices:
        point = transformations[choice].transform(x=point[0], y=point[1])
        points.append(point)

    points = _scale_points(points, lim_x, lim_y)

    return points


def generate_fractal(
    transformations: List[FractalTransformation],
    width: int,
    height: int,
    outputfile: str,
    return_freq: int = 1
) -> Generator:
    points = generate_points(transformations, width - 1, height - 1)


    # create new image
    image = Image.new("RGB", (width, height))

    return_time = len(points) // return_freq

    # plot points
    for i, point in enumerate(points):
        image.putpixel((int(point[0]), int(point[1])), (255, 255, 255))   
        if i % return_time == 0 or i == len(points) - 1:
            yield image
