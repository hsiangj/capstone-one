////// Home.html 
// AJAX call to server API to list all park topics
async function listTopics(){
  const response = await axios.get('/api/topics');
  
  const topics = response.data.data;
  for (let topic of topics){
    let eachTopic = makeTopicHTML(topic)
    $('#topics-list').append(eachTopic) 
  }
}

listTopics()

// HTML for topic display
function makeTopicHTML(topic){
  return `
  <a href="/parks/topic/${topic.id}" class="badge badge-pill badge-light" style="font-size:1.3em">${topic.name}</a>
  `
}


////// Show.html 
async function listParksByTopic(topic){
  const response = await axios.get(`/api/topic/${topic.id}`);
  console.log(response)
  const topics = response.data.data;
  // for (let topic of topics){
  //   let eachTopic = makeTopicHTML(topic)
  //   $('#parks-list').append(eachTopic) 
  // }
}