# CV Reviewer
This repo contains the CV Reviewer project, which anonymizes uploaded CVs and allows other users to check them out and connect with each other.

### Dataset
https://github.com/JAIJANYANI/Automated-Resume-Screening-System#dataset

### How to Set Up
CV Reviewer uses python3.9 with Flask and pure HTML/CSS.
Clone the progect and be sure to install project's dependencies using:
```
pip3 install -r requirements.txt
```
This project is built using Blueprint (Flask modules class), so inside the repo folder you'll have `cvreviewer` package with blueprints (home, users, posts). To run the project, simply use:
```
python3 main.py
```
and navigate to `127.0.0.1:5000`. (or download a Microsoft Visual Studio Code to run it just in a few clicks - this is not a promo 🙂)
There's also a Heroku-hosted web app at:
```
https://cvreviewer.herokuapp.com/
```
It takes some time to start the system - so consider waiting while the page is loading. Be sure to ask me for testing credentials :)

### How to Use
The system works best with "not so complex" CVs (it also ignores photos and graphics). The system uses PyPDF2 to extract CV text without custom encodings, while pdfminer.six helps extract text from more complex CVs.
The system should work with **any** type of CV (in .pdf, .doc/.docx format, 4 MBs maximum).
