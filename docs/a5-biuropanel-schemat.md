# A5 — Schemat BiuroPanelu w Airtable

Zadanie A5 z [`plan-pracy.md`](./plan-pracy.md). Dwa dni na schemat, potem **kwartał
używania na żywych sprawach** — i dopiero wtedy kod.

**Po co tak:** BiuroPanel jest rozwinięciem JPK Mappera (decyzja z `airtable-projekty.md`,
rozdział 2), więc schemat trafi docelowo do Supabase. Zanim to się stanie, warto wiedzieć,
które pola są naprawdę używane, a które tylko wymyślone. Kwartał w Airtable kosztuje dwa
dni; ten sam błąd odkryty po napisaniu panelu kosztuje tygodnie.

**Czego ten etap nie robi:** nie powstaje żaden interfejs dla klientów biura. Airtable
jest tu Twoim narzędziem roboczym, nie produktem.

---

## Punkt wyjścia: co już jest w JPK Mapperze

| Tabela | Co trzyma |
|---|---|
| `companies` | nazwa, NIP, `entity_type`, `entity_size`, `last_mapping_date`, `user_id` |
| `profiles` | `plan_type`, `plan_expiry_date`, `stripe_customer_id` |
| `saved_plans` | zapisany plan kont (`accounts` jako JSONB), `entity_type` |

Jest więc lista firm i historia mapowań. Nie ma **obowiązków i terminów** — a to jest
sedno pracy biura i cała treść BiuroPanelu.

### Trzy rzeczy do rozstrzygnięcia w kodzie (niezależnie od Airtable)

- **B3** — `companies` wisi przy `user_id`, polityki RLS brzmią `auth.uid() = user_id`.
  Lista firm należy do konta, nie do biura: dwie księgowe nie zobaczą tych samych
  klientów. Gotowy wzorzec jest w `platforma-szkolenia`: tabela `czlonek`
  (`organizator_id`, `uzytkownik_id`, `rola` — np. `wlasciciel`, `instruktor`).
  Zgłoszenie [`jpk-tag-finder#1`](https://github.com/chmielmagdalena/jpk-tag-finder/issues/1).
- **B4** — `saved_plans` nie ma `company_id`.
  Zgłoszenie [`jpk-tag-finder#2`](https://github.com/chmielmagdalena/jpk-tag-finder/issues/2).
- **C1** — czym limitowany jest plan BiuroPanelu: liczbą firm, liczbą użytkowników
  w organizacji, czy jednym i drugim?

B3 warto zrobić **przed** migracją schematu z Airtable — dziś dotyczy trzech tabel,
po dołożeniu BiuroPanelu kilkunastu.

---

## Etap 0 — decyzje przed startem (30 min)

- [ ] Wypisz, ilu klientów realnie obsługujesz i jakie mają formy prawne
- [ ] Ustal, czy w biurze pracuje ktoś poza Tobą (to przesądza, jak pilne jest B3)
- [ ] Odpowiedz na **C1** — od tego zależy cennik i limity
- [ ] Granica danych: w Airtable **metadane i statusy**, nigdy dokumenty i kwoty

---

## Etap 1 — sześć tabel (dzień pierwszy, ~4 h)

### `Klienci`

Rozszerzenie tego, co jest w `companies`.

| Pole | Typ |
|---|---|
| Nazwa | Single line text (główne) |
| NIP | Single line text |
| Forma prawna | Single select: `JDG` / `sp. z o.o.` / `fundacja` / `stowarzyszenie` / `spółdzielnia` / `wspólnota` / `inne` |
| Wielkość | Single select: `mikro` / `mała` / `inne` |
| Rodzaj księgowości | Single select: `KPiR` / `ryczałt` / `pełne księgi` |
| Pakiet | Single select + Cena (Currency) |
| Opiekun | Single select / Collaborator |
| Status współpracy | Single select: `onboarding` / `aktywny` / `zawieszony` / `zakończony` |
| Data rozpoczęcia | Date |
| Obowiązki | Link → `Obowiązki` |
| Notatki | Long text (bez danych wrażliwych) |

- [ ] Utworzyć i wypełnić prawdziwymi klientami

### `Obowiązki` — słownik

Wspólny dla wszystkich klientów: co, jak często, do kiedy.

| Pole | Typ |
|---|---|
| Obowiązek | Single line text |
| Cykl | Single select: `miesięczny` / `kwartalny` / `roczny` / `jednorazowy` |
| Termin ustawowy | Single line text (np. „do 25. dnia następnego miesiąca") |
| Dotyczy formy prawnej | Multiple select |
| Wymaga pełnomocnictwa | Checkbox |
| Podstawa | Single line text |

- [ ] Utworzyć tabelę
- [ ] Wypełnić (etap 2)

### `Zadania okresowe`

Klient × obowiązek × okres. To tu dzieje się praca.

| Pole | Typ |
|---|---|
| Nazwa | Formula: klient + obowiązek + okres |
| Klient | Link → `Klienci` |
| Obowiązek | Link → `Obowiązki` |
| Okres | Single line text (`2026-10`) |
| Termin | Date |
| Status | Single select: `dokumenty oczekiwane` / `otrzymane` / `zaksięgowane` / `wysłane` / `potwierdzone` |
| Data wysyłki | Date |
| UPO / potwierdzenie | Checkbox |
| Dni do terminu | Formula: `DATETIME_DIFF({Termin}, TODAY(), 'days')` |

- [ ] Utworzyć tabelę z formułami

### `Dokumenty — metadane`

**Bez plików.** Tylko: co wpłynęło, kiedy, od kogo, czego dotyczy, gdzie leży.

- [ ] Utworzyć tabelę

### `Pełnomocnictwa i dostępy`

UPL-1, ZAW-FA, dostępy do e-US i PUE: zakres, data złożenia, **data ważności**, status.

- [ ] Utworzyć tabelę
- [ ] Widok „wygasające w ciągu 60 dni"

### `Onboarding`

Checklista wdrożenia nowego klienta: umowa, pełnomocnictwa, dostępy, bilans otwarcia,
plan kont, ustalenie obiegu dokumentów.

- [ ] Utworzyć tabelę z szablonem zadań

---

## Etap 2 — wypełnienie słownika obowiązków (dzień drugi, ~2 h)

Jak w zadaniu A2: poniższa lista to **propozycja wyjściowa do weryfikacji**, nie
ustalenie. Terminy i zakres potwierdzasz źródłem — to Ty jesteś tu ekspertem.

### Miesięczne i kwartalne

- [ ] JPK_V7M / JPK_V7K
- [ ] Zaliczki na PIT i CIT
- [ ] Składki ZUS (DRA i rozliczenia pracownicze)
- [ ] PIT-4R / PIT-8AR — zaliczki od wynagrodzeń
- [ ] VAT-UE, gdy występują transakcje wewnątrzwspólnotowe
- [ ] PFRON, jeśli dotyczy

### Roczne

- [ ] Sprawozdanie finansowe (sporządzenie, zatwierdzenie, złożenie)
- [ ] CIT-8 wraz z załącznikami — przy NGO także te specyficzne
- [ ] PIT-36 / PIT-36L / PIT-28
- [ ] PIT-11 dla pracowników i zleceniobiorców
- [ ] Sprawozdawczość GUS
- [ ] Rozliczenie dotacji, gdy klient je otrzymał

### Specyficzne dla form prawnych

- [ ] Fundacje i stowarzyszenia: sprawozdanie merytoryczne, obowiązki wobec ministra
- [ ] Wspólnoty i spółdzielnie: rozliczenie roczne mediów, zebranie roczne
- [ ] KSeF — wpisać jako obowiązek z datą wejścia dla danej grupy klientów

Przy każdym: cykl, termin, czy wymaga pełnomocnictwa i czego dotyczy.

---

## Etap 3 — automatyzacja i widoki (dzień drugi, ~2 h)

Jedna automatyzacja robi tu największą różnicę.

- [ ] **Generowanie miesiąca:** pierwszego dnia miesiąca utwórz komplet `Zadań okresowych`
      dla wszystkich klientów o statusie `aktywny`, na podstawie ich obowiązków
- [ ] Widok `Ten miesiąc` — grupowanie po kliencie
- [ ] Widok `Pali się` — `Dni do terminu < 5` **i** status inny niż `wysłane`/`potwierdzone`
- [ ] Widok `Brak dokumentów` — `Status = dokumenty oczekiwane`, do wysyłki przypomnień
- [ ] Widok `Pełnomocnictwa wygasające`
- [ ] Automatyzacja: 5 dni przed terminem, gdy brak dokumentów → przypomnienie do klienta

---

## Etap 4 — kwartał używania (to jest właściwy test)

Przez trzy miesiące prowadź obsługę **naprawdę w tej bazie**, nie równolegle w głowie.
Co obserwować:

- [ ] Które pola zostają puste przez cały kwartał → kandydaci do usunięcia
- [ ] Czego brakowało i dopisywałaś w notatkach → kandydaci na nowe pola
- [ ] Czy automatyczne generowanie miesiąca daje listę, której nie trzeba poprawiać
- [ ] Które statusy zadania okazały się zbędne, a których brakuje
- [ ] Ile czasu zajmuje aktualizacja statusów — jeśli to męczy, model jest za drobny

Zapisuj te obserwacje w tabeli pomocniczej albo w notatkach — po kwartale to one
są najcenniejsze, nie same dane.

---

## Etap 5 — migracja do Supabase (po kwartale)

| W Airtable | Docelowo |
|---|---|
| `Klienci` | rozszerzenie istniejącej `companies` |
| `Obowiązki` | `obligations` — słownik wspólny |
| `Zadania okresowe` | `periodic_tasks` + zadanie cykliczne generujące miesiąc |
| `Dokumenty — metadane` | `documents`, pliki w Storage |
| `Pełnomocnictwa i dostępy` | `authorizations` |
| `Onboarding` | szablon zadań |

- [ ] Najpierw **B3** (organizacje i członkostwa) — inaczej nowe tabele powielą błąd
      przypisania do konta zamiast do biura
- [ ] Potem **B4** (`saved_plans.company_id`)
- [ ] Eksport tabel do CSV jako specyfikacja migracji
- [ ] Zgłoszenie w `jpk-tag-finder` ze schematem i mapowaniem
- [ ] Po migracji: Airtable przestaje trzymać dane klientów biura

---

## Gotowe, gdy

Po kwartale pierwszego dnia miesiąca otwierasz widok `Ten miesiąc`, dostajesz
wygenerowaną listę zadań, nie poprawiasz jej — i przez cały miesiąc żaden termin
nie przechodzi niezauważony. Wtedy schemat nadaje się do przepisania na Postgresa.

Jeśli listę trzeba co miesiąc poprawiać ręcznie, model obowiązków jest jeszcze
niedokończony i migracja utrwaliłaby ten błąd.

---

## Granica danych na czas pilotażu

W Airtable: nazwy firm, NIP-y, statusy, terminy, metadane dokumentów.
W systemie księgowym: dokumenty, kwoty, dane finansowe, dane pracowników klientów.
Przed pierwszym rekordem: DPA z Airtable i wpis w rejestrze czynności przetwarzania —
to dane kontaktowe i identyfikacyjne Twoich klientów, nie Twoje własne.

---

## Plan na dwa dni

| Dzień | Czas | Co |
|---|---|---|
| 1 | 30 min | Etap 0 — decyzje, w tym C1 |
| 1 | ~4 h | Etap 1 — sześć tabel, wypełnienie `Klientów` |
| 2 | ~2 h | Etap 2 — słownik obowiązków |
| 2 | ~2 h | Etap 3 — generowanie miesiąca i widoki |

Potem kwartał (etap 4) i dopiero migracja (etap 5).
