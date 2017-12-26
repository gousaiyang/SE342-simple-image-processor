# -*- coding: utf-8 -*-

class Version:
    def __init__(self):
        self.versions = []
        self.current_pos = None
        self.saved_pos = None

    def init(self, v):
        self.versions = [v]
        self.current_pos = 0
        self.saved_pos = 0

    def add(self, v):
        self.versions = self.versions[:self.current_pos + 1] + [v]
        self.current_pos += 1

    def undo(self):
        if self.current_pos > 0:
            self.current_pos -= 1

    def redo(self):
        if self.current_pos < len(self.versions) - 1:
            self.current_pos += 1

    def save(self, *, discard_old = False):
        if discard_old:
            self.versions = self.versions[self.current_pos:]
            self.current_pos = 0

        self.saved_pos = self.current_pos

    @property
    def unsaved(self):
        return self.current_pos != self.saved_pos

    @property
    def current_version(self):
        return self.versions[self.current_pos]
