# Bing Places — jak dodać wizytówkę

Po co to robimy: Bing zasila wyniki wyszukiwania w Windowsie, w przeglądarce
Edge i w Copilocie. To jedyna poważna mapa poza Google. Wpis jest darmowy
i robi się go raz.

Czego to **nie** da: Bing ma w Polsce ułamek ruchu Google. Nie spodziewamy się
po tym telefonów. Robimy to dla spójności danych i obecności w Copilocie,
nie dla ruchu.

---

## Najprostsza droga: import z wizytówki Google

Mamy zweryfikowaną wizytówkę Google, więc nie wpisujemy nic ręcznie. Bing
zaciągnie dane sam, a przy okazji **automatycznie zweryfikuje wpis**, bez
kodu i bez kartki pocztą.

1. Wejdź na **bingplaces.com** i kliknij „Sign in”.
2. Zaloguj się kontem Microsoft. Jeśli nie masz, załóż na firmowy adres
   kontakt@taxpolonica.pl. Konto Microsoft da się założyć na dowolny e-mail,
   nie trzeba zakładać skrzynki Outlook.
3. Wybierz opcję **„Import from your Google Business Profile”**.
4. Bing zapyta, jak często odświeżać dane z Google: tygodniowo, co dwa
   tygodnie albo miesięcznie. **Wybierz miesięcznie.** I tak rzadko zmieniamy
   dane, a rzadsza synchronizacja to mniej okazji, żeby coś się nadpisało.
5. Zaloguj się na konto Google, na którym jest wizytówka, i zatwierdź dostęp.
6. Z listy wykrytych firm wybierz **TAX POLONICA sp. z o.o.** i potwierdź import.

Po imporcie wpis idzie do publikacji. Zwykle trwa to **7–12 dni**. Przez ten
czas nic nie trzeba robić i nie ma sensu sprawdzać codziennie.

---

## Co się przeniesie, a co nie

| Przenosi się | Nie przenosi się |
|---|---|
| Nazwa, adres, telefon | Zdjęcia |
| Adres strony | Posty publikowane w Google |
| Godziny otwarcia | Opinie i odpowiedzi na nie |
| Kategoria | |

Opinii z Google przenieść się nie da i to normalne, nie da się tego obejść.
Zdjęcia można dodać ręcznie w panelu Bing po opublikowaniu wpisu, tymi samymi,
które są w wizytówce Google.

---

## Gdyby import nie zadziałał: dane do wpisania ręcznie

| Pole | Co wpisać |
|---|---|
| Business name | TAX POLONICA sp. z o.o. |
| Street address | ul. Kard. Stefana Wyszyńskiego 56 lok. 5 |
| City | Wrocław |
| ZIP / Postal code | 50-331 |
| Country | Poland |
| Phone | +48 789 643 335 |
| E-mail | kontakt@taxpolonica.pl |
| Website | https://taxpolonica.pl |
| Category | Accountants (albo Accounting Services) |

**Kategoria: wybierz księgową, nie podatkową.** Jeśli na liście będzie
„Tax Consultant”, „Tax Preparation” albo „Tax Return Service”, nie zaznaczaj
tego. Jesteśmy biurem rachunkowym, nie doradcą podatkowym, i kategoria w
katalogu też ma to odzwierciedlać.

Przy ręcznym wpisie weryfikacja idzie telefonem albo mailem i trwa dłużej.
Dlatego najpierw próbujemy importu.

### Opis do wklejenia (jeśli poprosi)

> TAX POLONICA to biuro rachunkowe z Wrocławia, działające od 2010 roku.
> Prowadzimy pełne księgi handlowe, KPiR, ewidencje ryczałtu, kadry i płace.
> Obsługujemy spółki, jednoosobowe działalności, fundacje i stowarzyszenia,
> a także spółdzielnie i wspólnoty mieszkaniowe. Księgi przejmujemy w dowolnym
> miesiącu, nie trzeba czekać do stycznia. Pracujemy też zdalnie, z klientami
> z całej Polski.

### Godziny otwarcia

Wpisz te same, które są w wizytówce Google. Jeśli import je zaciągnie, nie
poprawiaj ich ręcznie, bo przy miesięcznej synchronizacji i tak zostaną
nadpisane wersją z Google.

---

## Na co uważać

- **Nie zakładaj drugiego wpisu, jeśli Bing pokaże, że firma już istnieje.**
  Przy automatycznie utworzonych wizytówkach jest opcja przejęcia („Claim”).
  Dwa wpisy tej samej firmy szkodzą bardziej niż brak wpisu.
- **Nie wyłączaj synchronizacji z Google po imporcie.** Wyłączenie nie odłącza
  wizytówki Google od Bing, zatrzymuje tylko aktualizacje, więc dane zaczną
  się rozjeżdżać przy pierwszej zmianie.
- **Adres strony bez „www”**, tak jak wszędzie indziej. Jeśli import wciągnie
  wersję z „www”, znaczy to, że taka jest w wizytówce Google, i wtedy poprawiamy
  w Google, a nie w Bingu.

---

## Stan

| Krok | Stan |
|---|---|
| Konto Microsoft | zrobione |
| Import z wizytówki Google | zrobione 13.10.2026, synchronizacja włączona |
| Publikacja wpisu (7–12 dni od importu) | czeka, spodziewana do 25.10.2026 |
| E-mail uzupełniony ręcznie | do sprawdzenia, czy pole jest edytowalne |
| Zdjęcia dodane ręcznie | do zrobienia po publikacji |

Co zaciągnęło się z Google: nazwa „Tax Polonica Biuro Rachunkowe”, adres
Wyszyńskiego 56 lok. 5, telefon 789 643 335, strona `https://taxpolonica.pl/`,
kategoria „Księgowy”. Pole e-mail zostało puste, bo wizytówka Google nie ma
takiego pola.

Większości pól nie da się tu edytować. Bing wyświetla to wprost: żeby je
zmienić, poprawiamy dane w wizytówce Google i czekamy na synchronizację.
To dobrze, bo oznacza, że mamy jedno miejsce, w którym pilnujemy danych.


---

## Bing Webmaster Tools (osobna rzecz niż wizytówka)

Przy okazji wizytówki została dodana domena do Bing Webmaster Tools, czyli
odpowiednika Google Search Console. To nie to samo co Bing Places: wizytówka
dotyczy firmy na mapie, Webmaster Tools dotyczy strony w wynikach.

Weryfikacja przeszła **importem z Google Search Console**, bez wgrywania
żadnych plików na stronę. Gdyby kiedyś trzeba było powtórzyć: ta opcja jest
na ekranie dodawania strony, obok pola na adres. Metoda z plikiem
`BingSiteAuth.xml` też działa, ale wymaga publikacji pliku w katalogu
`public/` i jest zbędna, dopóki działa import.

| Krok | Stan |
|---|---|
| Domena taxpolonica.pl dodana i zweryfikowana | zrobione 13.10.2026 |
| Sitemapa zgłoszona (`https://taxpolonica.pl/sitemap.xml`) | zrobione 13.10.2026, status „Sukces”, 30 adresów, zero błędów |
| AI Performance: pierwsze dane | po 48 h od weryfikacji |

Zakładka **AI Performance** pokazuje, jak strona wypada w odpowiedziach
Copilota, łącznie z udziałem w cytowaniach. To jedyne darmowe źródło takich
danych, bo Google niczego podobnego nie udostępnia. Dane zbierają się od
momentu weryfikacji, więc na początku będzie pusto i to normalne.
