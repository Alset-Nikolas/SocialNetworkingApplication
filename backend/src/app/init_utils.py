import os
import warnings

import typing as t
from dotenv import load_dotenv
from fastapi import FastAPI

from app.core.config import get_settings, AppDevelopmentSettings, AppProductionSettings, AppTestSettings


def get_app_config_from_environ() -> str:
    try:
        app_config = os.environ["SOCIAL_NETWORK_CONFIG"]
    except KeyError as e:
        raise RuntimeError(f"Environ attr '{e.args[0]}' does not exist.")
    return app_config


def init_settings(app_config_name: str) -> t.Union[AppDevelopmentSettings, AppProductionSettings, AppTestSettings]:
    try:
        settings = get_settings(app_config_name)
        print(f'Settings name: {settings.SETTINGS_NAME}, {type(settings)}')
        return settings
    except KeyError as err:
        warnings.warn(f".env SETTINGS_NAME error (dev, prod, test): {err}")
        exit(0)
