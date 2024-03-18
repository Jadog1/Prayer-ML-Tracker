from typing import Union
import numpy as np
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
        
    def _cut_text(self, text: str, max_length=None)->str:
        if max_length is None:
            max_length = self.max_length

        if max_length > 0 and len(text) > max_length:
            return text[:max_length] + "..."
        return text

    @abstractmethod
    def get_row_text(self, index : int, max_length : int = None)->str:
        pass

    @abstractmethod
    def get_row_object(self, index : int)->dict:
        pass

class BibleVerseCorpus(Corpus):
    def __init__(self, corpus: pd.DataFrame, text_column: str, max_length: int = 0):
        self.df = corpus
        self.corpus_text = self.df[text_column].tolist()
        self.text_column = text_column
        self.max_length = max_length

    def _get_row_bible_context(self, row: pd.Series)->str:
        return f"{row['Book']} {row['Chapter']}:{row['Verse']}"
        
    def _get_row_object(self, row: pd.Series)->dict:
        result = {
            "text": row[self.text_column],
            "book": row['Book'],
            "chapter": int(row["Chapter"]),
            "verse": int(row["Verse"]),
            "type": "verse"
        }
        return result
        
    def get_row_text(self, index : int, max_length : int = None)->str:
        row = self.df.iloc[index]
        bibleContext = self._get_row_bible_context(row)
        verse = self._cut_text(row[self.text_column], max_length)
        return f"{bibleContext} - {verse}"
    
    def get_row_object(self, index : int)->dict:
        row = self.df.iloc[index]
        return self._get_row_object(row)

class BibleSectionCorpus(Corpus):
    def __init__(self, corpus: pd.DataFrame, text_column: str, max_length: int = 0):
        self.df = corpus
        self.corpus_text = self.df[text_column].tolist()
        self.text_column = text_column
        self.max_length = max_length

    def _get_row_bible_context(self, row: pd.Series)->str:
        return f"{row['Book']} {row['Chapter']}:{row['VerseNumberStart']} - {row['VerseNumberEnd']}"
    
    def _get_row_object(self, row: pd.Series)->dict:
        result = {
            "text": row[self.text_column],
            "book": row['Book'],
            "chapter": int(row["Chapter"]),
            "start_verse": int(row["VerseNumberStart"]),
            "end_verse": int(row["VerseNumberEnd"]),
            "type": "section"
        }
        return result

    def get_row_text(self, index : int, max_length : int = None)->str:
        row = self.df.iloc[index]
        bibleContext = self._get_row_bible_context(row)
        section = self._cut_text(row[self.text_column], max_length)
        return f"{bibleContext} - {section}"
    
    def get_row_object(self, index : int)->dict:
        row = self.df.iloc[index]
        return self._get_row_object(row)
    

class PrayerRequestCorpus(Corpus):
    def __init__(self, corpus: pd.DataFrame, max_length: int = 0):
        self.df = corpus
        self.corpus_text = self.df["prayerRequest"].tolist()
        self.max_length = max_length

    def get_row_text(self, index : int, max_length : int = None)->str:
        row = self.df.iloc[index]
        return row["subject"] + " - " + self._cut_text(row["prayerRequest"], max_length)

class Embedder(ABC):
    def __init__(self, embedder_name: str, postfix: str, cache_results = True):
        self.postfix = postfix
        self.embedder = None
        self.name = None
        self.corpus = None
        self.embedder_name = embedder_name
        self.cache_results = cache_results

    @abstractmethod
    def _file_name(self)->str:
        pass
    
    @abstractmethod
    def _cache_embeddings(self):
        pass
    
    @abstractmethod
    def load(self)->np.ndarray:
        pass

    @abstractmethod
    def calculate_embeddings(self, corpus: Union[list[str], str] = None)->np.ndarray:
        pass

    def set_data(self, name: str, corpus: Corpus):
        self.name = name
        self.corpus = corpus.corpus_text

    def _should_cache(self)->bool:
        return self.name is not None and self.cache_results

class HugfaceEmbedder(Embedder):
    def __init__(self, embedder_name: str, postfix: str = "_embeddings.pkl", cache_results = True):
        super().__init__(embedder_name, postfix, cache_results)
        self.embedder = SentenceTransformer(embedder_name)
        self.embeddings = None

    def _file_name(self)->str:
        return f'{self.name}_embeddings.pkl'

    def _cache_embeddings(self):
        self.embeddings = self.calculate_embeddings()
        if self._should_cache():
            with open(self._file_name(), 'wb+') as file:
                pickle.dump(self.embeddings, file)
        return self.embeddings
    
    def load(self)->list[np.ndarray]:
        if self._should_cache():
            return self._cache_embeddings()
        
        try:
            with open(self._file_name(), 'rb') as file:
                self.embeddings= pickle.load(file)
        except Exception as e:
            self._cache_embeddings()
            print(e)
        return self.embeddings
    
    def calculate_embeddings(self, corpus:Union[list[str], str] = None)->np.ndarray:
        if corpus is None:
            corpus = self.corpus
        isList = type(corpus) is list
        embeddings = self.embedder.encode(corpus, show_progress_bar=isList, convert_to_numpy=True)
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
    
    def get_results(self)->list[dict]:
        results = []
        for score, idx in zip(self.scores, self.indices):
            obj = self.corpus.get_row_object(int(idx))
            obj["score"] = float(score)
            results.append(obj)
        return results


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
    def find_similar(self, query: Union[str, np.ndarray], top_k=5)->TopResults:
        query_embedding = query if isinstance(query, np.ndarray) else self.embedder.calculate_embeddings(query)
        if len(self.embeddings) == 0:
            raise ValueError("No embeddings to compare to") 
        
        cos_scores = util.pytorch_cos_sim(torch.from_numpy(query_embedding), self.embeddings)[0]
        top_results = torch.topk(cos_scores, k=top_k, largest=True)
        
        return TopResults(self.corpus, top_results.indices.tolist(), top_results.values.tolist())
    
class DocumentSearchDotProd(DocumentSearch):
    def find_similar(self, query: Union[str, np.ndarray], top_k=5)->TopResults:
        query_embedding = query if isinstance(query, np.ndarray) else self.embedder.calculate_embeddings(query)
        if len(self.embeddings) == 0:
            raise ValueError("No embeddings to compare to") 

        dot_product = util.dot_score(torch.from_numpy(query_embedding), self.embeddings)[0]
        top_results = torch.topk(dot_product, k=top_k, largest=True)
        
        return TopResults(self.corpus, list(top_results.indices), list(top_results.values))
