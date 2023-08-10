import requests from bs4 import BeautifulSoup
import feedgenerator
from config import NAS_LITERATURE_LOC

URL = "https://www.automl.org/automl/literature-on-neural-architecture-search/"

response = requests.get(URL)
soup = BeautifulSoup(response.content, 'html.parser')

# Initialize feed
feed = feedgenerator.Rss201rev2Feed(
    title="NAS Literature"
    link=URL,
    description="New NAS literature from automl.org",
    language="en"
)

# Find all publications
publications = soup.find_all('div', class_='tp_publication')

for pub in publications:
    # Get the necessary details from the publication div
    number = pub.find('div', class_='tp_pub_number').text.strip()
    authors = pub.find('p', class_='tp_pub_author').text.strip()
    title = pub.find('p', class_='tp_pub_title').text.strip()
    link_div = pub.find('a', class_='tp_pub_list')
    
    if link_div:
        link = link_div['href']
    else:
        link = URL  # f no link is found, use the main URL

    # print(f"""
    # {number} {title}
    # {link}
    # {authors}""")
    # exit()
    # Add each entry to the feed
    feed.add_item(
        title=f"[{number}] {title}",
        link=link,
        description=f"Authors: {authors}",
    )

# Save the feed to an XML file
with open(NAS_LITERATURE_LOC, "w") as f:
    feed.write(f, 'utf-8')

