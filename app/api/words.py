from typing import Any

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Path
from fastapi import Query
from fastapi import status
from fastapi.responses import Response
import fastapi_pagination as fa_pagination
from motor.motor_asyncio import AsyncIOMotorDatabase

from app import constants
from app import deps
from app import schemas
from app.db import manager
from app.google_client import GoogleTranslateClient


router = APIRouter(prefix='/words', tags=['words'])


@router.post(
    '/{word}', response_model=schemas.WordInfo,
    responses={
        status.HTTP_201_CREATED: {
            'description': 'Add word details in db and return results.',
            'content': {
                'application/json': {
                    'schema': {'$ref': '#/components/schemas/WordInfo'}
                }
            }
        }
    })
async def get_word_details(
        response: Response,
        word: str = Path(
            ...,
            title='Word for details',
            description="""Word for which you want to receive definitions,
                            translations, synonyms and examples""",
            regex=constants.SINGE_WORD_REGEX
        ),
        db: AsyncIOMotorDatabase = Depends(deps.get_db),
):
    word_manager = manager.WordDBManager(db)
    word_info = await word_manager.get_word(word)
    if word_info is None:
        word_info = GoogleTranslateClient().get_word_info(word)
        await word_manager.insert_word_info(word_info)
        response.status_code = status.HTTP_201_CREATED
    return word_info


@router.get(
    '/',
    response_model=fa_pagination.Page[schemas.WordInfo],
    response_model_exclude_none=True,
)
async def get_words(
        search: str = Query(None),
        translations: bool = Query(False, title='Include translations'),
        examples: bool = Query(False, title='Include examples'),
        definitions: bool = Query(False, title='Include definitions'),
        sort: constants.SortTypeEnum = Query(constants.SortTypeEnum.asc.value),
        db: AsyncIOMotorDatabase = Depends(deps.get_db)
) -> Any:
    word_manager = manager.WordDBManager(db)
    result = await word_manager.get_words(
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
async def delete_word(
        word: str = Path(
            ...,
            title='Word to delete',
            description="""Delete word an all its definitions,
                            examples and translations""",
            regex=constants.SINGE_WORD_REGEX
        ),
        db: AsyncIOMotorDatabase = Depends(deps.get_db)
) -> Response:
    word_manager = manager.WordDBManager(db)
    result = await word_manager.delete_word(word)
    if result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=constants.WORD_NOT_FOUND.format(word=word)
    )
