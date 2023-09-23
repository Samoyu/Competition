import re

# Remove Emojis
def remove_emojis(text):
    # Remove emojis using regular expressions
    emoji_pattern = re.compile("["
                    u"\U0001F600-\U0001F64F"  # emoticons
                    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                    u"\U0001F680-\U0001F6FF"  # transport & map symbols
                    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                    u"\U00002500-\U00002BEF"  # chinese char
                    u"\U00002702-\U000027B0"
                    u"\U00002702-\U000027B0"
                    u"\U000024C2-\U0001F251"
                    u"\U0001f926-\U0001f937"
                    u"\U00010000-\U0010ffff"
                    u"\u2640-\u2642"
                    u"\u2600-\u2B55"
                    u"\u200d"
                    u"\u23cf"
                    u"\u23e9"
                    u"\u231a"
                    "\ufe0f"  # dingbats
                    "\u3030"
                    "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)


# Remove URL
def remove_urls(text):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub(r'', text)

# Preprocess the comments
def preprocessing(google_comment_df):
    clean_restaurant_comment = []

    for comment in google_comment_df['comment']:
        comment = str(comment)
        remove_emojis(comment)
        remove_urls(comment)
        clean_restaurant_comment.append(comment)

    google_comment_df.loc[:, 'comment'] = clean_restaurant_comment

    return google_comment_df