# SynapseOS Frontend Build Checklist

## Backend contract notes (verified from source)
- Auth: POST /auth/register, POST /auth/login (OAuth2 form: username,password) -> {access_token, refresh_token, token_type, user_id, role}
- No /auth/me, /auth/refresh, /auth/logout routes wired yet (schemas exist but unused) -> TODO
- Tenants: POST /tenants/
- Users: POST /users/ (ADMIN), GET /users/ (ADMIN, ANALYST)
- Datasets: POST /datasets, POST /datasets/{id}/versions (multipart files[]), GET /datasets, GET /datasets/{id}, GET /datasets/{id}/versions, GET /datasets/versions/{version_id}/files, GET /datasets/files/{file_id}/download, DELETE /datasets/{id}
- Knowledge: POST /knowledge/ingest (multipart file+collection_name), POST /knowledge/query {query,collection_name,top_k} -> {answer,sources[],metrics}. NO list/history endpoint -> TODO for Document Library table (show ingested-this-session only + TODO note)
- Analytics: POST /analytics/run {dataset_version_id} -> {overview,revenue,customers,products,sellers,reviews,operations,geography,trends,insights} (all optional/partial keys depending on dataset columns)
- Forecast: POST /forecast/train {dataset_version_id,date_column?,target_column?,query} -> {forecast_id,message}; POST /forecast/predict {forecast_id,periods} -> {forecast:[{date,prediction,lower,upper}]}. No GET list -> TODO
- Prediction: POST /predictions/run {dataset_version_id, prediction_type: customer_churn|delivery_delay} -> PredictionResult{prediction_type,summary{total_entities,high_risk_entities,average_probability,business_impact},predictions[{entity_id,probability,level,drivers,metrics}],recommendations[],metadata}; GET /predictions/history -> list of {id,prediction_type,result}
- Risk: GET /risks/analyze -> {overall_risk,level,risks:[{type,score,severity,impact,affected_entities,recommendations}]}
- Assistant: POST /assistant/chat {message,metadata} -> {answer,sources[],recommendations[],data,agent,tenant_id}; POST /assistant/chat/stream (SSE) events: data: {type: status|agent_started|agent_completed|complete|error, message, agent, data} ... final: data:{type:"final", response:{answer,sources,recommendations,data,agent,tenant_id}}
- No dedicated /dashboard endpoint -> Dashboard composes from datasets list, predictions history, risks -> TODO note for missing summary endpoints
- Enums: UserRole(ADMIN,ANALYST,EXECUTIVE), DatasetType(SALES,INVENTORY,CUSTOMER,FINANCE,GENERIC), BusinessDomain(RETAIL,ECOMMERCE,FINANCE,MANUFACTURING,HEALTHCARE,GENERIC), PredictionType(customer_churn,delivery_delay)

## Build order progress
- [x] 1. Project setup (package.json, vite, ts, tailwind, index.html, main.tsx)
- [x] 2. Types
- [x] 3. Axios client + services
- [x] 4. Zustand stores
- [x] 5. Providers + Theme
- [x] 6. Router
- [x] 7. Layout (Sidebar, TopNavbar, AppLayout, PageHeader, breadcrumbs)
- [x] 8. shadcn/ui primitives (button, input, card, dialog, table, badge, skeleton, dropdown, tabs, select, toast/sonner)
- [x] 9. Common reusable components (MetricCard, ChartCard, DataTable, SearchBar, EmptyState, ErrorState, LoadingSkeleton, UploadZone, StatusBadge, ConfirmationDialog)
- [x] 10. Auth feature (login, register pages)
- [x] 11. Dashboard feature
- [x] 12. AI Assistant feature (flagship: chat, execution panel, streaming)
- [x] 13. Datasets feature
- [x] 14. Knowledge feature
- [x] 15. Analytics feature
- [x] 16. Forecasting feature
- [x] 17. Prediction feature
- [x] 18. Scenario Planner feature
- [x] 19. Users feature
- [x] 20. Settings feature
- [x] 21. Final polish (README, .env.example, lazy loading verification)
