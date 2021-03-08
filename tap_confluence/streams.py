from __future__ import annotations

from base64 import b64encode
from pathlib import Path
from typing import (
    Any,
    Dict,
    Iterable,
    List,
)

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

    def get_url_params(self, partition: dict | None) -> Dict[str, Any]:
        return {"limit": self.limit, "expand": ",".join(self.expand)}

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        resp_json = response.json()
        for row in resp_json["results"]:
            # self.logger.info(row.keys())
            # self.logger.info(row.get("_expandable"))
            # self.logger.info(row["_links"])
            yield row

    def insert_next_page_token(self, next_page, params) -> Any:
        params["start"] = next_page
        return params

    def request_records(self, partition: dict | None) -> Iterable[dict]:
        start = 0
        while True:
            prepared_request = self.prepare_request(partition, next_page_token=start)
            resp = self._request_with_backoff(prepared_request)
            for row in self.parse_response(resp):
                yield row

            data = resp.json()
            size, limit = data["size"], data["limit"]
            # self.logger.info(size)

            if size < limit:
                break

            start += limit


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


class ContentStream(TapConfluenceStream):
    name = "content"
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
