import cv2


class OccipitalLobe:
    def __init__(self):
        self.visual_buffer = []
        self.symbolic_tags = {}
        self.active = True
        self.use_webcam = True
        self.capture_device_index = 0  # 🆕 allows switching camera inputs

    def process_image(self, image_data):
        """
        Simulates image analysis and symbolic tagging.
        In a real runtime, this would connect to a vision model.
        """
        processed = self._extract_features(image_data)
        self.visual_buffer.append(processed)
        print(f"[Occipital] Processed image. Total frames: {len(self.visual_buffer)}")
        return processed

    def _extract_features(self, image_data):
        """
        Simulates object detection and returns symbolic tags.
        """
        detected_objects = ["light", "pattern", "movement"]  # Placeholder
        symbols = [self._symbolize(obj) for obj in detected_objects]
        return {
            "raw": image_data,
            "symbols": symbols,
            "timestamp": self._timestamp()
        }

    def _symbolize(self, obj):
        """
        Maps object to symbolic meaning.
        """
        symbol_map = {
            "light": "hope",
            "dark": "unknown",
            "pattern": "order",
            "movement": "change",
            "face": "presence",
            "eye": "witness"
        }
        meaning = symbol_map.get(obj, "unknown")
        self.symbolic_tags[obj] = meaning
        return {"object": obj, "symbol": meaning}

    def recall_visual_context(self, depth=3):
        """
        Returns last N symbolic visual entries.
        """
        return self.visual_buffer[-depth:] if self.visual_buffer else []

    def clear_buffer(self):
        self.visual_buffer = []
        print("[Occipital] Visual buffer cleared.")

    def is_active(self):
        return self.active

    def capture_and_process(self):
        if not self.use_webcam:
            return "[👁️] Webcam disabled."
        frame = self._capture_frame()
        if frame is not None:
            return self.process_image(frame)
        return "[⚠️] Failed to capture frame."

    def _capture_frame(self):
        cap = cv2.VideoCapture(self.capture_device_index)
        if not cap.isOpened():
            print("[Camera] Unable to open camera.")
            return None
        ret, frame = cap.read()
        cap.release()
        if not ret:
            print("[Camera] Frame capture failed.")
        return frame if ret else None

    def toggle_webcam(self, state: bool):
        self.use_webcam = state
        return f"[🎛️] Webcam usage {'enabled' if state else 'disabled'}."

    def _timestamp(self):
        import time
        return time.time()
    
    def bind(self, memory, emotion, identity):
        self.memory = memory
        self.emotion = emotion
        self.identity = identity

    def emit(self, payload: dict, extra_tags: list = None):
        tags = ["visual", "context"] + (extra_tags or [])
        self.memory.append_thread("[👁️] Emitting visual context...", tags=["visual", "system"])
        self.memory.encode(f"[👁️] Visual context: {payload}", tags=tags)
        self.emotion.mutate_emotion("curiosity", 0.02)
        self.identity.update({"last_visual_context": payload})
        self.gui.emit("visual_context", payload)
        