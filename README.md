<div align="center"> 
  <img src="https://github.com/mrc2rules/CAIE_PastPaperOpener/assets/58372697/388bb400-5a58-4242-8f37-8410bde750e5" alt="logo" width="160">
</div>
<div align="center">
  <h1>CAIE PastPapersOpener </h1>
  <p>
    A comprehensive tool that lets you access multiple CAIE exam papers quickly and efficiently :)
    <br/>
    <br/>
    <a href="https://github.com/mrc2rules/CAIE_PastPapersOpener/wiki"><strong>Need Help? »</strong></a>
    <br/>
    <br/> 
    <img src="https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Windows" >
    <img src="https://img.shields.io/github/downloads/mrc2rules/CAIE_PastPapersOpener/total?style=for-the-badge&color=F62451" >
    <img src="https://img.shields.io/github/v/release/mrc2rules/CAIE_PastPaperOpener?style=for-the-badge" >
    <a href="https://discord.gg/Sb6QRYDxKG">
      <img src="https://img.shields.io/discord/1193530843151470592?style=for-the-badge&logo=discord&logoColor=7289da&label=Join%20Discord&color=7289da" >
    </a>
  </p>
</div>

## About
CAIE PastPaperOpener lets you access qp, ms, gt or er (even search it on YouTube!) all together in one go! It _maximises your efficiency_ and saves time by eliminating the need to google each paper seperately!

Whether you want to view or download the papers, all you need to do is enter the paper code _once_! Scroll down for usage examples

The program relies on the [PapaCambridge](https://papacambridge.com/) website.

[**Click here to download »»**](https://github.com/mrc2rules/CAIE_PastPapersOpener/releases/latest)

## Features
- 📄 _Preview_ mode, opens both papers in your browser
- 💾 _Download_ mode, downloads both papers in organized folders according to the paper code
- ⚙️ Toggable settings to enable/disable paper types to open (qp/ms/gt/er)
- 🔴 Search paper on YouTube
- 🎚️ Toggle confirmation popup and default mode settings
  
**Extras:-**
- 🖼️ Set a custom wallpaper and change logo

### Planned Features
- [ ] 💾 Ability to download different types of resources other than just papers
- [ ] 📂 Advanced paper generating mechanism, combining multiple years of papers according to the users choice. Print Ready
- [ ] 🔎 Ability to search for questions

The changelogs can be [**found here »»**](https://github.com/mrc2rules/CAIE_PastPapersOpener/blob/main/CHANGELOG.md)

## Linux Port (`caie_downloader.py`)
A pure-Python (standard library only) Linux port. It takes **just the subject code**
and downloads **all question papers (qp), mark schemes (ms) and inserts (in)** for
that subject, organised into `Past Papers/<SUBJECT>/<YEAR>/<Session>/`.

It understands every paper code convention, including leading-zero codes used by
subjects such as Pakistan Studies (`0448` IGCSE / `2059` O Level), where the question
paper is `_qp_01.pdf`/`_qp_02.pdf` but the mark scheme is `_ms_1.pdf`/`_ms_2.pdf`.

```bash
# Interactive - prompts for subject code(s) (defaults to last 10 years)
python3 caie_downloader.py

# Multiple subjects in one run
python3 caie_downloader.py 9702 0450 0500

# Multiple subjects with a shared year range
python3 caie_downloader.py 9702 0450 2019-2024

# All years for one or more subjects
python3 caie_downloader.py 9702 0450 --all

# A specific year (2-digit form avoids ambiguity with 4-digit subject codes)
python3 caie_downloader.py 9702 22          # year 2022
python3 caie_downloader.py 9702 2019-2023   # a range

# Only question papers, or only mark schemes (inserts off)
python3 caie_downloader.py 9702 2020-2023 --qp
python3 caie_downloader.py 9702 2020-2023 --ms

# Only inserts
python3 caie_downloader.py 2059 2022-2024 --in

# Skip inserts (default is to include them)
python3 caie_downloader.py 0448 2024 --no-in

# Tune parallelism (default 16 concurrent requests)
python3 caie_downloader.py 9702 2021-2024 --workers 8
```

> Year selection: a 4-digit number is read as a *subject code*, so to choose a
> single year use the 2-digit form (`22` → 2022), a range (`2019-2023`), or `--all`.

Requires only Python 3.6+ and an internet connection. No third-party packages.
Corrupted / non-PDF files are rejected automatically (PapaCambridge serves an HTML
page instead of a 404 for missing papers).

## Screenshots

<p float="center">
  <img src="https://github.com/mrc2rules/CAIE_PastPaperOpener/assets/58372697/eac7ec1a-4a9a-44b3-a466-89a07b557cdf" width="400" />
  <img src="https://github.com/mrc2rules/CAIE_PastPaperOpener/assets/58372697/20f237e2-ee4b-4c65-a11c-c59ce28b27c3" width="400" /> 
</p>

## Usage
![usage](https://github.com/mrc2rules/CAIE_PastPaperOpener/assets/58372697/ad46f151-ddeb-44fb-8feb-267b25207fd0)



## Installation
> [!IMPORTANT]
> Apps with `.exe` file format like this app, may trigger a warning from Windows and your browser, whether they are harmful or not. This means actual harmless apps get blocked unfortunately (false positives).
> 
> You can safely ignore it.
### Steps
1. **<a href="https://github.com/mrc2rules/IGCSE_PastPapers_Opener/releases/"><strong>Download the App »</strong></a>**
2. Select **Keep**

    ![image](https://github.com/mrc2rules/CAIE_PastPapersOpener/assets/58372697/ddbb1ba6-d5b3-4b7d-a05b-14655fd3bb63)
4. Select **Keep Anyway**
 
   ![image](https://github.com/mrc2rules/CAIE_PastPapersOpener/assets/58372697/2e980d0b-4407-4cb7-acda-f1026e83910e)
5. After you open the file, select **More Info > Run Anyway**

   ![image](https://github.com/mrc2rules/CAIE_PastPapersOpener/assets/58372697/424a2c17-8c0d-46c0-bbcb-c701da5e9eea)
6. That's it!

## License
mrc2rules/CAIE_PastPapersOpener is licensed under the **MIT License**. A copy of the license can be found in the [**LICENSE**](https://github.com/mrc2rules/CAIE_PastPapersOpener/blob/main/LICENSE) file.
