

document.addEventListener('DOMContentLoaded', function() {
    console.log('NN FoodGuide loaded!');
    
    function initScrollAnimations() {
        const fadeElements = document.querySelectorAll('.fade-in');
        
        fadeElements.forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        });
        
        function checkScroll() {
            fadeElements.forEach(element => {
                const elementTop = element.getBoundingClientRect().top;
                const windowHeight = window.innerHeight;
                
                if (elementTop < windowHeight - 100) {
                    element.style.opacity = '1';
                    element.style.transform = 'translateY(0)';
                }
            });
        }
        
        checkScroll();
        window.addEventListener('scroll', checkScroll);
    }
    
    function initPlaceFilters() {
        const searchInput = document.getElementById('searchInput');
        const categoryFilter = document.getElementById('categoryFilter');
        const priceFilter = document.getElementById('priceFilter');
        const sortFilter = document.getElementById('sortFilter');
        const placesContainer = document.getElementById('placesContainer');
        
        if (!placesContainer) return;
        
        function filterAndSortPlaces() {
            const placeCards = Array.from(placesContainer.getElementsByClassName('col-lg-4'));
            const searchText = searchInput ? searchInput.value.toLowerCase() : '';
            const selectedCategory = categoryFilter ? categoryFilter.value : '';
            const selectedPrice = priceFilter ? priceFilter.value : '';
            const sortBy = sortFilter ? sortFilter.value : 'name';
            
            placeCards.forEach(card => {
                let show = true;
                const name = card.querySelector('.card-title')?.textContent.toLowerCase() || '';
                const category = card.querySelector('.badge')?.textContent || '';
                const price = card.querySelector('.price-level')?.textContent || '';
                const rating = parseFloat(card.querySelector('.rating-stars span')?.textContent) || 0;
                
                if (searchText && !name.includes(searchText)) {
                    show = false;
                }
                
                if (selectedCategory && !category.toLowerCase().includes(selectedCategory.toLowerCase())) {
                    show = false;
                }
                
                card.style.display = show ? 'block' : 'none';
                card.style.order = show ? '0' : '999'; // Скрытые в конец
            });
            
            if (sortBy === 'rating') {
                const visibleCards = placeCards.filter(card => card.style.display !== 'none');
                visibleCards.sort((a, b) => {
                    const ratingA = parseFloat(a.querySelector('.rating-stars span')?.textContent) || 0;
                    const ratingB = parseFloat(b.querySelector('.rating-stars span')?.textContent) || 0;
                    return ratingB - ratingA; // По убыванию рейтинга
                });
                
                visibleCards.forEach((card, index) => {
                    placesContainer.appendChild(card);
                });
            }
        }
        
        if (searchInput) searchInput.addEventListener('input', filterAndSortPlaces);
        if (categoryFilter) categoryFilter.addEventListener('change', filterAndSortPlaces);
        if (priceFilter) priceFilter.addEventListener('change', filterAndSortPlaces);
        if (sortFilter) sortFilter.addEventListener('change', filterAndSortPlaces);
    }
    
    function initFavoriteButtons() {
        const favoriteButtons = document.querySelectorAll('.btn-favorite');
        
        favoriteButtons.forEach(button => {
            button.addEventListener('click', function() {
                const icon = this.querySelector('i');
                
                // Переключаем состояние
                if (icon.classList.contains('far')) { // Не в избранном
                    icon.classList.remove('far');
                    icon.classList.add('fas', 'text-danger');
                    this.title = 'Удалить из избранного';
                    
                    // Показываем уведомление
                    showToast('Добавлено в избранное!', 'success');
                } else { // Уже в избранном
                    icon.classList.remove('fas', 'text-danger');
                    icon.classList.add('far');
                    this.title = 'Добавить в избранное';
                    
                    showToast('Удалено из избранного', 'info');
                }
                
                console.log('Favorite toggled for place');
            });
        });
    }
    
    function initReviewForm() {
        const reviewForm = document.querySelector('form[action*="review"]');
        if (!reviewForm) return;
        
        const ratingInputs = reviewForm.querySelectorAll('input[name="rating"]');
        const ratingDisplay = document.getElementById('ratingDisplay');
        
        ratingInputs.forEach(input => {
            input.addEventListener('change', function() {
                const value = this.value;
                if (ratingDisplay) {
                    ratingDisplay.textContent = `${value}/5`;
                }
                
                const stars = reviewForm.querySelectorAll('.rating-star');
                stars.forEach((star, index) => {
                    if (index < value) {
                        star.classList.add('text-warning');
                        star.classList.remove('text-muted');
                    } else {
                        star.classList.remove('text-warning');
                        star.classList.add('text-muted');
                    }
                });
            });
        });
        
        const textarea = reviewForm.querySelector('textarea[name="text"]');
        if (textarea) {
            const counter = document.createElement('small');
            counter.className = 'form-text text-end text-muted';
            counter.id = 'charCounter';
            counter.textContent = `0/500 символов`;
            
            textarea.parentNode.appendChild(counter);
            
            textarea.addEventListener('input', function() {
                const length = this.value.length;
                counter.textContent = `${length}/500 символов`;
                
                if (length > 500) {
                    counter.classList.add('text-danger');
                    counter.classList.remove('text-muted');
                } else if (length > 450) {
                    counter.classList.add('text-warning');
                    counter.classList.remove('text-muted', 'text-danger');
                } else {
                    counter.classList.remove('text-danger', 'text-warning');
                    counter.classList.add('text-muted');
                }
            });
        }
    }
    
    function initImageCarousel() {
        const carousels = document.querySelectorAll('.carousel');
        carousels.forEach(carousel => {
            new bootstrap.Carousel(carousel, {
                interval: 5000,
                wrap: true
            });
        });
    }
    
    function initTooltips() {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    function initModals() {
        // Автоматическое скрытие сообщений через 5 секунд
        const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(alert => {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        });
    }
    
    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                
                if (href !== '#' && href.startsWith('#')) {
                    e.preventDefault();
                    const target = document.querySelector(href);
                    
                    if (target) {
                        window.scrollTo({
                            top: target.offsetTop - 80,
                            behavior: 'smooth'
                        });
                    }
                }
            });
        });
    }
    
    function showToast(message, type = 'info') {
        const toastContainer = document.getElementById('toastContainer');
        if (!toastContainer) {
            const container = document.createElement('div');
            container.id = 'toastContainer';
            container.style.cssText = 'position: fixed; top: 20px; right: 20px; z-index: 9999;';
            document.body.appendChild(container);
        }
        
        const toastId = 'toast-' + Date.now();
        const toastHtml = `
            <div id="${toastId}" class="toast align-items-center text-white bg-${type} border-0" role="alert">
                <div class="d-flex">
                    <div class="toast-body">
                        ${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                </div>
            </div>
        `;
        
        toastContainer.insertAdjacentHTML('beforeend', toastHtml);
        
        const toastEl = document.getElementById(toastId);
        const toast = new bootstrap.Toast(toastEl, { delay: 3000 });
        toast.show();
        
        toastEl.addEventListener('hidden.bs.toast', function() {
            this.remove();
        });
    }
    
    initScrollAnimations();
    initPlaceFilters();
    initFavoriteButtons();
    initReviewForm();
    initImageCarousel();
    initTooltips();
    initModals();
    initSmoothScroll();
    
    // 11. ДОПОЛНИТЕЛЬНЫЕ ОБРАБОТЧИКИ
    
    document.querySelectorAll('.btn-copy-link').forEach(button => {
        button.addEventListener('click', function() {
            const url = window.location.href;
            navigator.clipboard.writeText(url).then(() => {
                showToast('Ссылка скопирована в буфер обмена!', 'success');
            });
        });
    });
    
    document.querySelectorAll('.btn-show-map').forEach(button => {
        button.addEventListener('click', function() {
            showToast('Функция карты скоро будет доступна!', 'info');
        });
    });
    
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            const icon = this.querySelector('i');
            if (document.body.classList.contains('dark-mode')) {
                icon.classList.remove('fa-moon');
                icon.classList.add('fa-sun');
                localStorage.setItem('theme', 'dark');
                showToast('Ночной режим включен', 'info');
            } else {
                icon.classList.remove('fa-sun');
                icon.classList.add('fa-moon');
                localStorage.setItem('theme', 'light');
                showToast('Дневной режим включен', 'info');
            }
        });
        
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') {
            document.body.classList.add('dark-mode');
            const icon = themeToggle.querySelector('i');
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
        }
    }
});

/
function shareOnSocial(platform) {
    const url = encodeURIComponent(window.location.href);
    const title = encodeURIComponent(document.title);
    
    const shareUrls = {
        vk: `https://vk.com/share.php?url=${url}&title=${title}`,
        telegram: `https://t.me/share/url?url=${url}&text=${title}`,
        whatsapp: `https://wa.me/?text=${title}%20${url}`,
        twitter: `https://twitter.com/intent/tweet?url=${url}&text=${title}`
    };
    
    if (shareUrls[platform]) {
        window.open(shareUrls[platform], '_blank', 'width=600,height=400');
    } else {
        alert('Платформа не поддерживается');
    }
}

function openMap(lat, lng, name) {
    const mapsUrls = {
        yandex: `https://yandex.ru/maps/?pt=${lng},${lat}&z=16&l=map`,
        google: `https://www.google.com/maps/search/?api=1&query=${lat},${lng}&query_place_id=${name}`,
        osm: `https://www.openstreetmap.org/?mlat=${lat}&mlon=${lng}#map=16/${lat}/${lng}`
    };
    
    window.open(mapsUrls.yandex, '_blank');
}

function checkBrowserSupport() {
    const supports = {
        clipboard: !!navigator.clipboard,
        geolocation: !!navigator.geolocation,
        touch: 'ontouchstart' in window,
        serviceWorker: 'serviceWorker' in navigator
    };
    
    console.log('Browser support:', supports);
    return supports;
}

// Форматирование даты
function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now - date;
    
    // Если сегодня
    if (diff < 86400000 && date.getDate() === now.getDate()) {
        const hours = date.getHours().toString().padStart(2, '0');
        const minutes = date.getMinutes().toString().padStart(2, '0');
        return `Сегодня в ${hours}:${minutes}`;
    }
    
    // Если вчера
    if (diff < 172800000 && date.getDate() === now.getDate() - 1) {
        const hours = date.getHours().toString().padStart(2, '0');
        const minutes = date.getMinutes().toString().padStart(2, '0');
        return `Вчера в ${hours}:${minutes}`;
    }
    
    // Стандартный формат
    const day = date.getDate().toString().padStart(2, '0');
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const year = date.getFullYear();
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    
    return `${day}.${month}.${year} ${hours}:${minutes}`;
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.date-format').forEach(element => {
        if (element.dataset.date) {
            element.textContent = formatDate(element.dataset.date);
        }
    });
});