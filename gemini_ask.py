from email.mime import image
import os
import textwrap
from PIL import Image
import google.generativeai as genai
from IPython.display import Markdown


class ImageDescriptionGenerator:
    def __init__(self):
        self.model = None
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
        ]

    def configure_api_key(self, api_key):
        try:
            genai.configure(api_key=api_key)
        except Exception as e:
            print(f"[INFO] Error configuring API key: {e}")

    def initialize_model(self, model_name, generation_config):
        try:
            self.model = genai.GenerativeModel(
                model_name=model_name,
                generation_config=generation_config,
            )
        except Exception as e:
            print(f"[INFO] Error initializing model: {e}")

    def process_images(self, image_folder):
        try:
            image_files = os.listdir(image_folder)

            for filename in image_files:
                print(filename)
                if (
                    filename.lower().endswith(".jpg")
                    or filename.lower().endswith(".jpeg")
                    or filename.lower().endswith(".png")
                ):
                    image_path = os.path.join(image_folder, filename)

                    try:
                        img = Image.open(image_path)

                        response = self.model.generate_content(
                            [
                                "Choose the following answers that match to the image."
                                "The color is (A): colorful, (B): black and white."
                                "The style is (C): stripes, (D): filled up, (E): mixed",
                                "For example, if the picture is colorful and filled up then answer would be: A B",
                                img,
                            ],
                            stream=True,
                        )
                        response.resolve()

                        print(response.text)

                    except Exception as e:
                        print(f"[INFO] Error processing image '{filename}': {e}")

        except Exception as e:
            print(f"[INFO] Error listing image files: {e}")
