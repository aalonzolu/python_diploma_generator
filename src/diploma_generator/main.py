# -*- coding: utf-8 -*-
import os
import urllib.parse
import urllib.request
import argparse
import re

from fpdf import FPDF


class DiplomaGenerator:
    def __init__(self,
                 image_path: str = None,
                 x: float = 3,
                 y: float = 11,
                 w: float = 24,
                 h: float = 1,
                 font_size: float = 25,
                 font_path: str = None
                 ):
        """
        :param image_path: path to background image
        :param x: x position for name in cm
        :param y: y position for name in cm
        :param w: width for name space in cm
        :param h: height for name space in cm
        :param font_size: OPTIONAL font size for name float
        :param font_path: OPTIONAL font path
        """

        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.pdf = FPDF(orientation='L', unit='cm', format='Letter')
        self.font_path = os.path.join(os.path.dirname(__file__), 'font.ttf')
        if font_path is not None:
            self.font_path = font_path
        self.pdf.add_font('font', '', self.font_path, uni=True)
        self.pdf.set_font('font', '', font_size)
        self.background_image_path = image_path

    def add_diploma_page(self, name: str, qr_code: str = None):
        self.pdf.add_page()
        self.pdf.set_margins(left=0, top=0, right=0)
        self.pdf.set_auto_page_break(False)

        self._set_image(self.background_image_path)
        self.add_name(name)
        if qr_code is not None and qr_code != "":
            self.add_qr_code(qr_code)
        return f"Name: {name}"

    def _set_image(self, image_path: str):
        self.pdf.image(image_path, x=0, y=0, w=28.7, h=21.6)

    def add_name(self, name):
        self.pdf.set_xy(self.x, self.y)
        self.pdf.cell(self.w, self.h, name, 0, 0, align='C', fill=False)
        return f"Name: {name}"

    def add_qr_code(self, qr_text):
        qr_code_image_base = "https://public-api.qr-code-generator.com/v1/create/free?image_format=JPG&image_width" \
                             "=500&foreground_color=%23000000&qr_code_logo" \
                             "=&qr_code_pattern=&qr_code_text="
        qr_code_image = qr_code_image_base + urllib.parse.quote(qr_text) + "&?image.jpg"

        # download image url
        urllib.request.urlretrieve(qr_code_image, "qr_code.jpg")

        self.pdf.image("qr_code.jpg", x=24, y=0.5, w=3.5, h=3.5)

        # remove image
        os.remove("qr_code.jpg")

    def save(self, path):
        self.pdf.output(path)


def main():
    """
    command line arguments
     -i: background image path
     -n: name
     -o: output path optional (default: md5(email).pdf)
     -xy: x and y position for name ex: 3,11
     -w,h: width and height for name ex: 24,1
     -fz: font size
     -f: font path
     -h: help
    """

    parser = argparse.ArgumentParser(description='Process some command line arguments.')

    # Arguments
    parser.add_argument('-i', '--image', type=str, required=True, help='Path to the background image')
    parser.add_argument('-n', '--name', type=str, required=True, help='Name')
    parser.add_argument('-qr', '--qr_code', type=str, default=None, help='QR code text')
    parser.add_argument('-xy', '--xy', type=str, default="3,11", help='x and y position for name ex: 3,11')
    parser.add_argument('-wh', '--wh', type=str, default="24,1", help='width and height for name ex: 24,1')
    parser.add_argument('-fz', '--font_size', type=int, default=25, help='Font size default 25')
    parser.add_argument('-f', '--font', type=str, default=None, help='Font path')
    parser.add_argument('-o', '--output', type=str, default=None, help='Output path (default is output.pdf)')

    args = parser.parse_args()

    if args.output is None:
        args.output = "output.pdf"

    # add .pdf to output if not present
    if not args.output.endswith(".pdf"):
        args.output += ".pdf"

    x, y = args.xy.split(",")
    w, h = args.wh.split(",")

    font_size = args.font_size

    font_path = args.font

    diploma_generator = DiplomaGenerator(
        args.image,
        float(x), float(y),
        float(w), float(h),
        float(font_size), font_path
    )
    diploma_generator.add_diploma_page(args.name, args.qr_code)
    diploma_generator.save(args.output)


def clean_string(string):
    return re.sub(r'[^a-zA-Z0-9ÁÉÍÓÚÑáéíóúñ@ .,]', '', string)


def main_csv():
    """
    Same as main but with csv file containing name, QR Code and output path
    If output path is not specified it will be output.pdf
    If output is specified in csv file it will be used instead of the default
    """

    parser = argparse.ArgumentParser(description='Process some command line arguments.')
    # Arguments
    parser.add_argument('-i', '--image', type=str, required=True, help='Path to the background image')
    parser.add_argument('-xy', '--xy', type=str, default="3,11", help='x and y position for name ex: 3,11')
    parser.add_argument('-wh', '--wh', type=str, default="24,1", help='width and height for name ex: 24,1')
    parser.add_argument('-fz', '--font_size', type=int, default=25, help='Font size default 25')
    parser.add_argument('-f', '--font', type=str, default=None, help='Font path')
    parser.add_argument('-o', '--output', type=str, default=None, help='Output path (default is output.pdf)')

    parser.add_argument('-csv', '--csv', type=str, required=True,
                        help='Path to the csv file containing name, QR Code (optional) and output path(optional) NO '
                             'HEADER')

    parser.add_argument('-D', '--debug', action='store_true', help='Debug mode')

    args = parser.parse_args()

    single_file = args.output is not None
    default_output = "output.pdf"
    if args.output:
        args.output = args.output.strip()
    if args.output and not args.output.endswith(".pdf"):
        args.output += ".pdf"

    x, y = args.xy.split(",")
    w, h = args.wh.split(",")

    font_size = args.font_size

    font_path = args.font

    diploma_generator = DiplomaGenerator(
        args.image,
        float(x), float(y),
        float(w), float(h),
        float(font_size), font_path
    )

    with open(args.csv, 'r', encoding='utf-8') as csv_file:
        for line in csv_file:
            if not single_file:
                diploma_generator = DiplomaGenerator(
                    args.image,
                    float(x), float(y),
                    float(w), float(h),
                    float(font_size), font_path
                )
            # Split the line into parts
            parts = line.split(",")

            # Unpack the first three values and ignore the rest
            name, qr_code, output, *extra = parts[:3]
            name = clean_string(name.strip())
            qr_code = qr_code.strip()
            output = output.strip()

            # Generate the diploma
            diploma_generator.add_diploma_page(name, qr_code)

            if args.debug:
                print("[DEBUG] Generating diploma for the following data:")
                print("Name:", name)
                print("QR Code:", qr_code)
                print("Output file name:", output)
            if not single_file:
                output = output.strip()
                if output == "":
                    output = default_output
                elif not output.endswith(".pdf"):
                    output += ".pdf"
                diploma_generator.save(output)

    if single_file:
        diploma_generator.save(args.output)
