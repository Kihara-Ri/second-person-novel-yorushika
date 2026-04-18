#!/bin/zsh
set -euo pipefail

required_major=22
required_minor=12

version_ok() {
  local version="$1"
  version="${version#v}"
  local major="${version%%.*}"
  local rest="${version#*.}"
  local minor="${rest%%.*}"

  if (( major > required_major )); then
    return 0
  fi
  if (( major == required_major && minor >= required_minor )); then
    return 0
  fi
  return 1
}

pick_node() {
  local candidates=(
    "${HOME}/.nvm/versions/node/v22.22.1/bin/node"
    "/opt/homebrew/bin/node"
    "$(command -v node 2>/dev/null || true)"
  )

  local candidate
  for candidate in "${candidates[@]}"; do
    [[ -n "${candidate}" ]] || continue
    [[ -x "${candidate}" ]] || continue
    local version
    version="$("${candidate}" -v 2>/dev/null || true)"
    [[ -n "${version}" ]] || continue
    if version_ok "${version}"; then
      echo "${candidate}"
      return 0
    fi
  done

  echo "No suitable Node.js found. Need >= 22.12.0." >&2
  return 1
}

NODE_BIN="$(pick_node)"
exec "${NODE_BIN}" "$@"
