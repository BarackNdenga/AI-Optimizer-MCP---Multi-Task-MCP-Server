"""Standalone tests module for subprocess use."""
def run_tests(func):
    test_cases = [
        (2, 4),
        (5, 10),
        (10, 20),
        (-3, -6)
    ]
    score = 0
    for inp, expected in test_cases:
        try:
            if func(inp) == expected:
                score += 1
        except:
            pass
    return score, len(test_cases)

