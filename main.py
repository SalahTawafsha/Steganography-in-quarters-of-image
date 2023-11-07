from models.stego_image_extractor import StegoImageExtractor
from models.stego_image_generator import StegoImageGenerator
import argparse
import os


def main():
    # Make arg parser to use program as Command-line interface (CLI)
    parser = argparse.ArgumentParser()

    # add generate stego arguments
    parser.add_argument("-g",
                        '--generate-stego',
                        type=argparse.FileType('r'),
                        nargs=2,
                        metavar=("original_file", "stego_file"),
                        )

    # add extract stego arguments
    parser.add_argument('-e',
                        "--extract-file",
                        type=argparse.FileType('r'),
                        metavar="stego_file",
                        )
    args = parser.parse_args()

    if args.generate_stego:
        # get files from arguments
        original_file_path, stego_file_path = args.generate_stego

        stego_image_generator = StegoImageGenerator(original_file_path.name, stego_file_path.name)

        image = stego_image_generator.generate_stego_image()

        file_name, file_extension = os.path.splitext(stego_file_path.name)
        image.save(f"{file_name}-output{file_extension}")

    if args.extract_file:
        # get stego file from argument
        stego_file_path = args.extract_file.name

        stego_image_extractor = StegoImageExtractor(stego_file_path)

        binary_file, output_file_extension = stego_image_extractor.decode_file()
        with open(f"message-output{output_file_extension}", 'wb') as file:
            file.write(binary_file)


if __name__ == "__main__":
    main()
