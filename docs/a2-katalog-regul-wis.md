# A2 — Katalog reguł rozliczeniowych WIS

Zadanie A2 z [`plan-pracy.md`](./plan-pracy.md). Robota do odhaczania: schemat tabeli,
lista pozycji do wypełnienia, przypadki brzegowe, definicja ukończenia.

**Po co:** prototyp WIS przyjmuje dziś ręcznie wpisaną kwotę obciążenia — nie ma
naliczania, bo nie ma reguł. Ten katalog jest tą brakującą warstwą. Powstaje w Airtable,
bo tam poprawia się go w minutę, a kończy jako specyfikacja dla kodu.

**Zasada:** kolumna „Klucz podziału" w tabelach niżej to **propozycja wyjściowa**, nie
ustalenie. Podstawą jest zawsze uchwała wspólnoty, statut i regulamin spółdzielni albo
umowa z dostawcą. Odhaczasz pozycję dopiero wtedy, gdy klucz jest potwierdzony
źródłem — to Ty jesteś tu ekspertem, ja podaję punkt wyjścia do skreślania.

Realny czas: **po godzinie dziennie przez 2–3 tygodnie.** Nie da się tego zrobić
w jeden wieczór i nie warto próbować — połowa wartości siedzi w przypadkach brzegowych,
które przypominają się dopiero przy konkretnej pozycji.

---

## Etap 0 — przygotowanie (30 min)

- [ ] Założyć bazę w Airtable: `WIS — reguły rozliczeniowe`
- [ ] Przygotować pod ręką: jedną prawdziwą uchwałę o kosztach, jeden regulamin
      rozliczania mediów, jedno roczne rozliczenie, które robiłaś
- [ ] Ustalić, że w tej bazie **nie ma żadnych danych mieszkańców** — same reguły

---

## Etap 1 — tabela `Pozycje kosztowe` (45 min)

Pola do utworzenia:

| Pole | Typ | Opcje / uwagi |
|---|---|---|
| Pozycja | Single line text | pole główne |
| Kategoria | Single select | `media` / `eksploatacja` / `fundusz` / `administracja` / `podatki i opłaty` / `pożytki` |
| Klucz podziału | Single select | `udział` / `powierzchnia` / `liczba osób` / `licznik` / `ryczałt od lokalu` / `po równo` / `inny — opis` |
| Klucz — opis | Long text | gdy `inny`, albo gdy klucz ma warunki |
| Podstawa | Single select | `ustawa` / `uchwała wspólnoty` / `statut spółdzielni` / `regulamin` / `umowa z dostawcą` |
| Podstawa — odesłanie | Single line text | konkretny przepis, numer uchwały, paragraf regulaminu |
| Dotyczy | Multiple select | `wspólnota` / `spółdzielnia` |
| Zaliczkowo | Checkbox | czy pobierana jest zaliczka, czy rozliczenie następcze |
| Rozliczenie roczne | Single select | `nadpłata/niedopłata` / `przeksięgowanie` / `zwrot` / `nie dotyczy` |
| Przypadki brzegowe | Link → `Przypadki brzegowe` | |
| Status | Single select | `do opisania` / `opisana` / `potwierdzona źródłem` / `zaimplementowana w WIS` |
| Notatki z praktyki | Long text | „u zarządcy X robi się to tak, bo…" |

- [ ] Utworzyć tabelę z powyższymi polami
- [ ] Utworzyć drugą tabelę `Przypadki brzegowe`: `Opis`, `Dotyczy pozycji` (link),
      `Jak rozstrzygamy` (long text), `Źródło`, `Status`
- [ ] Widok `Do opisania` — filtr `Status = do opisania`
- [ ] Widok `Gotowe do implementacji` — filtr `Status = potwierdzona źródłem`

---

## Etap 2 — pozycje kosztowe do opisania

Propozycja wyjściowa. Klucz potwierdzasz albo poprawiasz; odhaczasz po potwierdzeniu
źródłem.

### Media

- [ ] **Woda zimna i ścieki** — propozycja: `licznik`; bez licznika `liczba osób`
- [ ] **Woda ciepła — zużycie** — propozycja: `licznik` (ciepłej wody)
- [ ] **Woda ciepła — podgrzanie** — propozycja: `licznik`; część stała często `powierzchnia`
- [ ] **Centralne ogrzewanie** — propozycja: podzielniki, a bez nich `powierzchnia`
- [ ] **Gaz z instalacji zbiorczej** — propozycja: `liczba osób` albo `licznik`
- [ ] **Energia elektryczna części wspólnych** — propozycja: `udział`
- [ ] **Wywóz odpadów** — zależy od uchwały gminy: `liczba osób` / `gospodarstwo` /
      `powierzchnia` / od zużycia wody

### Eksploatacja

- [ ] **Sprzątanie i utrzymanie czystości** — propozycja: `udział`
- [ ] **Konserwacja bieżąca** (hydraulik, elektryk, ślusarz) — propozycja: `udział`
- [ ] **Przeglądy okresowe** (gazowy, kominiarski, elektryczny, budowlany) — `udział`
- [ ] **Winda** — `udział`; sprawdzić, czy uchwała zwalnia parter
- [ ] **Domofon, brama, monitoring** — `udział`
- [ ] **Teren zielony, odśnieżanie** — `udział`
- [ ] **Antena zbiorcza / TV** — `ryczałt od lokalu` albo `po równo`

### Fundusze i administracja

- [ ] **Fundusz remontowy** — propozycja: `udział`; bywa `powierzchnia` wg uchwały
- [ ] **Zarządzanie / administrowanie** — `ryczałt od lokalu` albo od m²
- [ ] **Księgowość** — `ryczałt`
- [ ] **Koszty bankowe, pocztowe, materiały biurowe** — `udział`
- [ ] **Ubezpieczenie nieruchomości** — `udział`

### Podatki, opłaty, pożytki

- [ ] **Podatek od nieruchomości — części wspólne** — `udział`
- [ ] **Opłata za użytkowanie wieczyste gruntu** — `udział`
- [ ] **Pożytki** (reklama na elewacji, maszt, najem pomieszczenia) — jak dzielone
      i czy pomniejszają koszty, czy zasilają fundusz
- [ ] **Odsetki za zwłokę** — sposób naliczania i od kiedy

---

## Etap 3 — przypadki brzegowe

Ta część decyduje o tym, czy program liczy poprawnie. Każdy punkt to osobny rekord
w tabeli `Przypadki brzegowe` z rozstrzygnięciem.

### Lokale

- [ ] **Lokale użytkowe** — inne stawki, VAT, podstawa w uchwale
- [ ] **Garaże, miejsca postojowe, komórki** — czy mają udział, czy płacą osobno
- [ ] **Pustostany i lokale niesprzedane** — kto płaci, deweloper czy wspólnota
- [ ] **Lokal z własnym źródłem ciepła** — wyłączenie z CO i co z częścią stałą

### Zmiany w czasie

- [ ] **Zmiana właściciela w trakcie roku** — podział kosztów i rozliczenia rocznego
      (proporcjonalnie do dni? na dzień aktu?), kto dostaje nadpłatę
- [ ] **Zmiana liczby osób w trakcie okresu** — od którego miesiąca liczymy
- [ ] **Zmiana stawki w trakcie roku** — jak liczyć okres przejściowy
- [ ] **Wymiana licznika** — jak zsumować stan starego i nowego

### Liczniki i różnice

- [ ] **Brak odczytu** — ryczałt zastępczy: średnia z ilu okresów?
- [ ] **Licznik zepsuty lub po terminie legalizacji** — od kiedy szacujemy
- [ ] **Różnica bilansowa wody** — suma liczników mieszkaniowych mniejsza niż główny;
      jak dzielimy różnicę (udział, liczba osób, proporcjonalnie do zużycia)
- [ ] **Podejrzenie nielegalnego poboru** — jak to ujmujemy księgowo

### Rozliczenie roczne

- [ ] **Nadpłata** — zwrot czy zaliczenie na kolejne okresy, od jakiej kwoty zwrot
- [ ] **Niedopłata** — termin zapłaty, rozłożenie na raty
- [ ] **Korekta stawek zaliczek** — przy jakiej rozbieżności i od kiedy obowiązuje
- [ ] **Zaległości** — kiedy odsetki, kiedy wezwanie, kiedy windykacja

---

## Etap 4 — różnice wspólnota / spółdzielnia

Osobny przebieg przez katalog, bo to nie są te same reguły.

- [ ] Oznaczyć w polu `Dotyczy`, które pozycje są wspólne, a które rozłączne
- [ ] Opisać **ewidencję per nieruchomość** w spółdzielni i to, co z niej wynika
      dla kluczy podziału
- [ ] Opisać różnicę między **udziałem w nieruchomości wspólnej** (wspólnota)
      a **powierzchnią użytkową** jako podstawą rozliczeń w spółdzielni
- [ ] Opisać tytuły prawne do lokalu w spółdzielni (własnościowe, lokatorskie, najem,
      odrębna własność) i to, czy zmieniają zestaw opłat
- [ ] Zaznaczyć pozycje, których w ogóle nie ma po jednej ze stron

---

## Etap 5 — zamknięcie i przekazanie do kodu

- [ ] Przejrzeć widok `Do opisania` — ma być pusty
- [ ] Dla każdej pozycji: klucz, podstawa z odesłaniem, sposób rozliczenia rocznego
      i **co najmniej jeden przypadek brzegowy**
- [ ] Eksport tabel do CSV
- [ ] Nowe zgłoszenie w `SmartHousing-Manager`: „Model naliczeń — specyfikacja
      z katalogu reguł", z CSV w załączniku
- [ ] Dopisać do zgłoszenia, jakich encji brakuje dziś w schemacie:
      `Lokal` (powierzchnia, udział, typ), `Stawki i zaliczki`, `Naliczenia`,
      `Klucze podziału`, `Okresy rozliczeniowe`

---

## Gotowe, gdy

Bierzesz dowolną pozycję kosztową z prawdziwego rozliczenia, które kiedyś robiłaś,
i znajdujesz w katalogu komplet: klucz, podstawę, sposób rozliczenia rocznego
i rozstrzygnięcie przypadku brzegowego, który przy niej wystąpił.

Jeśli czegoś brakuje — katalog jeszcze nie jest gotowy. Jeśli jest komplet, masz
specyfikację, z której da się napisać moduł naliczeń bez dopytywania.

---

## Jak to wraca do kodu WIS

Katalog nie jest dokumentem do szuflady — przekłada się wprost na tabele:

| W katalogu | W bazie WIS |
|---|---|
| Pozycja kosztowa | `cost_items` — słownik |
| Klucz podziału | `allocation_keys` + `cost_item_allocation` (klucz może zależeć od wspólnoty) |
| Zaliczkowo, stawka | `advance_rates` — stawka per lokal i okres |
| Rozliczenie roczne | `settlements` — okres, koszt rzeczywisty, suma zaliczek, wynik |
| Przypadki brzegowe | przypadki testowe modułu naliczeń |

Ostatni wiersz jest najważniejszy: **każdy przypadek brzegowy z katalogu to jeden test.**
Moduł, który je przechodzi, liczy poprawnie — i to jest jedyny sensowny sposób, żeby
to sprawdzić przed wpuszczeniem prawdziwej wspólnoty.
