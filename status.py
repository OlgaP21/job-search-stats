from enum import Enum


class Status(Enum):
    
    TBD = 'TBD',
    Refusal = 'Eitav vastus'
    Unanswered = 'Vastust pole'
    
    def from_string(status: str) -> Enum:
        if status == 'TBD':
            return Status.TBD
        if status == 'Eitav vastus':
            return Status.Refusal
        if status == 'Vastust pole':
            return Status.Unanswered
        # Throw an exception
        # Unknown status type (?)
        pass
    
    
    def __str__(self):
        if type(self.value) is str:
            return self.value
        else:
            return self.value[0]
