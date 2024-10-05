import pandas as pd
import wikipediaapi

# Initialize Wikipedia API
wiki_wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent='ProjectName/1.0 (email@example.com)'
)

def get_battle_description(battle_name):
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

df = pd.read_csv("data/cleaned_data.csv")

# Add a new column with the battle description
df['Description'] = df['Battle'].apply(get_battle_description)  

df.to_csv("output_dataset.csv", index=False)
