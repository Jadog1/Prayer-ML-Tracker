# Project Overview

This project uses NLP in a few different ways to automate and assist leading some sort of prayer group / bible study. The idea came from a leadership in a bible study that I lead. The goal is to provide a set of tools to help people track how a person is doing (the ups and the downs), automate following up on prayer requests, provide methods for reminders, and link it all back to the bible.

As I continue to scope out the prayer request tracking part of this application, I also intend to build a feature suite for building bible studies. This will include additional modeling to include type ahead features and relating scripture back to whatever is being written.

This is still an active work in progress!

To see a demo, visit https://youtu.be/VLOUYgGJo9I

## Features

### Current Features
- Link prayer requests to hisorical prayer requests for an automated way of keeping track of prayers. This uses semantic similarity.
- Link prayer requests to bible verses, which also uses semantic similarity.
- Use sentimental analysis to track how a person is doing over time
- Use sentence classification to determine if a given request is a "prayer request" or "praise report"
- Use sentence classification to provide additional metadata like emotions
- Visualize common themes in prayer request sessions for an easy way to pray for common themes

### Features in Progress
- Build a rule-engine (as v1) to bring up prayer requests to follow up on
- Using the above features, start storing data on which prayer requests are being followed up on. This will allow for a later ranking model, once we have training data.

### Future Features
- Link prayer requests to GotQuestions, for in-depth answers that may apply to the prayer request
- Named Entity Recognition to track people, also track time (EG, when would a prayer request make most sense to be followed up on? If I typed "in two weeks from now...", i would want to follow up in two weeks)
- Build a ranking model to determine which prayer requests are most important to follow up on
- Add reminders for prayer requests
- Use survival analysis to track attendence (I could also just do a time series here -- TBD)
- Detect patterns in the prayer requests
- Build a feature suite for building bible studies

## Running the Project

Use the following command to run the project:

```bash
python -m uvicorn main:httpApp --reload
```

Optionally, you can also setup your environment for debugging using this launch.json file:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python Debugger: FastAPI",
            "type": "debugpy",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "main:httpApp",
                "--reload"
            ],
            "pythonArgs": [
                "-Xfrozen_modules=off"
            ],
            "jinja": true
        }
    ]
}
```

TODO: I would like to get this into a platform like Heroku once we standardize more of these features.