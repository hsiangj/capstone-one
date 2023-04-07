// Hamburger nav bar for responsiveness
let bar = document.querySelector('.bars');
let navItem = document.querySelector('.nav-items');

bar.addEventListener('click',() => {
  navItem.classList.toggle('active');
})