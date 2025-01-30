import pyautogui
import pytesseract
import keyboard
import time
import sys
import os
from PIL import Image
from openai import OpenAI
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_screen(region):
    screenshot = pyautogui.screenshot(region=region)
    text = pytesseract.image_to_string(screenshot)
    return text.strip()

def generate_comeback(prompt):
    try:
        completion = client.chat.completions.create(
            model= "gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a witty AI that generates clever comebacks."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=20,
            temperature=0.8
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error: {e}")
        return "Couldn't generate a comeback."

def run_comeback():
    region = (400, 100, 1000, 500)  
    text = extract_text_from_screen(region)
    
    if text:
        print(f"Extracted Text: {text}")
        comeback = generate_comeback(text)
        print(f"AI-Generated Comeback: {comeback}")

    time.sleep(5)

def exit_program():
    print("Exiting program...")
    sys.exit()

def main():
    keyboard.add_hotkey(']', run_comeback)
    keyboard.add_hotkey('[', exit_program)
    keyboard.wait()

if __name__ == "__main__":
    main()
