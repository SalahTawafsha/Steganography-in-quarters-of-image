from PIL import Image


class StegoImageExtractor:
    def __init__(self, stego_image_path: str):
        self.stego_image_path = stego_image_path
        self.binary_file_data = bytearray()
        self.file_extension = ".txt"
        self.data_index = 0
        self.current_byte = 0

    def _extract_data(self, img: Image, from_x_pixel: int, to_x_pixel: int, from_y_pixel: int, to_y_pixel: int):
        for x in range(from_x_pixel, to_x_pixel):
            for y in range(from_y_pixel, to_y_pixel):
                # get pixel in x, y location
                pixel = list(img.getpixel((x, y)))

                # Iterate on channels of pixel (RGB, RGBA, ...)
                for color_channel in range(len(img.getbands())):
                    if self.data_index % 8 == 0 and self.data_index > 0:
                        # when data_index == 8 then we reach end of byte
                        # so append the current byte to the hidden binary data and reset data_index
                        self.binary_file_data.append(self.current_byte)
                        self.current_byte = 0

                        # check if my end of data signature reached and return false to stop extraction
                        if self.data_index > 80 and self.binary_file_data[-5:] == bytearray([0, 16, 32, 48, 64]):
                            return False

                    # shift left to can add new bit and make or with pixel
                    # and the & 1 is to ignore value of byte expect the least significant bit (value & 0000 0001)
                    self.current_byte = (self.current_byte << 1) | (pixel[color_channel] & 1)
                    self.data_index += 1

                    # when data_index reach to 88 then we end file extension bytes so extract extension
                    if self.data_index == 88:
                        self.file_extension = self.binary_file_data[:10].rstrip(b'\x00').decode('utf-8')
                        self.binary_file_data = bytearray()
        return True

    def decode_file(self):
        # Open the stego image
        img = Image.open(self.stego_image_path)
        width, height = img.size

        # get data from quarters of image
        half_image_width = width // 2
        half_image_height = height // 2

        # hide data in second quarter
        if self._extract_data(img, half_image_width, width, 0, half_image_height):
            # hide data in first quarter
            if self._extract_data(img, 0, half_image_width, 0, half_image_height):
                # hide data in forth quarter
                if self._extract_data(img, half_image_width, width, half_image_height, height):
                    # hide data in third quarter
                    self._extract_data(img, 0, half_image_width, half_image_height, height)

        return self.binary_file_data[:-5], self.file_extension
