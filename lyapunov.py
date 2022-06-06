import math

from manim import *


class ContinuousLyapunov(Scene):
    scaling_factor = 3.5

    def construct(self):
        self.add_axes()
        self.add_equilibrium()

        vector_field = StreamLines(
            self.vector_field,
            x_range=[-1, 1, 0.1],
            y_range=[-1, 1, 0.1],
            padding=0.1,
            stroke_width=2,
            colors=[GOLD_D, BLUE_D]
        ).scale(self.scaling_factor)
        # self.play(vector_field.create())
        # self.wait()
        self.add(vector_field)
        vector_field.start_animation(warm_up=True, flow_speed=0.5)
        self.wait(vector_field.virtual_time / vector_field.flow_speed)

        # TODO: Add Lyapunov (in 3D)

        w, h = self.region_of_attraction()
        roa = Ellipse(width=w, height=h, color=RED_B)
        roa.scale(self.scaling_factor)
        self.play(Create(roa))
        self.wait()

    def add_axes(self):
        ax = Axes(
            x_range=[-1, 1, 0.5],
            y_range=[-1, 1, 0.5],
            x_length=2,
            y_length=2,
            tips=False,
            axis_config=dict(tip_width=0.05, tip_height=0.05, include_numbers=True, font_size=18, line_to_number_buff=0.15),
        ).scale(self.scaling_factor)
        self.add(ax)

    def add_equilibrium(self):
        equilibrium1 = np.array([0, 0, 0]) * self.scaling_factor
        equilibrium2 = np.array([(2 / 3) ** (2 / 3), (2 / 3) ** (1 / 3), 0]) * self.scaling_factor

        dot1 = Dot(equilibrium1, color=YELLOW)
        dot2 = Dot(equilibrium2, color=YELLOW)

        self.add(dot1, dot2)

    def vector_field(self, x):
        x, y = x[0], x[1]

        # https://www.ndsu.edu/pubweb/~novozhil/Teaching/480%20Data/13.pdf
        return (-x + y ** 2) * RIGHT + (-2 * y + 3 * x ** 2) * UP

    def region_of_attraction(self):
        a_squared = 2 / 9
        b_squared = 4 / 9

        a = math.sqrt(a_squared)
        b = math.sqrt(b_squared)

        width = 2 * a
        height = 2 * b

        return width, height

    def lyapunov(self, x):
        return x[0] ** 2 / 2 + x[1] ** 2 / 4

    def lyapunov_derivative(self, x):
        return -x[0] ** 2 + x[0] * x[1] ** 2 - x[1] ** 2 + (3 / 2) * x[1] * x[0] ** 2
