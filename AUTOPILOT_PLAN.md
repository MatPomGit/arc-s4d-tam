# Plan realizacji: arc-s4d-tam

**Wersja dokumentu: 1.0.0. Data: 2026-10-13.**
**Status: plan prac, zadania poniżej nie są oznaczone jako wykonane.**

Plan jest rozwinięciem aktualnego PROJECT_STATE.yaml i istniejących protokołów. Nie zmienia hipotez, kryteriów, zamrożonych metod ani statusu zgłoszeń. Źródła naukowe oraz dowody pozostają w dotychczasowych rejestrach. Przed następnym wykonaniem odczytaj bieżący main i sprawdź zmiany wobec tego snapshotu.

**Przeanalizowany main SHA:** `873e3d4db9a5967b20200ad19006f07c15f3c86e`

**Stan odczytany ze źródeł:** Syntetyczny smoke jest dostępny. Zbiory realne, baseline reproduction, wytrenowane artefakty i freeze konfirmacyjny pozostają blokadami.

**Pierwszy pakiet:** Przygotować kompletny manifest pierwszej kohorty TartanAir

## Źródła i istniejące instrukcje

- [AGENTS.md](https://github.com/MatPomGit/arc-s4d-tam/blob/873e3d4db9a5967b20200ad19006f07c15f3c86e/AGENTS.md)
- [PROJECT_STATE.yaml](https://github.com/MatPomGit/arc-s4d-tam/blob/873e3d4db9a5967b20200ad19006f07c15f3c86e/PROJECT_STATE.yaml)
- [README.md](https://github.com/MatPomGit/arc-s4d-tam/blob/873e3d4db9a5967b20200ad19006f07c15f3c86e/README.md)
- [TODO.md](https://github.com/MatPomGit/arc-s4d-tam/blob/873e3d4db9a5967b20200ad19006f07c15f3c86e/TODO.md)
- [configs/readiness/dataset_freeze_plan.yaml](https://github.com/MatPomGit/arc-s4d-tam/blob/873e3d4db9a5967b20200ad19006f07c15f3c86e/configs/readiness/dataset_freeze_plan.yaml)
- [docs/comparison-protocol.md](https://github.com/MatPomGit/arc-s4d-tam/blob/873e3d4db9a5967b20200ad19006f07c15f3c86e/docs/comparison-protocol.md)

## Kolejność zadań

Zadania bez zależności można przygotowywać niezależnie. Właściwe badanie wymaga spełnienia wszystkich bramek jego istniejącego protokołu. AI przygotowuje materiały i analizy; operator wykonuje pomiary urządzeń, a zespół badawczy badania uczestników.

| ID | Zadanie | Wykonawca | Poprzedniki / warunki | Rezultat | Kryterium ukończenia |
| --- | --- | --- | --- | --- | --- |
| S01 | Sprawdzić wersję źródłowego TartanAir, sensory, licencję, kalibrację i niezmienną listę sekwencji | AI | brak | Manifest wejściowy według dataset_freeze_plan | Żadne pole pochodzenia/sensora nie jest zgadywane |
| S02 | Wykonać convert/preflight/freeze pierwszej kompatybilnej kohorty | AI + lokalne obliczenia | S01 | Manifest, checksum i provenance | Test/training/calibration rozdzielone; mapy nie korzystają z finalnego ground truth |
| S03 | Odtworzyć co najmniej jeden kompatybilny baseline z ustalonego źródła/container | AI + lokalne obliczenia | S02 | AlgorithmResult i pełny execution record | Specyfikacja baseline zastąpiona dowodem rzeczywistego wykonania |
| S04 | Wytrenować oraz zamrozić model full i prerejestrowane H1–H7 pod ustalonym budżetem | AI + zatwierdzony lokalny GPU | zamrożone training/calibration | Artefakty full/ablations i manifest | Identyfikatory, seedy i rzeczywiste sumy; brak finalnych testów w tuningu |
| S05 | Zamknąć confirmatory_freeze i wykonać zamrożony benchmark offline | AI + lokalne obliczenia | S02,S03,S04 | Pakiet benchmarku i raport statystyczny | Parowane misje/sekwencje; awarie w mianowniku; dokładny H7 i multiplicity zachowane |
| S06 | Przeprowadzić niezależną reprodukcję i SIL; dopiero potem HIL | operator + AI | S05 | Pakiety reprodukcji/SIL/HIL | Każdy etap ma osobne kryteria i rzeczywiste raporty |
| S07 | Rozważyć lot kontrolowany tylko po niezależnej gotowości operacyjnej i decyzji operatora | operator | S06 + właściwa ocena bezpieczeństwa | Raport lotu albo NO-GO | Brak wnioskowania o certyfikacji z testów offline |
| S08 | Dokończyć P01 z generowanych wyników; skontrolować źródła i PDF | AI + autor | S05 i zakres dowodów właściwy twierdzeniom | Pakiet P01 | Granice offline/SIL/HIL/flight jednoznaczne; brak wymuszonego lotu dla zakresu offline |

## Ścieżki publikacyjne

To istniejące kierunki programu, w tym kandydaci warunkowi. Ich liczba nie jest obietnicą liczby publikacji. Zakres artykułu wynika z rzeczywistych dowodów.

| Manuskrypt | Kroki | Bramka / ograniczenie interpretacji |
| --- | --- | --- |
| P01 | Real cohort freeze → external baseline → trained full/H1–H7 → confirmatory offline → reprodukcja → artykuł | SIL/HIL/lot rozszerzają dowody etapowo |

## Zapis wyniku każdego zadania

1. Zweryfikuj bieżący SHA, AGENTS.md, PROJECT_STATE.yaml i właściwy protokół
2. Wykonaj jeden zakres prac z powyższej tabeli i zapisuj wyniki w jego istniejącej lokalizacji
3. Uruchom właściwe testy lub analizę; zapisz dokładne polecenie, wersję, wynik i ograniczenia
4. Zarejestruj rzeczywisty artefakt i jego sumę; zaktualizuj istniejący TODO, evidence/claim ledger oraz PROJECT_STATE.yaml tylko w zakresie faktycznej zmiany
5. Zamknij zadanie dopiero po spełnieniu kryterium; jeśli jest zablokowane, zapisz brak i przejdź do zadania bez tej zależności

Dodatkowy koszt usług: 0. Ciężkie obliczenia wymagają zweryfikowanej gotowości lokalnego sprzętu. Andromeda nie jest uruchamiana automatycznie. Nie przechowuj danych uczestników, sekretów ani licencjonowanych pełnych tekstów w Git.

## Weryfikacja tego planu

Użyto funkcji analyse_paths z research_repo_audit.py oraz compile_status z research_portfolio_status.py projektu research-autopilot. Odczytano przypięte źródła, zweryfikowano ich Git blob SHA i kompletność drzewa plików. Kontrola struktury nie ocenia jakości naukowej i nie zastępuje kontroli pełnych tekstów, danych ani metod.

Przed dopisaniem do tego dokumentu zwiększ numer wersji zgodnie ze schematem 1.x.x. Nie zmieniaj historycznego SHA tak, aby wyglądał na nowy audyt.
