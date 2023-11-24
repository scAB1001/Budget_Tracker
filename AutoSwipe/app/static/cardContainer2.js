// DOM
const swiper = document.querySelector('#swiper');
const like = document.querySelector('#like');
const dislike = document.querySelector('#dislike');

// variables
let cardCount = 0;

// functions
function appendNewCard(carData) {
  const card = new Card({
    imageUrl: carData.image_url,
    car_name: carData.car_name,
    details: carData.details,
    
    onDismiss: appendNewCard,
    onLike: () => {
      like.style.animationPlayState = 'running';
      like.classList.toggle('trigger');
    },
    onDislike: () => {
      dislike.style.animationPlayState = 'running';
      dislike.classList.toggle('trigger');
    }

  });

  swiper.append(card.element);
  cardCount++;

  const cards = swiper.querySelectorAll('.card:not(.dismissing)');
  cards.forEach((card, index) => {
    card.style.setProperty('--i', index);
  });
}

// Load the initial cards
cars.forEach((carData) => {
  appendNewCard(carData);
});