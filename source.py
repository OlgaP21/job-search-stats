from enum import Enum


class Source(Enum):
    
    CVKeskus = 'CVKeskus',
    CV = 'cv.ee',
    Tootukassa = 'Töötukassa',
    Letter = 'E-kiri',
    Miscellaneous = 'Muu'
    
    
    @staticmethod
    def from_string(source: str) -> Enum:
        if source == 'CVKeskus':
            return Source.CVKeskus
        if source == 'cv.ee':
            return Source.CV
        if source == 'Töötukassa':
            return Source.Tootukassa
        if source == 'E-kiri':
            return Source.Letter
        if source == 'Muu':
            return Source.Miscellaneous
        return None
    
    
    def __str__(self):
        if type(self.value) is str:
            return self.value
        else:
            return self.value[0]
