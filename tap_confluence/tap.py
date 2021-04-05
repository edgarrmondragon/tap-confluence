from typing import List

from singer_sdk.tap_base import Tap
from singer_sdk.typing import PropertiesList, Property, StringType

from tap_confluence.streams import (
    BlogpostsStream,
    GroupsStream,
    PagesStream,
    SpacesStream,
    ThemesStream,
)

PLUGIN_NAME = "tap-confluence"

STREAM_TYPES = [
    BlogpostsStream,
    PagesStream,
    GroupsStream,
    SpacesStream,
    ThemesStream,
]


class TapConfluence(Tap):
    """confluence tap class."""

    name = "tap-confluence"
    config_jsonschema = PropertiesList(
        Property("base_url", StringType, required=True),
        Property("email", StringType, required=True),
        Property("api_token", StringType, required=True),
        Property("user_agent", StringType),
    ).to_dict()

    def discover_streams(self) -> List:
        """Return a list of discovered streams."""
        return [stream(tap=self) for stream in STREAM_TYPES]


cli = TapConfluence.cli
