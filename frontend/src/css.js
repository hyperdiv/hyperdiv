// `ruleCache` holds an in-memory mapping of CSS selectors -> CSS rule
// DOM objects, so they can be quickly updated.
let ruleCache = {};
window.ruleCache = ruleCache;

function findHyperdivStyleSheet() {
  for (let i = 0; i < document.styleSheets.length; i++) {
    const styleSheet = document.styleSheets[i];
    if (styleSheet.ownerNode.id === "hyperdiv-styles") {
      return styleSheet;
    }
  }
  return null;
}

let cachedStyleSheet = null;

function getStyleSheet() {
  if (!cachedStyleSheet) {
    cachedStyleSheet = findHyperdivStyleSheet();
  }
  return cachedStyleSheet;
}

function updateSelector(selector, style) {
  const styleSheet = getStyleSheet();

  if (selector in ruleCache) {
    ruleCache[selector].style.cssText = style;
  } else {
    const styleSheetLength = styleSheet.cssRules
      ? styleSheet.cssRules.length
      : 0;
    styleSheet.insertRule(selector + "{" + style + "}", styleSheetLength);
    ruleCache[selector] = styleSheet.cssRules[styleSheetLength];
  }
}

// `cssCache` holds an in-memory mapping of Hyperdiv component key ->
// dictionary of style selectors at that key.
let cssCache = {};
window.cssCache = cssCache;

export function updateStyle(key, style) {
  if (typeof style === "undefined") {
    return;
  }

  const keyCache = cssCache[key] || {};

  const toRemove = new Set();

  for (const selector of Object.keys(keyCache)) {
    if (!(selector in style)) {
      toRemove.add(selector);
      delete keyCache[selector];
    }
  }

  removeSelectors(toRemove);

  for (const selector of Object.keys(style)) {
    if (keyCache[selector] !== style[selector]) {
      updateSelector(selector, style[selector]);
      keyCache[selector] = style[selector];
    }
  }

  if (Object.keys(keyCache).length > 0) {
    cssCache[key] = keyCache;
  } else {
    delete cssCache[key];
  }
}

function removeSelectors(selectors) {
  const styleSheet = getStyleSheet();

  if (selectors.size === 0) {
    return;
  }

  let i = 0;
  while (true) {
    if (i >= styleSheet.rules.length) {
      break;
    }
    const rule = styleSheet.rules[i];
    if (selectors.has(rule.selectorText)) {
      styleSheet.deleteRule(i);
      delete ruleCache[rule.selectorText];
    } else {
      i++;
    }
  }
}

export function removeStyles(keys) {
  const selectors = new Set();
  for (const key of keys) {
    const cachedStyle = cssCache[key];
    if (!cachedStyle) {
      continue;
    }

    for (const selector of Object.keys(cachedStyle)) {
      selectors.add(selector);
    }
  }

  removeSelectors(selectors);

  for (const key of keys) {
    delete cssCache[key];
  }
}

export function removeAllStyles() {
  const styleSheet = getStyleSheet();
  let numStyles = styleSheet.rules.length;

  while (numStyles > 0) {
    styleSheet.deleteRule(0);
    numStyles -= 1;
  }

  ruleCache = {};
  window.ruleCache = ruleCache;

  cssCache = {};
  window.cssCache = cssCache;
}
