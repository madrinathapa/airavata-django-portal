var path = require('path')
var webpack = require('webpack')
const ExtractTextPlugin = require("extract-text-webpack-plugin");
const CleanWebpackPlugin = require('clean-webpack-plugin');

module.exports = {
  entry: {
      'project-list': './static/django_airavata_workspace/js/entry-project-list',
      'dashboard': './static/django_airavata_workspace/js/entry-dashboard',
      'create-experiment': './static/django_airavata_workspace/js/entry-create-experiment',
      'view-experiment': './static/django_airavata_workspace/js/entry-view-experiment',
      'experiment-list': './static/django_airavata_workspace/js/entry-experiment-list',
  },
  output: {
    path: path.resolve(__dirname, './static/django_airavata_workspace/dist/'),
    publicPath: '/static/django_airavata_workspace/dist/',
    filename: '[name].js'
  },
  module: {
    rules: [
      {
        test: /\.vue$/,
        loader: 'vue-loader',
        options: {
          loaders: {
          },
          extractCSS: true
          // other vue-loader options go here
        }
      },
      {
        test: /\.js$/,
        loader: 'babel-loader',
        exclude: /node_modules/
      },
      {
          test: /\.css$/,
          use: ExtractTextPlugin.extract({
              fallback: "style-loader",
              use: "css-loader"
          })
      },
      {
        test: /\.(png|jpg|gif|svg)$/,
        loader: 'file-loader',
        options: {
          name: '[name].[ext]?[hash]'
        }
      }
    ]
  },
  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.esm.js'
    }
  },
  devServer: {
    historyApiFallback: true,
    noInfo: true
  },
  performance: {
    hints: false
  },
  devtool: '#eval-source-map',
  plugins: [
      // Exclude all but the 'en' locale from moment's locales
      new webpack.ContextReplacementPlugin(/moment[\/\\]locale$/, /^en$/),
      new ExtractTextPlugin("[name].css"),
      new CleanWebpackPlugin(['./static/django_airavata_workspace/dist']),
      new webpack.optimize.CommonsChunkPlugin({
          name: 'common',
      }),

  ]
}

if (process.env.NODE_ENV === 'production') {
  module.exports.devtool = '#source-map'
  // http://vue-loader.vuejs.org/en/workflow/production.html
  module.exports.plugins = (module.exports.plugins || []).concat([
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: '"production"'
      }
    }),
    new webpack.optimize.UglifyJsPlugin({
      sourceMap: true,
      compress: {
        warnings: false
      }
    }),
    new webpack.LoaderOptionsPlugin({
      minimize: true
    })
  ])
}
