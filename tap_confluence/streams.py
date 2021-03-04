from base64 import b64encode
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

import requests

from singer_sdk.streams import RESTStream
from singer_sdk.authenticators import APIAuthenticatorBase, SimpleAuthenticator


SCHEMAS_DIR = Path("./schemas")


class TapConfluenceStream(RESTStream):

    limit: int = 100
    expand = []

    @property
    def url_base(self) -> str:
        """Return the base Confluence URL."""
        return self.config.get("base_url")

    @property
    def authenticator(self) -> APIAuthenticatorBase:
        email = self.config.get("email")
        api_token = self.config.get("api_token")
        auth = b64encode(f"{email}:{api_token}".encode()).decode()

        http_headers = {"Authorization": f"Basic {auth}"}

        if self.config.get("user_agent"):
            http_headers["User-Agent"] = self.config.get("user_agent")

        return SimpleAuthenticator(stream=self, http_headers=http_headers)

    def get_url_params(self, partition: Optional[dict]) -> Dict[str, Any]:
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

    def request_records(self, partition: Optional[dict]) -> Iterable[dict]:
        start = 1
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
        "history.nextVersion",
        "restrictions.read.restrictions.user",
        "version",
        "descendants.comment",
    ]
