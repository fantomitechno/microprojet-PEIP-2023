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
from pygsheets import authorize, Worksheet
from pygsheets.client import Client

gc: Client = authorize(service_file="creds.json")

file = gc.open("solutions")

sheet: Worksheet = file.worksheet_by_title("view")

letters = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
    "AA",
    "AB",
    "AC",
    "AD",
    "AE",
    "AF",
    "AG",
    "AH",
    "AI",
    "AJ",
    "AK",
    "AL",
    "AM",
    "AN",
    "AO",
    "AP",
    "AQ",
    "AR",
    "AS",
    "AT",
    "AU",
    "AV",
    "AW",
    "AX",
    "AY",
    "AZ",
    "BA",
    "BB",
    "BC",
    "BD",
    "BE",
    "BF",
    "BG",
    "BH",
    "BI",
    "BJ",
    "BK",
    "BL",
    "BM",
    "BN",
    "BO",
    "BP",
    "BQ",
    "BR",
    "BS",
    "BT",
    "BU",
    "BV",
    "BW",
    "BX",
    "BY",
    "BZ",
]


if sheet.cols < len(letters):
    sheet.add_cols(len(letters) - sheet.cols)

for i in range(1, 61):
    for j in range(1, 61):
        f = open("solutions.csv", "r")
        lines = f.readlines()
        count = 0
        if (i * j / 2).is_integer():
            for line in lines:
                if line.startswith(
                    str(round(i * j / 2)) + ",=" + str(i) + ",=" + str(j)
                ):
                    count += 1
        sheet.update_value(letters[i] + str(j + 1), count)
        sheet.cell(letters[i] + str(j + 1)).color = (
            (1, 0, 0, 0.5) if count == 0 else (0, 1, 0, 0.5)
        )
