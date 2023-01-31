from typing import Any

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Path
from fastapi import Query
from fastapi import status
from fastapi.responses import Response
import fastapi_pagination as fa_pagination

from app import config
from app import constants
from app import deps
from app import schemas
from app.db import managers
from app.exceptions import WordNotFoundError
from app.google_client import GoogleTranslateClient


router = APIRouter(prefix='/words', tags=['words'])


@router.post(
    '/{word}', response_model=schemas.WordInfoModel,
    responses={
        status.HTTP_201_CREATED: {
            'description': """Word does not exist in database. Add word and
                              its details into database and return results.""",
            'content': {
                'application/json': {
                    'schema': {'$ref': '#/components/schemas/WordInfoModel'}
                }
            }
        }
    },
    response_model_exclude_none=True)
def get_word_details(
        response: Response,
        word: str = Path(
            ...,
            title='Target word',
            description="""Word for which you want to receive definitions,
                            translations, synonyms and examples""",
            regex=constants.SINGLE_WORD_REGEX
        ),
        manager: managers.WordDBManager = Depends(deps.get_word_manager)
) -> dict[str, str | Any] | Any:
    try:
        word_info = manager.get_word(word)
    except WordNotFoundError:
        settings = config.get_settings()
        client = GoogleTranslateClient(
            settings.DICTIONARY_API_SOURCE_LANGUAGE,
            settings.DICTIONARY_API_TARGET_LANGUAGE
        )
        word_info = client.get_word_info(word).dict()
        manager.insert_word_info(word_info)
        response.status_code = status.HTTP_201_CREATED
    return word_info


@router.get(
    '/',
    response_model=fa_pagination.Page[schemas.WordInfoModel],
    response_model_exclude_none=True,
    description="""Return paginated response of words with additional fields
    if needed."""
)
def get_words(
        search: str = Query(None),
        translations: bool = Query(False, title='Include translations'),
        examples: bool = Query(False, title='Include examples'),
        definitions: bool = Query(False, title='Include definitions'),
        sort: constants.SortTypeEnum = Query(constants.SortTypeEnum.asc.value),
        manager: managers.WordDBManager = Depends(deps.get_word_manager)
) -> Any:
    result = manager.get_words(
        sort,
        search_pattern=search,
        translations=translations,
        examples=examples,
        definitions=definitions
    )
    return fa_pagination.paginate(result)


@router.delete(
    '/{word}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {
            'description': 'Response if try to delete not existed word in db',
            'content': {
                'application/json': {
                    'example': {
                        'detail': constants.WORD_NOT_FOUND.format(word='word')
                    }
                }
            }
        }
    }
)
def delete_word(
        word: str = Path(
            ...,
            title='Word to delete',
            description="""Delete word, all its definitions, examples
                            and translations""",
            regex=constants.SINGLE_WORD_REGEX
        ),
        manager: managers.WordDBManager = Depends(deps.get_word_manager)
) -> Response:
    manager.delete_word(word)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
