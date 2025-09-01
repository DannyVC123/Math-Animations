from manim import *
import numpy as np

import sys
sys.path.append("..")
from manim_tools import ManimTools as mt

class Prove(Scene):
    def construct(self):
        self.setup()
        self.initial_tri()
        self.squares()

        self.lines()
    
    def setup(self):
        self.plane, self.unitSize = mt.grid(25)
        self.add(self.plane)

        self.sVecs = mt.scale_vecs(self.plane)
    
    def initial_tri(self):
        points = [
            mt.toScreen(self.plane, -4 -2),
            mt.toScreen(self.plane, -4, 2),
            mt.toScreen(self.plane, -2, -2)
        ]
        self.triangle = Polygon(*points, color=BLUE)
        self.triangle.set_fill(BLUE, opacity=0.5)

        self.triangle.rotate(-np.pi + np.atan(4 / 3))
        self.add(self.triangle)

        labels = mt.label_polygon(self.triangle, ["A", "C", "B"], [0.5, 0.4, 0.4])
        for lbl in labels:
            self.add(lbl)
    
    def squares(self):
        topP, rightP, leftP = self.triangle.get_vertices()[:3]

        leftVec = leftP - topP
        leftOrtho = np.array([leftVec[1], -leftVec[0], 0])
        rightVec = rightP - topP
        rightOrtho = np.array([-rightVec[1], rightVec[0], 0])
        botVec = rightP - leftP
        botOrtho = np.array([0, -botVec[0], 0])

        # Left square
        points = [leftP, leftP + leftOrtho, topP + leftOrtho, topP]
        self.leftSq = Polygon(*points, color=RED)
        self.leftSq.set_fill(RED, opacity=0.5)
        self.add(self.leftSq)
        labels = mt.label_polygon(self.leftSq, ["", "F", "G", ""], [-1, 0.4, 0.4, -1])
        for lbl in labels:
            self.add(lbl)

        # Right square
        points = [topP, topP + rightOrtho, rightP + rightOrtho, rightP]
        self.rightSq = Polygon(*points, color=RED)
        self.rightSq.set_fill(RED, opacity=0.5)
        self.add(self.rightSq)
        labels = mt.label_polygon(self.rightSq, ["", "H", "I", ""], [-1, 0.4, 0.4, -1])
        for lbl in labels:
            self.add(lbl)

        # Bottom square
        points = [rightP, rightP + botOrtho, leftP + botOrtho, leftP]
        self.botSq = Polygon(*points, color=RED)
        self.botSq.set_fill(RED, opacity=0.5)
        self.add(self.botSq)
        labels = mt.label_polygon(self.botSq, ["", "D", "E", ""], [-1, 0.4, 0.4, -1])
        for lbl in labels:
            self.add(lbl)
    
    def lines(self):
        topP, rightP, leftP = self.triangle.get_vertices()[:3]

        points = [
            topP,
            np.array([topP[0], self.botSq.get_vertices()[:4][1][1], 0])
        ]
        l = Line(*points, color=BLACK)
        self.play(Create(l), run_time=1)
        self.wait(1)