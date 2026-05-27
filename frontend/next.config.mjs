import { fileURLToPath } from "node:url";

const isDevelopment = process.env.NODE_ENV === "development";
const isFirebaseAppHosting = process.env.FIREBASE_APP_HOSTING === "1" || process.env.FIREBASE_APP_HOSTING === "true";
const devPort = process.env.PORT || process.env.npm_config_port || "3000";
const bigintBufferBrowserEntry = fileURLToPath(new URL("./node_modules/bigint-buffer/dist/browser.js", import.meta.url));
const appRoot = fileURLToPath(new URL("./", import.meta.url));
const workspaceRoot = fileURLToPath(new URL("../", import.meta.url));
const tracingRootConfig = { outputFileTracingRoot: isFirebaseAppHosting ? appRoot : workspaceRoot };

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: "standalone",
  ...tracingRootConfig,
  allowedDevOrigins: ["127.0.0.1", "localhost"],
  webpack: (config) => {
    config.resolve ??= {};
    config.resolve.alias = {
      ...(config.resolve.alias ?? {}),
      "bigint-buffer": bigintBufferBrowserEntry,
    };
    return config;
  },
  ...(isDevelopment ? { distDir: `.next-dev-${devPort}` } : {}),
};

export default nextConfig;
