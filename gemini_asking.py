from email.mime import image
import os
import textwrap
from PIL import Image
import google.generativeai as genai
from IPython.display import Markdown


# Configure API key
genai.configure(api_key="AIzaSyBeML2HTdNt9Ia9UTdC0Ic1DAjzRNyFYdw")

# Set model parameters
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

# Initialize the model
model = genai.GenerativeModel(
    model_name="gemini-1.0-pro-vision-latest",
    generation_config=generation_config,
    # safety_settings=NONE,
    # language="en",  # Specify English language
)

# Define the path to the image folder
image_folder = os.path.normpath(os.path.join(os.getcwd(), "photos/tattoos"))

# List all files in the directory
image_files = os.listdir(image_folder)


def to_markdown(text):
    text = text.replace("•", "  *")
    return Markdown(textwrap.indent(text, "> ", predicate=lambda _: True))


# Iterate over each image file
for filename in image_files:
    print(filename)
    # Check if the file is an image (you can add more image extensions if needed)
    if (
        filename.lower().endswith(".jpg")
        or filename.lower().endswith(".jpeg")
        or filename.lower().endswith(".png")
    ):
        # Construct the full path to the image
        image_path = os.path.join(image_folder, filename)

        # Open the image
        img = Image.open(image_path)
        # model = genai.GenerativeModel("gemini-pro-vision")
        # Display the image (optional)
        # img.show()
        response = model.generate_content(
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
        # Print the generated description
        print(response.text)
        # print(to_markdown(response.text))
