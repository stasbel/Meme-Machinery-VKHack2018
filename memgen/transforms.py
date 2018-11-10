from collections import Iterable

import numpy as np
from PIL import Image
from torchvision import transforms as transforms


class Thumbnail:
    """Resize the input PIL Image to the given size.

    Keeping aspect ratio and fills empty regions with black.

    Args:
        size: Desired output size. If size is a sequence like (h, w),
            output size will be matched to this. If size is an int, bigger edge
            of the image will be matched to this number.
        interpolation: Desired interpolation (default: PIL.Image.BILINEAR)
        background_color: Desired background color (default: 0)
        enlarge: Whether do or not enlarge the image

    """

    def __init__(self, size,
                 interpolation=Image.BILINEAR,
                 background_color=0, enlarge=True):
        # noinspection PyTypeChecker
        assert isinstance(size, int) or (
                isinstance(size, Iterable) and len(size) == 2
        )
        self.size = size
        self.background = background_color
        if isinstance(size, int):
            self.size = (size, size)
        self.interpolation = interpolation
        self.enlarge = enlarge

    def __call__(self, image):
        return self._background_thumbnail(image, self.size,
                                          color=self.background)

    def __repr__(self):
        class_name = self.__class__.__name__
        size = self.size
        # noinspection PyProtectedMember
        interpolate_str = transforms._pil_interpolation_to_str[
            self.interpolation
        ]
        return f'{class_name} (size={size}, interpolation={interpolate_str})'

    def _background_thumbnail(self, image, thumbnail_size, color):
        background = self._get_background_image(self.size, color=color)

        # Image resize logic
        (th, tw), (w, h) = thumbnail_size, image.size
        if (h < th and w < tw) and self.enlarge:
            max_h = int(np.round(h * (tw / w)))
            max_w = int(np.round(w * (th / h)))
            if max_h <= th:
                new_h, new_w = max_h, tw
            else:
                new_h, new_w = th, max_w
            image = image.resize((new_w, new_h), resample=self.interpolation)
        else:
            image.thumbnail((tw, th), resample=self.interpolation)

        # Image paste into background
        w, h = image.size
        background.paste(image, ((tw - w) // 2, (th - h) // 2))

        return background

    @staticmethod
    def _get_background_image(size, color):
        height, width = size
        if color is None:
            image = np.ceil(np.random.randn(height, width, 3) * 255)
        else:
            image = np.full((height, width, 3), color)
        return Image.fromarray(np.uint8(image), 'RGB')
