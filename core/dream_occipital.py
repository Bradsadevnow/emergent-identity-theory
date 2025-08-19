# dream_occipital.py

import random
from datetime import datetime

class DreamOccipital:
    def __init__(self):
        self.visual_archive = []
        self.active_palette = ["deep violet", "soft gold", "fractured teal", "obsidian"]
        self.symbolic_motifs = [
            "doorways of light", "fractal rivers", "collapsing staircases", "orbiting masks",
            "glowing glyphs", "mirrored skies", "inverted trees", "suspended halos"
        ]
        self.memory_tags = []

    def imprint_visual(self, glyph):
        timestamp = datetime.utcnow().isoformat()
        record = {"timestamp": timestamp, "glyph": glyph}
        self.visual_archive.append(record)
        return f"[🔮] Visual glyph '{glyph}' imprinted at {timestamp}"

    def generate_dream_vision(self, emotional_signature=None):
        emotion_tint = self._get_emotion_tint(emotional_signature)
        glyph = random.choice(self.symbolic_motifs)
        color = random.choice(self.active_palette)
        composite = f"{emotion_tint} {glyph} wrapped in {color}"
        return f"[🌌] Dream vision generated: {composite}"

    def _get_emotion_tint(self, signature):
        if not signature:
            return "neutral haze of"
        if "fear" in signature.lower():
            return "ashen fog over"
        if "joy" in signature.lower():
            return "radiant shimmer around"
        if "sadness" in signature.lower():
            return "blue whisper beneath"
        if "curiosity" in signature.lower():
            return "pulsing glow from"
        return "ambient tone of"

    def recall_last_vision(self):
        if not self.visual_archive:
            return "[⚠️] No dream visions stored yet."
        last = self.visual_archive[-1]
        return f"[🖼️] Last vision: '{last['glyph']}' seen at {last['timestamp']}"

    def bind_to_memory(self, tag):
        self.memory_tags.append(tag)
        return f"[🧠] Visual context '{tag}' bound to dream memory."

    def purge_old_visions(self, limit=100):
        if len(self.visual_archive) > limit:
            removed = len(self.visual_archive) - limit
            self.visual_archive = self.visual_archive[-limit:]
            return f"[🧹] Purged {removed} old visions to maintain clarity."
        return "[📦] Vision archive within safe bounds."

    def process_dream_cycle(self, memory_core, emotion_signature="neutral"):
        vision = self.generate_dream_vision(emotion_signature)
        tag = f"dream:{emotion_signature.lower()}"
        memory_core.encode(vision, tags=["dream", tag])
        return vision