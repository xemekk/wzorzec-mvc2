var modal = document.querySelector('.modal');
var openModal = document.querySelector('#open');
var closeModal = document.querySelector('#close');

openModal.addEventListener('click', () => {
    modal.showModal();
})

closeModal.addEventListener('click', () => {
    modal.close();
})