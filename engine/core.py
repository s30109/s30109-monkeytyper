import random


def get_random_words(words_list, count=30):
    """
    Zwraca losową listę słów z dostępnej listy.
    """
    return random.sample(words_list, count)


def evaluate_typing(typed_words, expected_words, time_taken):
    """
    Oblicza poprawność i WPM na podstawie wpisanych słów.

    :param typed_words: lista słów wpisanych przez użytkownika
    :param expected_words: lista słów oczekiwanych (wygenerowanych)
    :param time_taken: czas wpisywania w sekundach
    :return: słownik z wynikami (correct, total_words, wpm, accuracy)
    """
    correct = 0
    total_chars = 0

    for i, word in enumerate(typed_words):
        if i < len(expected_words) and word == expected_words[i]:
            correct += 1
        total_chars += len(word)

    wpm = round((total_chars / 5) / (time_taken / 60), 2)
    accuracy = round((correct / len(typed_words)) * 100, 2) if typed_words else 0.0

    return {
        "correct": correct,
        "total_words": len(typed_words),
        "wpm": wpm,
        "accuracy": accuracy
    }


def main():
    # Wczytaj słowa z pliku words.txt
    with open("words.txt", "r", encoding="utf-8") as f:
        words = [line.strip() for line in f if line.strip()]

    selected = get_random_words(words, count=10)
    print("Przepisz te słowa:")
    print(" ".join(selected))

    typed = input("Wpisz słowa oddzielone spacją:\n").split()
    time_taken = float(input("Podaj czas wpisywania (w sekundach):\n"))

    result = evaluate_typing(typed, selected, time_taken)
    print(f"\nWynik:")
    print(f"Poprawne: {result['correct']}")
    print(f"Wszystkie: {result['total_words']}")
    print(f"WPM: {result['wpm']}")
    print(f"Dokładność: {result['accuracy']}%")


if __name__ == "__main__":
    main()
