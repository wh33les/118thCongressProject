# Data gathering and defining stakeholders + KPIs

## Data

The data is all the bills introduced in the 118th Congress as of 1 June 2024.  Collected by [Legiscan API](https://legiscan.com/datasets).

## Problem

Will a bill introduced in the 118th Congress become a law?  Auxillary questions:
1. Will a bill introduced in the 118th Congress become a law, given that it passed in the House?
2. Will a bill introduced in the 118th Congress become a law, given that it passed in the Senate?
3. Will a bill introduced in the 118th Congress become a law, given that it passed in both chambers?

## Stakeholders

- Members of Congress who wish to be productive and pass laws will benefit from knowing what types of bills are likely to become law.
- American citizens can gauge how productive Congress is going to be for the rest of this session.

## KPIs

- Accuracy.  Is my model better than the baseline of just predicting every bill will fail to become a law?
- Precision.  What proportion of positives are true positives?  I.e., does my model predict too many non-law bills become law?
- Recall.  What proportion of positives were correctly detected?  I.e., did my model find all the bills that became law?
