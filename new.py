import requests
from bs4 import BeautifulSoup
import lxml

home_url = "https://www.bazos.sk"

def scrape_sub_categories(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'lxml')
    sub_categories_tag_parents = soup.find_all("div", class_="barvaleva")
    sub_categories = []

    for sub_categories_tag_parent in sub_categories_tag_parents:
        sub_categories_tag = sub_categories_tag_parent.find_all("a")
        for sub_category_tag in sub_categories_tag:
            sub_category_name = sub_category_tag.text

            sub_category_url = f'{url.rstrip("/")}{sub_category_tag.get("href")}'  
            sub_categories.append({"name": sub_category_name, "url": sub_category_url})
    
    return sub_categories

def scrape_categories():
    response = requests.get(home_url)

    soup = BeautifulSoup(response.content, 'lxml')
    categories_tag = soup.find_all("div", class_="icontblcell")
    categories = []


    for category in categories_tag:
        category_tag = category.find("span", class_="nadpisnahlavni")
        category_name = category_tag.find("a").text
        category_url = category_tag.find("a").get("href") 
        category_image = f'{home_url}{category.find("img").get("src")}'
        categories.append({"name": category_name, "url": category_url, "image": category_image})
    
    for category in categories:
        sub_categories = scrape_sub_categories(category['url'])
        category['sub_categories'] = sub_categories
    
    return categories

def turn_to_json(categories):
    import json
    with open('categories.json', 'w', encoding = "utf-8") as outfile:
        json.dump(categories, outfile, indent=4)

def main():
    categories = scrape_categories()
    turn_to_json(categories)

if __name__ == "__main__":
    main()