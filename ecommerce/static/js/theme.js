/**
 * Gestion du thème clair/sombre pour le site e-commerce
 * Ce script permet de basculer entre les modes clair et sombre
 * et sauvegarde la préférence de l'utilisateur dans localStorage
 */

document.addEventListener('DOMContentLoaded', function() {
    // Éléments DOM
    const themeToggleBtn = document.getElementById('theme-toggle');
    const html = document.documentElement;
    
    // Vérification des préférences système
    const prefersDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    // Récupération du thème sauvegardé dans localStorage ou utilisation des préférences système
    const savedTheme = localStorage.getItem('theme');
    const currentTheme = savedTheme || (prefersDarkMode ? 'dark' : 'light');
    
    // Application du thème initial
    if (currentTheme === 'dark') {
        html.classList.add('dark');
        updateThemeToggleIcon(true);
    } else {
        html.classList.remove('dark');
        updateThemeToggleIcon(false);
    }
    
    // Gestionnaire d'événement pour le bouton de bascule
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', function() {
            const isDarkMode = html.classList.contains('dark');
            
            if (isDarkMode) {
                html.classList.remove('dark');
                localStorage.setItem('theme', 'light');
                updateThemeToggleIcon(false);
            } else {
                html.classList.add('dark');
                localStorage.setItem('theme', 'dark');
                updateThemeToggleIcon(true);
            }
        });
    }
    
    /**
     * Met à jour l'icône du bouton de bascule en fonction du thème actuel
     * @param {boolean} isDarkMode - Indique si le mode sombre est actif
     */
    function updateThemeToggleIcon(isDarkMode) {
        if (!themeToggleBtn) return;
        
        // Sélection des icônes à l'intérieur du bouton
        const sunIcon = themeToggleBtn.querySelector('.sun-icon');
        const moonIcon = themeToggleBtn.querySelector('.moon-icon');
        
        if (sunIcon && moonIcon) {
            if (isDarkMode) {
                moonIcon.classList.add('hidden');
                sunIcon.classList.remove('hidden');
            } else {
                sunIcon.classList.add('hidden');
                moonIcon.classList.remove('hidden');
            }
        }
    }
    
    // Gestion du changement des préférences système
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (!localStorage.getItem('theme')) {
            if (e.matches) {
                html.classList.add('dark');
                updateThemeToggleIcon(true);
            } else {
                html.classList.remove('dark');
                updateThemeToggleIcon(false);
            }
        }
    });
});

/**
 * Initialisation des animations sur la page
 * Cette fonction applique des animations aux éléments sélectionnés
 */
function initAnimations() {
    // Animation de défilement
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    if (animatedElements.length > 0) {
        // Observe les éléments et déclenche les animations au défilement
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-fade-in');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });
        
        animatedElements.forEach(element => {
            observer.observe(element);
        });
    }
}

// Initialisation des animations au chargement de la page
document.addEventListener('DOMContentLoaded', initAnimations);

/**
 * Animation du menu mobile
 * Gère l'ouverture et la fermeture du menu hamburger sur mobile
 */
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuBtn = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
            
            // Animation du menu
            if (!mobileMenu.classList.contains('hidden')) {
                mobileMenu.classList.add('animate-slide-in');
            } else {
                mobileMenu.classList.remove('animate-slide-in');
            }
        });
    }
    
    // Fermer le menu si on clique en dehors
    document.addEventListener('click', function(event) {
        if (mobileMenu && 
            !mobileMenu.classList.contains('hidden') && 
            !mobileMenu.contains(event.target) && 
            !mobileMenuBtn.contains(event.target)) {
            mobileMenu.classList.add('hidden');
        }
    });
});

/**
 * Gestion des dropdowns du menu de navigation
 * Active les menus déroulants pour la navigation
 */
document.addEventListener('DOMContentLoaded', function() {
    const dropdownButtons = document.querySelectorAll('.dropdown-button');
    
    dropdownButtons.forEach(button => {
        const dropdown = button.nextElementSibling;
        
        // Ouvrir/fermer au clic
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            // Fermer tous les autres dropdowns
            dropdownButtons.forEach(otherButton => {
                if (otherButton !== button) {
                    otherButton.nextElementSibling.classList.add('hidden');
                    otherButton.setAttribute('aria-expanded', 'false');
                }
            });
            
            // Basculer ce dropdown
            dropdown.classList.toggle('hidden');
            
            const isExpanded = dropdown.classList.contains('hidden') ? 'false' : 'true';
            button.setAttribute('aria-expanded', isExpanded);
            
            if (!dropdown.classList.contains('hidden')) {
                dropdown.classList.add('animate-fade-in');
            }
        });
    });
    
    // Fermer les dropdowns lorsqu'on clique en dehors
    document.addEventListener('click', function(e) {
        dropdownButtons.forEach(button => {
            const dropdown = button.nextElementSibling;
            
            if (dropdown && !dropdown.classList.contains('hidden') && 
                !dropdown.contains(e.target) && 
                !button.contains(e.target)) {
                dropdown.classList.add('hidden');
                button.setAttribute('aria-expanded', 'false');
            }
        });
    });
});

/**
 * Gestion des animations de la page
 * Cette fonction initialise toutes les animations du site
 */
function initPageAnimations() {
    // Observer pour les animations au défilement
    const animationObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Ajoute les classes d'animation avec délai
                const element = entry.target;
                const delay = element.dataset.delay || '0';
                const animation = element.dataset.animation || 'fade';
                
                setTimeout(() => {
                    element.classList.add(`animate-${animation}`);
                    element.style.opacity = '1';
                }, parseInt(delay));
                
                // Désactive l'observation après l'animation
                if (!element.dataset.repeat) {
                    animationObserver.unobserve(element);
                }
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '50px'
    });

    // Sélectionne tous les éléments avec data-animation
    document.querySelectorAll('[data-animation]').forEach(element => {
        element.style.opacity = '0';
        animationObserver.observe(element);
    });

    // Animation du hero
    const heroElements = {
        title: document.querySelector('.hero h1'),
        subtitle: document.querySelector('.hero p'),
        cta: document.querySelector('.hero .btn-primary'),
        stats: document.querySelectorAll('.hero .stats-item')
    };

    // Anime les éléments du hero
    if (heroElements.title) {
        heroElements.title.classList.add('animate-slide-up', 'delay-100');
    }
    if (heroElements.subtitle) {
        heroElements.subtitle.classList.add('animate-slide-up', 'delay-200');
    }
    if (heroElements.cta) {
        heroElements.cta.classList.add('animate-slide-up', 'delay-300');
    }
    heroElements.stats.forEach((stat, index) => {
        stat.classList.add('animate-fade', `delay-${(index + 4) * 100}`);
    });

    // Animation des cartes de produits
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.dataset.animation = 'slide-up';
        card.dataset.delay = `${index * 100}`;
        animationObserver.observe(card);
    });

    // Animation des images
    const images = document.querySelectorAll('img[data-animate]');
    images.forEach(img => {
        img.addEventListener('load', () => {
            img.classList.add('animate-fade');
        });
    });

    // Animation du menu de navigation
    const navItems = document.querySelectorAll('.nav-link');
    navItems.forEach((item, index) => {
        item.classList.add('animate-fade', `delay-${index * 100}`);
    });

    // Animation des boutons
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('mouseenter', () => {
            btn.classList.add('animate-pulse');
        });
        btn.addEventListener('mouseleave', () => {
            btn.classList.remove('animate-pulse');
        });
    });
}

// Initialisation des animations au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    initPageAnimations();
});

// Réinitialisation des animations lors du changement de route (si SPA)
window.addEventListener('popstate', () => {
    setTimeout(initPageAnimations, 100);
});

/**
 * Animations avancées pour la page d'accueil
 */
const homeAnimations = {
    /**
     * Initialise les effets de parallaxe
     */
    initParallax() {
        const heroSection = document.querySelector('.hero');
        const parallaxElements = document.querySelectorAll('[data-parallax]');
        
        if (heroSection) {
            window.addEventListener('scroll', () => {
                const scrolled = window.pageYOffset;
                const rate = scrolled * 0.5;
                
                // Effet de parallaxe sur l'image de fond
                const heroImage = heroSection.querySelector('img');
                if (heroImage) {
                    heroImage.style.transform = `translate3d(0, ${rate * 0.5}px, 0) scale(${1 + scrolled * 0.0005})`;
                }
                
                // Effet sur les éléments décoratifs
                parallaxElements.forEach(element => {
                    const speed = element.dataset.parallaxSpeed || 0.2;
                    element.style.transform = `translate3d(0, ${rate * speed}px, 0)`;
                });
            });
        }
    },

    /**
     * Anime les éléments flottants
     */
    initFloatingElements() {
        const floatingElements = document.querySelectorAll('.animate-float, .animate-float-delayed, .animate-float-slow');
        
        floatingElements.forEach((element, index) => {
            const delay = index * 200;
            const duration = element.classList.contains('animate-float-slow') ? 4000 : 3000;
            
            element.style.animation = `float ${duration}ms ease-in-out infinite`;
            element.style.animationDelay = `${delay}ms`;
        });
    },

    /**
     * Anime les bordures décoratives
     */
    initBorderAnimations() {
        const borders = document.querySelectorAll('.animate-border-flow');
        
        borders.forEach((border, index) => {
            const delay = index * 150;
            border.style.animation = `borderFlow 2s ease-in-out infinite`;
            border.style.animationDelay = `${delay}ms`;
        });
    },

    /**
     * Effet de suivi de la souris
     */
    initMouseFollowEffect() {
        const hero = document.querySelector('.hero');
        if (!hero) return;

        const decorativeElements = hero.querySelectorAll('.blur-2xl, .blur-xl, .blur-lg');
        
        hero.addEventListener('mousemove', (e) => {
            const { left, top, width, height } = hero.getBoundingClientRect();
            const x = (e.clientX - left) / width;
            const y = (e.clientY - top) / height;

            decorativeElements.forEach((element, index) => {
                const speed = 1 - (index * 0.2);
                const offsetX = (x - 0.5) * 50 * speed;
                const offsetY = (y - 0.5) * 50 * speed;
                
                element.style.transform = `translate(${offsetX}px, ${offsetY}px)`;
                element.style.transition = 'transform 0.3s ease-out';
            });
        });
    },

    /**
     * Animation des statistiques
     */
    initStatsAnimation() {
        const stats = document.querySelectorAll('.stats-item');
        
        stats.forEach(stat => {
            const valueElement = stat.querySelector('.text-primary-400');
            if (!valueElement) return;

            const finalValue = parseInt(valueElement.textContent);
            let currentValue = 0;
            const duration = 2000; // 2 secondes
            const steps = 60;
            const increment = finalValue / steps;
            const stepDuration = duration / steps;

            const updateValue = () => {
                currentValue = Math.min(currentValue + increment, finalValue);
                valueElement.textContent = Math.round(currentValue);

                if (currentValue < finalValue) {
                    setTimeout(updateValue, stepDuration);
                }
            };

            // Démarrer l'animation quand l'élément est visible
            const observer = new IntersectionObserver((entries) => {
                if (entries[0].isIntersecting) {
                    updateValue();
                    observer.disconnect();
                }
            });

            observer.observe(stat);
        });
    },

    /**
     * Initialise toutes les animations de la page d'accueil
     */
    init() {
        this.initParallax();
        this.initFloatingElements();
        this.initBorderAnimations();
        this.initMouseFollowEffect();
        this.initStatsAnimation();
    }
};

// Initialisation des animations de la page d'accueil
document.addEventListener('DOMContentLoaded', () => {
    homeAnimations.init();
}); 