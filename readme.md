# Project Overview

This project uses NLP in a few different ways to automate and assist leading some sort of prayer group / bible study. The idea came from a leadership in a bible study that I lead. The goal is to provide a set of tools to help people track how a person is doing (the ups and the downs), provide methods for reminders, and link it all back to the bible.

This is still an active work in progress!

In specific, this project uses NLP to:
- Link prayer requests to hisorical prayer requests for an automated way of keeping track of prayers.
- Link prayer requests to bible verses for a daily verse.
- Link prayer requests to GotQuestions
- Use sentimental analysis to track how a person is doing over time.
- Use survival analysis to track attendence (I could also just do a time series here -- TBD)

## Running the Project

Use the following command to run the project:

```bash
python -m uvicorn main:httpApp --reload
```


## Ideas

Below are a jot of ideas that I have for this project. I will be using this as a way to keep track of what I want to do and what I have done.

- Can we use the raspberry PI to host our model and an endpoint as a v1?
- The model we want to...
  - Use classification to determine if the prayer falls into an unknown category
  - Detect patterns in the prayers for the current day
  - Detect patterns per user
  - Give a verse(s) of the day based on the prayer requests