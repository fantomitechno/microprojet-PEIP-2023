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
from requests import post
from typing import AbstractSet, Tuple
from time import time
from math import ceil, fabs
from sympy import zoo

import sympy.geometry as sg

class SolutionTriangle:
  def __init__(self, triangle: sg.Triangle, first: sg.Triangle, second: sg.Triangle, third: sg.Triangle) -> None:
    self.triangle = triangle
    self.first = first
    self.second = second
    self.third = third

def generate_triangles(area_min: int = 1, area_max: int = 30, step: int = 1) -> AbstractSet[sg.Triangle]:
  """
  Create all the triangles with an area between area_min and area_max and with integer base and height
  """
  triangles = set()
  for areas in range(area_min, area_max+1):
    bases = [2*areas/i for i in range(1, areas*2+1)]
    for i in range(len(bases)-1, 0, -1):
      if not bases[i].is_integer():
        bases.pop(i)
    heights = bases.copy()
    heights.reverse()
    # The initialisation could probably be much better
    for index, base in enumerate(bases):
      if index >= ceil(len(bases)/2):
        continue
      for jndex in range(0, round((ceil(base/2)*(1/step) + 1))):
        triangles.add(sg.Triangle(sg.Point(0, 0), sg.Point(base, 0), sg.Point(jndex*step, heights[index])))
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

def cut(triangle: sg.Triangle, A: int = 0, B: int = 2, step: int = 1) -> AbstractSet[sg.Triangle]:
  """
  Cut a triangle in two
  """
  if fabs(triangle.area) < 2:
    print("Area too small")
    return set()

  triangles = set()
  a, b = get_equation(triangle.vertices[A], triangle.vertices[B])

  for area in range(2, round((fabs(triangle.area) - 2)*(1/step))):
    height = 2*area*step/triangle.vertices[1].x

    if a == zoo: # Vertical line (zoo = infinity)
      if height > triangle.vertices[B].y: # Impossible triangle somehow
        continue
      x = triangle.vertices[B].x
    else:
      x = (height - b)/a
    triangles.add(sg.Triangle(triangle.vertices[0], triangle.vertices[1], sg.Point(x, height)))
  return triangles

def check_not_solution(solutions: AbstractSet[SolutionTriangle], area_min: int = 1, area_max: int = 30) -> AbstractSet[int]:
  """
  Check for no solutions
  """
  not_solution = set()
  for area in range(area_min, area_max+1):
    if not any([solution.triangle.area == area for solution in solutions]):
      not_solution.add(area)
  return not_solution

if __name__ == "__main__":
  start = time()

  triangles = generate_triangles(step=1/2)
  solutions: AbstractSet[SolutionTriangle] = set()
  raw: AbstractSet[SolutionTriangle] = set()
  
  for triangle in triangles:
    first_cut = cut(triangle, 0, 2, step=1/2)
    second_cut = cut(triangle, 1, 2, step=1/2)
  
    for first in first_cut:
      for second in second_cut:
        crossing = first.intersection(second)
        crossing: sg.Point2D = [i for i in crossing if i.is_Point][0]
  
        third = sg.Triangle(triangle.vertices[0], triangle.vertices[1], crossing)
        if third.area.is_integer and third.area != 0:
          solutions.add(SolutionTriangle(triangle, first, second, third))
        raw.add(SolutionTriangle(triangle, first, second, third))
    if not len(first_cut) or not len(second_cut):
      raw.add(SolutionTriangle(triangle, None, None, None))
        
  
  not_solution = check_not_solution(solutions, area_max=30)

  print(f"{len(solutions)} solutions trouvées")
  print(f"Temps d'éxecution : {time() - start}s")
  f = open("solutions.txt", "w")
  for solution in solutions:
    f.write(f"Triangle : {solution.triangle} {solution.triangle.area}\nPremier découpage : {solution.first}\nDeuxième découpage : {solution.second}\nTroisième découpage : {solution.third}\n\n")
  f.close()
  f = open("raw.txt", "w")
  for r in raw:
    f.write(f"Triangle : {r.triangle} {r.triangle.area}\nPremier découpage : {r.first}\nDeuxième découpage : {r.second}\nTroisième découpage : {r.third}\n\n")
  f.close()
  f = open("solutions.csv", "w")
  f.write("Aire, Base, Hauteur, Abscisse de la hauteur, Abscisse du point de premier découpage, Ordonnée du point de premier découpage, Abscisse du point de deuxième découpage, Ordonnée du point de deuxième découpage, Abscisse du point de troisième découpage, Ordonnée du point de troisième découpage\n")
  for solution in solutions:
    f.write(f"{solution.triangle.area}, {solution.triangle.vertices[1].x}, {solution.triangle.vertices[2].y}, {solution.triangle.vertices[2].x}, {solution.first.vertices[2].x}, {solution.first.vertices[2].y}, {solution.second.vertices[2].x}, {solution.second.vertices[2].y}, {solution.third.vertices[2].x}, {solution.third.vertices[2].y}\n")
  f.close()
  f = open("not_solution.txt", "w")
  for area in not_solution:
    f.write(f"{area}, ")
  f.close()