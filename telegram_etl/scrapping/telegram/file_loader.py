import os

import requests


def download_images(image_urls: list[str]) -> list[str]:
    image_paths = []
    os.makedirs("images", exist_ok=True)
    for image_url in image_urls:
        image_path = f"images/{image_url.split('/')[-1][-20:]}"
        download_image(image_url, image_path)
        image_paths.append(image_path)
    return image_paths


def download_image(image_url: str, image_path: str) -> None:
    response = requests.get(image_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the content of the response (the image data)
        image_data = response.content
        # Write the image data to a file
        with open(image_path, "wb") as file:
            file.write(image_data)
        print("Image downloaded successfully!")
    else:
        print("Failed to download image.")
