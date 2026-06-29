// components/admin/TrainingTab.tsx - قسم تدريبات البوت

import { useEffect, useState, useCallback } from 'react';
import { adminApi } from '@/lib/adminApi';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Textarea } from '@/components/ui/textarea';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { toast } from 'sonner';
import {
    Brain,
    Play,
    Trash2,
    Upload,
    FileJson,
    Loader2,
    CheckCircle,
    XCircle,
    Clock,
    FileText,
    Code2
} from 'lucide-react';
import { TrainingJob, errorMessage } from '@/types/admin';

const STATUS_CONFIG = {
    pending: { label: 'قيد الانتظار', icon: Clock, className: 'bg-yellow-500' },
    running: { label: 'جاري التدريب', icon: Loader2, className: 'bg-blue-500 animate-pulse' },
    completed: { label: 'مكتمل', icon: CheckCircle, className: 'bg-green-500' },
    failed: { label: 'فشل', icon: XCircle, className: 'bg-red-500' }
};

export default function TrainingTab() {
    const [jobs, setJobs] = useState<TrainingJob[]>([]);
    const [loading, setLoading] = useState(false);
    const [newJobOpen, setNewJobOpen] = useState(false);
    const [jobName, setJobName] = useState('');
    const [modelType, setModelType] = useState<'rasa' | 'custom'>('rasa');
    const [trainingData, setTrainingData] = useState<File | null>(null);
    const [domainData, setDomainData] = useState<string>('');
    const [configData, setConfigData] = useState<string>('');

    const loadJobs = useCallback(async () => {
        setLoading(true);
        try {
            const data = await adminApi<TrainingJob[]>('list_training_jobs', { method: 'GET' });
            setJobs(data);
        } catch (e) {
            toast.error(errorMessage(e, 'فشل تحميل مهام التدريب'));
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        loadJobs();
        const interval = setInterval(loadJobs, 5000);
        return () => clearInterval(interval);
    }, [loadJobs]);

    const startTraining = async () => {
        if (!jobName.trim()) {
            toast.error('أدخل اسم للمهمة');
            return;
        }
        if (!trainingData) {
            toast.error('يرجى رفع ملف بيانات التدريب');
            return;
        }

        const formData = new FormData();
        formData.append('name', jobName);
        formData.append('model_type', modelType);
        formData.append('file', trainingData);
        if (domainData) formData.append('domain', domainData);
        if (configData) formData.append('config', configData);

        try {
            await adminApi('start_training', {
                method: 'POST',
                body: formData,
                headers: {} // Let browser set content-type for FormData
            });
            toast.success('بدأت مهمة التدريب');
            setNewJobOpen(false);
            setJobName('');
            setTrainingData(null);
            setDomainData('');
            setConfigData('');
            loadJobs();
        } catch (e) {
            toast.error(errorMessage(e, 'فشل بدء التدريب'));
        }
    };

    const stopTraining = async (id: string) => {
        try {
            await adminApi('stop_training', { method: 'POST', body: { id } });
            toast.success('تم إيقاف التدريب');
            loadJobs();
        } catch (e) {
            toast.error(errorMessage(e));
        }
    };

    const deleteTraining = async (id: string) => {
        if (!confirm('حذف مهمة التدريب؟')) return;
        try {
            await adminApi('delete_training_job', { method: 'POST', body: { id } });
            toast.success('تم الحذف');
            loadJobs();
        } catch (e) {
            toast.error(errorMessage(e));
        }
    };

    const downloadModel = async (id: string) => {
        try {
            const response = await adminApi<{ download_url: string }>('download_model', {
                method: 'GET',
                query: { id }
            });
            if (response.download_url) {
                window.open(response.download_url, '_blank');
            }
        } catch (e) {
            toast.error(errorMessage(e, 'فشل تحميل النموذج'));
        }
    };

    const getSampleNluData = () => `version: "3.1"

nlu:
- intent: greet
  examples: |
    - مرحبا
    - السلام عليكم
    - اهلا
    - hello

- intent: goodbye
  examples: |
    - مع السلامة
    - الى اللقاء
    - وداعا

- intent: ask_price
  examples: |
    - كم سعر [المنتج](product)؟
    - سعر [الباقة](product)
    - كم تكلفة [الخدمة](product)

- intent: ask_support
  examples: |
    - احتاج مساعدة
    - الدعم الفني
    - مشكلة في النظام

- intent: provide_feedback
  examples: |
    - الخدمة ممتازة
    - سيء جدا
    - [السرعة](aspect) بطيئة

- intent: out_of_scope
  examples: |
    - ما هو الطقس اليوم؟
    - من هو رئيس مصر؟
    - اخبرني نكتة
`;

    const getSampleDomainData = `version: "3.1"

intents:
  - greet
  - goodbye
  - ask_price
  - ask_support
  - provide_feedback
  - out_of_scope

responses:
  utter_greet:
    - text: "مرحباً! كيف يمكنني مساعدتك؟"

  utter_goodbye:
    - text: "مع السلامة! نتمنى رؤيتك مرة أخرى"

  utter_ask_price:
    - text: "سعر المنتج هو 100 ريال"

  utter_ask_support:
    - text: "يمكنك التواصل مع الدعم الفني على support@example.com"

  utter_default:
    - text: "آسف، لم أفهم طلبك. هل يمكنك إعادة الصياغة؟"

session_config:
  session_expiration_time: 60
  carry_over_slots_to_new_session: true
`;

    return (
        <div className="space-y-6">
            <Card className="p-6">
                <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-2">
                        <Brain className="w-5 h-5 text-brand" />
                        <h3 className="font-bold text-lg">تدريب البوت</h3>
                    </div>
                    <Dialog open={newJobOpen} onOpenChange={setNewJobOpen}>
                        <DialogTrigger asChild>
                            <Button className="gap-2">
                                <Play className="w-4 h-4" />
                                تدريب جديد
                            </Button>
                        </DialogTrigger>
                        <DialogContent className="max-w-2xl max-h-[85vh] overflow-y-auto">
                            <DialogHeader>
                                <DialogTitle>بدء تدريب جديد</DialogTitle>
                            </DialogHeader>

                            <div className="space-y-4 py-4">
                                <div>
                                    <Label>اسم المهمة</Label>
                                    <Input
                                        value={jobName}
                                        onChange={(e) => setJobName(e.target.value)}
                                        placeholder="مثلاً: تدريب النسخة 2.0"
                                        className="mt-1.5"
                                    />
                                </div>

                                <div>
                                    <Label>نوع النموذج</Label>
                                    <Select value={modelType} onValueChange={(v) => setModelType(v as typeof modelType)}>
                                        <SelectTrigger className="mt-1.5">
                                            <SelectValue />
                                        </SelectTrigger>
                                        <SelectContent>
                                            <SelectItem value="rasa">Rasa (NLU + Stories)</SelectItem>
                                            <SelectItem value="custom">نموذج مخصص (TensorFlow/PyTorch)</SelectItem>
                                        </SelectContent>
                                    </Select>
                                </div>

                                <div>
                                    <Label>ملف بيانات التدريب</Label>
                                    <div className="mt-1.5 border-2 border-dashed border-border rounded-lg p-4 text-center hover:border-brand transition-colors">
                                        <input
                                            type="file"
                                            accept=".json,.md,.yml,.yaml,.txt"
                                            onChange={(e) => setTrainingData(e.target.files?.[0] || null)}
                                            className="hidden"
                                            id="training-file"
                                        />
                                        <label htmlFor="training-file" className="cursor-pointer">
                                            <Upload className="w-8 h-8 mx-auto text-muted-foreground mb-2" />
                                            <p className="text-sm">
                                                {trainingData ? trainingData.name : 'اختر ملف (JSON, YAML, أو MD)'}
                                            </p>
                                            <p className="text-xs text-muted-foreground mt-1">
                                                {modelType === 'rasa' ? 'ملف NLU بتنسيق Rasa' : 'ملف CSV/JSON للبيانات'}
                                            </p>
                                        </label>
                                    </div>
                                </div>

                                {modelType === 'rasa' && (
                                    <>
                                        <div>
                                            <Label>ملف Domain (اختياري)</Label>
                                            <Textarea
                                                value={domainData}
                                                onChange={(e) => setDomainData(e.target.value)}
                                                placeholder="الصق محتوى ملف domain.yml هنا"
                                                rows={6}
                                                className="mt-1.5 font-mono text-sm"
                                            />
                                            <Button
                                                type="button"
                                                variant="ghost"
                                                size="sm"
                                                onClick={() => setDomainData(getSampleDomainData)}
                                                className="mt-2"
                                            >
                                                <FileJson className="w-3 h-3 ml-1" />
                                                تحميل نموذج
                                            </Button>
                                        </div>

                                        <div>
                                            <Label>ملف Config (اختياري)</Label>
                                            <Textarea
                                                value={configData}
                                                onChange={(e) => setConfigData(e.target.value)}
                                                placeholder="إعدادات التدريب (YAML)"
                                                rows={4}
                                                className="mt-1.5 font-mono text-sm"
                                            />
                                        </div>
                                    </>
                                )}

                                <div className="bg-muted/30 rounded-lg p-3">
                                    <div className="flex items-center gap-2 text-sm font-bold mb-2">
                                        <Code2 className="w-4 h-4" />
                                        نموذج بيانات NLU
                                    </div>
                                    <pre className="text-xs overflow-x-auto bg-background p-2 rounded">
                                        {getSampleNluData().slice(0, 500)}...
                                    </pre>
                                </div>
                            </div>

                            <div className="flex justify-end gap-2">
                                <Button variant="outline" onClick={() => setNewJobOpen(false)}>إلغاء</Button>
                                <Button onClick={startTraining} className="bg-brand hover:bg-brand-glow">
                                    بدء التدريب
                                </Button>
                            </div>
                        </DialogContent>
                    </Dialog>
                </div>

                <div className="space-y-3">
                    {loading && jobs.length === 0 ? (
                        <div className="text-center py-12">
                            <Loader2 className="w-6 h-6 animate-spin mx-auto text-muted-foreground" />
                        </div>
                    ) : jobs.length === 0 ? (
                        <p className="text-sm text-muted-foreground text-center py-8">
                            لا توجد مهام تدريب. ابدأ تدريباً جديداً لتحسين أداء البوت
                        </p>
                    ) : jobs.map((job) => {
                        const StatusIcon = STATUS_CONFIG[job.status]?.icon || Clock;
                        return (
                            <div key={job.id} className="border border-border rounded-lg p-4">
                                <div className="flex items-center justify-between flex-wrap gap-2 mb-3">
                                    <div className="flex items-center gap-3">
                                        <StatusIcon className={`w-5 h-5 ${STATUS_CONFIG[job.status]?.className}`} />
                                        <div>
                                            <div className="font-semibold">{job.name}</div>
                                            <div className="text-xs text-muted-foreground">
                                                {job.model_type === 'rasa' ? 'Rasa NLU' : 'نموذج مخصص'} ·
                                                {new Date(job.created_at).toLocaleString('ar-EG')}
                                            </div>
                                        </div>
                                    </div>
                                    <div className="flex gap-2">
                                        {job.status === 'running' && (
                                            <Button size="sm" variant="outline" onClick={() => stopTraining(job.id)}>
                                                إيقاف
                                            </Button>
                                        )}
                                        {job.status === 'completed' && (
                                            <Button size="sm" variant="outline" onClick={() => downloadModel(job.id)}>
                                                تحميل النموذج
                                            </Button>
                                        )}
                                        <Button size="sm" variant="ghost" onClick={() => deleteTraining(job.id)} className="text-destructive">
                                            <Trash2 className="w-4 h-4" />
                                        </Button>
                                    </div>
                                </div>

                                {job.status === 'running' && (
                                    <div className="mt-3">
                                        <Progress value={Math.random() * 100} className="h-2" />
                                    </div>
                                )}

                                {job.status === 'completed' && job.stats && (
                                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-3 text-sm">
                                        <div className="bg-muted/30 rounded-lg p-2 text-center">
                                            <div className="text-muted-foreground text-xs">Epochs</div>
                                            <div className="font-bold">{job.stats.epochs}</div>
                                        </div>
                                        {job.stats.accuracy && (
                                            <div className="bg-muted/30 rounded-lg p-2 text-center">
                                                <div className="text-muted-foreground text-xs">الدقة</div>
                                                <div className="font-bold text-green-600">
                                                    {(job.stats.accuracy * 100).toFixed(1)}%
                                                </div>
                                            </div>
                                        )}
                                        {job.stats.loss && (
                                            <div className="bg-muted/30 rounded-lg p-2 text-center">
                                                <div className="text-muted-foreground text-xs">الخسارة</div>
                                                <div className="font-bold">{job.stats.loss.toFixed(4)}</div>
                                            </div>
                                        )}
                                        <div className="bg-muted/30 rounded-lg p-2 text-center">
                                            <div className="text-muted-foreground text-xs">الملفات</div>
                                            <div className="font-bold">{job.files.length}</div>
                                        </div>
                                    </div>
                                )}

                                {job.error_message && (
                                    <div className="mt-3 p-2 bg-red-50 dark:bg-red-950/20 rounded text-red-600 text-sm">
                                        {job.error_message}
                                    </div>
                                )}
                            </div>
                        );
                    })}
                </div>
            </Card>
        </div>
    );
}