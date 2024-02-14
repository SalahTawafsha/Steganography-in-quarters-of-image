# Steganography in Python

This is a simple steganography project in Python. updated to hide the file in the image be dividing the image into 4
quarters and hide the file in the parts of the image.

What we can do with this project:

- Hide a file in an image.
- Extract a file from an image.
- Generate hash for file and hide it in an image.
- Extract hash from an image and compare it with an existing file (by generating hash for the file and compare it with
  the extracted hash).

## installation

```bash
git clone https://github.com/SalahTawafsha/Steganography-in-quarters-of-image.git
pip install -r requirements.txt
```

## Usage

### 1. Hide a file in an image

We will run below command and replace `<file_path>` with the file path and `<image_path>` with the image path

```bash
py application.py -hf <file_path> <image_path>
```

### 2. Extract a file from an image

We will run below command and replace `<image_path>` with the image path

```bash
py application.py -rf <image_path>
```

### 3. Generate hash for file and hide it in an image

We will run below command and replace `<file_path>` with the file path to hide hash of it and `<image_path>` with the
image path

Note that this option can be used in network communication to verify the integrity of the file.

```bash
py application.py -hh <file_path> <image_path>
```

### 4. Extract hash from an image and compare it with an existing file

We will run below command and replace `<image_path>` with the image path that contain file hash and `<file_path>` with
the file to compare with

Note that this option can be used in network communication to verify the integrity of the file.

```bash
py application.py -rh <image_path> <file_path>
```