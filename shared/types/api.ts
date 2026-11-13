import type { ErrorCode } from '../constants/error-codes';

export interface DatabaseHealth {
  status: 'connected' | 'error';
  mode: string;
  value: string;
  timestamp?: string;
}

export interface HealthResponse {
  status: 'ok' | 'error';
  version: string;
  database: DatabaseHealth;
  timestamp?: string;
}

export interface StandardErrorResponse {
  error_code: ErrorCode | string;
  message: string;
  details?: Record<string, unknown>;
  timestamp: string;
}

export interface SessionInitRequest {
  language_code: 'hi' | 'en';
}

export interface SessionInitResponse {
  session_id: string;
  session_token: string;
  language_code: 'hi' | 'en';
  expires_at: string;
}

export interface MatchedMedication {
  formulary_id: string;
  detected_brand: string;
  generic_name: string;
  indication: string;
  default_slot: 'morning_with_food' | 'morning_after_food' | 'bedtime' | string;
  confidence: number;
}

export interface PrescriptionUploadResponse {
  upload_id: string;
  status: 'completed' | 'processing' | 'failed';
  ocr_text_preview: string;
  matched_medications: MatchedMedication[];
  unmatched_tokens: string[];
}

export interface FormularySearchItem {
  formulary_id: string;
  brand_name: string;
  generic_name: string;
  indication: string;
  default_slot: string;
}

export interface ScheduleItem {
  formulary_id: string;
  brand_name: string;
  indication: string;
  instruction: string;
}

export interface ScheduleGrouping {
  morning: ScheduleItem[];
  afternoon: ScheduleItem[];
  night: ScheduleItem[];
  benign_sensations: string[];
  red_flags: string[];
}

export interface AudioMetadata {
  audio_url: string;
  duration_seconds: number;
  format: string;
  transcript: string;
}

export interface RegimenDecodeRequest {
  confirmed_formulary_ids: string[];
}

export interface RegimenDecodeResponse {
  schedule_id: string;
  share_token: string;
  language: 'hi' | 'en';
  disclaimer: string;
  schedule: ScheduleGrouping;
  audio: AudioMetadata;
  whatsapp_share_url: string;
}
