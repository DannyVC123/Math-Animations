from manim import *
from manim import AnimationGroup

import numpy as np

from manim_tools import ManimTools as mt

LABELS = True

class Pythagoreon(Scene):
    def construct(self):
        self.setup()

        self.draw_triangle()
        self.draw_squares()

        self.vertical_line()
        self.diagonal_lines()

        self.congruence()
        self.sas()
    
    def setup(self):
        self.plane, self.unitSize = mt.grid(25)
        # self.add(self.plane)

        self.sVecs = mt.scale_vecs(self.plane)
    
    def draw_triangle(self):
        t = mt.text(
            r"Let $\triangle ACB$ be a right-angled triangle \\ with right angle $\angle CAB$.",
            mt.toScreen(self.plane, 5, 0)
        )
        self.play(FadeIn(t))
        self.wait(5)
       
        points = [
            mt.toScreen(self.plane, -5, -2),
            mt.toScreen(self.plane, -8, -2),
            mt.toScreen(self.plane, -5, 2)
        ]
        self.triangle = Polygon(*points, color=RED)
        self.play(Create(self.triangle), run_time=1)
        self.triangle.set_fill(RED, opacity=0.5)
        
        rAngle = RightAngle(
            Line(points[0], points[1]),
            Line(points[0], points[2]),
            length=0.2,
            color=RED
        )
        self.play(Create(rAngle))

        group = Group(self.triangle, rAngle)

        if LABELS:
            labels = mt.label_polygon(self.triangle, ["A", "C", "B"], [0.5, 0.4, 0.4])
            for lbl in labels:
                self.add(lbl)
                self.play(FadeIn(lbl))
            self.wait(1)

        self.play(Rotate(group, np.pi - np.atan(4 / 3)))
        # self.play(self.triangle.animate.shift(DOWN * self.unitSize))
        
        self.wait(3)
        self.play(FadeOut(t))

        self.topP, self.rightP, self.leftP = self.triangle.get_vertices()[:3]
    
    def draw_squares(self):
        t = mt.text(
            r"On each of the sides $BC$, $AB$, and $CA$, \\ draw a square.",
            mt.toScreen(self.plane, 5, 0)
        )
        self.play(FadeIn(t))
        self.wait(5)

        rightVec = self.rightP - self.topP
        rightOrtho = np.array([-rightVec[1], rightVec[0], 0])
        leftV = self.leftP - self.topP
        leftOrtho = np.array([leftV[1], -leftV[0], 0])
        botVec = self.rightP - self.leftP
        botOrtho = np.array([0, -botVec[0], 0])

        self.squares = []
        def draw_square(points, labels):
            square = Polygon(*points, color=PINK)
            self.play(Create(square), run_time=0.5)
            square.set_fill(PINK, opacity=0.5)
            
            if LABELS:
                l = mt.label_polygon(square, labels, [-1, 0.4, 0.4, -1])
                for lbl in l:
                    self.add(lbl)
                    self.play(FadeIn(lbl), run_time=0.5)
            
            self.squares.append(square)
            self.wait(0.5)

        # left
        points = [
            self.rightP,
            self.rightP + rightOrtho,
            self.topP + rightOrtho,
            self.topP
        ]
        draw_square(points, ["", "I", "H", ""])

        # right
        points = [
            self.topP,
            self.topP + leftOrtho,
            self.leftP + leftOrtho,
            self.leftP
        ]
        draw_square(points, ["", "G", "F", ""])

        # bottom
        points = [
            self.leftP,
            self.leftP + botOrtho,
            self.rightP + botOrtho,
            self.rightP
        ]
        draw_square(points, ["", "D", "E", ""])

        self.wait(3)
        self.play(FadeOut(t))

        t1 = mt.text(
            r"$\angle CAB = \angle BAG = 90^{\circ}$",
            mt.toScreen(self.plane, 5, 0)
        )
        self.play(FadeIn(t1))
        self.wait(5)

        t2 = mt.text(
            r"$\angle CAB + \angle BAG = 180^{\circ}$, \\ therefore, $CG$ is a straight line.",
            mt.toScreen(self.plane, 5, -1.5)
        )
        self.play(FadeIn(t2))
        self.wait(8)

        self.play(FadeOut(Group(t1, t2)))
    
    def vertical_line(self):
        t1 = mt.text(
            r"From $A$, draw a line parallel to $BD$ and $CE$.",
            mt.toScreen(self.plane, 5, 0)
        )
        self.play(FadeIn(t1))
        self.wait(5)

        botSqTopLeft, _, botSqBotRight, _ = self.squares[2].get_vertices()[:4]

        points = [
            self.topP,
            np.array([self.topP[0], botSqBotRight[1], 0])
        ]
        l = Line(*points, color=BLUE)
        self.play(Create(l), run_time=1)
        self.wait(1)

        t2 = mt.text(
            r"It will perpendicularly intersect $BC$ and $DE$ \\ at $K$ and $L$, respectively.",
            mt.toScreen(self.plane, 5, -1.5)
        )
        self.play(FadeIn(t2))
        self.wait(5)

        intersection = mt.segment_intersection(self.topP, [self.topP[0], botSqBotRight[1], 0], self.leftP, self.rightP)

        if LABELS:
            lbl = mt.label_point(intersection, "K", self.sVecs['UP_LEFT'], 0.3)
            self.play(FadeIn(lbl), run_time=1)
            
            lbl = mt.label_point(
                np.array([intersection[0], botSqBotRight[1], 0]),
                "L", self.sVecs['UP_LEFT'], 0.3
            )
            self.play(FadeIn(lbl), run_time=1)

        rAngle = RightAngle(
            Line(intersection, self.topP),
            Line(intersection, self.rightP),
            length=0.2,
            color=BLUE
        )
        self.play(Create(rAngle))

        botIntersection = np.array([intersection[0], botSqBotRight[1], 0])
        rAngle = RightAngle(
            Line(botIntersection, self.topP),
            Line(botIntersection, botSqBotRight),
            length=0.2,
            color=BLUE
        )
        self.play(Create(rAngle))

        self.wait(3)
        self.play(FadeOut(Group(t1, t2)))
    
    def diagonal_lines(self):
        t1 = mt.text(
            r"Draw lines segments $CF$ and $AD$.",
            mt.toScreen(self.plane, 5, 0)
        )
        self.play(FadeIn(t1))
        self.wait(5)

        leftSqBotRight, _, leftSqTopLeft, _ = self.squares[1].get_vertices()[:4]
        points = [self.rightP, leftSqTopLeft]
        l = Line(*points, color=BLUE)
        self.play(Create(l), run_time=1)
        self.wait(2)

        _, botSqBotLeft, _, botSqTopRight = self.squares[2].get_vertices()[:4]
        points = [self.topP, botSqBotLeft]
        l = Line(*points, color=BLUE)
        self.play(Create(l), run_time=1)
        self.wait(2)

        t2 = mt.text(
            r"This creates the triangles $\triangle BCF$ and $\triangle BDA$.",
            mt.toScreen(self.plane, 5, -1.5)
        )
        self.play(FadeIn(t2))
        self.wait(5)

        points = [self.leftP, leftSqTopLeft, self.rightP]
        self.triangle = Polygon(*points, color=BLUE)
        self.play(Create(self.triangle), run_time=1)
        self.triangle.set_fill(BLUE, opacity=0.5)
        self.wait(2)

        points = [self.leftP, self.topP, botSqBotLeft]
        self.triangle = Polygon(*points, color=BLUE)
        self.play(Create(self.triangle), run_time=1)
        self.triangle.set_fill(BLUE, opacity=0.5)
        
        self.wait(3)
        self.play(FadeOut(Group(t1, t2)))
    
    def congruence(self):
        t1 = mt.text(
            r"$AB = FB$ since they are sides of the same square.",
            mt.toScreen(self.plane, 5, 0)
        )
        self.play(FadeIn(t1))
        self.wait(5)

        leftSqBotRight, leftSqTopRight, leftSqTopLeft, leftSqBotLeft = self.squares[1].get_vertices()[:4]
        cm = mt.congruent_mark(leftSqBotRight, leftSqBotLeft, self.unitSize, BLUE, 0.5)[0]
        self.play(Create(cm), run_time=0.5)
        
        cm = mt.congruent_mark(leftSqBotLeft, leftSqTopLeft, self.unitSize, BLUE, 0.5)[0]
        self.play(Create(cm), run_time=0.5)

        t2 = mt.text(
            r"Likewise, $BD = BC$.",
            mt.toScreen(self.plane, 5, -1.5)
        )
        self.play(FadeIn(t2))
        self.wait(3)

        botSqTopLeft, botSqBotLeft, botSqBotRight, botSqTopRight = self.squares[2].get_vertices()[:4]
        cm = mt.congruent_mark(botSqTopLeft, botSqBotLeft, self.unitSize, BLUE, 0.5, count=2)
        self.play(AnimationGroup(*[Create(mark) for mark in cm]), run_time=0.5)
        
        cm = mt.congruent_mark(botSqTopRight, botSqTopLeft, self.unitSize, BLUE, 0.5, count=2)
        self.play(AnimationGroup(*[Create(mark) for mark in cm]), run_time=0.5)

        self.play(FadeOut(Group(t1, t2)))

        t1 = mt.text(
            r"$\angle ABD = \angle ABC + \angle CBD$",
            mt.toScreen(self.plane, 5, 0)
        )
        self.play(FadeIn(t1))
        self.wait(5)

        t2 = mt.text(
            r"$\angle FBC = \angle ABC + \angle FBA$",
            mt.toScreen(self.plane, 5, -1.5)
        )
        self.play(FadeIn(t2))
        self.wait(5)

        t3 = mt.text(
            r"$\angle CBD = \angle FBA = 90^{\circ}$ \\ $\Rightarrow \angle ABD = \angle ABC + 90^{\circ} = \angle FBD$.",
            mt.toScreen(self.plane, 5, -3)
        )
        self.play(FadeIn(t3))
        self.wait(5)

        angle1 = Angle(
            Line(self.leftP, botSqBotLeft),
            Line(self.leftP, self.topP),
            radius=0.3,
            color=BLUE
        )
        angle2 = Angle(
            Line(self.leftP, self.rightP),
            Line(self.leftP, leftSqTopLeft),
            radius=0.5,
            color=BLUE
        )

        self.play(AnimationGroup(*[Create(mark) for mark in Group(angle1, angle2)]), run_time=0.5)

        self.wait(3)
        self.play(FadeOut(Group(t1, t2, t3)))
        
    def sas(self):
        group = Group()
        def list_statements(text):
            for i, tex in enumerate(text):
                t = mt.text(
                    tex,
                    mt.toScreen(self.plane, 5, -i)
                )
                group.add(t)
                self.play(FadeIn(t), run_time=0.5)
                self.wait(0.5)

        list_statements([r"$AB = FB$", r"$BD = BC$", r"$\angle ABD = \angle FBC$"])
        self.wait(3)

        t = mt.text(
            r"$\Rightarrow \triangle ABD \cong \triangle FBC$ \\ by Side-Angle-Side (SAS) postulate.",
            mt.toScreen(self.plane, 5, -3.5)
        )
        group.add(t)
        self.play(FadeIn(t))
        self.wait(5)

        self.play(FadeOut(group))
