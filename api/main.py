from source.game_search_system_final.game_search import GameSearchSystem

game_search = GameSearchSystem()

query = "action adventure game"
results = game_search.search(query, top_k=10)

print(results)
