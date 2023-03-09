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
from typing import List, Tuple
from time import time
from math import ceil, fabs
from sympy import zoo

import sympy.geometry as sg

class SolutionTriangle:
  def __init__(self, triangle: sg.Triangle, first: sg.Triangle, second: sg.Triangle) -> None:
    self.triangle = triangle
    self.first = first
    self.second = second

def generate_triangles(area_min: int = 1, area_max: int = 30) -> List[sg.Triangle]:
  """
  Create all the triangles with an area between area_min and area_max and with integer base and height
  """
  triangles = []
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
      for jndex in range(ceil(base/2) + 1):
        triangles.append(sg.Triangle(sg.Point(0, 0), sg.Point(base, 0), sg.Point(jndex, heights[index])))
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

def cut(triangle: sg.Triangle, A: int = 0, B: int = 2) -> List[sg.Triangle]:
  """
  Cut a triangle in two
  """
  if fabs(triangle.area) < 2:
    print("Area too small")
    return []

  triangles = []
  a, b = get_equation(triangle.vertices[A], triangle.vertices[B])

  for area in range(2, round(fabs(triangle.area) - 2)):
    height = 2*area/triangle.vertices[1].x

    if a == zoo: # Vertical line (zoo = infinity)
      if height > triangle.vertices[B].y: # Impossible triangle somehow
        continue
      x = triangle.vertices[B].x
    else:
      x = (height - b)/a
    triangles.append(sg.Triangle(triangle.vertices[0], triangle.vertices[1], sg.Point(x, height)))
  return triangles

if __name__ == "__main__":
  start = time()

  triangles = generate_triangles(area_max=20)
  solutions = []
  
  for triangle in triangles:
    first_cut = cut(triangle, 0, 2)
    second_cut = cut(triangle, 1, 2)
  
    for first in first_cut:
      for second in second_cut:
        crossing = first.intersection(second)
        crossing: sg.Point2D = [i for i in crossing if i.is_Point][0]
  
        third = sg.Triangle(triangle.vertices[0], triangle.vertices[1], crossing)
        if third.area.is_integer and third.area != 0:
          solutions.append(SolutionTriangle(triangle, first, second))
  
  print(f"{len(solutions)} solutions trouvées")
  print(f"Temps d'éxecution : {time() - start}s")
  f = open("solutions.txt", "w")
  for solution in solutions:
    f.write(f"Triangle : {solution.triangle}\nPremier découpage : {solution.first}\nDeuxième découpage : {solution.second}\n\n")
  f.close()