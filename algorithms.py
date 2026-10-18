"""
DAA Project: KMP vs Boyer-Moore String Matching
Contains educational implementations of both algorithms.
"""

def kmp_search(text: str, pattern: str):
    """Return (match_positions, comparison_count) using KMP."""
    if pattern == "":
        return list(range(len(text) + 1)), 0

    # Build the Longest Prefix Suffix (LPS) array.
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length != 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1

    positions = []
    comparisons = 0
    i = j = 0

    while i < len(text):
        comparisons += 1
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == len(pattern):
                positions.append(i - j)
                j = lps[j - 1]
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

    return positions, comparisons


def boyer_moore_search(text: str, pattern: str):
    """
    Return (match_positions, comparison_count) using the Boyer-Moore
    bad-character heuristic. This is a clear, beginner-friendly version.
    """
    if pattern == "":
        return list(range(len(text) + 1)), 0

    n, m = len(text), len(pattern)
    if m > n:
        return [], 0

    # Store the rightmost position of each character in the pattern.
    last = {char: index for index, char in enumerate(pattern)}
    positions = []
    comparisons = 0
    shift = 0

    while shift <= n - m:
        j = m - 1

        # Compare from right to left.
        while j >= 0:
            comparisons += 1
            if pattern[j] == text[shift + j]:
                j -= 1
            else:
                break

        if j < 0:
            positions.append(shift)
            # Move forward safely after a match; supports overlapping matches.
            if shift + m < n:
                shift += m - last.get(text[shift + m], -1)
            else:
                shift += 1
        else:
            shift += max(1, j - last.get(text[shift + j], -1))

    return positions, comparisons
