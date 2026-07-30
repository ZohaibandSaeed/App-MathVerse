"""
2D Grid Module for Linear Algebra
"""
import numpy as np
import math
import matplotlib.patches as patches

class Grid2D:
    """A 2D coordinate grid visualizer."""
    
    def __init__(self, x_range=(-5, 5), y_range=(-5, 5)):
        self.x_range = x_range
        self.y_range = y_range
        self.elements = []
        
    def plot_coordinate(self, x: float, y: float, label: str = ""):
        self.elements.append({"type": "point", "x": x, "y": y, "label": label})
        
    def draw_line(self, m: float, c: float, color: str = "blue", label: str = ""):
        """Draw a line from equation y = mx + c"""
        self.elements.append({"type": "line_eq", "m": m, "c": c, "color": color, "label": label})
        
    def plot_function(self, func, x_range=None, color: str = "blue", label: str = "", points: int = 400):
        """Plot an arbitrary function y = f(x)."""
        self.elements.append({"type": "function", "func": func, "x_range": x_range, "color": color, "label": label, "points": points})
        
    def highlight_intersection(self, m1, c1, m2, c2):
        """Finds and highlights intersection of two lines."""
        if m1 == m2: return # Parallel
        x = (c2 - c1) / (m1 - m2)
        y = m1 * x + c1
        self.plot_coordinate(x, y, label=f"({round(x, 1)}, {round(y, 1)})")
        
    def draw_circle(self, x: float, y: float, radius: float, color: str = "blue", fill: bool = False, alpha: float = 0.3):
        """Draw a circle on the grid."""
        self.elements.append({"type": "circle", "x": x, "y": y, "r": radius, "color": color, "fill": fill, "alpha": alpha})
        
    def draw_polygon(self, points: list, color: str = "green", fill: bool = True, alpha: float = 0.3):
        """Draw a polygon (triangle, square, etc.) given a list of (x,y) coordinates."""
        self.elements.append({"type": "polygon", "points": points, "color": color, "fill": fill, "alpha": alpha})
        
    def draw_vector(self, origin: tuple, end: tuple, color: str = "red", label: str = ""):
        """Draw a directional vector arrow."""
        self.elements.append({"type": "vector", "origin": origin, "end": end, "color": color, "label": label})
        
    def draw_angle(self, vertex: tuple, p1: tuple, p2: tuple, radius: float = 0.5, label: str = "", color: str = "black"):
        """Draw an angle arc between two points from a vertex."""
        self.elements.append({"type": "angle", "vertex": vertex, "p1": p1, "p2": p2, "r": radius, "label": label, "color": color})
        
    def add_text(self, x: float, y: float, text: str, fontsize: int = 12, color: str = "black"):
        """Add floating text anywhere on the grid."""
        self.elements.append({"type": "text", "x": x, "y": y, "text": text, "fontsize": fontsize, "color": color})
        
    def shade_inequality(self, m: float, c: float, operator: str, color: str = "blue", alpha: float = 0.2):
        """
        Shade the region for an inequality y > mx + c or y < mx + c.
        operator must be '>', '<', '>=', or '<='.
        """
        self.elements.append({"type": "inequality", "m": m, "c": c, "operator": operator, "color": color, "alpha": alpha})

    def draw(self, ax, center_y: float = 0.0, height: float = 0.4):
        """Draws the grid in a sub-region of the main board."""
        width = 0.6
        inset_ax = ax.inset_axes([0.5 - width/2, center_y - height/2, width, height])
        
        inset_ax.set_xlim(self.x_range)
        inset_ax.set_ylim(self.y_range)
        inset_ax.grid(True, linestyle='--', alpha=0.6)
        
        # Origin lines
        inset_ax.axhline(0, color='black', lw=1.5)
        inset_ax.axvline(0, color='black', lw=1.5)
        
        for el in self.elements:
            if el["type"] == "point":
                inset_ax.plot(el["x"], el["y"], 'ro', zorder=5)
                if el["label"]:
                    inset_ax.text(el["x"]+0.2, el["y"]+0.2, f"${el['label']}$", fontsize=10)
            elif el["type"] == "line_eq":
                x_vals = np.array(self.x_range)
                y_vals = el["m"] * x_vals + el["c"]
                inset_ax.plot(x_vals, y_vals, color=el["color"], label=f"${el['label']}$" if el["label"] else None, zorder=4)
            elif el["type"] == "function":
                func_x_range = el["x_range"] if el["x_range"] else self.x_range
                x_vals = np.linspace(func_x_range[0], func_x_range[1], el.get("points", 400))
                y_vals = np.array([el["func"](x) for x in x_vals])
                inset_ax.plot(x_vals, y_vals, color=el["color"], label=f"${el['label']}$" if el["label"] else None, zorder=4)
            elif el["type"] == "circle":
                circle = patches.Circle((el["x"], el["y"]), el["r"], edgecolor=el["color"], 
                                        facecolor=el["color"] if el["fill"] else "none", 
                                        alpha=el["alpha"] if el["fill"] else 1.0, lw=2, zorder=3)
                inset_ax.add_patch(circle)
            elif el["type"] == "polygon":
                poly = patches.Polygon(el["points"], closed=True, edgecolor=el["color"], 
                                       facecolor=el["color"] if el["fill"] else "none", 
                                       alpha=el["alpha"] if el["fill"] else 1.0, lw=2, zorder=3)
                inset_ax.add_patch(poly)
            elif el["type"] == "vector":
                inset_ax.annotate('', xy=el["end"], xytext=el["origin"], 
                                  arrowprops=dict(arrowstyle="->", color=el["color"], lw=2), zorder=4)
                if el["label"]:
                    mid_x = (el["origin"][0] + el["end"][0]) / 2
                    mid_y = (el["origin"][1] + el["end"][1]) / 2
                    inset_ax.text(mid_x, mid_y + 0.3, f"${el['label']}$", color=el["color"], fontsize=11, ha="center")
            elif el["type"] == "angle":
                v = el["vertex"]
                a1 = math.degrees(math.atan2(el["p1"][1] - v[1], el["p1"][0] - v[0]))
                a2 = math.degrees(math.atan2(el["p2"][1] - v[1], el["p2"][0] - v[0]))
                if a2 < a1: a1, a2 = a2, a1
                if a2 - a1 > 180: a1, a2 = a2, a1 + 360
                
                arc = patches.Arc(v, el["r"]*2, el["r"]*2, angle=0.0, theta1=a1, theta2=a2, edgecolor=el["color"], lw=1.5, zorder=4)
                inset_ax.add_patch(arc)
                
                if el["label"]:
                    mid_a = math.radians((a1 + a2) / 2)
                    lx = v[0] + (el["r"] + 0.3) * math.cos(mid_a)
                    ly = v[1] + (el["r"] + 0.3) * math.sin(mid_a)
                    inset_ax.text(lx, ly, f"${el['label']}$", color=el["color"], ha='center', va='center', fontsize=10)
            elif el["type"] == "text":
                inset_ax.text(el["x"], el["y"], f"${el['text']}$", fontsize=el["fontsize"], color=el["color"], zorder=5)
            elif el["type"] == "inequality":
                x_vals = np.array(self.x_range)
                y_vals = el["m"] * x_vals + el["c"]
                if ">" in el["operator"]:
                    inset_ax.fill_between(x_vals, y_vals, self.y_range[1], color=el["color"], alpha=el["alpha"], zorder=2)
                elif "<" in el["operator"]:
                    inset_ax.fill_between(x_vals, self.y_range[0], y_vals, color=el["color"], alpha=el["alpha"], zorder=2)
                linestyle = '--' if '=' not in el["operator"] else '-'
                inset_ax.plot(x_vals, y_vals, color=el["color"], linestyle=linestyle, zorder=3)
                
        if any(el.get("label") for el in self.elements if el["type"] in ["line_eq"]):
            inset_ax.legend(loc="upper right")
