# -*- coding: utf-8 -*-
"""
Generator poradnika PDF: "Jak rozliczyć dotację, żeby przeszła bez uwag"
Tax Polonica — materiał bezpłatny do rozdawania.

Uruchomienie:  python3 generuj_poradnik.py
Wynik:         jak-rozliczyc-dotacje-poradnik.pdf
"""
import os
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether, ListFlowable,
                                ListItem, NextPageTemplate, PageBreak, PageTemplate,
                                Paragraph, Spacer, Table, TableStyle)

# ── marka ──────────────────────────────────────────────────────────────────
GRANAT = colors.HexColor("#1B2A4A")
ZLOTO = colors.HexColor("#B08D2F")
SZARY = colors.HexColor("#5A6270")
TLO = colors.HexColor("#F5F2EA")
TLO_UWAGA = colors.HexColor("#FBF3E4")
LINIA = colors.HexColor("#DCD8CC")

WWW = "www.taxpolonica.pl"
MAIL = "kontakt@taxpolonica.pl"

FONTS = "/usr/share/fonts/truetype/dejavu"
pdfmetrics.registerFont(TTFont("Body", f"{FONTS}/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("Body-Bold", f"{FONTS}/DejaVuSans-Bold.ttf"))
# DejaVu Sans nie ma odmiany pochyłej w systemie — kursywę bierzemy z Liberation Sans
ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"
pdfmetrics.registerFont(TTFont("Body-Italic", ITALIC if os.path.exists(ITALIC) else f"{FONTS}/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("Head", f"{FONTS}/DejaVuSerif-Bold.ttf"))
pdfmetrics.registerFontFamily("Body", normal="Body", bold="Body-Bold", italic="Body-Italic")

# ── style ──────────────────────────────────────────────────────────────────
S = {
    "cover_kicker": ParagraphStyle("ck", fontName="Body", fontSize=10.5, textColor=ZLOTO,
                                   alignment=TA_CENTER, leading=16, spaceAfter=10),
    "cover_title": ParagraphStyle("ct", fontName="Head", fontSize=27, textColor=colors.white,
                                  alignment=TA_CENTER, leading=36, spaceAfter=14),
    "cover_sub": ParagraphStyle("cs", fontName="Body", fontSize=12, textColor=colors.HexColor("#D8DCE4"),
                                alignment=TA_CENTER, leading=19),
    "cover_foot": ParagraphStyle("cf", fontName="Body", fontSize=10, textColor=colors.HexColor("#AAB2C0"),
                                 alignment=TA_CENTER, leading=16),
    "h1": ParagraphStyle("h1", fontName="Head", fontSize=18, textColor=GRANAT,
                         leading=24, spaceBefore=4, spaceAfter=12),
    "h2": ParagraphStyle("h2", fontName="Head", fontSize=12.5, textColor=GRANAT,
                         leading=18, spaceBefore=14, spaceAfter=6),
    "num": ParagraphStyle("num", fontName="Body-Bold", fontSize=9, textColor=ZLOTO,
                          leading=12, spaceAfter=2),
    "p": ParagraphStyle("p", fontName="Body", fontSize=10, textColor=colors.HexColor("#23282F"),
                        leading=15.5, alignment=TA_JUSTIFY, spaceAfter=8),
    "li": ParagraphStyle("li", fontName="Body", fontSize=10, textColor=colors.HexColor("#23282F"),
                         leading=15, spaceAfter=4),
    "box": ParagraphStyle("box", fontName="Body", fontSize=9.5, textColor=colors.HexColor("#23282F"),
                          leading=14.5, spaceAfter=5),
    "box_title": ParagraphStyle("bt", fontName="Body-Bold", fontSize=9.5, textColor=GRANAT,
                                leading=14, spaceAfter=4),
    "toc": ParagraphStyle("toc", fontName="Body", fontSize=10.5, textColor=colors.HexColor("#23282F"),
                          leading=21),
    "check": ParagraphStyle("chk", fontName="Body", fontSize=9.5, textColor=colors.HexColor("#23282F"),
                            leading=15.5, spaceAfter=3, leftIndent=2),
    "small": ParagraphStyle("sm", fontName="Body", fontSize=8.5, textColor=SZARY,
                            leading=13, spaceAfter=6),
    "th": ParagraphStyle("th", fontName="Body-Bold", fontSize=9.5, textColor=colors.white,
                         leading=14, spaceAfter=0),
}

# ── elementy pomocnicze ────────────────────────────────────────────────────
def P(t, s="p"):
    return Paragraph(t, S[s])

def bullets(items, style="li"):
    return ListFlowable(
        [ListItem(Paragraph(i, S[style]), leftIndent=14, value="circle") for i in items],
        bulletType="bullet", bulletFontSize=6, bulletColor=ZLOTO,
        leftIndent=12, bulletOffsetY=-2.5, spaceAfter=8,
    )

def numbered(items):
    return ListFlowable(
        [ListItem(Paragraph(i, S["li"]), leftIndent=16) for i in items],
        bulletType="1", bulletFontName="Body-Bold", bulletFontSize=10,
        bulletColor=ZLOTO, leftIndent=14, spaceAfter=8,
    )

def box(title, lines, bg=TLO, bar=ZLOTO):
    # jeden wiersz na akapit — dzięki temu długa ramka może się podzielić
    # między stronami zamiast zostawiać pustą dziurę na dole
    rows = []
    if title:
        rows.append([P(title, "box_title")])
    rows += [[P(l, "box")] for l in lines]
    t = Table(rows, colWidths=[165 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LEFTPADDING", (0, 0), (-1, -1), 11), ("RIGHTPADDING", (0, 0), (-1, -1), 11),
        ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (0, 0), 10), ("BOTTOMPADDING", (0, -1), (-1, -1), 10),
        ("LINEBEFORE", (0, 0), (0, -1), 2.5, bar),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return [t, Spacer(1, 10)]

def checklist(title, items):
    rows = [[P(title, "box_title")]]
    for i in items:
        rows.append([P("☐&nbsp;&nbsp;" + i, "check")])
    t = Table(rows, colWidths=[165 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), TLO),
        ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (0, 0), 10), ("BOTTOMPADDING", (0, -1), (-1, -1), 10),
        ("LINEBEFORE", (0, 0), (0, -1), 2.5, GRANAT),
    ]))
    # checklista ma sens tylko w całości — nie pozwalamy jej dzielić się między stronami
    return [KeepTogether([t, Spacer(1, 12)])]

def dwie_kolumny(naglowki, wiersze):
    data = [[P(naglowki[0], "th"), P(naglowki[1], "th")]]
    for a, b in wiersze:
        data.append([P(a, "box"), P(b, "box")])
    t = Table(data, colWidths=[78 * mm, 87 * mm], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GRANAT),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINIA),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#FAF9F6")]),
    ]))
    return [t, Spacer(1, 12)]

def rozdzial(numer, tytul):
    return [PageBreak(), P(f"ROZDZIAŁ {numer}", "num"), P(tytul, "h1")]

# ── szablony stron ─────────────────────────────────────────────────────────
def okladka(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(GRANAT)
    canvas.rect(0, 0, w, h, fill=1, stroke=0)
    canvas.setFillColor(ZLOTO)
    canvas.rect(0, h - 10 * mm, w, 10 * mm, fill=1, stroke=0)
    canvas.setStrokeColor(ZLOTO)
    canvas.setLineWidth(0.7)
    canvas.line(60 * mm, h - 118 * mm, 150 * mm, h - 118 * mm)
    canvas.restoreState()

def strona(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(ZLOTO)
    canvas.rect(0, h - 4 * mm, w, 4 * mm, fill=1, stroke=0)
    canvas.setStrokeColor(LINIA)
    canvas.setLineWidth(0.5)
    canvas.line(22 * mm, 15 * mm, w - 22 * mm, 15 * mm)
    canvas.setFont("Body", 7.5)
    canvas.setFillColor(SZARY)
    canvas.drawString(22 * mm, 10.5 * mm, f"Tax Polonica · {WWW} · {MAIL}")
    canvas.drawRightString(w - 22 * mm, 10.5 * mm, str(canvas.getPageNumber() - 1))
    canvas.restoreState()

def zbuduj(sciezka, story):
    doc = BaseDocTemplate(sciezka, pagesize=A4,
                          leftMargin=22 * mm, rightMargin=23 * mm,
                          topMargin=22 * mm, bottomMargin=22 * mm,
                          title="Jak rozliczyć dotację, żeby przeszła bez uwag",
                          author="Tax Polonica", subject="Poradnik dla fundacji i stowarzyszeń")
    ramka = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="n")
    ramka_ok = Frame(25 * mm, 30 * mm, A4[0] - 50 * mm, A4[1] - 60 * mm, id="c")
    doc.addPageTemplates([
        PageTemplate(id="okladka", frames=[ramka_ok], onPage=okladka),
        PageTemplate(id="tresc", frames=[ramka], onPage=strona),
    ])
    doc.build(story)

# ── treść ──────────────────────────────────────────────────────────────────
story = []

# OKŁADKA
story += [
    Spacer(1, 42 * mm),
    P("PORADNIK DLA FUNDACJI I STOWARZYSZEŃ", "cover_kicker"),
    P("Jak rozliczyć dotację,<br/>żeby przeszła bez uwag", "cover_title"),
    Spacer(1, 16 * mm),
    P("Od pierwszej faktury do sprawozdania końcowego.<br/>"
      "Praktycznie, po ludzku, z checklistami do odhaczenia.", "cover_sub"),
    Spacer(1, 52 * mm),
    P("Tax Polonica · biuro rachunkowe<br/>"
      f"{WWW} · {MAIL}<br/>Wrocław · obsługa organizacji w całej Polsce", "cover_foot"),
    NextPageTemplate("tresc"),
    PageBreak(),
]

# WSTĘP + SPIS TREŚCI
story += [
    P("Zanim zaczniesz", "h1"),
    P("Rozliczenie dotacji rzadko sypie się na końcu. Sypie się na początku — przy pierwszej fakturze, "
      "która trafiła do segregatora bez opisu, przy umowie zlecenia bez wskazania projektu, przy wydatku "
      "poniesionym dzień przed formalnym rozpoczęciem zadania. Kilka miesięcy później ktoś siada do sprawozdania "
      "i okazuje się, że części dokumentów nie da się już poprawić.", "p"),
    P("Ten poradnik prowadzi przez rozliczenie od końca do końca: co ustawić przed startem, jak opisywać dokumenty, "
      "co jest kosztem kwalifikowalnym, jak rozliczać wynagrodzenia i wkład własny, co sprawdza kontrola i jak "
      "złożyć sprawozdanie, które nie wróci z uwagami.", "p"),
    *box("Jak korzystać z tego poradnika", [
        "<b>Jeśli rozliczasz dotację pierwszy raz</b> — przeczytaj po kolei rozdziały 1–4 i skorzystaj z checklisty startowej "
        "na końcu. To wystarczy, żeby nie popełnić błędów nie do naprawienia.",
        "<b>Jeśli masz doświadczenie w projektach</b> — zajrzyj do rozdziałów 5–11 i do listy dziesięciu najczęstszych błędów. "
        "Fragmenty oznaczone <b>„Krok dalej”</b> dotyczą sytuacji trudniejszych: podziału wynagrodzeń, kosztów pośrednich, VAT-u.",
        "<b>Jeśli właśnie składasz sprawozdanie</b> — zacznij od rozdziału 10 i checklisty przedsprawozdaniowej.",
    ]),
    *box("Jedna zasada ważniejsza niż ten poradnik", [
        "Nadrzędna jest zawsze <b>umowa dotacji i wytyczne konkretnego grantodawcy</b>. Programy różnią się między sobą — "
        "to, co w jednym jest dozwolone, w drugim bywa zakazane. Ten poradnik pokazuje mechanizmy i pytania, które "
        "trzeba sobie zadać; odpowiedzi szukaj w swojej umowie. Materiał ma charakter informacyjny i nie jest poradą "
        "prawną ani podatkową.",
    ], bg=TLO_UWAGA),
    Spacer(1, 6),
    P("Spis treści", "h2"),
]

spis = [
    "1. Zanim wydasz pierwszą złotówkę",
    "2. Wyodrębniona ewidencja — serce rozliczenia",
    "3. Opis dokumentu księgowego",
    "4. Kwalifikowalność kosztów",
    "5. Wynagrodzenia w projekcie",
    "6. Wkład własny i wolontariat",
    "7. Przesunięcia w budżecie i zmiany w projekcie",
    "8. Zamówienia i rozeznanie rynku",
    "9. Dokumentacja merytoryczna",
    "10. Sprawozdanie końcowe krok po kroku",
    "11. Kontrola — co sprawdzają najpierw",
    "12. Dziesięć najczęstszych błędów",
    "Checklisty do odhaczenia",
    "Wzór opisu faktury",
]
story.extend(Paragraph(x, ParagraphStyle("t", parent=S["toc"], leftIndent=8)) for x in spis)

# 1
story += rozdzial(1, "Zanim wydasz pierwszą złotówkę")
story += [
    P("Większość problemów rozliczeniowych da się wyeliminować w pierwszym tygodniu projektu. Poniżej sześć rzeczy, "
      "które warto ustawić, zanim pojawi się pierwszy wydatek.", "p"),
    P("Przeczytaj umowę dotacji — całą", "h2"),
    P("Nie streszczenie, nie maila od grantodawcy. Całą umowę wraz z załącznikami i wytycznymi, do których odsyła. "
      "Wypisz sobie na kartce pięć rzeczy: datę rozpoczęcia i zakończenia zadania, termin złożenia sprawozdania, "
      "termin zwrotu niewykorzystanych środków, dopuszczalne przesunięcia między pozycjami budżetu oraz wymagania dotyczące "
      "rachunku bankowego. Te pięć liczb wraca później w każdej decyzji.", "p"),
    P("Sprawdź daty kwalifikowalności", "h2"),
    P("Koszt jest kwalifikowalny, jeśli został poniesiony w okresie realizacji zadania określonym w umowie. Wydatek sprzed "
      "daty rozpoczęcia zwykle przepada — nawet jeśli dotyczy projektu i jest oczywiście potrzebny. To najczęstszy błąd "
      "organizacji, które zaczynają działać od razu po ogłoszeniu wyników konkursu, nie czekając na podpisanie umowy.", "p"),
    *box("Uwaga na dwie różne daty", [
        "<b>Data poniesienia kosztu</b> (kiedy powstało zobowiązanie — data sprzedaży lub wykonania usługi) i "
        "<b>data zapłaty</b> to nie to samo. Część programów wymaga, żeby obie mieściły się w okresie realizacji, "
        "inne dopuszczają zapłatę w kilkanastu dniach po zakończeniu. Sprawdź to w umowie, zanim zaplanujesz "
        "grudniowe faktury.",
    ], bg=TLO_UWAGA),
    P("Załóż wyodrębniony rachunek albo subkonto", "h2"),
    P("Wiele umów tego wymaga wprost, a nawet jeśli nie wymaga — zrób to. Osobny rachunek oznacza, że w każdej chwili "
      "widać, ile środków dotacji zostało, i że żaden prywatny czy statutowy przelew nie wymiesza się z projektem. "
      "Pamiętaj o odsetkach bankowych: w większości programów odsetki od środków dotacji podlegają zwrotowi razem "
      "z niewykorzystaną kwotą.", "p"),
    P("Ustal, kto za co odpowiada", "h2"),
    P("W małej organizacji wszystko robi jedna osoba i to jest największe ryzyko projektu. Ustalcie na piśmie, "
      "kto opisuje dokumenty merytorycznie, kto zatwierdza wydatek przed poniesieniem i kto pilnuje budżetu. "
      "Nawet jeśli to dwie osoby z zarządu — zapiszcie to.", "p"),
    P("Przygotuj plan kont pod projekt", "h2"),
    P("To rozmowa z księgową, którą trzeba odbyć przed pierwszą fakturą, nie przed sprawozdaniem. Szczegóły "
      "znajdziesz w następnym rozdziale.", "p"),
    P("Zrób kopię budżetu w arkuszu", "h2"),
    P("Najprostsze narzędzie kontrolne, jakie istnieje: kolumny z pozycjami budżetu, kwotą planowaną, kwotą wydaną "
      "i różnicą. Aktualizowany co tydzień arkusz oszczędza dramatów w ostatnim miesiącu, gdy okazuje się, że "
      "jedna pozycja jest przekroczona o 40 procent.", "p"),
]

# 2
story += rozdzial(2, "Wyodrębniona ewidencja — serce rozliczenia")
story += [
    P("Jeśli miałabyś zapamiętać z tego poradnika jedną rzecz, to tę: <b>każdy koszt projektu musi dać się wyciągnąć "
      "z ksiąg osobno, bez ręcznego przeglądania segregatorów</b>. Obowiązek wyodrębnionej ewidencji księgowej środków "
      "z dotacji wynika wprost z przepisów o działalności pożytku publicznego, a w praktyce jest pierwszą rzeczą, "
      "o którą pyta kontrola.", "p"),
    P("Co to znaczy w praktyce", "h2"),
    P("Wyodrębniona ewidencja to nie osobny zeszyt ani plik w Excelu prowadzony obok księgowości. To sposób "
      "zapisywania operacji w księgach organizacji, który pozwala w każdej chwili wydrukować zestawienie: "
      "wszystkie przychody i koszty tego jednego projektu, w podziale na pozycje budżetu.", "p"),
    P("Technicznie osiąga się to najczęściej na dwa sposoby:", "p"),
    numbered([
        "<b>Konta analityczne</b> — do kont zespołu kosztów dodaje się analitykę projektu, np. 4-01-<b>PROJ1</b>-01 dla "
        "wynagrodzeń w projekcie, 4-01-<b>PROJ1</b>-02 dla materiałów. Każda pozycja budżetu dostaje swoją analitykę.",
        "<b>Znaczniki (wymiary) projektu</b> — w nowocześniejszych programach księgowych każdy zapis można oznaczyć "
        "projektem i pozycją budżetu, a raport generuje się po tych znacznikach.",
    ]),
    P("Który sposób wybierze Twoje biuro, jest wtórne. Ważne, żeby wybór zapadł <b>przed</b> pierwszym zapisem — "
      "przeksięgowanie kilkuset pozycji w połowie projektu to praca, za którą ktoś musi zapłacić.", "p"),
    *box("Krok dalej: analityka pod pozycje budżetu, nie pod rodzaje kosztów", [
        "Częsty błąd organizacji z doświadczeniem: analityka odwzorowuje księgowy podział kosztów (materiały, usługi obce, "
        "wynagrodzenia), a sprawozdanie wymaga podziału na pozycje budżetu z wniosku (koordynacja, promocja, warsztaty). "
        "Potem ktoś ręcznie przekłada jedno na drugie i myli się o kilkaset złotych.",
        "<b>Zasada:</b> analityka ma odpowiadać budżetowi z wniosku — pozycja w pozycję, w tej samej kolejności i z tymi samymi nazwami. "
        "Wtedy sprawozdanie powstaje z wydruku, a nie z przepisywania.",
    ]),
    P("Zestawienie, które warto drukować co miesiąc", "h2"),
    P("Poproś księgową o comiesięczny wydruk kosztów projektu w układzie pozycji budżetu. Dziesięć minut miesięcznie "
      "kosztuje mniej niż jeden wieczór szukania różnicy w listopadzie. Jeśli biuro odpowiada, że „nie da się tak "
      "wydrukować” — to sygnał, że ewidencja nie została wyodrębniona.", "p"),
]

# 3
story += rozdzial(3, "Opis dokumentu księgowego")
story += [
    P("Faktura bez opisu jest dla grantodawcy paragonem z nieznanego sklepu. Opis łączy dokument z projektem, "
      "pozycją budżetu i źródłem finansowania — i to on, a nie sama faktura, jest dowodem w rozliczeniu.", "p"),
    P("Co musi znaleźć się w opisie", "h2"),
]
story.extend(dwie_kolumny(
    ["Element opisu", "Przykład zapisu"],
    [
        ("Nazwa projektu i numer umowy", "„Młodzi dla Wrocławia”, umowa nr 123/2026 z 12.03.2026"),
        ("Pozycja budżetu", "Poz. 4 budżetu — materiały warsztatowe"),
        ("Źródło finansowania i podział kwoty",
         "Kwota 1 230,00 zł, w tym: dotacja 1 000,00 zł, wkład własny 230,00 zł"),
        ("Opis merytoryczny — po co ten wydatek",
         "Zakup materiałów plastycznych na 6 warsztatów dla 60 uczestników, zrealizowanych w maju 2026 r."),
        ("Potwierdzenie zgodności z procedurami",
         "Wydatek poniesiony zgodnie z umową dotacji oraz procedurą rozeznania rynku z dnia …"),
        ("Dekretacja księgowa", "Konto 4-01-PROJ1-04 (uzupełnia księgowość)"),
        ("Podpisy", "Osoba opisująca merytorycznie, osoba zatwierdzająca do wypłaty, księgowa"),
    ]))
story += [
    *box("Gdzie umieścić opis", [
        "Klasycznie: pieczątka lub odręczny opis na odwrocie faktury. Jeśli dokument jest elektroniczny albo opis "
        "się nie mieści — przygotuj załącznik opisowy trwale połączony z fakturą i podpisany tak samo. Nie rób opisów "
        "wyłącznie w arkuszu na dysku: przy kontroli liczą się dokumenty, nie tabelki.",
        "Opisuj <b>na bieżąco</b>. Opisywanie stu faktur w ostatnim tygodniu projektu kończy się tym, że nikt "
        "nie pamięta, ilu uczestników było na warsztacie w marcu.",
    ]),
    P("Krok dalej: faktury dzielone między źródła", "h2"),
    P("Gdy jedna faktura finansuje dwa projekty albo projekt i działalność statutową, opis musi pokazywać <b>klucz podziału</b>: "
      "nie tylko że 60 procent idzie na projekt A, ale też dlaczego akurat 60. Klucz powinien być możliwy do zweryfikowania — "
      "liczba uczestników, metry kwadratowe, godziny pracy, liczba wydrukowanych egzemplarzy. Klucz „przyjęty szacunkowo” "
      "jest pierwszym kandydatem do zakwestionowania.", "p"),
]

# 4
story += rozdzial(4, "Kwalifikowalność kosztów")
story += [
    P("Koszt kwalifikowalny to taki, który grantodawca uzna i sfinansuje. Zasady różnią się między programami, "
      "ale cztery warunki powtarzają się niemal zawsze.", "p"),
]
story.extend(dwie_kolumny(
    ["Warunek", "Co to znaczy w praktyce"],
    [
        ("Związek z projektem",
         "Wydatek służy realizacji zadania opisanego we wniosku. Musisz umieć wyjaśnić związek jednym zdaniem."),
        ("Ujęcie w budżecie",
         "Pozycja istnieje w zatwierdzonym budžcie, a kwota mieści się w limicie lub dopuszczalnym przesunięciu."),
        ("Okres realizacji",
         "Koszt poniesiony między datą rozpoczęcia a zakończenia zadania, zgodnie z umową."),
        ("Udokumentowanie",
         "Jest faktura lub równoważny dokument, opis, dowód zapłaty i ślad w księgach."),
        ("Gospodarność",
         "Cena odpowiada warunkom rynkowym. Przy większych kwotach potrzebne rozeznanie rynku — zob. rozdział 8."),
    ]))
story += [
    P("Koszty, które najczęściej są odrzucane", "h2"),
    bullets([
        "wydatki poniesione przed rozpoczęciem lub po zakończeniu okresu realizacji zadania,",
        "kary, grzywny, odsetki za zwłokę i koszty postępowań sądowych,",
        "VAT, który organizacja może odliczyć (zob. ramka niżej),",
        "koszty już sfinansowane z innego źródła publicznego — tzw. podwójne finansowanie,",
        "wydatki nieujęte w budžcie i nieobjęte zaakceptowaną zmianą,",
        "zakupy środków trwałych, jeśli program ich nie przewiduje,",
        "koszty bez wiarygodnego dokumentu — paragon zamiast faktury tam, gdzie wymagana jest faktura.",
    ]),
    *box("Krok dalej: VAT w projekcie", [
        "Reguła jest prosta w słowach i kłopotliwa w praktyce: <b>VAT jest kosztem kwalifikowalnym tylko wtedy, "
        "gdy organizacja nie ma prawa go odliczyć</b>. Jeśli organizacja jest czynnym podatnikiem VAT i odlicza podatek "
        "od danego zakupu, do rozliczenia wchodzi kwota netto.",
        "Problem pojawia się u organizacji, które prowadzą działalność mieszaną — część sprzedaży zwolniona, część "
        "opodatkowana. Wtedy prawo do odliczenia bywa częściowe i wymaga ustalenia proporcji. To rozmowa do odbycia "
        "z księgową na etapie składania wniosku, nie przy rozliczeniu — bo od tego zależy, czy w budžcie planujesz kwoty "
        "brutto czy netto.",
    ]),
    P("Koszty administracyjne i pośrednie", "h2"),
    P("Większość programów dopuszcza finansowanie części kosztów funkcjonowania organizacji — księgowości, czynszu, "
      "telefonu, obsługi biura — do określonego procentu dotacji. Dwie rzeczy, o których warto pamiętać: limit "
      "liczy się zwykle od wartości dotacji, nie całego budżetu, a koszty pośrednie też muszą być udokumentowane. "
      "Ryczałt nie zawsze oznacza brak dokumentów — sprawdź to w wytycznych.", "p"),
]

# 5
story += rozdzial(5, "Wynagrodzenia w projekcie")
story += [
    P("Wynagrodzenia to największa pozycja w większości projektów i najczęstszy punkt zapalny kontroli. "
      "Podstawowa zasada: <b>z dokumentów musi wynikać, że dana osoba pracowała dla tego projektu, w tym okresie "
      "i w tym wymiarze</b>.", "p"),
    P("Forma zatrudnienia", "h2"),
    bullets([
        "<b>Umowa o pracę</b> — w treści umowy lub aneksie wskazuje się projekt i wymiar zaangażowania. "
        "Do rozliczenia wchodzi wynagrodzenie brutto wraz ze składkami po stronie pracodawcy.",
        "<b>Umowa zlecenia</b> — w treści nazwa projektu, zakres zadań i okres. Do umowy dołącza się rachunek "
        "i najczęściej ewidencję godzin.",
        "<b>Umowa o dzieło</b> — tylko tam, gdzie faktycznie powstaje dzieło o indywidualnym charakterze "
        "(scenariusz, publikacja, projekt graficzny). Cykliczne prowadzenie warsztatów dziełem nie jest, "
        "a przekwalifikowanie umowy przez ZUS oznacza składki wstecz.",
        "<b>Faktura od osoby prowadzącej działalność</b> — dopuszczalna, jeśli program tego nie wyklucza; "
        "uwaga na powiązania z członkami zarządu.",
    ]),
    *box("Dokumenty, które muszą być w teczce każdej osoby", [
        "umowa ze wskazaniem projektu · rachunek lub lista płac · ewidencja czasu pracy, jeśli program jej wymaga · "
        "potwierdzenie przelewu wynagrodzenia · deklaracje i potwierdzenia zapłaty składek oraz zaliczki na podatek · "
        "przy umowie o dzieło — zgłoszenie umowy do ZUS, jeśli było wymagane.",
    ]),
    P("Krok dalej: jedna osoba, kilka projektów", "h2"),
    P("To sytuacja, w której najczęściej sypie się rozliczenie w organizacjach z kilkoma dotacjami naraz. "
      "Koordynatorka pracuje przy trzech projektach i działalności statutowej, a jej wynagrodzenie dzielone jest "
      "„mniej więcej po równo”. Przy kontroli pierwszego projektu pada pytanie, na jakiej podstawie przyjęto te proporcje "
      "— i nie ma odpowiedzi.", "p"),
    P("Rozwiązanie jest mniej pracochłonne, niż się wydaje: prowadźcie <b>jedną ewidencję czasu pracy na osobę</b>, "
      "z podziałem na projekty, podpisywaną co miesiąc. Podział wynagrodzenia wynika wtedy z godzin, a nie z deklaracji. "
      "Dodatkowo pilnujcie, żeby łączne zaangażowanie jednej osoby nie przekraczało realnych możliwości czasowych — "
      "kontrolerzy sumują etaty między projektami i to jest łatwa do wychwycenia nieprawidłowość.", "p"),
    *box("Wynagrodzenie członka zarządu", [
        "Część programów dopuszcza je, część wyłącza. Niezależnie od tego, w stowarzyszeniach i fundacjach obowiązują "
        "szczególne zasady reprezentacji przy umowach z członkami zarządu — umowy nie może podpisać sam zainteresowany. "
        "Sprawdź statut i przepisy, zanim taka umowa powstanie, bo jej późniejsza naprawa bywa niemożliwa.",
    ], bg=TLO_UWAGA),
]

# 6
story += rozdzial(6, "Wkład własny i wolontariat")
story += [
    P("Wkład własny bywa traktowany jako formalność do wpisania we wniosku — aż do momentu, gdy przy rozliczeniu "
      "trzeba go udokumentować. Wtedy okazuje się, że nikt nie zbierał kart pracy wolontariuszy.", "p"),
    P("Trzy rodzaje wkładu", "h2"),
    bullets([
        "<b>Finansowy</b> — środki własne organizacji lub z innego źródła, wydane na projekt. Dokumentuje się "
        "dokładnie tak samo jak dotację: faktura, opis, przelew, zapis w księgach.",
        "<b>Osobowy</b> — praca wolontariuszy i nieodpłatna praca członków organizacji.",
        "<b>Rzeczowy</b> — udostępnienie sali, sprzętu, materiałów. Wymaga wyceny i dokumentu potwierdzającego "
        "użyczenie; nie wszystkie programy go dopuszczają.",
    ]),
    P("Jak udokumentować pracę wolontariusza", "h2"),
    numbered([
        "<b>Porozumienie wolontariackie</b> — na piśmie, ze wskazaniem zakresu, miejsca i czasu świadczenia. "
        "Przy współpracy dłuższej niż 30 dni forma pisemna jest obowiązkowa, a organizacja ma obowiązki "
        "ubezpieczeniowe wobec wolontariusza.",
        "<b>Karta pracy wolontariusza</b> — data, liczba godzin, opis wykonanych czynności, podpis wolontariusza "
        "i koordynatora. To ona jest dowodem w rozliczeniu.",
        "<b>Wycena</b> — stawka godzinowa na poziomie rynkowym dla danego rodzaju pracy. Nie zawyżaj: wycena pracy "
        "przy ulotkach na poziomie stawki trenerskiej jest pierwszą rzeczą, którą kwestionuje kontrola. "
        "Zapisz, skąd wzięła się stawka.",
    ]),
    *box("Najczęstszy błąd", [
        "Karty pracy wypełniane hurtem na koniec projektu, wszystkie tym samym długopisem, z okrągłymi liczbami godzin. "
        "Kontrolerzy widzą takie komplety regularnie. Karta wypełniana po każdym działaniu zajmuje minutę i jest "
        "nie do podważenia.",
    ], bg=TLO_UWAGA),
]

# 7
story += rozdzial(7, "Przesunięcia w budżecie i zmiany w projekcie")
story += [
    P("Prawie żaden projekt nie realizuje się dokładnie tak, jak go zaplanowano. To normalne i grantodawcy to wiedzą — "
      "problemem nie jest zmiana, tylko zmiana niezgłoszona.", "p"),
    P("Co zwykle wolno bez pytania", "h2"),
    P("Wiele umów dopuszcza przesunięcia między pozycjami budżetu do określonego procentu — często kilkunastu — "
      "bez aneksu, pod warunkiem zachowania celu i rezultatów zadania. Sprawdź konkretną wartość w swojej umowie "
      "i zapisz ją w arkuszu budżetowym, żeby nie liczyć jej za każdym razem od nowa.", "p"),
    P("Co wymaga zgody albo aneksu", "h2"),
    bullets([
        "przekroczenie dopuszczalnego progu przesunięć między pozycjami,",
        "dodanie pozycji, której w budžcie nie było,",
        "zmiana terminów realizacji zadania,",
        "istotna zmiana zakresu działań lub liczby uczestników,",
        "zmiana rachunku bankowego lub danych organizacji.",
    ]),
    *box("Zasada, która oszczędza kłopotów", [
        "Zgłaszaj zmianę <b>zanim</b> ją wprowadzisz, na piśmie lub mailem, i zachowaj odpowiedź. Zgoda uzyskana "
        "telefonicznie nie istnieje w rozliczeniu. Jeśli opiekun projektu odpowiada mailem — ten mail jest dokumentem; "
        "wydrukuj go i dołącz do dokumentacji projektu.",
    ]),
    P("Oszczędności w projekcie", "h2"),
    P("Jeśli coś wyszło taniej, niż planowano, niewykorzystana część dotacji zwykle podlega zwrotowi — chyba że "
      "grantodawca zgodzi się na przeznaczenie jej na inne działania w projekcie. O taką zgodę trzeba wystąpić "
      "przed końcem realizacji zadania, nie po sprawozdaniu.", "p"),
]

# 8
story += rozdzial(8, "Zamówienia i rozeznanie rynku")
story += [
    P("Wydatkowanie środków publicznych wiąże się z obowiązkiem gospodarności. W praktyce oznacza to, że przy "
      "większych zakupach trzeba wykazać, że cena była rynkowa — a nie że wybrano firmę szwagra.", "p"),
    P("Jak wygląda rozeznanie rynku", "h2"),
    numbered([
        "Opisz przedmiot zamówienia — co dokładnie kupujesz, w jakiej ilości i jakości.",
        "Zbierz oferty — najczęściej trzy. Mogą to być maile, wydruki ze stron sprzedawców, oferty z portali. "
        "Zapisz datę pozyskania każdej.",
        "Porównaj i wybierz — krótka notatka z uzasadnieniem wyboru. Najtańsza oferta nie zawsze musi wygrać, "
        "ale wybór droższej wymaga wyjaśnienia.",
        "Zachowaj komplet — oferty i notatka trafiają do dokumentacji projektu i są powołane w opisie faktury.",
    ]),
    *box("Powiązania osobowe", [
        "Zakup od członka zarządu, jego firmy albo osoby bliskiej nie zawsze jest zakazany — ale zawsze jest "
        "podejrzany i często wprost wyłączony w wytycznych. Jeśli nie da się tego uniknąć, sprawdź zapisy "
        "programu, udokumentuj rozeznanie rynku szczególnie starannie i wyłącz zainteresowaną osobę z decyzji "
        "o wyborze oferty.",
    ], bg=TLO_UWAGA),
]

# 9
story += rozdzial(9, "Dokumentacja merytoryczna")
story += [
    P("Rozliczenie dotacji to nie tylko faktury. Grantodawca finansuje rezultaty, więc musi zobaczyć, "
      "że działania faktycznie się odbyły i dotarły do zadeklarowanej liczby osób.", "p"),
    P("Co zbierać na bieżąco", "h2"),
    bullets([
        "<b>Listy obecności</b> — data, nazwa działania, podpisy uczestników. Przy dzieciach — zgody opiekunów.",
        "<b>Dokumentacja zdjęciowa</b> — kilka zdjęć z każdego działania, ze zgodami na wizerunek.",
        "<b>Materiały wytworzone w projekcie</b> — egzemplarze publikacji, ulotek, plakatów, scenariuszy zajęć.",
        "<b>Dowód oznakowania</b> — zdjęcia lub pliki pokazujące logo i informację o finansowaniu tam, gdzie "
        "wymaga tego umowa: na plakatach, w mediach społecznościowych, na stronie, na sali.",
        "<b>Ślad w mediach</b> — zrzuty ekranu postów, linki do artykułów, wydruki ze strony.",
        "<b>Ankiety lub inne mierniki rezultatów</b>, jeśli wniosek je przewidywał.",
    ]),
    *box("Obowiązek informacyjny to nie ozdobnik", [
        "Brak logotypów grantodawcy na materiałach bywa podstawą do zakwestionowania kosztów promocji. "
        "Sprawdź wymagane oznaczenia <b>przed</b> drukiem — dodruk plakatów na własny koszt to najbardziej "
        "frustrujący wydatek w całym projekcie.",
    ]),
    P("Dane osobowe uczestników", "h2"),
    P("Listy obecności, zgody i ankiety to dane osobowe. Zbieraj tylko to, czego naprawdę wymaga umowa, "
      "poinformuj uczestników o celu przetwarzania i przechowuj dokumenty tak, żeby nie leżały w ogólnodostępnym "
      "miejscu. Okres przechowywania dokumentacji projektowej wynika z umowy — zwykle jest dłuższy, niż się ludziom wydaje.", "p"),
]

# 10
story += rozdzial(10, "Sprawozdanie końcowe krok po kroku")
story += [
    P("Jeśli poprzednie rozdziały zostały zrobione na bieżąco, sprawozdanie jest czynnością techniczną na kilka godzin. "
      "Jeśli nie — jest rekonstrukcją wydarzeń sprzed roku. Ta różnica jest całą treścią tego poradnika.", "p"),
    P("Kolejność pracy", "h2"),
    numbered([
        "<b>Wydrukuj zestawienie kosztów projektu z ksiąg</b> w układzie pozycji budżetu. To punkt wyjścia — "
        "nie arkusz prowadzony równolegle, tylko dane z ewidencji.",
        "<b>Porównaj z budżetem</b> pozycja po pozycji. Każda różnica musi mieć wyjaśnienie: przesunięcie w granicach "
        "umowy, zaakceptowana zmiana albo oszczędność do zwrotu.",
        "<b>Sprawdź komplet dokumentów</b> — czy każda pozycja zestawienia ma fakturę, opis i dowód zapłaty.",
        "<b>Zestaw wkład własny</b> — finansowy z ksiąg, osobowy z kart pracy wolontariuszy.",
        "<b>Napisz część merytoryczną</b> — odnieś się do każdego działania i każdego rezultatu z wniosku, "
        "tymi samymi nazwami. Jeśli rezultat nie został osiągnięty — napisz to wprost i wyjaśnij dlaczego. "
        "Przemilczenie jest gorsze niż niepowodzenie.",
        "<b>Policz zwrot</b> — niewykorzystana część dotacji plus, jeśli umowa tak stanowi, odsetki bankowe "
        "od środków na rachunku.",
        "<b>Zrób zwrot w terminie</b> — zwykle liczonym w dniach od zakończenia realizacji zadania, często krótszym "
        "niż termin na sprawozdanie. Spóźniony zwrot oznacza odsetki jak od zaległości podatkowych.",
        "<b>Złóż sprawozdanie</b> w terminie i w formie wymaganej przez grantodawcę — w generatorze, przez e‑PUAP "
        "albo papierowo. Zachowaj potwierdzenie złożenia.",
    ]),
    *box("Dwa terminy, które warto mieć w kalendarzu od pierwszego dnia", [
        "<b>Termin zwrotu niewykorzystanych środków</b> i <b>termin złożenia sprawozdania</b>. To zwykle dwie różne daty, "
        "a ta pierwsza bywa wcześniejsza. Wpisz obie do kalendarza w dniu podpisania umowy, z przypomnieniem "
        "na dwa tygodnie wcześniej.",
    ], bg=TLO_UWAGA),
    P("Gdy sprawozdanie wróci z uwagami", "h2"),
    P("To nie katastrofa i zdarza się dość często. Odpowiadaj konkretnie na każdą uwagę, w tej samej kolejności, "
      "dołączając brakujące dokumenty. Dotrzymaj terminu na uzupełnienie — on bywa krótki. Jeśli grantodawca kwestionuje "
      "koszt, a masz argumenty, przedstaw je rzeczowo: decyzje bywają zmieniane.", "p"),
]

# 11
story += rozdzial(11, "Kontrola — co sprawdzają najpierw")
story += [
    P("Kontrola projektu nie polega na czytaniu wszystkiego. Kontroler ma ograniczony czas i sprawdza w określonej "
      "kolejności — warto wiedzieć jakiej, bo to pokazuje, co przygotować najstaranniej.", "p"),
]
story.extend(dwie_kolumny(
    ["Co sprawdzają", "Czego szukają"],
    [
        ("Wyodrębniona ewidencja",
         "Czy istnieje i czy zestawienie z ksiąg zgadza się ze sprawozdaniem co do złotówki."),
        ("Największe pozycje kosztów",
         "Zwykle wynagrodzenia i usługi obce. Tu kontrola idzie najgłębiej."),
        ("Opisy dokumentów",
         "Czy są, czy są kompletne i czy nie wyglądają na wypełnione jednorazowo na końcu."),
        ("Daty",
         "Czy koszty mieszczą się w okresie realizacji. To najszybsza do wychwycenia nieprawidłowość."),
        ("Związek działań z rezultatami",
         "Czy liczba uczestników z list obecności odpowiada temu, co napisano w sprawozdaniu."),
        ("Podział kosztów wspólnych",
         "Na jakiej podstawie przyjęto klucz podziału między projekty i działalność statutową."),
        ("Powiązania osobowe",
         "Czy kontrahenci nie są powiązani z zarządem organizacji."),
    ]))
story += [
    *box("Jak się zachować podczas kontroli", [
        "Przygotuj dokumentację projektu w jednym miejscu i w kolejności pozycji budżetu. Odpowiadaj na pytania, "
        "które padają — nie opowiadaj więcej, niż trzeba. Jeśli czegoś nie wiesz, powiedz, że sprawdzisz i odpiszesz; "
        "to lepsze niż zgadywanie. Z protokołu kontroli masz prawo złożyć zastrzeżenia — korzystaj z tego, gdy uważasz, "
        "że ustalenia są błędne.",
    ]),
]

# 12
story += rozdzial(12, "Dziesięć najczęstszych błędów")
story += [
    P("Zestawienie z praktyki — uszeregowane od najczęstszych. Pierwsze pięć odpowiada za większość uwag "
      "w rozliczeniach.", "p"),
]
story.append(numbered([
    "<b>Brak wyodrębnionej ewidencji.</b> Koszty projektu wymieszane z pozostałymi, zestawienie robione ręcznie "
    "z segregatora. Naprawa: rozmowa z księgową przed pierwszą fakturą.",
    "<b>Faktury bez opisów albo opisywane hurtem na końcu.</b> Widać to na pierwszy rzut oka i podważa wiarygodność "
    "całej dokumentacji.",
    "<b>Wydatek poza okresem realizacji.</b> Zamówienie złożone przed podpisaniem umowy albo faktura wystawiona "
    "tydzień po zakończeniu zadania.",
    "<b>Przekroczenie pozycji budżetu bez zgłoszenia.</b> Przesunięcie ponad dopuszczalny próg, o którym nikt "
    "nie poinformował grantodawcy.",
    "<b>Wynagrodzenia bez śladu podziału między projekty.</b> Brak ewidencji czasu pracy przy osobie "
    "zaangażowanej w kilka działań.",
    "<b>Karty pracy wolontariuszy wypełnione jednego dnia.</b> Wkład osobowy zakwestionowany w całości.",
    "<b>VAT rozliczony niezgodnie z prawem do odliczenia.</b> Kwoty brutto w projekcie organizacji, która VAT odlicza.",
    "<b>Brak rozeznania rynku przy większym zakupie.</b> Albo rozeznanie sporządzone po fakcie, z datami "
    "późniejszymi niż faktura.",
    "<b>Spóźniony zwrot niewykorzystanej dotacji.</b> Skutek: odsetki, a przy poważniejszych uchybieniach — "
    "wykluczenie z kolejnych konkursów.",
    "<b>Sprawozdanie merytoryczne niezgodne z wnioskiem.</b> Inne nazwy działań, inne wskaźniki, brak odniesienia "
    "do części rezultatów — przez co nie da się stwierdzić, czy zadanie wykonano.",
]))

# CHECKLISTY
story += [PageBreak(), P("DO ODHACZENIA", "num"), P("Checklisty", "h1")]
story.extend(checklist("Na start — pierwszy tydzień projektu", [
    "Przeczytana cała umowa wraz z załącznikami i wytycznymi",
    "Wypisane daty: rozpoczęcie, zakończenie, zwrot środków, sprawozdanie",
    "Terminy wpisane do kalendarza z przypomnieniem dwa tygodnie wcześniej",
    "Znany dopuszczalny próg przesunięć między pozycjami budżetu",
    "Założony wyodrębniony rachunek lub subkonto",
    "Ustalona z księgową analityka odpowiadająca pozycjom budżetu",
    "Przygotowany arkusz kontroli budżetu: plan, wykonanie, różnica",
    "Ustalone, kto opisuje dokumenty i kto zatwierdza wydatki",
    "Znane wymagane oznakowanie materiałów — przed pierwszym drukiem",
    "Przygotowane wzory: opis faktury, karta pracy wolontariusza, lista obecności",
]))
story.extend(checklist("Co miesiąc", [
    "Wszystkie faktury miesiąca opisane i przekazane do księgowości",
    "Wydruk kosztów projektu z ksiąg, w układzie pozycji budżetu",
    "Arkusz kontroli budżetu zaktualizowany, różnice wyjaśnione",
    "Ewidencje czasu pracy podpisane przez osoby zaangażowane w projekt",
    "Karty pracy wolontariuszy z tego miesiąca uzupełnione i podpisane",
    "Listy obecności i zdjęcia z działań zebrane w jednym miejscu",
    "Sprawdzone, czy nie zbliża się przekroczenie którejś pozycji budżetu",
]))
story.extend(checklist("Przed złożeniem sprawozdania", [
    "Zestawienie z ksiąg zgadza się ze sprawozdaniem co do złotówki",
    "Każda pozycja ma fakturę, opis i dowód zapłaty",
    "Wszystkie koszty mieszczą się w okresie realizacji zadania",
    "Różnice wobec budżetu wyjaśnione lub zgłoszone i zaakceptowane",
    "Wkład własny finansowy udokumentowany tak samo jak dotacja",
    "Wkład osobowy poparty porozumieniami i kartami pracy",
    "Część merytoryczna odnosi się do każdego działania i rezultatu z wniosku",
    "Niezrealizowane rezultaty opisane wprost, z wyjaśnieniem",
    "Policzony zwrot niewykorzystanych środków wraz z odsetkami bankowymi",
    "Zwrot wykonany w terminie z umowy — wcześniejszym niż sprawozdanie",
    "Zachowane potwierdzenie złożenia sprawozdania",
    "Dokumentacja projektu skompletowana i odłożona na okres wymagany umową",
]))

# WZÓR OPISU
story += [PageBreak(), P("DO SKOPIOWANIA", "num"), P("Wzór opisu faktury", "h1"),
          P("Poniższy wzór wystarczy dostosować do swojego projektu i wydrukować jako naklejkę albo "
            "załącznik do dokumentu. Elementy w nawiasach kwadratowych uzupełniasz przy każdej fakturze.", "p")]
wzor = [
    "<b>Projekt:</b> [nazwa zadania zgodna z wnioskiem]",
    "<b>Umowa dotacji nr:</b> [numer] z dnia [data], zawarta z [nazwa grantodawcy]",
    "<b>Pozycja budżetu:</b> [numer i nazwa pozycji]",
    "<b>Kwota dokumentu:</b> [brutto] zł, w tym finansowane z dotacji: [kwota] zł, "
    "z wkładu własnego: [kwota] zł",
    "<b>Opis merytoryczny:</b> [co zakupiono lub zlecono, na potrzeby jakiego działania, "
    "kiedy i dla ilu osób się ono odbyło]",
    "<b>Klucz podziału</b> (jeśli dokument dotyczy też innych działań): [np. 60% — udział godzin "
    "przepracowanych w projekcie według ewidencji czasu pracy za [miesiąc]]",
    "<b>Tryb wyboru wykonawcy:</b> [np. rozeznanie rynku z dnia …, zebrano 3 oferty, "
    "wybrano ofertę najkorzystniejszą]",
    "<b>Oświadczenie:</b> Wydatek poniesiony zgodnie z umową dotacji, w okresie realizacji zadania, "
    "jest niezbędny do jego wykonania i nie został sfinansowany z innego źródła.",
    "<b>Dekretacja:</b> [konto analityczne — uzupełnia księgowość]",
    "<b>Sprawdzono pod względem merytorycznym:</b> [imię, nazwisko, data, podpis]",
    "<b>Zatwierdzono do wypłaty:</b> [imię, nazwisko, data, podpis]",
]
story.extend(box(None, wzor, bg=colors.HexColor("#FAF9F6"), bar=GRANAT))
story.append(P("Wskazówka: nie wszystkie pola będą potrzebne przy każdym dokumencie. Klucz podziału uzupełniasz tylko "
               "przy kosztach wspólnych, tryb wyboru wykonawcy — tylko tam, gdzie rozeznanie rynku było wymagane. "
               "Reszta powinna pojawiać się zawsze.", "small"))

# KONTAKT
story += [PageBreak(), P("NA KONIEC", "num"), P("Jeśli chcesz mieć to z głowy", "h1"),
          P("Ten poradnik opisuje, co trzeba zrobić. Nie zmienia tego, że w małej organizacji robi to zwykle "
            "ta sama osoba, która prowadzi warsztaty, pisze wnioski i odpowiada na maile — wieczorami.", "p"),
          P("W Tax Polonica prowadzimy księgowość fundacji i stowarzyszeń. Ustawiamy wyodrębnioną ewidencję "
            "od pierwszej faktury, pilnujemy budżetu w trakcie projektu, a nie po nim, i przygotowujemy część "
            "finansową sprawozdania. Obsługujemy też organizacje pożytku publicznego, działalność odpłatną "
            "i gospodarczą oraz kadry i płace w projektach.", "p"),
          *box("Co możemy zrobić od ręki", [
              "<b>Bezpłatny przegląd</b> — sprawdzimy, czy ewidencja projektów jest prowadzona poprawnie i czy "
              "nie płacicie za pełne księgi tam, gdzie wystarczy uproszczona ewidencja.",
              "<b>Przejęcie księgowości w trakcie roku</b> — z datą dopasowaną do kalendarza Waszych projektów, "
              "nie do kalendarza podatkowego. Nie trzeba czekać do stycznia.",
              "<b>Uporządkowanie zaległości</b> — jeśli sprawozdania czekają albo księgi wymagają poprawy, "
              "zaczynamy od przeglądu i wyceny, zanim cokolwiek podpiszemy.",
          ]),
          P(f"Napisz: <b>{MAIL}</b><br/>Więcej: <b>{WWW}</b><br/>"
            "Wrocław · obsługujemy organizacje z całej Polski, zdalnie.", "p"),
          Spacer(1, 10),
          P("Materiał bezpłatny. Możesz go przekazywać dalej innym organizacjom w całości i bez zmian.", "small"),
          P("Stan prawny ogólny; poradnik ma charakter informacyjny i nie stanowi porady prawnej ani podatkowej. "
            "Nadrzędne są zapisy umowy dotacji i wytyczne grantodawcy. Przed decyzjami skonsultuj się ze swoją "
            "księgową lub doradcą.", "small")]

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "jak-rozliczyc-dotacje-poradnik.pdf")
    zbuduj(out, story)
    print("Zapisano:", out)
