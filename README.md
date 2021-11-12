# tap-confluence

[![Super-Linter](https://github.com/edgarrmondragon/tap-confluence/actions/workflows/superlinter.yml/badge.svg)](https://github.com/edgarrmondragon/tap-confluence/actions/workflows/superlinter.yml)

Singer tap for the Confluence REST API. Developed using the [Singer SDK][sdk].

## Installation

```bash
pipx install git+https://github.com/edgarrmondragon/tap-confluence.git
```

## Roadmap

- [x] Content
- [x] Spaces
- [x] Themes
- [x] Groups
- [ ] Users

## Configuration

```json
{
    "base_url": "https://your-domain.atlassian.net/wiki/rest/api",
    "email": "<your_email@domain.com>",
    "api_token": "<your_user_api_token>",
    "user_agent": "MyDataIntegrationApp/1.0.0 Singer.io Tap for Confluence"
}
```

## Developer Resources

### Initialize your Development Environment

You will need [Poetry](https://python-poetry.org/docs/#installation) installed on your machine.

```bash
# Install package dependencies
poetry install

# Extract records
poetry run tap-confluence --config config.json
```

## Links

- [Confluence API docs][confluence-docs]
- [Basic Auth for Confluence API][confluence-basic-auth]

[sdk]: https://gitlab.com/meltano/singer-sdk/
[confluence-docs]: https://developer.atlassian.com/cloud/confluence/rest/intro/
[confluence-basic-auth]: https://developer.atlassian.com/cloud/confluence/basic-auth-for-rest-apis/
