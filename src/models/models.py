from .document_search import HugfaceEmbedder
import pandas as pd
from torch import Tensor

class EmbeddingResult:
    def __init__(self, gte_base: list[Tensor], msmarco_base: list[Tensor]):
        self.gte_base = gte_base
        self.msmarco_base = msmarco_base

    def get_gte_base(self)->list[Tensor]:
        return self.gte_base
    
    def get_msmarco_base(self)->list[Tensor]:
        return self.msmarco_base
    

class Embeddings:
    def __init__(self):
        self.gte_base = HugfaceEmbedder("thenlper/gte-base")
        self.msmarco_base = HugfaceEmbedder("msmarco-distilbert-base-dot-prod-v3")

    def calculate_embeddings(self, text: str)->EmbeddingResult:
        gte_base = self.gte_base.calculate_embeddings(text)
        msmarco_base = self.msmarco_base.calculate_embeddings(text)
        return EmbeddingResult(gte_base, msmarco_base)
