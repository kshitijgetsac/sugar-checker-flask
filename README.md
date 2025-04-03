# Flask OCR App with Tesseract on Heroku

This project is a Flask-based web application that uses [pytesseract](https://pypi.org/project/pytesseract/) to perform Optical Character Recognition (OCR) on uploaded images. The app is deployed on Heroku and uses the Apt buildpack to install Tesseract and its language data.

## Table of Contents

- [Project Overview](#project-overview)
- [Dependencies](#dependencies)
- [Aptfile and System Packages](#aptfile-and-system-packages)
- [Environment Variables](#environment-variables)
- [Deployment on Heroku](#deployment-on-heroku)
- [Troubleshooting Tesseract Errors](#troubleshooting-tesseract-errors)
- [Using the `find` Command](#using-the-find-command)
- [License](#license)

## Project Overview

This application provides a simple API endpoint to check images for sugar content using OCR. It is built with Flask and uses Tesseract (installed as a system package) to extract text from images.

## Dependencies

### Python Packages

Listed in the `requirements.txt` file:
- Flask
- pytesseract
- Pillow
- pillow-heif
- Flask-Cors

These packages are installed via pip when Heroku deploys your app.

### System Packages

Since Tesseract is not a Python package, it must be installed at the system level. We use the [heroku-community/apt](https://elements.heroku.com/buildpacks/heroku/heroku-buildpack-apt) buildpack along with an `Aptfile` to install:
- `tesseract-ocr`
- `tesseract-ocr-eng`

## Aptfile and System Packages

The **Aptfile** is used by the Heroku Apt buildpack to install system dependencies on the dyno. Create an `Aptfile` (with no extension) in the root of your project (next to `requirements.txt`) with the following content:

```plain
tesseract-ocr
tesseract-ocr-eng

you could face some issues while sending an api request to backend if you follow the above given steps to the letter than there might be an issue where the flask app will not be able to find the tesseract.eng file to resolve that just find the file name in heroku bash (to go to heroku bash just run heroku run bash on your terminal) then use the find command to find the tesseract-ocr directory and after you've found the path exit the bash and set the path using "heroku config:set TESSDATA_PREFIX=.apt/usr/share/tesseract-ocr/5/tessdata/ --app=sugar-checker"
