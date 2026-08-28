from manimlib import *
import numpy as np

def get_requirements_cost(x):
    """Cost function for requirements and design phase."""
    return 2.0 * np.exp(-((x - 1.2) / 0.6) ** 2)

def get_acquisition_cost(x):
    """Cost function for acquisition and installation phase."""
    return 4.5 * np.exp(-((x - 2.8) / 0.7) ** 2)

def get_operating_cost(x):
    """Cost function for operating and maintenance phase."""
    rise = 1 / (1 + np.exp(-3 * (x - 4.0)))
    fall = 1 / (1 + np.exp(4 * (x - 9.0)))
    shape = 4.0 + 0.2 * x
    return shape * rise * fall

def get_phaseout_cost(x):
    """Cost function for phaseout and disposal phase."""
    return 1.8 * np.exp(-((x - 9.3) / 0.3) ** 2)

from scipy.integrate import quad

def get_total_cost(t):
    return get_requirements_cost(t) + get_acquisition_cost(t) + get_operating_cost(t) + get_phaseout_cost(t)

TOTAL_COST, _ = quad(get_total_cost, 0, 10)

def get_cumulative_cost(x):
    """Function that calculates the cumulative cost as a percentage of total."""
    val, _ = quad(get_total_cost, 0, x)
    return (val / TOTAL_COST) * 8.0  # Scale to fit the visual axes height of 8

class LifecycleCostAnalysis(Scene):
    def construct(self):
        # 1. Setup Axes
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 8, 1],
            width=10,
            height=6,
            axis_config={"include_numbers": False, "include_tip": True}
        )
        axes.center()
        axes.shift(DOWN * 0.5)

        # 2. Labels for axes
        x_label = Text("Time", font_size=24).next_to(axes.x_axis, DOWN, buff=0.2)
        y_label = Text("Costs", font_size=24).next_to(axes.y_axis, LEFT, buff=0.2).rotate(PI / 2)
        
        start_label = Text("Start", font_size=20).next_to(axes.c2p(0, 0), DOWN, buff=0.5)
        end_label = Text("End of\nlife cycle", font_size=20).next_to(axes.c2p(10, 0), DOWN, buff=0.5)

        self.play(ShowCreation(axes), Write(x_label), Write(y_label), Write(start_label), Write(end_label))

        # 3. Individual Graphs
        # We will illustrate the cost of the different lifecycle phases
        graph_req = axes.get_graph(get_requirements_cost, color=BLUE)
        graph_acq = axes.get_graph(get_acquisition_cost, color=YELLOW)
        graph_ops = axes.get_graph(get_operating_cost, color=TEAL)
        graph_disp = axes.get_graph(get_phaseout_cost, color=RED)

        # Labels for the individual phases
        label_req = Text("Requirements\nand design", font_size=20).next_to(axes.c2p(1.2, 2.0), UP, buff=0.2)
        label_acq = Text("Acquisition and\ninstallation", font_size=20).next_to(axes.c2p(2.8, 4.5), UP, buff=0.2)
        label_ops = Text("Operating and\nmaintenance", font_size=24).move_to(axes.c2p(6.5, 3.0))
        label_disp = Text("Phaseout\nand disposal", font_size=20).next_to(axes.c2p(9.3, 1.8), UP+RIGHT, buff=0.1)

        # 4. Animate Individual Phases
        self.play(ShowCreation(graph_req), Write(label_req))
        self.wait(0.5)
        self.play(ShowCreation(graph_acq), Write(label_acq))
        self.wait(0.5)
        self.play(ShowCreation(graph_ops), Write(label_ops))
        self.wait(0.5)
        self.play(ShowCreation(graph_disp), Write(label_disp))
        
        self.wait(2)

        # 5. Plot the cumulative cost curve as a percentage
        graph_cumulative = axes.get_graph(get_cumulative_cost, color=PURPLE)
        label_cumulative = Text("Cumulative % of Total Cost", font_size=28, color=PURPLE).to_corner(UR)

        line_100 = DashedLine(start=axes.c2p(0, 8), end=axes.c2p(10, 8), color=PURPLE, stroke_width=2)
        text_100 = Text("100%", font_size=20, color=PURPLE).next_to(axes.c2p(0, 8), LEFT, buff=0.2)
        text_0 = Text("0%", font_size=20, color=PURPLE).next_to(axes.c2p(0, 0), LEFT, buff=0.2)

        self.play(
            ReplacementTransform(VGroup(graph_req, graph_acq, graph_ops, graph_disp), graph_cumulative),
            FadeOut(VGroup(label_req, label_acq, label_ops, label_disp)),
            ReplacementTransform(y_label, VGroup(text_100, text_0)),
            Write(label_cumulative),
            ShowCreation(line_100),
            run_time=2
        )
        
        self.wait(3)
