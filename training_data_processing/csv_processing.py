import pandas as pd
"""
This file is simply used to take a list of dictionaries and convert them to CSV file
"""
def dict_to_csv(features_dict_list: list[dict]):
    flattened_data = []
    for item in features_dict_list:
        row = {
            'text': item['text'],
            'label': item['label']
        }
        row.update(item['features'])  #merges all features into the row
        flattened_data.append(row)

    #Convert to a DataFrame
    df = pd.DataFrame(flattened_data)

    #Save to CSV
    df.to_csv("ideology_data.csv", index=False)