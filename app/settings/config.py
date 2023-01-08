from typing import Optional

import pydantic


class Settings(pydantic.BaseSettings):
    app_name: str = 'Dictionary API'
    dictionary_api_mongodb_url: Optional[str]
    db_name: str = 'dictionarydb'
