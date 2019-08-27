# RedditSummerizer


---
### Overview
RedditSummerizer is a tool that makes browsing Reddit a more seamless and less time consuming endeavor. The RedditSummerizer sends out curated 'newsletters' that contain the summerized contents of articles the Reddit user saved to view later.



The RedditSummerizer will monitor a users 'Saved' content and attempt to summerize the text within it. The tool with then send a 'newsletter' to the user which contains the summeries of all the saved content for that day.

This project was designed to help avoid drowning in the vast sea of information that is out there on Reddit. I found myself finding so much content that I wanted to consume but didn't have enough time to read at the moment. With this tool, I am now able to read a short summary of the content I found interesting and go back to read the original article if I found the topic useful or interesting.

### Examples
* Example Usages, screenshots / links to videos / demos
- high level

### Getting Started
* This project will require:
- Python ?.?
- Praw (https://praw.readthedocs.io/en/latest/)
* The program will look for environment variables for the log in credentials. You will need to configure:
- $VARIABLE_ONE
* How it works???

### Retrospective
* **Lessons Learned**
   - First time hitting an external endpoint with Python!
* **Limitations and known issues**
   - This tool isn't very scaleable in terms of the number of users.
   - Relies on the SMMRY API instead of using an in-house summerization API.
   - The SMMRY API only allows 100 free calls per day. This will be an issue if we need to scale.
   - Rreddit has a premium feature that allows users to create categories for their `Saved` content. Unfortunately, the official Reddit API does not let you query content from those categories NOR do they provide the category information in the normal 'SavedContent' endpoint (even though there's a JSON field for it in their documentation...)
* **Future Possibilities**
   - Make it possible for the user to configure when & how often they want the 'summerization digest'.
   - Configure the tool to run as a single web service that clients can then utilize instead of the clients needing to run the service on their own machines.
   - Expand outside of saved Reddit posts. Make a Chrome Extension that provides the same functionality.
   - I'm sure there is a better way to store user credentials...

### Developer Info
* MIT license
* Uses the SMMRY API to summerize text (https://smmry.com/api)

