## Requirements:
1. pytorch
2. manim

## Run
`$ manim main.py`

## Explanation
- `DIV_ITER=24` in main.py is scaling factor for one-step expansion <br>
- `get_subrange` finds the region where about half of region diverges
- At now, `get_subrange` only find along horizontal(y=0) range
