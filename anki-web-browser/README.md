# Anki Web Browser

The **Anki Web Browser** is a simple Internet Browser within Anki (as the name suggests).  
It aims to make it easy when you are studying or editing a card and want to look something up on the internet.  
You can also use it to open up your system desktop instead of the embedded browser (*from version 1.1*)

For instance, you are studying a foreign language and suddenly there is a word which you haven't properly understood. In such case it's common to shift to the web browser and search for the term there. 
This addon makes this task smoother.  

Therefore, this addon provides 2 functionalities:  

* Search the selected text in a website
  * Or use one of the _no selection_ options (*from version 3.0*)
* Import text and images directly from a website to current card

## Configuration

In order to search something on a website, the user is given a list of registered websites to choose from. This list is called **providers**.  
In the Configurations view, the user may specify the providers that will be available.  

The *web browser* may close itself when the user shifts cards, that is, when a new card is shown as opposed to the one which was used for a query.  
This feature may be *enabled* or *disabled* using the configuration **Keep card opened**.  

The config **Always on top** is intuitive. It means that if enabled, when the *web browser* is shown, it remains above everything. This might be useful when editiing several notes.  

The config **Use System Browser** disabled the embedded web browser. With this the addons invokes the system web browser instead. Both the provider and the queried term will be used likewise.  

There are 2 **shortcuts** available, which are customizable:

* Show Web Browser menu: It's the same as right click, but it shows the Anki Web Browser only menu 
* Search again, repeating last provider: Skip the *Select a provider* part (See more below)

It's possible to automatically remove/strip some words from the text to be searched. These words are specified on **Filter following words** (separated by spaces).  

> From version 3.0

![Config View](doc/anki-webb-config.png)

> [ TODO ] Image outdate 

## Using

The functions of this addons are accessed through the context menu (either *right click* on mouse or *right menu key* on the keyboard) or using shortcuts.  

### Search selected text

While studying or editing a given card:  

* Select a word or sentence
* Right click (or use the shortcut)
* *Search on Web*
* Select the desired provider

Then a new window with the *web browser* will be opened, if it isn't opened yet.  

![Web Browser on reviewer](doc/anki-webb-review.gif)
  

### Search without selection (No selection option)

> From version 3.0+

If no text is selected for the search, the user may selected other option (following):

* Type in the term to look up
* Use the content of one of the fields on current card
* Do nothing (just expect a text selected)

With the 2nd and 3rd options, it's possible to *memorize* the selected option. 
This way, the user won't be prompted about *no selection option* anymore, **in the current Anki session**.  


#### Query a new word with same provider

> From version 1.2+

If the user have already used this addon in the current Anki session, this action opens up the web browser without asking to choose a provider.  
It's going to use the same as the last query. 

Conversely, if it's the first query in the current session, the menu will be shown.

### Get data directly from the web browser

When using this addon while adding or editing a note, it's possible to get text and images from the opened website to the card.  

![Editing from Web Browser](doc/anki-webb-edit.gif)

After looking something up with the previous steps (above), on the *web browser*:  

* Select some text and then *right click* OR just *right click* over an image
* *Assign to field*
* A list with the fields from the source card is shown
* Choose one of them

This way, the text or image will be appended to the selected field.  
Even the image! (It's downloaded and imported into the collection automatically) (Check the restriction below)  

This feature makes it really simple and fast to get some information from the Internet and build or improve your Anki's collection.  

> This feature works only using the embedded web browser. If you use the system browser, it's not possible to get data automatically

#### Repeat assignement

> From version 3.0

To speed up this process, here it's also possible to repeat the last action; that is, assign the content to the same field used last time (**on current Anki session**). 

To do this, just *hold Ctrl* when right-clicking on some selected text or image.

## Limitation

The image downloading supports only URLs finished with image suffix (like png, jpg)...
This addon uses Anki engine to perform that action, and Anki imposes that restriction.  

## Bugs / Suggestions / more...

Please, feel free to make suggestions and open issues for possible bugs found. 

Some pages aren't opening in this browser and for other ones sometimes the user needs to reload it. This is a known bug but there is no fix planned yet.