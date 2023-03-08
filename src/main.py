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
from typing import List, Tuple
from time import time

import sympy.geometry as sg

class OurTriangle:
  def __init__(self, triangle: sg.Triangle) -> None:
    self.triangle = triangle
    self.first_cut: sg.Triangle = None
    self.second_cut: sg.Triangle = None

def generate_triangles(area_min: int = 1, area_max: int = 30) -> List[sg.Triangle]:
  """
  Create all the triangles with an area between area_min and area_max and with integer base and height
  """
  triangles = []
  for areas in range(area_min, area_max):
    bases = [2*areas/i for i in range(1, areas*2+1)]
    for i in range(len(bases)-1, 0, -1):
      if not bases[i].is_integer():
        bases.pop(i)
    heights = bases.copy()
    heights.reverse()
    # The initialisation could probably be much better
    for index, base in enumerate(bases):
      for jndex in range(round(base/2) + 1):
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
  if triangle.area < 2:
    return []
  triangles = []
  a, b = get_equation(triangle.vertices[A], triangle.vertices[B])
  for area in range(2, triangle.area - 2):
    height = 2*area/triangle.base
    x = (height - b)/a
    triangles.append(sg.Triangle(triangle.vertices[0], triangle.vertices[1], sg.Point(x, height)))
  return triangles

if __name__ == "__main__":
  start = time()
  triangles = generate_triangles(area_max=30)
  solutions = []
  for triangle in triangles:
    first_cut = cut(triangle, 0, 2)
    second_cut = cut(triangle, 1, 2)
  print(f"Temps d'éxecution : {time() - start}s")