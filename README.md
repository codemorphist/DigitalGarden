<img 
    style="display: block; 
           margin-left: auto;
           margin-right: auto;
           width: 100%;"
    src="./resources/cover.png" 
    alt="Cover">
</img>

<p align="center">REAMDE.md lang: </p><a href="." align="center">🇺🇸ENG</a><a href=".">🇺🇦UKR</a>

___

<!-- TOC start (generated with https://github.com/derlin/bitdowntoc) -->

# Навігація

- [🔎 Про проєкт](#about)
- [🚀 Як запустити?](#how-to-run)
   * [Залежності](#dependencies)
   * [Poetry](#poetry)
   * [Windows](#windows)
   * [Linux / MacOs](#linux-macos)
- [🔥 Як використовувати?](#hot-to-usage)
  * [Generate Plant](#generate-plant)
  * [Smash Plants](#smash-plants)
  * [Mass Smash](#mass-smash)
- [🏞️ Галерея](#gallery)
- [📃 Ліцензія](#license)
- [💻 Розробники](#developers)

<!-- TOC end -->

___
<!-- TOC --><a name="about"></a>
# 🔎 Про проєкт

**DigitalGarden** — це поєкт для генерації цифрових рослин за допомогою агентів що малють кола. 
Окрім генерування власних рослин за геномом ви, також, можете схрещувати раніше згенеровані рослини декількома способами,
після чого зберігати їх та ділитися своїми результатами.

___

<!-- toc --><a name="how-to-run"></a>
# 🚀 Як запустити?

<!-- toc --><a name="dependencies"></a>
## Залежності
- 🐍 `python >= 3.11`: мова програмування 
- 🖼️ `Pillow >= 10.3.0`: використовується для малювання рослин
- 🪴 `plant_generator`: використовується для генерації рослин
- 🛠️ `tools`: допоміжні інструменти

Перш за все клонуйте код проєкту та перейдіть в папку з кодом:
```bash
git clone https://github.com/codemorphist/DigitalGarden.git
cd DigitalGarden
```

Дійте далі відповідно до того яку операціну систему та менеджер пакетів ви використовуєте

<!-- TOC --><a name="poetry"></a>
## Poetry

Проєкт використовує менеджер пакетів та залежностей [Poetry](https://python-poetry.org/), 
тому якщо ви хочете швидко запустити код (в незалежності від того, яку операційну систему ви використовуєте) можете втановити **Poetry** і виконати наступні команди:

Встановіть залежності:
```bash
poetry install
```

Запустіть проєкт:
```bash
poetry run python app
```

<!-- toc --><a name="windows"></a>
## Windows

### pip

Створіть нове віртуальне середовище та встановіть залежності:
```bash
$ python -m venv venv
$ .\venv\Scripts\activate
$ pip install -r requirements.txt
```

Запустіть проєкт:
```bash
python app
```

### conda

Якщо ви використувуєту **conda** створіть віртуальне середовище та активуйте його: 
```bash
$ conda env create -f environment.yml
$ conda activate digitalgarden
```

Запустіть проєкт:
```bash
$ python app
```

<!-- TOC --><a name="linux-macos"></a>
## Linux / MacOS

### pip
Створіть нове віртуальне середовище та встановіть залежності:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Запустіть проєкт:
```bash
python app
```

### conda

Якщо ви використувуєту **conda** створіть віртуальне середовище та активуйте його: 

```bash
$ conda env create -f environment.yml
$ conda activate digitalgarden
```

Запустіть проєкт:

```bash
$ python app
```

<!-- toc --><a name="how-to-usage"></a>
# 🔥 Як використовувати?

В цій секції ви можете знайти детальну інформацію як генерувати рослини, схрещувати та зберігати їх в окремі файли.

<!-- toc --><a name="generate-plant"></a>
## Generate Plant

...

<!-- toc --><a name="Smash Plants"></a>
## Smash Plants 

...

<!-- toc --><a name="Mass Smash"></a>
## Mass Smash

...

<!-- TOC --><a name="gallery"></a>
# 🏞️ Галерея

| <img src="./gallery/blues.png" width="512"> | <img src="./gallery/coral_palm.png" width="512"> |
|--|--|
| [blues.txt](./orangery/blues.txt) | [coral_palm.txt](./orangery/coral_palm.txt) |

| <img src="./gallery/exotic.png" width="512"> | <img src="./gallery/fire_palm.png" width="512"> |
|--|--|
| [exotic.txt](./orangery/exotic.txt) | [fire_palm.txt](./orangery/fire_palm.txt) |

| <img src="./gallery/luminosity.png" width="512"> | <img src="./gallery/orange_tree.png" width="512"> |
|--|--|
| [luminosity.txt](./orangery/luminosity.txt) | [orange_tree.txt](./orangery/orange_tree.txt) |

| <img src="./gallery/purple_tree.png" width="512"> | <img src="./gallery/violet.png" width="512"> |
|--|--|
| [purple_tree.txt](./orangery/purple_tree.txt) | [violet.txt](./orangery/violet.txt) |

<!-- toc --><a name="license"></a>
# 📃 Ліцензія 

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Heckert_GNU_white.svg/1024px-Heckert_GNU_white.svg.png" width="100" align="right"></img>
Код проекту поширюється під ліцензією **GNU General Public License v3.0**
<br>
Детальніше ознайомитися з ліцензією можна тут: [LICENCE](./LICENSE)

<!-- TOC --><a name="developers"></a>
# 💻 Розробники

| <img src="https://avatars.githubusercontent.com/u/112182502?v=4" width="100"> | <img src="https://avatars.githubusercontent.com/u/158076825?v=4" width="100"> |
|--|--|
| Alex Katrenko <br> [@codemorphist](https://www.github.com/codemorphist) | Illia Karbyshev <br> [@karbyshevillia](https://www.github.com/karbyshevillia) |

