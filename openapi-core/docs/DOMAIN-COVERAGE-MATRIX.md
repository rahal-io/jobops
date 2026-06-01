# Domain coverage matrix

OpenAPI 3.1 specs under [`openapi-core/src/`](../src/) — 15 domains in [`domains.json`](../domains.json).

**Goal linkage:** `strategy.CareerGoal.analyticsGoalId` optionally references `analytics.AnalyticsGoal.id` for progress tracking. They remain separate aggregates.

| Domain | `x-domain` | Entities (`x-entity`) | Key value objects / enums | HTTP operations |
|--------|------------|-------------------------|---------------------------|-----------------|
| discovery | disc | JobPosting, JobBoard, SavedJob | SearchFilter, SalaryRange, JobBoardAdapterType | 7 |
| evaluation | eval | JobEvaluation | FitDimension, DimensionScore | 4 |
| pipeline | pip | Application, FollowUp | ApplicationStatus, PipelineStage, StatusHistoryEntry | 6 |
| application-execution | aex | ApplicationSubmission | SubmissionStatus, FormField, FieldAnswer, SubmissionResult | 4 |
| resume | res | Resume, GeneratedResume | CvTemplate, Skill, AtsKeywordSet, ResumeSection | 4 |
| company | co | CompanyProfile | GlassdoorRating, EmployerReview, CompanySentiment | 3 |
| interview | int | InterviewSession | InterviewQuestion, PracticeAnswer, InterviewFeedback, DifficultyLevel | 5 |
| contacts | con | Contact, MessageTemplate, OutreachLog | ContactChannel, ResponseStatus | 5 |
| training | trn | Course, Project, Certification | Skill, SkillLevel, LearningStatus, Portfolio (aggregate DTO) | 8 |
| offer | off | JobOffer, OfferEvaluation | Salary→Money, CompensationPackage, OfferDimensionScore | 5 |
| analytics | anl | RejectionRecord, AnalyticsGoal, AnalyticsReport | PatternStats, Trend, MetricSnapshot | 5 |
| profile | prf | UserProfile | ContactInfo, Credential, SkillSummary, UserPreferences | 4 |
| strategy | str | CareerGoal | CareerArchetype, NorthStar, GoalMetric | 3 |
| ai | aia | AiModel, PromptTemplate, AgentRun | JobSearchWorkflow, AgentWorkflowResult (oneOf), InferenceMode | 12 |
| platform | plt | — | HealthResponse, BoundedContextInfo, CliModeMapping | 3 |

**Shared primitives:** [`src/common/primitives.yaml`](../src/common/primitives.yaml) — `Money`, `DateRange`, `ExternalUrl`.

**Validation:** `cd openapi-core && pnpm test` (Redocly lint + bundle all 15 domains).
