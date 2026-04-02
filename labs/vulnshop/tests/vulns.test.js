import { describe, it, expect } from "vitest";
import request from "supertest";
import app from "../index.js";

describe("Routes", () => {
  it("GET / returns 200 with app name", async () => {
    const res = await request(app).get("/");
    expect(res.status).toBe(200);
    expect(res.text).toContain("ShopTech");
  });

  it("GET /login returns 200", async () => {
    const res = await request(app).get("/login");
    expect(res.status).toBe(200);
    expect(res.text).toContain("Login");
  });

  it("GET /search returns 200", async () => {
    const res = await request(app).get("/search");
    expect(res.status).toBe(200);
  });

  it("GET /files returns 200", async () => {
    const res = await request(app).get("/files");
    expect(res.status).toBe(200);
  });

  it("GET /merge returns 200", async () => {
    const res = await request(app).get("/merge");
    expect(res.status).toBe(200);
  });

  it("GET /fetch returns 200", async () => {
    const res = await request(app).get("/fetch");
    expect(res.status).toBe(200);
  });
});

describe("Auth", () => {
  it("valid login returns success and token", async () => {
    const res = await request(app)
      .post("/api/login")
      .send({ username: "admin", password: "admin123" });
    expect(res.status).toBe(200);
    expect(res.body.success).toBe(true);
    expect(res.body.token).toBeDefined();
    expect(res.body.user.username).toBe("admin");
  });

  it("invalid login returns 401", async () => {
    const res = await request(app)
      .post("/api/login")
      .send({ username: "admin", password: "wrong" });
    expect(res.status).toBe(401);
    expect(res.body.error).toBe("Invalid credentials");
  });

  it("login returns user role", async () => {
    const res = await request(app)
      .post("/api/login")
      .send({ username: "user1", password: "password1" });
    expect(res.status).toBe(200);
    expect(res.body.user.role).toBe("user");
  });
});

describe("API - Users", () => {
  it("GET /api/users returns all users", async () => {
    const res = await request(app).get("/api/users");
    expect(res.status).toBe(200);
    expect(Array.isArray(res.body)).toBe(true);
    expect(res.body.length).toBeGreaterThan(0);
  });

  it("GET /api/users?role=admin filters by role", async () => {
    const res = await request(app).get("/api/users?role=admin");
    expect(res.status).toBe(200);
    expect(res.body.every((u) => u.role === "admin")).toBe(true);
  });
});

describe("API - Messages", () => {
  it("GET /api/messages/:username returns messages", async () => {
    const res = await request(app).get("/api/messages/user1");
    expect(res.status).toBe(200);
    expect(Array.isArray(res.body)).toBe(true);
    expect(res.body.length).toBeGreaterThan(0);
  });

  it("GET /api/messages/:username returns empty for unknown user", async () => {
    const res = await request(app).get("/api/messages/nobody");
    expect(res.status).toBe(200);
    expect(res.body).toEqual([]);
  });
});

describe("API - Config", () => {
  it("GET /api/config returns app config", async () => {
    const res = await request(app).get("/api/config");
    expect(res.status).toBe(200);
    expect(res.body.appName).toBe("ShopTech");
    expect(res.body.version).toBe("1.0.0");
  });
});

describe("API - Merge", () => {
  it("POST /api/merge merges objects", async () => {
    const res = await request(app)
      .post("/api/merge")
      .send({ type: "custom", extra: "value" });
    expect(res.status).toBe(200);
    expect(res.body.merged.type).toBe("custom");
    expect(res.body.merged.extra).toBe("value");
  });
});

describe("Files", () => {
  it("GET /files?name=readme.txt returns the file", async () => {
    const res = await request(app).get("/files?name=readme.txt");
    expect(res.status).toBe(200);
  });

  it("GET /files?name=nonexistent returns 404", async () => {
    const res = await request(app).get("/files?name=does_not_exist.txt");
    expect(res.status).toBe(404);
  });
});

describe("Search", () => {
  it("GET /search?q=test returns 200", async () => {
    const res = await request(app).get("/search?q=test");
    expect(res.status).toBe(200);
    expect(res.text).toContain("Results for:");
  });
});
