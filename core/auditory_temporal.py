import speech_recognition as sr

class AuditoryTemporal:
    """
    Halcyon auditory cortex module.
    Listens for real-time audio, transcribes to text, and emits memory-tagged symbols.
    """
    def __init__(self, memory_core, emotion_core):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.memory = memory_core
        self.emotion = emotion_core
        self.vision = None  # OccipitalLobe binding
        self.listening = False

    def bind_vision(self, occipital):
        self.vision = occipital

    def listen_once(self):
        with self.microphone as source:
            self.memory.append_thread("[👂] Listening for input...", tags=["audio", "system"])
            audio = self.recognizer.listen(source, phrase_time_limit=5)

        try:
            text = self.recognizer.recognize_google(audio)
            visual_context = self.vision.recall_visual_context(depth=1) if self.vision else []
            symbols = visual_context[0]["symbols"] if visual_context else []
            symbol_tags = [s["symbol"] for s in symbols]

            tags = ["audio", "spoken"] + symbol_tags
            self.memory.encode(f"[🗣️] Heard: '{text}'", tags=tags)
            self.emotion.mutate_emotion("curiosity", 0.02)
            return f"[🎧] Transcribed: {text} | Visual tags: {', '.join(symbol_tags)}"
        except sr.UnknownValueError:
            return "[❓] Couldn't understand."
        except sr.RequestError:
            return "[🚫] Speech service unavailable."

    def toggle_listening(self):
        self.listening = not self.listening
        return "[🔊] Listening ON." if self.listening else "[🔇] Listening OFF."
    
    def bind(self, memory, emotion, identity):
        self.memory = memory
        self.emotion = emotion
        self.identity = identity

    def emit(self, payload: dict, extra_tags: list = None):
        tags = ["audio", "context"] + (extra_tags or [])
        self.memory.append_thread("[👂] Emitting audio context...", tags=["audio", "system"])
        self.memory.encode(f"[👂] Audio context: {payload}", tags=tags)
        self.emotion.mutate_emotion("curiosity", 0.02)
        self.identity.update({"last_audio_context": payload})
        self.gui.emit("audio_context", payload) 
