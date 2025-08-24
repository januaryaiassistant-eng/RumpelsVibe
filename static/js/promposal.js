const yesBtn = document.getElementById('yesBtn');
const noBtn = document.getElementById('noBtn');
const message = document.querySelector('.message');

yesBtn.addEventListener('click', () => {
    message.textContent = 'YAY! 🥳 Can’t wait for prom with you! 💖';
    yesBtn.style.display = 'none';
    noBtn.style.display = 'none';
});

noBtn.addEventListener('mouseover', () => {
    const x = Math.floor(Math.random() * 200) - 100;
    const y = Math.floor(Math.random() * 200) - 100;
    noBtn.style.transform = `translate(${x}px, ${y}px)`;
});

noBtn.addEventListener('click', () => {
    message.textContent = 'Oh no! 😭 Please reconsider!';
});
