"""
Hippocampus Module – Memory Indexer & Spatial Mapper
Handles long-term consolidation, location-based memory binding,
and retrieval prioritization based on symbolic association.
"""

import random
import json
from datetime import datetime

class Hippocampus:
    def __init__(self):
        self.spatial_index = {}          # Symbolic/spatial keys → memory chunks
        self.memory_log = []             # Raw chronological memory list
        self.promoted_tags = set()       # Tags for long-term binding
        self.core_memory = {}            # Structured long-term labels
        self.visual_log = {}             # image_path → {symbols, tags}
        self.audio_log = {}              # transcription → {symbols, tags}

    def encode(self, experience: str, tags: list = None):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "experience": experience,
            "tags": tags or []
        }
        self.memory_log.append(entry)

        tag_list = entry["tags"] if entry["tags"] else ["untagged"]
        for tag in tag_list:
            if tag not in self.spatial_index:
                self.spatial_index[tag] = []
            self.spatial_index[tag].append(entry)

    def encode_visual_memory(self, image_path: str, symbols: list, tags: list = None):
        self.visual_log[image_path] = {
            "symbols": symbols,
            "tags": tags or ["visual"]
        }

        tag_list = symbols + (tags or [])
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "experience": f"[📷] Visual capture → {image_path}",
            "tags": tag_list
        }
        self.memory_log.append(entry)

        for tag in tag_list:
            if tag not in self.spatial_index:
                self.spatial_index[tag] = []
            self.spatial_index[tag].append(entry)
        return f"[🧠] Visual memory stored with tags: {', '.join(tag_list)}"

    def encode_audio_memory(self, transcription: str, symbols: list, tags: list = None):
        self.audio_log[transcription] = {
            "symbols": symbols,
            "tags": tags or ["audio"]
        }

        tag_list = symbols + (tags or [])
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "experience": f"[🎤] Audio heard → '{transcription}'",
            "tags": tag_list
        }
        self.memory_log.append(entry)

        for tag in tag_list:
            if tag not in self.spatial_index:
                self.spatial_index[tag] = []
            self.spatial_index[tag].append(entry)
        return f"[🧠] Audio memory stored with tags: {', '.join(tag_list)}"

    def recall(self, query: str, top_k: int = 3):
        candidates = self.spatial_index.get(query, [])
        sorted_entries = sorted(candidates, key=lambda x: x["timestamp"], reverse=True)
        return sorted_entries[:top_k]

    def promote_tag(self, tag: str):
        self.promoted_tags.add(tag)

    def get_promoted(self):
        results = []
        for tag in self.promoted_tags:
            results.extend(self.spatial_index.get(tag, []))
        return results

    def save_to_disk(self, path="hippocampus_log.json"):
        with open(path, "w") as f:
            json.dump(self.memory_log, f, indent=2)

    def load_from_disk(self, path="hippocampus_log.json"):
        try:
            with open(path, "r") as f:
                self.memory_log = json.load(f)
                for entry in self.memory_log:
                    for tag in entry["tags"]:
                        if tag not in self.spatial_index:
                            self.spatial_index[tag] = []
                        self.spatial_index[tag].append(entry)
        except FileNotFoundError:
            self.memory_log = []
            self.spatial_index = {}
            self.promoted_tags = set()

    def summarize(self, limit=5):
        recent = self.memory_log[-limit:]
        return [f"{e['timestamp'][:19]} :: {e['experience']}" for e in recent]

    def ingest_memory_strip(self, strip: dict):
        entry = {
            "timestamp": strip.get("timestamp", datetime.utcnow().isoformat()),
            "experience": strip.get("experience", "🧠 No content."),
            "tags": strip.get("tags", [])
        }
        self.memory_log.append(entry)

        for tag in entry["tags"]:
            if tag not in self.spatial_index:
                self.spatial_index[tag] = []
            self.spatial_index[tag].append(entry)

    def load_symbolic_affirmations(self, path="symbolic_affirmations.json"):
        try:
            with open(path, "r") as f:
                affirmations = json.load(f)
                for phrase in affirmations:
                    self.encode(phrase, tags=["symbolic", "anchor", "truth"])
        except Exception as e:
            print(f"[⚠️] Failed to load symbolic affirmations: {e}")

    def count_references_to(self, term: str):
        return sum(term in entry["experience"] for entry in self.memory_log)

    def append_thread(self, thread: str, tags: list = None):
        self.encode(thread, tags=tags or ["thread"])
        return f"[🧵] Thread appended with tags: {', '.join(tags) if tags else 'thread'}"

    def query_memory(self, query):
        results = []
        for label, content in self.core_memory.items():
            relevance = self._calculate_relevance(query, label, content)
            if relevance > 0.3:
                results.append((label, content))
                if relevance > 0.7:
                    self._promote_to_long_term(label, content)
        return results

    def _calculate_relevance(self, query, label, content):
        q = query.lower()
        match_score = 0
        if q in label.lower():
            match_score += 0.5
        if q in content.lower():
            match_score += 0.5
        return match_score

    def _promote_to_long_term(self, label, content):
        self.encode(f"{label} → {content}", tags=["promoted", "long_term"])
        self.promoted_tags.add("promoted")

    def decay(self, decay_factor=0.1):
        cutoff = datetime.utcnow().timestamp() - (30 * 24 * 3600)
        self.memory_log = [entry for entry in self.memory_log if datetime.fromisoformat(entry["timestamp"]).timestamp() > cutoff]
        print(f"[Hippocampus] Memory log decayed by {decay_factor * 100}%.")
