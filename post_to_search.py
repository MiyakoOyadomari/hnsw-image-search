import requests

def post_image_to_search(file_path):
    url = "http://127.0.0.1:8000/search"
    try:
        with open(file_path, "rb") as f:
            response = requests.post(url, files={"file": f})
        print("Response:", response.json())
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    # アップロードしたい画像のパスを指定してください
    file_path = "source/test_tile_1.jpg"
    post_image_to_search(file_path)