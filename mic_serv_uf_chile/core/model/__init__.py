from dataclasses import dataclass, asdict

@dataclass
class UF:
    """UF representation by day."""
    value: str
    date: str
    dict = asdict
