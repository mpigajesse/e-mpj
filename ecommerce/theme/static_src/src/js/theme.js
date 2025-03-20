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
 * Gestion du thème clair/sombre et des animations pour le site e-commerce
 */

document.addEventListener('DOMContentLoaded', function() {
    // Configuration des animations
    const animationConfig = {
        menuItems: {
            enter: ['opacity-0', 'translate-y-2'],
            final: ['opacity-100', 'translate-y-0'],
            transition: 'transition-all duration-300 ease-out'
        },
        dropdown: {
            enter: ['opacity-0', 'scale-95', '-translate-y-2'],
            final: ['opacity-100', 'scale-100', 'translate-y-0'],
            transition: 'transition-all duration-200 ease-out'
        },
        navbar: {
            scroll: ['backdrop-blur-md', 'bg-white/75', 'dark:bg-gray-800/75'],
            default: ['bg-white', 'dark:bg-gray-800']
        }
    };

    /**
     * Animation des éléments du menu principal
     */
    function initMenuAnimations() {
        const menuItems = document.querySelectorAll('.nav-link');
        
        menuItems.forEach((item, index) => {
            // Ajouter les classes initiales
            item.classList.add(...animationConfig.menuItems.enter);
            item.classList.add(animationConfig.menuItems.transition);
            
            // Animer avec délai
            setTimeout(() => {
                item.classList.remove(...animationConfig.menuItems.enter);
                item.classList.add(...animationConfig.menuItems.final);
            }, 100 * index);
        });
    }

    /**
     * Animation de la navbar au scroll
     */
    function initScrollAnimations() {
        const header = document.querySelector('header');
        let lastScroll = 0;
        
        window.addEventListener('scroll', () => {
            const currentScroll = window.pageYOffset;
            
            if (currentScroll > 50) {
                header.classList.remove(...animationConfig.navbar.default);
                header.classList.add(...animationConfig.navbar.scroll);
                header.classList.add('shadow-lg');
            } else {
                header.classList.remove(...animationConfig.navbar.scroll);
                header.classList.add(...animationConfig.navbar.default);
                header.classList.remove('shadow-lg');
            }
            
            // Animation de masquage/affichage au scroll
            if (currentScroll > lastScroll && currentScroll > 100) {
                header.style.transform = 'translateY(-100%)';
                header.style.transition = 'transform 0.3s ease-in-out';
            } else {
                header.style.transform = 'translateY(0)';
            }
            
            lastScroll = currentScroll;
        });
    }

    /**
     * Animation des dropdowns améliorée
     */
    function initDropdownAnimations() {
        const dropdownButtons = document.querySelectorAll('.dropdown-button');
        
        dropdownButtons.forEach(button => {
            const dropdown = button.nextElementSibling;
            
            // Configuration initiale
            if (dropdown) {
                dropdown.classList.add(...animationConfig.dropdown.enter);
                dropdown.classList.add(animationConfig.dropdown.transition);
            }
            
            button.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                // Fermer les autres dropdowns avec animation
                dropdownButtons.forEach(otherButton => {
                    if (otherButton !== button) {
                        const otherDropdown = otherButton.nextElementSibling;
                        if (otherDropdown && !otherDropdown.classList.contains('hidden')) {
                            animateDropdownClose(otherDropdown);
                            otherButton.setAttribute('aria-expanded', 'false');
                        }
                    }
                });
                
                // Animer ce dropdown
                if (dropdown.classList.contains('hidden')) {
                    animateDropdownOpen(dropdown);
                    button.setAttribute('aria-expanded', 'true');
                } else {
                    animateDropdownClose(dropdown);
                    button.setAttribute('aria-expanded', 'false');
                }
            });
        });
        
        // Fermeture au clic extérieur avec animation
        document.addEventListener('click', function(e) {
            dropdownButtons.forEach(button => {
                const dropdown = button.nextElementSibling;
                if (dropdown && !dropdown.classList.contains('hidden') && 
                    !dropdown.contains(e.target) && 
                    !button.contains(e.target)) {
                    animateDropdownClose(dropdown);
                    button.setAttribute('aria-expanded', 'false');
                }
            });
        });
    }

    /**
     * Animation d'ouverture du dropdown
     */
    function animateDropdownOpen(dropdown) {
        dropdown.classList.remove('hidden');
        requestAnimationFrame(() => {
            dropdown.classList.remove(...animationConfig.dropdown.enter);
            dropdown.classList.add(...animationConfig.dropdown.final);
        });
    }

    /**
     * Animation de fermeture du dropdown
     */
    function animateDropdownClose(dropdown) {
        dropdown.classList.remove(...animationConfig.dropdown.final);
        dropdown.classList.add(...animationConfig.dropdown.enter);
        
        setTimeout(() => {
            dropdown.classList.add('hidden');
        }, 200);
    }

    // Initialisation des animations
    initMenuAnimations();
    initScrollAnimations();
    initDropdownAnimations();
});

// Commentaire: Ce fichier contient les scripts JavaScript essentiels pour notre site
// Il gère plusieurs fonctionnalités:
// 1. Thème clair/sombre avec sauvegarde des préférences
// 2. Animations au défilement pour améliorer l'expérience utilisateur
// 3. Menu mobile responsive avec animation d'ouverture/fermeture
// 4. Gestion des menus déroulants de navigation
// Ces fonctionnalités améliorent l'expérience tout en restant légères 