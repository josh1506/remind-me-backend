import string
import random

from .models import Workspace


def generate_link():
    letters_and_numbers = string.ascii_letters + string.digits
    unique_token = ''.join(random.choice(
        letters_and_numbers) for i in range(8))

    if Workspace.objects.filter(link=unique_token).exists():
        return generate_link(unique_token)

    else:
        return unique_token
