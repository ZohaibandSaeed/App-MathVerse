"""
Calculus Graphing Module
"""
import numpy as np
import math

class CalculusGraph:
    """A 2D graph optimized for smooth continuous functions and calculus."""
    
    def __init__(self, x_range=(-5, 5), y_range=None):
        self.x_range = x_range
        self.y_range = y_range
        self.elements = []
        
    def _evaluate(self, expr: str, x_vals):
        """Safely evaluates the math expression over an array x."""
        env = {"x": x_vals, "np": np, "math": math}
        return eval(expr, {"__builtins__": {}}, env)
        
    def plot_function(self, expression: str, color="blue", label=""):
        self.elements.append({"type": "func", "expr": expression, "color": color, "label": label})
        
    def draw_tangent(self, expression: str, x_point: float, line_length: float = 3.0, color="red"):
        self.elements.append({"type": "tangent", "expr": expression, "x": x_point, "len": line_length, "color": color})
        
    def shade_integral(self, expression: str, start: float, end: float, color="green", alpha: float = 0.3):
        self.elements.append({"type": "integral", "expr": expression, "start": start, "end": end, "color": color, "alpha": alpha})
        
    def shade_area_between(self, expr1: str, expr2: str, start: float, end: float, color="purple", alpha: float = 0.3):
        self.elements.append({"type": "integral_between", "e1": expr1, "e2": expr2, "start": start, "end": end, "color": color, "alpha": alpha})

    def draw_asymptote(self, x=None, y=None, color="gray"):
        self.elements.append({"type": "asymptote", "x": x, "y": y, "color": color})

    def draw_riemann_rectangles(self, expression: str, start: float, end: float, n: int, method: str = "left", color="orange", alpha: float = 0.4):
        self.elements.append({"type": "riemann", "expr": expression, "start": start, "end": end, "n": n, "method": method, "color": color, "alpha": alpha})

    def draw_secant(self, expression: str, x1: float, x2: float, color="orange", label=""):
        self.elements.append({"type": "secant", "expr": expression, "x1": x1, "x2": x2, "color": color, "label": label})

    def plot_hole(self, x: float, y: float, color="blue"):
        self.elements.append({"type": "hole", "x": x, "y": y, "color": color})

    def plot_parametric(self, x_expr: str, y_expr: str, t_range: tuple, color="purple", label=""):
        self.elements.append({"type": "parametric", "x_expr": x_expr, "y_expr": y_expr, "t_range": t_range, "color": color, "label": label})

    def plot_polar(self, r_expr: str, theta_range: tuple, color="magenta", label=""):
        self.elements.append({"type": "polar", "r_expr": r_expr, "theta_range": theta_range, "color": color, "label": label})

    def plot_slope_field(self, dy_dx_expr: str, x_points=20, y_points=20, color="gray"):
        self.elements.append({"type": "slope_field", "expr": dy_dx_expr, "xp": x_points, "yp": y_points, "color": color})

    def highlight_extrema(self, expression: str, color="black"):
        self.elements.append({"type": "extrema", "expr": expression, "color": color})

    def draw(self, ax, center_y: float = 0.0, height: float = 0.4):
        width = 0.6
        inset_ax = ax.inset_axes([0.5 - width/2, center_y - height/2, width, height])
        
        inset_ax.set_xlim(self.x_range)
        inset_ax.grid(True, linestyle='--', alpha=0.6)
        
        # Origin lines
        inset_ax.axhline(0, color='black', lw=1.5)
        inset_ax.axvline(0, color='black', lw=1.5)
        
        x_vals = np.linspace(self.x_range[0], self.x_range[1], 1000)
        all_y = []
        
        for el in self.elements:
            if el["type"] == "func":
                y_vals = self._evaluate(el["expr"], x_vals)
                all_y.extend(y_vals)
                inset_ax.plot(x_vals, y_vals, color=el["color"], label=f"${el['label']}$" if el["label"] else None, lw=2, zorder=3)
                
            elif el["type"] == "tangent":
                xp = el["x"]
                h = 1e-5
                y0 = self._evaluate(el["expr"], np.array([xp - h]))[0]
                y1 = self._evaluate(el["expr"], np.array([xp + h]))[0]
                yp = self._evaluate(el["expr"], np.array([xp]))[0]
                slope = (y1 - y0) / (2 * h)
                inset_ax.plot(xp, yp, 'ko', zorder=5)
                l = el["len"] / 2
                x_tan = np.array([xp - l, xp + l])
                y_tan = yp + slope * (x_tan - xp)
                inset_ax.plot(x_tan, y_tan, color=el["color"], linestyle='--', lw=2, zorder=4)
                
            elif el["type"] == "integral":
                x_int = np.linspace(el["start"], el["end"], 200)
                y_int = self._evaluate(el["expr"], x_int)
                inset_ax.fill_between(x_int, y_int, 0, color=el["color"], alpha=el["alpha"], zorder=2)
                
            elif el["type"] == "integral_between":
                x_int = np.linspace(el["start"], el["end"], 200)
                y_int1 = self._evaluate(el["e1"], x_int)
                y_int2 = self._evaluate(el["e2"], x_int)
                inset_ax.fill_between(x_int, y_int1, y_int2, color=el["color"], alpha=el["alpha"], zorder=2)
                
            elif el["type"] == "asymptote":
                if el["x"] is not None:
                    inset_ax.axvline(el["x"], color=el["color"], linestyle='--', lw=2, zorder=1)
                if el["y"] is not None:
                    inset_ax.axhline(el["y"], color=el["color"], linestyle='--', lw=2, zorder=1)
                    
            elif el["type"] == "riemann":
                dx = (el["end"] - el["start"]) / el["n"]
                import matplotlib.patches as patches
                for i in range(el["n"]):
                    if el["method"] == "left":
                        xi = el["start"] + i * dx
                    elif el["method"] == "right":
                        xi = el["start"] + (i + 1) * dx
                    else: # midpoint
                        xi = el["start"] + (i + 0.5) * dx
                    yi = self._evaluate(el["expr"], np.array([xi]))[0]
                    x_rect = el["start"] + i * dx
                    rect = patches.Rectangle((x_rect, 0), dx, yi, edgecolor="black", facecolor=el["color"], alpha=el["alpha"], lw=1, zorder=2)
                    inset_ax.add_patch(rect)
                    
            elif el["type"] == "secant":
                x1, x2 = el["x1"], el["x2"]
                y1 = self._evaluate(el["expr"], np.array([x1]))[0]
                y2 = self._evaluate(el["expr"], np.array([x2]))[0]
                inset_ax.plot([x1, x2], [y1, y2], 'ko', zorder=5)
                slope = (y2 - y1) / (x2 - x1)
                length = (self.x_range[1] - self.x_range[0])
                x_sec = np.array([x1 - length, x2 + length])
                y_sec = y1 + slope * (x_sec - x1)
                inset_ax.plot(x_sec, y_sec, color=el["color"], linestyle='--', lw=2, zorder=4)
                if el["label"]:
                    inset_ax.text((x1+x2)/2, (y1+y2)/2 + 0.5, f"${el['label']}$", color=el["color"])
                    
            elif el["type"] == "hole":
                inset_ax.plot(el["x"], el["y"], marker='o', markerfacecolor='white', markeredgecolor=el["color"], markersize=8, markeredgewidth=2, zorder=6)
                
            elif el["type"] == "parametric":
                t_vals = np.linspace(el["t_range"][0], el["t_range"][1], 1000)
                env = {"t": t_vals, "np": np, "math": math}
                xt = eval(el["x_expr"], {"__builtins__": {}}, env)
                yt = eval(el["y_expr"], {"__builtins__": {}}, env)
                all_y.extend(yt)
                inset_ax.plot(xt, yt, color=el["color"], label=f"${el['label']}$" if el["label"] else None, lw=2, zorder=3)
                
            elif el["type"] == "polar":
                th_vals = np.linspace(el["theta_range"][0], el["theta_range"][1], 1000)
                env = {"theta": th_vals, "np": np, "math": math}
                rt = eval(el["r_expr"], {"__builtins__": {}}, env)
                xt = rt * np.cos(th_vals)
                yt = rt * np.sin(th_vals)
                all_y.extend(yt)
                inset_ax.plot(xt, yt, color=el["color"], label=f"${el['label']}$" if el["label"] else None, lw=2, zorder=3)
                
            elif el["type"] == "slope_field":
                y_r = self.y_range if self.y_range else (-5, 5)
                X, Y = np.meshgrid(np.linspace(self.x_range[0], self.x_range[1], el["xp"]), 
                                   np.linspace(y_r[0], y_r[1], el["yp"]))
                env = {"x": X, "y": Y, "np": np, "math": math}
                dy = eval(el["expr"], {"__builtins__": {}}, env)
                # Ensure dy is array
                if np.isscalar(dy):
                    dy = np.ones_like(X) * dy
                dx = np.ones_like(dy)
                L = np.sqrt(dx**2 + dy**2)
                L[L == 0] = 1 # prevent div by zero
                dx, dy = dx/L, dy/L
                inset_ax.quiver(X, Y, dx, dy, color=el["color"], pivot='mid', scale=el["xp"]*1.5, zorder=1, alpha=0.5)
                
            elif el["type"] == "extrema":
                y_vals = self._evaluate(el["expr"], x_vals)
                dy = np.diff(y_vals)
                sign_changes = np.where(np.diff(np.sign(dy)))[0]
                for idx in sign_changes:
                    if abs(dy[idx] - dy[idx+1]) > 1e-4:
                        xp, yp = x_vals[idx+1], y_vals[idx+1]
                        inset_ax.plot(xp, yp, marker='o', color=el["color"], zorder=6)
                        label = "Min" if dy[idx+1] > dy[idx] else "Max"
                        inset_ax.text(xp, yp - 0.5 if label == "Min" else yp + 0.5, label, color=el["color"], ha="center", fontsize=9, zorder=7)

        if self.y_range:
            inset_ax.set_ylim(self.y_range)
        elif all_y:
            y_min, y_max = np.nanmin(all_y), np.nanmax(all_y)
            if not np.isinf(y_min) and not np.isinf(y_max):
                pad = (y_max - y_min) * 0.1
                if pad == 0: pad = 1
                inset_ax.set_ylim([y_min - pad, y_max + pad])
            
        if any(el.get("label") for el in self.elements if el["type"] in ["func", "parametric", "polar"]):
            inset_ax.legend(loc="best")
