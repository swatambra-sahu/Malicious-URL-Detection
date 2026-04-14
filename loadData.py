import os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

matplotlib.use('TkAgg')

def generate_wordcloud(text_data, title):
    """Helper function to generate and display a word cloud."""
    wordcloud = WordCloud(
        width=1600, 
        height=800, 
        colormap='Paired',
        stopwords=STOPWORDS
    ).generate(text_data)
    
    plt.figure(figsize=(12, 14), facecolor='k')
    plt.title(title, color='white', fontsize=16)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show(block=False)
    plt.pause(2)
    plt.close()

def main():
    dataset_path = 'Dataset/malicious_phish.csv'
    
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset not found at {dataset_path}. Please check the path.")
        return

    # Load dataset
    data = pd.read_csv(dataset_path)
    
    # Print basic info
    print(data.shape)
    print(data.head())
    print(data.tail())
    print(data.info())
    print(data.dtypes)
    print("---")

    # Generate word clouds for each category
    categories = data['type'].unique()
    
    for category in categories:
        print(f"Generating wordcloud for {category}...")
        # Filter urls belonging to the specific category
        subset = data[data['type'] == category]
        
        # Optimize string concatenation
        text = " ".join(subset['url'].astype(str))
        
        # Call the helper function
        generate_wordcloud(text, f"{category.capitalize()} URLs")
        
    print("Finished loading data and generating visualizations.")

if __name__ == "__main__":
    main()
