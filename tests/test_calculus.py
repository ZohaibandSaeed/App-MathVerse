import os
from mathverse import MathBoard
from mathverse.calculus import CalculusGraph

def test_calculus_graph(tmp_path):
    board = MathBoard("Definite Integral")
    board.add_step(r"\int_{0}^{\pi} \sin(x) dx", "Area under sine curve")
    
    # Render sin(x)
    cg = CalculusGraph(x_range=(0, 4))
    cg.plot_function("np.sin(x)", label=r"y = \sin(x)")
    cg.shade_integral("np.sin(x)", start=0, end=3.14159, color="green")
    cg.draw_tangent("np.sin(x)", x_point=1.5708, color="red") # Tangent at pi/2 (slope 0)
    
    board.add_visual(cg)
    output_file = tmp_path / "calculus_output.png"
    result_path = board.render(str(output_file))
    
    assert os.path.exists(result_path)
    assert len(board.visuals) == 1
