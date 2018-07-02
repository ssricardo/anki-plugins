# Schedule Priority

The goal of this addon is to let you define different intervals for a group of cards in a deck.

Suppose you have a deck and you to increase the interval when you mark a revision as good (for example).  
Currently you can do so using Anki through Deck Options. Now, let's say you want to customize the interval of only some cards. 
Through that "Deck Options" this is not possible, because it applies the options to the entire deck. 

## Setting a different time than those defined by Anki

Having this feature could interesting because in many times you want to use a customized time. 
Even if you remembered a given card as "good", sometimes you would like to review it again, before the given time.  

It's possible to do it somehow with a few addons. For instance:   

* Define any custom time you want, with a shortcut that asks you what interval you want; 
* Lots of extra buttons with customized times, for each one

These options do work. They need you to manually choose the interval that you desire in each revision.  
As you have so many options (especially with those buttons), sometimes you are not sure about which one to use in that time.  

### Schedule Priority comes up

This addon creates customized interval based on the card (note) record. So when you are studying it, the time is assigned automatically. No need to think about this detail during the review. 

## How to use it

In the edit view, while either creating or editing the card, use the context menu (with right click) and select of the given option.

> Edit card -> Right click -> Card Priorization -> Click the choosen option

[gif]

## How it works

Basically, when you select to assign "High" or "Low" priority, this addon uses the card's tags to save this information.
The following tags are related to this addon:

* priority:low
* priority:high

When a "normal" priority is selected, both os those tags are removed from the card. Therefore, the standard priority is "normal" (of course, right?!).

Throughout the review, when a given card is loaded, this addons checks whether there is any of those tags or not. Then modify card's next times, based on which of those tags is present (or none of them: do nothing).

## How to customize it

To customize this add-on, open up:

> Tools -> Add-ons -> schedule-priority -> Edit...

In the current version, it is possible to modify:

* **Multiplier** value for High and Low priority

Multiplier value is expressed as percentage.  
Consider that a *normal priority* card uses the same intervals as assigned by Anki. This means, 100% of the value calculated by Anki.   

High priority means that it must be repeated in shorter time. Therefore, it should be less than 100% (compared to the time gotten from Anki).  
Converselly, Low priority should not be repeat as much as other (meaning longer intervals). Thus, its intervals must be above 100%.

> Default values: 
>   low_priority_multiplier = 140
>   high_priority_multiplier = 70

*Reinforcing:* 

* *low_priority_multiplier* is required to be more then 100
* *high_priority_multiplier* is required to be less then 100

## Future steps

There are a few ideas planned for next versions:

* Add a shortcut for priority definition (add tags)
* Create a visual window for configuration (instead of needing to do it in the script file)
* Maybe, add the option to modify priority during review (as opposed to only in the Editor)

...

> 1. This is still in a very first version. If you find any bug or have other ideas, please send me it. I'll be happy to work on it.

> 2. As English is not my native language and right now I don't have time to check details, please help me to fix possible mistakes in the text