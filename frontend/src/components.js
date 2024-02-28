import {
  ShoelaceComponent,
  HtmlComponent,
  Plugin,
  Alert,
  Avatar,
  Badge,
  Button,
  Details,
  Dialog,
  Drawer,
  Dropdown,
  IconButton,
  MenuItem,
  Plaintext,
  RadioGroup,
  Select,
  Slider,
  Text,
  TextInput,
  Textarea,
  Tooltip,
} from "./components/core.js";
import { Animation } from "./components/animation.js";
import { BreadcrumbItem } from "./components/breadcrumb-item.js";
import { Carousel } from "./components/carousel.js";
import { Chart } from "./components/chart.js";
import { Checkbox } from "./components/checkbox.js";
import { ColorPicker } from "./components/color-picker.js";
import { Form } from "./components/form.js";
import { ImageComparer } from "./components/image-comparer.js";
import { Link } from "./components/link.js";
import { Markdown } from "./components/markdown.js";
import { Menu } from "./components/menu.js";
import { Switch } from "./components/switch.js";
import { Tab } from "./components/tab.js";
import { TabGroup } from "./components/tab-group.js";
import { Tag } from "./components/tag.js";
import { TreeItem } from "./components/tree-item.js";
import { Tree } from "./components/tree.js";
import { Audio, Video } from "./components/media.js";

const mapping = {
  alert: Alert,
  animation: Animation,
  avatar: Avatar,
  badge: Badge,
  breadcrumb_item: BreadcrumbItem,
  button: Button,
  carousel: Carousel,
  chart: Chart,
  checkbox: Checkbox,
  color_picker: ColorPicker,
  details: Details,
  dialog: Dialog,
  drawer: Drawer,
  dropdown: Dropdown,
  form: Form,
  icon_button: IconButton,
  image_comparer: ImageComparer,
  link: Link,
  markdown: Markdown,
  menu: Menu,
  menu_item: MenuItem,
  plaintext: Plaintext,
  radio_group: RadioGroup,
  select: Select,
  slider: Slider,
  switch: Switch,
  tab: Tab,
  tab_group: TabGroup,
  tag: Tag,
  text: Text,
  text_input: TextInput,
  textarea: Textarea,
  tooltip: Tooltip,
  tree_item: TreeItem,
  tree: Tree,
  audio: Audio,
  video: Video,
};

export const getComponentLogic = (name, tag) => {
  if (name in mapping) {
    return mapping[name];
  }
  if (tag.startsWith("sl-")) {
    return ShoelaceComponent;
  }
  if (tag === "hyperdiv-plugin") {
    return Plugin;
  }
  return HtmlComponent;
};
