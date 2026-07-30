import os
from mathverse import MathBoard
from mathverse.algebra import NumberLine, Grid2D

def test_algebra_number_line(tmp_path):
    board = MathBoard("Inequality Solution")
    board.add_step("x > 5", "Final Answer")
    
    nl = NumberLine(start=0, end=10)
    nl.plot_point(5, style="open", label="5")
    nl.shade_ray(5, direction="right", color="red")
    
    board.add_visual(nl)
    output_file = tmp_path / "nl_output.png"
    result_path = board.render(str(output_file))
    
    assert os.path.exists(result_path)
    assert len(board.visuals) == 1

def test_algebra_grid2d(tmp_path):
    board = MathBoard("System of Equations")
    grid = Grid2D()
    grid.draw_line(1, 0, color="blue", label="y = x")
    grid.draw_line(-1, 2, color="red", label="y = -x + 2")
    grid.highlight_intersection(1, 0, -1, 2)
    
    board.add_visual(grid)
    output_file = tmp_path / "grid_output.png"
    result_path = board.render(str(output_file))
    
    assert os.path.exists(result_path)
    assert len(board.visuals) == 1
