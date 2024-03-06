class CharIndex:
    def __init__(self, characters: int = 2) -> None:
        start = ord('c') if characters == 1 else ord('a')
        self._characters: list[int] = [start for _ in range(characters)]
    
    def increment(self) -> None:
        self._characters[-1] += 1
        for i, char_index in enumerate(self._characters[::-1]):
            if char_index > ord('z'):
                self._characters[i] += 1
                self._characters[i - 1] = ord('a')
    
    def get(self) -> str:
        return ''.join([chr(i) for i in self._characters])
