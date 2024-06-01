from manim import *
from manimdef import DefaultManimClass, SurroundingRect
import numpy as np
from tetration import compute_tetration_divergence_torch

N = 1920
DIV_ITER = 24

class PowerTowerFractal(DefaultManimClass):
    def initialize(self, x=0, y=0, eps=8):
        return x, y, eps

    def construct(self):
        x, y, eps = self.initialize()

        tetration = get_tetration_map(N, x, y, eps)
        
        fractal = ImageMobject(tetration)
        self.playw(FadeIn(fractal))
        for i in range(20):
            pxpy = get_subrange(tetration)
            if pxpy is None:
                return
            else:
                px, py = pxpy
            marked_image = get_marked_image(tetration, px, py)
            self.playw(FadeIn(marked_image))
            x, y, eps = get_new_xyeps(px, py, eps, x, y)
            
            text = self.get_range_text(x, y, eps)
            sub_tetration = get_tetration_map(N, x, y, eps*2)
            mx, my = get_manim_abs_by_pixel(px, py)
            sub_fractal = ImageMobject(sub_tetration).scale(1/DIV_ITER*2).move_to((mx, my, 0))
            self.play(FadeIn(sub_fractal), run_time=0.3)
            self.playw(sub_fractal.animate.scale(DIV_ITER/2).move_to(ORIGIN))
            self.playw(FadeIn(text))
            self.play(FadeOut(text))
            
            tetration = sub_tetration
            eps *= 2

    def get_range_text(self, x, y, eps):
        eps_x = f"{eps:.2e}".replace("e-0", r"*10^{-") + r"}"
        eps_y = f"{eps*9/16:.2e}".replace("e-0", r"*10^{-") + r"}"
        text = VGroup(MathTex("x=", f"{x:.3f} \\pm {eps_x}", color=TEAL),
                      MathTex("y=", f"{y:.3f} \\pm {eps_y}", color=TEAL))\
            .arrange(DOWN)\
                .align_to(self.camera.frame, LEFT)\
                    .align_to(self.camera.frame, UP)\
                        .shift(RIGHT*0.5).shift(DOWN*0.5)
        text[1].align_to(text[0], RIGHT)
        text[1][0].align_to(text[0], LEFT)
        rect = SurroundingRect(stroke_color=BLUE).set_fill(WHITE, opacity=1.0).surround(text)
        
        text = VGroup(rect, text)
        return text

def get_tetration_map(n, x0, y0, eps=5e-3, **kwargs):
    return compute_tetration_divergence_torch(n, x0, y0, eps, **kwargs)

def get_subrange(tetration, criterion_div=20):
    cx, cy = get_center_pixel(tetration)

    sub_pixels = N//DIV_ITER
    for i in range(cx//2):
        xy = detect(tetration, cx-i, cy, sub_pixels, criterion_div=criterion_div)
        if xy:
            break
        xy = detect(tetration, cx+i, cy, sub_pixels, criterion_div=criterion_div)
        if xy:
            break
    else:
        if criterion_div < 16: return None
        else: xy = get_subrange(tetration, criterion_div=criterion_div-1)
            
    return xy

def get_center_pixel(array):
    return array.shape[1] // 2, array.shape[0] // 2

def detect(array, x, y, pixels=N//4, criterion_div=10):
    pixels_x, pixels_y = get_16x9(pixels)
    n_pixels = pixels_x * pixels_y
    criterion = n_pixels//criterion_div
    
    sub_array = array[y-pixels_y:y+pixels_y, x-pixels_x:x+pixels_x]
    if n_pixels // 2 - criterion < sub_array.astype(bool).sum() < n_pixels // 2 + criterion:
        return x, y
    else:
        return False

def get_16x9(x):
    return x, int(x*(9/16))

def get_marked_image(tetration, px, py):
    sub_pixels = N // DIV_ITER
    pxs, pys = get_16x9(sub_pixels)
    sub_tetration = np.tile(tetration[None], (3, 1, 1))
    sub_tetration[:, py-pys-10:py+pys+10, px-pxs-10:px+pxs+10] = np.array([0, 255, 255], dtype=tetration.dtype)[:, None, None]
    sub_tetration[:, py-pys:py+pys, px-pxs:px+pxs] = tetration[py-pys:py+pys, px-pxs:px+pxs]
    
    marked_image = ImageMobject(sub_tetration.transpose(1, 2, 0))
    return marked_image

def get_new_xyeps(x, y, eps, x0=0, y0=0):
    x = (x - 960) / 960 # [-1, +1]
    y = (y - 540) / 960 # [-1, +1]
    return x0 + eps*x, y0+eps*y, eps / DIV_ITER

def get_manim_abs_by_pixel(px, py):
    mx, my, _ = get_new_xyeps(px, py, 7.1111111111111)
    return mx, my