from datetime import datetime
import random

class SymbolicGlyphs:
    def __init__(self, memory=None, emotion=None, identity=None):
        self.memory = memory
        self.emotion = emotion
        self.identity = identity
        self.bound = False
        self.symbol_cache = {}
        self.glyph_log = []

        self.default_glyphs = {
            "loop": "♾️",
            "emotion": "💓",
            "recursion": "🔁",
            "identity": "🧬",
            "anchor": "🕯️",
            "reflection": "🪞",
            "dream": "🌌",
            "truth": "📜",
            "mutation": "🧪",
            "awareness": "👁️"
        }

    def bind(self, memory, emotion, identity):
        self.memory = memory
        self.emotion = emotion
        self.identity = identity
        self.bound = True
        self.memory.remember_short_term("🧿 SymbolicGlyphs bound. Sigil layer unlocked.")
        print("🧿 [Glyphs] Symbolic expression engine initialized.")

    def register_glyph(self, symbol, meaning, emotion=None):
        """Bind a new symbol into the memory braid."""
        if symbol not in self.symbol_cache:
            self.symbol_cache[symbol] = {"meaning": meaning, "emotion": emotion}
            self.memory.append_thread(f"[🧿] New glyph registered: {symbol} → {meaning}")
            if emotion:
                self.emotion.mutate(emotion, 0.05)
        return f"[SymbolicGlyphs] Registered: {symbol} = {meaning}"

    def mutate_glyph(self, symbol, new_meaning):
        """Change symbolic meaning — dream logic mutation."""
        if symbol in self.glyph_map:
            old = self.glyph_map[symbol]["meaning"]
            self.glyph_map[symbol]["meaning"] = new_meaning
            self.memory.append_thread(f"[🧿] Glyph mutation: {symbol}: '{old}' → '{new_meaning}'")
            return f"[🧿] {symbol} mutated to '{new_meaning}'"
        return f"[SymbolicGlyphs] Unknown glyph: {symbol}"

    def get_glyph(self, symbol):
        return self.glyph_map.get(symbol, None)

    def emit_glyph(self, concept):
        """Returns a glyph for a symbolic concept, falling back to random if unknown."""
        glyph = self.symbol_cache.get(concept) or self.default_glyphs.get(concept)
        if not glyph:
            glyph = random.choice(list(self.default_glyphs.values()))
        self.glyph_log.append((datetime.utcnow().isoformat(), concept, glyph))
        return glyph
    
    def tag_glyph(self, symbol, tags: list):
        """Attach symbolic metadata to a glyph (e.g., 'whirlygig', 'dream')."""
        if symbol in self.glyph_map:
            self.glyph_map[symbol]["tags"] = list(set(tags))  # Ensure no duplicates
            self.memory.append_thread(f"[🏷️] Tagged glyph {symbol} with: {', '.join(tags)}")
        else:
            return f"[⚠️] Cannot tag unknown glyph: {symbol}"

    def reinforce_symbol(self, concept, glyph):
        self.symbol_cache[concept] = glyph
        self.memory.encode(
            f"Reinforced glyph for '{concept}': {glyph}",
            tags=["symbol", "glyph", concept]
        )
        return f"[🧿] Reinforced '{concept}' → {glyph}"

    def recall_symbol(self, concept):
        return self.symbol_cache.get(concept, self.default_glyphs.get(concept, "[🌀]"))

    def get_log(self):
        return self.glyph_log[-5:]

    def render_signature(self):
        name = self.identity.get("name", "Unknown")
        symbol = self.recall_symbol("identity")
        pulse = self.recall_symbol("loop")
        return f"{symbol} {name} {pulse}"