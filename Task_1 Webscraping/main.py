import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


print("Connecting to website...")

url = "https://books.toscrape.com/"

response = requests.get(url)

if response.status_code == 200:
    print("Website Loaded Successfully!")
    print("Status Code :", response.status_code)
else:
    print("Failed to load website.")
    exit()

print("Scraping Data from Website...\n")

book_data = []
total_pages = 50

for page in range(1, total_pages + 1):

    page_url = f"https://books.toscrape.com/catalogue/page-{page}.html"

    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.find_all("article", class_="product_pod")

    for book in books:

        title = book.h3.a["title"]

        price = (
            book.find("p", class_="price_color")
            .text.replace("Â", "")
            .replace("£", "")
        )

        rating = book.find("p", class_="star-rating")["class"][1]

        availability = (
            book.find("p", class_="instock availability")
            .text.strip()
        )

        book_data.append({
            "Title": title,
            "Price": float(price),
            "Rating": rating,
            "Availability": availability
        })

print("Data Scraped Successfully!")

df = pd.DataFrame(book_data)

print("\nTotal Pages Scraped :", total_pages)
print("Total Books Scraped :", len(df))
print("Dataset Created Successfully!")

print("\nPreview of Dataset:")
print(df.head())

print("\nDataset Shape :", df.shape)

print("\nColumns:")
print(df.columns.tolist())
print("\nData Types:")
print(df.dtypes)

df.to_csv("books.csv", index=False, encoding="utf-8-sig")

print("\nCSV File Saved Successfully!")
print("File Name : books.csv")

