(function () {
  const scriptUrl = document.currentScript && document.currentScript.src;
  if (!scriptUrl) return;

  const statusUrl = new URL("../source-status.json", scriptUrl).toString();

  function shortSha(value) {
    return value ? value.slice(0, 12) : "—";
  }

  function render(data) {
    const host = document.getElementById("docs-source-status");
    if (!host) return;

    const status = String(data.status || "UNKNOWN").toUpperCase();
    const cssStatus = ["CURRENT", "OUTDATED", "UNKNOWN"].includes(status) ? status.toLowerCase() : "unknown";
    const current = data.current_source_sha || "unavailable";
    const documented = data.documented_source_sha || "unavailable";

    host.className = "docs-freshness docs-freshness--" + cssStatus;
    host.innerHTML =
      '<div class="docs-freshness__header">' +
        '<span class="docs-freshness__dot"></span>' +
        '<strong>Docs ' + status + '</strong>' +
      '</div>' +
      '<div class="docs-freshness__body">' +
        '<div><span>Documented source</span><code>' + shortSha(documented) + '</code></div>' +
        '<div><span>Current main</span><code>' + shortSha(current) + '</code></div>' +
        '<div><span>Baseline</span><code>Core ' + (data.core || "—") + ' · ' + (data.schema || "—") + ' · ABI ' + (data.abi || "—") + '</code></div>' +
        '<div class="docs-freshness__reason">' + (data.reason || "") + '</div>' +
      '</div>';
  }

  fetch(statusUrl, { cache: "no-store" })
    .then(function (response) {
      if (!response.ok) throw new Error("status HTTP " + response.status);
      return response.json();
    })
    .then(render)
    .catch(function (error) {
      render({
        status: "UNKNOWN",
        reason: "Не вдалося завантажити freshness status: " + error.message
      });
    });
})();
