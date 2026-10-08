#!/usr/bin/env bash
# Przygotowuje katalog publikacji dla Netlify.
#
# Do sieci trafiają wyłącznie pliki wymienione niżej. Reszta repozytorium
# (docs/, tax-polonica/, README) zostaje poza katalogiem publikacji, więc
# nie jest dostępna pod żadnym adresem.
set -euo pipefail

PLIKI=(index.html style.css script.js)
KATALOG=site

rm -rf "$KATALOG"
mkdir -p "$KATALOG"

for plik in "${PLIKI[@]}"; do
  if [[ ! -f "$plik" ]]; then
    echo "Brak pliku: $plik" >&2
    exit 1
  fi
  cp "$plik" "$KATALOG/"
done

echo "Opublikowane pliki:"
ls -1 "$KATALOG"
