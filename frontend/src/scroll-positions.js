let scrollPositionsByLocation = {};

// Helper function to find all scrollable containers
function getAllElements() {
  const scrollables = [];
  document.querySelectorAll("*").forEach((el) => {
    if (el.id) {
      scrollables.push(el);
    }
  });
  return scrollables;
}

// Gets the current scroll positions of all scrollable containers.
export function getScrollPositions() {
  const scrollPositions = {};
  const containers = getAllElements();
  containers.forEach((container) => {
    scrollPositions[container.id] = container.scrollTop;
  });
  return scrollPositions;
}

// Saves the current scroll positions for the given location.
export function saveScrollPositionsForLocation(location) {
  scrollPositionsByLocation[location] = getScrollPositions();
}

// Restores the scroll positions for a given location. If
// `scrollPositions` is not null, it restores the positions from the
// given `scrollPositions` object. Otherwise it restores the positions
// from the global scroll positions object.
export function restoreScrollPositionsForLocation(
  location,
  scrollPositions = null
) {
  if (scrollPositions) {
    scrollPositions[location] = scrollPositions;
  } else {
    scrollPositions = scrollPositionsByLocation[location];
  }
  if (scrollPositions) {
    const containers = getAllElements();
    containers.forEach((container) => {
      if (container.id in scrollPositions) {
        const savedPosition = scrollPositions[container.id];
        container.scrollTop = savedPosition;
      }
    });
  }
}

export function clearScrollCache() {
  scrollPositionsByLocation = {};
}
