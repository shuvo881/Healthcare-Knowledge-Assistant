import os
from sentence_transformers import SentenceTransformer
from langdetect import detect
import faiss
import numpy as np
import json
from typing import List, Dict
from .translator import TranslatorAdapter

class MultilingualRAG:
    def __init__(self, embedding_dim=384, index_path=r"data\faiss_index.faiss", store_path=r"data\doc_store.json"):
        self.embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.translator = TranslatorAdapter()
        
        self.embedding_dim = embedding_dim
        self.index_path = index_path
        self.store_path = store_path

        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.store_path), exist_ok=True)

        # Load or initialize FAISS index
        try:
            self.index = faiss.read_index(self.index_path)
            print(f"Loaded FAISS index from {self.index_path}")
        except:
            self.index = faiss.IndexFlatIP(self.embedding_dim)
            print("Initialized new FAISS index")
        
        # Load or initialize document store
        try:
            with open(self.store_path, 'r', encoding='utf-8') as f:
                self.doc_store = json.load(f)
            print(f"Loaded document store from {self.store_path}")
        except:
            self.doc_store = {}
            print("Initialized new document store")

    def save_local(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.store_path, 'w', encoding='utf-8') as f:
            json.dump(self.doc_store, f, ensure_ascii=False, indent=2)
        print("Saved FAISS index and document store locally")

    def _chunk_text(self, text: str, chunk_size=500, overlap=50) -> List[str]:
        """
        Chunk text into overlapping segments
        """
        chunks = []
        start = 0
        text_len = len(text)
        while start < text_len:
            end = min(start + chunk_size, text_len)
            chunk = text[start:end]
            chunks.append(chunk)
            start += chunk_size - overlap
        return chunks

    def add_txt_files(self, file_paths: List[str], chunk_size=500, overlap=50):
        """
        Load .txt files, chunk, and add to FAISS index
        """
        embeddings = []
        new_doc_ids = []

        for path in file_paths:
            if not os.path.exists(path) or not path.endswith(".txt"):
                print(f"Skipping invalid file: {path}")
                continue
            
            filename = os.path.basename(path)
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()

            chunks = self._chunk_text(text, chunk_size, overlap)
            
            for i, chunk in enumerate(chunks):
                doc_id = f"{filename}_{i}"
                metadata = {
                    "filename": filename,
                    "path": path
                }

                # Detect language
                try:
                    lang = detect(chunk)
                    metadata['language'] = lang
                    metadata['original_language'] = lang
                except:
                    metadata['language'] = 'en'
                    metadata['original_language'] = 'en'

                embedding = self.embedding_model.encode(chunk, convert_to_numpy=True)
                embedding = embedding / np.linalg.norm(embedding)
                embeddings.append(embedding)

                self.doc_store[doc_id] = {
                    'content': chunk,
                    'metadata': metadata
                }
                new_doc_ids.append(doc_id)

        if embeddings:
            embeddings_np = np.vstack(embeddings).astype('float32')
            self.index.add(embeddings_np)
            self.save_local()
            print(f"Added {len(new_doc_ids)} text chunks to FAISS and saved locally")
        else:
            print("No valid chunks to add.")

    def query(self, query_text: str, n_results: int = 5, target_language: str = None) -> Dict:
        query_lang = detect(query_text)
        if target_language is None:
            target_language = query_lang
        
        query_embedding = self.embedding_model.encode(query_text, convert_to_numpy=True)
        query_embedding = query_embedding / np.linalg.norm(query_embedding)
        query_embedding = np.expand_dims(query_embedding.astype('float32'), axis=0)
        
        distances, indices = self.index.search(query_embedding, n_results)
        
        results = []
        doc_ids_list = list(self.doc_store.keys())
        
        for idx, dist in zip(indices[0], distances[0]):
            doc_id = doc_ids_list[idx]
            doc_info = self.doc_store[doc_id]
            content = doc_info['content']
            metadata = doc_info['metadata']
            
            translated_content = content
            if metadata['language'] != target_language:
                try:
                    translated_content = self.translator.translate(content, src=metadata['language'], dest=target_language).text
                except:
                    pass
            
            results.append({
                'content': translated_content,
                'original_content': content,
                'similarity_score': float(dist),
                'source_language': metadata['language'],
                'translated': metadata['language'] != target_language,
                'metadata': metadata
            })
        
        return {
            'query': query_text,
            'query_language': query_lang,
            'target_language': target_language,
            'results': results
        }
