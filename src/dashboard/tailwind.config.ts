import type { Config } from 'tailwindcss';

export default <Partial<Config>>{
    theme: {
        screens: {
            xl: '1280px',
        },
        extend: {
            colors: {
                customGray: '#323232',
            },
        },
    },
};
