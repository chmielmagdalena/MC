# Airtable w projektach MC — przegląd zastosowań

Dokument roboczy. Założenie przyjęte na wejściu: Airtable pełni rolę **back-office'u**,
czyli bazy wewnętrznej. Nie jest bazą produkcyjną aplikacji ani CMS-em stron.

Szczegółowy schemat dla priorytetowego projektu (kursy) → [`airtable-kursy.md`](./airtable-kursy.md).

---

## Gdzie Airtable jest mocny, a gdzie nie

Airtable to baza relacyjna z ludzką twarzą: tabele, relacje, widoki (kalendarz, kanban,
grid), formularze i automatyzacje bez kodu. Zastępuje pięć arkuszy Excela, przypominajki
w mailach i notatki „kto komu co wysłał".

Czego nie zastąpi: prawdziwego backendu. Limity rekordów, brak transakcji, dane na
serwerach w USA, brak realnego systemu uprawnień dla klientów zewnętrznych. Dlatego
decyzja „tylko wewnętrznie" jest właściwa — Airtable obsługuje **proces**, a nie produkt.

---

## 1. Kursy i szkolenia — priorytet

Projekt, w którym Airtable daje najwięcej od razu, bo szkolenia to w 80% logistyka
i przypomnienia: kto się zapisał, kto zapłacił, kto dostał link, kto dostał certyfikat.

Pełny schemat, automatyzacje i plan wdrożenia: [`airtable-kursy.md`](./airtable-kursy.md).

W skrócie: pięć tabel (`Kursy`, `Terminy`, `Osoby`, `Zapisy`, `Materiały`), formularz
zapisu na stronie, siedem automatyzacji mailowych. Jeden dzień pracy.
To jedyny element z tej listy, który zarabia od razu i nie wymaga żadnej decyzji
architektonicznej.

---

## 2. BiuroPanel — Airtable jako specyfikacja produktu

Najciekawsze zastosowanie, inne niż „baza danych".

**Zanim zbudujesz BiuroPanel jako aplikację, poprowadź go 2–3 miesiące w Airtable.**
Po kwartale masz dwie rzeczy naraz: działający proces obsługi klientów i gotowy model
danych — schemat tabel staje się dosłownie specyfikacją bazy w prawdziwej aplikacji.
To najtańszy znany sposób na uniknięcie zbudowania panelu, którego nikt nie używa.

Zarys tabel:

| Tabela | Zawartość |
|---|---|
| Klienci | nazwa, NIP, forma prawna, pakiet, cena, opiekun, status |
| Obowiązki | co za deklaracja (VAT-7, JPK_V7, CIT-8, PIT, ZUS, sprawozdanie), cykl, ustawowy termin |
| Zadania okresowe | klient × obowiązek × miesiąc; status `dokumenty oczekiwane` → `otrzymane` → `zaksięgowane` → `wysłane` → `potwierdzone` |
| Dokumenty (metadane) | co wpłynęło, kiedy, od kogo, czego dotyczy — **bez samych plików** |
| Pełnomocnictwa i dostępy | UPL-1, ZAW-FA, dostępy do e-US/PUE, daty ważności |
| Onboarding | checklista wdrożenia nowego klienta |

Widoki, które robią robotę: „co wisi w tym miesiącu", „klienci, którzy nie dostarczyli
dokumentów na 5 dni przed terminem", „pełnomocnictwa wygasające w ciągu 60 dni",
kalendarz ustawowych terminów.

Automatyzacja bazowa: pierwszego dnia miesiąca wygeneruj komplet zadań okresowych
dla wszystkich aktywnych klientów. To jedna automatyzacja, która zastępuje
comiesięczne przepisywanie listy.

**Granica:** w Airtable tylko metadane i statusy. Dokumenty księgowe, kwoty, skany —
w systemie księgowym. Gdy BiuroPanel przestanie być tabelą, a stanie się produktem
z logowaniem klientów, to jest moment na Supabase/Postgres, a nie na wyższy plan Airtable.

---

## 3. WIS — program dla wspólnot i spółdzielni mieszkaniowych

WIS to produkt: zarządzanie wspólnotami i spółdzielniami wraz z ich księgowaniem.
Odpowiedź jest tu inna niż przy pozostałych projektach — **Airtable nie może być bazą
tego programu**. Nie z wygody, tylko przez trzy twarde bariery:

- **Skala.** Jedna wspólnota stulokalowa to kilka tysięcy rekordów rocznie: naliczenia
  zaliczek, wpłaty, odczyty liczników, rozrachunki, rozliczenie roczne mediów.
  Kilkanaście wspólnot wyczerpuje limit planu Team w rok.
- **Dane.** Właściciele lokali, salda, zaległości, windykacja — dane osobowe i finansowe
  setek osób, które nie są Twoimi klientami, tylko klientami Twoich klientów.
  To wymaga backendu z prawdziwym systemem uprawnień, nie bazy udostępnianej linkiem.
- **Logika.** Naliczenie, korekta, rozliczenie roczne mediów to operacje transakcyjne.
  Airtable nie ma transakcji — przerwana automatyzacja zostawia rozjechane salda,
  a w księgowości zarządcy to koniec zaufania do programu.

Backend tego produktu to Postgres/Supabase albo inna prawdziwa baza. Bez dyskusji.

Airtable ma tu natomiast rolę **wokół produktu, a nie w produkcie** — i akurat w WIS
jest ona najcenniejsza ze wszystkich opisanych w tym dokumencie.

### a) Katalog reguł rozliczeniowych ⭐

Serce takiego programu to klucze podziału kosztów — a one są inne dla każdej pozycji
i każdej wspólnoty: udział w nieruchomości wspólnej, powierzchnia lokalu, liczba osób,
wskazanie licznika, ryczałt, podział po równo.

| Pole | Zawartość |
|---|---|
| Pozycja kosztowa | woda zimna, woda ciepła, CO, odpady, sprzątanie, winda, domofon, ubezpieczenie, zarząd, fundusz remontowy |
| Klucz podziału | `udział` / `powierzchnia` / `liczba osób` / `licznik` / `ryczałt` / `po równo` |
| Podstawa | ustawa / uchwała wspólnoty / statut spółdzielni / umowa z dostawcą |
| Dotyczy | wspólnota / spółdzielnia / obie |
| Przypadki brzegowe | lokale użytkowe, garaże i komórki, pustostany, zmiana liczby osób w trakcie okresu, zmiana właściciela w trakcie roku, licznik zepsuty lub bez odczytu |
| Sposób rozliczenia rocznego | nadpłata/niedopłata, przeksięgowanie, zwrot |
| Zaimplementowane w WIS | checkbox + link do zgłoszenia |

Ta jedna tabela robi trzy rzeczy naraz: jest specyfikacją dla programisty, listą
przypadków testowych i ściągą przy rozmowie z zarządcą. Buduj ją od pierwszego dnia —
to wiedza z 18 lat praktyki, której nie ma w dokumentacji żadnego konkurenta,
a która decyduje o tym, czy program liczy poprawnie.

### b) Model domenowy jako specyfikacja

Ta sama strategia co przy BiuroPanelu: spisz encje jako tabele Airtable, **zanim**
powstanie schemat prawdziwej bazy.

Encje do rozpisania: `Wspólnota/Spółdzielnia`, `Nieruchomość`, `Lokal`, `Udziały`,
`Właściciel/Członek`, `Liczniki`, `Odczyty`, `Stawki i zaliczki`, `Naliczenia`,
`Wpłaty`, `Rozrachunki`, `Uchwały`, `Umowy z dostawcami`, `Zgłoszenia usterek`,
`Fundusz remontowy`, `Sprawozdania`.

Na danych syntetycznych (trzy wspólnoty, dwadzieścia lokali, jeden rok) sprawdzisz
relacje i kompletność modelu w kilka godzin — zamiast odkrywać brakującą encję
trzy miesiące po starcie kodowania. **Wyłącznie dane sztuczne.** Żadnego importu
z prawdziwej wspólnoty, nawet „na chwilę, do testu".

### c) Wymagania prawne i sprawozdawcze

Rejestr obowiązków, które program ma obsłużyć: ustawa o własności lokali, ustawa
o spółdzielniach mieszkaniowych, ustawa o rachunkowości, rozliczenie roczne mediów,
terminy zebrań rocznych, sprawozdanie finansowe, obowiązki podatkowe, sprawozdawczość GUS.

Kolumny: obowiązek, podstawa prawna, termin ustawowy, dotyczy (wspólnota/spółdzielnia),
czy WIS to obsługuje, priorytet, link do zgłoszenia. To jednocześnie roadmapa
i argumentacja sprzedażowa — zarządca kupuje program, który pilnuje terminów za niego.

### d) Pilotaże, backlog i feedback

- **Pipeline wdrożeń:** zarządca, liczba wspólnot i lokali, status `rozmowa` → `demo`
  → `pilotaż` → `wdrożenie`, obecny program (z czego migruje), blokery
- **Backlog funkcji** z priorytetem i źródłem — który zarządca o to poprosił i ilu
  innych poprosiło o to samo
- **Zgłoszenia błędów** z pilotażu, powiązane z modułem

Airtable wygrywa tu z Jirą prostotą: zarządca wypełni formularz zgłoszenia, nie założy konta w Jirze.

**Granica:** w tabelach pilotaży trzymasz dane kontaktowe zarządcy — firma, osoba,
telefon, mail. Nigdy dane mieszkańców, numerów lokali z nazwiskami ani sald.

---

## 4. Strony internetowe

Trzy odrębne zastosowania, wszystkie wewnętrzne:

**Rejestr projektów** — klient, etap (`brief` → `treści` → `projekt` → `wdrożenie` → `live`),
deadline, kwota, dostępy (gdzie są, nie same hasła), hosting, domena
i **data wygaśnięcia domeny** z przypomnieniem 30 dni wcześniej. Ta ostatnia rzecz mści
się raz na kilka lat i zawsze w najgorszym momencie.

**Kalendarz treści** — plik `tax-polonica/plan-widocznosci-google.md` to w zasadzie
gotowa tabela: temat, fraza kluczowa, intencja, status (`pomysł` → `szkic` → `opublikowane`),
data publikacji, URL, pozycja w Google, data ostatniego sprawdzenia. W Airtable zyskuje
widok kalendarza i filtr „do odświeżenia po 6 miesiącach".

**Leady** — zgłoszenia z formularzy kontaktowych wszystkich stron w jednym miejscu,
z tagiem źródła i statusem obsługi. Łączy się naturalnie z tabelą `Osoby` z bazy kursów.

Uwaga na przyszłość: gdyby kalendarz treści miał kiedyś zasilać stronę przez API,
to już wyjście poza back-office — wymaga osobnej decyzji o kluczach i cache'owaniu.

---

## 5. RODO — trzy zasady wspólne dla wszystkich baz

1. **Minimalizacja.** Do Airtable trafiają dane kontaktowe, statusy i terminy.
   Nie trafiają: skany dokumentów księgowych, wyciągi, listy płac, dane finansowe
   klientów Twoich klientów, dane szczególnych kategorii.
2. **Umowa powierzenia.** Airtable udostępnia DPA ze standardowymi klauzulami umownymi —
   podpisana przed pierwszym rekordem. Serwery w USA (rezydencja w UE bywa tylko
   w najwyższych planach) → ujawnienie w polityce prywatności i wpis w rejestrze
   czynności przetwarzania.
3. **Zgody i retencja.** Zgoda marketingowa zawsze z datą i treścią klauzuli;
   ustalony okres przechowywania i kwartalne czyszczenie bazy według widoku po dacie.
   Przy kursach to niezbędne — z listy uczestników zawsze robi się lista mailingowa.

---

## 6. Koszty

Plan Free: limit rzędu 1000 rekordów na bazę, ograniczone automatyzacje — wystarcza
na start bazy kursów. Plan Team: ok. 20–24 USD za użytkownika miesięcznie, limit rzędu
kilkudziesięciu tysięcy rekordów. Cennik i limity Airtable zmieniają się — przed zakupem
sprawdź aktualne.

---

## 7. Kolejność wdrożenia

1. **Kursy** — jeden dzień, efekt od pierwszego zapisu.
2. **Kalendarz treści** — pół dnia, przeniesienie istniejącego planu widoczności.
3. **BiuroPanel** — dwa dni na schemat, potem kwartał używania jako walidacja produktu.
4. **WIS** — katalog reguł rozliczeniowych (punkt 3a) od razu, równolegle
   z pracą nad programem; reszta w miarę postępu projektu.
