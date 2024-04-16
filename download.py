import requests


def download(url):
    response = requests.get(url)
    # print(response.content)

    filename = url.split("/")[-1]
    with open(filename, "wb") as f:
        f.write(response.content)


print(download("https://icatcare.org/app/uploads/2018/07/Thinking-of-getting-a-cat.png"))