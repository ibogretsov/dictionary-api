from typing import Any

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Path
from fastapi import Query
from fastapi import status
from fastapi.responses import Response
from googletrans import Translator
from motor.motor_asyncio import AsyncIOMotorDatabase

from app import constants
from app import data_parser
from app import deps
from app import schemas
from app import validators
from app.db import manager


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
        translator = Translator(raise_exception=True)
        # Unfortunately translator does not have async feature. We can run it in
        # separate thread to simulate async code
        # TODO (ibogretsov): add threading to run
        try:
            translated_data = translator.translate(word, dest='ru', src='en')
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=constants.TRANSLATOR_CLIENT_ERROR
            )
        validators.validate_translated_word(translated_data)
        parser: data_parser.Parser = data_parser.Parser(
            translated_data.extra_data['parsed'][3]
        )
        parser.parse_data()
        word_info = {
            'word': word,
            'definitions': parser.parsed_data['definitions'],
            'translations': parser.parsed_data['translations'],
            'examples': parser.parsed_data['examples']
        }
        await word_manager.insert_word_info(word_info)
        response.status_code = status.HTTP_201_CREATED
    return word_info


@router.get('/')
async def get_words(
        page: int = Query(0),
        page_size: int = Query(50),
        search: str = Query(None),
        with_tr: bool = Query(False),
        with_ex: bool = Query(False),
        with_def: bool = Query(False),
        db: AsyncIOMotorDatabase = Depends(deps.get_db)
) -> Any:
    search_params = ({} if not search
                     else {'word': {'$regex': search, '$options': 'i'}})
    columns_map = {'_id': 0}
    if not with_tr:
        columns_map['translations'] = 0
    if not with_ex:
        columns_map['examples'] = 0
    if not with_def:
        columns_map['definitions'] = 0
    result = await (db.words
                      .find(search_params, columns_map)
                      .skip(page)
                      .to_list(page_size))
    return result


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
