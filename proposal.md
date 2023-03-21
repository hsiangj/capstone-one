# Project Proposal 

### What is Park Collector? 
Park Collector is a web app that aims to help users explore the 400+ parks available in the National Park Service (NPS). It allows visitors to track parks of interest as well as visited parks. The visited parks are shown as 'collected' cards along with tally of parks visited. 

### Target Demographic
From hikers to nature photographers to campers, anyone who would like to explore what the NPS has to offer with the option to track their experience.  

### Data Usage
- User data: store user information for authentication and authorization
- Saved/favorite parks: user's saved/favorite parks
- Completed parks: user's completed parks

### Project Approach
##### Database schema 
<img src='/images/proposal_db_schema.png' width='500'>

Potential schema for further study implementation:
<br>
<img src='/images/proposal_db_schema_fs.png' width='500'>

##### Anticipated challenges
- API availability and stability
- Extraction of desired API data that fits the goal of the project
  - Determining which type, if any, of the API data to store in database
- Deployment to Heroku 
- Balance of time to complete the project

##### Data security
User password will be hashed and stored. Authentication will be in place to validate user. 

##### Functionality/features 
- User-friendly, responsive interface
- A search option/ browse park by topic, eg. music, American revolution, women’s history 
- Pagination
- Option to manage saved data/parks
- Card-like collection
- Visited park count

##### User flow
1.	Homepage: user signup or login
  * Signup: requires username and password to pass requirement validation
  *	Login: username and password authentication
2.	Successful signup or login redirects user to search page 
  - Navigation bar will change to show username, links to logout, saved parks and visited parks
3.	Search by typing in park name in search bar or filter by state or click on a park topic
4.	Browse parks populated. Click to see more, add to favorite, or add to collection. 
5.	Favorite parks page: show list of favorite parks with options to see more
6.	Visited parks page: show ‘collected’ parks as cards and total parks tally
7.	Logout

##### Stretch Goals/ Further Study
* Park recommendation
* Collected park cards arranged by card deck
* Park sharing by email 
