(() => {
  const exactTitles = Object.freeze({
    "LifeOS HQ": "LifeOS_HQ",
    "Life OS Maintenance HQ": "Maintenance_HQ",
    "Engineering HQ": "Engineering_HQ",
    "Business HQ": "Business_HQ",
    "Office Leaks HQ": "Office_Leaks_HQ",
    "Finance HQ": "Finance_HQ",
    "Chief of Staff HQ": "Chief_of_Staff_HQ",
    "Wellness HQ": "Wellness_HQ",
    "Engineering Worker": "Engineering_Worker",
    "Main Assistant HQ": "Chief_of_Staff_HQ",
    "Logistics HQ": "Maintenance_HQ",
    "Life Logistics HQ": "Maintenance_HQ",
  });

  window.LIFEOS_CANONICAL_ROOM_TITLES = exactTitles;

  function canonicalLabel(value) {
    const text = String(value ?? "");
    const trimmed = text.trim();
    if (Object.hasOwn(exactTitles, trimmed)) {
      return text.replace(trimmed, exactTitles[trimmed]);
    }
    for (const [legacy, canonical] of Object.entries(exactTitles)) {
      if (trimmed.startsWith(`${legacy} ·`)) {
        return text.replace(legacy, canonical);
      }
    }
    return text;
  }

  function rewriteTextNode(node) {
    const current = node.nodeValue || "";
    const canonical = canonicalLabel(current);
    if (canonical !== current) node.nodeValue = canonical;
  }

  function rewriteElement(element) {
    if (element.nodeType === Node.TEXT_NODE) {
      rewriteTextNode(element);
      return;
    }
    if (!(element instanceof Element)) return;
    const walker = document.createTreeWalker(element, NodeFilter.SHOW_TEXT);
    while (walker.nextNode()) rewriteTextNode(walker.currentNode);
  }

  const observer = new MutationObserver((mutations) => {
    for (const mutation of mutations) {
      if (mutation.type === "characterData") rewriteTextNode(mutation.target);
      mutation.addedNodes.forEach(rewriteElement);
    }
  });

  rewriteElement(document.body);
  observer.observe(document.body, {
    childList: true,
    characterData: true,
    subtree: true,
  });
})();
