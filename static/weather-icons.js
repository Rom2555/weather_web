function getWeatherIcon(icon) {
    // Базовые фигуры для облаков (безопасная геометрия)
    const cloud = '<g><ellipse cx="24" cy="36" rx="14" ry="10" fill="white" opacity="0.9"/><ellipse cx="40" cy="36" rx="16" ry="12" fill="white"/><rect x="10" y="36" width="44" height="14" rx="7" fill="white"/></g>';
    const cloudDark = '<g opacity="0.3"><ellipse cx="24" cy="38" rx="14" ry="10" fill="white"/><ellipse cx="40" cy="38" rx="16" ry="12" fill="white"/><rect x="10" y="38" width="44" height="14" rx="7" fill="white"/></g>';

    // Капли дождя (простые вытянутые круги)
    const rain = '<g fill="white" opacity="0.9"><ellipse cx="20" cy="56" rx="2" ry="3.5"/><ellipse cx="32" cy="58" rx="2" ry="3.5"/><ellipse cx="44" cy="56" rx="2" ry="3.5"/></g>';

    // Снежинки
    const snow = '<g fill="white" opacity="0.9"><circle cx="20" cy="56" r="2.5"/><circle cx="32" cy="58" r="2.5"/><circle cx="44" cy="56" r="2.5"/></g>';

    // Молния
    const bolt = '<path d="M34 48 L28 60 L37 56 L30 66" fill="#FFD700" stroke="white" stroke-width="0.5"/>';

    const icons = {
        '01d': '<svg viewBox="0 0 64 64" fill="none"><circle cx="32" cy="32" r="14" fill="white"/><g stroke="white" stroke-width="2.5" stroke-linecap="round" opacity="0.9"><line x1="32" y1="2" x2="32" y2="10"/><line x1="32" y1="54" x2="32" y2="62"/><line x1="2" y1="32" x2="10" y2="32"/><line x1="54" y1="32" x2="62" y2="32"/></g></svg>',

        '01n': '<svg viewBox="0 0 64 64" fill="none"><path fill="white" d="M45 6C27.3 6 13 20.3 13 38s14.3 32 32 32c4.5 0 8.8-.9 12.7-2.5C45.1 61.4 32 50 32 34S45.1 6.6 45 6z"/></svg>',

        '02d': `<svg viewBox="0 0 64 64" fill="none"><circle cx="48" cy="18" r="10" fill="white" opacity="0.9"/>${cloud}</svg>`,
        '02n': `<svg viewBox="0 0 64 64" fill="none">${cloudDark}</svg>`,

        '03d': `<svg viewBox="0 0 64 64" fill="none">${cloud}</svg>`,
        '03n': `<svg viewBox="0 0 64 64" fill="none">${cloudDark}</svg>`,

        '04d': `<svg viewBox="0 0 64 64" fill="none">${cloudDark}${cloud}</svg>`,
        '04n': `<svg viewBox="0 0 64 64" fill="none" opacity="0.7">${cloudDark}${cloud}</svg>`,

        '09d': `<svg viewBox="0 0 64 64" fill="none">${cloud}${rain}</svg>`,
        '09n': `<svg viewBox="0 0 64 64" fill="none" opacity="0.7">${cloudDark}${rain}</svg>`,

        '10d': `<svg viewBox="0 0 64 64" fill="none">${cloud}${rain}</svg>`,
        '10n': `<svg viewBox="0 0 64 64" fill="none" opacity="0.7">${cloudDark}${rain}</svg>`,

        '11d': `<svg viewBox="0 0 64 64" fill="none" opacity="0.9">${cloudDark}${cloud}${bolt}</svg>`,
        '11n': `<svg viewBox="0 0 64 64" fill="none" opacity="0.4">${cloudDark}${cloud}${bolt}</svg>`,

        '13d': `<svg viewBox="0 0 64 64" fill="none">${cloud}${snow}</svg>`,
        '13n': `<svg viewBox="0 0 64 64" fill="none" opacity="0.7">${cloudDark}${snow}</svg>`,

        '50d': `<svg viewBox="0 0 64 64" fill="none"><line x1="10" y1="28" x2="54" y2="28" stroke="white" stroke-width="3" stroke-linecap="round" opacity="0.5"/><line x1="14" y1="36" x2="50" y2="36" stroke="white" stroke-width="3" stroke-linecap="round" opacity="0.8"/><line x1="10" y1="44" x2="54" y2="44" stroke="white" stroke-width="3" stroke-linecap="round" opacity="0.5"/></svg>`,
        '50n': `<svg viewBox="0 0 64 64" fill="none"><line x1="10" y1="28" x2="54" y2="28" stroke="white" stroke-width="3" stroke-linecap="round" opacity="0.3"/><line x1="14" y1="36" x2="50" y2="36" stroke="white" stroke-width="3" stroke-linecap="round" opacity="0.5"/><line x1="10" y1="44" x2="54" y2="44" stroke="white" stroke-width="3" stroke-linecap="round" opacity="0.3"/></svg>`
    };
    return icons[icon] || icons['02d'];
}