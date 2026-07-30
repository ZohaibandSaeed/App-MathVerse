# MathVerse

MathVerse is a powerful, open-source, LLM-friendly Python library designed to act as a visual rendering engine for math. It makes it incredibly easy for Large Language Models (like Gemini) and developers to generate step-by-step mathematical solutions and beautiful geometric/algebraic diagrams.

## Features
- **Step-by-step Equation Rendering:** Render mathematical steps like a digital whiteboard.
- **Algebra Visualization:** 1D Number lines (rays, intervals) and 2D Grids (lines, intersections, shapes, vectors, inequalities).
- **Calculus Visualization:** Advanced 2D function plotting, tangent lines (auto-derivatives), Riemann sums, definite integrals (area shading), secant lines, parametric/polar curves, and slope fields!

## Installation

You can install MathVerse via pip:

```bash
pip install mathverse
```

## Quick Start

Here is a quick example of how to solve an inequality and draw a number line:

```python
from mathverse import MathBoard, NumberLine

# Initialize the board
board = MathBoard("Solving an Inequality")

# Add steps
board.add_step("2x > 4", "Divide both sides by 2")
board.add_step("x > 2", "Final Answer")

# Create and add a visual diagram
nl = NumberLine(start=-2, end=6)
nl.plot_point(2, style="open", label="2")
nl.shade_ray(2, direction="right", color="red")
board.add_visual(nl)

# Render output
board.render("result.png")
```

## Calculus Example

```python
from mathverse import MathBoard, CalculusGraph

board = MathBoard("Calculus Example")
cg = CalculusGraph(x_range=(-5, 5))

# Plot a function and its tangent
cg.plot_function("x**2")
cg.draw_tangent("x**2", x_point=2.0)
cg.shade_integral("x**2", start=0, end=2)

board.add_visual(cg)
board.render("calculus_result.png")
```
