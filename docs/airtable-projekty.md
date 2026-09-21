# Airtable w projektach MC — przegląd zastosowań

Dokument roboczy, oparty na stanie faktycznym repozytoriów (przegląd: 21.09.2026).
Założenie przyjęte na wejściu: Airtable pełni rolę **back-office'u**, czyli bazy
wewnętrznej. Nie jest bazą produkcyjną aplikacji ani CMS-em stron.

Szczegółowy schemat dla priorytetowego projektu (kursy) → [`airtable-kursy.md`](./airtable-kursy.md).

---

## Stan faktyczny projektów

| Repo | Co to jest | Stos | Dojrzałość |
|---|---|---|---|
| `jpk-tag-finder` | JPK CIT Mapper + panel firm | Lovable, React, Supabase, Stripe | produkcja, płatny plan 99 zł |
| `taxpolonica` | strona biura rachunkowego | Lovable, React, Supabase Edge Functions | produkcja |
| `MC` | strona wizytówka | statyczny HTML/CSS/JS | produkcja |
| `SmartHousing-Manager` (WIS) | wspólnoty i spółdzielnie | Google AI Studio, Express + SQLite, React 19 | wczesny prototyp |
| `africano-booking` | rezerwacja stolików (Africano, Wrocław) | Lovable, React, Supabase | osobny projekt, przydatny wzorzec |

Kursy nie mają jeszcze repozytorium — i nie potrzebują. To właśnie miejsce dla Airtable.

---

## Gdzie Airtable jest mocny, a gdzie nie

Airtable to baza relacyjna z ludzką twarzą: tabele, relacje, widoki (kalendarz, kanban,
grid), formularze i automatyzacje bez kodu. Zastępuje pięć arkuszy Excela, przypominajki
w mailach i notatki „kto komu co wysłał".

Czego nie zastąpi: prawdziwego backendu. Limity rekordów, brak transakcji, dane na
serwerach w USA, brak realnego systemu uprawnień dla klientów zewnętrznych. Dlatego
Airtable obsługuje **proces**, a nie produkt. W Twoich projektach produkty już mają
swoje backendy (Supabase w trzech repo, SQLite w WIS) — i tak ma zostać.

---

## 1. Kursy i szkolenia — priorytet

Jedyny projekt bez kodu i jedyny, w którym Airtable jest docelowym rozwiązaniem,
a nie protezą. Szkolenia to w 80% logistyka i przypomnienia: kto się zapisał, kto
zapłacił, kto dostał link, kto dostał certyfikat.

Pełny schemat, automatyzacje i plan wdrożenia: [`airtable-kursy.md`](./airtable-kursy.md).
W skrócie: pięć tabel, formularz zapisu na stronie, siedem automatyzacji mailowych,
jeden dzień pracy.

Gdyby zapisy miały kiedyś wyjść poza Airtable, nie zaczynasz od zera: `africano-booking`
to gotowy wzorzec rezerwacji na Supabase — `reservations`, `reservation_requests`,
`user_roles`, formularz klienta plus panel administratora. Ta sama struktura obsługuje
zapisy na szkolenia po zmianie nazw encji.

---

## 2. BiuroPanel — dziś to tabela `companies` w JPK Mapperze

W repozytoriach nie ma osobnego projektu „BiuroPanel". To, co istnieje, to panel firm
wewnątrz `jpk-tag-finder`: tabela `companies` (`name`, `nip`, `entity_type`,
`entity_size`, `last_mapping_date`), RLS per użytkownik, `profiles.plan_type`
z planem free/płatnym i obsługa subskrypcji przez Stripe (`create-checkout`,
`customer-portal`, `check-subscription`).

Czyli biuro rachunkowe ma tam dziś listę obsługiwanych firm i historię mapowań —
ale nie ma obsługi **obowiązków i terminów**, a to jest sedno pracy biura.

**Tu pytanie, na które tylko Ty odpowiesz:** czy BiuroPanel to rozwinięcie panelu firm
w JPK Mapperze (jeden produkt, jedna subskrypcja, wspólne `companies`), czy osobny
produkt? Od tego zależy, czy projektujesz nowy schemat, czy dokładasz tabele do
istniejącego Supabase.

Niezależnie od odpowiedzi — **poprowadź BiuroPanel 2–3 miesiące w Airtable, zanim
napiszesz do niego kod.** Po kwartale masz działający proces i gotowy model danych;
schemat tabel staje się specyfikacją. Masz już `companies` jako punkt wyjścia, więc
w Airtable dokładasz to, czego tam brakuje:

| Tabela | Zawartość |
|---|---|
| Klienci | to, co w `companies`, plus pakiet, cena, opiekun, status współpracy |
| Obowiązki | JPK_V7, CIT-8, PIT, ZUS, sprawozdanie — cykl i termin ustawowy |
| Zadania okresowe | klient × obowiązek × miesiąc; `dokumenty oczekiwane` → `otrzymane` → `zaksięgowane` → `wysłane` |
| Dokumenty (metadane) | co wpłynęło, kiedy, od kogo — **bez plików** |
| Pełnomocnictwa i dostępy | UPL-1, ZAW-FA, dostępy do e-US/PUE, daty ważności |
| Onboarding | checklista wdrożenia nowego klienta |

Jedna automatyzacja robi największą różnicę: pierwszego dnia miesiąca wygeneruj komplet
zadań okresowych dla wszystkich aktywnych klientów.

---

## 3. WIS (`SmartHousing-Manager`) — prototyp, który potrzebuje specyfikacji

Stan na dziś: Express + SQLite, React 19, cztery tabele — `communities`, `residents`,
`billing_history`, `meter_readings`. Działa dodawanie wspólnot, mieszkańców, ręcznych
obciążeń i wpłat, odczyty wodomierzy z kontrolą ciągłości daty, wykresy i eksport PDF.
Kwoty liczone na `decimal.js` z zaokrągleniem do dwóch miejsc — dobra decyzja,
bo `float` w księgowości zawsze się mści.

Czego w schemacie nie ma, a co jest istotą takiego programu:

- **lokalu jako encji** — dziś adres to pole tekstowe przy mieszkańcu; nie ma powierzchni,
  udziału w nieruchomości wspólnej, typu (mieszkalny / użytkowy / garaż)
- **stawek i zaliczek** — nie ma definicji, ile kto płaci; `billing_history` przyjmuje
  ręcznie wpisaną kwotę, więc nie ma naliczania
- **kluczy podziału kosztów** — czyli tego, co odróżnia program dla wspólnot od arkusza
- **rozliczenia rocznego mediów**, uchwał, funduszu remontowego, sprawozdań

**Airtable nie może być bazą tego produktu** — skala (jedna wspólnota stulokalowa to
kilka tysięcy rekordów rocznie), dane osobowe i finansowe setek mieszkańców, brak
transakcji przy naliczeniach i korektach. Backend zostaje w SQLite/Postgresie.

Airtable ma tu rolę **wokół produktu** i akurat w WIS jest ona najcenniejsza:

### a) Katalog reguł rozliczeniowych ⭐

To jest dokładnie ta warstwa, której w prototypie brakuje — a Ty masz ją w głowie
z 18 lat praktyki.

| Pole | Zawartość |
|---|---|
| Pozycja kosztowa | woda zimna, woda ciepła, CO, odpady, sprzątanie, winda, domofon, ubezpieczenie, zarząd, fundusz remontowy |
| Klucz podziału | `udział` / `powierzchnia` / `liczba osób` / `licznik` / `ryczałt` / `po równo` |
| Podstawa | ustawa / uchwała wspólnoty / statut spółdzielni / umowa z dostawcą |
| Dotyczy | wspólnota / spółdzielnia / obie |
| Przypadki brzegowe | lokale użytkowe, garaże i komórki, pustostany, zmiana liczby osób w trakcie okresu, zmiana właściciela w trakcie roku, licznik zepsuty lub bez odczytu, różnica bilansowa wody |
| Rozliczenie roczne | nadpłata/niedopłata, przeksięgowanie, zwrot |
| Zaimplementowane w WIS | checkbox + link do zgłoszenia |

Jedna tabela, trzy zastosowania: specyfikacja dla programisty, lista przypadków
testowych, ściąga przy rozmowie z zarządcą. Zacznij od niej — bez niej kolejne tygodnie
kodowania pójdą w interfejs, a nie w to, co decyduje o poprawności obliczeń.

### b) Docelowy model domenowy

Encje do rozpisania obok czterech istniejących: `Lokal`, `Udziały`, `Stawki i zaliczki`,
`Naliczenia`, `Rozrachunki`, `Uchwały`, `Umowy z dostawcami`, `Zgłoszenia usterek`,
`Fundusz remontowy`, `Sprawozdania`. Na danych syntetycznych (trzy wspólnoty,
dwadzieścia lokali, jeden rok) sprawdzisz kompletność modelu w kilka godzin — zamiast
odkrywać brakującą encję trzy miesiące po starcie kodowania.

**Wyłącznie dane sztuczne.** Żadnego importu z prawdziwej wspólnoty, nawet „na chwilę".

### c) Wymagania prawne i sprawozdawcze

Rejestr: ustawa o własności lokali, ustawa o spółdzielniach mieszkaniowych, ustawa
o rachunkowości, rozliczenie roczne mediów, terminy zebrań, sprawozdanie finansowe,
obowiązki podatkowe, GUS. Kolumny: obowiązek, podstawa, termin, dotyczy, czy WIS to
obsługuje, priorytet. To jednocześnie roadmapa i argument sprzedażowy — zarządca kupuje
program, który pilnuje terminów za niego.

### d) Pilotaże, backlog i zgłoszenia

Pipeline wdrożeń (zarządca, liczba wspólnot i lokali, status `rozmowa` → `demo` →
`pilotaż` → `wdrożenie`, program, z którego migruje), backlog funkcji ze źródłem
zgłoszenia, rejestr błędów z pilotażu. W tabelach pilotaży trzymasz **wyłącznie dane
kontaktowe zarządcy** — nigdy danych mieszkańców.

### Dwie rzeczy do naprawienia w kodzie, zanim WIS zobaczy kogokolwiek z zewnątrz

1. **Logowanie jest atrapą.** `src/App.tsx` sprawdza `admin` / `admin123` po stronie
   przeglądarki, a żaden endpoint w `server.ts` nie ma autoryzacji — każdy, kto zna
   adres, czyta i zapisuje dane wszystkich wspólnot.
2. **Podwójny import w `src/App.tsx`** (`AlertCircle` i `Plus` importowane dwa razy
   z `lucide-react`, linie 6–18 i 34) — to błąd kompilacji TypeScriptu. Nie udało mi się
   uruchomić `tsc` w tej sesji, więc potwierdź lokalnie przez `npm run lint`.

Oba punkty są normalne dla prototypu z AI Studio — ale oznaczają, że do WIS nie wolno
dziś wprowadzić żadnych prawdziwych danych.

---

## 4. Strony internetowe

`taxpolonica` (Lovable + React + Supabase Edge Functions) i `MC` (statyczny HTML).
Trzy zastosowania Airtable, wszystkie wewnętrzne:

**Leady — i konkretna dziura do załatania.** W `taxpolonica` funkcja `guide-download`
zapisuje pobrania poradnika do tabeli `guide_leads`, ale `contact-form` **tylko wysyła
maila** i nie zapisuje nic. Zgłoszenia z formularza kontaktowego żyją więc wyłącznie
w skrzynce: nie policzysz, ile ich było, nie sprawdzisz, które zostały obsłużone,
nie zobaczysz, z której podstrony przyszły. Airtable jako rejestr leadów zamyka ten temat
(webhook z funkcji albo integracja z mailem), a docelowo warto dopisać insert do bazy.

**Rejestr projektów** — klient, etap (`brief` → `treści` → `projekt` → `wdrożenie` →
`live`), deadline, kwota, hosting, domena i **data wygaśnięcia domeny** z przypomnieniem
30 dni wcześniej.

**Kalendarz treści** — `tax-polonica/plan-widocznosci-google.md` to w zasadzie gotowa
tabela: temat, fraza, status (`pomysł` → `szkic` → `opublikowane`), data, URL, pozycja
w Google, data ostatniego sprawdzenia. W Airtable zyskuje widok kalendarza i filtr
„do odświeżenia po 6 miesiącach". Reguły z `taxpolonica/CLAUDE.md` (granica między
czynnością księgową a doradztwem) zostają w repo — to zasady pisania, nie dane.

---

## 5. RODO — trzy zasady wspólne dla wszystkich baz

1. **Minimalizacja.** Do Airtable trafiają dane kontaktowe, statusy i terminy.
   Nie trafiają: skany dokumentów księgowych, dane finansowe klientów Twoich klientów,
   dane mieszkańców wspólnot, dane szczególnych kategorii.
2. **Umowa powierzenia.** Airtable udostępnia DPA ze standardowymi klauzulami umownymi —
   podpisana przed pierwszym rekordem. Serwery w USA → ujawnienie w polityce prywatności
   i wpis w rejestrze czynności przetwarzania.
3. **Zgody i retencja.** Zgoda marketingowa zawsze z datą i treścią klauzuli, ustalony
   okres przechowywania, kwartalne czyszczenie według widoku po dacie.

---

## 6. Koszty

Plan Free: limit rzędu 1000 rekordów na bazę, ograniczone automatyzacje — wystarcza
na start bazy kursów. Plan Team: ok. 20–24 USD za użytkownika miesięcznie, limit rzędu
kilkudziesięciu tysięcy rekordów. Cennik i limity Airtable zmieniają się — sprawdź
aktualne przed zakupem.

---

## 7. Kolejność wdrożenia

1. **Kursy** — jeden dzień, efekt od pierwszego zapisu. Jedyna rzecz, która zarabia od razu.
2. **Katalog reguł rozliczeniowych WIS** — zacznij równolegle, po godzinie dziennie.
   To najcenniejszy zasób w całym zestawieniu i nie wymaga ani linijki kodu.
3. **Rejestr leadów ze stron** — pół dnia, zamyka dziurę w `contact-form`.
4. **Kalendarz treści** — pół dnia, przeniesienie istniejącego planu widoczności.
5. **BiuroPanel** — po decyzji, czy to rozwinięcie JPK Mappera, czy osobny produkt.
   Dwa dni na schemat, potem kwartał używania jako walidacja.
