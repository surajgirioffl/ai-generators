# AI Generator (A Browser Automation Project To Generate AI Contents)

* **An advanced browser automation project with CLI & GUI, featuring dynamic functionalities for ImageToVideo, TextToVideo, TextToText and ImageToText AI generations across numerous websites**
* [Github Repository](https://github.com/surajgirioffl/ai-generators)

* How to read this documentation:
  * This is a markdown file.
  * You can read this file using any markdown reader.
  * Install below markdown readers extension to your browser to read this documentation effectively.
    * [For Chrome](https://chromewebstore.google.com/detail/markdown-reader/medapdbncneneejhbgcjceippjlfkmkg)
    * [For Edge](https://chromewebstore.google.com/detail/markdown-viewer/ckkdlimhmcjmikdlpkmbgfkaikojcbjk)

## 1. Installation Docs (One Time Process)

### Installing Python (windows)

* Download and install Python from [here](https://www.python.org/downloads/).
* Check if Python is installed properly or not.
  * Open command prompt and type `python --version` and press enter.
  * If you get the output of python version then python is installed properly.

### Installing dependencies

* Open command prompt (any terminal) in the project directory (Not required in case of providing absolute path of the `requirements.txt`)
* Write command `pip install -r requirements.txt` and press enter.
* Wait until all dependencies have been installed.

### Installing Webdriver

* Visit to [GoogleChromeLabs](https://googlechromelabs.github.io/chrome-for-testing/).
* Navigate to `Stable` channel then click and copy the `URL` of Binary named as `chromedriver` for your platform (say win64).
* Open new table of your browser and paste the copied link. It will download a zip file.
* Extract the zip file using any extractor (like WinRAR).
* Now, Open the extracted directory and copy it's path. Make sure that it contains an EXE named as `chromedriver.exe`.
* Now, We have to add that directory to the PATH.
  * To add the directory path to system environment PATH. Follow following steps:
  * Open `Control Panel`
  * Search for `path`
  * Click on `Edit the system environment variables`
  * Click on `Environments Variables`
  * Double click on `path` variable of the section named as `User variable for <your system username>`
  * Click on `New`
  * Now paste the directory path in the appeared textbox.
  * Now, click on OK > OK > OK
  * ALL DONE ✅👍

## 2. Starting the application

* In windows,
  * Click on the `app.bat` file to open the application.
  * On each click, a new instance of application will started. So, you can use multiple instances simultaneously.
* In linux,
  * Open the `app.sh` file in the terminal.
  * Write `./app.sh` and press enter.
  * On each execution of the file, a new instance of application will started. So, you can use multiple instances simultaneously.

* Other method (work in both windows and linux)
  * Open terminal(CMD/Powershell/Bash etc) in the project directory.
  * Write command `python app.py` and press enter.
  * Each time you execute this command, a new instance of the application will created. So, you can use multiple instances simultaneously.

## 3. Customization

* Use `options` sheet of `preferences.xlsx` excel file to provide value for options of all sites.
* Prompts and Images can be stored in different sheets of the `preferences.xlsx` excel file (See docs of the Excel file).
* Each site has it's own configuration file (txt/json). You can customize the configuration file as per your need.
  * Don't pass any value to deprecated options because they are deprecated and script will ignore values associated for those options.

## 4. `preferences.xlsx` Docs

### `options` sheet

* Don't change any content of the column named as `login_required`.
* `automation_status` column specify if the automation script for the respective site is working or not (Not implemented yet).
* No need to pass any value to `prompt` or `image` option of any site. It will automatically taken from the selected prompt sheet or image sheet.
* If any options are compulsory for any site then must pass values for those options otherwise it will lead to failure of the automation process for the respective site.

* WordHero
  * Don't pass any value to the `prompt` or `headline` option.
  * Excel sheet for prompts for wordhero don't have any separate rule for sheet name. Use same sheet name as of other sites. Sheet name must be starts with `prompt` and must contain a column named as `prompt`.
    * In this case, the `prompt` column must contain headlines instead of complete prompt. Prompt will auto generated by the script.

### Other sheets

* You can add as many sheets as you want. But sheet names starts with `prompt` and `image` will only read by the script (except `options` sheet.)

* Prompts sheets
  * The sheet name must be starts with the keyword `prompt` (case sensitive) else it will not added as option in the prompt sheet selection dropdown.
  * The sheet must have a column named as `prompt` that contains all prompts.
* Images Sheets (For the category image_to_video)
  * The sheet name must be starts with the keyword `image` (case sensitive) else it will not added as option in the image sheet selection dropdown.
  * The sheet must have a column named as `image` that contains all images path.

## 5. Others

* See log of the application: `<project_dir>/appdata/script.log`
