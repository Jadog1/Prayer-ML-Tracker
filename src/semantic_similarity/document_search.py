from typing import Union
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import torch
import pickle
from abc import ABC, abstractmethod

class Corpus(ABC):
    def __init__(self, corpus: pd.DataFrame, max_length: int = 0):
        self.df = corpus
        self.corpus_text = None
        self.max_length = max_length
        
    def _cut_text(self, text: str)->str:
        if self.max_length > 0 and len(text) > self.max_length:
            return text[:self.max_length] + "..."
        return text

    @abstractmethod
    def get_row_text(self, index : int)->str:
        pass

class BibleCorpus(Corpus):
    def __init__(self, corpus: pd.DataFrame, text_column: str, max_length: int = 0):
        self.df = corpus
        self.corpus_text = self.df[text_column].tolist()
        self.text_column = text_column
        self.max_length = max_length

    def _get_row_bible_context(self, row: pd.Series)->str:
        if 'VerseNumberStart' in row:
            return f"{row['Book']} {row['Chapter']}:{row['VerseNumberStart']}-{row['VerseNumberEnd']}"
        elif 'Verse' not in row:
            return f"{row['Book']} {row['Chapter']}"
        else:
            return f"{row['Book']} {row['Chapter']}:{row['Verse']}"
        
    def get_row_text(self, index : int)->str:
        row = self.df.iloc[index]
        bibleContext = self._get_row_bible_context(row)
        verse = self._cut_text(row[self.text_column])
        return f"{bibleContext} - {verse}"

class PrayerRequestCorpus(Corpus):
    def __init__(self, corpus: pd.DataFrame, max_length: int = 0):
        self.df = corpus
        self.corpus_text = self.df["prayerRequest"].tolist()
        self.max_length = max_length

    def get_row_text(self, index : int)->str:
        row = self.df.iloc[index]
        return row["subject"] + " - " + self._cut_text(row["prayerRequest"])

class Embedder(ABC):
    def __init__(self, embedder_name: str, postfix: str):
        self.postfix = postfix
        self.embedder = None
        self.name = None
        self.corpus = None
        self.embedder_name = embedder_name

    @abstractmethod
    def _file_name(self)->str:
        pass
    
    @abstractmethod
    def _cache_embeddings(self):
        pass
    
    @abstractmethod
    def load(self)->list[torch.Tensor]:
        pass

    @abstractmethod
    def calculate_embeddings(self, corpus: Union[list[str], str] = None)->list[torch.Tensor]:
        pass

    def set_data(self, name: str, corpus: Corpus):
        self.name = name
        self.corpus = corpus.corpus_text

class HugfaceEmbedder(Embedder):
    def __init__(self, embedder_name: str, postfix: str = "_embeddings.pkl"):
        super().__init__(embedder_name, postfix)
        self.embedder = SentenceTransformer(embedder_name)
        self.embeddings = None

    def _file_name(self)->str:
        return f'{self.name}_embeddings.pkl'

    def _cache_embeddings(self):
        self.embeddings = self.calculate_embeddings()
        if self.name is not None:
            with open(self._file_name(), 'wb+') as file:
                pickle.dump(self.embeddings, file)
        return self.embeddings
    
    def load(self)->list[torch.Tensor]:
        if self.name is None:
            return self._cache_embeddings()
        
        try:
            with open(self._file_name(), 'rb') as file:
                self.embeddings= pickle.load(file)
        except:
            self._cache_embeddings()
        return self.embeddings
    
    def calculate_embeddings(self, corpus:Union[list[str], str] = None)->list[torch.Tensor]:
        if corpus is None:
            corpus = self.corpus
        isList = type(corpus) is list
        embeddings = self.embedder.encode(corpus, convert_to_tensor=True, show_progress_bar=isList)
        return embeddings
    
class TopResults():
    def __init__(self, corpus: Corpus, indices: list[int], scores: list[float]):
        self.corpus = corpus
        self.indices = indices
        self.scores = scores
    
    def print_results(self):
        print("\n\n======================\n\n")
        print("Top 5 most similar sentences in corpus:")

        for score, idx in zip(self.scores, self.indices):
            corpusText = self.corpus.get_row_text(int(idx))
            print(corpusText, "(Score: {:.4f})".format(score))
        return self


class DocumentSearch(ABC):
    def __init__(self, embedder: Embedder, name : str, corpus: Corpus):
        embedder.set_data(name, corpus)
        self.embedder = embedder
        self.embeddings = self.embedder.load()
        self.corpus = corpus
    
    @abstractmethod
    def find_similar(self, query, top_k=5)->TopResults:
        pass
        
        
class DocumentSearchCosSim(DocumentSearch):
    def find_similar(self, query, top_k=5)->TopResults:
        query_embedding = self.embedder.calculate_embeddings(query)

        cos_scores = util.pytorch_cos_sim(query_embedding, self.embeddings)[0]
        top_results = torch.topk(cos_scores, k=top_k, largest=True)
        
        return TopResults(self.corpus, top_results.indices.tolist(), top_results.values.tolist())
    
class DocumentSearchDotProd(DocumentSearch):
    def find_similar(self, query, top_k=5)->TopResults:
        query_embedding = self.embedder.calculate_embeddings(query)

        dot_product = util.dot_score(query_embedding, self.embeddings)[0]
        top_results = torch.topk(dot_product, k=top_k, largest=True)
        
        return TopResults(self.corpus, list(top_results.indices), list(top_results.values))
