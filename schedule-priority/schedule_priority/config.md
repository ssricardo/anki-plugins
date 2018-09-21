# Schedule Priority Configuration

The available configuration allows the user to adjust the interval customization.  
For each Priority it is possible to set the multiplier percent to be applied.  

Consider that the value for the **Normal** interval is **100** (which is not modifiable), that is, cards with *Normal priority* will use 100% of the original interval given by Anki.  

## Constraints

Priorities **above** normal (High, Highest) are supposed to be repeated in a shorter time. Therefore, their interval must be **less than 100**.  
On the other hand, priorities **below** normal (Low, Lowest) wil be repeated in longer times. Thus, in such cases the interval must be **more than 100**.  