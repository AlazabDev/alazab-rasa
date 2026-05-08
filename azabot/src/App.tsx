/**
 * AzaBot — App Root
 * ─────────────────────────────────────────────────────────
 * • SiteProvider يُغلّف كل شيء داخل BrowserRouter
 *   حتى يستطيع useLocation قراءة المسار الحالي
 * • كل وجهة موقع تستخدم <SitePage> التي تستهلك السياق
 * • lazy loading للصفحات غير الحيوية
 * ─────────────────────────────────────────────────────────
 */

import { lazy, Suspense, useState, Component, ErrorInfo, ReactNode } from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Link, Route, Routes } from "react-router-dom";
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { SiteProvider } from "@/context/SiteContext";
import { Menu, X, ShieldCheck, LogIn, Home } from "lucide-react";

// Page حيوية — eager
import SitePage from "./pages/SitePage";

// Pages — lazy (تحمّل عند الطلب فقط)
const Admin = lazy(() => import("./pages/Admin"));
const AdminLogin = lazy(() => import("./pages/AdminLogin"));
const NotFound = lazy(() => import("./pages/NotFound"));

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60_000,
      retry: 1,
    },
  },
});

function PageFallback() {
  return <div className="min-h-screen bg-background flex items-center justify-center">
    <div className="w-8 h-8 border-4 border-brand border-t-transparent rounded-full animate-spin" />
  </div>;
}

class ErrorBoundary extends Component<{ children: ReactNode }, { hasError: boolean }> {
  constructor(props: { children: ReactNode }) {
    super(props);
    this.state = { hasError: false };
  }
  static getDerivedStateFromError() { return { hasError: true }; }
  componentDidCatch(error: Error, errorInfo: ErrorInfo) { console.error("Uncaught error:", error, errorInfo); }
  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-background p-4 text-center">
          <div className="max-w-md space-y-4">
            <h1 className="text-2xl font-bold">عذراً، حدث خطأ غير متوقع</h1>
            <p className="text-muted-foreground">يرجى تحديث الصفحة أو المحاولة لاحقاً.</p>
            <button onClick={() => window.location.reload()} className="px-6 py-2 bg-brand text-white rounded-xl">تحديث الصفحة</button>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}


function AdminHamburger() {
  const [open, setOpen] = useState(false);

  const links = [
    {
      to: "/",
      label: "الرئيسية",
      description: "واجهة عزبوت",
      icon: Home,
    },
    {
      to: "/admin",
      label: "لوحة الإدارة",
      description: "إدارة المحادثات والإعدادات",
      icon: ShieldCheck,
    },
    {
      to: "/admin/login",
      label: "دخول الإدارة",
      description: "تسجيل دخول المسؤول",
      icon: LogIn,
    },
  ];

  return (
    <div className="fixed top-4 right-4 z-[70]" dir="rtl">
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        className="flex h-11 w-11 items-center justify-center rounded-2xl border border-border bg-background/95 text-foreground shadow-[0_12px_30px_rgba(15,23,42,0.14)] backdrop-blur-md transition hover:scale-105 active:scale-95"
        aria-label={open ? "إغلاق قائمة الإدارة" : "فتح قائمة الإدارة"}
        aria-expanded={open}
      >
        {open ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
      </button>

      {open && (
        <div className="mt-3 w-72 overflow-hidden rounded-3xl border border-border bg-background/95 shadow-[0_18px_45px_rgba(15,23,42,0.18)] backdrop-blur-xl animate-in fade-in-0 zoom-in-95 duration-200">
          <div className="border-b border-border px-4 py-3">
            <p className="text-sm font-bold text-foreground">قائمة الإدارة</p>
            <p className="mt-1 text-xs text-muted-foreground">
              روابط سريعة لإدارة عزبوت
            </p>
          </div>

          <nav className="p-2">
            {links.map((item) => {
              const Icon = item.icon;

              return (
                <Link
                  key={item.to}
                  to={item.to}
                  onClick={() => setOpen(false)}
                  className="flex items-center gap-3 rounded-2xl px-3 py-3 text-sm transition hover:bg-muted"
                >
                  <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl bg-brand/10 text-brand">
                    <Icon className="h-5 w-5" />
                  </span>

                  <span className="min-w-0">
                    <span className="block font-bold text-foreground">
                      {item.label}
                    </span>
                    <span className="mt-0.5 block text-xs text-muted-foreground">
                      {item.description}
                    </span>
                  </span>
                </Link>
              );
            })}
          </nav>
        </div>
      )}
    </div>
  );
}


export default function App() {
  return (
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <TooltipProvider>
          <Toaster />
          <Sonner position="top-center" richColors />
          <BrowserRouter>
            <AdminHamburger />
            <SiteProvider>
              <Routes>
                <Route path="/" element={<SitePage />} />
                <Route path="/brand-identity" element={<SitePage />} />
                <Route path="/luxury-finishing" element={<SitePage />} />
                <Route path="/uberfix" element={<SitePage />} />
                <Route path="/laban-alasfour" element={<SitePage />} />

                <Route
                  path="/admin/*"
                  element={
                    <Suspense fallback={<PageFallback />}>
                      <Admin />
                    </Suspense>
                  }
                />
                <Route
                  path="/admin/login"
                  element={
                    <Suspense fallback={<PageFallback />}>
                      <AdminLogin />
                    </Suspense>
                  }
                />

                <Route
                  path="*"
                  element={
                    <Suspense fallback={<PageFallback />}>
                      <NotFound />
                    </Suspense>
                  }
                />
              </Routes>
            </SiteProvider>
          </BrowserRouter>
        </TooltipProvider>
      </QueryClientProvider>
    </ErrorBoundary>
  );
}
