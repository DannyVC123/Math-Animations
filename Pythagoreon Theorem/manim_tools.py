from manim import *
import numpy as np

class ManimTools():
    @staticmethod
    def scale_vecs(plane):
        x_unit = plane.x_axis.unit_size
        y_unit = plane.y_axis.unit_size
        
        scaled_vectors = {
            "UP": UP * y_unit,
            "DOWN": DOWN * y_unit,
            "LEFT": LEFT * x_unit,
            "RIGHT": RIGHT * x_unit,
            "UP_RIGHT": (UP * y_unit + RIGHT * x_unit),
            "UP_LEFT": (UP * y_unit + LEFT * x_unit),
            "DOWN_RIGHT": (DOWN * y_unit + RIGHT * x_unit),
            "DOWN_LEFT": (DOWN * y_unit + LEFT * x_unit),
            "ORIGIN": ORIGIN
        }
        
        return scaled_vectors

    @staticmethod
    def grid(x_units):
        frame_width = config.frame_width
        frame_height = config.frame_height

        unit_size = frame_width / x_units
        y_units = int(frame_height / unit_size)

        plane = NumberPlane(
            x_range=[-x_units/2, x_units/2, 1],
            y_range=[-y_units/2, y_units/2, 1],
            x_length=frame_width,
            y_length=unit_size * y_units,
            axis_config={"include_numbers": True}
        )
        
        return plane, unit_size

    @staticmethod
    def toScreen(plane, x, y):
        x_screen = x * plane.x_axis.unit_size
        y_screen = y * plane.y_axis.unit_size

        return np.array([x_screen, y_screen, 0])

    @staticmethod
    def text(string, pos, font_size=35):
        text = Tex(string, font_size=font_size).move_to(pos)
        return text
    
    @staticmethod
    def label_polygon(polygon, labels, offsets):
        labeled_objs = []

        for i, lbl in enumerate(labels):
            if not lbl:
                continue
            label_mobj = always_redraw(
                lambda i=i, lbl=lbl: MathTex(lbl, font_size=30).move_to(
                    polygon.get_vertices()[i] + ManimTools._label_offset(polygon, i, offsets[i])
                )
            )
            labeled_objs.append(label_mobj)

        return labeled_objs

    @staticmethod
    def _label_offset(polygon, idx, offset):
        v = polygon.get_vertices()[idx]
        center = polygon.get_center()
        direction = v - center
        return direction / np.linalg.norm(direction) * offset

    @staticmethod
    def label_point(point, label, direction, offset):
        l = MathTex(label, font_size=30)
        return l.move_to(
            point + direction / np.linalg.norm(direction) * offset
        )
    
    @staticmethod
    def segment_intersection(p1, p2, p3, p4):
        # https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection#Given_two_points_on_each_line

        x1, y1, _ = p1
        x2, y2, _ = p2
        x3, y3, _ = p3
        x4, y4, _ = p4

        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if denom == 0:
            return None

        px = ((x1*y2 - y1*x2)*(x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)) / denom
        py = ((x1*y2 - y1*x2)*(y3 - y4) - (y1 - y2)*(x3*y4 - y3*x4)) / denom

        if (min(x1, x2) <= px <= max(x1, x2) and
            min(y1, y2) <= py <= max(y1, y2) and
            min(x3, x4) <= px <= max(x3, x4) and
            min(y3, y4) <= py <= max(y3, y4)):
            return np.array([px, py, 0])
        else:
            return None
    
    @staticmethod
    def congruent_mark(p1, p2, unit_size, color, mark_length, count=1, spacing=0.2):
        x1, y1, _ = p1
        x2, y2, _ = p2
        mid = np.array([(x1 + x2) / 2, (y1 + y2) / 2, 0])

        vec = p2 - p1
        vec_unit = (vec / np.linalg.norm(vec)) * unit_size

        perp_unit = np.array([-vec_unit[1], vec_unit[0], 0])

        marks = []
        for i in range(count):
            offset = (i - (count - 1) / 2) * spacing  # center them
            mark_start = mid - perp_unit * mark_length / 2 + vec_unit * offset
            mark_end = mid + perp_unit * mark_length / 2 + vec_unit * offset
            mark = Line(mark_start, mark_end, color=color)
            marks.append(mark)

        return Group(*marks)

