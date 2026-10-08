# A4 — Kalendarz treści

Zadanie A4 z [`plan-pracy.md`](./plan-pracy.md). Pół dnia pracy, rozpisane na etapy
z checkboxami.

**Po co:** plan widoczności w Google ([`../tax-polonica/plan-widocznosci-google.md`](../tax-polonica/plan-widocznosci-google.md))
jest dobry, ale jako dokument nie przypomina o sobie. Krok 6 tego planu to **rytm**:
jeden post na wizytówce tygodniowo, jedna prośba o opinię po każdym zamkniętym miesiącu,
jeden nowy tekst na stronie miesięcznie. Rytmu nie da się prowadzić w pliku `.md` —
trzeba widzieć, co zaplanowane, co opublikowane i co przestało działać.

**Efekt:** jedna baza, która odpowiada na pytanie „o czym pisać w tym miesiącu"
i „czy to, co napisałam pół roku temu, cokolwiek przyniosło".

---

## Co już istnieje

Zanim zaczniesz planować nowe teksty — na stronie Tax Polonica jest ich więcej,
niż sugeruje plan widoczności. Stan z kodu (08.10.2026):

| Jest | Gdzie |
|---|---|
| Zmiana biura rachunkowego | `ChangeAccountant` |
| Księgowość dla fundacji i stowarzyszeń | `NonprofitAccounting` |
| Księgowość wspólnot i spółdzielni | `HousingCooperatives` |
| Cennik | `Pricing` |
| FAQ, blog, poradniki | `Faq`, `Blog`/`BlogPost`, `Guides`/`GuideDetail` |
| 9 poradników | `src/data/guides.ts` — m.in. PIT, JPK, VAT-UE, KSeF, spółdzielnie, MŚP |

Czyli trzy z czterech podstron z Kroku 4 planu widoczności już są. Kalendarz ma je
najpierw **zinwentaryzować**, a dopiero potem dokładać nowe.

---

## Etap 0 — przygotowanie (15 min)

- [ ] Otworzyć plan widoczności i wypisać, które kroki są zrobione, a które nie
      (wizytówka Google, opinie, Search Console, katalogi)
- [ ] Zalogować się do Search Console → zakładka **Skuteczność**; to jest źródło
      tematów oparte na faktach, nie na przeczuciu
- [ ] Zdecydować, czy kalendarz obejmuje tylko stronę, czy także posty na wizytówce
      i wpisy w grupach (propozycja: wszystko, bo rytm dotyczy wszystkiego)

---

## Etap 1 — tabela `Treści` (45 min)

| Pole | Typ | Uwagi |
|---|---|---|
| Temat | Single line text | pole główne — sformułowany jako pytanie klienta |
| Rodzaj | Single select | `podstrona` / `poradnik` / `wpis na blogu` / `post na wizytówce` / `odpowiedź w grupie` / `aktualizacja istniejącego` |
| Fraza kluczowa | Single line text | ta, której szuka klient, nie nazwa firmy |
| Intencja | Single select | `informacyjna` / `porównawcza` / `zakupowa` |
| Status | Single select | `pomysł` / `szkic` / `do publikacji` / `opublikowane` / `do odświeżenia` |
| Priorytet | Single select | `wysoki` / `średni` / `niski` |
| Data publikacji | Date | |
| URL | URL | |
| Skąd temat | Single select | `pytanie klienta` / `Search Console` / `grupa na FB` / `zmiana w przepisach` / `własny pomysł` |
| Pozycja w Google | Number | wpisywana ręcznie przy przeglądzie |
| Data sprawdzenia pozycji | Date | |
| Do odświeżenia po | Formula | `DATEADD({Data publikacji}, 6, 'months')` |
| Wyświetlenia | Number | z `site_events`, uzupełniane przy przeglądzie miesięcznym |
| Leady z tej strony | Number | z `contact_leads.referrer` — patrz etap 5 |
| Notatki | Long text | |

- [ ] Utworzyć tabelę z powyższymi polami
- [ ] Sprawdzić formułę `Do odświeżenia po` na jednym rekordzie

---

## Etap 2 — import tego, co już jest (45 min)

- [ ] Wpisać istniejące podstrony (tabela wyżej) ze statusem `opublikowane` i ich URL-ami
- [ ] Wpisać 9 poradników z `src/data/guides.ts`
- [ ] Przenieść z planu widoczności tematy jeszcze niezrobione — m.in.
      `/ksiegowosc-online` — jako `pomysł`
- [ ] Dopisać 3–5 tematów z Search Console: frazy, na które strona **już** się wyświetla,
      a nie ma pod nie osobnego tekstu
- [ ] Przy każdej istniejącej pozycji uzupełnić `Data publikacji`, żeby zadziałał
      licznik odświeżenia

---

## Etap 3 — widoki (20 min)

- [ ] `Kalendarz` — widok Calendar po dacie publikacji
- [ ] `Do napisania` — `Status = szkic` lub `do publikacji`, sortowanie po priorytecie
- [ ] `Bank pomysłów` — `Status = pomysł`, grupowanie po `Skąd temat`
- [ ] `Do odświeżenia` — `Do odświeżenia po < dziś` **i** `Status = opublikowane`
- [ ] `Co działa` — `Status = opublikowane`, sortowanie po `Leady z tej strony` malejąco

Ostatni widok jest najważniejszy po kwartale: pokazuje, które teksty przynoszą zapytania,
a które tylko zajmują miejsce.

---

## Etap 4 — rytm z Kroku 6 jako automatyzacje (40 min)

Plan widoczności mówi „30 minut w tygodniu". Te przypomnienia zamieniają to w nawyk.

| # | Kiedy | Przypomnienie |
|---|---|---|
| 1 | poniedziałek rano | post na wizytówce Google — podpowiedź tematu z widoku `Bank pomysłów` |
| 2 | pierwszy roboczy dzień miesiąca | nowy tekst na stronie: co z widoku `Do napisania` |
| 3 | po zamknięciu miesiąca | poproś zadowolonego klienta o opinię |
| 4 | raz w miesiącu | sprawdź widok `Do odświeżenia` — teksty starsze niż pół roku |

- [ ] Automatyzacje 1 i 2
- [ ] Automatyzacje 3 i 4
- [ ] Ustawić przypomnienie o sprawdzeniu Search Console raz na kwartał

---

## Etap 5 — pomiar: domknięcie pętli (30 min)

Tu kalendarz spina się z zadaniem A3 i z tym, co strona już zbiera.

**Co masz w bazie Tax Polonica:**

- `site_events` — wyświetlenia i zdarzenia (`event_name`, `path`, `label`, `referrer`),
  wypełniane przez `PageViewTracker` i `trackEvent`
- `contact_leads` — zgłoszenia z formularza wraz z `referrer`, czyli adresem podstrony,
  z której przyszły (zadanie B5)
- `guide_leads` — pobrania poradników z `guide_slug`

Czyli da się policzyć, **który tekst przyniósł zapytanie**, a nie tylko ile osób go
otworzyło.

- [ ] Raz w miesiącu: zapytanie o liczbę wyświetleń per `path` z `site_events`
      → wpisać do pola `Wyświetlenia`
- [ ] Raz w miesiącu: liczba rekordów w `contact_leads` per `referrer`
      → pole `Leady z tej strony`
- [ ] Pobrania poradników z `guide_leads` per `guide_slug` → te same pola przy poradnikach
- [ ] Zapisać gotowe zapytania SQL w notatce przy tabeli, żeby nie wymyślać ich co miesiąc

Jeśli to uzupełnianie okaże się uciążliwe, dopiero wtedy warto je zautomatyzować —
nie odwrotnie.

---

## Gotowe, gdy

W pierwszy poniedziałek miesiąca otwierasz jeden widok i wiesz: o czym piszesz w tym
miesiącu, który stary tekst wymaga odświeżenia i który z dotychczasowych przyniósł
najwięcej zapytań. Bez zaglądania do Search Console, do kodu i do skrzynki.

---

## Czego ten kalendarz nie zastąpi

Search Console zostaje jedynym źródłem prawdy o pozycjach i wyświetleniach w Google —
Airtable trzyma tylko odczyty z przeglądu, żeby widzieć trend. Teksty piszesz tam, gdzie
dotąd: w repozytorium strony, zgodnie z zasadami z `taxpolonica/CLAUDE.md` (granica
między czynnością księgową a doradztwem obowiązuje też w blogu).

---

## Plan na pół dnia

| Czas | Co |
|---|---|
| 15 min | Etap 0 — przegląd planu widoczności i Search Console |
| 45 min | Etap 1 — tabela |
| 45 min | Etap 2 — import istniejących treści i pomysłów |
| 20 min | Etap 3 — widoki |
| 40 min | Etap 4 — przypomnienia |
| 30 min | Etap 5 — zapytania do pomiaru |
