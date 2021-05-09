module.exports = {
    purge: [],
    darkMode: false, // or 'media' or 'class'
    theme: {
        extend: {
            colors: {
                customBlue: "#8DE4FF",
                customFaintBlue: "#a0efff",
                customGray: "#484848",
                customViolet: "#3F2E56",
                customGreen: "#06B184",
                customRed: "#FF6666"
            },
            transitionProperty: {
                'height': 'height',
                'max-height': 'max-height',
                'top': 'top',
                'right': 'right'
            },
            keyframes: {
                searchDropdownKeyFramesOpen: {
                    '0%': {top: '0.75rem', maxHeight: 0},
                    '50%': {top: '2.75rem'},
                    '100%': {maxHeight: '16rem', top: '2.75rem'}
                },
                searchDropdownKeyFramesClose: {
                    '0%': {maxHeight: '16rem', top: '2.75rem'},
                    '60%': {maxHeight: '0.75rem', top: '2rem'},
                    '40%': {opacity: 1},
                    '70%': {opacity: 0},
                    '100%': {maxHeight: 0, top: '0.75rem'},
                },
            },
            animation: {
                searchDropdownOpen: 'searchDropdownKeyFramesOpen 300ms ease-out 0s 1 normal forwards',
                searchDropdownClose: 'searchDropdownKeyFramesClose 300ms ease-out 0s 1 normal forwards',
            }
        },
    },
    variants: {
        extend: {},
    },
    plugins: [],
};
