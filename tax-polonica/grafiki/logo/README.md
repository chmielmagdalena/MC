# Logo Tax Polonica

Pliki odtwarzają znak ze strony: romb z literą T oraz napis złożony krojem
Playfair Display, z podpisem krojem Inter. Tekst jest zamieniony na krzywe,
więc pliki wyglądają tak samo wszędzie, bez instalowania fontów.

## Kolory

| | |
|---|---|
| złoty (romb) | `#B08D2F` |
| granatowy (nazwa) | `#1B2A4A` |
| szary (podpis) | `#6B7280` |

## Co wybrać

| Zastosowanie | Plik |
|---|---|
| katalogi firm, stopka maila, dokumenty | `logo-kolor-1200.png` (przezroczyste tło) |
| gdy system nie radzi sobie z przezroczystością | `logo-kolor-1200-na-bialym.png` |
| druk jednokolorowy, faks, pieczątka, ogłoszenie czarno-białe | `logo-czarne-1200.png` |
| ciemne tło, stopka na granacie | `logo-biale-1200.png` |
| zdjęcie profilowe, awatar, favicon | `sygnet-kolor-512.png`, `sygnet-kolor-1024.png` |
| profil wymagający kwadratu i jasnego tła | `profil-kwadrat-1024.png` |
| drukarnia, duży format, dowolne skalowanie | pliki `.svg` |

Pliki SVG skalują się bez utraty jakości i to one idą do drukarni. Pliki PNG
mają przezroczyste tło poza wariantem „na białym" i kwadratem profilowym.

## Zasady używania

Zostaw wokół znaku odstęp co najmniej wysokości rombu. Nie rozciągaj
nieproporcjonalnie, nie zmieniaj kolorów ani nie obracaj. Na niejednolitym
tle, na przykład na zdjęciu, użyj wariantu jednokolorowego.

Przy małych rozmiarach, poniżej mniej więcej 40 pikseli wysokości, podpis
„Biuro Rachunkowe" przestaje być czytelny. Wtedy lepszy jest sam sygnet.

## Skąd się wzięły

Wygenerowane ze znaku użytego na stronie (`src/components/Logo.tsx`
w repozytorium taxpolonica), żeby materiały zewnętrzne zgadzały się
z witryną. Skrypt generujący nie jest częścią repozytorium; przy zmianie
znaku na stronie pliki trzeba wygenerować ponownie.
