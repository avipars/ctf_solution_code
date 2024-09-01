import os

from PyPDF2 import PdfReader, PdfWriter

"""
Given a password protected PDF and a password
Decrypt the PDF and extract images and attachments

"""


def attack_pdf(input_pdf_path, output_pdf_path, password):
    """
    decrypts pdf, then extracts images and attachments from the PDF
    """
    attachments = {}  # empty dictionary to store attachments

    img_count = 0  # number of images in the PDF
    out = PdfWriter()
    file = PdfReader(input_pdf_path)
    if not file.is_encrypted:
        return False, input_pdf_path, attachments, img_count

    try:
        file.decrypt(password)  # pycryptodome required for aes encryption
    except Exception as e:
        print(f"Failed to decrypt file with password, error {e}", password)
        return False, None, attachments, img_count

    for page in file.pages:
        # process all images in the PDF
        for (
            img_file
        ) in (
            page.images
        ):  # https://pypdf2.readthedocs.io/en/3.0.0/user/extract-images.html relies on PILLOW
            img_path = os.path.join(
                output_pdf_path, str(img_count) + img_file.name)
            with open(img_path, "wb") as fp:
                fp.write(img_file.data)
                img_count += 1  # unique image count = unique image names

        # process all attachments in the PDF
        out.add_page(page)  # finally add the page to the output PDF
    out_file = os.path.join(output_pdf_path, "_res.pdf")

    with open(out_file, "wb") as f:
        out.write(f)

    attachments = get_attachments(file)

    return (True, out_file, attachments, img_count)


def get_attachments(reader):
    """
    Take out all the attachments from the PDF and save in dictionary (return value)
    Originally from https://gist.github.com/kevinl95/29a9e18d474eb6e23372074deff2df38 and modified slightly
    """
    catalog = reader.trailer["/Root"]
    file_names = catalog["/Names"]["/EmbeddedFiles"]["/Names"]
    attachments = {}
    for file_n in file_names:
        if isinstance(file_n, str):
            name = file_n
            data_index = file_names.index(file_n) + 1
            f_dict = file_names[data_index].get_object()
            f_data = f_dict["/EF"]["/F"].get_object()
            attachments[name] = (
                f_data.get_data()
            )  # get data (bytes) instead of the encoded stream
    return attachments


def main():

    input_pdf = input("Enter the path of the PDF file (including .pdf): ")
    password = input("Enter the password: ")
    out_path = input(
        "Enter the path to save the decrypted PDF (and attachments) without .pdf at end: "
    )

    if not os.path.exists(out_path):
        os.makedirs(out_path)
        print("Created output directory", out_path)

    res, output_pdf, attch, img_count = attack_pdf(
        input_pdf, out_path, password)

    if res:
        print("Decrypted PDF saved at", output_pdf)
    elif res and output_pdf is None:
        print("PDF Decryption with password failed")
    else:
        print("PDF is not encrypted")

    if attch:
        print("Attachments found in the PDF")
        for name, data in attch.items():
            attch_path = os.path.join(out_path, name)
            print("Saving attachment to:", attch_path)
            with open(attch_path, "wb") as f:
                f.write(data)
    if img_count > 0:
        print("Images found in the PDF")
        print("Images saved in the same folder as the output PDF")


if __name__ == "__main__":
    main()
