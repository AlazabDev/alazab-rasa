import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { adminApi, adminToken } from "@/lib/adminApi";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { LogOut, Settings, Plug, MessageSquare, FileText, BarChart3, Paperclip, BookOpen, Brain, ShieldCheck } from "lucide-react";
import azabotLogo from "@/assets/azabot-logo.png";
import { toast } from "sonner";
import KnowledgeBaseTab from "@/components/admin/KnowledgeBaseTab";
import GeneralTab from "@/components/admin/GeneralTab";
import IntegrationsTab from "@/components/admin/IntegrationsTab";
import TrainingTab from "@/components/admin/TrainingTab";
import ConversationsTab from "@/components/admin/ConversationsTab";
import UploadsTab from "@/components/admin/UploadsTab";
import LogsTab from "@/components/admin/LogsTab";
import StatsTab from "@/components/admin/StatsTab";
import SecurityTab from "@/components/admin/SecurityTab";


export default function Admin() {
  const nav = useNavigate();
  const [ready, setReady] = useState(false);

  useEffect(() => {
    if (!adminToken.get()) {
      nav("/admin/login", { replace: true });
      return;
    }
    adminApi("stats", { method: "GET" })
      .then(() => setReady(true))
      .catch(() => nav("/admin/login", { replace: true }));
  }, [nav]);

  const logout = () => {
    adminToken.clear();
    toast.success("تم تسجيل الخروج");
    nav("/admin/login");
  };

  if (!ready) return <div className="min-h-screen bg-background" />;

  return (
    <div dir="rtl" className="min-h-screen bg-background">
      <header className="border-b border-border bg-card">
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-brand flex items-center justify-center">
              <img src={azabotLogo} alt="AzaBot" className="w-7 h-7" />
            </div>
            <div>
              <h1 className="font-bold text-foreground">لوحة تحكم AzaBot</h1>
              <p className="text-xs text-muted-foreground">إدارة البوت والتكاملات</p>
            </div>
          </div>
          <Button variant="ghost" onClick={logout} className="gap-2">
            <LogOut className="w-4 h-4" /> خروج
          </Button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-6">
        <Tabs defaultValue="stats" className="w-full">
          <TabsList className="flex flex-wrap h-auto gap-1 bg-transparent border-b border-border rounded-none mb-8 p-0">
            <TabsTrigger value="stats" className="rounded-none border-b-2 border-transparent data-[state=active]:border-brand data-[state=active]:bg-transparent gap-2 px-4 py-3">
              <BarChart3 className="w-4 h-4" /> نظرة عامة
            </TabsTrigger>
            <TabsTrigger value="knowledge" className="rounded-none border-b-2 border-transparent data-[state=active]:border-brand data-[state=active]:bg-transparent gap-2 px-4 py-3">
              <BookOpen className="w-4 h-4" /> المعرفة
            </TabsTrigger>
            <TabsTrigger value="training" className="rounded-none border-b-2 border-transparent data-[state=active]:border-brand data-[state=active]:bg-transparent gap-2 px-4 py-3">
              <Brain className="w-4 h-4" /> التدريب
            </TabsTrigger>
            <TabsTrigger value="conversations" className="rounded-none border-b-2 border-transparent data-[state=active]:border-brand data-[state=active]:bg-transparent gap-2 px-4 py-3">
              <MessageSquare className="w-4 h-4" /> المحادثات
            </TabsTrigger>
            <TabsTrigger value="integrations" className="rounded-none border-b-2 border-transparent data-[state=active]:border-brand data-[state=active]:bg-transparent gap-2 px-4 py-3">
              <Plug className="w-4 h-4" /> التكاملات
            </TabsTrigger>
            <TabsTrigger value="uploads" className="rounded-none border-b-2 border-transparent data-[state=active]:border-brand data-[state=active]:bg-transparent gap-2 px-4 py-3">
              <Paperclip className="w-4 h-4" /> الملفات
            </TabsTrigger>
            <TabsTrigger value="general" className="rounded-none border-b-2 border-transparent data-[state=active]:border-brand data-[state=active]:bg-transparent gap-2 px-4 py-3">
              <Settings className="w-4 h-4" /> الإعدادات
            </TabsTrigger>
            <TabsTrigger value="security" className="rounded-none border-b-2 border-transparent data-[state=active]:border-brand data-[state=active]:bg-transparent gap-2 px-4 py-3">
              <ShieldCheck className="w-4 h-4" /> الأمان
            </TabsTrigger>
            <TabsTrigger value="logs" className="rounded-none border-b-2 border-transparent data-[state=active]:border-brand data-[state=active]:bg-transparent gap-2 px-4 py-3">
              <FileText className="w-4 h-4" /> السجلات
            </TabsTrigger>
          </TabsList>

          <TabsContent value="stats" className="mt-0 focus-visible:outline-none"><StatsTab /></TabsContent>
          <TabsContent value="knowledge" className="mt-0 focus-visible:outline-none"><KnowledgeBaseTab /></TabsContent>
          <TabsContent value="training" className="mt-0 focus-visible:outline-none"><TrainingTab /></TabsContent>
          <TabsContent value="conversations" className="mt-0 focus-visible:outline-none"><ConversationsTab /></TabsContent>
          <TabsContent value="integrations" className="mt-0 focus-visible:outline-none"><IntegrationsTab /></TabsContent>
          <TabsContent value="uploads" className="mt-0 focus-visible:outline-none"><UploadsTab /></TabsContent>
          <TabsContent value="general" className="mt-0 focus-visible:outline-none"><GeneralTab /></TabsContent>
          <TabsContent value="security" className="mt-0 focus-visible:outline-none"><SecurityTab /></TabsContent>
          <TabsContent value="logs" className="mt-0 focus-visible:outline-none"><LogsTab /></TabsContent>
        </Tabs>
      </main>
    </div>
  );
}
