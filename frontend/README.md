## The Hyperdiv Frontend

Hyperdiv is made of a server/runtime system written in Python, and a browser client/frontend written in JS/HTML/CSS. When a browser connects to the server, the server ships the built frontend to the browser. Then the frontend and server communicate over a websocket.

This directory contains the code for the frontend.

To work on the frontend, you need a recent version of `node` installed. To install depedencies:
```sh
npm install
```
To build the frontend:
```sh
npm run build
```
The built files will be created in the `public/build` directory.

To start the development server, which watches changes to files, automatically rebuilds the frontend when files change, and reloads connected browsers:
```sh
npm run dev
```

Note that the frontend does not contain an `index.html` file. This file is generated on the Python side and served to the browser from memory. See [`index_page.py`](../hyperdiv/index_page.py) and [`main.py`](../hyperdiv/main.py).
