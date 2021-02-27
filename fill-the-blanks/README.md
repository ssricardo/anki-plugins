# Fill the blanks - Improved type:cloze

> *TLDR;*  
> This addons makes Anki handle cards of the kind *type:cloze* properly and adds support for multiple cloze parts on those cards

With the addon applied:  

![Fill the blanks](doc/review-inputs.png)

## Motivation

Typing in the answers are interesting for studying. For many people, writing is more efficient for memorization than just reading.  
On cloze cards, when hiding just the cloze parts, it's possible to study contents within a context.  

The current version of Anki doesn't work well with that combination (On cloze card, it replaces the entire content with a single *input text*).  

This addon solves this issue.  

> Note from dev: At first, I'm using it for source code blocks. Soon, I think about using for cards with language (ex: German) phrases as well

## How it works

* Create a card of type Cloze deletion

![Card editor with cloze](doc/cloze-card.png)

* On the note templates editor, instead of using *cloze:fieldName*, use *type:cloze:[fieldName]* 

> Example with a field named "Texto"

![The card template editor](doc/card-template.png)

* Then, on review time, the cloze parts will be replaced with *input texts*

![Modifying to use the addon](doc/from-cloze-to-input.gif)

> Note: this addon does not create a new note type. You need to either edit or duplicate an existing. Look up "type:cloze" on Anki's manual. 

## Extra feature

### Instant feedback

While the user types in the answer, the corresponding input field changes.  
The background color changes according to the value:  

* incomplete: yellow
* correct: green
* incorrect: red

![Feedback](doc/intant-feedback.gif)

> Note from dev: In my own tests, this is really good. It makes me try harder to get the right answer.


**Configurations:**  

It's possible to enable/disable feedback, ignore case (upper/lower) and ignore accents through configurations.

For details, refer to [Configuration](src/config.md)

### Answer feedback

> From 2.0

Especially for those who disable _instant feedback_, on "Show answer" the add-on also provides a feedback per field.

## Bugs / Suggestions / more...

Please, feel free to make suggestions and open issues about possible bugs found.  

That and the source code are available on: [Github](https://github.com/ssricardo/anki-plugins/tree/master/fill-the-blanks)

## Updates

> Check [RELEASE_NOTES](RELEASE_NOTES.md)

## About

Add-on developed by *ssricardo*.  
Check out more of my add-ons on [Github Anki Plugins](https://github.com/ssricardo/anki-plugins)

### Buy me a coffee

> If you feel like...

https://www.buymeacoffee.com/ricardoss