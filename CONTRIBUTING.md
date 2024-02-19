# Notes for Developers

High quality PRs will be considered for merging. For significant work, open an issue first, or a draft PR, so we can discuss the approach.

## Code Organization

The code is organized as follows:

* [`hyperdiv`](hyperdiv): The Hyperdiv Python implementation.
  * [`hyperdiv/components`](hyperdiv/components). The implementations of Hyperdiv components.
  * [`hyperdiv/component_mixins`](hyperdiv/component_mixins). Mixins are non-component classes that define common sets of props that can be "mixed into" components via inheritance.
  * [`hyperdiv/prop_types`](hyperdiv/prop_types). The implementations of Hyperdiv's prop types.
* [`frontend`](frontend): The Hyperdiv Javascript frontend.
  * [`frontend/src`](frontend/src): The frontend's source code.

When a browser connects to a running Hyperdiv app, the Hyperdiv server serves the built frontend to the browser. Once it starts running, the frontend opens a Websocket connection back to the Hyperdiv server. The Hyperdiv app then runs, and its output virtual dom is sent to the browser, which translates it into browser dom. Then, the frontend and the server continue to exchange messages: The frontend sends UI events to the server, and the server sends virtual dom diffs back to the frontend, which patches them into the browser dom.

## Python

Hyperdiv uses [Poetry](https://python-poetry.org) as its build system and dependencies are maintained in [pyproject.toml](pyproject.toml) and [poetry.lock](poetry.lock). The lock file recursively freezes the version numbers of the entire dependency tree, making sure that as long as [pyproject.toml](pyproject.toml) doesn't change, the dependency tree is identical every time dependencies are installed.

After installing Poetry and cloning the Hyperdiv repo, you can `cd` into the repo and install its dependencies:

```sh
poetry install
```

This will create a `.venv` directory with the virtualenv that contains all the dependencies. To enter the virtualenv you can do:

```sh
poetry shell
```

This creates a new shell that automatically enters the virtualenv. At this point you can run `pytest` to run the test suite.

## Frontend

To install the frontend dependencies and build the frontend:

```sh
cd frontend
npm install
npm run build
```

If you're actively developing the frontend, you should start the development build server:

```sh
npm run dev
```

The build server will watch source files and it will automatically rebuild the frontend, and reload any connected Hyperdiv apps, as you save source files.

## Writing Tests

Hyperdiv uses Pytest to run unit tests.

The tests corresponding to each Python source code directory are placed in a subdirectory of that directory, called `tests/`.

A bit of test boilerplate can be found in [`hyperdiv/test_utils.py`](hyperdiv/test_utils.py).

To run the tests and print out coverage results, `cd` into the Hyperdiv repo and run:

```sh
pytest
```

## Documentation

The documentation app is in the [hyperdiv-docs](https://github.com/hyperdiv/hyperdiv-docs) repo. Changes to documentation should be made by modifying that app. In general, if making minor modifications like adding/removing props or updating docstrings, the documentation app will automatically pick up those changes.

## Makefile

Hyperdiv has a [`Makefile`](Makefile) that is used to prepare Hyperdiv for being published to [PyPI](https://pypi.org). The Makefile assumes that the [hyperdiv-docs](https://github.com/hyperdiv/hyperdiv-docs) repo is cloned in the same directory as the Hyperdiv repo and checked out to the correct version. The Makefile builds the frontend and then copies both the `hyperdiv-docs` repo and the `public` directory of the built frontend into the `hyperdiv` Python source directory, which will be shipped to PyPI.
