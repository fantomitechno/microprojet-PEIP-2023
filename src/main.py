"""
MIT License

Copyright (c) 2023 Simon - fantomitechno

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from typing import Set, Tuple
from time import time
from math import ceil, fabs
from tqdm import tqdm
from multiprocessing import Pool
from os import remove
from sympy import zoo

import sympy.geometry as sg


class SolutionTriangle:
    def __init__(
        self,
        triangle: sg.Triangle,
        first: sg.Triangle,
        second: sg.Triangle,
        third: sg.Triangle,
    ) -> None:
        self.triangle = triangle
        self.first = first
        self.second = second
        self.third = third


def generate_triangles(
    area_min: int = 1, area_max: int = 30, step: float = 1
) -> Set[sg.Triangle]:
    """
    Create all the triangles with an area between area_min and area_max and with integer base and height
    """
    triangles = set()
    for area in tqdm(range(area_min, area_max + 1)):
        bases = [2 * area / i for i in range(1, area * 2 + 1)]
        for i in range(len(bases) - 1, 0, -1):
            if not bases[i].is_integer():
                bases.pop(i)
        heights = bases.copy()
        heights.reverse()
        # The initialisation could probably be much better
        for index, base in enumerate(bases):
            for jndex in range(
                -round(base * (1 / step)), round((ceil(base / 2) * (1 / step) + 1))
            ):
                triangles.add(
                    sg.Triangle(
                        sg.Point(0, 0),
                        sg.Point(base, 0),
                        sg.Point(jndex * step, heights[index]),
                    )
                )
    print(f"{len(triangles)} triangles générés")
    return triangles


def get_equation(first: sg.Point2D, second: sg.Point2D) -> Tuple[int, int]:
    """
    Get the equation of the line passing through two points
    Return (a, b) with y = ax + b
    """
    a = (second.y - first.y) / (second.x - first.x)
    b = first.y - a * first.x
    return a, b


def cut(triangle: sg.Triangle, A: int = 0, B: int = 2) -> Set[sg.Triangle]:
    """
    Cut a triangle in two
    """
    if fabs(triangle.area) < 2:
        print("Area too small")
        return set()

    triangles = set()
    a, b = get_equation(triangle.vertices[A], triangle.vertices[B])

    for area in range(2, round(fabs(triangle.area) - 2)):
        height = 2 * area / triangle.vertices[1].x

        if a == zoo:  # Vertical line (zoo = infinity)
            if height > triangle.vertices[B].y:  # Impossible triangle somehow
                continue
            x = triangle.vertices[B].x
        else:
            x = (height - b) / a
        triangles.add(
            sg.Triangle(triangle.vertices[0], triangle.vertices[1], sg.Point(x, height))
        )
    return triangles


def run(triangles: Tuple[Set[sg.Triangle], int]):
    solutions = open("solutions-" + str(triangles[1]) + ".txt", "w")
    solutionsCSV = open("solutions-" + str(triangles[1]) + ".csv", "w")
    raw = open("raw-" + str(triangles[1]) + ".txt", "w")
    for triangle in triangles[0]:
        first_cut = cut(triangle, 0, 2)
        second_cut = cut(triangle, 1, 2)
        for first in first_cut:
            for second in second_cut:
                crossing = first.intersection(second)
                crossing: sg.Point2D = [i for i in crossing if i.is_Point][0]
                third = sg.Triangle(
                    triangle.vertices[0], triangle.vertices[1], crossing
                )
                if third.area.is_integer and third.area != 0:
                    solutions.write(
                        f"Triangle : {triangle} {triangle.area}\nPremier découpage : {first}\nDeuxième découpage : {second}\nTroisième découpage : {third}\n\n"
                    )
                    solutionsCSV.write(
                        f"{triangle.area},={triangle.vertices[1].x},={triangle.vertices[2].y},={triangle.vertices[2].x},={first.vertices[2].x},"
                        + f"={first.vertices[2].y},={first.area},={second.vertices[2].x},={second.vertices[2].y},={second.area},={third.vertices[2].x},"
                        + f"={third.vertices[2].y},={third.area},={first.area-third.area},={second.area-third.area},"
                        + f"={triangle.area - (first.area + second.area - third.area)}\n"
                    )
                    raw.write(
                        f"Triangle : {triangle} {triangle.area}\nPremier découpage : {first}\nDeuxième découpage : {second}\nTroisième découpage : {third}\n\n"
                    )
        if not len(first_cut) or not len(second_cut):
            raw.write(
                f"Triangle : {triangle} {triangle.area}\nPremier découpage : None\nDeuxième découpage : None\nTroisième découpage : None\n\n"
            )
    solutions.close()
    solutionsCSV.close()
    raw.close()


if __name__ == "__main__":
    start = time()
    triangles = generate_triangles(step=1 / 2)

    n = len(triangles)
    triangles = [
        (set(list(triangles)[i * n // 10 : (i + 1) * n // 10]), i) for i in range(10)
    ]

    with Pool(10) as p:
        p.map(run, triangles)

    solutionsCSV = open("solutions.csv", "w")
    solutionsCSV.write(
        "Aire, Base, Hauteur, Abscisse de la hauteur, Abscisse du point de premier découpage, "
        + "Ordonnée du point de premier découpage, Aire du premier découpage, Abscisse du point de deuxième découpage, "
        + "Ordonnée du point de deuxième découpage, Aire du deuxième découpage, Abscisse du croisement, Ordonnée du croisement, "
        + "Aire du triangle sous le croisement, Aire du triangle à gauche du croisement, Aire du triangle à droite du croisement, "
        + "Aire du quadrilatère au dessus du croisement\n"
    )
    solutions = open("solutions.txt", "w")
    raw = open("raw.txt", "w")
    for i in range(10):
        solutionsCSV.write(open("solutions-" + str(i) + ".csv", "r").read())
        remove("solutions-" + str(i) + ".csv")
        raw.write(open("raw-" + str(i) + ".txt", "r").read())
        remove("raw-" + str(i) + ".txt")
        solutions.write(open("solutions-" + str(i) + ".txt", "r").read())
        remove("solutions-" + str(i) + ".txt")
    solutionsCSV.close()
    raw.close()
    solutions.close()

    solutions = len(open("solutions.csv", "r").read().splitlines()) - 1

    print(f"{solutions} solutions trouvées")
    print(f"Temps d'éxecution : {time() - start}s")
    from no_solution import run_check

    run_check()
