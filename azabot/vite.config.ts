import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react-swc";
import path from "path";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const BACKEND = env.VITE_DEV_BACKEND_URL || "http://127.0.0.1:8000";

  return {
    server: {
      host: "::",
      port: 8080,
      hmr: { overlay: true },

      // ── Proxy: كل طلبات API تُحوَّل للباك أوتوماتيكياً ──────
      proxy: {
        "/chat":      { target: BACKEND, changeOrigin: true, secure: false },
        "/brands":    { target: BACKEND, changeOrigin: true, secure: false },
        "/admin":     { target: BACKEND, changeOrigin: true, secure: false },
        "/health":    { target: BACKEND, changeOrigin: true, secure: false },
        "/uberfix":   { target: BACKEND, changeOrigin: true, secure: false },
        "/webhook":   { target: BACKEND, changeOrigin: true, secure: false },
        "/embed":     { target: BACKEND, changeOrigin: true, secure: false },
        "/piper":     { target: BACKEND, changeOrigin: true, secure: false },
        "/static":    { target: BACKEND, changeOrigin: true, secure: false },
        "/ws": {
          target: BACKEND.replace("http", "ws"),
          ws: true,
          changeOrigin: true,
        },
      },
    },

    plugins: [react()],

    resolve: {
      alias: { "@": path.resolve(__dirname, "./src") },
      dedupe: [
        "react", "react-dom",
        "react/jsx-runtime", "react/jsx-dev-runtime",
        "@tanstack/react-query", "@tanstack/query-core",
      ],
    },

    build: {
      target: "es2020",
      sourcemap: mode === "development",
      minify: "esbuild",
      cssMinify: true,
      rollupOptions: {
        output: {
          manualChunks(id: string) {
            if (id.includes("node_modules/react") || id.includes("node_modules/react-dom") || id.includes("node_modules/react-router-dom")) return "react-vendor";
            if (id.includes("node_modules/@radix-ui") || id.includes("node_modules/lucide-react")) return "ui-vendor";
            if (id.includes("node_modules/@tanstack")) return "query-vendor";
            if (id.includes("node_modules/react-markdown") || id.includes("node_modules/remark") || id.includes("node_modules/rehype")) return "markdown-vendor";
          },
          chunkFileNames:  "assets/[name]-[hash].js",
          entryFileNames:  "assets/[name]-[hash].js",
          assetFileNames:  "assets/[name]-[hash][extname]",
        },
      },
      chunkSizeWarningLimit: 600,
    },

    optimizeDeps: {
      include: ["react", "react-dom", "react-router-dom", "@tanstack/react-query"],
    },
  };
});
