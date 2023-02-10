# py-scraper
A simple web scraper in Python adhering to best practices.

## To run:
1. Clone this repository on your local machine
2. Run `docker build --tag python-scraper app/`
3. Run `docker run --mount type=bind,source="$(pwd)/app",target=/app/ -env ENVIRONMENT="prod" --website http(s)://www.<anywebsite>.com/`

## Output: 
The docker container should output two files in the `app/` directory:
1. "content_file.json" -> This a json list of all the external urls loaded in the page provided
2. "word_count_file.json -> This is a json dictionary with the frequency of each word appearing in the privacy policy

## For debubgging:
You can change the env variable to "dev" for more thorough logs like so:
`docker run python-scraper -env ENVIRONMENT="dev" --website http(s)://www.<anywebsite>.com/`

##Running tests:
- Install `pytest`
- Run `pytest` and the tests should run :) 