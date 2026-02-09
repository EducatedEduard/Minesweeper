from dataclasses import dataclass

@dataclass(frozen=True)
class OpenAction:
    field: tuple[int, int]
    multi: bool
    
    def __str__(self) -> str:
        return f"OpenAction(field={self.field}, multi={self.multi})"
    
    
@dataclass(frozen=True)
class FlagAction:
    field: tuple[int, int]
    
    def __str__(self) -> str:
        return f"FlagAction(field={self.field})"