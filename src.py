import pandas as pd
import cv2
import numpy as np
import pytesseract
from pdf2image import convert_from_bytes
from io import StringIO
import os
from PIL import Image, ImageDraw
import re


class TextReport:
    """Class for textual reports handling"""

    def __init__(self, file_obj, lang):
        """Init Method for the class
        Args:
            file_obj (file object): File object of the PDF
            lang (str): Language of the PDF (fra for french, eng for english)
        """
        self.file_obj = file_obj
        self.lang = lang
        self.image_stack = []
        self.raw_text = ""
        self.text_as_list = []
        self.header_text = []
        self.results_match_dict = {}

    def get_grayscale(self, image):
        """Convert an image as numpy array to grayscale
        Args:
            image (numpy array): Image as numpy array
        Returns:
            image: image object
        """
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def thresholding(self, image):
        """Treshold pixel of greyscale image
        Args:
            image (numpy array): Image as numpy array
        Returns:
            image: image object
        """
        return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    def pdf_to_text(self):
        """Convert PDF file object from image to text using Tesseract with langage settings.
        OEM 1 PSM 1
        Returns:
            str: raw text as a string
        """
        self.image_stack = convert_from_bytes(self.file_obj.read())
        page_list = []
        # Loop on each image (page) of the PDF file
        for image in self.image_stack:
            open_cv_image = np.array(image)
            # Convert RGB to BGR
            open_cv_image = open_cv_image[:, :, ::-1].copy()
            # Preprocess image
            open_cv_image = self.thresholding(self.get_grayscale(open_cv_image))
            # Tesseract OCR
            custom_config = r"-l " + self.lang + r" --oem 1 --psm 1 "
            text_page = pytesseract.image_to_string(open_cv_image, config=custom_config)
            # Save text results
            page_list.append(text_page)
        self.raw_text = "\n".join(page_list)
        self.text_as_list = self.raw_text.split("\n")
        return self.raw_text

    def pdf_censor(self, output_folder):
        self.image_stack = convert_from_bytes(self.file_obj.read())
        censored_image_stack = []
        page_list = []
        new_filename = os.path.basename(self.file_obj.name) + "_censored.pdf"
        # Loop on each image (page) of the PDF file
        for image in self.image_stack:
            open_cv_image = np.array(image)
            open_cv_image = open_cv_image[:, :, ::-1].copy()
            open_cv_image = self.thresholding(self.get_grayscale(open_cv_image))
            custom_config = r"-l " + self.lang + r" --oem 1 --psm 1 "
            text_page = pytesseract.image_to_string(open_cv_image, config=custom_config)
            self.image_data_table_as_str = pytesseract.image_to_data(
                open_cv_image, config=custom_config
            )
            image_data_table = pd.read_csv(
                StringIO(self.image_data_table_as_str),
                sep="\t",
                quoting=3,
                on_bad_lines="skip",
            )
            text_as_list = text_page.split("\n")
            biopsy_id, to_censor = self._regex_match(text_as_list)
            if biopsy_id is not None:
                new_filename = biopsy_id.replace("/", "-") + "_" + self.file_obj.name
            list_bbox = self._get_bbox(image_data_table, to_censor)
            image_censored = self._draw_censor(image, list_bbox)
            censored_image_stack.append(image_censored)
        output_path = os.path.join(output_folder, new_filename)
        while os.path.isfile(output_path):
            new_filename = "dup_" + new_filename
            output_path = os.path.join(output_folder, new_filename)
        censored_image_stack[0].save(
            output_path, save_all=True, append_images=censored_image_stack[1:]
        )
        return output_path

    def _regex_match(self, text_as_list):
        re_nom = re.compile(r"Nom.*: *([A-Za-zÀ-ÿ- ]+)")
        re_nom2 = re.compile(r"(([A-Z][a-zÀ-ÿ-]{3,} ?)+ ([A-Z-]{3,} ?)+)")
        re_nom3 = re.compile(r"(([A-Z-]{3,} ?)+ ([A-Z][a-zÀ-ÿ-]{3,} ?)+)")
        re_date = re.compile(
            r"([(\.]?[0-9]{1,2}[\.\/][0-9]{1,2}[\.\/][0-9]{1,4}[()\.]?)"
        )
        re_biopsy_number = re.compile(r": *([0-9]{4,8}[-\/]?[0-9]{0,3})")
        re_biopsy_number2 = re.compile(r"Bps +N° +([0-9-\/]{1,10})")
        to_censor = []
        biopsy_id = None

        for line in text_as_list:
            match_nom = re_nom.search(line)
            if match_nom is not None:
                to_censor.append(match_nom.group(1))
            match_nom2 = re_nom2.search(line)
            if match_nom2 is not None:
                to_censor.append(match_nom2.group(1))
            match_nom3 = re_nom3.search(line)
            if match_nom3 is not None:
                to_censor.append(match_nom3.group(1))
            match_date = re_date.search(line)
            if match_date is not None:
                to_censor.append(match_date.group(1))
            match_number_biop = re_biopsy_number.search(line)
            if match_number_biop is not None:
                biopsy_id = match_number_biop.group(1)
            match_number_biop2 = re_biopsy_number2.search(line)
            if match_number_biop2 is not None:
                biopsy_id = match_number_biop2.group(1)
        return biopsy_id, to_censor

    def _get_bbox(self, ocr_datatable, to_censor):
        list_bbox = []
        for terms in to_censor:
            for words in terms.split(" "):
                line = ocr_datatable.loc[ocr_datatable["text"] == words]
                # try:
                for index, row in line.iterrows():
                    bbox = [row[6], row[7], row[6] + row[8], row[7] + row[9]]
                    list_bbox.append(bbox)
                # except Exception as e:
                #    print("Error for word:", words, "in ", self.file_obj.name)
        return list_bbox

    def _draw_censor(self, image, list_bbox):
        im_draw = ImageDraw.Draw(image)
        for bbox in list_bbox:
            im_draw.rectangle(bbox, fill="black")
        return image