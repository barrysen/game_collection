import json
import os

SCORES_FILE = "high_scores.json"

def load_scores():
    """加载历史最高分数"""
    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, 'r') as f:
                return json.load(f)
        except:
            return {"snake": 0, "tetris": 0, "minesweeper": 0}
    return {"snake": 0, "tetris": 0, "minesweeper": 0}

def save_score(game_name: str, score: int):
    """保存新的最高分数"""
    scores = load_scores()
    if score > scores.get(game_name, 0):
        scores[game_name] = score
        with open(SCORES_FILE, 'w') as f:
            json.dump(scores, f) 