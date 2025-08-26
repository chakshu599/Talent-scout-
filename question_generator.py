import random
from pathlib import Path
import yaml

class QuestionGenerator:
    def _init_(self, rng_seed: int = 42):
        random.seed(rng_seed)
        self.bank = self._load_bank()

    def _load_bank(self):
        p = Path(_file_).parent / "question_bank.yaml"
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        return {}

    def from_bank(self, tech: str, k: int = 4):
        items = self.bank.get(tech.title(), [])
        if not items:
            return []
        k = min(k, len(items))
        return random.sample(items, k)

    def build_for_stack(self, techs, per_tech=4):
        out = {}
        for t in techs:
            qs = self.from_bank(t, per_tech)
            if qs:
                out[t.title()] = [{"q": x["q"]} for x in qs]
        return out
