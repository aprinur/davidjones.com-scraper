# David Jones Scraper

Tired of copy and paste product information from davidjones.com to google spreadsheet or excel manually? Well, I have solution for that
<br>

## What program is this?

This is a program that automatically collects information from the David Jones website. The information that collected by this program includes name, id, price, brand, product url and image url.
<br>

## How's the program work

This program works by using curl_cffi's requests to fetch the HTML. Next, it uses a regular expression to filter the JSON data within the HTML, followed by parsing the data using the .get() method, just like a dictionary data type. The result is stored in a Google spreadsheet as well as exported as an Excel and CSV file.
<br>

## Feature

This program allows you to

- Create new worksheet
- Display worksheet value
- Export worksheet
- Delete worksheet
  <br>

## Requirement

- Python 3.8+
- Google Sheets API
- Spreadsheet
- Code editor, IDE or Terminal
  <br>

## How to use

<br>

### Preparation

1. Python 3.8+
   Since this program is written in Python, you need Python to run it. Some dependencies don't support versions below 3.8, so the minimum required version is 3.8, but I recommend using a newer version. You can download the latest version from the [original page](https://www.python.org/downloads/).
   <br>
2. Google Sheet API
   If you don't have it, open this [documentation](https://docs.gspread.org/en/latest/oauth2.html) and follow section 'For Bots: Using Service Account section' to create one. After obtain the api key as json file, put it in the working directory and the program will handle the rest.
   <br>
3. Spreadsheet
   After obtaining the API key, create a Spreadsheet file in your Google Drive and share it with the email found in the `client_email` key of the JSON API.
   <br>
4. Code Editor, IDE or Terminal
   To run this program you need one of those three tool, since most device have terminal installed in it, you can start right away.
   <br>

### Execution

1. Creating Virtual Environment (RECOMMENDED) and Installing Dependencies
   
   To isolate project and its dependencies so your environment will be clean I suggest to create virtual environment first. To create and activate the environment you can follow this steps
   <br>
   
   1. Open your command promt
   2. Navigate to your working directory using
      
      ```
      cd path\to\your\project
      ```
   3. Create virtual environment
      
      ```
      python -m venv venv_name
      ```
      
      Replace venv_name with the name you desired, usually it named with .venv
   4. Activate virtual environment
      
      ```
      your_venv_name\Scripts\activate
      ```
      
      to deactivate type ``deactivate`` and press enter
   5. Install dependencies with
      
      ```
      pip install -r requirements.txt
      ```
      
      <br>
2. Excecute main.py
   
   ```
   python main.py
   ```
   
   To run the program and enter the spreadsheet name followed with Google sheet API name you've created earlier. The program will create .env file and folder credentials automatically to store your Google sheet API file to use in the future.
   
   <br>
3. Options
   
   After fill up those form you'll be faced with 4 options:
   
   <br>
   
   * Scrape Website
     
     The program scrapes data based on the base URL you specify, saves everything to a worksheet in your spreadsheet, and then exports to Excel and .csv. For example, if you want to scrape subcategory 'Jeans' from category 'Men' the base URL will look like this:
     
     ```
     https://www.davidjones.com/men/clothing/jeans
     ```
     You can do this to any category on the website. Just make sure to copy every character before the question mark (`?`) from the browser’s URL bar.
     <br>
   * View Worksheet
     
     By entering worksheet name, the program will display values of the available worksheet.
     <br>
   * Export Worksheet
     
     You can re-export worksheet from the spreadsheet using this option. For ease of identification, file name of   the exported file will be the same with your worksheet name.
     <br>
   * Delete Worksheet
     
     This option allows you to remove worksheet from your spreadsheet. I suggest to use this option wisely.

