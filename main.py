from models.binary_data_generator import FileBinaryDataGenerator, StringBinaryDataGenerator
from models.file_hash_code import FileHashCode
from models.stego_image_extractor import StegoImageExtractor
from models.stego_image_generator import StegoImageGenerator
import argparse
import os


def main():
    # Make arg parser to use program as Command-line interface (CLI)
    parser = argparse.ArgumentParser()

    # add hide file in image arguments
    parser.add_argument("-hf",
                        '--hide-file',
                        type=argparse.FileType('r'),
                        nargs=2,
                        metavar=("file_to_hide", "image"),
                        )

    # add hide hash of file in image arguments
    parser.add_argument("-hh",
                        '--hide-hash',
                        type=argparse.FileType('r'),
                        nargs=2,
                        metavar=("file_to_hide", "image"),
                        )

    # add extract file from stego image arguments
    parser.add_argument('-ef',
                        "--extract-file",
                        type=argparse.FileType('r'),
                        metavar="stego_file",
                        )

    # add extract hash from stego image arguments
    parser.add_argument('-eh',
                        "--extract-hash",
                        type=argparse.FileType('r'),
                        nargs=2,
                        metavar=("stego_file", "need_to_check_file"),
                        )
    args = parser.parse_args()

    if args.hide_file:
        # get files from arguments
        original_file_path, stego_file_path = args.hide_file

        # get file as binary data
        file_binary_data_generator = FileBinaryDataGenerator(original_file_path.name)

        # create StegoImageGenerator object
        stego_image_generator = StegoImageGenerator(file_binary_data_generator.generate_binary_data(),
                                                    stego_file_path.name)

        # generate stego image
        image = stego_image_generator.generate_stego_image()

        # save stego image
        stego_file_name, stego_file_extension = os.path.splitext(stego_file_path.name)
        image.save(f"{stego_file_name}-stego file{stego_file_extension}")

    if args.extract_file:
        # get stego file from argument
        stego_file_path = args.extract_file.name

        # create StegoImageExtractor object
        stego_image_extractor = StegoImageExtractor(stego_file_path)

        # extract file data and extension
        binary_file, output_file_extension = stego_image_extractor.extract_data()

        # save extracted data
        with open(f"extracted-file{output_file_extension}", 'wb') as file:
            file.write(binary_file)

    if args.hide_hash:
        # get files from arguments
        original_file_path, stego_file_path = args.hide_hash

        file_hash_code = FileHashCode(original_file_path.name)
        hash_code = file_hash_code.generate_hash()

        # create StringBinaryDataGenerator object that to convert hash_code to binary data
        string_binary_data_generator = StringBinaryDataGenerator(hash_code)

        hash_binary_data = string_binary_data_generator.generate_binary_data()

        # create StegoImageGenerator object
        stego_image_generator = StegoImageGenerator(hash_binary_data,
                                                    stego_file_path.name)

        # generate stego image
        image = stego_image_generator.generate_stego_image()

        # save stego image
        stego_file_name, stego_file_extension = os.path.splitext(stego_file_path.name)
        image.save(f"{stego_file_name}-hash{stego_file_extension}")

    if args.extract_hash:
        # get stego file and the file that we want to check from argument
        stego_file, need_to_check_file = args.extract_hash

        # create StegoImageExtractor object
        stego_image_extractor = StegoImageExtractor(stego_file.name)

        # extract hash value
        binary_hash, ignored = stego_image_extractor.extract_data()

        # create FileHashCode and check if binary hash is the hash of file
        file_hash_code = FileHashCode(need_to_check_file.name)

        if file_hash_code.is_file_hash(binary_hash.decode('utf-8')):
            print("Success")
        else:
            print("Failed")


if __name__ == "__main__":
    main()
