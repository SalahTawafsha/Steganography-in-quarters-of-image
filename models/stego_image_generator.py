import os

from PIL import Image


class StegoImageGenerator:
    def __init__(self, original_file_path: str, image_file_path: str):
        self.original_file_path = original_file_path
        self.image_file_path = image_file_path
        # extract files and validate that we can hide the message in the image
        self.__extract_and_validate()
        self.data_index = 0

    def __extract_and_validate(self):
        self.img = Image.open(self.image_file_path)
        self.image_width, self.image_height = self.img.size
        image_size = self.image_width * self.image_height

        with open(self.original_file_path, 'rb') as file:
            self.binary_file_data = file.read()

        file_name, file_extension = os.path.splitext(self.original_file_path)

        # Convert the file_extension to bytes and complete it to 10 byte
        file_extension_bytes = file_extension.encode('utf-8')[:10]
        padding_size = 10 - len(file_extension_bytes)
        if padding_size > 0:
            file_extension_bytes += b'\x00' * padding_size

        # add file_extension at the beginning of file data to store it
        # and add signature to can determine end of file
        self.binary_file_data = file_extension_bytes + self.binary_file_data + b'\x00\x10\x20\x30\x40'

        # get data length and check if we can hide it in image bytes
        self.data_length = len(self.binary_file_data)

        # (image_size * len(self.img.getbands())) is size of image * number of channels (RGB, RGBA, ...)
        if self.data_length > (image_size * len(self.img.getbands())) / 8:
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
                                (self.binary_file_data[self.data_index] >> bit_index) & 1)

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
