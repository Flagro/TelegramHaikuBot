import re


def count_syllables(word: str) -> int:
    """
    Count syllables in a word using a simple algorithm.
    This is a basic implementation and may not be perfect.
    Supports Latin (with diacritics), Cyrillic, and mixed text.
    """
    word = word.lower().strip()
    if not word:
        return 0

    # Remove non-alphabetic characters (keep Latin, Cyrillic, and diacritics)
    # Keep: a-z, Latin with diacritics (À-ÿ), Cyrillic (Ё, ё, А-я)
    word = re.sub(r"[^a-zà-ÿёа-я]", "", word)

    if len(word) <= 3:
        return 1

    # Count vowel groups
    # Latin vowels (including common diacritics) + Cyrillic vowels
    vowels = "aeiouyàáâãäåèéêëìíîïòóôõöùúûüýÿаеёиоуыэюя"
    syllable_count = 0
    previous_was_vowel = False

    for char in word:
        is_vowel = char in vowels
        if is_vowel and not previous_was_vowel:
            syllable_count += 1
        previous_was_vowel = is_vowel

    # Adjust for silent 'e' at the end (Latin languages only)
    if word.endswith("e") and syllable_count > 1:
        syllable_count -= 1

    # Adjust for 'le' at the end (Latin languages only)
    if word.endswith("le") and len(word) > 2 and word[-3] not in vowels:
        syllable_count += 1

    return max(1, syllable_count)


def count_line_syllables(line: str) -> int:
    """Count total syllables in a line of text."""
    # Match words containing Latin (with diacritics), Cyrillic, or mixed
    words = re.findall(r"[a-zà-ÿёа-я]+", line, re.IGNORECASE)
    return sum(count_syllables(word) for word in words)


def find_haiku_splits(words: list[str]) -> list[str] | None:
    """
    Try to find a valid 5-7-5 split of the words into 3 lines.

    Args:
        words: List of words to split

    Returns:
        A list of 3 lines if a valid haiku split is found, None otherwise
    """
    if len(words) < 3:
        return None

    # Try all possible ways to split words into 3 lines
    # Line 1: words[0:i], Line 2: words[i:j], Line 3: words[j:]
    for i in range(1, len(words)):
        line1_words = words[:i]
        line1 = " ".join(line1_words)
        line1_syllables = count_line_syllables(line1)

        # Early exit if line 1 doesn't have 5 syllables
        if line1_syllables != 5:
            continue

        for j in range(i + 1, len(words) + 1):
            line2_words = words[i:j]
            line2 = " ".join(line2_words)
            line2_syllables = count_line_syllables(line2)

            # Early exit if line 2 doesn't have 7 syllables
            if line2_syllables != 7:
                continue

            line3_words = words[j:]
            line3 = " ".join(line3_words)
            line3_syllables = count_line_syllables(line3)

            # Check if line 3 has 5 syllables
            if line3_syllables == 5:
                return [line1, line2, line3]

    return None


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
    text = text.strip()
    if not text:
        return False, None

    # Normalize all whitespace (including newlines) to single spaces
    normalized_text = re.sub(r"\s+", " ", text)

    # Extract all words from the normalized text
    words = re.findall(r"[a-zà-ÿёа-я]+", normalized_text, re.IGNORECASE)

    if len(words) < 3:
        return False, None

    # Try to find a valid 5-7-5 split
    haiku_lines = find_haiku_splits(words)

    if haiku_lines:
        return True, haiku_lines

    return False, None
