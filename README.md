# tap-confluence

[![Super-Linter](https://github.com/edgarrmondragon/tap-confluence/actions/workflows/superlinter.yml/badge.svg)](https://github.com/edgarrmondragon/tap-confluence/actions/workflows/superlinter.yml)

Singer tap for the Confluence REST API. Developed using the [Singer SDK][sdk].

## Roadmap

- [x] Content
- [x] Spaces
- [x] Themes
- [x] Groups
- [ ] Users

## Configuration

### Using JSON

```shell
tap-confluence --config config.json
```

where `config.json` is

```json
{
    "base_url": "https://your-domain.atlassian.net/wiki/rest/api",
    "email": "<your_email@domain.com>",
    "api_token": "<your_user_api_token>",
    "resources": [
        "spaces",
        "content",
        "groups"
    ]
}
```

### Using environment variables

They can be used together with JSON configuration:

```shell
TAP_CONFLUENCE_base_url=https://your-domain.atlassian.net/wiki/rest/api \
TAP_CONFLUENCE_email=<your_email@domain.com> \
TAP_CONFLUENCE_api_token=<your_user_api_token> \
tap-confluence --config simpleConfig.json
```

where `simpleConfig.json` is

```json
{
    "resources": [
        "spaces",
        "content",
        "themes",
        "groups"
    ]
}
```

## Links

- [Confluence API docs][confluence-docs]
- [Basic Auth for Confluence API][confluence-basic-auth]

[sdk]: https://gitlab.com/meltano/singer-sdk/
[confluence-docs]: https://developer.atlassian.com/cloud/confluence/rest/intro/
[confluence-basic-auth]: https://developer.atlassian.com/cloud/confluence/basic-auth-for-rest-apis/
