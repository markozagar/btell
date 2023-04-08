import random
import itertools


def generate_random_password(length: int) -> str:
    """Generates a random, secure password of the given length."""

    a_to_z = [chr(c) for c in range(ord('a'), ord('z') + 1)]
    digits = [chr(c) for c in range(ord('0'), ord('9') + 1)]
    specials = ['!@#$%^&*_-']
    characters = list(itertools.chain(
        *a_to_z,
        *[c.upper() for c in a_to_z],
        *digits,
        *specials,
    ))
    password = [random.choice(characters) for _ in range(length)]
    return "".join(password)
