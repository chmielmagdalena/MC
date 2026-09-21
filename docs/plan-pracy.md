# Plan pracy — punkt wyjścia

Ten plik jest spisem tego, co ustalone i co czeka. Z telefonu wystarczy podać numer
zadania, np. „zrób A2" albo „co z B1?".

Stan na 21.09.2026.

---

## Projekty i ich stan

| Skrót | Projekt | Repozytorium | Stan |
|---|---|---|---|
| **JPK** | JPK CIT Mapper + panel firm | `jpk-tag-finder` | produkcja, plan płatny 99 zł |
| **BP** | BiuroPanel | — (rozwinięcie `jpk-tag-finder`) | decyzja podjęta, projekt przed startem |
| **WIS** | wspólnoty i spółdzielnie | `SmartHousing-Manager` | wczesny prototyp |
| **TP** | strona Tax Polonica | `taxpolonica` | produkcja |
| **MC** | strona wizytówka | `MC` | produkcja |
| **KUR** | kursy i szkolenia AI | — | do uruchomienia, bez kodu |

Decyzje, które już zapadły:

1. **BiuroPanel jest rozwinięciem JPK Mappera**, nie osobnym produktem — jeden Supabase,
   jedna subskrypcja, wspólna tabela `companies`.
2. **Airtable pełni rolę back-office'u.** Nie jest bazą żadnego produktu ani CMS-em stron.
3. **WIS nie dostaje prawdziwych danych** do czasu naprawy dostępu do API.

---

## A. Airtable — do wdrożenia

| # | Zadanie | Czas | Gdzie opisane |
|---|---|---|---|
| A1 | Baza kursów: tabele, formularz zapisu, automatyzacje mailowe | 1 dzień | [`airtable-kursy.md`](./airtable-kursy.md) |
| A2 | Katalog reguł rozliczeniowych WIS (klucze podziału kosztów) | po godzinie dziennie przez 2–3 tygodnie | **[`a2-katalog-regul-wis.md`](./a2-katalog-regul-wis.md)** — rozpisane z checkboxami |
| A3 | Rejestr leadów ze stron | pół dnia | [`airtable-projekty.md`](./airtable-projekty.md#4-strony-internetowe) |
| A4 | Kalendarz treści (przeniesienie planu widoczności) | pół dnia | [`airtable-projekty.md`](./airtable-projekty.md#4-strony-internetowe) |
| A5 | Schemat BiuroPanelu w Airtable + kwartał używania na żywych sprawach | 2 dni + kwartał | [`airtable-projekty.md`](./airtable-projekty.md#2-biuropanel--rozwinięcie-jpk-mappera) |

Kolejność nie jest przypadkowa: **A1 zarabia od razu**, **A2 jest najcenniejszym zasobem
i nie wymaga ani linijki kodu**, reszta może poczekać.

Przed pierwszym rekordem w Airtable: podpisana umowa powierzenia (DPA), wpis w rejestrze
czynności przetwarzania, informacja w polityce prywatności o przetwarzaniu poza EOG.

---

## B. Kod — zgłoszenia na GitHubie

| # | Czego dotyczy | Projekt | Zgłoszenie |
|---|---|---|---|
| B1 | dostęp do danych w prototypie — **blokuje wprowadzenie prawdziwych danych** | WIS | [`SmartHousing-Manager#1`](https://github.com/chmielmagdalena/SmartHousing-Manager/issues/1) |
| B2 | błąd blokujący kompilację | WIS | [`SmartHousing-Manager#2`](https://github.com/chmielmagdalena/SmartHousing-Manager/issues/2) |
| B3 | organizacje i członkostwa zamiast konta jako właściciela firm | JPK / BP | [`jpk-tag-finder#1`](https://github.com/chmielmagdalena/jpk-tag-finder/issues/1) |
| B4 | powiązanie zapisanego planu kont z firmą | JPK | [`jpk-tag-finder#2`](https://github.com/chmielmagdalena/jpk-tag-finder/issues/2) |
| B5 | zapis zgłoszeń z formularza kontaktowego do bazy | TP | [`taxpolonica#15`](https://github.com/chmielmagdalena/taxpolonica/issues/15) |

**B1 ma pierwszeństwo przed wszystkim innym w WIS.** B3 warto zrobić przed dokładaniem
kolejnych tabel — dziś dotyczy trzech, za rok kilkunastu.

---

## C. Do rozstrzygnięcia

| # | Pytanie | Kogo dotyczy |
|---|---|---|
| C1 | Czym limitowany jest plan BiuroPanelu — liczbą firm, liczbą użytkowników w organizacji, czy jednym i drugim? | BP |
| C2 | Czy szkolenia są zwolnione z VAT w Twoim przypadku? Wpływa na cennik i formularz zapisu. | KUR |
| C3 | Czy WIS celuje w zarządców (kilkadziesiąt wspólnot), czy w samodzielne wspólnoty? Inny produkt, inna cena, inny onboarding. | WIS |

---

## Jak wydawać komendy z telefonu

Wystarczy numer zadania i czasownik:

- „zrób B5" — wejdę w repozytorium, zrobię zmianę, wypchnę na gałąź i otworzę PR
- „co z B1?" — sprawdzę stan zgłoszenia i powiem, co zostało
- „rozpisz A2" — przygotuję gotowy schemat tabeli do skopiowania do Airtable
- „dopisz C4: <pytanie>" — dołożę pozycję do listy

Czego nie zrobię bez Twojego potwierdzenia: scalenia PR-a, zmian w treściach
opublikowanych stron, niczego, co dotyka prawdziwych danych klientów.

---

## Dokumenty

- [`airtable-kursy.md`](./airtable-kursy.md) — pełny schemat bazy dla szkoleń
- [`a2-katalog-regul-wis.md`](./a2-katalog-regul-wis.md) — zadanie A2 rozpisane na etapy
- [`airtable-projekty.md`](./airtable-projekty.md) — przegląd wszystkich projektów
- `tax-polonica/` — teksty, plan widoczności w Google, poradnik PDF
