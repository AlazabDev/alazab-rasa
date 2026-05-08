import { useEffect, useState } from "react";
import { adminApi } from "@/lib/adminApi";
import { Card } from "@/components/ui/card";
import { MessageSquare, Users, Calendar, Paperclip, ArrowUpRight, Zap, Shield, Globe } from "lucide-react";
import { AdminStats } from "@/types/admin";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";

export default function StatsTab() {
  const [stats, setStats] = useState<AdminStats | null>(null);

  useEffect(() => {
    adminApi<AdminStats>("stats", { method: "GET" }).then(setStats).catch(() => {});
  }, []);

  const items = [
    { label: "إجمالي المحادثات", value: stats?.conversations ?? "0", icon: Users, color: "text-blue-500", bg: "bg-blue-500/10" },
    { label: "إجمالي الرسائل", value: stats?.messages ?? "0", icon: MessageSquare, color: "text-brand", bg: "bg-brand/10" },
    { label: "الملفات المرفوعة", value: stats?.uploads ?? "0", icon: Paperclip, color: "text-amber-500", bg: "bg-amber-500/10" },
    { label: "محادثات اليوم", value: stats?.today ?? "0", icon: Calendar, color: "text-green-500", bg: "bg-green-500/10" },
  ];

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {items.map((it) => (
          <Card key={it.label} className="p-6 overflow-hidden relative group border-none bg-card shadow-sm hover:shadow-md transition-all">
            <div className="flex items-center justify-between relative z-10">
              <div>
                <p className="text-sm text-muted-foreground font-medium">{it.label}</p>
                <p className="text-3xl font-bold mt-2 text-foreground">{it.value}</p>
              </div>
              <div className={`w-12 h-12 rounded-2xl ${it.bg} flex items-center justify-center`}>
                <it.icon className={`w-6 h-6 ${it.color}`} />
              </div>
            </div>
            <div className="absolute -bottom-2 -right-2 w-24 h-24 bg-gradient-to-br from-transparent to-muted opacity-50 group-hover:scale-110 transition-transform rounded-full" />
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="p-6 lg:col-span-2">
          <div className="flex items-center justify-between mb-6">
            <h3 className="font-bold text-lg flex items-center gap-2">
              <Zap className="w-5 h-5 text-brand" />
              إجراءات سريعة
            </h3>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <Button variant="outline" className="h-auto py-4 justify-start gap-4 hover:border-brand hover:bg-brand/5 group">
              <div className="w-10 h-10 rounded-lg bg-muted flex items-center justify-center group-hover:bg-brand/10">
                <Globe className="w-5 h-5 text-muted-foreground group-hover:text-brand" />
              </div>
              <div className="text-right">
                <div className="font-semibold">تحديث الموقع</div>
                <div className="text-xs text-muted-foreground">مزامنة إعدادات البوت مع الموقع</div>
              </div>
            </Button>
            <Button variant="outline" className="h-auto py-4 justify-start gap-4 hover:border-brand hover:bg-brand/5 group">
              <div className="w-10 h-10 rounded-lg bg-muted flex items-center justify-center group-hover:bg-brand/10">
                <Shield className="w-5 h-5 text-muted-foreground group-hover:text-brand" />
              </div>
              <div className="text-right">
                <div className="font-semibold">فحص الأمان</div>
                <div className="text-xs text-muted-foreground">مراجعة سجلات الدخول المشبوهة</div>
              </div>
            </Button>
          </div>
        </Card>

        <Card className="p-6 overflow-hidden">
          <h3 className="font-bold mb-4 flex items-center gap-2">
            <ArrowUpRight className="w-5 h-5 text-brand" />
            رابط التضمين
          </h3>
          <p className="text-sm text-muted-foreground mb-4">
            استخدم هذا الكود لتضمين البوت في أي موقع إلكتروني بشكل احترافي.
          </p>
          <div className="relative group">
            <pre className="bg-muted p-4 rounded-xl text-xs overflow-x-auto border border-border group-hover:border-brand transition-colors" dir="ltr">{`<iframe
  src="${window.location.origin}"
  style="position:fixed;bottom:20px;right:20px;width:400px;height:600px;border-radius:16px;box-shadow:0 10px 25px rgba(0,0,0,0.1);z-index:9999;"
  allow="microphone"
></iframe>`}</pre>
            <Button size="sm" variant="ghost" className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity" onClick={() => {
              navigator.clipboard.writeText(`<iframe src="${window.location.origin}" style="position:fixed;bottom:20px;right:20px;width:400px;height:600px;border-radius:16px;box-shadow:0 10px 25px rgba(0,0,0,0.1);z-index:9999;" allow="microphone"></iframe>`);
              toast.success("تم نسخ الكود");
            }}>
              نسخ
            </Button>
          </div>
        </Card>
      </div>
    </div>
  );
}
