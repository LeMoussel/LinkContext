# LinkContext

Catégorisation des liens par segmentation d’une page HTML.

Ce programme Python, développé au dessus de Block-o-Matic (BoM), permet de décomposer une page web en segments, visuellement et sémantiquement cohérents, appelés blocs. Les liens sont ensuite extraits pour chaque bloc identifié.

## Pré-requis

* [Python](https://www.python.org/) version 3.7. Les versions plus anciennes de Python ne devraient PAS fonctionner. Les versions plus récentes de Python devraient être OK.

* [Microsoft Playwright for Python](https://playwright.dev/python/). Playwright nécessite Python 3.7 ou plus. Les binaires de navigateur pour Chromium, Firefox et WebKit fonctionnent sur les 3 plateformes (Windows, macOS, Linux). Voir [Installation de Playwright for Python](https://playwright.dev/python/docs/intro#installation).

* [Matplotlib](https://matplotlib.org/stable/index.html) : Visualisation avec Python. Matplotlib est une bibliothèque complète permettant de créer des visualisations statiques, animées et interactives en Python.

* Librairie [JS BoM](https://github.com/openpreserve/pagelyzer/blob/master/SettingsFiles/js/bomlib.js).

## Execution

### Windows 10

```shell
# Windows
py main.py --url "http://example.com/"

# Linux
python3 main.py --url "http://example.com/"
```

## Références

* [Block-o-Matic](https://bom.ciens.ucv.ve/get-it/) : BOM - Segmenteur de page web automatique.
  * Andrés Sanoja Vargas. [Web page segmentation, evaluation and applications](https://tel.archives-ouvertes.fr/tel-01128002/). Web. Université Pierre et Marie Curie - Paris VI, 2015. English. NNT: 2015PA066004. tel-01128002.

## Todo

Toutes suggestions qui semble être une bonne idée. S'il vous plaît, essayez-le, soumettez des PRs pour étendre ou corriger des choses, et signalez toute bizarrerie ou bogue que vous rencontrez :smile:

