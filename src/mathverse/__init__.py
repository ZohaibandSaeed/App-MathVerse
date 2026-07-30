"""
MathVerse Library
"""
from .core.board import MathBoard
from .algebra.number_line import NumberLine
from .algebra.grid2d import Grid2D
from .calculus.graph import CalculusGraph

__version__ = "0.1.0"
__all__ = ["MathBoard", "NumberLine", "Grid2D", "CalculusGraph"]
