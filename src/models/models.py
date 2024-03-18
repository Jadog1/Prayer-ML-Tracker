import os

import numpy as np
from .document_search import BibleSectionCorpus, BibleVerseCorpus, DocumentSearchCosSim, DocumentSearchDotProd, HugfaceEmbedder
import pandas as pd
from torch import Tensor
import pathlib
filePath = pathlib.Path(__file__).parent.resolve()

class EmbeddingResult:
    def __init__(self, gte_base: np.ndarray, msmarco_base: np.ndarray):
        self.gte_base = gte_base
        self.msmarco_base = msmarco_base

    def get_gte_base(self)->np.ndarray:
        return self.gte_base
    
    def get_msmarco_base(self)->np.ndarray:
        return self.msmarco_base
    

class Embeddings:
    """
    Class representing embeddings for text data.

    Attributes:
        gte_base (HugfaceEmbedder): Hugging Face embedder for the "thenlper/gte-base" model.
        msmarco_base (HugfaceEmbedder): Hugging Face embedder for the "msmarco-distilbert-base-dot-prod-v3" model.
    """

    def __init__(self):
        self.gte_base = HugfaceEmbedder("thenlper/gte-base")
        self.msmarco_base = HugfaceEmbedder("msmarco-distilbert-base-dot-prod-v3")

    def calculate_embeddings(self, text: str) -> EmbeddingResult:
        """
        Calculates embeddings for the given text.

        Args:
            text (str): The input text to calculate embeddings for.

        Returns:
            EmbeddingResult: An object containing the calculated embeddings.
        """
        gte_base = self.gte_base.calculate_embeddings(text)
        msmarco_base = self.msmarco_base.calculate_embeddings(text)
        return EmbeddingResult(gte_base, msmarco_base)
    
class BibleEmbeddings:
    def __init__(self):
        gteBase = HugfaceEmbedder("thenlper/gte-base", cache_results=False)
        msmarco = HugfaceEmbedder("msmarco-distilbert-base-dot-prod-v3", cache_results=False)
        df_niv = pd.read_csv('src/scraped_data/NIV.csv')
        df_niv_sections = pd.read_csv('src/scraped_data/NIV_sections.csv')
        # cachePath = lambda x: "cache/bibles/niv/"+x
        cachePath = lambda x: os.path.join(filePath, '..', '..', 'cache', 'bibles', 'niv', x)

        self.docVerses = DocumentSearchCosSim(gteBase, cachePath("verses_base"), BibleVerseCorpus(df_niv, "Text"))
        self.docSections = DocumentSearchDotProd(msmarco, cachePath("sections_base"), BibleSectionCorpus(df_niv_sections, "VerseText"))

    def search_verses(self, query_embedding: EmbeddingResult, top_k: int)->list[dict]:
        verses = self.docVerses.find_similar(query_embedding.get_gte_base(), top_k)
        sections = self.docSections.find_similar(query_embedding.get_msmarco_base(), top_k)
        # Combine the results, and select the top ones based on the top scores. 
        # Sections has a max of around 0.65 typically, so anything greater than 0.6 we will want to include
        # as a top. Otherwise, use verses
        results = []
        sectionsIndex = 0
        versesIndex = 0
        for i in range(top_k):
            if sections.scores[i] > 45 and sectionsIndex < 2:
                print(sections.scores[i])
                results.append(sections.get_results()[sectionsIndex])
                sectionsIndex += 1
            else:
                results.append(verses.get_results()[versesIndex])
                versesIndex += 1

        return results

