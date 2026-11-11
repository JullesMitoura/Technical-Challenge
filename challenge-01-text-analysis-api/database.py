from models import HistoryRecord

history: list[HistoryRecord] = []

def save(record: HistoryRecord) -> None:
    history.append(record)

def get_history() -> list[HistoryRecord]:
    return history