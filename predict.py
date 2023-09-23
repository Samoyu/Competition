import torch
from model import Roberta_Model
from transformers import RobertaTokenizer

# Load tokenizer
tokenizer = RobertaTokenizer.from_pretrained('roberta-base', truncation=True, do_lower_case=True)

# Load fine tune model on cpu 
model = Roberta_Model()
model.load_state_dict(torch.load('roberta_model.pth', map_location=torch.device('cpu')))
model.eval()

def predict(google_comment_df):
    comments_grades = []

    for text in google_comment_df['comment']:
        text = str(text)
        text = " ".join(text.split())

        inputs = tokenizer.encode_plus(
                    text,
                    None,
                    add_special_tokens = True, 
                    max_length = 64,
                    padding = "max_length", 
                    truncation = True,
                    return_token_type_ids = True
                )

        ids = inputs['input_ids'] 
        masks = inputs['attention_mask'] 
        token_type_ids = inputs["token_type_ids"]

        ids = torch.tensor(ids, dtype=torch.long).unsqueeze(0)
        masks = torch.tensor(masks, dtype=torch.long).unsqueeze(0)
        token_type_ids = torch.tensor(token_type_ids, dtype=torch.long).unsqueeze(0)


        # Perform sentiment analysis using the model
        with torch.no_grad():
            outputs = model(ids, masks, token_type_ids)
            sentiment_class = torch.argmax(outputs.data, dim=1)
            comments_grades.append(sentiment_class.item())
    
    google_comment_df['grade'] = comments_grades

    google_predict_positive_comment = google_comment_df[google_comment_df['grade'] == 1].reset_index(drop=True)
    google_predict_negative_comment = google_comment_df[google_comment_df['grade'] == 0].reset_index(drop=True)
    google_predict_positive_comment = google_predict_positive_comment.drop('grade', axis=1)
    google_predict_negative_comment = google_predict_negative_comment.drop('grade', axis=1)

    negative_comments_number = len(google_comment_df[google_comment_df['grade'] == 0])
    positive_comments_number = len(google_comment_df[google_comment_df['grade'] == 1])

    return google_comment_df, google_predict_positive_comment, google_predict_negative_comment, positive_comments_number, negative_comments_number