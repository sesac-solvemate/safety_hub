const TsconfigPathsPlugin = require("tsconfig-paths-webpack-plugin");
const path = require("path");

module.exports = {
  webpack: {
    alias: {
      '@': path.resolve(__dirname, 'src/'),
    },
    plugins: {
      add: [
        new TsconfigPathsPlugin({
          configFile: "./tsconfig.json",
        }),
      ],
    },
    configure: (webpackConfig, { env, paths }) => {
      webpackConfig.devServer = {
        ...webpackConfig.devServer,
        setupMiddlewares: (middlewares, devServer) => {
          if (!devServer) {
            throw new Error('webpack-dev-server is not defined');
          }

          // 기존 onBeforeSetupMiddleware의 로직
          devServer.app.get('/some/path', (req, res) => {
            res.json({ custom: 'response' });
          });

          // 기존 onAfterSetupMiddleware의 로직
          middlewares.push((req, res, next) => {
            // Custom middleware logic
            next();
          });

          return middlewares;
        },
      };

      return webpackConfig;
    },
  },
};
