import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import RobertaModel, RobertaTokenizer

class Roberta_Model(nn.Module):
    def __init__(self):
        super(Roberta_Model, self).__init__()
        self.roberta_model = RobertaModel.from_pretrained("roberta-base") # Import pretrained model (Roberta)
        self.pre_classifier = nn.Linear(768, 50) # Default hidden size for each tensor in roberta is 768
        self.dropout = nn.Dropout(0.3) # Randomly dropout 30% of the data to prevent overfitting
        self.classifier = nn.Linear(50, 2) # Output positive, negative 

    def forward(self, input_ids, attention_mask, token_type_ids):
        raw_output = self.roberta_model(input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)
        pooler = raw_output["pooler_output"] # Shape is [batch_size, 768], "pooler output" means output of [CLS] token
        pooler = self.pre_classifier(pooler) 
        pooler = nn.ReLU()(pooler) # Activation function RELU
        pooler = self.dropout(pooler)
        output = self.classifier(pooler) # Shape is [batch_size, 3]
        return output