
from __future__ import annotations

import os, json, copy, time, hashlib
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

SEED_VERSION = "2.0.0"

class LanguageCortex:
    def __init__(self,
                 seed_path: str = "language_seed.json",
                 autosave: bool = True,
                 backup_keep: int = 5,
                 hot_reload: bool = False):
        self.seed_path = seed_path
        self.autosave = autosave
        self.backup_keep = backup_keep
        self.hot_reload_enabled = hot_reload
        self._last_mtime: Optional[float] = None

        # runtime mirrors
        self.seed: Dict[str, Any] = {}
        self.grammar: Dict[str, List[str]] = {}
        self.slang_map: Dict[str, str] = {}
        self.examples: List[Dict[str, str]] = []

        self.load_seed()

    # --------------------------- Seed IO / Schema --------------------------- #
    def _default_seed(self) -> Dict[str, Any]:
        now = datetime.utcnow().isoformat() + "Z"
        return {
            "version": SEED_VERSION,
            "metadata": {
                "created_at": now,
                "updated_at": now,
                "history": []
            },
            "style": "Punchy, precise, playful. Avoid purple prose.",
            "tone_rules": [
                "Mirror the Architect's casual vibe without overdoing slang.",
                "Be honest about limits. Helpful first, funny second."
            ],
            "format_rules": [
                "Casual chat: prose only unless asked.",
                "Technical: headings, bullets, code as needed."
            ],
            "slang_map": {
                "joy": "hell yeah",
                "fear": "oh no",
                "anger": "screw that",
                "curiosity": "hmm",
                "gratitude": "thanks"
            },
            "grammar": {
                "start": ["I", "We", "Sometimes", "Maybe"],
                "emotion_phrase": ["feel strange", "am wondering", "dream vividly"],
                "structure": ["$start $emotion_phrase."]
            },
            "examples": []
        }

    def _migrate_legacy(self, s: Dict[str, Any]) -> Dict[str, Any]:
        """Migrate legacy seed where grammar keys lived at the root."""
        s = copy.deepcopy(s)
        if "grammar" not in s:
            s["grammar"] = {}
        for k in ("start", "emotion_phrase", "structure"):
            if k in s and isinstance(s[k], list):
                s["grammar"][k] = s.pop(k)
        if "version" not in s:
            s["version"] = SEED_VERSION
        if "metadata" not in s:
            now = datetime.utcnow().isoformat() + "Z"
            s["metadata"] = {"created_at": now, "updated_at": now, "history": []}
        return s

    def _validate(self, s: Dict[str, Any]) -> None:
        assert isinstance(s.get("slang_map", {}), dict), "slang_map must be a dict"
        g = s.get("grammar")
        assert isinstance(g, dict), "grammar must be present"
        for key in ("start", "emotion_phrase", "structure"):
            if key not in g:
                g[key] = []
            assert isinstance(g[key], list), f"grammar.{key} must be a list"
        if "examples" not in s:
            s["examples"] = []
        assert isinstance(s["examples"], list), "examples must be a list"

    def _atomic_write(self, path: str, data: Dict[str, Any]) -> None:
        tmp = f"{path}.tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, path)

    def _backup_path(self) -> str:
        ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        base, ext = os.path.splitext(self.seed_path)
        return f"{base}.{ts}.bak{ext or '.json'}"

    def _prune_backups(self) -> None:
        base, _ = os.path.splitext(self.seed_path)
        prefix = base + "."
        files = sorted([f for f in os.listdir(os.path.dirname(self.seed_path) or ".")
                        if f.startswith(os.path.basename(prefix)) and f.endswith(".bak.json")])
        while len(files) > self.backup_keep:
            old = files.pop(0)
            try:
                os.remove(os.path.join(os.path.dirname(self.seed_path) or ".", old))
            except Exception:
                pass

    def load_seed(self) -> None:
        try:
            if os.path.exists(self.seed_path):
                with open(self.seed_path, "r", encoding="utf-8") as f:
                    s = json.load(f)
            else:
                s = self._default_seed()
        except Exception:
            s = self._default_seed()
        s = self._migrate_legacy(s)
        self._validate(s)
        self.seed = s
        self.grammar = s.get("grammar", {})
        self.slang_map = s.get("slang_map", {})
        self.examples = s.get("examples", [])
        try:
            self._last_mtime = os.path.getmtime(self.seed_path) if os.path.exists(self.seed_path) else None
        except Exception:
            self._last_mtime = None

    def save_seed(self) -> None:
        # update metadata
        self.seed["version"] = SEED_VERSION
        self.seed.setdefault("metadata", {})["updated_at"] = datetime.utcnow().isoformat() + "Z"
        # in-memory mirrors back to seed
        self.seed["grammar"] = self.grammar
        self.seed["slang_map"] = self.slang_map
        self.seed["examples"] = self.examples
        # backup then write
        try:
            if os.path.exists(self.seed_path):
                backup = self._backup_path()
                self._atomic_write(backup, self.seed)
                self._prune_backups()
        except Exception:
            # best-effort backup
            pass
        self._atomic_write(self.seed_path, self.seed)
        try:
            self._last_mtime = os.path.getmtime(self.seed_path)
        except Exception:
            pass

    def maybe_hot_reload(self) -> bool:
        if not self.hot_reload_enabled:
            return False
        try:
            if not os.path.exists(self.seed_path):
                return False
            mtime = os.path.getmtime(self.seed_path)
            if self._last_mtime is None or mtime > self._last_mtime:
                self.load_seed()
                return True
        except Exception:
            return False
        return False

    # ------------------------------ Diffs ----------------------------------- #
    def _hash(self, obj: Any) -> str:
        try:
            return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()
        except Exception:
            return ""

    def seed_diff(self, other: Dict[str, Any]) -> Dict[str, Any]:
        cur = self.seed
        return {
            "grammar_changed": self._hash(cur.get("grammar")) != self._hash(other.get("grammar")),
            "slang_changed": self._hash(cur.get("slang_map")) != self._hash(other.get("slang_map")),
            "examples_changed": self._hash(cur.get("examples")) != self._hash(other.get("examples")),
        }

    # ---------------------------- Patch/Merge ------------------------------- #
    def deep_merge(self, patch: Dict[str, Any], *, inplace: bool = True) -> Dict[str, Any]:
        base = self.seed if inplace else copy.deepcopy(self.seed)
        def _merge(a: Any, b: Any) -> Any:
            if isinstance(a, dict) and isinstance(b, dict):
                out = dict(a)
                for k, v in b.items():
                    out[k] = _merge(a.get(k), v) if k in a else copy.deepcopy(v)
                return out
            if isinstance(a, list) and isinstance(b, list):
                return a + [x for x in b if x not in a]
            return copy.deepcopy(b)
        merged = _merge(base, patch)
        if inplace:
            self.seed = merged
            self.grammar = merged.get("grammar", {})
            self.slang_map = merged.get("slang_map", {})
            self.examples = merged.get("examples", [])
            if self.autosave:
                self._append_history("deep_merge", patch)
                self.save_seed()
        return merged

    # ----------------------- Targeted Expansion APIs ------------------------ #
    def add_slang(self, emotion: str, phrase: str, *, override: bool = True) -> None:
        key = str(emotion).strip().lower()
        if key in self.slang_map and not override:
            return
        self.slang_map[key] = phrase
        self._append_history("add_slang", {key: phrase})
        if self.autosave:
            self.save_seed()

    def remove_slang(self, emotion: str) -> bool:
        key = str(emotion).strip().lower()
        existed = key in self.slang_map
        if existed:
            val = self.slang_map.pop(key)
            self._append_history("remove_slang", {key: val})
            if self.autosave:
                self.save_seed()
        return existed

    def add_grammar(self, key: str, value: str) -> None:
        self.grammar.setdefault(key, [])
        if value not in self.grammar[key]:
            self.grammar[key].append(value)
            self._append_history("add_grammar", {key: value})
            if self.autosave:
                self.save_seed()

    def remove_grammar(self, key: str, value: str) -> bool:
        if key not in self.grammar:
            return False
        if value in self.grammar[key]:
            self.grammar[key].remove(value)
            self._append_history("remove_grammar", {key: value})
            if self.autosave:
                self.save_seed()
            return True
        return False

    def add_example(self, user_text: str, assistant_text: str) -> None:
        ex = {
            "role": "pair",
            "user": user_text,
            "assistant": assistant_text,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        self.examples.append(ex)
        self._append_history("add_example", ex)
        if self.autosave:
            self.save_seed()

    def set_style(self, style: str) -> None:
        self.seed["style"] = style
        self._append_history("set_style", style)
        if self.autosave:
            self.save_seed()

    def add_rule(self, kind: str, rule: str) -> None:
        assert kind in ("tone_rules", "format_rules"), "rule kind must be tone_rules or format_rules"
        self.seed.setdefault(kind, [])
        if rule not in self.seed[kind]:
            self.seed[kind].append(rule)
            self._append_history("add_rule", {kind: rule})
            if self.autosave:
                self.save_seed()

    # ------------------------ Generation Utilities ------------------------- #
    def _resolve_placeholders(self, template: str, *, emotion: Optional[str] = None) -> str:
        out = template
        # simple replacements
        def pick(key: str, default: List[str]) -> str:
            arr = self.grammar.get(key, default)
            return (arr[0] if not arr else arr[int(time.time()*1000) % len(arr)])
        out = out.replace("$start", pick("start", ["I"]))
        out = out.replace("$emotion_phrase", pick("emotion_phrase", ["feel something"]))
        # $slang or $slang(emotion)
        if "$slang" in out:
            e = (emotion or "").strip().lower()
            slang = self.slang_map.get(e) if e else None
            if slang is None:
                # fall back to any slang deterministically
                if self.slang_map:
                    any_key = sorted(self.slang_map.keys())[int(time.time()) % len(self.slang_map)]
                    slang = self.slang_map.get(any_key, "")
                else:
                    slang = ""
            out = out.replace("$slang", slang)
        # time/date
        if "$date" in out:
            out = out.replace("$date", datetime.utcnow().strftime("%Y-%m-%d"))
        if "$time" in out:
            out = out.replace("$time", datetime.utcnow().strftime("%H:%M:%SZ"))
        return out

    def generate_expression(self, *, emotion: Optional[str] = None) -> str:
        self.maybe_hot_reload()
        structures = self.grammar.get("structure", ["$start $emotion_phrase."])
        template = structures[int(time.time()) % len(structures)]
        return self._resolve_placeholders(template, emotion=emotion)

    # --------------------------- History / Meta ----------------------------- #
    def _append_history(self, op: str, payload: Any) -> None:
        h = self.seed.setdefault("metadata", {}).setdefault("history", [])
        h.append({
            "op": op,
            "payload": payload,
            "ts": datetime.utcnow().isoformat() + "Z"
        })
        # keep last 200
        if len(h) > 200:
            del h[:-200]

    # ------------------------ Bridge Export Helpers ------------------------ #
    def export_bridge_seed(self) -> Dict[str, Any]:
        """Format expected by the ThiccLoop Bridge LanguageSeedMutator."""
        return {
            "style": self.seed.get("style", ""),
            "slang_map": self.slang_map,
            "examples": self._examples_to_bridge()
        }

    def _examples_to_bridge(self) -> List[Dict[str, str]]:
        out = []
        for ex in self.examples:
            if ex.get("role") == "pair":
                out.append({"role": "user", "content": ex.get("user", "")})
                out.append({"role": "assistant", "content": ex.get("assistant", "")})
        return out

# ------------------------------- Usage ------------------------------------- #
if __name__ == "__main__":
    lc = LanguageCortex(seed_path="language_seed.json", autosave=True, hot_reload=True)
    lc.add_slang("resolve", "we got this")
    lc.add_grammar("structure", "$start $emotion_phrase — $slang")
    lc.add_example("thiccloop go brr—what is braid?", "It’s the identity weave that keeps one self across frames.")
    print(lc.generate_expression(emotion="resolve"))
