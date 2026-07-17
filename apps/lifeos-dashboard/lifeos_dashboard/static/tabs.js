const tabButtons = Array.from(document.querySelectorAll("[data-tab-target]"));
const tabPanels = Array.from(document.querySelectorAll("[data-tab-panel]"));

const activateTab = (target) => {
  tabButtons.forEach((button) => {
    const active = button.dataset.tabTarget === target;
    button.classList.toggle("active", active);
    button.setAttribute("aria-selected", String(active));
    button.tabIndex = active ? 0 : -1;
  });

  tabPanels.forEach((panel) => {
    const active = panel.dataset.tabPanel === target;
    panel.hidden = !active;
  });

  window.localStorage.setItem("lifeos-active-tab", target);
};

tabButtons.forEach((button, index) => {
  button.addEventListener("click", () => activateTab(button.dataset.tabTarget));
  button.addEventListener("keydown", (event) => {
    if (!["ArrowLeft", "ArrowRight"].includes(event.key)) return;
    event.preventDefault();
    const direction = event.key === "ArrowRight" ? 1 : -1;
    const next = (index + direction + tabButtons.length) % tabButtons.length;
    tabButtons[next].focus();
    activateTab(tabButtons[next].dataset.tabTarget);
  });
});

const remembered = window.localStorage.getItem("lifeos-active-tab");
const initial = tabButtons.some((button) => button.dataset.tabTarget === remembered)
  ? remembered
  : "overview";
activateTab(initial);
