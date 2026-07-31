from mathly.core.board import MathBoard
from mathly.algebra.grid2d import Grid2D
board = MathBoard("Mathly Playground")
grid = Grid2D(x_range=(-5, 5), y_range=(-5, 5))
grid.plot_function("x**2", color="blue", label="f(x) = x^2")
board.add_visual(grid)
board.render("output.png")
