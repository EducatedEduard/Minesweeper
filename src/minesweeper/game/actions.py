from dataclasses import dataclass

@dataclass(frozen=True)
class OpenAction:
    row: int
    col: int
    
@dataclass(frozen=True)
class FlagAction:
    row: int
    col: int