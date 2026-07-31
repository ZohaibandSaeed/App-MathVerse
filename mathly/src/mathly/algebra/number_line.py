"""
Number Line Module for 1D Algebra (Inequalities, Intervals)
"""

class NumberLine:
    """A 1D number line visualizer."""
    
    def __init__(self, start: int = -5, end: int = 5):
        self.start = start
        self.end = end
        self.elements = []
        
    def plot_point(self, value: float, style: str = "closed", label: str = ""):
        """Plot a point on the number line."""
        self.elements.append({"type": "point", "value": value, "style": style, "label": label})
        
    def shade_interval(self, start: float, end: float, color: str = "blue", alpha: float = 0.3):
        """Shade a region between two values."""
        self.elements.append({"type": "interval", "start": start, "end": end, "color": color, "alpha": alpha})
        
    def shade_ray(self, start: float, direction: str, color: str = "blue", alpha: float = 0.3):
        """Shade from a point to infinity (direction='right' or 'left')."""
        self.elements.append({"type": "ray", "start": start, "direction": direction, "color": color, "alpha": alpha})

    def draw(self, ax, center_y: float = 0.0, height: float = 0.2):
        """Draws the number line on the given matplotlib Axes via inset_axes."""
        # Create an inset axes to bound the number line cleanly
        width = 0.8
        inset_ax = ax.inset_axes([0.5 - width/2, center_y - height/2, width, height])
        inset_ax.axis('off')
        
        y_pos = 0.5 # relative to inset_ax
        
        # Draw the main line
        inset_ax.hlines(y_pos, self.start, self.end, colors='black', linewidth=1.5)
        
        # Draw arrows at the ends
        inset_ax.annotate('', xy=(self.end + 0.5, y_pos), xytext=(self.end, y_pos),
                    arrowprops=dict(arrowstyle="->", color='black', lw=1.5))
        inset_ax.annotate('', xy=(self.start - 0.5, y_pos), xytext=(self.start, y_pos),
                    arrowprops=dict(arrowstyle="->", color='black', lw=1.5))
                    
        # Draw ticks and labels
        for i in range(int(self.start), int(self.end) + 1):
            inset_ax.vlines(i, y_pos - 0.1, y_pos + 0.1, colors='black', linewidth=1)
            inset_ax.text(i, y_pos - 0.2, str(i), ha='center', va='top', fontsize=10)
            
        # Draw elements
        for el in self.elements:
            if el["type"] == "point":
                facecolor = "black" if el["style"] == "closed" else "white"
                inset_ax.plot(el["value"], y_pos, marker='o', markersize=8, 
                        markeredgecolor='black', markerfacecolor=facecolor, zorder=3)
                if el["label"]:
                    inset_ax.text(el["value"], y_pos + 0.2, f"${el['label']}$", ha='center', va='bottom', fontsize=12)
            
            elif el["type"] == "interval":
                inset_ax.hlines(y_pos, el["start"], el["end"], colors=el["color"], linewidth=4, alpha=el["alpha"], zorder=2)
                
            elif el["type"] == "ray":
                end_val = self.end + 0.4 if el["direction"] == "right" else self.start - 0.4
                inset_ax.hlines(y_pos, el["start"], end_val, colors=el["color"], linewidth=4, alpha=el["alpha"], zorder=2)
                # Ray arrow
                inset_ax.annotate('', xy=(end_val, y_pos), xytext=(end_val - (0.1 if el["direction"] == "right" else -0.1), y_pos),
                    arrowprops=dict(arrowstyle="->", color=el["color"], lw=4, alpha=el["alpha"]))
