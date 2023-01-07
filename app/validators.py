from fastapi import status
from fastapi.exceptions import HTTPException
from googletrans.models import Translated


def validate_translated_word(translated_data: Translated) -> None:
    if len(translated_data.extra_data['parsed']) < 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Not valid word to get info.'
        )
