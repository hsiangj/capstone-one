document.addEventListener('DOMContentLoaded', function(){

  ////// Home.html //////
  // Search bar autocomplete
  let input = document.getElementById('q');
  let suggestions = document.querySelector('#suggestions ul');

  // AJAX call to server API for park names
  let parks = [];
  async function getParkNames(){
    
    let response = await axios.get('/api/parks/names');
    parks = response.data.names;
    
  }
  getParkNames();

  function search(str, arr) {
    const results = [];
    const lowerStr = str.toLowerCase()
    if (str) {
      for (let park of parks) {
        if (park.toLowerCase().includes(lowerStr)) {
          let idx = arr.indexOf(park);
          results.push(arr[idx]);
        }
      }
      return results;
    }
  }

  function searchHandler(e) {
    suggestions.innerHTML = '';
    if (e.target.value !== '') {
      const searchVal = e.target.value; 
      const results = search(searchVal, parks);
      showSuggestions(results);
    }
  }

  function showSuggestions(results) {
    for (let park of results) {
      const newSuggestion = document.createElement('li');
      newSuggestion.innerText = park;
      suggestions.append(newSuggestion);
    }
  }

  function useSuggestion(e) {
    const selectedPark = e.target.innerText;
    input.value = selectedPark;
    suggestions.innerHTML = '';
  }
  
  if (input){
    input.addEventListener('keyup', searchHandler);
  }
  if (suggestions){
    suggestions.addEventListener('click', useSuggestion);
  }

  
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

  ////// Park.html //////
  // Toggle bookmark icon to add/remove park from bookmark section 
  async function toggleParkBookmark(e){
    e.preventDefault()
    const tgt = $(e.target);
    const closestBtn = tgt.closest('button');
    const parkCode = closestBtn.attr('id');
    const parkName = $('#park-actions').prev('h1').text()

    if(closestBtn.text() == 'Bookmark'){
      await axios.post(`/api/bookmark/${parkCode}`, {parkName});
      closestBtn.text('Bookmarked!');
      closestBtn.addClass('bookmarked');
      
    } else {
      await axios.delete(`/api/bookmark/${parkCode}`);
      closestBtn.text('Bookmark');
      closestBtn.removeClass('bookmarked');
    }
    }

  $('#park-actions').on('click', toggleParkBookmark);


  // Toggle 'collect' button to add/remove park from collected section 
  async function toggleParkCollect(e){
    e.preventDefault()
    const tgt = $(e.target);
    const closestBtn = tgt.closest('button');
    const parkCode = closestBtn.attr('id');
    const parkName = $('#park-actions').prev('h1').text()
    
    if(closestBtn.text() == 'Collect'){
      await axios.post(`/api/collect/${parkCode}`, {parkName});
      closestBtn.text('Collected!');
    } else {
      await axios.delete(`/api/collect/${parkCode}`);
      closestBtn.text('Collect');
    }
    }

  $('#park-actions').on('click', toggleParkCollect);


  ////// Bookmarked.html //////
  // Delete park from bookmark section
  async function deleteParkFromBookmarked(e){
    e.preventDefault()
    const tgt = $(e.target);
    const closestTr = tgt.closest('tr');
    const parkCode = closestTr.attr('id');
    await axios.delete(`/api/bookmark/${parkCode}`);
    closestTr.remove();
  }

  $('button#delete-bookmarked-btn').on('click', deleteParkFromBookmarked);


  ////// Collected.html //////
  // Get collected parks' image URLS via AJAX call to server API
  async function getCollectedParkImgAndLoc(){
    let parkObj = {}
    // let locArr = []
    
    const cards = Array.from(document.querySelectorAll('.collection-card'))
    for (let card of cards){
      parkObj[card.id] = ""
    }
    
    for (let key in parkObj){
      response = await axios.get(`/api/park/${key}`)
      parkObj[key] = response.data.data[0].images[0]['url']
      // locArr.push(response.data.data[0].states)
    }

    updateCollectedCardImg(cards, parkObj)
  
  }
  
  getCollectedParkImgAndLoc();


  function updateCollectedCardImg(cards, obj){
    for (let card of cards){
      for (let [k, v] of Object.entries(obj)){
        if (k == card.id){
          card.children[1].children[0].src = v;
        }
      }
    }
  }
  
 

  //listen for double click to remove card
  async function deleteCollectedCard(e){
    e.preventDefault;
    const tgt = $(e.target);
    const closestCard = tgt.closest('.collection-card');
    const parkCode = closestCard.attr('id');
    await axios.delete(`/api/collect/${parkCode}`);
    closestCard.remove()
  }
  $('div.collection').on('click', deleteCollectedCard);

  //////
  // AJAX call to server API to save all parks to DB
  async function getParks(){
    await axios.get('api/parks');
  }
  getParks();

  

})

