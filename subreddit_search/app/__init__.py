from appdirs import user_cache_dir, user_config_dir
from dataclasses import dataclass

from pathlib import Path

from subreddit_search.__about__ import __APP_NAME__, __AUTHOR__, __DESCRIPTION__, __VERSION__


class AppPaths:
    def __init__(self, app_object):
        self.__app = app_object
        self.__appname = self.app.app_name
        self.__author = self.app.author

    @property
    def app(self):
        return self.__app

    @property
    def app_name(self):
        return self.__appname

    @property
    def author(self):
        return self.__author

    @property
    def cache_dir(self):
        return Path(user_cache_dir(self.app_name, self.author))


@dataclass(frozen=True)
class AppData:
    """Dataclass to store application metadata.

    Attributes:
        author (str): The author of the application.
        version (str): The version of the application.
        app_name (str): The name of the application.
    """

    author: str
    version: str
    app_name: str
    description: str


class App:
    APP_DATA = AppData(author=__AUTHOR__, version=__VERSION__, app_name=__APP_NAME__, description=__DESCRIPTION__)
    PATHS = AppPaths(APP_DATA)

