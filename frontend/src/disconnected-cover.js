import { websocket } from "./websocket.js";

function createElementFromHTML(htmlString) {
  const div = document.createElement("div");
  div.innerHTML = htmlString.trim();
  return div.firstChild;
}

const coverNode = createElementFromHTML(`
  <div class="disconnected-cover">
    <div class="disconnected-icon-container">
       <sl-icon name="plug"></sl-icon>
    </div>
  </div>
`);

document.body.appendChild(coverNode);

websocket.on("connection-change", (connected) => {
  if (!connected) {
    document.body.appendChild(coverNode);
  } else {
    document.body.removeChild(coverNode);
  }
});
