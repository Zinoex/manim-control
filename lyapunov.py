import math

from manim import *
from improved_vector_field import *


class ContinuousLyapunov(ThreeDScene):
    scaling_factor = 3

    # 1. Title scene
    # 2. Equation
    # 3. Equilibrium
    # 4. Dynamics
    # 5. Transition to 3D
    # 6. Lyapunov in 3D
    # 7. StreamLines on Lyapunov surface
    # 8. Derive negative gradient
    # 9. Region of attraction

    def construct(self):
        self.play_intro()

        self.add_ode()
        self.add_equilibrium()
        self.add_vector_field()

        # self.move_camera(phi=PI / 3)
        # self.move_camera(frame_center=[0, 0, 2.0])
        #
        # # TODO: Add Lyapunov (in 3D)
        #
        # w, h = self.region_of_attraction()
        # roa = Ellipse(width=w, height=h, color=RED)
        # roa.scale(self.scaling_factor)
        # self.play(Create(roa))
        # self.wait()

    def play_intro(self):
        title1 = Text('Continuous-time', font_size=60, color=BLUE).shift(2 * UP)
        title2 = Text('Lyapunov function', font_size=60, color=BLUE).shift(UP)
        title = Group(title1, title2)
        self.add(title)

        self.wait(2)

        ode = MathTex(r'\dot{x} = f(x)', font_size=72).shift(DOWN)
        self.play(FadeIn(ode))

        self.wait(3)
        self.play(FadeOut(title, ode))

        self.remove(title, ode)

    def add_ode(self):
        system = Text('System', font_size=24).shift(3 * UP + 3 * LEFT)
        self.ode = MathTex(r'\dot{x} &= -x + y^2 \\ \dot{y} &= -2y + 3x^2').next_to(system, DOWN)

        self.play(FadeIn(system, self.ode))
        self.wait(2)

    def add_equilibrium(self):
        equilibrium_text = Text('Equilibrium', font_size=24, color=YELLOW).shift(1 * DOWN + 3 * LEFT)
        equilibrium_equation1 = MathTex(r'\dot{x} &= -x + y^2 \\ \dot{y} &= -2y + 3x^2', color=YELLOW).next_to(equilibrium_text, DOWN)
        equilibrium_equation2 = MathTex(r'0 &= -x + y^2 \\ 0 &= -2y + 3x^2', color=YELLOW).next_to(equilibrium_text, DOWN)
        equilibrium = Group(equilibrium_text, equilibrium_equation1)

        self.play(
            TransformFromCopy(self.ode, equilibrium),
            Transform(equilibrium_equation1, equilibrium_equation2),
            runtime=4)
        self.wait(3)

        equilibrium_point1 = MathTex(r'(x_0, y_0) = (0, 0)', color=YELLOW).next_to(equilibrium_text, DOWN)
        equilibrium_point2 = MathTex(r'(x_0, y_0) = ((2 / 3)^{2 / 3}, (2 / 3)^{1 / 3})', color=YELLOW).next_to(equilibrium_point1, DOWN)

        self.play(
            TransformFromCopy(equilibrium_equation1, equilibrium_point1),
            ReplacementTransform(equilibrium_equation1, equilibrium_point2),
            runtime=4)
        self.wait(3)

        self.ax = Axes(
            x_range=[-1, 1, 0.5],
            y_range=[-1, 1, 0.5],
            x_length=2,
            y_length=2,
            tips=False,
            axis_config=dict(tip_width=0.05, tip_height=0.05, include_numbers=True, font_size=12, line_to_number_buff=0.15)
        ).scale(self.scaling_factor).shift(3 * RIGHT)

        self.play(FadeIn(self.ax), runtime=2)

        equilibrium1 = [0, 0, 0]
        equilibrium2 = [(2 / 3) ** (2 / 3), (2 / 3) ** (1 / 3), 0]

        self.dot1 = Dot(equilibrium1, color=YELLOW).move_to(self.ax.c2p(*equilibrium1))
        self.dot2 = Dot(equilibrium2, color=YELLOW).move_to(self.ax.c2p(*equilibrium2))
        self.dot1.z_index = 1
        self.dot2.z_index = 1

        self.play(
            ReplacementTransform(equilibrium_point1, self.dot1),
            ReplacementTransform(equilibrium_point2, self.dot2),
            FadeOut(equilibrium_text),
            runtime=3
        )
        self.wait(2)

        ax_no_label = Axes(
            x_range=[-1, 1, 0.5],
            y_range=[-1, 1, 0.5],
            x_length=2,
            y_length=2,
            tips=False,
            axis_config=dict(tip_width=0.05, tip_height=0.05)
        ).scale(self.scaling_factor).shift(3 * RIGHT)

        self.play(Transform(self.ax, ax_no_label),
                  self.dot1.animate.move_to(ax_no_label.c2p(*equilibrium1)),
                  self.dot2.animate.move_to(ax_no_label.c2p(*equilibrium2)),
                  runtime=2)
        self.wait(2)

    def add_vector_field(self):
        def color_scheme(p, v):
            c = self.ax.p2c(p)
            v = self.vector_field(c)
            return np.linalg.norm(v)

        vector_field = BetterStreamLines(
            self.vector_field,
            x_range=[-1, 1, 0.1],
            y_range=[-1, 1, 0.1],
            padding=0.1,
            stroke_width=2,
            colors=[GOLD_D, BLUE_D],
            color_scheme=color_scheme
        ).scale(self.scaling_factor).shift(self.ax.c2p(*ORIGIN))

        self.add(vector_field)
        vector_field.start_animation(warm_up=True, flow_speed=0.5)
        self.wait(2 * vector_field.virtual_time / vector_field.flow_speed)

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
