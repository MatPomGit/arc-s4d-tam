# GitHub Actions — polityka repozytorium publicznego

Reguły obowiązują agentów AI oraz autorów pull requestów.

- Dozwolone są **lekkie testy automatyczne** o niewielkim koszcie (lint, szybkie testy jednostkowe, kontrola składni), pod warunkiem ograniczenia do `push` na `main` i wąskich filtrów `paths`.
- Ciężkie buildy (Android, pełny LaTeX, GPU, trening, symulacje, benchmarki, publikacje) uruchamiaj ręcznie przez `workflow_dispatch`, z zachowaniem zatwierdzeń i limitów.
- Nie uruchamiaj automatycznie testów na gałęziach roboczych ani przy `pull_request`; nie dodawaj `pull_request_target` ani `merge_group`. Każdy job kontroluje `github.ref == 'refs/heads/main'`.
- Agenci przeprowadzają lokalne testy PR, ograniczają koszt wykonywania workflow i nie uruchamiają Actions ze starszych gałęzi. CI po merge nie zastępuje wcześniejszej kontroli jakości.
- Zadbaj o ochronę gałęzi, uprawnienia, sekrety i monitorowanie zużycia. Wyjątki uzasadnij w repozytorium.
