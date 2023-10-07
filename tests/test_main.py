import unittest
import os
import hashlib

from diploma_generator.main import DiplomaGenerator


class TestMain(unittest.TestCase):

    def setUp(self) -> None:
        self.diploma_path = "C:\\Users\\aalon\\Documents\Projects\\python_diploma_generator\\resources\\diploma-min.jpg"
        self.diploma_generator = DiplomaGenerator(self.diploma_path)

    def test_main(self):
        name = "Nombre De Ejemplo"

        email = "aalonzolu@gmail.com"
        email_md5 = hashlib.md5(email.encode('utf-8')).hexdigest()
        asiti_url_qr = "https://asiti.io.gt/events/asiti2023/#" + email_md5

        result = self.diploma_generator.add_diploma_page(name, asiti_url_qr)

        self.diploma_generator.save("C:\\Users\\aalon\\Documents\Projects\\python_diploma_generator\\resources\\diploma-out.pdf")

        self.assertEqual(result, f"Name: {name}")
