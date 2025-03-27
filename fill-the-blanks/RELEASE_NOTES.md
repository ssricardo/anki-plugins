# Notes

**1.0** | 25/04/2019

* Initial release
  * Fixes Anki handling for type:cloze
  * Adds support for multiple cloze in those kind of cards
  * Adds Instant feedback (while typing in)


**1.1** | 29/04/2019

* Improvement on handler for special characters and for working with other add-ons (with change the original content)

**1.2** | 12/05/2019

* Makes *instant feedback* optional (added configuration 'feedback-enabled', default: true)
* Tries to set focus to the first input field

**1.3** | 01/08/2019

* Makes *case sensitivity* optional (added configuration 'feedback-ignore-case', default: false)

**1.4** | 13/08/2019

* Solve issue #27 (DEFAULT_ANKI_CLOZE is not defined)

**1.5** | 28/01/2020

* Solve:  
  * Issue #31 - Support cloze with hints (just making them hidden)
  * Issue #42 - More then 9 type:cloze on a card

**1.6** | 30/01/2020

* Solve issue #45 - Avoid printing sound tags 

**1.7** | 13/03/2020

* Issue #31 - Support hints as placeholder (collaboration from Lai Yu-Hsuan / raincole)
* Issue #48 - Add configuration to ignore accents on Feedback 

**2.0** | 27/02/2021

* Include support to feedback on "Show answer"
* Issue #82 - Problem with too many fields 

**2.1** | 27/02/2021

* Fix: Type answer: unknown field Word

**2.2** | 28/02/2021

* Change default colors on Answer
* Issue #84

**2.3** | 06/03/2021

* Make _feedback on Answer_ available, even when _instant feedback_ is disabled

**2.4** | 06/05/2021

* Make _feedback on Answer_ consider configuration "ignore case" (thanks @matt2112)
* Issue #92

**2.5** | 28/07/2021

* Support asian languages (new trial - still experimental)
* Support customizing the size of the input-field
* Issues #59, #64, #93

**2.6** | 05/08/2021

* Fix formatting for multiple fields (thanks @matt2112)

**2.7** | 10/01/2023 

* Replace integration with Anki for compatibility with other add-ons (thanks @Abdo)
* Possibly already make integration with other add-ons work (issues #109, #96, #115)
* Fix feedback not showing in recent Anki (issues #109, #122, #124)
* Update anki reference to note_type (issue #117)
* Add warning in Template editor (issue #120)
* Fix issue when there are many cloze or text is very long (issues #100, #116)
* Change a bit input clean up to avoid user error (issue #111)

*2.8* | 14/01/2023

* Re-work input cleaning up (thanks Andre/@lightmotive)
  * Issue #126
* Also possibly for issues #125 and #129

*3.0* | 03/05/2023

* Add new integration (still experimental)
* Merge support for zero-width space (thanks Andre/@lightmotive)
* issue #39

*25.3-1* | 07/03/2025

* Remove the old integration in favor or the new (now default)
* Add feature: Suggest next character (issue #70)
* Support CSS styles for distinct field size (related to issue #151)
* Strip HTML in the value in the input field (issue #157)

* ~Merge support for cloze across multiple fields~ (issue #156)
  * Cancelled/Reverted

*25.3-2* | 08/03/2025

* Fix shortcut for "show next character" on MacOS

*25.3-3* | 27/03/2025

* Fix ignore-case feedback (issue #164 - thanks @ryndovaira)
* Fix cleaning context up
  * To Avoid running the addon in cards that it's not used (related to issue #163)
* Add a margin between a wrong answer and the expected one (besides adding the typed value as a on-mouse-over hint)