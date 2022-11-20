import configparser

from typing import Optional


class GitLabConfigParser:

    project_id: int

    def __init__(self, section: str) -> None:
        self.url: Optional[str] = None
        self.private_token: Optional[str] = None
        self.section: str = section

        self._parse_config()

    def _parse_config(self) -> None:
        _config = configparser.ConfigParser()
        _config.read("gitlaber.cfg", encoding="utf-8")

        self.url = _config.get(self.section, "url")
        self.private_token = _config.get(self.section, "private_token")
        self.project_id = int(_config.get(self.section, "project_id"))
