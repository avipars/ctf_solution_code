import os

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

"""
split an image into its bit planes and export
"""


def extract_bit_planes(image_path, grayscale=False):
    """
    Play with the bit planes of an image
    """
    img = Image.open(image_path)  # load the image

    if grayscale:
        img_array = np.array(
            img.convert("L")
        )  # image to grayscale (if not already) -> to numpy array
        bit_planes = {
            "Gray": []
        }  # dictionary to hold the bit planes (array stores all pixels)

        # extract each bit of the 8 bit color depth
        for i in range(8):  # 2^8 = 256 colors in 8-bit image
            # extract the bit plane using bitwise operations
            bit_planes["Gray"].append(
                ((img_array >> i) & 1) * 255
            )  # scale to 0-255 for visualization
        return bit_planes
    else:
        # image to RGB -> to numpy array
        img_array = np.array(img.convert("RGB"))
        # dictionaries to hold the bit planes for R, G, and B channels - array
        # stores all pixels
        bit_planes = {"Red": [], "Green": [], "Blue": [], "All": []}
        # Extract each bit plane
        for i in range(8):
            # add the bit plane modified pixel to each respective dictionary
            bit_planes["Red"].append(((img_array[:, :, 0] >> i) & 1) * 255)
            bit_planes["Green"].append(((img_array[:, :, 1] >> i) & 1) * 255)
            bit_planes["Blue"].append(((img_array[:, :, 2] >> i) & 1) * 255)
            bit_planes["All"].append(
                ((img_array >> i) & 1) * 255
            )  # all channels combined

    return bit_planes


def save_bit_planes(bit_planes, output_path, prefix="_bit_plane"):
    for color, planes in bit_planes.items():
        # 2 rows, 4 columns (2*4=8 bit planes)
        _, axes = plt.subplots(2, 4, figsize=(12, 6))  # plot all bit planes
        axes = axes.ravel()  # flatten the axes array
        print(f"Saving {color} bit planes")
        for i in range(8):
            axes[i].imshow(
                planes[i], cmap="gray"
            )  # color map is gray - black and white results have more contrast
            # set the title of the plot for reference
            axes[i].set_title(f"{color} {i}")

        plt.tight_layout()  # fit nicely in the plot
        plt.savefig(
            os.path.join(
                output_path,
                f"{color}{prefix}s.png"))  # save to file
        # plot show had some issue on my computer (windows 10 with python venv) so saving works just as well
        # plt.show()


def runner(img_path, output_path):
    print("Processing in Grayscale")
    bit_planes = extract_bit_planes(img_path, grayscale=True)
    save_bit_planes(bit_planes, output_path)
    print("Processing in RGB")
    bit_planes = extract_bit_planes(img_path, grayscale=False)
    save_bit_planes(bit_planes, output_path)


def main():
    # Example usage
    img_path = input(
        "Enter the path of the source image file (including extension): ")
    output_path = input(
        "Enter the output path to save the bit planes images: ")

    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print("Created output directory", output_path)

    runner(img_path, output_path)


if __name__ == "__main__":
    main()
