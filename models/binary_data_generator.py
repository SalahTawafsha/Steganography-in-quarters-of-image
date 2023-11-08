import os


class BinaryDataGenerator:
    def generate_binary_data(self):
        pass


class FileBinaryDataGenerator(BinaryDataGenerator):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.binary_file_data = b""

    def generate_binary_data(self):
        with open(self.file_path, 'rb') as file:
            self.binary_file_data = file.read()

        file_name, file_extension = os.path.splitext(self.file_path)

        # Convert the file_extension to bytes and complete it to 10 byte
        file_extension_bytes = file_extension.encode('utf-8')[:10]
        padding_size = 10 - len(file_extension_bytes)
        if padding_size > 0:
            file_extension_bytes += b'\x00' * padding_size

        # add file_extension at the beginning of file data to store it
        # and add signature to can determine end of file
        return file_extension_bytes + self.binary_file_data + b'\x00\x10\x20\x30\x40'


class StringBinaryDataGenerator(BinaryDataGenerator):
    def __init__(self, string_data: str):
        self.string_data = string_data
        self.binary_string_data = b""

    def generate_binary_data(self):
        self.binary_string_data = self.string_data.encode('utf-8')
        # add signature to can determine end of data
        return self.binary_string_data + b'\x00\x10\x20\x30\x40'
