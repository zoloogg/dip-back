import openai
import requests
from PIL import Image
from io import BytesIO

# OpenAI API Key
openai.api_key = "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"

# Lingvanex API Key and Endpoint
lingvanex_api_key = "a_YqXNPOh2XCBVekWNzoNFuKtUnuoWN26LMxDHFabKDst6O9KlHC9QqNjjeDLxADXYqVb2JiXzUw3i8aCx"
lingvanex_url = "https://api-b2b.backenster.com/b1/api/v3/translate"

# Function to translate text using Lingvanex API
def translate_lingvanex(text, from_lang='mn', to_lang='en'):
    headers = {
        'Authorization': f'Bearer {lingvanex_api_key}',
        'Content-Type': 'application/json'
    }
    payload = {
        'from': from_lang,
        'to': to_lang,
        'text': text
    }
    response = requests.post(lingvanex_url, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        translated_text = result.get('result', None)
        return translated_text
    else:
        print(f"Translation failed. Status Code: {response.status_code}")
        print(f"Error: {response.text}")
        return None

# Function to display styles and let the user choose
def choose_style():
    styles = {
        1: "Фотореалист",
        2: "Дижитал урлаг",
        3: "Хар зураг",
        4: "Анимэ",
        5: "Тосон зураг"
    }
    print("\nЗургийнхаа хэв маягийг сонгоно уу:")
    for key, value in styles.items():
        print(f"{key}. {value}")

    while True:
        try:
            choice = int(input("Сонгосон загварын дугаараа оруулна уу (1-5): "))
            if choice in styles:
                return styles[choice]
            else:
                print("Буруу сонголт. 1-ээс 5 хүртэлх тоог сонгоно уу.")
        except ValueError:
            print("Буруу оролт. Дугаар оруулна уу.")

# Function to generate the image via OpenAI's DALL·E 3 API
def generate_image(prompt, style):
    translated_prompt = translate_lingvanex(prompt)

    # Combine the translated prompt with the chosen style
    full_prompt = f"{translated_prompt}, {style}, highly detailed, HD"

    print("\nGenerating your image, please wait...")
    try:
        # Call OpenAI's DALL·E 3 API
        response = openai.images.generate(
            model="dall-e-3",  # Use the DALL·E 3 model
            prompt=full_prompt,
            size="1024x1024",
            n=1  # Number of images
        )

        # Extract the image URL
        image_url = response.data[0].url
        print(f"\nImage successfully generated! Image URL: {image_url}")

        # Display and save the image
        display_image(image_url)

    except Exception as e:
        print(f"Error generating image: {e}")

# Function to display and save the image using the URL
def display_image(image_url):
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            img.show()
            img.save("generated_image.png")
            print("Image saved as 'generated_image.png'")
        else:
            print("Failed to download the image.")
    except Exception as e:
        print(f"Error displaying image: {e}")

# Main function
def main():
    while True:
        # Step 1: Choose a style
        chosen_style = choose_style()
        print(f"\nТа сонгосон: {chosen_style}")

        # Step 2: Enter a prompt
        while True:
            prompt = input("\nЗургаа тайлбарлахын тулд монгол бичвэр оруулах (эсвэл өөр загвар сонгох бол 'солих', гарах бол 'exit' гэж бичнэ үү): ").strip()
            if prompt.lower() == 'exit':
                print("Програмаас гарч байна. Баяртай!")
                return
            elif prompt.lower() == 'солих':
                print("\nШинэ загвар руу шилжиж байна...")
                break  # Break out to choose a new style
            elif not prompt:
                print("Сануулга хоосон байж болохгүй. Дахин оролдоно уу.")
            else:
                generate_image(prompt, chosen_style)

if __name__ == "__main__":
    main()
