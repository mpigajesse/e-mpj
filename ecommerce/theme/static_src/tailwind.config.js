/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /*
         * Templates in core app (BASE_DIR/core/templates).
         * Adjust the following line to match your project structure.
         */
        '../../core/templates/**/*.html',

        /*
         * Templates in products app (BASE_DIR/products/templates).
         * Adjust the following line to match your project structure.
         */
        '../../products/templates/**/*.html',

        /*
         * JavaScript files in static directories.
         * Adjust the following lines to match your project structure.
         */
        '../../static/js/**/*.js',
        '../../core/static/js/**/*.js',
        '../../products/static/js/**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        extend: {
            colors: {
                primary: {
                    50: '#eef9ff',
                    100: '#dcf2ff',
                    200: '#b3e8ff',
                    300: '#73d8ff',
                    400: '#34c2ff',
                    500: '#0ca3f5',
                    600: '#0083d4',
                    700: '#0069ab',
                    800: '#005a8d',
                    900: '#074b73',
                    950: '#053047',
                },
                secondary: {
                    50: '#f8f8f8',
                    100: '#f0f0f0',
                    200: '#e4e4e4',
                    300: '#d1d1d1',
                    400: '#b4b4b4',
                    500: '#9a9a9a',
                    600: '#818181',
                    700: '#6a6a6a',
                    800: '#5a5a5a',
                    900: '#4e4e4e',
                    950: '#292929',
                },
                accent: {
                    50: '#fff8eb',
                    100: '#ffecc6',
                    200: '#ffd789',
                    300: '#ffbd4a',
                    400: '#ffa61b',
                    500: '#f98500',
                    600: '#dd6400',
                    700: '#b74500',
                    800: '#953600',
                    900: '#7b2f00',
                    950: '#461500',
                },
                success: {
                    50: '#edfdf5',
                    100: '#d3f9e6',
                    200: '#aaf1d1',
                    300: '#73e4b7',
                    400: '#3acf97',
                    500: '#1fb37c',
                    600: '#0e9163',
                    700: '#0c7352',
                    800: '#0c5c43',
                    900: '#094c38',
                    950: '#042b21',
                },
                danger: {
                    50: '#fef2f2',
                    100: '#ffe1e1',
                    200: '#ffc9c9',
                    300: '#fea3a3',
                    400: '#fc6f6f',
                    500: '#f43f3f',
                    600: '#e12424',
                    700: '#be1a1a',
                    800: '#9d1a1a',
                    900: '#821c1c',
                    950: '#470b0b',
                },
            },
            fontFamily: {
                sans: ['Inter', 'system-ui', 'sans-serif'],
                serif: ['Merriweather', 'serif'],
                mono: ['Fira Code', 'monospace'],
            },
            container: {
                center: true,
                padding: {
                    DEFAULT: '1rem',
                    sm: '2rem',
                    lg: '4rem',
                    xl: '5rem',
                    '2xl': '6rem',
                },
            },
            borderRadius: {
                'sm': '0.125rem',
                DEFAULT: '0.25rem',
                'md': '0.375rem',
                'lg': '0.5rem',
                'xl': '0.75rem',
                '2xl': '1rem',
                '3xl': '1.5rem',
                'pill': '9999px',
            },
            typography: (theme) => ({
                DEFAULT: {
                    css: {
                        color: theme('colors.gray.700'),
                        a: {
                            color: theme('colors.primary.600'),
                            '&:hover': {
                                color: theme('colors.primary.500'),
                            },
                        },
                        h1: {
                            color: theme('colors.gray.800'),
                        },
                        h2: {
                            color: theme('colors.gray.800'),
                        },
                        h3: {
                            color: theme('colors.gray.800'),
                        },
                        h4: {
                            color: theme('colors.gray.800'),
                        },
                    },
                },
                dark: {
                    css: {
                        color: theme('colors.gray.300'),
                        a: {
                            color: theme('colors.primary.400'),
                            '&:hover': {
                                color: theme('colors.primary.300'),
                            },
                        },
                        h1: {
                            color: theme('colors.gray.100'),
                        },
                        h2: {
                            color: theme('colors.gray.100'),
                        },
                        h3: {
                            color: theme('colors.gray.100'),
                        },
                        h4: {
                            color: theme('colors.gray.100'),
                        },
                    },
                },
            }),
            animation: {
                'fade-in': 'fadeIn 0.3s ease-in-out',
                'slide-in': 'slideIn 0.3s ease-in-out',
                'slide-in-up': 'slideInUp 0.3s ease-in-out',
                'bounce-slow': 'bounce 3s infinite',
            },
            keyframes: {
                fadeIn: {
                    '0%': { opacity: '0' },
                    '100%': { opacity: '1' },
                },
                slideIn: {
                    '0%': { transform: 'translateX(-100%)' },
                    '100%': { transform: 'translateX(0)' },
                },
                slideInUp: {
                    '0%': { transform: 'translateY(100%)' },
                    '100%': { transform: 'translateY(0)' },
                },
            },
        },
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
        // Le plugin line-clamp n'est pas installé, on le supprime pour éviter l'erreur
        // require('@tailwindcss/line-clamp'),
    ],
    darkMode: 'class', // Active le mode sombre via la classe 'dark'
}
