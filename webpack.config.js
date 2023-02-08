const path = require('path');

module.exports = {
    entry: './static/js/index.js',
    mode: 'development',
    output: {
        filename: 'main.js',
        path: path.resolve(__dirname, 'static/dist'),
    },
    optimization: {
        minimize: true
    },

    // Easy way to also bundle the dropzone css.
    module: {rules: [{test: /\.css$/, use: ["style-loader", "css-loader"]}]},
};
