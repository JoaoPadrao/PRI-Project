import pandas as pd
import wikipediaapi
import requests
from bs4 import BeautifulSoup

# ---------------------- WIKIPEDIA API ----------------------

wiki_wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent='ProjectName/1.0 (email@example.com)'
)

# Search the description with the API of Wikipedia
def get_battle_description_wikipedia(battle_name):
    # Search for the battle name with "Battle of" prefix
    search_name = f"Battle of {battle_name}"
    page = wiki_wiki.page(search_name)
    if page.exists():
        # Split the summary into paragraphs
        paragraphs = page.summary.split('\n')
        # Return the first paragraph
        return paragraphs[0] if paragraphs else "No description available"
    else:
        return "No description available"


# ---------------------- 10000BATTLES API ----------------------

def get_battle_list():
    url = "https://www.10000battles.com/battles2.php?bat=6"  # URL example
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the dropdown list
        dropdown = soup.find('select', {'name': 'menus'}) 
        options = dropdown.find_all('option')
        
        # Create a dictionary with the battle names and their respective IDs
        battle_names = {option.text.strip(): option['value'] for option in options if 'value' in option.attrs and option['value']}
        return battle_names
    else:
        return {}


# Format the ID of the dataset to match the website dropdown list
def format_battle_name(battle_name):
    for i, char in enumerate(battle_name):
        if char.isdigit():  # Find the first digit
            return f"{battle_name[:i].strip()}, {battle_name[i:].strip()}"
    return battle_name

# Get the URL of the battle from the list
def get_battle_url_from_list(battle_name, battle_list):
    formatted_name = format_battle_name(battle_name)
    for battle, url in battle_list.items():
        if formatted_name in battle:
            return url
    return None

# Get the description from the 10000battles website
def get_battle_description_10000battles(battle_url):
    url = f"https://www.10000battles.com/{battle_url}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the description
        description = soup.find('div', class_='inf_r').text.strip()
        
        # Replace newlines with spaces
        description = description.replace('\n', ' ')

        return description if description else "No description found"
    else:
        return "Failed to retrieve page"

# Output the dataset with the descriptions
def output_dataset(df, battle_list):
    def get_combined_description(row):
        description = get_battle_description_wikipedia(row['Battle'])
        if description == "No description available":
            battle_url = get_battle_url_from_list(row['ID'], battle_list)
            if battle_url:
                return get_battle_description_10000battles(battle_url)
        return description
    
    df['Description'] = df.apply(get_combined_description, axis=1)
    return df

df = pd.read_csv("data/cleaned_data.csv")

battle_list = get_battle_list()

df = output_dataset(df, battle_list)

df.to_csv("test_dataset.csv", index=False)