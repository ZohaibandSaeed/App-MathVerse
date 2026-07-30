import os
from mathverse import MathBoard
from mathverse.calculus import CalculusGraph

def test_advanced_calculus(tmp_path):
    board = MathBoard("Advanced Calculus test")
    cg = CalculusGraph(x_range=(-5, 5))
    
    # 1. Riemann
    cg.plot_function("x**2")
    cg.draw_riemann_rectangles("x**2", start=0, end=3, n=6, method="right")
    
    # 2. Secant
    cg.draw_secant("x**2", x1=-2, x2=1)
    
    # 3. Hole
    cg.plot_hole(0, 0)
    
    # 4. Parametric
    cg.plot_parametric("2*np.cos(t)", "2*np.sin(t)", t_range=(0, 3.14))
    
    # 5. Polar
    cg.plot_polar("1 + np.cos(theta)", theta_range=(0, 6.28))
    
    # 6. Slope Field
    cg.plot_slope_field("x + y", x_points=10, y_points=10)
    
    # 7. Extrema
    cg.highlight_extrema("np.sin(x)")
    
    board.add_visual(cg)
    output_file = tmp_path / "advanced_calc_output.png"
    result_path = board.render(str(output_file))
    
    assert os.path.exists(result_path)
