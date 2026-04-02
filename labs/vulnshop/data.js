// In-memory "Database" — VULNERABLE by design

const users = [
  {
    id: 1,
    username: "admin",
    password: "admin123",
    role: "admin",
    secret: "FLAG{nosql_injection_success}",
  },
  {
    id: 2,
    username: "user1",
    password: "password1",
    role: "user",
    secret: "user1 personal data",
  },
  {
    id: 3,
    username: "manager",
    password: "manager2024",
    role: "manager",
    secret: "FLAG{prototype_pollution_win}",
  },
];

const messages = [
  {
    id: 1,
    from: "admin",
    to: "user1",
    text: "Welcome to the new ShopTech platform.",
    read: false,
  },
  {
    id: 2,
    from: "admin",
    to: "manager",
    text: "Backup credentials are: bk_s3cret_2024",
    read: false,
  },
];

const config = {
  appName: "ShopTech",
  debug: true,
  version: "1.0.0",
  internalAPI: "http://127.0.0.1:4000",
};

const sessions = {};

module.exports = { users, messages, config, sessions };
