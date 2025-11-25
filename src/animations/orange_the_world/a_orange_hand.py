from PIL import Image
import random
from color_functions import cycle, rand_faculty_color
from typing import List, Tuple, Optional

DEFAULT_X_SIZE = 28
DEFAULT_Y_SIZE = 14

class OrangeHand():

    @staticmethod
    def get_instance(xsize: int = DEFAULT_X_SIZE,
                     ysize: int = DEFAULT_Y_SIZE,
                     fps: int = 10, paths: Optional[List[str]] = None):
        new_instance = OrangeHand()
        new_instance.params(DEFAULT_X_SIZE, DEFAULT_Y_SIZE, fps)
        # images wird ggf. durch load_images befüllt
        new_instance.images = []
        new_instance.order = []
        new_instance.current_index = 0
        new_instance.next_index = 0
        blank = [[(0,0,0) for _ in range(new_instance.ysize)] for _ in range(new_instance.xsize)]
        new_instance.current_image = blank
        new_instance.next_image = blank

        try:
            if paths:
                new_instance.load_images(paths)
            else:
                new_instance.load_images([
                    "./src/animations/orange_the_world/hand_orange.png",
                    "./src/animations/orange_the_world/hand_purple.png",
                ])
        except Exception as e:
            print(e)
            print(e.__traceback__)

        return new_instance

    def params(self, xsize: int = DEFAULT_X_SIZE, ysize: int = DEFAULT_Y_SIZE, fps: int = 10):
        self.name = "Image Crossfader"
        self.xsize = DEFAULT_X_SIZE
        self.ysize = DEFAULT_Y_SIZE
        self.fps = fps
        self.update_interval = 5.0
        self.fade_steps = max(1, int(self.fps * self.update_interval))
        self.step = 0
        self.color: Tuple[int,int,int] = (255,127,0)  # fallback, unused
        self.images: List[List[List[Tuple[int,int,int]]]] = []
        self.current_index = 0
        self.next_index = 0
        # current_image and next_image are in order [x][y]
        self.current_image: List[List[Tuple[int,int,int]]] = [[(0,0,0) for _ in range(self.ysize)] for _ in range(self.xsize)]
        self.next_image: List[List[Tuple[int,int,int]]] = [[(0,0,0) for _ in range(self.ysize)] for _ in range(self.xsize)]
        self.order: List[int] = []

    def _image_to_internal(self, pil_img: Image.Image) -> List[List[Tuple[int,int,int]]]:
        pil_img = pil_img.convert("RGB")

        print(f"Imported image of size {pil_img.size}")
        resized = pil_img.resize((self.xsize, self.ysize), Image.Resampling.NEAREST)
        pixels = resized.load()
        out = [[(0,0,0) for _ in range(self.ysize)] for _ in range(self.xsize)]
        for x in range(self.xsize):
            for y in range(self.ysize):
                pixel = pixels[x, y]
                out[x][y] = pixel if isinstance(pixel, tuple) else (pixel, pixel, pixel)
        return out

    def add_image(self, path: str):
        print(f"Loading image from {path}")
        with Image.open(path) as img:
            img = img.convert("RGB")
            img_grid = self._image_to_internal(img)
            self.images.append(img_grid)
            # update order if empty
            if not self.order:
                self.order = list(range(len(self.images)))
            else:
                self.order.append(len(self.images)-1)
            # if this is the first image, set as current
            if len(self.images) == 1:
                self.current_index = 0
                self.next_index = 0
                self.current_image = self.images[0]
                self.next_image = self.images[0]

    def load_images(self, paths: List[str]):
        print(paths)
        for p in paths:
            self.add_image(p)

    def clear_images(self):
        self.images = []
        self.order = []
        blank = [[(0,0,0) for _ in range(self.ysize)] for _ in range(self.xsize)]
        self.current_image = blank
        self.next_image = blank
        self.current_index = 0
        self.next_index = 0
        self.step = 0

    # ---------- core crossfade logic ----------
    def _start_next_transition(self):
        if not self.images:
            return
        if not self.order:
            self.order = list(range(len(self.images)))
        try:
            pos = self.order.index(self.current_index)
            next_pos = (pos + 1) % len(self.order)
            self.next_index = self.order[next_pos]
        except ValueError:
            self.next_index = (self.current_index + 1) % len(self.images)
        self.next_image = self.images[self.next_index]

    def get_fade_frame(self, step: int) -> List[List[Tuple[int,int,int]]]:
        alpha = step / max(1, self.fade_steps)
        if alpha < 0.0:
            alpha = 0.0
        if alpha > 1.0:
            alpha = 1.0

        frame: List[List[Tuple[int,int,int]]] = [[(0,0,0) for _ in range(self.ysize)] for _ in range(self.xsize)]
        for x in range(self.xsize):
            for y in range(self.ysize):
                r0, g0, b0 = self.current_image[x][y]
                r1, g1, b1 = self.next_image[x][y]
                r = int(r0 * (1 - alpha) + r1 * alpha)
                g = int(g0 * (1 - alpha) + g1 * alpha)
                b = int(b0 * (1 - alpha) + b1 * alpha)
                frame[x][y] = (r, g, b)
        return frame

    def commit_transition(self):
        self.current_index = self.next_index
        self.current_image = self.next_image
        # prepare following next
        self._start_next_transition()

    def get_frame(self) -> List[List[Tuple[int,int,int]]]:
        if not self.images:
            return [[(0,0,0) for _ in range(self.ysize)] for _ in range(self.xsize)]

        if self.current_image is None or self.next_image is None:
            self.current_index = 0
            self.next_index = (1 % len(self.images)) if len(self.images) > 1 else 0
            self.current_image = self.images[self.current_index]
            self.next_image = self.images[self.next_index]

        if len(self.images) == 1:
            return self.current_image

        if self.step == 0:
            self._start_next_transition()

        self.step += 1
        frame = self.get_fade_frame(self.step)

        if self.step >= self.fade_steps:
            # finalize exact next image
            self.commit_transition()
            self.step = 0

        return frame
