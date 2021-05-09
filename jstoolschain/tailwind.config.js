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
        'max-height': 'max-height'
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
};
