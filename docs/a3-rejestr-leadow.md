# A3 — Rejestr leadów ze stron

Zadanie A3 z [`plan-pracy.md`](./plan-pracy.md). Pół dnia pracy, rozpisane na etapy
z checkboxami.

**Po co:** dziś zgłoszenia z formularza kontaktowego Tax Polonica istnieją **wyłącznie
w skrzynce pocztowej** — funkcja `contact-form` wysyła maila i nie zapisuje nic.
Nie policzysz, ile ich było w miesiącu, nie sprawdzisz, które obsłużyłaś, nie zobaczysz,
z której podstrony przyszły. Jeśli mail wpadnie do spamu, zgłoszenie znika bez śladu.

**Efekt:** jedno miejsce, w którym widać wszystkie zapytania ze wszystkich stron, ich
status obsługi i czas odpowiedzi.

---

## Skąd realnie przychodzą zgłoszenia

Stan na 08.10.2026, z kodu:

| Źródło | Co się dzieje dziś | Czy coś zostaje |
|---|---|---|
| Formularz kontaktowy Tax Polonica (`ContactForm` → `contact-form`) | wysyłka maila | **nic** |
| Pobranie poradnika (`GuideDownloadForm` → `guide-download`) | mail + zapis | tabela `guide_leads` (e-mail, imię, `guide_slug`, zgoda, `referrer`) |
| Rezerwacja konsultacji (`BookingSection`) | przekierowanie do Calendly | wpis w Calendly |
| Strona MC | `mailto:` — brak formularza | mail w skrzynce |

Czyli jedno źródło zapisuje, jedno gubi, dwa żyją poza Twoją kontrolą. Rejestr ma je
zebrać w całość.

---

## Etap 0 — decyzje przed startem (20 min)

- [ ] Ustal **SLA**: w ciągu ilu godzin roboczych odpowiadasz na zapytanie? (propozycja: 24 h)
- [ ] Ustal, które źródła wchodzą w pierwszej wersji — minimum formularz kontaktowy
      i poradnik; Calendly i `mailto` mogą dojść później
- [ ] Zdecyduj, czy rejestr obejmuje też zapytania z LinkedIn i telefonu (wpisywane ręcznie)

---

## Etap 1 — tabela `Leady` (40 min)

Jedna tabela, bez relacji — rejestr ma być prosty, inaczej nie będziesz go uzupełniać.

| Pole | Typ | Uwagi |
|---|---|---|
| Kto | Single line text | pole główne: imię i nazwisko albo firma |
| E-mail | Email | |
| Telefon | Phone | |
| Firma | Single line text | |
| Treść zapytania | Long text | |
| Źródło | Single select | `formularz TP` / `poradnik` / `Calendly` / `mail MC` / `LinkedIn` / `telefon` / `polecenie` |
| Podstrona | URL | z której strony przyszło (`referrer`) |
| Czego dotyczy | Single select | `księgowość` / `NGO` / `dotacje` / `KSeF` / `szkolenie` / `inne` |
| Data wpływu | Created time | |
| Termin odpowiedzi | Formula | `DATEADD({Data wpływu}, 1, 'days')` — albo wg ustalonego SLA |
| Status | Single select | `nowy` / `w trakcie` / `odpowiedziano` / `spotkanie` / `klient` / `odrzucony` / `brak odpowiedzi` |
| Data pierwszej odpowiedzi | Date | |
| Czas reakcji (h) | Formula | `DATETIME_DIFF({Data pierwszej odpowiedzi}, {Data wpływu}, 'hours')` |
| Wartość szacunkowa | Currency | wypełniane przy `spotkanie` i dalej |
| Zgoda marketingowa | Checkbox | |
| Data i treść zgody | Date + Long text | dowód zgody — wymagane, jeśli lead trafia do mailingu |
| Notatki | Long text | **bez danych wrażliwych klienta** |

- [ ] Utworzyć tabelę z powyższymi polami
- [ ] Sprawdzić formuły na jednym testowym rekordzie

---

## Etap 2 — widoki (20 min)

- [ ] `Do obsługi` — filtr `Status = nowy`, sortowanie po dacie wpływu rosnąco
- [ ] `Po terminie` — `Status = nowy` **i** `Termin odpowiedzi < dziś` (to jest widok,
      który pilnuje SLA)
- [ ] `W toku` — kanban po statusie
- [ ] `Ten miesiąc` — grupowanie po źródle, do policzenia skąd przychodzą
- [ ] `Do mailingu` — `Zgoda marketingowa = zaznaczone` (jedyna legalna lista wysyłkowa)
- [ ] `Przegrane` — `Status = odrzucony` lub `brak odpowiedzi`, do kwartalnego przeglądu

---

## Etap 3 — podpięcie źródeł (90 min)

### 3a. Formularz kontaktowy Tax Polonica ⭐

To jest sedno zadania. Kolejność operacji w funkcji `contact-form` ma być taka:

1. **zapis do bazy** (`contact_leads` w Supabase) — żeby awaria czegokolwiek dalej
   nie oznaczała utraty zgłoszenia,
2. wysyłka maila do Ciebie,
3. kopia do Airtable.

Każdy krok w osobnym `try`, bo błąd trzeciego nie może wywrócić pierwszego.

- [ ] Dodać tabelę `contact_leads` w Supabase (zgłoszenie [`taxpolonica#15`](https://github.com/chmielmagdalena/taxpolonica/issues/15), zadanie **B5**)
- [ ] Dopisać do funkcji zapis przed wysyłką maila
- [ ] Dopisać wywołanie Airtable API (klucz w secrets funkcji, **nigdy** w kodzie strony)
- [ ] Przekazywać `referrer`, żeby było wiadomo, z której podstrony przyszło zgłoszenie
- [ ] Przetestować: wysłać zapytanie przez prawdziwy formularz i sprawdzić, że rekord
      jest w obu miejscach

### 3b. Poradnik

Dane już są w `guide_leads`, więc wystarczy je przenieść.

- [ ] Jednorazowy import dotychczasowych rekordów do Airtable (CSV)
- [ ] Dopisać do funkcji `guide-download` kopię do Airtable przy nowych pobraniach
- [ ] Zmapować `guide_slug` → pole `Czego dotyczy`

### 3c. Calendly i mail z MC (opcjonalnie, w drugiej kolejności)

- [ ] Calendly → Make/Zapier → nowy rekord w `Leady` ze źródłem `Calendly`
- [ ] Dla MC: albo reguła w Gmailu (etykieta → Make → Airtable), albo zamiana `mailto:`
      na prawdziwy formularz — do decyzji, bo to zmiana na stronie

---

## Etap 4 — automatyzacje (30 min)

| # | Wyzwalacz | Akcja |
|---|---|---|
| 1 | nowy rekord | automatyczne potwierdzenie do zgłaszającego: „odezwę się w ciągu 24 h" |
| 2 | codziennie 9:00 | jeśli widok `Po terminie` nie jest pusty → powiadomienie do Ciebie |
| 3 | `Status` → `odpowiedziano` | wpisz `Data pierwszej odpowiedzi`, jeśli pusta |
| 4 | w poniedziałek rano | zestawienie tygodnia: ile leadów, z jakich źródeł, ile bez odpowiedzi |

- [ ] Automatyzacja 1 i 2 (te dwie dają największą różnicę)
- [ ] Automatyzacja 3 i 4, jeśli zostanie czas

---

## Etap 5 — RODO (20 min)

- [ ] Uzupełnić politykę prywatności: zgłoszenia są **przechowywane**, nie tylko
      przesyłane mailem; podać okres retencji
- [ ] Wpisać rejestr leadów do rejestru czynności przetwarzania (Airtable = podmiot
      przetwarzający poza EOG, DPA podpisane)
- [ ] Zgoda marketingowa na formularzu jako **osobny, dobrowolny** checkbox — nigdy
      połączona z akceptacją regulaminu
- [ ] Ustalić i zapisać regułę czyszczenia: leady bez konwersji kasowane po X miesiącach

W rejestrze trzymasz dane kontaktowe i treść zapytania. Nie trzymasz tam dokumentów
ani danych finansowych — jeśli ktoś w zapytaniu przyśle liczby, przenieś sprawę do
systemu księgowego i skróć notatkę.

---

## Gotowe, gdy

Odpowiadasz z pamięci na trzy pytania, patrząc wyłącznie w Airtable:

1. Ile zapytań przyszło w zeszłym miesiącu i z których źródeł?
2. Czy któreś czeka dłużej niż SLA?
3. Ile z nich skończyło się rozmową, a ile klientem?

Jeśli na którekolwiek trzeba zaglądać do skrzynki — rejestr jeszcze nie działa.

---

## Co z tego wyjdzie po kwartale

- **konwersja per źródło** — czy poradnik faktycznie przynosi klientów, czy tylko adresy
- **czas reakcji** — i czy koreluje z tym, kto zostaje klientem
- **tematy zapytań** — podpowiedź, o czym pisać w kalendarzu treści (zadanie A4)

---

## Plan na pół dnia

| Czas | Co |
|---|---|
| 20 min | Etap 0 — decyzje |
| 40 min | Etap 1 — tabela |
| 20 min | Etap 2 — widoki |
| 90 min | Etap 3a i 3b — formularz i poradnik |
| 30 min | Etap 4 — dwie automatyzacje |
| 20 min | Etap 5 — RODO |

Calendly, mail z MC i pozostałe automatyzacje dochodzą później, przy okazji.
