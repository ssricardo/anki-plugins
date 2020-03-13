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