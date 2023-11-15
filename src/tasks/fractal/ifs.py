#! /usr/bin/env python
# coding: utf-8

from __future__ import division

from typing import List, Tuple

from numpy import random
from PIL import Image, ImageDraw

from src.schemas.fractal_transformation import FractalTransformation


def generate_points(
    transformations: List[FractalTransformation], initial_point: Tuple[float] = (0, 0), n_points=100000
) -> List[Tuple]:
    n_transformation = len(transformations)
    probs = FractalTransformation.get_probs(transformations)
    choices = random.choice(n_transformation, n_points, replace=True, p=probs)

    point = initial_point
    points: List[Tuple] = [point]

    for choice in choices:
        point = transformations[choice].transform(x = point[0], y = point[1])
        points.append(point)

    return points


def generate_fractal(transformations: List[FractalTransformation], width: int, height: int, outputfile: str):
    points = generate_points(transformations)

    # find out image limits determine scaling and translating
    min_x = min(points, key=lambda p: p[0])[0]
    max_x = max(points, key=lambda p: p[0])[0]
    min_y = min(points, key=lambda p: p[1])[1]
    max_y = max(points, key=lambda p: p[1])[1]
    p_width = max_x - min_x
    p_height = max_y - min_y

    width_scale = width / p_width
    height_scale = height / p_height
    scale = min(width_scale, height_scale)

    # create new image
    image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(image)

    # plot points
    for point in points:
        x = (point[0] - min_x) * scale
        y = height - (point[1] - min_y) * scale
        draw.point((x, y))

    # save image file
    image.save(outputfile, "PNG")