"""
Core Board Module
This module provides the main MathBoard class to orchestrate math rendering.
"""
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

# Configure matplotlib to use Computer Modern (LaTeX style) for math text
mpl.rcParams['mathtext.fontset'] = 'cm'
mpl.rcParams['font.family'] = 'serif'

class MathBoard:
    """
    The main canvas for rendering mathematical equations and diagrams.
    Designed with a simple, declarative API for LLM code generation.
    """
    
    def __init__(self, title: str = "Math Solution"):
        """Initialize a new math board."""
        self.title = title
        self.steps = []
        self.visuals = []
        
    def add_visual(self, visual_obj):
        """Add an algebraic visual (like NumberLine or Grid2D) to the board."""
        self.visuals.append(visual_obj)
        
    def add_step(self, equation: str, description: str = ""):
        """
        Add a new mathematical step.
        
        Args:
            equation (str): The mathematical equation (in LaTeX format if possible).
            description (str): A short description of what this step does.
        """
        # Ensure the equation is wrapped in $...$ for matplotlib math text rendering
        eq = equation.strip()
        if not eq.startswith('$') and not eq.startswith('\\['):
            eq = f"${eq}$"
            
        self.steps.append({"equation": eq, "description": description})
        
    def render(self, output_path: str = "output.png"):
        """
        Render the board to a file (e.g., PNG or SVG).
        
        Args:
            output_path (str): The file path to save the output.
        """
        # Create a new figure
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.axis('off') # Hide axes for a clean board
        
        # Add Title
        ax.text(0.5, 0.95, self.title, fontsize=18, fontweight='bold', ha='center', transform=ax.transAxes)
        
        # Draw steps vertically from top to bottom
        y_pos = 0.85
        line_spacing = 0.1
        
        for i, step in enumerate(self.steps):
            # Display step number and description
            desc_text = f"Step {i+1}: {step['description']}" if step['description'] else f"Step {i+1}:"
            ax.text(0.05, y_pos, desc_text, fontsize=12, color='gray', transform=ax.transAxes)
            y_pos -= 0.05
            
            # Display the equation (indented)
            ax.text(0.2, y_pos, step['equation'], fontsize=16, color='black', transform=ax.transAxes)
            y_pos -= line_spacing
            
        # Draw algebraic visuals (if any)
        for vis in self.visuals:
            y_pos -= 0.1 # Padding
            # visual height is approx 0.3 of the board
            vis.draw(ax, center_y=y_pos, height=0.3)
            y_pos -= 0.35
            
        # Ensure the directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            
        # Save the figure
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
        plt.close(fig)
        return output_path
