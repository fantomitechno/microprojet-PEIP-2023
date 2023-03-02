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
from typing import List
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
    # areas = 30
    bases = [2*areas/i for i in range(1, areas*2+1)]
    for i in range(len(bases)-1, 0, -1):
      if not bases[i].is_integer():
        bases.pop(i)
    heights = bases.copy()
    heights.reverse()
    # The initialisation could probably be much better
    # print(bases)
    # print(heights)
    for index, base in enumerate(bases):
    # index = 0
    # base = bases[index]
      for jndex in range(round(base/2) + 1):
        triangles.append(sg.Triangle(sg.Point(0, 0), sg.Point(base, 0), sg.Point(jndex, heights[index])))
      # for triangle in triangles:
      #   print(triangle.area)
  print(f"{len(triangles)} triangles générés")
  return triangles


def cut(triangle: sg.Triangle, A: int = 0, B: int = 1) -> List[sg.Triangle]:
  """
  Cut a triangle in two
  """

if __name__ == "__main__":
  start = time()
  triangles = generate_triangles(area_max=30)
  solutions = []
  for triangle in triangles:
    cut(triangle)
  print(f"Temps d'éxecution : {time() - start}s")