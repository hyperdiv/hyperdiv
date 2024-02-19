import { onClick } from "./common-handlers.js";
import { ShoelaceComponent } from "./core.js";
import { onLinkClick } from "./link.js";

export class BreadcrumbItem extends ShoelaceComponent {
  static eventHandlers() {
    return [onClick, onLinkClick];
  }
}
