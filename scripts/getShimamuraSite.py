import requests
import os
import time

# Create the html_data directory if it doesn't exist
if not os.path.exists("html_data"):
    os.makedirs("html_data")

# Loop through steps from 1 to 110
for step in range(1, 111):
    url = f"https://www.shimamura.gr.jp/shop/list/?q=1&step={step}"

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0",
    }

    response = requests.get(url, headers=headers)

    # Save the response content to a file in the html_data directory
    filename = f"html_data/step_{step}.html"
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(response.text)

    print(f"Step {step} data saved to {filename}")

    # 1-minute pause between requests
    time.sleep(60)
