import string
import random

from .models import WorkBoard


def generate_link():
    '''
    This is use for generating unique code for WorkBoard link
    where user only need to type this generated link when joining
    to the workBoard
    '''
    letters_and_numbers = string.ascii_letters + string.digits
    unique_token = ''.join(random.choice(
        letters_and_numbers) for i in range(8))

    if WorkBoard.objects.filter(link=unique_token).exists():
        return generate_link(unique_token)

    else:
        return unique_token
