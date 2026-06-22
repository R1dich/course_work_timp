ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALPHA_SIZE = len(ALPHABET)


def prepare_key(key):
    cleaned = ""
    for ch in key.upper():
        if ch in ALPHABET:
            cleaned += ch
    if not cleaned:
        raise ValueError("Key must contain at least one letter")
    return cleaned


def vigenere_encrypt(plaintext, key):
    key = prepare_key(key)
    ciphertext = []
    key_index = 0
    for ch in plaintext:
        upper = ch.upper()
        if upper in ALPHABET:
            shift = ALPHABET.index(key[key_index % len(key)])
            pos = (ALPHABET.index(upper) + shift) % ALPHA_SIZE
            encrypted = ALPHABET[pos]
            ciphertext.append(encrypted if ch.isupper() else encrypted.lower())
            key_index += 1
        else:
            ciphertext.append(ch)
    return "".join(ciphertext)


def vigenere_decrypt(ciphertext, key):
    key = prepare_key(key)
    plaintext = []
    key_index = 0
    for ch in ciphertext:
        upper = ch.upper()
        if upper in ALPHABET:
            shift = ALPHABET.index(key[key_index % len(key)])
            pos = (ALPHABET.index(upper) - shift) % ALPHA_SIZE
            decrypted = ALPHABET[pos]
            plaintext.append(decrypted if ch.isupper() else decrypted.lower())
            key_index += 1
        else:
            plaintext.append(ch)
    return "".join(plaintext)


def frequency_analysis(text):
    counts = {}
    total = 0
    for ch in text.upper():
        if ch in ALPHABET:
            counts[ch] = counts.get(ch, 0) + 1
            total += 1
    if total == 0:
        return {}
    return {ch: counts[ch] / total for ch in sorted(counts, key=counts.get, reverse=True)}


def index_of_coincidence(text):
    counts = {}
    n = 0
    for ch in text.upper():
        if ch in ALPHABET:
            counts[ch] = counts.get(ch, 0) + 1
            n += 1
    if n < 2:
        return 0.0
    numerator = sum(f * (f - 1) for f in counts.values())
    return numerator / (n * (n - 1))


def main():
    message = "The quick brown fox jumps over the lazy dog"
    key = "SECRET"

    encrypted = vigenere_encrypt(message, key)
    decrypted = vigenere_decrypt(encrypted, key)

    print(f"Original : {message}")
    print(f"Key      : {key}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Match    : {message == decrypted}")

    print("\nFrequency analysis (top 5):")
    freq = frequency_analysis(encrypted)
    for i, (ch, prob) in enumerate(list(freq.items())[:5]):
        print(f"  {ch}: {prob:.3f}")

    ic = index_of_coincidence(encrypted)
    print(f"\nIndex of Coincidence: {ic:.4f}")
    print("(English ~0.065, random ~0.038)")


if __name__ == "__main__":
    main()
