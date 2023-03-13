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


def check_has_no_solution(
    solutions: str, area_min: int = 1, area_max: int = 30
) -> List[int]:
    """
    Check for no solutions
    """
    no_solution = []
    for area in range(area_min, area_max + 1):
        if not any([solution.startswith(str(area) + ",") for solution in solutions]):
            no_solution.append(area)
    return no_solution


def check_has_solution(
    solutions: str, area_min: int = 1, area_max: int = 30
) -> List[int]:
    """
    Check for solutions
    """
    solution = []
    for area in range(area_min, area_max + 1):
        if any([solution.startswith(str(area) + ",") for solution in solutions]):
            solution.append(area)
    return solution


def run_check():
    with open("solutions.csv", "r") as file:
        solutions = file.read().splitlines()
    has_no_solution = check_has_no_solution(solutions)
    has_solution = check_has_solution(solutions)
    print(has_no_solution)
    print(has_solution)
    with open("has_no_solution.txt", "w") as file:
        file.write(str(has_no_solution))
    with open("has_solution.txt", "w") as file:
        file.write(str(has_solution))


if __name__ == "__main__":
    run_check()
