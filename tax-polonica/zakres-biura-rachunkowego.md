# Tax Polonica — zakres biura rachunkowego i zasady pisania treści

*Ten sam dokument jest w repozytorium strony jako `CLAUDE.md` — tam wczytuje się automatycznie
przy każdej pracy nad serwisem. Tutaj leży jako materiał do ręcznego użycia: przy wizytówce
Google, postach, ogłoszeniach i ofertach.*

## Zasada nadrzędna

**Jesteśmy biurem rachunkowym. Nie jesteśmy doradcą podatkowym ani kancelarią prawną.**

Każda treść na stronie — oferta, podstrona, poradnik, post, opis usługi — musi mieścić się
w granicach usługowego prowadzenia ksiąg rachunkowych. Jeśli zdanie sugeruje doradztwo
podatkowe, poradę prawną albo przejęcie odpowiedzialności, która z mocy prawa ciąży
na kliencie lub na zarządzie — nie wchodzi na stronę.

Przy pisaniu każdego tekstu zadaj trzy pytania:

1. Czy to jest czynność księgowa, czy już doradztwo podatkowe lub prawne?
2. Czy możemy to zrobić **bez pełnomocnictwa**, czy potrzebujemy go do wysyłki?
3. Czy ten obowiązek ciąży na nas, czy na kliencie lub zarządzie?

---

## Co robimy — i jak o tym pisać

### Prowadzenie ksiąg i ewidencji
- Księga przychodów i rozchodów, ryczałt, pełne księgi rachunkowe.
- Rejestr środków trwałych i odpisy amortyzacyjne.
- Ewidencje VAT, pliki JPK.
- **Dotacje i projekty: ujęcie w księgach.** Prowadzimy wyodrębnioną ewidencję księgową
  projektu, przygotowujemy zestawienia kosztów z ksiąg w układzie pozycji budżetu.
  **Nie wypełniamy za klienta wniosków, druków ani formularzy grantodawcy.**

### Rozliczenia i deklaracje
- Wyliczamy zobowiązania podatkowe i składkowe na podstawie dostarczonych dokumentów.
- Przygotowujemy deklaracje podatkowe i ZUS.
- **Wysyłamy deklaracje wyłącznie wtedy, gdy mamy pełnomocnictwo** — do urzędu skarbowego
  i do ZUS. Bez pełnomocnictwa przygotowujemy dokument, a wysyła go klient.
- W treściach zawsze: „składamy deklaracje na podstawie udzielonego pełnomocnictwa",
  nigdy samo „składamy za Ciebie wszystko".

### Kadry i płace
- Dokumentacja pracownicza, ewidencja czasu pracy.
- Naliczanie wynagrodzeń, składek ZUS i zaliczek na podatek.
- Deklaracje ZUS i PIT-11.
- Rozliczanie urlopów, zwolnień lekarskich, nadgodzin.

### Sprawozdawczość
- Przygotowujemy sprawozdanie finansowe od strony księgowej: bilans, rachunek zysków
  i strat, informacja dodatkowa.
- **Sprawozdanie podpisuje i składa zarząd — obowiązek ciąży na nim, nie na biurze.**
  Możemy przeprowadzić przez proces technicznie, ale nie składamy sprawozdania za zarząd
  i nie bierzemy za to odpowiedzialności.
- Raporty miesięczne i kwartalne dla zarządu.

---

## Czego nie robimy — czerwona lista

Tych sformułowań **nie wolno** używać w treściach:

| Nie pisz | Napisz zamiast tego |
|---|---|
| „Złożymy sprawozdanie do NIW" | „Przygotujemy dane finansowe do sprawozdania; składa je zarząd" |
| „Załatwimy formalności w urzędzie za Ciebie" | „Deklaracje składamy na podstawie pełnomocnictwa" |
| „Wypełnimy wniosek o dotację / rozliczenie w generatorze" | „Przygotujemy zestawienie kosztów projektu z ksiąg" |
| „Doradzimy, jaką formę opodatkowania wybrać" | „Policzymy skutki księgowe każdego wariantu" |
| „Zinterpretujemy przepisy" | „Wskażemy, jak ująć to w księgach" |
| „Przejmujemy odpowiedzialność za Twoje rozliczenia" | „Odpowiadamy za poprawność ksiąg i terminowość tego, do czego mamy pełnomocnictwo" |
| „Pomożemy uzyskać status OPP" / „wpis do KRS" | pomijamy — to sprawa zarządu i prawnika |
| „Przygotujemy wypowiedzenie umowy" | „Podpowiemy, czego zażądać od poprzedniego biura" |
| kancelaria, doradztwo podatkowe, optymalizacja podatkowa, reprezentacja przed organami | nie używamy w ogóle |

Zasada ogólna: **możemy pomóc technicznie przejść przez proces, ale nie wykonujemy
czynności zastrzeżonych i nie bierzemy odpowiedzialności za obowiązki klienta.**

---

## Podział odpowiedzialności — tak to opisujemy

**Biuro odpowiada za:**
- poprawność księgową prowadzonych ksiąg, ewidencji i rejestrów,
- rzetelność wyliczeń podatków i składek na podstawie otrzymanych dokumentów,
- terminowość tego, do czego mamy pełnomocnictwo,
- ochronę danych zgodnie z RODO.

**Klient lub zarząd odpowiada za:**
- dostarczenie kompletnych i prawdziwych dokumentów w terminie,
- informowanie o istotnych zmianach w firmie lub organizacji,
- decyzje biznesowe,
- podpisanie i złożenie sprawozdania finansowego,
- obowiązki wynikające z umowy dotacji i wytycznych grantodawcy.

Jeśli klient dostarczy niepełne lub nieprawdziwe dane — odpowiedzialność jest po jego
stronie. Jeśli błąd wynika z zaniedbania biura — odpowiada biuro, w ramach polisy OC.

---

## Do przemyślenia — miejsca w istniejącym artykule wykraczające poza tę granicę

W artykule `czym-zajmuje-sie-biuro-rachunkowe` (plik `src/data/guides.ts`) są trzy
sformułowania, które wykraczają poza powyższą zasadę. Zostały tam z wcześniejszej wersji
serwisu i warto je przejrzeć:

1. „Interpretacja przepisów podatkowych" — interpretacja przepisów to czynność doradcy
   podatkowego. Bezpieczniej: „informowanie o zmianach w przepisach i o ich skutkach
   księgowych".
2. „Start-upy — wymagające wsparcia w rejestracji, wyborze formy działalności" — wybór
   formy działalności i formy opodatkowania to doradztwo. Bezpieczniej: „start-upy, które
   potrzebują poukładać księgowość od pierwszego miesiąca".
3. „To oni przejmują odpowiedzialność za rozliczenia" — wprost sprzeczne z podziałem
   odpowiedzialności opisanym w dalszej części tego samego artykułu.

Nie zmieniono ich samodzielnie, bo to treść merytoryczna serwisu — decyzja należy
do właścicielki.

---

## Ton i forma

- Piszemy po ludzku, konkretnie, bez korporacyjnego żargonu.
- Nie obiecujemy czasu reakcji w godzinach ani stałych kwot, jeśli nie ma ich w umowie.
- Nie podajemy konkretnych progów, limitów i dat ustawowych, które bywają zmieniane —
  piszemy „w terminach obowiązujących za dany rok". Nieaktualna liczba na stronie biura
  rachunkowego szkodzi bardziej niż jej brak.
- Poradniki i materiały edukacyjne zawsze z zastrzeżeniem, że nie stanowią porady prawnej
  ani podatkowej, a nadrzędne są przepisy oraz umowa klienta.
