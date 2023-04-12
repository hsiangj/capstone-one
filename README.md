# Park Collector

This repository is completed as part of capstone one of Springboard Software Engineering Career Track.

### Application Description
"Park Collector" is a web app for users to explore, bookmark, and track visited national parks using data from the National Park Service API. Visited parks are "collected" and displayed as card collection with counts to encourage users to explore more.

View the application [here](https://park-collector.herokuapp.com/ "Park Collector") on Heroku.

### Technologly Stack
* HTML5
* CSS3
* Bootstrap 4
* JavaScript
* jQuery
* Python
* Flask
* SQLAlchemy

### Preview
Home page before signup/login  
<img src="/screenshots/main.png" alt="Park Collector main" width="auto" height="250px">

Search by park name or topics  
<img src="/screenshots/search.png" alt="Park Collector search" width="auto" height="250px">

User's bookmarked section  
<img src="/screenshots/bookmarked.png" alt="Park Collector bookmarked" width="auto" height="250px">

User's collection  
<img src="/screenshots/collection.png" alt="Park Collector collection" width="auto" height="250px">

### Standard User Flow
*Signup/Login*
1. New user creates an account / Returning user logs in.
2. User begins search for national parks either by park name or by topic.
    1. Selection by park name will lead directly to park information page.
    2. Selection by topic will lead to paginated pages displaying relevant parks. Clicking on 'learn more' leads to park information page.
3. Once on park information page, user can bookmark the park for later and/or collect the park for a visited place. The page also includes introductory description along with a link to the National Park Service website for additional information. 

*Bookmarked and Collection*
- Parks that have been bookmarked and/or collected can be managed directly from its respective section.

4. User logs out.

### Credits
* [National Park Service API](https://www.nps.gov/subjects/developer/api-documentation.htm)
* [Mountain clipart](https://creazilla.com/nodes/77137-mountain-clipart)





