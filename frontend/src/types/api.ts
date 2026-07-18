// ---------------------------------------------------------------------------
// Types mirrored 1:1 from the FastAPI backend Pydantic schemas.
// DO NOT invent fields that are not present in the backend contracts.
// ---------------------------------------------------------------------------

// ---- Enums (src/models/enums.py, dataset_enums.py, ml/prediction/schemas.py) --

export type UserRole = "ADMIN" | "ANALYST" | "EXECUTIVE";

export type DatasetType = "SALES" | "INVENTORY" | "CUSTOMER" | "FINANCE" | "GENERIC";

export type BusinessDomain =
  | "RETAIL"
  | "ECOMMERCE"
  | "FINANCE"
  | "MANUFACTURING"
  | "HEALTHCARE"
  | "GENERIC";

export type DatasetStatus =
  | "UPLOADING"
  | "UPLOADED"
  | "PROFILING"
  | "READY"
  | "FAILED"
  | "ARCHIVED";

export type PredictionType = "customer_churn" | "delivery_delay";

export type PredictionLevel = "LOW" | "MEDIUM" | "HIGH";

// ---- Auth (modules/auth/schemas.py) ----------------------------------------

export interface RegisterRequest {
  company_name: string;
  industry: string;
  full_name: string;
  email: string;
  password: string;
}

export interface RegisterResponse {
  message: string;
  tenant_id: string;
  user_id: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user_id: string;
  role: string;
}

// ---- Tenants (modules/tenants/schemas.py) ----------------------------------

export interface TenantCreate {
  company_name: string;
  industry: string;
}

export interface TenantResponse {
  id: string;
  company_name: string;
  industry: string;
  is_active: boolean;
  created_at: string;
}

// ---- Users (modules/users/schemas.py) --------------------------------------

export interface CreateUserRequest {
  full_name: string;
  email: string;
  password: string;
  role: UserRole;
}

export interface UserResponse {
  id: string;
  full_name: string;
  email: string;
  role: UserRole;
}

// ---- Datasets (modules/data/schemas.py) ------------------------------------

export interface DatasetCreateRequest {
  name: string;
  description?: string | null;
  dataset_type: DatasetType;
  business_domain: BusinessDomain;
  tags?: string[] | null;
}

export interface DatasetCreateResponse {
  dataset_id: string;
  message: string;
}

export interface DatasetVersionUploadResponse {
  version_id: string;
  version: number;
  message: string;
}

export interface DatasetResponse {
  id: string;
  name: string;
  description: string | null;
  dataset_type: DatasetType;
  business_domain: BusinessDomain;
  created_at: string;
}

export interface DatasetDetailResponse extends DatasetResponse {
  tags: string[] | null;
}

export interface DatasetVersionItem {
  id: string;
  version: number;
  status: string;
  created_at: string;
}

export interface DatasetFileResponse {
  id: string;
  logical_name: string;
  original_filename: string;
  rows_count: number | null;
  columns_count: number | null;
  created_at: string;
}

// ---- Knowledge (modules/knowledge/schemas.py) ------------------------------

export interface DocumentUploadResponse {
  message: string;
  document_id: string;
  chunks_processed: number;
  collection_name: string;
}

export interface SourceChunk {
  text: string;
  score: number;
  file_name: string;
  page_label: string;
  page_number: number | null;
  chunk_index: number | null;
  file_type: string | null;
  chunk_length: number | null;
  chunk_id: string | null;
}

export interface QueryMetrics {
  retrieval_time_ms: number;
  generation_time_ms: number;
  total_time_ms: number;
  chunks_retrieved: number;
  average_similarity: number;
  highest_similarity: number;
}

export interface QueryRequest {
  query: string;
  collection_name?: string;
  top_k?: number;
}

export interface QueryResponse {
  answer: string;
  sources: SourceChunk[];
  metrics: QueryMetrics;
}

// ---- Analytics (modules/analytics/schemas.py + ml/analytics/commerce.py) ---

export interface DatasetFilters {
  states?: string[];
  city?: string[];
  categories?: string[];
  brands?: string[];
  seller_id?: string[];
  customer_id?: string[];

  min_revenue?: number;
  max_revenue?: number;

  min_review_score?: number;
  max_review_score?: number;

  date_from?: string;
  date_to?: string;
}

export interface AnalyticsRequest {
  dataset_version_id: string;
  filters?: DatasetFilters;
}

export interface AnalyticsResult {
  overview?: { total_records: number; columns: number };
  revenue?: { total_revenue: number; average_order_value: number; highest_order_value: number };
  customers?: { total_customers: number; repeat_customers: number; repeat_customer_rate: number };
  products?: {
    top_categories_by_orders?: Record<string, number>;
    top_categories_by_revenue?: Record<string, number>;
    top_categories_by_rating?: Record<string, number>;
  };
  sellers?: {
    total_sellers: number;
    top_sellers_by_revenue?: Record<string, number>;
    top_sellers_by_rating?: Record<string, number>;
  };
  reviews?: { average_rating: number; low_rating_orders: number };
  operations?: { average_delivery_days?: number; late_orders?: number };
  geography?: { top_regions: Record<string, number> };
  trends?: { monthly_revenue: Record<string, number>; monthly_growth_percentage: Record<string, number> };
  insights?: string[];
}

// ---- Forecast (modules/forecast/schemas.py) --------------------------------

export interface TrainForecastRequest {
  dataset_version_id: string;
  query?: string;
}

export interface TrainForecastResponse {
  forecast_id: string;
  message: string;
}

export interface ForecastPredictRequest {
  forecast_id: string;
  periods?: number;
}

export interface ForecastPoint {
  date: string;
  prediction: number;
  lower: number;
  upper: number;
}

export interface ForecastEvaluation {
  performance_score: number;
  performance_label: string;
  mae: number;
  rmse: number;
  mape: number;
}

export interface ForecastSummary {
  forecast_days: number;
  total_expected_value: number;
  average_daily_value: number;

  highest_period: ForecastPoint;
  lowest_expected_period: ForecastPoint;

  confidence: {
    average_uncertainty_range: number;
    interpretation: string;
  };
}

export interface ForecastPredictResponse {
  forecast: ForecastPoint[];

  summary?: ForecastSummary;

  evaluation?: ForecastEvaluation;
}

// ---- Prediction (modules/prediction/schemas.py + ml/prediction/schemas.py) -

export interface PredictionRequest {
  dataset_version_id: string;
  prediction_type: PredictionType;
}

export interface EntityPrediction {
  entity_id: string;
  probability: number;
  level: PredictionLevel;
  drivers: string[];
  metrics: Record<string, unknown>;
}

export interface PredictionSummary {
  total_entities: number;
  high_risk_entities: number;
  average_probability: number;
  business_impact: Record<string, unknown>;
}

export interface PredictionResult {
  prediction_type: PredictionType;
  summary: PredictionSummary;
  predictions: EntityPrediction[];
  recommendations: string[];
  metadata: {
    metrics?: {
      accuracy: number;
      precision: number;
      recall: number;
      f1_score: number;
      roc_auc: number;
    };

    feature_importance?: {
      feature: string;
      importance: number;
    }[];
  };
}

export interface PredictionHistoryItem {
  id: string;
  prediction_type: PredictionType;
  result: PredictionResult;
}

// ---- Risk (modules/risk/schemas.py) ----------------------------------------

export interface RiskItem {
  type: string;
  score: number;
  severity: string;
  impact: Record<string, unknown>;
  affected_entities: number | null;
  recommendations: string[];
}

export interface RiskResponse {
  overall_risk: number;
  level: string;
  risks: RiskItem[];
}

// ---- Assistant (modules/assistant/schemas.py + events.py) -----------------

export interface AssistantChatRequest {
  message: string;
  metadata?: Record<string, unknown>;
}

export interface AssistantChatResponse {
  answer: string;
  sources: Record<string, unknown>[];
  recommendations: string[];
  data: Record<string, unknown>;
  agent: string | null;
  tenant_id: string | null;
}

export type StreamEventType = "status" | "agent_started" | "agent_completed" | "complete" | "error";

export interface StreamEvent {
  type: StreamEventType;
  message: string;
  agent: string | null;
  data: Record<string, unknown>;
}

export interface AssistantStreamFinalEvent {
  type: "final";
  response: AssistantChatResponse;
}

// ---- Generic API error envelope --------------------------------------------

export interface ApiErrorBody {
  detail: string | { msg: string; loc: (string | number)[] }[];
}
