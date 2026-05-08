// components/admin/KnowledgeBaseTab.tsx - إدارة قاعدة المعرفة

import { useEffect, useState, useCallback } from 'react';
import { adminApi } from '@/lib/adminApi';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Progress } from '@/components/ui/progress';
import { Textarea } from '@/components/ui/textarea';
import { toast } from 'sonner';
import {
    Database,
    Library,
    Upload,
    Trash2,
    Search,
    FileText,
    Loader2,
    CheckCircle,
    XCircle,
    Plus,
    FolderOpen
} from 'lucide-react';
import { KnowledgeBaseDocument, KnowledgeBaseCollection, errorMessage } from '@/types/admin';

export default function KnowledgeBaseTab() {
    const [collections, setCollections] = useState<KnowledgeBaseCollection[]>([]);
    const [documents, setDocuments] = useState<KnowledgeBaseDocument[]>([]);
    const [selectedCollection, setSelectedCollection] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [searchQuery, setSearchQuery] = useState('');
    const [uploadOpen, setUploadOpen] = useState(false);
    const [newCollectionOpen, setNewCollectionOpen] = useState(false);
    const [newCollectionName, setNewCollectionName] = useState('');
    const [newCollectionDesc, setNewCollectionDesc] = useState('');

    // Upload state
    const [uploadFiles, setUploadFiles] = useState<File[]>([]);
    const [uploadUrls, setUploadUrls] = useState<string[]>([]);
    const [uploadType, setUploadType] = useState<'files' | 'urls'>('files');

    const loadCollections = useCallback(async () => {
        try {
            const data = await adminApi<KnowledgeBaseCollection[]>('list_kb_collections', { method: 'GET' });
            setCollections(data);
        } catch (e) {
            toast.error(errorMessage(e, 'فشل تحميل المجموعات'));
        }
    }, []);

    const loadDocuments = useCallback(async () => {
        if (!selectedCollection) return;
        setLoading(true);
        try {
            const query: Record<string, string> = { collection_id: selectedCollection };
            if (searchQuery) query.q = searchQuery;
            const data = await adminApi<KnowledgeBaseDocument[]>('list_kb_documents', { method: 'GET', query });
            setDocuments(data);
        } catch (e) {
            toast.error(errorMessage(e, 'فشل تحميل المستندات'));
        } finally {
            setLoading(false);
        }
    }, [selectedCollection, searchQuery]);

    useEffect(() => {
        loadCollections();
    }, [loadCollections]);

    useEffect(() => {
        if (selectedCollection) {
            loadDocuments();
        }
    }, [selectedCollection, loadDocuments]);

    const createCollection = async () => {
        if (!newCollectionName.trim()) {
            toast.error('أدخل اسم المجموعة');
            return;
        }
        try {
            await adminApi('create_kb_collection', {
                method: 'POST',
                body: { name: newCollectionName, description: newCollectionDesc }
            });
            toast.success('تم إنشاء المجموعة');
            setNewCollectionOpen(false);
            setNewCollectionName('');
            setNewCollectionDesc('');
            loadCollections();
        } catch (e) {
            toast.error(errorMessage(e));
        }
    };

    const uploadDocuments = async () => {
        const formData = new FormData();
        if (uploadType === 'files') {
            uploadFiles.forEach(file => formData.append('files', file));
        } else {
            formData.append('urls', JSON.stringify(uploadUrls.filter(u => u.trim())));
        }
        formData.append('collection_id', selectedCollection || 'default');

        try {
            await adminApi('upload_kb_documents', {
                method: 'POST',
                body: formData,
                headers: {}
            });
            toast.success('تم رفع المستندات وجاري المعالجة');
            setUploadOpen(false);
            setUploadFiles([]);
            setUploadUrls([]);
            loadDocuments();
        } catch (e) {
            toast.error(errorMessage(e, 'فشل رفع المستندات'));
        }
    };

    const deleteDocument = async (id: string) => {
        if (!confirm('حذف هذا المستند؟')) return;
        try {
            await adminApi('delete_kb_document', { method: 'POST', body: { id } });
            toast.success('تم الحذف');
            loadDocuments();
        } catch (e) {
            toast.error(errorMessage(e));
        }
    };

    const deleteCollection = async (id: string, name: string) => {
        if (!confirm(`حذف مجموعة "${name}" وجميع مستنداتها؟`)) return;
        try {
            await adminApi('delete_kb_collection', { method: 'POST', body: { id } });
            toast.success('تم حذف المجموعة');
            if (selectedCollection === id) setSelectedCollection(null);
            loadCollections();
        } catch (e) {
            toast.error(errorMessage(e));
        }
    };

    return (
        <div className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Collections Sidebar */}
                <Card className="p-4 lg:col-span-1">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="font-bold flex items-center gap-2">
                            <FolderOpen className="w-4 h-4 text-brand" />
                            المجموعات
                        </h3>
                        <Dialog open={newCollectionOpen} onOpenChange={setNewCollectionOpen}>
                            <DialogTrigger asChild>
                                <Button size="sm" variant="outline" className="gap-1">
                                    <Plus className="w-3 h-3" />
                                    جديدة
                                </Button>
                            </DialogTrigger>
                            <DialogContent>
                                <DialogHeader>
                                    <DialogTitle>مجموعة جديدة</DialogTitle>
                                </DialogHeader>
                                <div className="space-y-4 py-4">
                                    <div>
                                        <Label>اسم المجموعة</Label>
                                        <Input
                                            value={newCollectionName}
                                            onChange={(e) => setNewCollectionName(e.target.value)}
                                            placeholder="مثلاً: دعم العملاء"
                                            className="mt-1.5"
                                        />
                                    </div>
                                    <div>
                                        <Label>الوصف (اختياري)</Label>
                                        <Input
                                            value={newCollectionDesc}
                                            onChange={(e) => setNewCollectionDesc(e.target.value)}
                                            placeholder="وصف مختصر للمجموعة"
                                            className="mt-1.5"
                                        />
                                    </div>
                                </div>
                                <div className="flex justify-end gap-2">
                                    <Button variant="outline" onClick={() => setNewCollectionOpen(false)}>إلغاء</Button>
                                    <Button onClick={createCollection}>إنشاء</Button>
                                </div>
                            </DialogContent>
                        </Dialog>
                    </div>

                    <div className="space-y-2">
                        <button
                            onClick={() => setSelectedCollection(null)}
                            className={`w-full text-right p-2 rounded-lg transition-colors ${!selectedCollection ? 'bg-brand/10 text-brand' : 'hover:bg-muted'
                                }`}
                        >
                            <div className="font-medium">الكل</div>
                            <div className="text-xs text-muted-foreground">
                                {collections.reduce((sum, c) => sum + c.document_count, 0)} مستند
                            </div>
                        </button>

                        {collections.map((col) => (
                            <div key={col.id} className="group">
                                <button
                                    onClick={() => setSelectedCollection(col.id)}
                                    className={`w-full text-right p-2 rounded-lg transition-colors ${selectedCollection === col.id ? 'bg-brand/10 text-brand' : 'hover:bg-muted'
                                        }`}
                                >
                                    <div className="flex items-center justify-between">
                                        <span className="font-medium truncate flex-1">{col.name}</span>
                                        <Button
                                            size="icon"
                                            variant="ghost"
                                            className="h-6 w-6 opacity-0 group-hover:opacity-100"
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                deleteCollection(col.id, col.name);
                                            }}
                                        >
                                            <Trash2 className="w-3 h-3 text-destructive" />
                                        </Button>
                                    </div>
                                    <div className="text-xs text-muted-foreground">
                                        {col.document_count} مستند · {col.chunk_count} مقطع
                                    </div>
                                </button>
                            </div>
                        ))}
                    </div>
                </Card>

                {/* Documents Area */}
                <Card className="p-4 lg:col-span-2">
                    <div className="flex items-center justify-between mb-4 flex-wrap gap-3">
                        <div className="flex items-center gap-2">
                            <Library className="w-5 h-5 text-brand" />
                            <h3 className="font-bold">
                                {selectedCollection
                                    ? collections.find(c => c.id === selectedCollection)?.name || 'المستندات'
                                    : 'جميع المستندات'}
                            </h3>
                        </div>
                        <div className="flex gap-2">
                            <div className="relative">
                                <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                                <Input
                                    value={searchQuery}
                                    onChange={(e) => setSearchQuery(e.target.value)}
                                    placeholder="بحث في المستندات"
                                    className="pr-10 w-48"
                                />
                            </div>
                            <Dialog open={uploadOpen} onOpenChange={setUploadOpen}>
                                <DialogTrigger asChild>
                                    <Button className="gap-2">
                                        <Upload className="w-4 h-4" />
                                        رفع مستندات
                                    </Button>
                                </DialogTrigger>
                                <DialogContent className="max-w-lg">
                                    <DialogHeader>
                                        <DialogTitle>رفع مستندات إلى قاعدة المعرفة</DialogTitle>
                                    </DialogHeader>

                                    <Tabs value={uploadType} onValueChange={(v) => setUploadType(v as typeof uploadType)}>
                                        <TabsList className="grid w-full grid-cols-2">
                                            <TabsTrigger value="files">ملفات محلية</TabsTrigger>
                                            <TabsTrigger value="urls">روابط URL</TabsTrigger>
                                        </TabsList>

                                        <TabsContent value="files" className="space-y-4">
                                            <div className="border-2 border-dashed border-border rounded-lg p-6 text-center hover:border-brand transition-colors">
                                                <input
                                                    type="file"
                                                    multiple
                                                    accept=".pdf,.txt,.md,.docx,.csv,.json"
                                                    onChange={(e) => setUploadFiles(Array.from(e.target.files || []))}
                                                    className="hidden"
                                                    id="kb-file-upload"
                                                />
                                                <label htmlFor="kb-file-upload" className="cursor-pointer">
                                                    <Upload className="w-8 h-8 mx-auto text-muted-foreground mb-2" />
                                                    <p className="text-sm">اختر ملفات للرفع</p>
                                                    <p className="text-xs text-muted-foreground mt-1">
                                                        PDF, TXT, MD, DOCX, CSV, JSON
                                                    </p>
                                                </label>
                                            </div>
                                            {uploadFiles.length > 0 && (
                                                <div className="space-y-1">
                                                    {uploadFiles.slice(0, 5).map((f, i) => (
                                                        <div key={i} className="text-sm flex items-center gap-2">
                                                            <FileText className="w-4 h-4" />
                                                            <span className="truncate">{f.name}</span>
                                                            <span className="text-xs text-muted-foreground">
                                                                {(f.size / 1024).toFixed(0)} KB
                                                            </span>
                                                        </div>
                                                    ))}
                                                    {uploadFiles.length > 5 && (
                                                        <div className="text-xs text-muted-foreground">
                                                            +{uploadFiles.length - 5} ملفات أخرى
                                                        </div>
                                                    )}
                                                </div>
                                            )}
                                        </TabsContent>

                                        <TabsContent value="urls" className="space-y-4">
                                            <Textarea
                                                value={uploadUrls.join('\n')}
                                                onChange={(e) => setUploadUrls(e.target.value.split('\n').filter(l => l.trim()))}
                                                placeholder="أدخل روابط URL كل رابط في سطر جديد"
                                                rows={5}
                                            />
                                            <p className="text-xs text-muted-foreground">
                                                يدعم: صفحات ويب، مستندات Google Docs، ملفات PDF عامة
                                            </p>
                                        </TabsContent>
                                    </Tabs>

                                    <div className="flex justify-end gap-2">
                                        <Button variant="outline" onClick={() => setUploadOpen(false)}>إلغاء</Button>
                                        <Button onClick={uploadDocuments}>رفع ومعالجة</Button>
                                    </div>
                                </DialogContent>
                            </Dialog>
                        </div>
                    </div>

                    {loading ? (
                        <div className="text-center py-12">
                            <Loader2 className="w-6 h-6 animate-spin mx-auto text-muted-foreground" />
                        </div>
                    ) : documents.length === 0 ? (
                        <div className="text-center py-12">
                            <Database className="w-12 h-12 mx-auto text-muted-foreground mb-3 opacity-50" />
                            <p className="text-muted-foreground">لا توجد مستندات في هذه المجموعة</p>
                            <Button variant="link" onClick={() => setUploadOpen(true)} className="mt-2">
                                رفع مستندات جديدة
                            </Button>
                        </div>
                    ) : (
                        <div className="space-y-3">
                            {documents.map((doc) => {
                                const StatusIcon = doc.status === 'ready' ? CheckCircle : doc.status === 'failed' ? XCircle : Loader2;
                                return (
                                    <div key={doc.id} className="border border-border rounded-lg p-3 hover:bg-muted/30">
                                        <div className="flex items-start justify-between">
                                            <div className="flex items-start gap-3 flex-1">
                                                <FileText className="w-5 h-5 text-brand shrink-0 mt-0.5" />
                                                <div className="flex-1 min-w-0">
                                                    <div className="font-medium truncate">{doc.name}</div>
                                                    <div className="flex flex-wrap gap-3 text-xs text-muted-foreground mt-1">
                                                        <span>{doc.type.toUpperCase()}</span>
                                                        {doc.chunks_count && (
                                                            <span>{doc.chunks_count} مقطع</span>
                                                        )}
                                                        <span>{new Date(doc.created_at).toLocaleString('ar-EG')}</span>
                                                        <Badge
                                                            variant="outline"
                                                            className={doc.status === 'ready' ? 'border-green-500 text-green-600' :
                                                                doc.status === 'failed' ? 'border-red-500 text-red-600' :
                                                                    'border-yellow-500 text-yellow-600'}
                                                        >
                                                            <StatusIcon className="w-3 h-3 ml-1" />
                                                            {doc.status === 'ready' ? 'جاهز' :
                                                                doc.status === 'processing' ? 'قيد المعالجة' :
                                                                    doc.status === 'failed' ? 'فشل' : 'قيد الانتظار'}
                                                        </Badge>
                                                    </div>
                                                    {!!doc.metadata?.source && (
                                                        <div className="text-xs text-muted-foreground mt-1 truncate">
                                                            المصدر: {doc.metadata.source as string}
                                                        </div>
                                                    )}
                                                </div>
                                            </div>
                                            <Button
                                                size="sm"
                                                variant="ghost"
                                                onClick={() => deleteDocument(doc.id)}
                                                className="text-destructive shrink-0"
                                            >
                                                <Trash2 className="w-4 h-4" />
                                            </Button>
                                        </div>
                                        {doc.status === 'processing' && (
                                            <div className="mt-3">
                                                <Progress value={Math.random() * 80 + 10} className="h-1" />
                                            </div>
                                        )}
                                    </div>
                                );
                            })}
                        </div>
                    )}
                </Card>
            </div>
        </div>
    );
}