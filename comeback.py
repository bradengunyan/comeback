import pyautogui
import pytesseract
import keyboard
import sys
import os
import time
from PIL import Image
from openai import OpenAI
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_image(image):
    """Convert image to grayscale and increase contrast."""
    image = image.convert("L")  # Convert to grayscale
    image = image.point(lambda x: 0 if x < 128 else 255)  # Increase contrast
    return image

def extract_text_from_screen(region):
    """Capture screenshot, preprocess it, and extract text using Tesseract."""
    screenshot = pyautogui.screenshot(region=region)
    processed_image = preprocess_image(screenshot)
    text = pytesseract.image_to_string(processed_image, config="--psm 6")
    return text.strip()

def generate_comeback(prompt):
    """Generate a witty AI comeback using OpenAI API."""
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a witty AI that generates clever comebacks."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50,  # Increase length for better responses
            temperature=0.9  # More creativity
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error: {e}")
        return "Couldn't generate a comeback."

def run_comeback():

    region = (20, 1000, 70, 50)
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save("chat_screenshot.png")  # Save for debugging

    # Process image and extract text
    image = Image.open("chat_screenshot.png")
    processed_image = preprocess_image(image)
    chat = pytesseract.image_to_string(processed_image, config="--psm 6")
    print(f"THIS IS THE CHAT:::::{chat}")

    region = (20, 800, 400, 250)  # Define the correct region for chat text

    # Capture and save screenshot for debugging
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save("debug_screenshot.png")  # Save for debugging

    # Process image and extract text
    image = Image.open("debug_screenshot.png")
    processed_image = preprocess_image(image)
    text = pytesseract.image_to_string(processed_image, config="--psm 6")

    if text:
        print(f"Extracted Text: {text}")

        # Generate AI comeback
        comeback = generate_comeback(text)
        print(f"AI-Generated Comeback: {comeback}")

        # Type the comeback into the chat
        keyboard.press('shift')
        time.sleep(0.5)
        keyboard.press_and_release('enter')  # Open chat (if required)
        time.sleep(0.2)
        keyboard.release('shift')
        keyboard.write(comeback, delay=0.05)  # Type the AI response
        time.sleep(0.5)
        keyboard.press_and_release('enter')  # Send the message
    else:
        print("No text found")

def exit_program():
    print("Exiting program...")
    sys.exit()

def main():
    keyboard.add_hotkey(']', run_comeback)  # Press "]" to trigger comeback
    keyboard.add_hotkey('[', exit_program)  # Press "[" to exit
    keyboard.wait()

if __name__ == "__main__":
    main()
