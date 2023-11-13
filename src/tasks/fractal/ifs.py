#! /usr/bin/env python
# coding: utf-8

from __future__ import division

from typing import List, Tuple

from numpy import random

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


# def process_file(transformations, width, height, iterations=1, outputfile="out.png"):

#     probability_join = sum(t[0] for t in transformations)

#     points = set([(0, 0)])

#     # for each iteration
#     for i in range(iterations):
#         new_points = set()

#         # for each point
#         for point in points:

#             # decide on which transformation to apply
#             rnd = uniform(0, probability_join)
#             p_sum = 0
#             for probability, function in transformations:
#                 p_sum += probability
#                 if rnd <= p_sum:
#                     new_points.add(function(*point))
#                     break

#         points.update(new_points)
#         print(i)

#     # find out image limits determine scaling and translating
#     min_x = min(points, key=lambda p: p[0])[0]
#     max_x = max(points, key=lambda p: p[0])[0]
#     min_y = min(points, key=lambda p: p[1])[1]
#     max_y = max(points, key=lambda p: p[1])[1]
#     p_width = max_x - min_x
#     p_height = max_y - min_y

#     width_scale = width / p_width
#     height_scale = height / p_height
#     scale = min(width_scale, height_scale)

#     # create new image
#     image = Image.new("RGB", (width, height))
#     draw = ImageDraw.Draw(image)

#     # plot points
#     for point in points:
#         x = (point[0] - min_x) * scale
#         y = height - (point[1] - min_y) * scale
#         draw.point((x, y))

#     # save image file
#     image.save(outputfile, "PNG")


# def parse(filename):
#     with open(filename) as f:
#         definition = load(f)

#     # check for errors
#     if "width" not in definition:
#         raise ValueError('"width" parameter missing')
#     if "height" not in definition:
#         raise ValueError('"height" parameter missing')
#     if "iterations" not in definition:
#         raise ValueError('"iterations" parameter missing')
#     if "transformations" not in definition:
#         raise ValueError('"transformations" parameter missing')

#     def make_t_function(expression):
#         return lambda x, y: eval(expression, {"x": x, "y": y})

#     definition["transformations"] = [
#         (float(probability), make_t_function(expression))
#         for probability, expression in definition["transformations"]
#     ]

#     return definition


# if __name__ == "__main__":

#     import sys

#     # if there is one argument and it's not "-"
#     if len(sys.argv) > 1 and sys.argv[1] != "-":
#         # process each filename in input
#         for filename in sys.argv[1:]:
#             result = parse(filename)
#             process_file(
#                 result["transformations"],
#                 result["width"],
#                 result["height"],
#                 result["iterations"],
#                 filename.split(".")[0] + ".png",
#             )
#     else:
#         # read contents from stdin
#         eval(sys.stdin.read())
#         process_file(transformation, width, height, iterations)
