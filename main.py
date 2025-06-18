import time
from engine.core import get_random_words, evaluate_typing

def ask_username():
    return input("Podaj swoją nazwę użytkownika: ")

def load_words(path="words.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return [w.strip() for w in f if w.strip()]

def main():
    username = ask_username()
    words = load_words()
    test_words = get_random_words(words, 30)

    print("\nPrzepisz poniższe słowa (oddzielaj spacją):")
    print(" ".join(test_words))
    input("\nMasz 30 sekund. Naciśnij ENTER aby zacząć...\n")

    print("Zacznij pisać (masz 30 sekund):")
    start_time = time.time()

    try:
        typed_line = input()
    except Exception as e:
        print("❌ Błąd odczytu:", e)
        return

    end_time = time.time()
    duration = round(end_time - start_time)
    typed_words = typed_line.strip().split()

    result = evaluate_typing(typed_words, test_words, 30)
    correct = result["correct"]
    wpm = result["wpm"]
    accuracy = result["accuracy"]

    print("\n=== KONIEC GRY ===")
    print(f"Użytkownik: {username}")
    print(f"Poprawnych słów: {correct} / {len(test_words)}")
    print(f"WPM: {wpm}")
    print(f"Accuracy: {accuracy}%")
    print(f"Czas: {duration}s")

if __name__ == "__main__":
    main()
