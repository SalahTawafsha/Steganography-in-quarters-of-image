import hashlib


class FileHashCode:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def generate_hash(self) -> str:
        # Create a hash object using SHA-256 algorithm
        sha256_hash = hashlib.sha256()

        # Open the file in binary mode and read it in chunks
        with open(self.file_path, "rb") as file:
            while True:
                # Read a chunk of data from the file
                chunk = file.read(4096)  # You can adjust the chunk size as needed

                # If no more data is left to read, break the loop
                if not chunk:
                    break

                # Update the hash object with the chunk of data
                sha256_hash.update(chunk)

        # Get the hexadecimal representation of the hash
        file_hash = sha256_hash.hexdigest()

        return file_hash

    def is_file_hash(self, hash_code: str) -> bool:
        return self.generate_hash() == hash_code
