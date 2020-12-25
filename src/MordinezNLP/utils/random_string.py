import random
import string
from typing import List


def random_string(length: int = 64, choices_list: List[str] = string.ascii_uppercase + string.digits) -> str:
    """
    Generate random string which contains characters from *choices_list* arg.

    Args:
        length (int): length of generated string
        choices_list (List[str]): List of characters from which random string should be generated

    Returns:
        str: Randomly generated string
    """
    return "".join(
        [
            random.choice(choices_list) for _ in range(length)
        ]
    )


if __name__ == '__main__':
    rs = random_string(32)
    print(rs)

    rs = random_string(10, string.digits)
    print(rs)
