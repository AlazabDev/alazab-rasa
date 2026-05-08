// components/admin/IntegrationsTab.tsx

import { useEffect, useState } from "react";
import { adminApi } from "@/lib/adminApi";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Card } from "@/components/ui/card";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Textarea } from "@/components/ui/textarea";
import { toast } from "sonner";
import {
  Plus, Trash2, TestTube, Webhook, Send, MessageCircle, Phone,
  Slack, Disc, Mail, Loader2, Zap, Settings, ExternalLink
} from "lucide-react";
import { AdminIntegration, IntegrationType, errorMessage, getIntegrationTypeLabel } from "@/types/admin";

const TYPES: Array<{ id: IntegrationType; label: string; icon: React.ComponentType<{ className?: string }>; desc: string }> = [
  { id: "webhook", label: "Webhook عام", icon: Webhook, desc: "أرسل لأي URL — يعمل مع n8n/Make/Zapier" },
  { id: "telegram", label: "Telegram", icon: Send, desc: "أرسل لقناة/بوت تيليجرام" },
  { id: "whatsapp", label: "WhatsApp Business", icon: MessageCircle, desc: "Meta Cloud API" },
  { id: "twilio", label: "Twilio (SMS/WhatsApp)", icon: Phone, desc: "رسائل SMS أو WhatsApp عبر Twilio" },
  { id: "slack", label: "Slack", icon: Slack, desc: "إرسال إلى قناة Slack" },
  { id: "discord", label: "Discord", icon: Disc, desc: "إرسال إلى خادم Discord" },
  { id: "email", label: "البريد الإلكتروني", icon: Mail, desc: "إرسال عبر SMTP" },
];

const EVENTS = [
  { id: "conversation.started", label: "بدء محادثة جديدة" },
  { id: "message.created", label: "كل رسالة جديدة" },
  { id: "message.user", label: "رسالة زائر جديدة" },
  { id: "message.bot", label: "رد البوت" },
  { id: "feedback.received", label: "تقييم المستخدم" },
];

const getDefaultConfig = (type: IntegrationType): Record<string, unknown> => {
  switch (type) {
    case "webhook":
      return { url: "", secret: "", method: "POST", retry_count: 3, timeout_seconds: 30 };
    case "telegram":
      return { bot_token: "", chat_id: "", parse_mode: "HTML", disable_notification: false };
    case "whatsapp":
      return { phone_number_id: "", access_token: "", recipient: "" };
    case "twilio":
      return { account_sid: "", auth_token: "", from: "", to: "" };
    case "slack":
      return { webhook_url: "", channel: "", username: "AzaBot", icon_emoji: ":robot:" };
    case "discord":
      return { webhook_url: "", username: "AzaBot" };
    case "email":
      return { smtp_host: "smtp.gmail.com", smtp_port: 587, smtp_user: "", smtp_password: "", from_email: "", to_emails: [], use_tls: true };
    default:
      return {};
  }
};

export default function IntegrationsTab() {
  const [list, setList] = useState<AdminIntegration[]>([]);
  const [editing, setEditing] = useState<AdminIntegration | null>(null);
  const [open, setOpen] = useState(false);
  const [testingId, setTestingId] = useState<string | null>(null);

  const load = () => adminApi<AdminIntegration[]>("list_integrations", { method: "GET" })
    .then(setList)
    .catch((e: unknown) => toast.error(errorMessage(e)));

  useEffect(() => { load(); }, []);

  const startNew = (type: IntegrationType) => {
    setEditing({
      type,
      name: TYPES.find((t) => t.id === type)?.label || "",
      enabled: true,
      config: getDefaultConfig(type) as any,
      events: ["message.created"]
    });
    setOpen(true);
  };

  const startEdit = (it: AdminIntegration) => { setEditing({ ...it, config: { ...it.config } }); setOpen(true); };

  const save = async () => {
    if (!editing) return;
    try {
      await adminApi("save_integration", { body: editing });
      toast.success("تم الحفظ");
      setOpen(false); setEditing(null); load();
    } catch (e: unknown) { toast.error(errorMessage(e)); }
  };

  const del = async (id: string) => {
    if (!confirm("حذف هذا التكامل؟")) return;
    await adminApi("delete_integration", { body: { id } });
    toast.success("تم الحذف"); load();
  };

  const test = async (id: string) => {
    setTestingId(id);
    toast.loading("جارٍ الاختبار...", { id: "test" });
    try {
      const r = await adminApi<{ status: string; statusCode?: number; errorMessage?: string }>("test_integration", { body: { id } });
      toast.dismiss("test");
      if (r.status === "success") toast.success(`نجح الاختبار (${r.statusCode})`);
      else toast.error(`فشل: ${r.errorMessage || r.statusCode}`);
    } catch (e: unknown) {
      toast.dismiss("test");
      toast.error(errorMessage(e));
    } finally {
      setTestingId(null);
    }
  };

  const updateConfig = (key: string, value: unknown) => {
    if (!editing) return;
    setEditing({
      ...editing,
      config: { ...editing.config, [key]: value }
    });
  };

  const getConfigValue = (key: string): string => {
    if (!editing) return "";
    const val = (editing.config as any)[key];
    if (typeof val === 'string') return val;
    if (Array.isArray(val)) return val.join(", ");
    if (typeof val === 'boolean') return val ? "true" : "false";
    if (val === undefined || val === null) return "";
    return String(val);
  };

  return (
    <div className="space-y-4">
      <Card className="p-6">
        <h3 className="font-bold text-lg mb-4">إضافة تكامل جديد</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {TYPES.map((t) => (
            <button key={t.id} onClick={() => startNew(t.id)}
              className="flex items-start gap-3 p-4 rounded-xl border border-border hover:border-brand hover:bg-accent transition-smooth text-right">
              <t.icon className="w-6 h-6 text-brand shrink-0" />
              <div className="flex-1">
                <div className="font-semibold text-foreground">{t.label}</div>
                <div className="text-xs text-muted-foreground mt-0.5">{t.desc}</div>
              </div>
            </button>
          ))}
        </div>
      </Card>

      <Card className="p-6">
        <h3 className="font-bold text-lg mb-4">التكاملات المُفعّلة ({list.length})</h3>
        {list.length === 0 ? (
          <p className="text-sm text-muted-foreground text-center py-8">لا توجد تكاملات بعد</p>
        ) : (
          <div className="space-y-2">
            {list.map((it) => {
              const T = TYPES.find((t) => t.id === it.type);
              const Icon = T?.icon || Webhook;
              return (
                <div key={it.id} className="flex items-center gap-3 p-3 rounded-lg border border-border">
                  <Icon className="w-5 h-5 text-brand shrink-0" />
                  <div className="flex-1 min-w-0">
                    <div className="font-semibold text-foreground truncate">{it.name}</div>
                    <div className="text-xs text-muted-foreground">{getIntegrationTypeLabel(it.type)} · {it.events?.length || 0} حدث</div>
                  </div>
                  <Switch checked={it.enabled} onCheckedChange={async (v) => {
                    await adminApi("save_integration", { body: { ...it, enabled: v } }); load();
                  }} />
                  <Button
                    size="icon"
                    variant="ghost"
                    onClick={() => it.id && test(it.id)}
                    disabled={!it.id || testingId === it.id}
                    title="اختبار"
                  >
                    {testingId === it.id ?
                      <Loader2 className="w-4 h-4 animate-spin" /> :
                      <TestTube className="w-4 h-4" />
                    }
                  </Button>
                  <Button size="icon" variant="ghost" onClick={() => startEdit(it)}>
                    <Settings className="w-4 h-4" />
                  </Button>
                  <Button size="icon" variant="ghost" onClick={() => it.id && del(it.id)} disabled={!it.id} className="text-destructive">
                    <Trash2 className="w-4 h-4" />
                  </Button>
                </div>
              );
            })}
          </div>
        )}
      </Card>

      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent dir="rtl" className="max-w-2xl max-h-[85vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>{editing?.id ? "تعديل" : "إضافة"} تكامل {TYPES.find((t) => t.id === editing?.type)?.label}</DialogTitle>
          </DialogHeader>
          {editing && (
            <div className="space-y-4">
              <div>
                <Label>اسم التكامل</Label>
                <Input value={editing.name} onChange={(e) => setEditing({ ...editing, name: e.target.value })} className="mt-1.5" />
              </div>

              <Tabs defaultValue="config" className="w-full">
                <TabsList className="grid w-full grid-cols-2">
                  <TabsTrigger value="config">الإعدادات</TabsTrigger>
                  <TabsTrigger value="events">الأحداث</TabsTrigger>
                </TabsList>

                <TabsContent value="config" className="space-y-4 mt-4">
                  {/* Webhook Config */}
                  {editing.type === "webhook" && (
                    <>
                      <div>
                        <Label>URL</Label>
                        <Input dir="ltr" value={getConfigValue("url")}
                          onChange={(e) => updateConfig("url", e.target.value)}
                          placeholder="https://example.com/webhook" className="mt-1.5" />
                      </div>
                      <div>
                        <Label>Secret (اختياري)</Label>
                        <Input dir="ltr" value={getConfigValue("secret")}
                          onChange={(e) => updateConfig("secret", e.target.value)}
                          className="mt-1.5" />
                      </div>
                      <div className="grid grid-cols-2 gap-3">
                        <div>
                          <Label>Method</Label>
                          <Select value={getConfigValue("method") || "POST"} onValueChange={(v) => updateConfig("method", v)}>
                            <SelectTrigger className="mt-1.5"><SelectValue /></SelectTrigger>
                            <SelectContent>
                              <SelectItem value="POST">POST</SelectItem>
                              <SelectItem value="PUT">PUT</SelectItem>
                              <SelectItem value="PATCH">PATCH</SelectItem>
                            </SelectContent>
                          </Select>
                        </div>
                        <div>
                          <Label>Timeout (ثانية)</Label>
                          <Input type="number" value={getConfigValue("timeout_seconds") || 30}
                            onChange={(e) => updateConfig("timeout_seconds", parseInt(e.target.value))}
                            className="mt-1.5" />
                        </div>
                      </div>
                      <div>
                        <Label>Headers (JSON)</Label>
                        <Textarea
                          value={(() => {
                            const headers = (editing.config as any).headers;
                            if (typeof headers === 'object' && headers !== null) {
                              return JSON.stringify(headers, null, 2);
                            }
                            return "{}";
                          })()}
                          onChange={(e) => {
                            try {
                              const headers = JSON.parse(e.target.value);
                              updateConfig("headers", headers);
                            } catch { }
                          }}
                          rows={4}
                          className="mt-1.5 font-mono text-sm"
                          placeholder='{"X-Custom": "value"}'
                        />
                      </div>
                    </>
                  )}

                  {/* Telegram Config */}
                  {editing.type === "telegram" && (
                    <>
                      <div>
                        <Label>Bot Token</Label>
                        <Input dir="ltr" type="password" value={getConfigValue("bot_token")}
                          onChange={(e) => updateConfig("bot_token", e.target.value)}
                          placeholder="123456:ABC-..." className="mt-1.5" />
                      </div>
                      <div>
                        <Label>Chat ID</Label>
                        <Input dir="ltr" value={getConfigValue("chat_id")}
                          onChange={(e) => updateConfig("chat_id", e.target.value)}
                          placeholder="-1001234567890" className="mt-1.5" />
                        <p className="text-xs text-muted-foreground mt-1">
                          <a href="https://api.telegram.org/bot&lt;TOKEN&gt;/getUpdates" target="_blank" rel="noopener noreferrer" className="text-brand inline-flex items-center gap-1">
                            احصل على Chat ID <ExternalLink className="w-3 h-3" />
                          </a>
                        </p>
                      </div>
                      <div>
                        <Label>Parse Mode</Label>
                        <Select value={getConfigValue("parse_mode") || "HTML"} onValueChange={(v) => updateConfig("parse_mode", v)}>
                          <SelectTrigger className="mt-1.5"><SelectValue /></SelectTrigger>
                          <SelectContent>
                            <SelectItem value="HTML">HTML</SelectItem>
                            <SelectItem value="MarkdownV2">MarkdownV2</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                    </>
                  )}

                  {/* WhatsApp Config */}
                  {editing.type === "whatsapp" && (
                    <>
                      <div>
                        <Label>Phone Number ID</Label>
                        <Input dir="ltr" value={getConfigValue("phone_number_id")}
                          onChange={(e) => updateConfig("phone_number_id", e.target.value)}
                          className="mt-1.5" />
                      </div>
                      <div>
                        <Label>Access Token</Label>
                        <Input dir="ltr" type="password" value={getConfigValue("access_token")}
                          onChange={(e) => updateConfig("access_token", e.target.value)}
                          className="mt-1.5" />
                      </div>
                      <div>
                        <Label>Recipient Number</Label>
                        <Input dir="ltr" value={getConfigValue("recipient")}
                          onChange={(e) => updateConfig("recipient", e.target.value)}
                          placeholder="966501234567" className="mt-1.5" />
                      </div>
                    </>
                  )}

                  {/* Twilio Config */}
                  {editing.type === "twilio" && (
                    <>
                      <div>
                        <Label>Account SID</Label>
                        <Input dir="ltr" value={getConfigValue("account_sid")}
                          onChange={(e) => updateConfig("account_sid", e.target.value)}
                          className="mt-1.5" />
                      </div>
                      <div>
                        <Label>Auth Token</Label>
                        <Input dir="ltr" type="password" value={getConfigValue("auth_token")}
                          onChange={(e) => updateConfig("auth_token", e.target.value)}
                          className="mt-1.5" />
                      </div>
                      <div className="grid grid-cols-2 gap-3">
                        <div>
                          <Label>From</Label>
                          <Input dir="ltr" value={getConfigValue("from")}
                            onChange={(e) => updateConfig("from", e.target.value)}
                            placeholder="+15017122661" className="mt-1.5" />
                        </div>
                        <div>
                          <Label>To</Label>
                          <Input dir="ltr" value={getConfigValue("to")}
                            onChange={(e) => updateConfig("to", e.target.value)}
                            placeholder="+966501234567" className="mt-1.5" />
                        </div>
                      </div>
                    </>
                  )}

                  {/* Slack Config */}
                  {editing.type === "slack" && (
                    <>
                      <div>
                        <Label>Webhook URL</Label>
                        <Input dir="ltr" value={getConfigValue("webhook_url")}
                          onChange={(e) => updateConfig("webhook_url", e.target.value)}
                          placeholder="https://hooks.slack.com/services/..." className="mt-1.5" />
                      </div>
                      <div>
                        <Label>Channel (اختياري)</Label>
                        <Input dir="ltr" value={getConfigValue("channel")}
                          onChange={(e) => updateConfig("channel", e.target.value)}
                          placeholder="#general" className="mt-1.5" />
                      </div>
                      <div>
                        <Label>Username</Label>
                        <Input value={getConfigValue("username") || "AzaBot"}
                          onChange={(e) => updateConfig("username", e.target.value)}
                          className="mt-1.5" />
                      </div>
                    </>
                  )}

                  {/* Discord Config */}
                  {editing.type === "discord" && (
                    <>
                      <div>
                        <Label>Webhook URL</Label>
                        <Input dir="ltr" value={getConfigValue("webhook_url")}
                          onChange={(e) => updateConfig("webhook_url", e.target.value)}
                          placeholder="https://discord.com/api/webhooks/..." className="mt-1.5" />
                      </div>
                      <div>
                        <Label>Username</Label>
                        <Input value={getConfigValue("username") || "AzaBot"}
                          onChange={(e) => updateConfig("username", e.target.value)}
                          className="mt-1.5" />
                      </div>
                    </>
                  )}

                  {/* Email Config */}
                  {editing.type === "email" && (
                    <>
                      <div className="grid grid-cols-2 gap-3">
                        <div>
                          <Label>SMTP Host</Label>
                          <Input dir="ltr" value={getConfigValue("smtp_host")}
                            onChange={(e) => updateConfig("smtp_host", e.target.value)}
                            placeholder="smtp.gmail.com" className="mt-1.5" />
                        </div>
                        <div>
                          <Label>SMTP Port</Label>
                          <Input type="number" value={getConfigValue("smtp_port") || 587}
                            onChange={(e) => updateConfig("smtp_port", parseInt(e.target.value))}
                            className="mt-1.5" />
                        </div>
                      </div>
                      <div>
                        <Label>SMTP User</Label>
                        <Input dir="ltr" value={getConfigValue("smtp_user")}
                          onChange={(e) => updateConfig("smtp_user", e.target.value)}
                          className="mt-1.5" />
                      </div>
                      <div>
                        <Label>SMTP Password</Label>
                        <Input dir="ltr" type="password" value={getConfigValue("smtp_password")}
                          onChange={(e) => updateConfig("smtp_password", e.target.value)}
                          className="mt-1.5" />
                      </div>
                      <div className="grid grid-cols-2 gap-3">
                        <div>
                          <Label>From Email</Label>
                          <Input dir="ltr" value={getConfigValue("from_email")}
                            onChange={(e) => updateConfig("from_email", e.target.value)}
                            className="mt-1.5" />
                        </div>
                        <div>
                          <Label>To Emails</Label>
                          <Input dir="ltr" value={getConfigValue("to_emails")}
                            onChange={(e) => updateConfig("to_emails", e.target.value.split(",").map(s => s.trim()))}
                            placeholder="email1@example.com, email2@example.com"
                            className="mt-1.5" />
                        </div>
                      </div>
                      <div className="flex items-center justify-between">
                        <Label>Use TLS</Label>
                        <Switch checked={getConfigValue("use_tls") !== "false"}
                          onCheckedChange={(v) => updateConfig("use_tls", v)} />
                      </div>
                    </>
                  )}
                </TabsContent>

                <TabsContent value="events" className="space-y-3 mt-4">
                  {EVENTS.map((ev) => (
                    <label key={ev.id} className="flex items-center gap-2 cursor-pointer p-2 rounded hover:bg-muted/30">
                      <input
                        type="checkbox"
                        checked={(editing.events || []).includes(ev.id)}
                        onChange={(e) => {
                          const cur = new Set(editing.events || []);
                          if (e.target.checked) cur.add(ev.id);
                          else cur.delete(ev.id);
                          setEditing({ ...editing, events: [...cur] });
                        }}
                      />
                      <span className="text-sm">{ev.label}</span>
                    </label>
                  ))}
                </TabsContent>
              </Tabs>

              <div className="flex justify-end gap-2 pt-4 border-t">
                <Button variant="outline" onClick={() => setOpen(false)}>إلغاء</Button>
                <Button onClick={save} className="bg-brand hover:bg-brand-glow text-brand-foreground gap-2">
                  <Zap className="w-4 h-4" />
                  حفظ
                </Button>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}