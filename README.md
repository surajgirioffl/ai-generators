# AI Generator

## Preferences.xlsx Docs

### `options` sheet

* Don't change any content of the column`login_required`.
* `automation_status` column specify if the automation script for the respective site is working or not.
* No need to pass any value to `prompt` or `image` option of any site. It will automatically taken from the selected prompt sheet or image sheet.

* WordHero
  * Don't pass any value to `prompt` or `headline` option.
  * Excel sheet for prompts for wordhero has not any separate schema. Use same schema as of other sites. Sheet name must be with `prompt` and must contain a column named as `prompt`.
    * In this case, the `prompt` column must contain headlines instead of complete prompt. Prompt will auto generated by the script.

### Other sheets

* You can add as many sheets as you want. But sheet names starts with `prompt` and `image` will only read by the script (except `options` sheet.)

* Prompts sheets
  * The sheet name must be starts with the keyword `prompt` (case sensitive) else it will not added as option in the prompt sheet selection dropdown.
  * The sheet must have a column named as `prompt` that contains all prompts.
* Images Sheets (For the category image_to_video)
  * The sheet name must be starts with the keyword `image` (case sensitive) else it will not added as option in the image sheet selection dropdown.
  * The sheet must have a column named as `image` that contains all images path.
