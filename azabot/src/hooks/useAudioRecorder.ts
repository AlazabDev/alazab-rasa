/**
 * useAudioRecorder — hook تسجيل صوتي احترافي
 * - MediaRecorder API مع دعم webm/opus
 * - waveform visualization عبر AnalyserNode
 * - اختصار لوحة مفاتيح: Space
 * - إلغاء تلقائي بعد MAX_DURATION ثانية
 * - تنظيف تلقائي عند unmount
 */

import { useState, useRef, useCallback, useEffect, useLayoutEffect } from "react";

const MAX_DURATION = 120; // ثانية
const CHUNK_INTERVAL = 250; // ms

export type RecorderState = "idle" | "recording" | "processing";

export interface AudioRecorderResult {
  state: RecorderState;
  duration: number;
  waveform: number[]; // 0–1 per bar
  startRecording: () => Promise<void>;
  stopRecording: () => void;
  cancelRecording: () => void;
  error: string | null;
}

export function useAudioRecorder(
  onAudioReady: (blob: Blob) => Promise<void>
): AudioRecorderResult {
  const [state, setState] = useState<RecorderState>("idle");
  const [duration, setDuration] = useState(0);
  const [waveform, setWaveform] = useState<number[]>(new Array(32).fill(0));
  const [error, setError] = useState<string | null>(null);

  const recorderRef  = useRef<MediaRecorder | null>(null);
  const streamRef    = useRef<MediaStream | null>(null);
  const chunksRef    = useRef<Blob[]>([]);
  const timerRef     = useRef<ReturnType<typeof setInterval> | null>(null);
  const animFrameRef = useRef<number | null>(null);
  const analyserRef  = useRef<AnalyserNode | null>(null);
  const cancelledRef = useRef(false);

  // تنظيف عند unmount
  useEffect(() => {
    return () => {
      _cleanup();
    };
  }, []);

  // اختصار Space لبدء/إيقاف التسجيل
  // نستخدم refs لتجنب إعادة register الـ listener عند كل تغيير
  const stateRef = useRef(state);
  stateRef.current = state;
  const startRecordingRef = useRef(startRecording);
  startRecordingRef.current = startRecording;
  const stopRecordingRef = useRef(stopRecording);
  stopRecordingRef.current = stopRecording;

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.code !== "Space") return;
      const tag = (e.target as HTMLElement).tagName;
      if (["INPUT", "TEXTAREA", "SELECT", "BUTTON"].includes(tag)) return;
      e.preventDefault();
      if (stateRef.current === "idle") startRecordingRef.current();
      else if (stateRef.current === "recording") stopRecordingRef.current();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const _cleanup = () => {
    if (timerRef.current) clearInterval(timerRef.current);
    if (animFrameRef.current) cancelAnimationFrame(animFrameRef.current);
    streamRef.current?.getTracks().forEach((t) => t.stop());
    streamRef.current = null;
    recorderRef.current = null;
    analyserRef.current = null;
  };

  const _startWaveform = (stream: MediaStream) => {
    try {
      const ctx = new AudioContext();
      const source = ctx.createMediaStreamSource(stream);
      const analyser = ctx.createAnalyser();
      analyser.fftSize = 64;
      source.connect(analyser);
      analyserRef.current = analyser;

      const data = new Uint8Array(analyser.frequencyBinCount);
      const NUM_BARS = 32;

      const draw = () => {
        analyser.getByteFrequencyData(data);
        const bars: number[] = [];
        const step = Math.floor(data.length / NUM_BARS);
        for (let i = 0; i < NUM_BARS; i++) {
          const val = data[i * step] / 255;
          bars.push(val);
        }
        setWaveform(bars);
        animFrameRef.current = requestAnimationFrame(draw);
      };
      animFrameRef.current = requestAnimationFrame(draw);
    } catch {
      // AnalyserNode قد لا يعمل في كل البيئات — نتجاهل الخطأ
    }
  };

  // stopRecording ref للاستخدام داخل startRecording بدون deps دورية
  const stopRecordingCbRef = useRef<() => void>(() => {});

  const startRecording = useCallback(async () => {
    setError(null);
    cancelledRef.current = false;

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          sampleRate: 16000,
        },
      });
      streamRef.current = stream;

      const mimeType = MediaRecorder.isTypeSupported("audio/webm;codecs=opus")
        ? "audio/webm;codecs=opus"
        : "audio/webm";

      const recorder = new MediaRecorder(stream, { mimeType });
      recorderRef.current = recorder;
      chunksRef.current = [];

      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) chunksRef.current.push(e.data);
      };

      recorder.onstop = async () => {
        if (animFrameRef.current) cancelAnimationFrame(animFrameRef.current);
        setWaveform(new Array(32).fill(0));
        stream.getTracks().forEach((t) => t.stop());
        streamRef.current = null;
        if (timerRef.current) clearInterval(timerRef.current);

        if (cancelledRef.current) {
          setState("idle");
          setDuration(0);
          return;
        }

        const blob = new Blob(chunksRef.current, { type: mimeType });
        if (blob.size < 1000) {
          setState("idle");
          setDuration(0);
          return;
        }

        setState("processing");
        try {
          await onAudioReady(blob);
        } finally {
          setState("idle");
          setDuration(0);
        }
      };

      recorder.start(CHUNK_INTERVAL);
      setState("recording");
      setDuration(0);
      _startWaveform(stream);

      // مؤقت المدة + إيقاف تلقائي
      timerRef.current = setInterval(() => {
        setDuration((d) => {
          if (d + 1 >= MAX_DURATION) stopRecordingCbRef.current();
          return d + 1;
        });
      }, 1000);
    } catch (err) {
      const msg = err instanceof Error && err.name === "NotAllowedError"
        ? "الرجاء السماح بالوصول للميكروفون من إعدادات المتصفح."
        : "لا يمكن الوصول للميكروفون.";
      setError(msg);
    }
  }, [onAudioReady]);

  const stopRecording = useCallback(() => {
    recorderRef.current?.stop();
    setState("recording"); // onstop سيغيّرها
    if (timerRef.current) clearInterval(timerRef.current);
  }, []);

  // ربط stopRecordingCbRef بـ stopRecording الفعلي
  useLayoutEffect(() => {
    stopRecordingCbRef.current = stopRecording;
  });

  const cancelRecording = useCallback(() => {
    cancelledRef.current = true;
    recorderRef.current?.stop();
    if (animFrameRef.current) cancelAnimationFrame(animFrameRef.current);
    setWaveform(new Array(32).fill(0));
    if (timerRef.current) clearInterval(timerRef.current);
    setState("idle");
    setDuration(0);
  }, []);

  return {
    state,
    duration,
    waveform,
    startRecording,
    stopRecording,
    cancelRecording,
    error,
  };
}
