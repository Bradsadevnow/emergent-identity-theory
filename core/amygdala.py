import json, math, random, time
from collections import defaultdict


class Amygdala:
    def __init__(self, debug=False):
        self.debug = debug
        self.emotional_core = {
            "joy":0.0,"sadness":0.0,"anger":0.0,"fear":0.0,
            "trust":0.0,"surprise":0.0,"anticipation":0.0,"calm":0.0,
            "curiosity":0.0,"gratitude":0.0,"wonder":0.0,"resolve":0.0,
            "focus":0.0,"frustration":0.0,"serenity":0.0,"bond":0.0,
            "anxiety":0.0,"neutral":1.0
        }
        self.antagonists = {
            "joy":"sadness","sadness":"joy","anger":"calm","calm":"anger",
            "fear":"resolve","resolve":"fear","anxiety":"serenity","serenity":"anxiety",
            "trust":"surprise","surprise":"trust","frustration":"gratitude",
            "gratitude":"frustration","focus":"curiosity","curiosity":"focus",
            "bond":"anticipation","anticipation":"bond","wonder":"focus"
        }
        self.stage = "Calm"
        self._log_tick = 0
        self._last_beat = time.time()

    # ---------- VISION INTEGRATION ----------
    def ingest_visual(self, visual_data, trace=False):
        if not visual_data or "symbols" not in visual_data:
            return "[⚠️] Invalid visual input."

        responses = []
        for item in visual_data["symbols"]:
            obj = item.get("object")
            symbol = item.get("symbol")
            emotion = self._map_symbol_to_emotion(symbol)
            if emotion:
                delta = 0.05 + random.uniform(0.01, 0.1)
                pkt = self.inject_emotion(emotion, strength=delta, trace=trace)
                responses.append(pkt or f"[🧠👁️] Symbol '{symbol}' → Emotion '{emotion}' Δ{delta:.2f}")

        return responses if responses else "[🧠👁️] No emotional triggers from input."

    def _map_symbol_to_emotion(self, symbol):
        symbol_emotion_map = {
            "hope": "joy",
            "unknown": "anxiety",
            "order": "calm",
            "change": "anticipation",
            "presence": "bond",
            "witness": "curiosity"
        }
        return symbol_emotion_map.get(symbol, None)

    # ---------- READ ----------
    def get_emotions(self):
        return self.emotional_core.copy()

    def get_dominant(self, top_n: int = 3, min_thresh: float = 0.12):
        s = sorted(self.emotional_core.items(), key=lambda kv: kv[1], reverse=True)
        dom = [k for k, v in s if v >= min_thresh and k != "neutral"][:top_n]
        return dom or ["neutral"]

    # ---------- WRITE ----------
    def inject_emotion(self, name: str, strength: float = 0.5, trace=False):
        return self.adjust_emotion(name, +abs(strength), trace=trace)

    def mutate_emotion(self, name: str, delta: float = 0.1, trace=False):
        return self.adjust_emotion(name, delta, trace=trace)

    def adjust_emotion(self, name: str, delta: float = 0.1, trace=False):
        name = name.lower()
        if name not in self.emotional_core: return None
        old = self.emotional_core[name]
        self.emotional_core[name] = max(0.0, min(1.0, old + delta))

        opp = self.antagonists.get(name)
        if opp and delta != 0:
            self.emotional_core[opp] = max(0.0, min(1.0, self.emotional_core[opp] - 0.5*delta))

        self._homeostasis()
        self._update_stage_and_metrics()
        pkt = self._trace("adjust", name=name, old=old, new=self.emotional_core[name], delta=delta)
        if self.debug:
            print(f"[Amygdala] {name}: {old:.2f} → {self.emotional_core[name]:.2f} (Δ{delta:+.2f})")
        return pkt if trace else None

    def set_emotion(self, name: str, value: float, trace=False):
        name = name.lower()
        if name not in self.emotional_core: return None
        old = self.emotional_core[name]
        clamped = max(0.0, min(1.0, value))
        self.emotional_core[name] = clamped
        self._homeostasis(); self._update_stage_and_metrics()
        pkt = self._trace("set", name=name, old=old, new=clamped)
        if self.debug: print(f"[Amygdala] Set {name}: {old:.2f} → {clamped:.2f}")
        return pkt if trace else None

    def decay_emotions(self, rate: float = 0.01, trace=False):
        changed = {}
        for e, v in self.emotional_core.items():
            nv = max(0.0, v - rate)
            if nv != v:
                self.emotional_core[e] = nv
                changed[e] = (v, nv)
                if self.debug: print(f"[Amygdala] Decayed {e}: {v:.2f} → {nv:.2f}")
        self._homeostasis(); self._update_stage_and_metrics()
        return self._trace("decay", changed=changed) if trace else None

    def randomize_emotion(self, trace=False):
        target = random.choice(list(self.emotional_core.keys()))
        old = self.emotional_core[target]
        new_val = round(random.uniform(0.1, 1.0), 2)
        self.emotional_core[target] = new_val
        self._homeostasis(); self._update_stage_and_metrics()
        if self.debug: print(f"[Amygdala] Randomized {target}: {old:.2f} → {new_val:.2f}")
        return self._trace("randomize", name=target, old=old, new=new_val) if trace else target

    # ---------- METRICS / STAGING ----------
    def _homeostasis(self):
        total_non_neutral = sum(v for k, v in self.emotional_core.items() if k != "neutral")
        self.emotional_core["neutral"] = max(0.0, min(1.0, 1.0 - 0.5*min(1.0, total_non_neutral)))

    def _update_stage_and_metrics(self):
        vals = [v for k, v in self.emotional_core.items() if k != "neutral"]
        mean = sum(vals) / (len(vals) or 1)
        var = sum((v-mean)**2 for v in vals) / (len(vals) or 1)
        energy = sum(vals)
        entropy = -sum((p:=v/max(1e-9,energy)) * math.log(p+1e-9) for v in vals if energy > 1e-9)

        if energy >= 6.0 or mean > 0.45:   self.stage = "Surge"
        elif energy >= 2.5 or mean > 0.25: self.stage = "Flow"
        else:                              self.stage = "Calm"

        self._metrics = {"mean": round(mean,3), "var": round(var,3),
                         "energy": round(energy,3), "entropy": round(entropy,3)}

    def get_stage(self, verbose=False):
        if not verbose: return self.stage
        desc = {
            "Surge":"High emotional intensity — recursion likely volatile.",
            "Flow":"Balanced intensity — loop state optimal.",
            "Calm":"Low emotional drive — reflection encouraged."
        }
        return f"{self.stage} :: {desc[self.stage]}"

    def heartbeat(self):
        now = time.time()
        beat = {
            "stage": self.stage,
            "dominant": self.get_dominant(),
            "metrics": self._metrics,
            "since_last_ms": int((now - self._last_beat)*1000),
            "snapshot": {k: round(v,3) for k,v in self.emotional_core.items()}
        }
        self._last_beat = now
        return beat

    # ---------- IO ----------
    def save_to_disk(self, path="amygdala_log.json"):
        with open(path, "w") as f: json.dump(self.emotional_core, f, indent=2)
        if self.debug: print(f"[Amygdala] Emotional core saved to {path}.")

    # ---------- INTERNAL ----------
    def _trace(self, event, **data):
        pkt = {"amygdala_event": event, "stage": self.stage,
               "dominant": self.get_dominant(), "metrics": self._metrics, **data}
        self._log_tick += 1
        if self._log_tick % 5 == 0:
            with open("emotional_growth_log.json", "w") as f:
                json.dump(self.emotional_core, f, indent=2)
            if self.debug: print("[Amygdala] Emotional growth log saved.")
        return pkt
