def count_letters(text: str) -> int:
    return sum(1 for char in text if char.isalpha())