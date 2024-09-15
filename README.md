# Strava Activities Fetcher

This project fetches activities from the Strava API and stores them in a SQLite database. `black`, `ruff` and `mypy` are used to enforce code style and quality.

## Features

- Fetch activities from Strava API
- Store activities in SQLite database
- Comprehensive test coverage
- Type hints for better code clarity
- Logging for debugging and monitoring

## Upcoming features

- Listen for new strava activities via [Strava Webhooks](https://developers.strava.com/docs/webhooks/)
- Get second-granularity power and HR data via the [api](https://developers.strava.com/docs/reference/#api-Streams-getActivityStreams)
- Use plotly to visualise

## Requirements

- Python 3.11
- `pip` for managing dependencies

## Setup

1. **Clone the repository:**

    ```sh
    git clone https://github.com/tleger/strava-reader.git
    cd strava-reader
    ```

2. **Create a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a `.env` file in the root directory and add the following (replacing placeholder values with your actual credentials):

    ```env
    PASSWORD=your_password
    STRAVA_CLIENT_ID=your_client_id
    STRAVA_CLIENT_SECRET=your_client_secret
    STRAVA_REFRESH_TOKEN=your_refresh_token
    ```

5. **Pre-commit**

    To ensure code quality and consistency, `pre-commit` is used (see config in `.pre-commit-config.yaml`). To install pre-commit hooks:

    ```sh
    pre-commit install
    ```

## Running the application
Simple run `python main.py`.

## Continuous Integration
This project uses GitHub Actions for continuous integration. The configuration file is located at `.github/workflows/ci.yml`.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## FAQ

**Q: How do I get my Strava API credentials?**

A: You can get your Strava API credentials by creating an application on the [Strava Developer Portal](https://developers.strava.com/docs/getting-started/#account).
