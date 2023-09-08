import math

from manimlib import *
# from improved_vector_field import *


class ContinuousLyapunov(ThreeDScene):
    scaling_factor = 3

    # 1. Title scene
    # 2. Equation
    # 3. Equilibrium
    # 4. Dynamics
    # 5. Show stable equilibrium
    # 6. Transition to 3D
    # 7. Lyapunov in 3D
    # 8. StreamLines on Lyapunov surface
    # 9. Derive negative gradient

    def construct(self):
        self.play_intro()

        self.add_ode()
        self.add_equilibrium()
        self.add_vector_field()
        # self.show_stable()
        # self.transition_to_3d()
        # self.add_lyapunov()
        # self.project_onto_lyapunov()

    def play_intro(self):
        title1 = Text('Continuous-time', font_size=60, color=BLUE).shift(2 * UP)
        title2 = Text('Lyapunov function', font_size=60, color=BLUE).shift(UP)
        title = Group(title1, title2)
        self.add(title)

        self.wait(2)

        ode = MathTex(r'{{ \dot{x} }} = {{ f(x) }}', font_size=72).shift(DOWN)
        self.play(FadeIn(ode))

        self.wait(3)
        self.play(FadeOut(title, ode))

        self.remove(title, ode)

    def add_ode(self):
        self.system = Text('System', font_size=24).shift(3 * UP + 3 * LEFT)
        self.ode = MathTex(r'{{ \dot{x} }} &= {{-x + y^2}} \\ {{ \dot{y} }} &= {{-2y + 3x^2}}').next_to(self.system, DOWN)
        self.camera.add_fixed_in_frame_mobjects(self.system, self.ode)

        self.play(FadeIn(self.system, self.ode))
        self.wait(2)

    def add_equilibrium(self):
        equilibrium_text = Text('Equilibrium', font_size=24, color=YELLOW).shift(1 * DOWN + 3 * LEFT)
        equilibrium_equation1 = MathTex(r'{{ \dot{x} }} &= {{-x + y^2}} \\ {{ \dot{y} }} &= {{ -2y + 3x^2 }}', color=YELLOW).next_to(equilibrium_text, DOWN)
        equilibrium_equation2 = MathTex(r'{{ 0 }} &= {{-x + y^2}} \\ {{ 0 }} &= {{-2y + 3x^2}}', color=YELLOW).next_to(equilibrium_text, DOWN)

        self.play(
            TransformFromCopy(self.system, equilibrium_text),
            TransformFromCopy(self.ode, equilibrium_equation1),
            Transform(equilibrium_equation1, equilibrium_equation2),
            run_time=3)
        self.wait(5)

        equilibrium_point1 = MathTex(r'{{ (x_0, y_0) }} = {{ (0, 0) }}', color=YELLOW).next_to(equilibrium_text, DOWN)
        equilibrium_point2 = MathTex(r'{{ (x_0, y_0) }} = {{ ((2 / 3)^{2 / 3}, (2 / 3)^{1 / 3}) }}', color=YELLOW).next_to(equilibrium_point1, DOWN)

        self.play(
            ReplacementTransform(equilibrium_equation1[:3], equilibrium_point1),
            ReplacementTransform(equilibrium_equation1[4:], equilibrium_point2),
            run_time=3)
        self.wait(5)

        self.ax = ThreeDAxes(
            x_range=[-1, 1, 0.5],
            y_range=[-1, 1, 0.5],
            z_range=[0, 1, 0.5],
            x_length=2,
            y_length=2,
            z_length=2,
            tips=False,
            axis_config=dict(tip_width=0.05, tip_height=0.05, include_numbers=True, font_size=12, line_to_number_buff=0.15),
            z_axis_config=dict(stroke_opacity=0.0)
        ).scale(self.scaling_factor).shift(3 * RIGHT)
        self.ax.z_index = 1

        self.play(FadeIn(self.ax), runtime=2)

        equilibrium1 = [0, 0, 0]
        equilibrium2 = [(2 / 3) ** (2 / 3), (2 / 3) ** (1 / 3), 0]

        self.dot1 = Dot(equilibrium1, color=YELLOW).move_to(self.ax.c2p(*equilibrium1))
        self.dot2 = Dot(equilibrium2, color=YELLOW).move_to(self.ax.c2p(*equilibrium2))
        self.dot1.z_index = 2
        self.dot2.z_index = 2

        self.play(
            ReplacementTransform(equilibrium_point1, self.dot1),
            ReplacementTransform(equilibrium_point2, self.dot2),
            FadeOut(equilibrium_text),
            run_time=4
        )
        self.wait(4)

        ax_no_label = ThreeDAxes(
            x_range=[-1, 1, 0.5],
            y_range=[-1, 1, 0.5],
            z_range=[0, 1, 0.5],
            x_length=2,
            y_length=2,
            z_length=2,
            tips=False,
            axis_config=dict(tip_width=0.05, tip_height=0.05),
            z_axis_config=dict(stroke_opacity=0.0)
        ).scale(self.scaling_factor)

        self.play(ReplacementTransform(self.ax, ax_no_label),
                  self.dot1.animate.move_to(ax_no_label.c2p(*equilibrium1)),
                  self.dot2.animate.move_to(ax_no_label.c2p(*equilibrium2)),
                  FadeOut(self.system),
                  FadeOut(self.ode),
                  run_time=4)
        self.wait(4)

    def add_vector_field(self):
        self.vector_field = StreamLines(
            lambda p: self.ax.c2p(*f(self.ax.p2c(p * self.scaling_factor))) / self.scaling_factor - self.ax.get_origin(),
            x_range=[-1, 1, 0.1],
            y_range=[-1, 1, 0.1],
            padding=0.1,
            stroke_width=1.0,
            color=BLUE_D
        )

        self.add(self.vector_field)
        self.vector_field.start_animation(warm_up=True, flow_speed=0.5, time_width=0.2)
        self.wait(2 * self.vector_field.virtual_time / self.vector_field.flow_speed)

        self.vector_field.end_animation()
        self.wait(2)

    def show_stable(self):
        stable_text = Text('Stable', font_size=24, color=GREEN).next_to(self.dot1, LEFT + DOWN, aligned_edge=RIGHT)
        unstable_text = Text('Unstable', font_size=24, color=RED).next_to(self.dot2, LEFT, aligned_edge=RIGHT)

        self.play(self.dot1.animate.set_color(GREEN),
                  self.dot2.animate.set_color(RED),
                  FadeIn(stable_text),
                  FadeIn(unstable_text))
        self.wait(4)

        self.play(self.dot1.animate.set_color(GREEN),
                  self.dot2.animate.set_color(RED),
                  FadeOut(stable_text),
                  FadeOut(unstable_text),
                  Uncreate(self.dot2))
        self.wait(2)

    def transition_to_3d(self):
        self.move_camera(phi=PI / 3, frame_center=self.ax, zoom=0.8)
        self.wait(4)

        self.begin_ambient_camera_rotation()

    def add_lyapunov(self):
        self.lyapunov_plane = Surface(
            lambda u, v: self.ax.c2p(u, v, lyapunov(u, v)),
            resolution=(10, 20),
            v_range=[-1, 1],
            u_range=[-1, 1],
            fill_color=RED_E,
            fill_opacity=0.5,
            checkerboard_colors=[RED_D, RED_E]
        )

        self.lyapunov_text = MathTex(r'V(x, y) = \frac{x^2}{2} + \frac{y^2}{4}').shift(3 * UP)

        self.camera.add_fixed_in_frame_mobjects(self.lyapunov_text)
        self.play(
            FadeIn(self.lyapunov_plane),
            FadeIn(self.lyapunov_text),
            run_time=3)
        self.wait(20)

    def project_onto_lyapunov(self):
        proj_vector_field = ProjectedStreamLines(
            f,
            proj_lyap,
            x_range=[-1, 1, 0.1],
            y_range=[-1, 1, 0.1],
            padding=0.1,
            stroke_width=1.0,
            color=BLUE_D
        ).scale(self.scaling_factor).shift(self.ax.c2p(*ORIGIN))

        self.play(
            Transform(self.vector_field, proj_vector_field),
            run_time=3
        )
        self.wait(4)

        lyapunov_deriv_text = MathTex(r'\dot{V}(x, y) = -x^2 + xy^2 - y^2 + (3 / 2) yx^2').shift(3 * UP)
        # self.camera.add_fixed_in_frame_mobjects(lyapunov_deriv_text)

        self.play(
            Transform(self.lyapunov_text, lyapunov_deriv_text),
            run_time=3
        )
        self.wait(4)


def f(p):
    x, y = p[0], p[1]

    # https://www.ndsu.edu/pubweb/~novozhil/Teaching/480%20Data/13.pdf
    return (-x + y ** 2) * RIGHT + (-2 * y + 3 * x ** 2) * UP


def proj_lyap(p):
    x, y = p[0], p[1]

    return x * RIGHT + y * UP + lyapunov(x, y) * OUT


def region_of_attraction():
    a_squared = 2 / 9
    b_squared = 4 / 9

    a = math.sqrt(a_squared)
    b = math.sqrt(b_squared)

    width = 2 * a
    height = 2 * b

    return width, height


def lyapunov(x, y):
    return x ** 2 / 2 + y ** 2 / 4


def lyapunov_derivative(x, y):
    return -x ** 2 + x * y ** 2 - y ** 2 + (3 / 2) * y * x ** 2
