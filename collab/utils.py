import string
import random

from .models import Workspace


def generate_link():
    '''
    This is use for generating unique code for Workspace link
    where user only need to type this generated link when joining
    to the workspace
    '''
    letters_and_numbers = string.ascii_letters + string.digits
    unique_token = ''.join(random.choice(
        letters_and_numbers) for i in range(8))

    if Workspace.objects.filter(link=unique_token).exists():
        return generate_link(unique_token)

    else:
        return unique_token
