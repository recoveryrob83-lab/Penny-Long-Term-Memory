(() => {
  const SERVER_UNAVAILABLE_MESSAGE = (
    "Dashboard server is unavailable. Restart the server, then reload this page."
  );
  const originalFetch = window.fetch.bind(window);
  let serverUnavailable = false;

  const setText = (id, value) => {
    const element = document.getElementById(id);
    if (element) element.textContent = value;
  };

  const showServerToast = () => {
    const toast = document.getElementById("toast");
    if (!toast) return;
    toast.textContent = SERVER_UNAVAILABLE_MESSAGE;
    toast.classList.add("visible");
    window.setTimeout(() => toast.classList.remove("visible"), 5000);
  };

  const markServerUnavailable = () => {
    document.body.dataset.lifeosServer = "unavailable";
    setText("cc-status", "Server offline");
    setText("cc-scheduler-status", "Server offline");
    setText("cc-summary", SERVER_UNAVAILABLE_MESSAGE);
    setText("cc-schedule-summary", SERVER_UNAVAILABLE_MESSAGE);
    setText("dashboard-subtitle", "The local dashboard server is unavailable.");
    setText("snapshot-state", "Server unavailable");
    if (!serverUnavailable) showServerToast();
    serverUnavailable = true;
  };

  const markServerReachable = () => {
    document.body.dataset.lifeosServer = "reachable";
    serverUnavailable = false;
  };

  window.fetch = async (...args) => {
    try {
      const response = await originalFetch(...args);
      markServerReachable();
      return response;
    } catch (error) {
      markServerUnavailable();
      const unavailableError = new Error(SERVER_UNAVAILABLE_MESSAGE);
      unavailableError.name = "LifeOSServerUnavailableError";
      unavailableError.cause = error;
      throw unavailableError;
    }
  };

  window.LifeOSServerAvailability = {
    message: SERVER_UNAVAILABLE_MESSAGE,
    isUnavailable: () => serverUnavailable,
    markServerUnavailable,
  };
})();
