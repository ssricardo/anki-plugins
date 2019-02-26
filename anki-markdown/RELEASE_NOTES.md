# Notes

**1.0**

* Initial version
  * Interprets text surrounded by <amd> as Markdown and converts it to HTML

**1.1** | 24/10/2018

* Support for trim and replace-spaces configuration, both globally and locally
* Config renamed: showMdButton -> show-md-button  
* There is no longer the limitation for code block, as trimmimg may is customizable 

**2.0** | 26/02/2019

* Large refactor
* Added conversion from HTML to MD
* Added options to execute the conversions immediately (in-place) (Either HTML to MD or MD to HTML)
* Handles notes edition, preventing Anki from formatting the inputs as HTML
* Added options to invoke the conversions as a batch operation (on Browser view)
* Added visual demarcation to parts handled by this add on (left border)
* Dropped the configurations *trim* and *replace-spaces* as they aren't necessary anymore