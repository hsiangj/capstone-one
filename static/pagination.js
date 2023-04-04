const paginationNumbers = document.getElementById('pagination-numbers');
const paginatedList = document.getElementById('paginated-list');
const listItems = paginatedList.querySelectorAll('li');
const nextButton = document.getElementById('next-button');
const prevButton = document.getElementById('prev-button');

let paginationLimit = 12; // how many items displayed per page
let pageCount = Math.ceil(listItems.length / paginationLimit) //how many pages there will be based on paginationLimit
let currentPage; //store value of currentPage

const appendPageNumber = (index) => {
  const pageNumber = document.createElement('button');
  pageNumber.className = 'pagination-number';
  pageNumber.innerHTML = index;
  pageNumber.setAttribute('page-index', index);

  paginationNumbers.appendChild(pageNumber)
};

const getPaginationNumbers = () => {
  for (let i = 1; i<= pageCount; i++) {
    appendPageNumber(i)
  }
};

const setCurrentPage = (pageNum) => {
  currentPage = pageNum;

  handleActivePageNumber();
  handlePageButtonsStatus();

  const prevRange = (pageNum - 1) * paginationLimit;
  const currRange = (pageNum) * paginationLimit;

  listItems.forEach((item, index) => {
    item.classList.add('hidden');
    if (index >= prevRange && index < currRange ){
      item.classList.remove('hidden');
    }
  })
};

const handleActivePageNumber = () => {
  document.querySelectorAll('.pagination-number').forEach((button) => {
    button.classList.remove('active');
    
    const pageIndex = Number(button.getAttribute('page-index'));
    if (pageIndex == currentPage) {
      button.classList.add('active');
    }
  });
};

const disableButton = (button) => {
  button.classList.add('disabled');
  button.setAttribute('disabled', true);
};
const enableButton = (button) => {
  button.classList.remove('disabled');
  button.removeAttribute('disabled');
};
const handlePageButtonsStatus = () => {
  if (currentPage === 1) {
    disableButton(prevButton);
  } else {
    enableButton(prevButton);
  }
  if (pageCount === currentPage) {
    disableButton(nextButton);
  } else {
    enableButton(nextButton);
  }
};

document.addEventListener('DOMContentLoaded', () => {
  getPaginationNumbers();
  setCurrentPage(1);

  prevButton.addEventListener('click', () => {
    setCurrentPage(currentPage - 1);
  })

  nextButton.addEventListener('click', () => {
    setCurrentPage(currentPage + 1);
  })

  document.querySelectorAll('.pagination-number').forEach((button)=> {
    const pageIndex = Number(button.getAttribute('page-index'));

    if(pageIndex){
      button.addEventListener('click', () => {
        setCurrentPage(pageIndex);
      })
    }
  })
});