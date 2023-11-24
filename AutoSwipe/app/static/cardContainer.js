// DOM
const swiper = document.querySelector('#swiper');
const like = document.querySelector('#like');
const dislike = document.querySelector('#dislike');

// constants
const urls = [
  './static/cars/testarossa1.jpg',
  './static/cars/countachlp400Lamborghini1.jpg',
  './static/cars/astonMartinLagonda1.jpg',
  './static/cars/308GTRainbow1.jpg',
  './static/cars/testarossa1.jpg' 
];

// variables
let cardCount = 0;

// functions
function appendNewCard() {
  const carName = "Car"; 
  const details = "Lease Price: £12,000pm   \tBody: Coupe\nHorsepower: 390bhp\t\tMake: Ferrari";

  const card = new Card({
    // This will cycle through your array of local images
    imageUrl: urls[cardCount % urls.length],
    
    onDismiss: appendNewCard,
    onLike: () => {
      like.style.animationPlayState = 'running';
      like.classList.toggle('trigger');
    },
    onDislike: () => {
      dislike.style.animationPlayState = 'running';
      dislike.classList.toggle('trigger');
    },

    carName: carName,
    details: details
  });

  swiper.append(card.element);
  cardCount++;

  const cards = swiper.querySelectorAll('.card:not(.dismissing)');
  cards.forEach((card, index) => {
    card.style.setProperty('--i', index);
  });
}

// first 5 cards (urls.length)
for (let i = 0; i < 5; i++) {
  appendNewCard();
}
