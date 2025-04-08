document.addEventListener('DOMContentLoaded', () => {
    const menuOpen = document.querySelector('.menu-open');
    const menuClose = document.querySelector('.menu-close');
    const menuList = document.querySelector('.menu-list');

    menuOpen.addEventListener('click', () => {
        menuList.style.display = 'flex';
        setTimeout(() => {
            menuList.style.left = '0';
        }, 100);
    });
    

    menuClose.addEventListener('click', () => {
        menuList.style.left = '100%';
        setTimeout(() => {
            menuList.style.display = 'none';
        }, 400);
    });
});
