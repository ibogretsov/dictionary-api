from fastapi import status
from fastapi.exceptions import HTTPException
from googletrans.models import Translated

from app import constants


def validate_translated_word(translated_data: Translated) -> None:
    """Validate translated data.

    If word is not valid then parsed data will have length less than 4.
    In this case we don't need to save data in the database or return some
    details about not existing word. Raise exception.
    """
    if len(translated_data.extra_data['parsed']) < 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=constants.NOT_VALID_WORD_TO_GET_INFO
        )
