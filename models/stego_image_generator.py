from PIL import Image


class StegoImageGenerator:
    def __init__(self, binary_data_to_hide: bytes, image_file_path: str):
        # image class variable
        self.img = Image.open(image_file_path)
        self.image_width, self.image_height = self.img.size

        # store binary data and length of it
        self.binary_data_to_hide = binary_data_to_hide
        self.data_length = len(self.binary_data_to_hide)

        # validate that we can hide binary data in the image
        self._validate()

        # current index to save
        self.data_index = 0

    def _validate(self):
        # image pixels
        image_pixels = self.image_width * self.image_height

        # (image_pixels * len(self.img.getbands())) is size of image * number of channels (RGB, RGBA, ...),
        # / 8 because each pixel channel is one byte, and we want to store each byte of data in 8 channels of image
        if self.data_length > (image_pixels * len(self.img.getbands())) / 8:
            raise ValueError("File too large to encode in the given image")

    # hide data in range of image pixels and return True if data Not end or False if end
    def _hide_data(self, from_x_pixel: int, to_x_pixel: int, from_y_pixel: int, to_y_pixel: int):
        bit_index = 7

        for x in range(from_x_pixel, to_x_pixel):
            for y in range(from_y_pixel, to_y_pixel):
                # get pixel in x, y location
                pixel = list(self.img.getpixel((x, y)))

                # Iterate on channels of pixel (RGB, RGBA, ...)
                for color_channel in range(len(self.img.getbands())):
                    if self.data_index < self.data_length:
                        # pixel[color_channel] & ~1 is to clear the least significant bit (value & 1111 1110)
                        # then make or operation with current data index shifted right by current bit index
                        # and the & 1 is to ignore value of byte expect the least significant bit (value & 0000 0001)
                        pixel[color_channel] = pixel[color_channel] & ~1 | (
                                (self.binary_data_to_hide[self.data_index] >> bit_index) & 1)

                        # if it's not zero then decrement to get next upper significant bit
                        if bit_index != 0:
                            bit_index -= 1
                        # else then we end the byte so go next byte by increment data_index and reset bit_index
                        else:
                            self.data_index += 1
                            bit_index = 7
                    else:
                        # false is to determine that reach end of file
                        return False

                # save pixel after end modify
                self.img.putpixel((x, y), tuple(pixel))

        # true is to continue writing pixels
        return True

    def generate_stego_image(self):
        # distribute binary file in quarters of image
        half_image_width = self.image_width // 2
        half_image_height = self.image_height // 2

        # hide data in second quarter
        if self._hide_data(half_image_width, self.image_width, 0, half_image_height):
            # hide data in first quarter
            if self._hide_data(0, half_image_width, 0, half_image_height):
                # hide data in forth quarter
                if self._hide_data(half_image_width, self.image_width, half_image_height, self.image_height):
                    # hide data in third quarter
                    self._hide_data(0, half_image_width, half_image_height, self.image_height)

        return self.img
