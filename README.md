<img 
    style="display: block; 
           margin-left: auto;
           margin-right: auto;
           width: 100%;"
    src="./resources/cover.png" 
    alt="Cover">
</img>

<div align="center" width="128">
  <a href="./README.md" align="left" style="padding: 5px;"> 🇺🇸ENG </a><a href="./README.ua.md" align="right" style="padding: 5px;"> 🇺🇦UKR </a>
</div>

___

<!-- TOC start (generated with https://github.com/derlin/bitdowntoc) -->

# Navigation

- [🔎 About the Project](#about)
- [🚀 How to run it?](#how-to-run)
   * [Dependencies](#dependencies)
   * [Poetry](#poetry)
   * [Windows](#windows)
   * [Linux / MacOs](#linux-macos)
- [🔥 How to use it?](#hot-to-usage)
  * [Generate Plant](#generate-plant)
  * [Smash Plants](#smash-plants)
  * [Mass Smash](#mass-smash)
- [🏞️ Gallery](#gallery)
- [📃 License](#license)
- [💻 Developers](#developers)

<!-- TOC end -->

___
<!-- TOC --><a name="about"></a>
# 🔎 About the Project

**DigitalGarden** is a digital plant generator that employs circle-drawing agents. Apart from stand-alone plant generation, you 
can also combine (i.e. "smash") previously generated plants in a variety of ways, and save/share your findings thereafter.
___

<!-- toc --><a name="how-to-run"></a>
# 🚀 How to run it?

<!-- toc --><a name="dependencies"></a>
## Dependencies
- 🐍 `python >= 3.11`: the programming language
- 🖼️ `Pillow >= 10.3.0`: used for drawing plants
- 🪴 `plant_generator`: used for plant generation
- 🛠️ `tools`: ancillary instruments

First of all, clone the project repository and switch to the corresponding directory:
```bash
$ git clone https://github.com/codemorphist/DigitalGarden.git --depth 1
$ cd DigitalGarden
```

Your further actions will depend upon the operating system and the dependency manager you are using:

<!-- TOC --><a name="poetry"></a>
## Poetry

The project employs the [Poetry](https://python-poetry.org/) dependency manager; thus, if you wish to run the code quickly, regardless of your operating system, you can download **Poetry** and execute the following:

Download the dependencies:
```bash
$ poetry install
```

Run the app:
```bash
$ poetry run python app
```

<!-- toc --><a name="windows"></a>
## Windows

### pip

Create a new virtual environment and download the dependencies:
```bash
$ python -m venv venv
$ .\venv\Scripts\activate
$ pip install -r requirements.txt
```

Run the app:
```bash
$ python app
```

### conda

If you are using **conda**, create a new virtual environment and activate it:

```bash
$ conda env create -f environment.yml
$ conda activate digitalgarden
```

Run the app:

```bash
$ python app
```

<!-- TOC --><a name="linux-macos"></a>
## Linux / MacOS

### pip

If you are using **pip**, create a new virtual environment and download the dependencies:

```bash
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Run the app:
```bash
$ python app
```

### conda

If you are using **conda**, create a new virtual environment and activate it:

```bash
$ conda env create -f environment.yml
$ conda activate digitalgarden
```

Run the app:

```bash
$ python app
```

<!-- TOC --><a name="how-to-usage"></a>
# 🔥 How to use it?

In this Section you will find detailed information regarding generating plants, combining them, as well as managing them through a file system:

<!-- TOC --><a name="generate-plant"></a>
## Generate Plant

<details>

<summary>Generate Plant</summary>

![Generate Plant](./resources/generate_plant_screenshoot.png)

1. The canvas; here the generated plant will display
2. The progress bar; it shows the current stage of plant generation
3. The genome input table
4. The import button; it allows for importing genomes from files
5. The random generation button; it fills out the genome table with random values
6. The export button; it allows for exporting the genome into a file
7. The generation button; it launches an animated generation process
8. The fast generation button; it launches an animationless generation process
9. The save button; it allows for saving images of the generated plants

</details>

<!-- TOC --><a name="Smash Plants"></a>
## Smash Plants

<details>

<summary>Smash Plants</summary>

![Smash Plants](./resources/smash_plants_screenshot.png)

1. The canvas with a progress bar that will display the first parent
2. The canvas with a progress bar that will display the child plant
3. The canvas with a progress bar that will display the second parent
4. This import button allows for importing a parent genome
5. This button launches an animated generation process for a parent
6. This button launches an animationless generation process for a parent
7. This button opens a window where the genome combination method can be set
8. This button launches the generation of the child plant
9. This button allows for exporting the genome of the child plant
10. This button allows for saving the image of the child plant

</details>

<!-- TOC --><a name="Mass Smash"></a>
## Mass Smash

<details>

<summary>Mass Smash</summary>

![Mass Smash](./resources/mass_smash_screenshot.png)

1. The canvas with a progress bar that will display the child plant
2. The list of parent genomes (order-sensitive)
3. This button moves the selected parent genomes one position upward in the list
4. This button moves the selected parent genomes one position downward in the list
5. This button allows for importing other parent genomes and adding them to the list
6. This buttons allows for deleting selected parent genomes from the list
7. This button opens a window where the genome combination method can be set
8. This button launches an animated generation of the child plant
9. This button launches an animationless generation of the child plant
10. This button allows for exporting the genome of the child plant
11. This button allows for saving the image of the child plant

</details>


<!-- TOC --><a name="gallery"></a>
# 🏞️ Gallery

The plant gallery is available via [DigitalGarden Gallery](https://codemorph.xyz/DigitalGarden/)

<!-- toc --><a name="license"></a>
# 📃 License

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Heckert_GNU_white.svg/1024px-Heckert_GNU_white.svg.png" width="100" align="right"></img>
The project source code is distributed under the **GNU General Public License v3.0**
<br>
Further information about the license is to be found via [LICENCE](./LICENSE)

<!-- TOC --><a name="developers"></a>
# 💻 Developers

| <img src="https://avatars.githubusercontent.com/u/112182502?v=4" width="100"> | <img src="https://avatars.githubusercontent.com/u/158076825?v=4" width="100"> |
|--|--|
| Alex Katrenko <br> [@codemorphist](https://www.github.com/codemorphist) | Illia Karbyshev <br> [@karbyshevillia](https://www.github.com/karbyshevillia) |

