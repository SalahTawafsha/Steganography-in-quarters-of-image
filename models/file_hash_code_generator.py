class FileHashCodeGenerator:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def generate_hash(self) -> str:
        hash_value = 0

        # Open the file in binary mode and read it in chunks
        with open(self.file_path, "rb") as file:
            while True:
                # Read a chunk of data from the file
                chunk = file.read(4096)  # You can adjust the chunk size as needed

                # If no more data is left to read, break the loop
                if not chunk:
                    break

                # Update the hash_value by add ones representation
                for byte in chunk:
                    binary_representation = bin(byte)
                    hash_value += binary_representation.count('1')

        return hash_value

    def is_for_file(self, hash_code: int) -> bool:
        return self.generate_hash() == hash_code


