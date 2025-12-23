import numpy as np
import pickle
from sentence_transformers import SentenceTransformer


class GameSearchSystem:
    def __init__(self, model_path='./source/game_search_system_final/model', index_path='./source/game_search_system_final/index'):
        self.model = SentenceTransformer(model_path)
        self.game_embeddings = np.load(f'{index_path}/game_embeddings.npy')

        with open(f'{index_path}/id_to_idx.pkl', 'rb') as f:
            id_to_idx = pickle.load(f)

        with open(f'{index_path}/game_names.pkl', 'rb') as f:
            self.game_names = pickle.load(f)

        self.idx_to_id = {idx: game_id for game_id, idx in id_to_idx.items()}

        print(f"Поисковая система загружена: {len(self.game_embeddings)} игр")

    def search(self, query, top_k=10):
        query_embedding = self.model.encode([query])

        query_norm = query_embedding / np.linalg.norm(query_embedding)
        games_norm = self.game_embeddings / np.linalg.norm(self.game_embeddings, axis=1, keepdims=True)

        similarities = np.dot(query_norm, games_norm.T)[0]

        top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []
        for idx in top_indices:
            game_id = self.idx_to_id[idx]
            score = similarities[idx]

            results.append({
                'game_id': game_id,
                'name': self.game_names[game_id],
                'score': float(score),
                'score_percent': int(score * 100)
            })

        return results
