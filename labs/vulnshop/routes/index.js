const authRoutes = require("./auth");
const apiRoutes = require("./api");
const filesRoutes = require("./files");
const pagesRoutes = require("./pages");

function registerRoutes(app) {
  app.use(authRoutes);
  app.use(apiRoutes);
  app.use(filesRoutes);
  app.use(pagesRoutes);
}

module.exports = { registerRoutes };
