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

  // Toggle bookmark icon to add/remove park from bookmark section (used in park.html)
  async function toggleParkBookmark(e){
    e.preventDefault()
    const tgt = $(e.target);
    console.log(tgt)
    const closestSpan = tgt.closest('span');
  
    const closestI = closestSpan.children('i');
    console.log(closestI)
    const parkCode = closestSpan.attr('id');
    const parkName = $('#park-actions').prev('h1').text()

    if(closestI.hasClass('far')){
      await axios.post(`/api/bookmark/${parkCode}`, {parkName});
      closestI.toggleClass('fas far');
    } else {
      await axios.delete(`/api/bookmark/${parkCode}`);
      closestI.toggleClass('far fas');
    }
    }

  $('#park-actions').on('click', toggleParkBookmark);


  // Toggle 'collect' button to add/remove park from collected section (used in park.html)
  async function toggleParkCollect(e){
    e.preventDefault()
    const tgt = $(e.target);
    const closestBtn = tgt.closest('button');
    const parkCode = closestBtn.attr('id');
    const parkName = $('#park-actions').prev('h1').text()
    console.log(closestBtn.text())
    console.log(closestBtn.text() == 'Collect')
    if(closestBtn.text() == 'Collect'){
      await axios.post(`/api/collect/${parkCode}`, {parkName});
      closestBtn.text('Collected!');
    } else {
      await axios.delete(`/api/collect/${parkCode}`);
      closestBtn.text('Collect');
    }
    }

  $('#park-actions').on('click', toggleParkCollect);



  // Delete park from bookmark section
  async function deleteParkFromBookmarked(e){
    e.preventDefault()
    const tgt = $(e.target);
    console.log(tgt)
    const closestTr = tgt.closest('tr');
    const parkCode = closestTr.attr('id')
    await axios.delete(`/api/bookmark/${parkCode}`)
    closestTr.remove()
  }
  $('#delete-bookmarked-btn').on('click', deleteParkFromBookmarked)

})

