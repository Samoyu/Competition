from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import random
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import wget

# Download the font file
wget.download("https://drive.google.com/uc?id=1eGAsTN1HBpJAkeVM57_C7ccp7hbgSz3_&export=download","TaipeiSansTCBeta-Regular.ttf")

def plot_wordcloud(mytitle, seg_list):

    fig, ax = plt.subplots(figsize=(6, 6), dpi=300)  # Create a figure and axes
    colormaps = ['plasma', 'inferno', 'magma', 'viridis', 'cividis', 'twilight', 'tab10']
    random_colormap = random.choice(colormaps)

    wc = WordCloud(
        width=1500,
        height=1500,
        background_color='white',               
        max_words=150,                    
        max_font_size=None,                   
        font_path="TaipeiSansTCBeta-Regular.ttf",
        regexp=r"\w+(?:[-']\w+)*",
        random_state=50,                      
        contour_width=1,  
        contour_color='black',  
        colormap=random_colormap,  
        prefer_horizontal=0.9
        )               

    wc.generate_from_frequencies(seg_list)
    # Add a border to the plot
    border = patches.Rectangle((0, 0), 1500, 1500, linewidth=2, edgecolor='black', facecolor='none')
    ax.add_patch(border)

    # Plot
    plt.axis("off")
    plt.imshow(wc, interpolation="bilinear")
    plt.title(mytitle, fontsize=24, color='#0a9396', pad=4)

    # Convert plot to image
    image_path = "wordcloud.png"
    plt.savefig(image_path, bbox_inches='tight', dpi=700)
    plt.close(fig)
    return image_path