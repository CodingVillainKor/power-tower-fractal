## Requirements:
1. pytorch
2. manim

## Run
`$ manim main.py`

## Explanation
- `DIV_ITER=24` in main.py is a scaling factor for one-step expansion. <br>
- `get_subrange` finds the region where about half of region diverges. <br>
- Currently, `get_subrange` only searches the range along horizontal axis(y=0).
