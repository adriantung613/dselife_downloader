import requests
import os
from bs4 import BeautifulSoup


def create_directory(Directory_list_path):
    for index, _ in enumerate(Directory_list_path):
        Path = "/".join(Directory_list_path[:index + 1])
        if not os.path.isdir(Path):
            os.mkdir(Path)
            print(f"{Path} directory created")


def extract_all_links(site):
    html = requests.get(site).text
    soup = BeautifulSoup(html, 'html.parser').find_all('a')
    Links = [link.get('href') for link in soup]

    Past_paper_links = []
    for Link in Links:
        if Link is None:
            continue

        if len(Link.split("/")) >= 2:
            if Link.split("/")[1] == "static":
                Past_paper_links += [Link]

    return Past_paper_links


homepage = input("Please input the link of the homepage: ")
print()
past_paper_links = extract_all_links(homepage)   # change this line

for progress, past_paper_path in enumerate(past_paper_links):
    print(f"progress: {progress}/{len(past_paper_links)}")

    past_paper_path = "/".join(past_paper_path.split("/")[1:])
    url = f"https://dse.life/{past_paper_path}"

    response = None
    if not os.path.isfile(past_paper_path):
        print(f"extracting from {url}")

        for i in range(15):
            try:
                response = requests.get(url, timeout=1)
                break
            except:
                print("request failed")

        if response is None and requests.get("https://www.google.com/", timeout=1) is None:
            raise "connection error"

        print("request success")

        directory_list_path = past_paper_path.split("/")[:-1]
        create_directory(directory_list_path)

        with open(past_paper_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=256):
                f.write(chunk)

        print(f"download success")

    else:
        print(f"{url} is already existed")

    print()
