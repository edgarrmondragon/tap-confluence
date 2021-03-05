from __future__ import annotations

import abc
from base64 import b64encode
from pathlib import Path
from typing import Any, Dict, Iterable, List

import requests
from singer_sdk.streams import RESTStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class TapConfluenceStream(RESTStream):

    limit: int = 100
    expand: List[str] = []

    @property
    def url_base(self) -> str:
        """Return the base Confluence URL."""
        return self.config.get("base_url")

    @property
    def http_headers(self) -> dict:
        result = super().http_headers

        email = self.config.get("email")
        api_token = self.config.get("api_token")
        auth = b64encode(f"{email}:{api_token}".encode()).decode()

        result["Authorization"] = f"Basic {auth}"

        return result

    def get_url_params(self, partition: dict | None, next_page_token: int) -> Dict[str, Any]:
        return {
            "limit": self.limit,
            "start": next_page_token,
            "expand": ",".join(self.expand),
        }

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        resp_json = response.json()
        for row in resp_json["results"]:
            # self.logger.info(row.keys())
            # self.logger.info(row.get("_expandable"))
            # self.logger.info(row["_links"])
            yield row

    def get_next_page_token(
        self,
        response: requests.Response,
        previous_token: int | None,
    ) -> int | None:

        previous_token = previous_token or 1

        data = response.json()
        size, limit = data["size"], data["limit"]

        if size < limit:
            return None

        return previous_token + limit


class GroupsStream(TapConfluenceStream):
    name = "groups"
    path = "/group"
    primary_keys = ["id"]
    schema_filepath = SCHEMAS_DIR / "group.json"


class SpacesStream(TapConfluenceStream):
    name = "spaces"
    path = "/space"
    primary_keys = ["id"]
    schema_filepath = SCHEMAS_DIR / "space.json"

    expand = [
        "permissions",
        "icon",
        "description.plain",
        "description.view",
    ]


class ThemesStream(TapConfluenceStream):
    name = "themes"
    path = "/settings/theme"
    primary_keys = ["themeKey"]
    schema_filepath = SCHEMAS_DIR / "theme.json"

    expand = [
        "icon",
    ]


class BaseContentStream(TapConfluenceStream, metaclass=abc.ABCMeta):
    path = "/content"
    primary_keys = ["id"]
    schema_filepath = SCHEMAS_DIR / "content.json"

    expand = [
        "history",
        "history.lastUpdated",
        "history.previousVersion",
        "history.contributors",
        "restrictions.read.restrictions.user",
        "version",
        "descendants.comment",
    ]

    @property
    @abc.abstractmethod
    def content_type(self) -> str:
        """Content type (page or blogpost)."""
        pass

    def get_url_params(
        self,
        partition: dict | None,
        next_page_token: int | None,
    ) -> Dict[str, Any]:
        result = super().get_url_params(partition, next_page_token)
        result["type"] = self.content_type
        return result


class BlogpostsStream(BaseContentStream):
    name = "pages"
    content_type = "page"


class PagesStream(BaseContentStream):
    name = "blogposts"
    content_type = "blogpost"
