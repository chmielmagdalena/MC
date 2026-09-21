# Airtable dla kursów i szkoleń — gotowy schemat bazy

Dokument roboczy. Zakres: **back-office**, czyli baza wewnętrzna dla organizacji szkoleń
„AI dla księgowych". Uczestnik styka się z nią wyłącznie przez formularz zapisu i maile.

Cel: jeden dzień pracy → działająca obsługa zapisów, płatności i przypomnień,
bez arkuszy Excela i bez ręcznego pilnowania terminów.

---

## 1. Model danych

Pięć tabel plus jedna pomocnicza. Sercem układu jest tabela **Zapisy** — łączy osobę
z konkretnym terminem. Bez niej wszystko rozjedzie się przy drugiej edycji kursu
(ta sama osoba na dwóch szkoleniach, ten sam kurs w trzech terminach).

```
Kursy ──< Terminy ──< Zapisy >── Osoby
  │                     │
  └──< Materiały        └──< (płatność, faktura, certyfikat, ankieta)

Terminy ──< Zadania (checklista przygotowania)
```

### Tabela: Kursy

| Pole | Typ | Uwagi |
|---|---|---|
| Nazwa | Single line text | pole główne |
| Typ | Single select | `live online` / `stacjonarnie` / `nagranie` / `hybryda` |
| Opis | Long text | tekst na stronę i do maila |
| Program | Long text | agenda w punktach |
| Cena netto | Currency (PLN) | |
| Stawka VAT | Single select | `23%` / `zw.` (szkolenia bywają zwolnione — sprawdź podstawę) |
| Czas trwania (h) | Number | |
| Status | Single select | `w przygotowaniu` / `aktywny` / `wycofany` |
| Terminy | Link → Terminy | |
| Materiały | Link → Materiały | |
| Przychód łącznie | Rollup (SUM z Zapisy.Kwota) | przez Terminy |

### Tabela: Terminy

| Pole | Typ | Uwagi |
|---|---|---|
| Nazwa terminu | Formula | `Kurs & " — " & DATETIME_FORMAT(Data, 'DD.MM.YYYY')` |
| Kurs | Link → Kursy | |
| Data i godzina | Date (z godziną) | |
| Forma | Single select | `online` / `stacjonarnie` |
| Miejsce / link | URL lub text | link do Meet/Zoom albo adres sali |
| Limit miejsc | Number | |
| Zapisy | Link → Zapisy | |
| Liczba zapisanych | Count (Zapisy) | |
| Liczba opłaconych | Rollup (COUNTA po statusie `opłacony`) | |
| Wolne miejsca | Formula | `Limit miejsc - Liczba zapisanych` |
| Status | Single select | `planowany` / `zapisy otwarte` / `potwierdzony` / `lista rezerwowa` / `odwołany` / `zakończony` |
| Próg rentowności | Number | minimalna liczba osób, poniżej której termin się nie opłaca |
| Notatki | Long text | |

### Tabela: Osoby

| Pole | Typ | Uwagi |
|---|---|---|
| Imię i nazwisko | Single line text | pole główne |
| E-mail | Email | |
| Telefon | Phone | |
| Firma | Single line text | |
| NIP | Single line text | tylko gdy potrzebna faktura na firmę |
| Rola | Single select | `księgowa` / `właściciel biura` / `CFO` / `inne` |
| Źródło | Single select | `LinkedIn` / `Google` / `polecenie` / `newsletter` / `konferencja` / `inne` |
| Zgoda marketingowa | Checkbox | |
| Data zgody | Date | wypełniane automatycznie przy zaznaczeniu |
| Treść zgody | Long text | dokładna klauzula, którą osoba zaakceptowała (dowód z RODO) |
| Zapisy | Link → Zapisy | |
| Liczba szkoleń | Count (Zapisy) | wraca po raz drugi = kandydat na stałego klienta |
| Notatki | Long text | **bez** danych wrażliwych |

### Tabela: Zapisy ⭐

Jeden rekord = jedna osoba na jednym terminie.

| Pole | Typ | Uwagi |
|---|---|---|
| ID zapisu | Autonumber | pole główne |
| Osoba | Link → Osoby | |
| Termin | Link → Terminy | |
| Kurs | Lookup (Termin → Kurs) | do filtrowania |
| Data zgłoszenia | Created time | |
| Status | Single select | `zgłoszenie` / `potwierdzony` / `opłacony` / `zrealizowany` / `rezygnacja` / `no-show` |
| Kwota | Currency | |
| Termin płatności | Formula | `DATEADD(Data zgłoszenia, 7, 'days')` |
| Data płatności | Date | |
| Dni po terminie | Formula | `IF(AND(Data płatności = BLANK(), Status = 'zgłoszenie'), DATETIME_DIFF(TODAY(), Termin płatności, 'days'), 0)` |
| Faktura wystawiona | Checkbox | |
| Nr faktury | Single line text | |
| Link do spotkania wysłany | Checkbox | |
| Certyfikat wysłany | Checkbox | |
| Ankieta — ocena | Rating (1–5) | |
| Ankieta — komentarz | Long text | |
| Uwagi | Long text | np. „faktura na firmę", „dieta bezglutenowa" |

### Tabela: Materiały

| Pole | Typ | Uwagi |
|---|---|---|
| Nazwa | Single line text | |
| Kurs | Link → Kursy | |
| Rodzaj | Single select | `slajdy` / `nagranie` / `szablon` / `checklista` / `certyfikat (wzór)` |
| Plik / link | Attachment lub URL | duże pliki → Google Drive, w Airtable tylko link |
| Udostępniać | Single select | `przed szkoleniem` / `po szkoleniu` / `nie udostępniać` |
| Wersja | Single line text | |

### Tabela: Zadania

Checklista przygotowania jednego terminu — generowana automatycznie przy otwarciu zapisów.

| Pole | Typ |
|---|---|
| Zadanie | Single line text |
| Termin (szkolenia) | Link → Terminy |
| Deadline | Date |
| Status | Single select: `do zrobienia` / `w toku` / `zrobione` |

Typowa lista: aktualizacja slajdów → utworzenie spotkania → wysyłka linku (D-2) →
wysyłka materiałów → faktury → certyfikaty → ankieta → podsumowanie przychodu.

---

## 2. Widoki, które oszczędzają czas od pierwszego dnia

**Terminy**
- `Kalendarz` — widok Calendar po dacie, wszystkie edycje na osi czasu
- `Zapisy otwarte` — filtr `Status = zapisy otwarte`, sortowanie po dacie
- `Zagrożone` — filtr `Liczba opłaconych < Próg rentowności` **i** data za mniej niż 7 dni;
  to jest widok, który mówi „albo promuj, albo odwołuj"

**Zapisy**
- `Kanban po statusie` — przeciągasz kartę, gdy wpłynie przelew
- `Do opłacenia` — filtr `Status = zgłoszenie` **i** `Dni po terminie > 0`
- `Do zafakturowania` — `Status = opłacony` **i** `Faktura wystawiona = puste`
- `Po szkoleniu` — `Status = zrealizowany` **i** `Certyfikat wysłany = puste`
- `Oceny poniżej 4` — do przeczytania przed kolejną edycją

**Osoby**
- `Newsletter` — filtr `Zgoda marketingowa = zaznaczone` (jedyna legalna baza wysyłkowa)
- `Powracający` — `Liczba szkoleń > 1`

---

## 3. Automatyzacje (natywne, bez kodu)

| # | Wyzwalacz | Akcja |
|---|---|---|
| 1 | Nowy rekord w `Zapisy` (z formularza) | e-mail potwierdzający: co, kiedy, kwota, dane do przelewu, termin płatności |
| 2 | Codziennie 9:00 | znajdź `Do opłacenia` → przypomnienie do uczestnika + zadanie dla Ciebie |
| 3 | `Status` → `opłacony` | e-mail „widzimy się", dopisanie do listy wysyłkowej terminu |
| 4 | 2 dni przed datą terminu | do wszystkich opłaconych: link do spotkania + materiały „przed szkoleniem"; zaznacz `Link wysłany` |
| 5 | `Wolne miejsca = 0` | `Status` terminu → `lista rezerwowa` + powiadomienie do Ciebie |
| 6 | Dzień po terminie | `Status` zapisów → `zrealizowany`, e-mail z ankietą, certyfikatem i nagraniem |
| 7 | `Status` terminu → `zapisy otwarte` | wygeneruj komplet rekordów w `Zadania` z deadline'ami liczonymi od daty szkolenia |

Limit automatyzacji zależy od planu — jeśli Free przestanie wystarczać, najpierw
przenieś do Make/Zapier automatyzacje 2 i 6 (najbardziej „cykliczne").

---

## 4. Formularz zapisu

Airtable Form podpięty do tabeli `Zapisy`, osadzony na stronie (iframe) lub jako link
z przycisku „Zapisz się".

Pola na formularzu: imię i nazwisko, e-mail, telefon, firma, NIP (opcjonalnie),
wybór terminu (lista tylko ze statusem `zapisy otwarte`), skąd się dowiedziałaś/eś,
uwagi, **checkbox regulaminu** (wymagany) i **osobny checkbox zgody marketingowej** (dobrowolny).

Dwie rzeczy do zapamiętania:
- zgoda marketingowa **nie może** być połączona z akceptacją regulaminu w jednym checkboxie,
- pod formularzem link do polityki prywatności z informacją, że dane przetwarza dostawca spoza EOG.

Alternatywa bez brandingu Airtable: własny formularz na stronie → zapis przez Airtable API.
Wtedy klucz API trzyma serwer/funkcja, nigdy kod strony.

Gdyby zapisy miały kiedyś wyjść poza Airtable: repozytorium `africano-booking` ma
gotowy wzorzec rezerwacji na Supabase (`reservations`, `reservation_requests`,
`user_roles`, formularz klienta plus panel administratora). Ta sama struktura obsługuje
zapisy na szkolenia po zmianie nazw encji.

---

## 5. Co z tego mierzysz

Widok `Kursy` z rollupami odpowiada na pytania, które zwykle giną w mailach:

- przychód na kurs i na termin,
- obłożenie (`Liczba zapisanych / Limit miejsc`) — czy limit jest realistyczny,
- konwersja `zgłoszenie → opłacony` — jeśli spada, problem jest w cenie albo w mailu potwierdzającym,
- źródła uczestników — skąd realnie przychodzą, a nie skąd Ci się wydaje,
- średnia ocena i komentarze.

Po trzech edycjach widać, który temat sprzedaje się sam.

---

## 6. Integracje

| Potrzeba | Rozwiązanie |
|---|---|
| Wysyłka maili | natywna akcja Airtable; przy większych wolumenach osobny mailing |
| Kalendarz | synchronizacja Terminów z Google Calendar (natywna lub przez Make) |
| Materiały, nagrania | Google Drive — w Airtable tylko linki, nie pliki |
| Płatności | Stripe / Przelewy24 → Make → zmiana `Status` na `opłacony` |
| Faktury | Fakturownia lub wFirma przez API/Make — wyzwalacz: `Status = opłacony` |
| Certyfikaty | szablon w Google Docs → merge z danymi zapisu → PDF na maila |

---

## 7. RODO — granica, którą warto ustawić od razu

1. **Minimalizacja.** W Airtable: imię, nazwisko, e-mail, telefon, firma, NIP do faktury,
   statusy i terminy. **Nie**: skany dokumentów, dane finansowe klientów Twoich klientów,
   żadne dane szczególnych kategorii. Uwagi w rekordzie osoby czyta się kiedyś na głos —
   pisz tylko to, co zniesie taką sytuację.
2. **Umowa powierzenia (DPA).** Airtable udostępnia DPA ze standardowymi klauzulami
   umownymi; podpisz przed wprowadzeniem pierwszego rekordu. Serwery są w USA
   (rezydencja danych w UE bywa dostępna tylko w najwyższych planach) — musi to być
   ujawnione w polityce prywatności i w rejestrze czynności przetwarzania.
3. **Zgody i retencja.** Zgoda marketingowa zawsze z datą i treścią klauzuli.
   Ustal okres przechowywania (np. dane uczestników 5 lat ze względu na dokumentację
   księgową, dane marketingowe do wycofania zgody) i raz na kwartał czyść bazę
   według widoku filtrującego po dacie.

Przy tych ograniczeniach baza kursów jest bezpieczna. Gdyby kiedyś miały wejść
dokumenty księgowe — to jest moment na własny backend, nie na Airtable.

---

## 8. Koszty i granica stosowalności

Plan Free ma limit rzędu 1000 rekordów na bazę i ograniczoną liczbę uruchomień
automatyzacji — na start (kilka edycji, kilkadziesiąt osób) wystarcza. Plan Team to
ok. 20–24 USD za użytkownika miesięcznie i limit rzędu kilkudziesięciu tysięcy rekordów.
Cennik i limity Airtable zmieniają się — sprawdź aktualne przed zakupem.

Moment na przesiadkę na własny backend (Supabase/Postgres): setki tysięcy rekordów,
dane wrażliwe księgowo, logowanie klientów z prawdziwymi uprawnieniami,
logika transakcyjna. Do obsługi szkoleń ten moment nie nadejdzie szybko.

---

## 9. Plan wdrożenia — jeden dzień

1. **60 min** — tabele `Kursy`, `Terminy`, `Osoby`, `Zapisy` z polami z sekcji 1 (bez formuł).
2. **30 min** — relacje, rollupy, formuły.
3. **45 min** — widoki z sekcji 2.
4. **60 min** — formularz zapisu + treść maila potwierdzającego.
5. **60 min** — automatyzacje 1, 2, 4, 6.
6. **30 min** — wprowadź najbliższy termin i przejdź całą ścieżkę na własnym mailu jako testowy uczestnik.
7. **15 min** — polityka prywatności i klauzula zgody na formularzu.

Reszta (materiały, zadania, płatności, faktury) dochodzi w trakcie pierwszej edycji.
