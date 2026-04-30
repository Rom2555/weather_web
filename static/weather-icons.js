function getWeatherIcon(icon) {
    const icons = {
        '01d': `<svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <defs><radialGradient id="sun-g" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#FFEE58"/><stop offset="100%" stop-color="white" stop-opacity="0.8"/></radialGradient></defs>
                    <circle cx="32" cy="32" r="16" fill="url(#sun-g)"/>
                    <g stroke="white" stroke-width="2.5" stroke-linecap="round" opacity="0.9">
                        <line x1="32" y1="2" x2="32" y2="12"/><line x1="32" y1="52" x2="32" y2="62"/>
                        <line x1="2" y1="32" x2="12" y2="32"/><line x1="52" y1="32" x2="62" y2="32"/>
                        <line x1="10.1" y1="10.1" x2="17.2" y2="17.2"/><line x1="46.8" y1="46.8" x2="53.9" y2="53.9"/>
                        <line x1="10.1" y1="53.9" x2="17.2" y2="46.8"/><line x1="46.8" y1="17.2" x2="53.9" y2="10.1"/>
                    </g>
                </svg>`,

        '01n': `<svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <defs><radialGradient id="moon-g" cx="40%" cy="40%" r="50%"><stop offset="0%" stop-color="white"/><stop offset="100%" stop-color="#E0E0E0" stop-opacity="0.9"/></radialGradient></defs>
                    <path d="M45 6C27.3 6 13 20.3 13 38s14.3 32 32 32c4.5 0 8.8-.9 12.7-2.5C45.1 61.4 32 50 32 34S45.1 6.6 45 6z" fill="url(#moon-g)"/>
                </svg>`,

        '02d': `<svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <defs><radialGradient id="sun-g2" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#FFEE58"/><stop offset="100%" stop-color="white" stop-opacity="0.9"/></radialGradient><linearGradient id="cloud-g" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#FFFFFF"/><stop offset="100%" stop-color="#D6D6D6" stop-opacity="0.95"/></linearGradient></defs>
                    <circle cx="48" cy="18" r="10" fill="url(#sun-g2)" opacity="0.9"/>
                    <path d="M16 42c-4.4 0-8-3.6-8-8s3.6-8 8-8h28c2.2 0 4-1.8 4-4s-1.8-4-4-4H32c-5.5 0-10 4.5-10 10 0 2.1.6 4 1.8 5.6C20.4 41.4 18.3 42 16 42z" fill="url(#cloud-g)" transform="translate(-4, 2)"/>
                </svg>`,

        '02n': `<svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <defs><linearGradient id="cloud-gn" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#CCCCCC"/><stop offset="100%" stop-color="#999999" stop-opacity="0.8"/></linearGradient></defs>
                    <path d="M16 42c-4.4 0-8-3.6-8-8s3.6-8 8-8h28c2.2 0 4-1.8 4-4s-1.8-4-4-4H32c-5.5 0-10 4.5-10 10 0 2.1.6 4 1.8 5.6C20.4 41.4 18.3 42 16 42z" fill="url(#cloud-gn)" transform="translate(-4, 2)"/>
                </svg>`,

        '03d': `<svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <defs><linearGradient id="cloud-g3" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#FFFFFF"/><stop offset="100%" stop-color="#BBBBBB" stop-opacity="0.95"/></linearGradient></defs>
                    <path d="M10 44c-5.5 0-10-4.5-10-10s4.5-10 10-10h34c2.8 0 5-2.2 5-5s-2.2-5-5-5H36c-6.6 0-12 5.4-12 12 0 2.6.8 5 2.2 6.9C22 43.2 19.7 44 17 44H10z" fill="url(#cloud-g3)" transform="translate(2, -2)"/>
                </svg>`,

        '03n': `<svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <defs><linearGradient id="cloud-g3n" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#CCCCCC"/><stop offset="100%" stop-color="#888888" stop-opacity="0.8"/></linearGradient></defs>
                    <path d="M10 44c-5.5 0-10-4.5-10-10s4.5-10 10-10h34c2.8 0 5-2.2 5-5s-2.2-5-5-5H36c-6.6 0-12 5.4-12 12 0 2.6.8 5 2.2 6.9C22 43.2 19.7 44 17 44H10z" fill="url(#cloud-g3n)" transform="translate(2, -2)"/>
                </svg>`,

        '04d': `<svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <defs><linearGradient id="cloud-g4" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#E0E0E0"/><stop offset="100%" stop-color="#A0A0A0" stop-opacity="0.95"/></linearGradient></defs>
                    <path d="M10 44c-5.5 0-10-4.5-10-10s4.5-10 10-10h34c2.8 0 5-2.2 5-5s-2.2-5-5-5H36c-6.6 0-12 5.4-12 12 0 2.6.8 5 2.2 6.9C22 43.2 19.7 44 17 44H10z" fill="url(#cloud-g4)" transform="translate(2, -2)"/>
                    <path d="M14 48c-4.4 0-8-3.6-8-8s3.6-8 8-8h22c2.2 0 4-1.8 4-4s-1.8-4-4-4H30c-5.5 0-10 4.5-10 10 0 2.1.6 4 1.8 5.6C18.4 47.4 16.3 48 14 48z" fill="white" opacity="0.5" transform="translate(-6, 2)"/>
                </svg>`,

        '04n': `<svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <defs><linearGradient id="cloud-g4n" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#AAAAAA"/><stop offset="100%" stop-color="#777777" stop-opacity="0.8"/></linearGradient></defs>
                    <path d="M10 44c-5.5 0-10-4.5-10-10s4.5-10 10-10h34c2.8 0 5-2.2 5-5s-2.2-5-5-5H36c-6.6 0-12 5.4-12 12 0 2.6.8 5 2.2 6.9C22 43.2 19.7 44 17 44H10z" fill="url(#cloud-g4n)" transform="translate(2, -2)"/>
                    <path d="M14 48c-4.4 0-8-3.6-8-8s3.6-8 8-8h22c2.2 0 4-1.8 4-4s-1.8-4-4-4H30c-5.5 0-10 4.5-10 10 0 2.1.6 4 1.8 5.6C18.4 47.4 16.3 48 14 48z" fill="white" opacity="0.3" transform="translate(-6, 2)"/>
                </svg>`,

        '09d': `<svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <defs><linearGradient id="cloud-g9" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#FFFFFF"/><stop offset="100%" stop-color="#BBBBBB" stop-opacity="0.95"/></linearGradient></defs>
                    <path d="M10 40c-5.5 0-10-4.5-10-10s4.5-10 10-10h34c2.8 0 5-2.2 5-5s-2.2-5-5-5H36c-6.6 0-12 5.4-12 12 0 2.6.8 5 2.2 6.9C22 39.2 19.7 40 17 40H10z" fill="url(#cloud-g9)"/>
                    <path d="M22 48c0 2.2-1.8 4-4 4s-4-1.8-4-4 1.8-4 4-4 4 1.8 4 4zm8 8c0 2.2-1.8 4-4 4s-4-1.8-4-4 1.8-4 4-4 4 1.8 4 4zm8-6c0 2.2-1.8 4-4 4s-4-1.8-4-4 1.8-4 4-4 4 1.8 4 4z" fill="white" opacity="0.9"/>
                </svg>`,

        '09n': `<svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <defs><linearGradient id="cloud-g9n" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#CCCCCC"/><stop offset="100%" stop-color="#888888" stop-opacity="0.8"/></linearGradient></defs>
                    <path d="M10 40c-5.5 0-10-4.5-10-10s4.5-10 10-10h34c2.8 0 5-2.2 5-5s-2.2-5-5-5H36c-6.6 0-12 5.4-12 12 0 2.6.8 5 2.2 6.9C22 39.2 19.7 40 17 40H10z" fill="url(#cloud-g9n)"/>
                    <path d="M22 48c0 2.2-1.8 4-4 4s-4-1.8-4-4 1.8-4 4-4 4 1.8 4 4zm8 8c0 2.2-1.8 4-4 4s-4-1.8-4-4 1.8-4 4-4 4 1.8 4 4zm8-6c0 2.2-1.8 4-4 4s-4-1.8-4-4 1.8-4 4-4 4 1.8 4 4z" fill="white" opacity="0.7"/>
                </svg>`,

        '10d': `<svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <defs><linearGradient id="cloud-g10" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#FFFFFF"/><stop offset="100%" stop-color="#BBBBBB" stop-opacity="0.95"/></linearGradient></defs>
                    <path d="M10 36c-5.5 0-10-4.5-10-10s4.5-10 10-10h34c2.8 0 5-2.2 5-5s-2.2-5-5-5H36c-6.6 0-12 5.4-12 12 0 2.6.8 5 2.2 6.9C22 35.2 19.7 36 17 36H10z" fill="url(#cloud-g10)"/>
                    <path d="M18 44c0 2.2-1.8 4-4 4s-4-1.8-4-4 1.8-4 4-4 4 1.8 4 4zm10 8c0 2.2-1.8 4-4 4s-4-1.8-4-4 1.8-4 4-4 4 1.8 4 4zm8-8c0 2.2-1.8 4-4 4s-4-1.8-4-4 1.8-4 4-4 4 1.8 4 4zm-6 6c0 2.2-1.8 4-4 4s-4-1.8-4-4 1.8-4 4-4 4 1.8 4 4z" fill="white" opacity="0.9"/>
                </svg>`,

        '10n': `<svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <defs><linearGradient id="cloud-g10n" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#CCCCCC"/><stop offset="100%" stop-color="#888888" stop-opacity="0.8"/></linearGradient></defs>
                    <path d="M10 36c-5.5 0-10-4.5-10-10s4.5-10 10-10h34c2.8 0 5-2.2 5-5s-2.2-5-5-5H36c-6.6 0-12 5.4-12 12 0 2.6.8 5 2.2 6.9C22 35.2 19.7 36 17 36H10z" fill="url(#cloud-g10n)"/>
                    <path d="M18 44c0 2.2-1.8 4-4 4s-4-1.8-4-4 1.8-4 4-4 4 1.8 4 4zm10 8c0 2.2-1.8 4-4 4s-4-1.8-4-4 1.8-4 4-4 4 1.8 4 4zm8-8c0 2.2-1.8 4-4 4s-4-1.8-4-4 1.8-4 4-4 4 1.8 4 4zm-6 6c0 2.2-1.8 4-4 4s-4-1.8-4-4 1.8-4 4-4 4 1.8 4 4z" fill="white" opacity="0.7"/>
                </svg>`,

        '11d': `<svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <defs><linearGradient id="cloud-g11" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#E0E0E0"/><stop offset="100%" stop-color="#AAAAAA" stop-opacity="0.95"/></linearGradient></defs>
                    <path d="M10 38c-5.5 0-10-4.5-10-10s4.5-10 10-10h34c2.8 0 5-2.2 5-5s-2.2-5-5-5H36c-6.6 0-12 5.4-12 12 0 2.6.8 5 2.2 6.9C22 37.2 19.7 38 17 38H10z" fill="url(#cloud-g11)"/>
                    <path d="M36 38l-8 14 10-2 -6 16 14-20z" fill="#FFD700" stroke="white" stroke-width="1"/>
                </svg>`,

        '11n': `<svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <defs><linearGradient id="cloud-g11n" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#AAAAAA"/><stop offset="100%" stop-color="#777777" stop-opacity="0.8"/></linearGradient></defs>
                    <path d="M10 38c-5.5 0-10-4.5-10-10s4.5-10 10-10h34c2.8 0 5-2.2 5-5s-2.2-5-5-5H36c-6.6 0-12 5.4-12 12 0 2.6.8 5 2.2 6.9C22 37.2 19.7 38 17 38H10z" fill="url(#cloud-g11n)"/>
                    <path d="M36 38l-8 14 10-2 -6 16 14-20z" fill="#FFD700" stroke="white" stroke-width="1" opacity="0.8"/>
                </svg>`,

        '13d': `<svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <defs><linearGradient id="cloud-g13" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#FFFFFF"/><stop offset="100%" stop-color="#BBBBBB" stop-opacity="0.95"/></linearGradient></defs>
                    <path d="M10 38c-5.5 0-10-4.5-10-10s4.5-10 10-10h34c2.8 0 5-2.2 5-5s-2.2-5-5-5H36c-6.6 0-12 5.4-12 12 0 2.6.8 5 2.2 6.9C22 37.2 19.7 38 17 38H10z" fill="url(#cloud-g13)"/>
                    <circle cx="20" cy="52" r="2.5" fill="white"/><circle cx="32" cy="56" r="2.5" fill="white"/><circle cx="44" cy="50" r="2.5" fill="white"/>
                </svg>`,

        '13n': `<svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <defs><linearGradient id="cloud-g13n" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#CCCCCC"/><stop offset="100%" stop-color="#888888" stop-opacity="0.8"/></linearGradient></defs>
                    <path d="M10 38c-5.5 0-10-4.5-10-10s4.5-10 10-10h34c2.8 0 5-2.2 5-5s-2.2-5-5-5H36c-6.6 0-12 5.4-12 12 0 2.6.8 5 2.2 6.9C22 37.2 19.7 38 17 38H10z" fill="url(#cloud-g13n)"/>
                    <circle cx="20" cy="52" r="2.5" fill="white" opacity="0.7"/><circle cx="32" cy="56" r="2.5" fill="white" opacity="0.7"/><circle cx="44" cy="50" r="2.5" fill="white" opacity="0.7"/>
                </svg>`,

        '50d': `<svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M10 32c0-2.2 1.8-4 4-4h36c2.2 0 4 1.8 4 4s-1.8 4-4 4H14c-2.2 0-4-1.8-4-4z" fill="white" opacity="0.5"/>
                    <path d="M6 40c0-2.2 1.8-4 4-4h44c2.2 0 4 1.8 4 4s-1.8 4-4 4H10c-2.2 0-4-1.8-4-4z" fill="white" opacity="0.8"/>
                    <path d="M10 48c0-2.2 1.8-4 4-4h36c2.2 0 4 1.8 4 4s-1.8 4-4 4H14c-2.2 0-4-1.8-4-4z" fill="white" opacity="0.5"/>
                </svg>`,

        '50n': `<svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M10 32c0-2.2 1.8-4 4-4h36c2.2 0 4 1.8 4 4s-1.8 4-4 4H14c-2.2 0-4-1.8-4-4z" fill="white" opacity="0.3"/>
                    <path d="M6 40c0-2.2 1.8-4 4-4h44c2.2 0 4 1.8 4 4s-1.8 4-4 4H10c-2.2 0-4-1.8-4-4z" fill="white" opacity="0.5"/>
                    <path d="M10 48c0-2.2 1.8-4 4-4h36c2.2 0 4 1.8 4 4s-1.8 4-4 4H14c-2.2 0-4-1.8-4-4z" fill="white" opacity="0.3"/>
                </svg>`
    };
    return icons[icon] || icons['02d'];
}