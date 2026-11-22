"""String Studio: an interactive tour of Python's built-in string methods."""


def show(title, value):
    """Print a method name and its result in a readable way."""
    print(f"{title:<24} -> {value!r}")


def string_studio(text):
    print("\n" + "=" * 60)
    print("                 PYTHON STRING STUDIO")
    print("=" * 60)
    print("Your original text:", repr(text))

    # Change letter case
    print("\n--- Change letter case ---")
    show("capitalize()", text.capitalize())
    show("casefold()", text.casefold())
    show("lower()", text.lower())
    show("upper()", text.upper())
    show("title()", text.title())
    show("swapcase()", text.swapcase())

    # Find, count, and check pieces of text
    print("\n--- Search and check ---")
    show("count('a')", text.count("a"))
    show("find('a')", text.find("a"))
    show("rfind('a')", text.rfind("a"))
    show("startswith('Hello')", text.startswith("Hello"))
    show("endswith('!')", text.endswith("!"))
    show("'Python' in text", "Python" in text)

    # Remove unwanted spaces or characters
    print("\n--- Clean text ---")
    show("strip()", text.strip())
    show("lstrip()", text.lstrip())
    show("rstrip()", text.rstrip())
    show("replace('a', '@')", text.replace("a", "@"))
    show("removeprefix('Hello ')", text.removeprefix("Hello "))
    show("removesuffix('!')", text.removesuffix("!"))

    # Split text into parts and join it again
    print("\n--- Split and join ---")
    words = text.split()
    show("split()", words)
    show("rsplit(maxsplit=1)", text.rsplit(maxsplit=1))
    show("' | '.join(words)", " | ".join(words))
    show("splitlines()", text.splitlines())
    show("partition(' ')", text.partition(" "))
    show("rpartition(' ')", text.rpartition(" "))

    # Check what kind of characters the text contains
    print("\n--- Character checks ---")
    show("isalnum()", text.isalnum())
    show("isalpha()", text.isalpha())
    show("isascii()", text.isascii())
    show("isdecimal()", text.isdecimal())
    show("isdigit()", text.isdigit())
    show("isidentifier()", text.isidentifier())
    show("islower()", text.islower())
    show("isnumeric()", text.isnumeric())
    show("isprintable()", text.isprintable())
    show("isspace()", text.isspace())
    show("istitle()", text.istitle())
    show("isupper()", text.isupper())

    # Align text and replace characters using translation
    print("\n--- Format and translate ---")
    show("center(30, '-')", text.center(30, "-"))
    show("ljust(30, '.')", text.ljust(30, "."))
    show("rjust(30, '.')", text.rjust(30, "."))
    show("zfill(20)", text.zfill(20))
    show("expandtabs(4)", text.expandtabs(4))
    translator = str.maketrans("aeiou", "12345")
    show("translate(vowels)", text.translate(translator))

    # A small useful result made from the entered text
    cleaned_words = [word.strip(".,!?;:").title() for word in text.split()]
    headline = " ".join(cleaned_words)
    print("\n--- Your polished headline ---")
    print(headline if headline else "(You did not enter any words.)")
    print(f"Word count: {len(words)} | Character count: {len(text)}")
    print("=" * 60)


def main():
    print("Welcome! This program explores Python string functions.")
    text = input("Type a sentence (or press Enter for the example): ")
    if not text:
        text = "  Hello Python, strings are fun!  "
    string_studio(text)


if __name__ == "__main__":
    main()
