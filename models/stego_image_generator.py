import os

from PIL import Image


class StegoImageGenerator:
    def __init__(self, original_file_path: str, image_file_path: str):
        self.original_file_path = original_file_path
        self.image_file_path = image_file_path
        self.__extract_and_validate()  # validate that we can hide the message in the image
        self.data_index = 0

    def __extract_and_validate(self):
        self.img = Image.open(self.image_file_path)
        self.image_width, self.image_height = self.img.size
        image_size_in_bytes = self.image_width * self.image_height

        with open(self.original_file_path, 'rb') as file:
            self.binary_file_data = file.read()

        file_name, file_extension = os.path.splitext(self.original_file_path)

        # Convert the file_extension to bytes and ensure it's not longer than 10 bytes
        file_extension_bytes = file_extension.encode('utf-8')[:10]
        padding_size = 10 - len(file_extension_bytes)
        if padding_size > 0:
            file_extension_bytes += b'\x00' * padding_size

        # Create the modified binary data with the file_extension at the beginning
        # and add signature for end of file
        self.binary_file_data = file_extension_bytes + self.binary_file_data + b'\x00\x10\x20\x30\x40'

        self.data_length = len(self.binary_file_data)
        self.chunk_size = image_size_in_bytes / 4

        if self.data_length > (image_size_in_bytes * 3) / 8:
            raise ValueError("File too large to encode in the given image")

    # hide data in range of image pixels and return True if data Not end or False if end
    def _hide_data(self, from_x_pixel: int, to_x_pixel: int, from_y_pixel: int, to_y_pixel: int):
        bit_index = 7

        for x in range(from_x_pixel, to_x_pixel):
            for y in range(from_y_pixel, to_y_pixel):
                pixel = list(self.img.getpixel((x, y)))

                for color_channel in range(len(self.img.getbands())):
                    if self.data_index < self.data_length:
                        pixel[color_channel] = pixel[color_channel] & ~1 | (
                                (self.binary_file_data[self.data_index] >> bit_index) & 1)
                        if bit_index != 0:
                            bit_index = (bit_index - 1)
                        else:
                            self.data_index += 1
                            bit_index = 7
                    else:
                        return False

                self.img.putpixel((x, y), tuple(pixel))
        return True

    def generate_stego_image(self):
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
