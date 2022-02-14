//
//
//

const path = require("path");
const webpack = require("webpack");

const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
    context: __dirname,
    entry: {
        default_js: "./assets/js/default",
        default: [
            path.join(__dirname, "node_modules", "bootstrap", "scss", "bootstrap.scss"),
            path.join(__dirname, "assets", "scss", "default.scss"), 
        ],
    },
    output: {
        filename: "[name].bundle.js",
        path: path.join(__dirname, "COMPHUB", "static", "build"),
    },
    resolve: {
        extensions: [".js", ".jsx"]
    },
    plugins: [
        new MiniCssExtractPlugin({filename: "[name].bundle.css" }),
    ],
    module: {
        rules: [
            {
                test: /\.s[ac]ss$/i,
                use: [
                    {
                        loader: MiniCssExtractPlugin.loader,
                        options: {},
                    },
                    "css-loader",
                    {
                        loader: "sass-loader",
                        options: { implementation: require("sass") },
                    },
                ],
            },
            {
                test: /\.js(x)$/i,
                exclude: /node_modules/,
                use: [
                    {
                        loader: "babel-loader",
                        options: {
                            presets: ["@babel/preset-env"],
                            cacheDirectory: true,
                        },
                    },
                ],
            },
            {
                test: /\.(svg|png|jpe?g|gif|ico)(\?.*)?$/i,
                type: "asset/resource",
                generator: { filename: "img/[name][ext]" },
            },
            {
                test: /\.(woff2|ttf|eot)(\?.*)?$/i,
                type: "asset",
                generator: { filename: "font/[name][ext]" },
            }
        ],
    },
};
