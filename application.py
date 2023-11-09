from models.binary_data_generator import FileBinaryDataGenerator, HashBinaryDataGenerator
from models.file_hash_code_generator import FileHashCodeGenerator
from models.stego_image_extractor import StegoImageExtractor
from models.stego_image_generator import StegoImageGenerator
import argparse
import os


def main():
    # Make argparse to use program as Command-line interface (CLI)
    parser = argparse.ArgumentParser()

    # add hide file in image arguments
    parser.add_argument("-hf",
                        '--hide-file',
                        nargs=2,
                        metavar=("file_to_hide", "image"),
                        )

    # add hide hash of file in image arguments
    parser.add_argument("-hh",
                        '--hide-hash',
                        nargs=2,
                        metavar=("file_to_hide_hash", "image"),
                        )

    # add extract file from stego image arguments
    parser.add_argument('-rf',
                        "--recover-file",
                        metavar="stego_file",
                        )

    # add extract hash from stego image arguments
    parser.add_argument('-rh',
                        "--recover-hash",
                        nargs=2,
                        metavar=("stego_file", "need_to_check_file"),
                        )
    args = parser.parse_args()

    if args.hide_file:
        # get files from arguments
        file_to_hide_path, image_path = args.hide_file

        # create binary data generator object
        file_binary_data_generator = FileBinaryDataGenerator(file_to_hide_path)

        # generate file binary data from file
        file_binary_data = file_binary_data_generator.generate_binary_data()

        # create StegoImageGenerator object
        stego_image_generator = StegoImageGenerator(file_binary_data, image_path)

        # generate stego image
        stego_image = stego_image_generator.generate_stego_image()

        # get image name and extension to can modify name and save stego image in it
        image_name, image_extension = os.path.splitext(image_path)
        stego_image.save(f"{image_name}-stego file{image_extension}")

    if args.recover_file:
        # get stego file from argument
        image_path = args.recover_file

        # create StegoImageExtractor object
        stego_image_extractor = StegoImageExtractor(image_path, True)

        # extract file data and extension
        binary_file, output_file_extension = stego_image_extractor.recover_data()

        # save extracted data
        with open(f"recovered-file{output_file_extension}", 'wb') as file:
            file.write(binary_file)

    if args.hide_hash:
        # get files from arguments
        file_to_hide_path, image_path = args.hide_hash

        # create FileHashCodeGenerator and generate hash code
        file_hash_code_generator = FileHashCodeGenerator(file_to_hide_path)
        hash_value = file_hash_code_generator.generate_hash()

        # create StringBinaryDataGenerator object that to convert hash_value to binary data
        string_binary_data_generator = HashBinaryDataGenerator(hash_value)

        # generate hash hash_binary_data to hide it
        hash_binary_data = string_binary_data_generator.generate_binary_data()

        # create StegoImageGenerator object
        stego_image_generator = StegoImageGenerator(hash_binary_data, image_path)

        # generate stego image
        stego_image = stego_image_generator.generate_stego_image()

        # get image name and extension to can modify name and save stego image in it
        image_name, image_extension = os.path.splitext(image_path)
        stego_image.save(f"{image_name}-hash{image_extension}")

    if args.recover_hash:
        # get stego file and the file that we want to check from argument
        stego_file, need_to_check_file = args.recover_hash

        # create StegoImageExtractor object
        stego_image_extractor = StegoImageExtractor(stego_file)

        # extract hash value
        binary_hash, ignored = stego_image_extractor.recover_data()

        # create FileHashCodeGenerator object
        file_hash_code_generator = FileHashCodeGenerator(need_to_check_file)

        # check if binary hash is the hash of file
        if file_hash_code_generator.is_for_file(int.from_bytes(binary_hash, byteorder='big')):
            print("Success Test")
        else:
            print("Failed Test")


if __name__ == "__main__":
    main()
