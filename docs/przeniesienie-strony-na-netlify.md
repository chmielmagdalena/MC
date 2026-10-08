# Przeniesienie strony MC z GitHub Pages na Netlify

Cel: strona wizytówka ma działać dalej, a repozytorium `MC` ma stać się **prywatne**.
Na darmowym planie GitHuba Pages działa wyłącznie z repozytoriów publicznych, więc
hosting musi się przeprowadzić **zanim** zmienisz widoczność.

Netlify obsługuje prywatne repozytoria w planie darmowym — tak samo stoi już
`taxpolonica`.

---

## Co jest przygotowane w repozytorium

| Plik | Po co |
|---|---|
| `scripts/build-site.sh` | kopiuje do katalogu `site/` **wyłącznie** `index.html`, `style.css` i `script.js` |
| `netlify.toml` | mówi Netlify, żeby uruchomił ten skrypt i opublikował katalog `site/` |
| `.gitignore` | `site/` nie trafia do repozytorium — powstaje przy każdym wdrożeniu |

**Dlaczego nie publikujemy katalogu głównego:** wtedy pod adresem strony dostępne
byłyby też `docs/` i `tax-polonica/`, czyli dokumenty robocze i teksty marketingowe.
Przy takim ustawieniu prywatne repozytorium niewiele by dało.

---

## Kolejność — ważna

- [ ] **1. Netlify: nowa strona z repozytorium**
      `Add new site` → `Import an existing project` → `GitHub` → wybierz `MC`.
      Przy pierwszym podłączeniu Netlify poprosi o dostęp do repozytoriów — wystarczy
      zaznaczyć samo `MC`.

- [ ] **2. Ustawienia budowania** (powinny podstawić się z `netlify.toml`):
      - Branch: `main`
      - Build command: `bash scripts/build-site.sh`
      - Publish directory: `site`

- [ ] **3. Deploy i sprawdzenie**
      Otwórz adres `*.netlify.app`. Sprawdź: strona się ładuje, style działają,
      a `TWÓJ-ADRES.netlify.app/docs/plan-pracy.md` zwraca **404**. Jeśli zwraca plik,
      publikowany jest zły katalog — zatrzymaj się tutaj.

- [ ] **4. Adres strony**
      - Masz własną domenę → `Domain management` → dodaj ją i przepnij DNS zgodnie
        z instrukcją Netlify; dopiero po propagacji przejdź dalej.
      - Używasz adresu `chmielmagdalena.github.io/MC` → **ten adres przestanie
        działać** po zmianie na prywatne. Zmień go wszędzie, gdzie go podałaś:
        wizytówka Google, LinkedIn, podpis w mailu, profile w katalogach.
        Najlepsza chwila, żeby przejść na własną domenę.

- [ ] **5. Dopiero teraz: wyłącz GitHub Pages**
      `Settings` → `Pages` → źródło na `None`.

- [ ] **6. Zmień repozytorium na prywatne**
      `Settings` → `General` → `Danger Zone` → `Change visibility` → `Make private`.

- [ ] **7. Sprawdzenie po zmianie**
      - strona na Netlify nadal działa (zrób próbny commit, sprawdź czy wdrożenie rusza)
      - `github.com/chmielmagdalena/MC` otwarty w oknie incognito daje 404

---

## O czym pamiętać

**Historia pozostaje publiczna do momentu zmiany.** Repozytorium było publiczne od
początku, więc wszystko, co w nim było, mogło zostać skopiowane lub zaindeksowane.
Zmiana widoczności działa od teraz, nie wstecz. Nie ma tam haseł ani kluczy —
sprawdzałam — więc nie jest to pilne, ale warto o tym wiedzieć.

**Linki do plików w repozytorium przestaną działać** dla osób bez dostępu. Jeśli
gdzieś podałaś odnośnik do poradnika PDF z `tax-polonica/poradniki/`, przenieś plik
na stronę albo na Drive.

**Netlify buduje przy każdym pushu do `main`** — także wtedy, gdy zmieniasz tylko
dokumenty w `docs/`. To bez znaczenia (budowanie trwa sekundy), ale nie dziw się
powiadomieniom o wdrożeniu po commicie z samą dokumentacją.
