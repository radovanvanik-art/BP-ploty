# Zdroj webu LIBES s.r.o.

Web sa generuje skriptami — HTML stránky v koreni repozitára needitujte ručne.

| Súbor | Čo obsahuje |
|---|---|
| `page.html` | hlavná stránka (dizajn, štýly, plánovač plota, objednávka) |
| `build.py` | texty a šablóna 6 podstránok služieb + ochrana osobných údajov |
| `tools.py` | interaktívne nástroje podstránok (stena, výkop, váha materiálu, kontajner) |
| `prod.py` | zloží ostrú verziu: SEO hlavičky, údaje firmy (IČO, DIČ), cookies/GA, formulár FormSubmit, realizácie, kontakt, 404, sitemap |

Úprava: zmeniť `page.html` / `build.py` / `tools.py`, potom `python3 build.py && python3 prod.py`.
Údaje firmy (IČO, DIČ, sídlo, e‑mail pre objednávky, doména) sú na začiatku `prod.py`.
Priečinok začína podčiarkovníkom, takže ho GitHub Pages nezverejní.
