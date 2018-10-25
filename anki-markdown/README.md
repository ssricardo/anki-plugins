# Anki Markdown Formatter

> TLDR; Surround your content with `<amd>` to have it processed as Markdown. There are some customization/configurations below...

[If you already know Markdown, skip the next paragraph...]  

Markdown is an easy way of formatting texts, based on a predefined syntax.  
It makes it simple and fast to write texts because the user doesn't need to worry about annoying details, like when you user tool like Word. 
It's like on WhatsApp, you write \_text_ and after sending it, its shown as _text_.  

Check more information and the syntax out on the following websites:  

* [markdownguide](https://www.markdownguide.org/)
    * [Syntax](https://www.markdownguide.org/basic-syntax/)
* [commonmark.org](https://commonmark.org/help/)

And many other websites...

**This addon** makes it possible to interpret cards (or parts of them) as Markdown.  
While editing or adding cards, write it in plain text. No formatting is done in this view.  
Then, when reviewing the card, it is interpreted as markdown and converted to formatted text (HTML actually).


## Usage

Markdown-formatter won't process everything. Therefore, you need to identify the area(s) that it should work on.  
This is done using a markup tag: `<amd>`.  

On the HTML code, put the tags `<amd>` and `</amd>` around the area to be processed.  

**Example:**  

        <amd>{{Example}}</amd>

This might be done either in the Card Type (Note) level or in parts of a given card. 

### Format the entire card type

This is done through Card Type Configuration. Thus, it's applied to all cards of that type.  

![Card type config](doc/md-tags-cards.png)

### Format part of a card

In the editor, you can either use the Markdown button in the toolbar or use the shortcut.  
The default **shorcut** is *Ctrl+Shift+M* (may be changed in Configurations).  

Just **select the block** to be processed, then use one of the options.

![Modifying from editor](doc/md-button-editor.png)

### Pre-processing

Some handling needs to be done in the content before processing it as Markdown.  This happens duo to the way Anki stores the content (as HTML).

1. Trim lines
    * Trimming means removing spaces before the first word and after the last one on each line.
1. Replace escaped spaces
    * Anki uses HTML format, which escapes spaces using `&nbsp;`. So, even though the user sees an empty space, there are some extra characters there. 

#### Effects and customization

These procedures are needed because Markdown has a specific syntax. Some markup needs to be at the beginning of the line. Likewise, some of them requires one or more empty spaces. 
For instance: headers, list-itens, blockquotes...

Conversely, trimmig the lines (and perhaps replacing spaces) leads to problems with other formats, like *code blocks*.  

Therefore, these procedures may be set (customized) in two levels.  Both globally, through the addon's configurations, and locally, into the `amd` tag. Check the example below!  

**Local customization** for a code block:  

        <amd trim="false" replace-spaces="true">
        {{CodeField}}
        </amd>

## Configuration

The following customization are available:  

* Shortcut
    * As it says... shortcut for adding tags around selected text
* Show markdown button
    * Indicates whether the Markdown button shoud be shown or not
* Trim
    * Indicates whether each line should be trimmed
* Replace-spaces
    * Indicates whether it should replace escaped HTML spaces (\&nbsp;)



## Bugs / Suggestions / more...

Please, feel free to make suggestions and open issues about possible bugs found.  

That and the source code are available on: [Github](https://github.com/ssricardo/anki-plugins/tree/master/anki-markdown)

## Updates

24/10/2018: **version 1.1**:

* Support for *trim* and *replace-spaces* configuration, both globally and locally
* Config renamed: showMdButton -> show-md-button  
* There is no longer the limitation for code block, as trimmimg may is customizable  

## About

Addon developed by *ssricardo*.  
Check out more of my addons on [https://github.com/ssricardo/anki-plugins]()