let cachedRules = null;

export async function normalizeForTTS(text) {
  const rules = await loadPronunciationRules();
  let output = text;
  for (const [source, target] of rules) {
    if (!source || !target) continue;
    output = output.replaceAll(source, target);
  }
  return output;
}

async function loadPronunciationRules() {
  if (cachedRules) return cachedRules;

  const lexiconUrl = new URL("../pronunciation_lexicon.yml", import.meta.url);
  try {
    const response = await fetch(lexiconUrl, { cache: "no-store" });
    if (!response.ok) {
      cachedRules = [];
      return cachedRules;
    }
    cachedRules = parseLexicon(await response.text());
  } catch {
    cachedRules = [];
  }
  return cachedRules;
}

function parseLexicon(source) {
  const rules = [];
  let matches = [];
  let currentWritten = null;
  let inMatchBlock = false;

  for (const rawLine of source.split(/\r?\n/)) {
    const line = rawLine.trim();
    if (!line || line.startsWith("#")) continue;

    if (line.startsWith("- id:")) {
      matches = [];
      currentWritten = null;
      inMatchBlock = false;
      continue;
    }

    if (line.startsWith("- written:")) {
      currentWritten = parseScalar(line.split(":").slice(1).join(":").trim());
      inMatchBlock = false;
      continue;
    }

    if (line.startsWith("preferred_spoken:") && currentWritten) {
      rules.push([currentWritten, parseScalar(line.split(":").slice(1).join(":").trim())]);
      currentWritten = null;
      continue;
    }

    if (line === "match:") {
      inMatchBlock = true;
      continue;
    }

    if (line.startsWith("say_as:")) {
      const target = parseScalar(line.split(":").slice(1).join(":").trim());
      for (const match of matches) {
        rules.push([match, target]);
      }
      matches = [];
      inMatchBlock = false;
      continue;
    }

    if (inMatchBlock && line.startsWith("- ")) {
      matches.push(parseScalar(line.slice(2).trim()));
    }
  }

  return rules.sort((a, b) => b[0].length - a[0].length);
}

function parseScalar(value) {
  const trimmed = value.trim();
  if (trimmed.length >= 2 && trimmed[0] === trimmed[trimmed.length - 1] && ["'", '"'].includes(trimmed[0])) {
    return trimmed.slice(1, -1);
  }
  return trimmed;
}
