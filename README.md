[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/srcole/burritos/master)

# burritos
Analysis of burritos across San Diego, outlined in the notebooks below.

## Burrito dataset overview.ipynb
Analysis of the burrito dataset including
* descriptive statistics
* taco shop ranking
* modeling of overall satisfaction as a function of individual burrito dimensions
* principal component analysis

## Rating reliability.ipynb
Analysis of the consistency of ratings for a given taco shop's burrito across
visits. Here, we also get a sense of the inter-reviewer reliability.

## Chipotle orders.ipynb
Some analysis of how items are ordered together at Chipotle. Specifically,
it shows:
* Orders containing a vegetarian item are less like to also contain soda,
compared to no veggie items
* Orders for a burrito bowl are more often accompanied by chips and bottled water
compared to orders that only contain burritos.

## Future potential analysis
* How do California burritos differ from the rest of the burritos?
    * Do they tend to give higher overall satisfaction than other burritos?
    * Control for other factors (like the person and taco shop)
    * Which taco shops have the best California burritos?
* What dimensions are reviewers most critical (small mean)? Least critical? Most sensitive? Least sensitive (small variance)?
* How does the contribution of each dimension to overall rating vary over reviewers and taco shops?
* How does each burrito dimension contribute to overall satisfaction (both linearly and nonlinearly)

## Related information
* [Raw data](https://docs.google.com/spreadsheets/d/18HkrklYz1bKpDLeL-kaMrGjAhUM6LeJMIACwEljCgaw/edit#gid=1703829449)
* [Contribute your burrito data](https://docs.google.com/forms/d/e/1FAIpQLSdWAkbSKzHydtzJ-AKHp_rXKHeG80cZuUBjyEeMAUZXJsiFKQ/viewform)
* [Blog post](https://srcole.github.io/100burritos/)
