import { websocket } from "./websocket.js";

function createElementFromHTML(htmlString) {
  const div = document.createElement("div");
  div.innerHTML = htmlString.trim();
  return div.firstChild;
}

const coverNode = createElementFromHTML(`
  <div class="disconnected-cover">
    <div class="disconnected-icon-container">
      <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="bi bi-plug" viewBox="0 0 16 16">
        <path d="M6 0a.5.5 0 0 1 .5.5V3h3V.5a.5.5 0 0 1 1 0V3h1a.5.5 0 0 1 .5.5v3A3.5 3.5 0 0 1 8.5 10c-.002.434-.01.845-.04 1.22-.041.514-.126 1.003-.317 1.424a2.083 2.083 0 0 1-.97 1.028C6.725 13.9 6.169 14 5.5 14c-.998 0-1.61.33-1.974.718A1.922 1.922 0 0 0 3 16H2c0-.616.232-1.367.797-1.968C3.374 13.42 4.261 13 5.5 13c.581 0 .962-.088 1.218-.219.241-.123.4-.3.514-.55.121-.266.193-.621.23-1.09.027-.34.035-.718.037-1.141A3.5 3.5 0 0 1 4 6.5v-3a.5.5 0 0 1 .5-.5h1V.5A.5.5 0 0 1 6 0zM5 4v2.5A2.5 2.5 0 0 0 7.5 9h1A2.5 2.5 0 0 0 11 6.5V4H5z"/>
      </svg>
    </div>
  </div>
`);

let slowConnection = false;

const timeoutId = setTimeout(() => {
  document.body.appendChild(coverNode);
  slowConnection = true;
}, 3000);

websocket.on("connection-change", (connected) => {
  if (!connected) {
    document.body.appendChild(coverNode);
  } else {
    if (document.body.contains(coverNode)) {
      document.body.removeChild(coverNode);
    }
    if (!slowConnection) {
      clearTimeout(timeoutId);
    }
  }
});
