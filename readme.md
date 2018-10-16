# Contactie

**Contactie** brings the magic of a rolodex to the Internet. Finally, a way to store your address book, safely and
securely on a public API anyone can access. To get started adding features to this software, you'll need:

* A working PostgreSQL setup
* `pipenv`
* `vue-cli` and `yarn`

If you have questions about this, email [ken@kkinder.com](mailto:ken@kkinder.com). 

## Local Development Setup

### Setup local dev API

1. Do virtualenv/docker, if you want.
2. Make sure you have a PostgreSQL database to test with.
3. Use `pipenv` to setup environment (`pipenv install`, `pipenv shell --fancy`)
4. Copy `.env-sample` to `.env` and modify it to include the connection information.
5. `python server.py`

### Setup local vue dev

1. Setup project `yarn install`
2. Run dev server, which proxies `/api` automatically. `yarn run serve`


## Testing

### Running the Python tests.

1. Have PostgreSQL.
2. Create a database and user for tests.
3. Copy `tests/.env-test-sample` to `tests/.env-test` and modify it to include the connection information.
4. Make sure you're using the pipenv.
5. `python -m unittest discover`

## Building

Build for production
```
yarn run build
```

