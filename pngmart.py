import requests
from bs4 import BeautifulSoup

# Get sitemap url
url = "https://www.pngmart.com/sitemap.xml/"
respone = requests.get(url)
xml = respone.text
soup = BeautifulSoup(xml, "lxml")
sitemap = soup.find_all("loc")
image_count = 0
urls = []

# Loop to get main sitemap url 
for loc in sitemap:
    if "post_tag" in loc.text or "page" in loc.text or "category" in loc.text:
        break

    else:
        urls.append(loc.text)

# Test the code only download 2 image       
#urls = urls [1:2]

# Loop to get image page url 
for url in urls:
    respone = requests.get(url)
    xml = respone.text
    soup = BeautifulSoup(xml, "lxml")
    images_url = soup.find_all("loc")
    images_url = images_url [0:2]

    # Loop to get png url 
    for image_url in images_url:
        respone = requests.get(image_url.text)
        xml = respone.text
        soup = BeautifulSoup(xml, "html.parser")
        png_url = soup.find("a",{"class" : "download"})["href"]
        print (png_url)

        # Count downloaded image
        image_count += 1

        # get image as request
        image = requests.get(png_url)

        # Get titile for images
        image_titel = image_url.text.split('/')[-1] + '-' + png_url.split('/')[-1]

        # write image content to drive
        with open ("downloaded_png/" + image_titel, "wb") as file:
            file.write(image.content)

print (f"Total Image Downloaded : {image_count}")