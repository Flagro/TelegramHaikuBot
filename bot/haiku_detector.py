import re


def count_syllables(word: str) -> int:
    """
    Count syllables in a word using a simple algorithm.
    This is a basic implementation and may not be perfect.
    """
    word = word.lower().strip()
    if not word:
        return 0

    # Remove non-alphabetic characters
    word = re.sub(r"[^a-z]", "", word)

    if len(word) <= 3:
        return 1

    # Count vowel groups
    vowels = "aeiouy"
    syllable_count = 0
    previous_was_vowel = False

    for char in word:
        is_vowel = char in vowels
        if is_vowel and not previous_was_vowel:
            syllable_count += 1
        previous_was_vowel = is_vowel

    # Adjust for silent 'e' at the end
    if word.endswith("e") and syllable_count > 1:
        syllable_count -= 1

    # Adjust for 'le' at the end
    if word.endswith("le") and len(word) > 2 and word[-3] not in vowels:
        syllable_count += 1

    return max(1, syllable_count)


def count_line_syllables(line: str) -> int:
    """Count total syllables in a line of text."""
    words = re.findall(r"\b\w+\b", line)
    return sum(count_syllables(word) for word in words)


def detect_haiku(text: str) -> tuple[bool, list[str] | None]:
    """
    Detect if the text contains a haiku (5-7-5 syllable pattern).

    Args:
        text: The text to check for haiku

    Returns:
        A tuple of (is_haiku, lines) where:
        - is_haiku: True if text is a haiku
        - lines: The three lines if it's a haiku, None otherwise
    """
    # Split by newlines and filter empty lines
    lines = [line.strip() for line in text.strip().split("\n") if line.strip()]

    # A haiku must have exactly 3 lines
    if len(lines) != 3:
        return False, None

    # Count syllables for each line
    syllable_counts = [count_line_syllables(line) for line in lines]

    # Check if it matches the 5-7-5 pattern
    if syllable_counts == [5, 7, 5]:
        return True, lines

    return False, None
