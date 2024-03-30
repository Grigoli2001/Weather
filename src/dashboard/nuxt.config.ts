// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    app: {
        head: {
            title: 'Weather APP',
        },
    },
    ssr: false,
    devtools: { enabled: true },
    pages: true,
    modules: ['@nuxt/ui', '@nuxtjs/google-fonts', '@nuxtjs/tailwindcss'],
    googleFonts: {
        families: {
            Roboto: true,
            Inter: [400, 700],
            'Josefin+Sans': true,
            Lato: [100, 300],
            Raleway: {
                wght: [100, 400],
                ital: [100],
            },
            'Crimson Pro': {
                wght: '200..900',
                ital: '200..700',
            },
        },
    },
});
