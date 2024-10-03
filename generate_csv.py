import pandas as pd

# Your dictionary data
data = {
    'Flavor': ['Fruity', 'Nutty', 'Chocolatey', 'Earthy', 'Citrus', 'Spicy', 'Floral', 'Herbal', 'Smoky', 'Bold'],
    'Roast Level': ['Light', 'Medium', 'Dark', 'Medium', 'Light', 'Dark', 'Light', 'Medium', 'Dark', 'Medium'],
    'Acidity': ['Medium', 'Low', 'High', 'Medium', 'Low', 'High', 'Medium', 'Low', 'High', 'Medium'],
    'Drink Type': ['Drip', 'Espresso', 'Aeropress', 'Pourover', 'Drip', 'Espresso', 'Aeropress', 'Pourover', 'Drip', 'Espresso'],
    'Country': ['Ethiopia', 'Colombia', 'Brazil', 'Kenya', 'Costa Rica', 'Honduras', 'Yemen', 'Peru', 'Guatemala', 'Mexico'],
    'Health Benefit': ['Antioxidant-rich', 'Energy Boost', 'Mood Enhancer', 'Stress Relief', 'Immunity Boost', 'Digestive Aid', 'Anti-inflammatory', 'Focus Improvement', 'Detoxifying', 'Metabolism Boost'],
    'Description': ['Chocolatey', 'Nutty', 'Fruity', 'Earthy', 'Citrusy', 'Spicy', 'Floral', 'Herbal', 'Smoky', 'Bold'],
    'Video URL': [
        'https://example.com/video1', 'https://example.com/video2', 'https://example.com/video3',
        'https://example.com/video4', 'https://example.com/video5', 'https://example.com/video6',
        'https://example.com/video7', 'https://example.com/video8', 'https://example.com/video9', 
        'https://example.com/video10'
    ],
    'Drink Time': ['Morning', 'Afternoon', 'Evening', 'Morning', 'Afternoon', 'Evening', 'Morning', 'Afternoon', 'Evening', 'Morning'],
    'Strength': ['Mild', 'Medium', 'Strong', 'Medium', 'Mild', 'Strong', 'Mild', 'Medium', 'Strong', 'Medium']
}

# # # Convert dictionary to DataFrame
csv2_df = pd.DataFrame(data)

# # Read the first CSV file
# csv1_df = pd.read_csv(r"C:\Users\adams\Downloads\coffee_clean.csv")

# # Merge the DataFrames
# merged_df = pd.concat([csv1_df, csv2_df])

# Save the merged DataFrame to a new CSV file
csv2_df.to_csv('coffee_data.csv', index=False)
import pandas as pd
data=pd.read_csv('coffee_data.csv')
data