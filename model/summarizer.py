from transformers import BartTokenizer, BartForConditionalGeneration, pipeline
import torch
import sentence_transformers

class Summarizer_Base:
    def __init__(self):
        self.tokenizer = BartTokenizer.from_pretrained("sshleifer/distilbart-xsum-12-1", cache_dir='./cache')
        self.model = BartForConditionalGeneration.from_pretrained("sshleifer/distilbart-xsum-12-1", cache_dir='./cache')
    def encode(self, text):
        pass
    def decode(self, text):
        pass
    def summarize(self, text):
        pass

class Summarizer(Summarizer_Base):
    def __init__(self):
        super().__init__()
        self.summarizer = pipeline("summarization", model=self.model, tokenizer=self.tokenizer)

    def summarize(self, text):
        inputs = self.tokenizer(text, return_tensors="pt")
        return self.summarizer(text, min_length = 15, max_length=50)
