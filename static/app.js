document.addEventListener('DOMContentLoaded', function(){

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

////// Park actions: bookmark (used in park.html)
async function addParkBookmark(e){
  e.preventDefault()
  const tgt = $(e.target);
  console.log(tgt)
  const closestBtn = tgt.closest('button');
  console.log(closestBtn)
  const parkCode = closestBtn.attr('id');
  
  if(tgt.hasClass('far')){
    await axios.post(`/api/bookmark/${parkCode}`)
    tgt.closest('i').toggleClass('fas far');
  } 
}

$('#park-actions').on('click', addParkBookmark);



////// Park.html 
 


})

