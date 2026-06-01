# 1. High-Level Context Map

- **Opportunity Discovery:** Crawls and aggregates job postings from portals (company career pages and boards) into a central catalog.  
- **Job Evaluation:** Scores and ranks discovered jobs using a multi‑dimensional fit model (e.g. the 10D/A–F framework) to filter and prioritize opportunities【19†L80-L89】.  
- **Resume/CV Generation:** Generates or customizes the user’s CV for each target role, optimizing keywords, format, and narrative (“North Star” archetype) for ATS and recruiter appeal【19†L123-L134】.  
- **Application Execution:** Automates filling and submitting application forms (web forms, questionnaires) for selected job applications, leveraging AI to tailor answers.  
- **Pipeline & Tracking:** Maintains the application “pipeline” – a structured tracker of all jobs, submitted applications, statuses, and follow-ups【18†L159-L160】.  Ensures de-duplication and integrity of the pipeline data.  
- **Company Research:** Gathers deep background on a target company (mission, tech stack, culture) to inform fit assessment and interview prep.  
- **Contact/Outreach:** Manages networking contacts (LinkedIn connections, recruiters) and outreach messages. Generates templated messages for outreach campaigns.  
- **Interview Preparation:** Supports interview readiness by building a “story bank” (STAR-format answers, negotiation scripts) and question lists.  
- **Training & Projects:** Evaluates potential training courses, certifications, or portfolio projects, mapping them to skill gaps and career goals.  
- **Career Strategy (North Star):** Tracks long-term career goals (“North Star archetype”), user profile, and preferences to guide decisions and personalize scoring.  
- **Analytics & Patterns:** Analyzes outcomes (e.g. rejections) to detect patterns or biases, informing adjustments.  

Each context encapsulates its own language and model (e.g. in **Job Evaluation** we speak of “Score” and “Dimension”, while **Pipeline** deals in “ApplicationStatus” and “FollowUp”). This clear separation prevents a “god model” and aligns with DDD principles【17†L62-L70】.

# 2. Detailed Context Breakdown

### Opportunity Discovery
- **Purpose:** Find and import new job listings from configured sources.  
- **Owned Concepts:** `JobListing`, `JobPortal`, `SearchQuery`, `JobCriteria`.  
- **Key Aggregates:** **JobListing** (an aggregate root encapsulating the full description and metadata of a found job).  
- **Entities:** *CompanySite*, *JobPostingDetail* (if treated separately; often part of the aggregate).  
- **Value Objects:** `Location`, `RoleTitle`, `ExperienceRange`, `RemoteOption`.  
- **Domain Services:** *PortalScanner* – interfaces with external APIs or headless browsers to fetch listings. *DeduplicationService* – filters out duplicates.  
- **Commands / Use Cases:** `ScanPortals()`, `ImportListing()`, `RefreshJobData()`.  
- **Events Produced:** `JobFound` (new listing discovered), `JobExpired` (previous listing no longer available).  
- **Events Consumed:** `ProfileUpdated` (to adjust search filters if user preferences change).  

*Ubiquitous Language:* e.g. “We scanned the Greenhouse portal and retrieved 50 new **JobListing** entries”【22†L725-L733】. The context knows nothing of CVs or applications – just raw opportunities.

### Job Evaluation
- **Purpose:** Assess how well a job fits the user’s profile. Compute a composite score (A–F grade) based on multiple dimensions (skills, seniority, comp, location, etc.)【19†L80-L89】.  
- **Owned Concepts:** `JobScore`, `FitDimension` (e.g. RoleMatch, SkillsAlignment, Seniority, Compensation, Geographic, Growth, etc.).  
- **Key Aggregates:** **JobEvaluation** (root containing the `JobListing` reference and its score breakdown).  
- **Entities:** (No complex entities beyond aggregates; each evaluation is fresh per job.)  
- **Value Objects:** `Score` (value object representing the numeric grade or letter), `DimensionScore` (value object for each dimension’s score).  
- **Domain Services:** *EvaluationService* – applies the scoring logic or invokes an AI agent to reason about the fit. *ExperienceMatcher* – compares CV proof points to job requirements. *CompResearchService* – looks up salary benchmarks.  
- **Commands / Use Cases:** `EvaluateJob(jobID)`, `ReevaluateJob(jobID)` (e.g. after profile update).  
- **Events Produced:** `JobEvaluated` (with result scores), `JobFilteredOut` (if score < threshold).  
- **Events Consumed:** `JobFound` (from Opportunity Discovery), `ProfileUpdated`, `NewContactAdded` (perhaps to check networking angle).  

*Ubiquitous Language:* “After running the 10D model, this **JobListing** earned a B in RoleMatch and a C in Compensation, yielding an overall ‘B’ grade”【19†L80-L89】. This context does not generate CVs or track applications – it only “rates” jobs.

### Resume/CV Generation
- **Purpose:** Create or adapt the user’s resume/CV for a specific job, injecting relevant keywords and formatting for ATS compliance【19†L123-L134】.  
- **Owned Concepts:** `BaseCV` (the user’s master CV), `Keywords`, `TemplateFormat`, `Archetype`.  
- **Key Aggregates:** **CurriculumVitae** (root containing the master CV content).  
- **Entities:** **GeneratedResume** (an entity representing the CV tailored for a particular job, including the final PDF).  
- **Value Objects:** `ATSKeywords` (list of terms), `CVLayout` (paper size, style).  
- **Domain Services:** *CVGenerator* – injects keywords and rephrases sections. *PDFService* – renders a formatted PDF (using e.g. HTML/CSS templates). *ArchetypeClassifier* – identifies the user’s career archetype (“North Star”) to keep narrative consistent【19†L133-L134】.  
- **Commands / Use Cases:** `GenerateResumeForJob(jobID)`, `UpdateBaseCV()`, `AdjustTemplate(region)`.  
- **Events Produced:** `ResumeGenerated` (with link to PDF), `CVUpdated`.  
- **Events Consumed:** `JobEvaluated`, `ProfileUpdated`, `CompanyInfoFound` (to tailor narrative).  

*Ubiquitous Language:* “We injected 15–20 keywords into the **CV** to optimize ATS matching【19†L127-L134】. The resume template was adjusted to EU A4 format for this company.” This context only deals with CV content; it does not itself send applications or update pipeline status.

### Application Execution
- **Purpose:** Use AI agents to fill out and submit job application forms on behalf of the user, according to stored profile and the job’s application URL.  
- **Owned Concepts:** `ApplicationForm`, `FieldAnswer`, `SubmissionResult`.  
- **Key Aggregates:** **ApplicationSubmission** (root that tracks one attempt to apply to a job).  
- **Entities:** (Might treat each *FieldAnswer* as an entity during the filling process, but usually ephemeral.)  
- **Value Objects:** `URL`, `FormField`, `AIResponse`.  
- **Domain Services:** *FormFillerService* – orchestrates retrieving form fields and using AI to craft answers. *SubmissionService* – handles web form submission, CAPTCHA, and confirmation.  
- **Commands / Use Cases:** `SubmitApplication(jobID)`, `FillApplicationForm(jobID)`, `RetrySubmission(jobID)`.  
- **Events Produced:** `ApplicationSubmitted`, `SubmissionFailed`.  
- **Events Consumed:** `JobEvaluated`, `ContactAdded` (maybe to CC a referral contact), `FollowUpScheduled`.  

*Ubiquitous Language:* “When executing `/career-ops apply`, the **ApplicationForm** for job 123 was auto-filled and submitted by the agent【22†L688-L695】.” It does not itself score jobs or generate CVs, only manages submission.

### Pipeline & Tracking
- **Purpose:** Central “source of truth” for all applications. Tracks each target job and the status of its application (applied, interview scheduled, rejected, etc.), and schedules follow-ups. Ensures data integrity (no duplicates)【18†L159-L160】.  
- **Owned Concepts:** `Application`, `PipelineEntry`, `ApplicationStatus`, `FollowUpAction`.  
- **Key Aggregates:** **Pipeline** (root that contains all Applications for the user).  
- **Entities:** **Application** (each entry with status history).  
- **Value Objects:** `Status` (e.g. Pending, Submitted, Interview, Offer, Rejected), `FollowUpPlan`.  
- **Domain Services:** *PipelineManager* – merge new entries, dedupe, normalize statuses (e.g. “Interview Scheduled” vs “Phone Screen”). *HealthCheckService* – alerts if no update on a stale application.  
- **Commands / Use Cases:** `AddApplication(jobID)`, `UpdateStatus(applicationID, newStatus)`, `ScheduleFollowUp(applicationID)`, `ViewPipeline(filter)`.  
- **Events Produced:** `ApplicationAdded`, `StatusUpdated`, `FollowUpScheduled`.  
- **Events Consumed:** `JobEvaluated` (to possibly add top-scoring jobs to pipeline), `ResumeGenerated`, `ApplicationSubmitted`, `PipelineIntegrityCheckTrigger`.  

*Ubiquitous Language:* “A new **Application** was created in the pipeline for job 456 with status ‘Applied’. We deduplicated it against 680+ URLs【18†L159-L160】. Next follow-up is scheduled in 7 days.” This context does not itself scan for jobs or generate content; it aggregates events about applications.

### Company Research
- **Purpose:** Aggregate rich information about a target company (mission, products, culture, news) to inform evaluation and interviews.  
- **Owned Concepts:** `CompanyProfile`, `ProductLine`, `NewsArticle`.  
- **Key Aggregates:** **Company** (root containing the company’s collected data).  
- **Entities:** *OfficeLocation*, *KeyContact* (if scraping LinkedIn or news).  
- **Value Objects:** `Sector`, `SizeCategory`, `MissionStatement`.  
- **Domain Services:** *ResearchService* – queries public sources, APIs, or uses AI to summarize company info. *NewsFetcher*, *TechStackScanner*.  
- **Commands / Use Cases:** `ResearchCompany(companyID)`, `GetCompetitors(companyID)`.  
- **Events Produced:** `CompanyInfoFound`, `CompetitorListFetched`.  
- **Events Consumed:** `JobEvaluated`, `ApplicationSubmitted` (for context), `ProfileUpdated`.  

*Ubiquitous Language:* “Deep research on Acme Corp shows they are a **Series B startup** in fintech【22†L594-L600】. The company profile context feeds insights to the Job Evaluation context (e.g. *CompanyStage*) and Interview Preparation.”

### Contact/Outreach
- **Purpose:** Maintain an address book of professional contacts and send tailored outreach messages.  
- **Owned Concepts:** `Contact` (name, role, company, link), `OutreachMessageTemplate`.  
- **Key Aggregates:** **ContactList** (root containing all contacts).  
- **Entities:** **Contact** (each with unique ID).  
- **Value Objects:** `EmailAddress`, `LinkedInURL`, `MessageBody`.  
- **Domain Services:** *MessagingService* (integrates with LinkedIn API or email to send messages). *ContactImporter* (imports contacts from CSV/LinkedIn).  
- **Commands / Use Cases:** `AddContact()`, `SendOutreach(contactID)`, `LogCommunication(contactID)`.  
- **Events Produced:** `ContactAdded`, `OutreachSent`.  
- **Events Consumed:** `PipelineUpdated` (if a contact works at a target company), `ProfileUpdated`.  

*Ubiquitous Language:* “Using `/career-ops contacto` we generated a LinkedIn outreach message to the recruiter contact”【22†L686-L694】. Contacts are managed independently of applications until an outreach is sent.

### Interview Preparation
- **Purpose:** Build and manage a “story bank” (STAR-format career stories) and generate question lists and practice materials for interviews. Provide negotiation scripts.  
- **Owned Concepts:** `InterviewStory`, `BehavioralQuestion`, `NegotiationScript`.  
- **Key Aggregates:** **InterviewPlan** (root containing questions and stories for one interview).  
- **Entities:** **Story** (a STAR-format answer, with fields Situation/Task/Action/Result/Reflection), **Question** (with suggested answer outline).  
- **Value Objects:** `Skill` (tag associated with each story), `STARModel`.  
- **Domain Services:** *InterviewCoachService* – generates possible interview questions and matches them with stories. *StoryBankService* – accumulates and retrieves personal stories from prior applications【22†L590-L592】. *NegotiationAdvisor* – produces negotiation scripts.  
- **Commands / Use Cases:** `PrepareInterview(jobID)`, `AddStory(story)`, `GenerateQuestions(role)`.  
- **Events Produced:** `InterviewPrepared` (materials ready).  
- **Events Consumed:** `JobEvaluated`, `CompanyInfoFound` (for company-specific questions), `ProfileUpdated`, `ApplicationStatusChanged` (e.g. when an interview is scheduled).  

*Ubiquitous Language:* “Before calling `/career-ops interview-prep`, the system collected 5–10 **STAR** stories as a story bank【22†L590-L592】. Each interview prep includes those stories and negotiation tips relevant to the company’s profile.”

### Training & Projects
- **Purpose:** Help the user evaluate learning resources and projects that improve skills or resume, aligned to career goals.  
- **Owned Concepts:** `Course`, `Certification`, `PortfolioProject`, `SkillGap`.  
- **Key Aggregates:** **LearningPlan** (root containing recommended courses and projects).  
- **Entities:** **Course**, **Project** (each with metadata).  
- **Value Objects:** `SkillLevel`, `Rating`.  
- **Domain Services:** *CourseEvaluator* – analyzes a course description against skill gaps. *ProjectAnalyzer* – assesses a project’s relevance to target roles.  
- **Commands / Use Cases:** `EvaluateCourse(url)`, `EvaluateProject(repoURL)`.  
- **Events Produced:** `CourseRecommended`, `ProjectAssigned`.  
- **Events Consumed:** `ProfileUpdated`, `JobEvaluated` (to identify gaps).  

*Ubiquitous Language:* “Using `/career-ops training`, the system evaluated an online AI course and found it aligns well with my *Data Science* skill gap. The project context similarly rates portfolio projects.” These are standalone tasks not tied to a specific job application.

### Career Strategy (North Star)
- **Purpose:** Maintain the user’s overall career goals and identity (the “North Star” archetype), and ensure all activities align with these goals.  
- **Owned Concepts:** `NorthStar`, `CareerGoal`, `Archetype` (e.g. “AI Platform Engineer”).  
- **Key Aggregates:** **CareerProfile** (root holding the user’s background, goals, and archetype).  
- **Entities:** **CareerGoal** (e.g. target role or domain).  
- **Value Objects:** `Preference` (location, industry, etc.).  
- **Domain Services:** *CareerAdvisor* – suggests archetype adjustments or goal updates. *ProfileManager* – manages the underlying data (CV.md, preferences file).  
- **Commands / Use Cases:** `UpdateCareerGoal(goal)`, `SetNorthStar(archetype)`.  
- **Events Produced:** `CareerGoalUpdated`, `ArchetypeSelected`.  
- **Events Consumed:** Nearly all contexts; e.g. `ProfileUpdated` triggers re-evaluation of pipeline, `JobEvaluated` for vetoing non-aligned jobs.  

*Ubiquitous Language:* “The user has an **Archetype** of ‘Agentic Workflows’. All job scoring and CV generation are tailored to reinforce this North Star【19†L133-L134】.” This context governs shared data, and all other contexts must respect its definitions (possibly via an Anti-Corruption Layer if integrated as a separate module【17†L92-L100】).

### Analytics & Patterns
- **Purpose:** Analyze the outcomes of the job search (e.g. rejections, interviews) to detect systematic patterns (such as skill gaps or bias) and feed insights back into strategy.  
- **Owned Concepts:** `RejectionPattern`, `ApplicationStatistics`.  
- **Key Aggregates:** **PatternReport** (root with findings from analysis runs).  
- **Entities:** (Primarily the patterns themselves; could include *RejectionReason* as detail).  
- **Value Objects:** `Pattern` (e.g. “80% of rejections cite lack of X skill”).  
- **Domain Services:** *AnalyticsService* – mines application outcomes, possibly with AI, to produce reports. *FeedbackAnalyzer* – identifies common factors in rejections.  
- **Commands / Use Cases:** `AnalyzeRejections(period)`, `GenerateAnalyticsReport()`.  
- **Events Produced:** `PatternsIdentified`.  
- **Events Consumed:** `ApplicationStatusChanged` (especially to “Rejected”), `ProfileUpdated`, `JobEvaluated`.  

*Ubiquitous Language:* “The patterns context might note that most rejections occur on roles requiring Python, suggesting a **SkillGap** in Python knowledge. These insights can lead to new Training recommendations.” This is a monitoring/support context; it doesn’t itself change application state but advises the user.

# 3. Context Relationships

- **Data Flow:** Discovered `JobListing` events from *Opportunity Discovery* flow into *Job Evaluation* (score calculation) and the *Company Research* context (for company data). High-scoring jobs flow into *Pipeline* (creating an `Application`). The *Resume Generation* context pulls data from *CareerProfile* and the specific `JobListing` to produce a tailored resume, then emits `ResumeGenerated` consumed by *Pipeline* (to attach the CV to the application). When the user invokes *Application Execution*, a submission is made and the *Pipeline* context is updated with `ApplicationSubmitted`. Interview outcomes (from *Pipeline*) trigger the *Interview Preparation* context. Training and project recommendations leverage both *CareerProfile* and *JobEvaluation* insights.  
- **Dependencies:** Each context is upstream/downstream as needed. For example, *Opportunity Discovery* is upstream of *Job Evaluation*. *Career Profile* can be considered a shared kernel or core that all contexts depend on for user data.  
- **Communication Style:** 
  - *Async, Event-Driven:* Many interactions use events. For instance, `JobFound` → *Job Evaluation*; `JobEvaluated` → *Pipeline* or *Resume Generator*. This decouples contexts and allows parallel processing (batch evaluation, etc.).  
  - *Sync (APIs):* Certain operations may be synchronous (e.g. *Application Execution* might call the *Pipeline* to retrieve status before submission, or *Contact* service might synchronously look up a contact). However, even form filling can be async via tasks.  
- **Anti-Corruption Layers:** When integrating external sources (job portals, LinkedIn APIs), each context uses translation layers. For example, the raw data from an ATS API is mapped into our internal `JobListing` model; this ACL protects the rest of the system from external schema changes. Similarly, if we consumed the *CareerProfile* from a separate microservice, an ACL would translate its objects into our ubiquitous language.  
- **Context Mapping:** The map could be roughly: *Opportunity Discovery* → *Job Evaluation* → *Pipeline*; *Job Evaluation* is upstream of *Pipeline*. *Career Profile* is a customer to all, feeding their models. *Interview Prep* and *Company Research* sit downstream of *Evaluation/Pipeline*. *Contact* is largely orthogonal but links into *Pipeline*. These relationships avoid cyclic dependencies and allow autonomy (e.g. *Evaluation* doesn’t reach directly into *Pipeline’s* model, it just emits events).

# 4. Mapping to career-ops Modes

- `scan` → **Opportunity Discovery** (portal crawler).  
- `oferta`, `ofertas` → **Job Evaluation** (score single/multiple offers)【19†L112-L116】.  
- `batch` → Orchestration across **Opportunity** + **Evaluation** (parallel processing of many URLs)【19†L109-L116】.  
- `pdf` → **Resume/CV Generation** (produce tailored ATS-optimized PDF)【19†L115-L116】.  
- `apply` → **Application Execution** (auto-fill forms).  
- `tracker`, `pipeline`, `followup` → **Pipeline & Tracking** (view and update application statuses)【8†L688-L695】【18†L159-L160】.  
- `deep` → **Company Research** (detailed company analysis)【22†L686-L694】.  
- `contacto` → **Contact/Outreach** (LinkedIn recruiter messaging)【22†L694-L700】.  
- `training` → **Training & Projects** (evaluate a course)【22†L696-L699】.  
- `project` → **Training & Projects** (evaluate a portfolio project)【22†L697-L699】.  
- `interview-prep` → **Interview Preparation** (generate stories and Q&A)【22†L584-L592】.  
- `update` → **Career Strategy** (update profile/goals).  
- `patterns` → **Analytics & Patterns** (analyze rejection patterns, not directly shown but implied by context).  

For example, invoking `/career-ops scan` triggers the Opportunity Discovery context to fill the pipeline【22†L725-L733】, while `/career-ops apply` engages the Application Execution context【22†L686-L694】. The mode definitions in the docs align neatly with these bounded contexts.

# 5. Suggested Architecture

- **Service Granularity:** Given the complexity and need for agentic workflows, we recommend a *modular microservices* approach (or at least a modular monolith). Each bounded context can be its own service with its own data store, allowing independent scaling (e.g. many parallel *Evaluation* agents) and deployment. This matches the notion of an “AI sub-agent per context”【17†L62-L70】. For example, a standalone **Evaluation Service** can run multiple scoring agents in parallel, while a separate **Resume Service** handles CV generation.  
- **Event-Driven Pipeline:** Use an event bus or message queue (e.g. Kafka/RabbitMQ) so contexts communicate asynchronously. E.g., *Discovery* emits `JobFound`, which *Evaluation* and *Company Research* subscribe to. This allows asynchronous batch processing and easy extension. Contexts can also call each other via well-defined APIs when needed (e.g. *Pipeline* might request a resume from *CV Service* synchronously).  
- **AI Agents:** AI/LLM calls can be encapsulated as services within contexts (like *EvaluationAgent*, *FormFillerAgent*). Each mode can spawn an agent that acts within its context boundary, as per DDD guidance on AI agents【17†L92-L100】【17†L169-L174】. For example, the *Job Evaluation* context could host an AI service that reasons about fit, while the *Interview* context has a different agent focusing on generating Q&A. Agents should respect the context’s model (not touch another context’s internal objects directly).  
- **Extensibility:** New modes/contexts can subscribe to existing events or APIs. The use of an event bus facilitates adding new consumers (e.g. a future “Salary Negotiation” context could listen to `JobEvaluated`). Anti-corruption layers (adapters) should be designed so new external integrations (a new portal API) plug into the relevant context without leaking outside.

# 6. Risks & Boundary Smells

- **Boundary Violations:** A risk is letting one context read or write another’s data models directly. For example, if the *Resume Generation* started querying the *Pipeline* DB for job statuses, that would blur boundaries. Use domain events or ACL transformations instead.  
- **Tight Coupling:** Without care, *Application Execution* and *Pipeline* could become tightly coupled (e.g. if *Pipeline* assumes every submission uses a particular CV format). Ensuring each context publishes events (like `ResumeGenerated`) rather than synchronous calls to each other reduces coupling【17†L92-L100】.  
- **God Services:** The *Career Strategy* or *Profile* context might tempt the team to dump global logic into one place. Instead, it should only govern shared definitions (e.g. goals, archetypes) and let other contexts own their workflows.  
- **Shared Kernel Risk:** If contexts share the same database tables (e.g. *Opportunity* and *Pipeline* using a shared “jobs” table), that is a smell. Each context needs its own persistence. For shared references (like user profile), use a well-defined interface or propagate changes via events.  
- **Overlapping Responsibilities:** e.g., *Job Evaluation* vs *Interview Prep* both deal with assessing candidate-job fit, but one for scoring, one for storytelling. Keep *Evaluation* focused on numeric/qualitative scoring, and *Interview Prep* on personal narratives and questions.  
- **AI Hallucinations:** In an AI-driven system, make sure each context validates outputs (Human-in-the-Loop is key【18†L156-L164】). For example, if the *Resume Service* hallucinates skills, the *Pipeline* might catch it in a review step (i.e. treat "ResumeGenerated" as pending until approval).  
- **Scalability Boundaries:** Some contexts (like *Opportunity Discovery* and *Evaluation*) will scale differently. Plan for horizontal scaling of the scanning/evaluation agents without affecting other services. Use circuit breakers or back-pressure to isolate slow contexts.  

By adhering to DDD principles and defining these boundaries clearly, “career-ops” can evolve new modes or swap AI providers without collapsing into a tangled, monolithic agent. Each context has a single responsibility and communicates via explicit contracts (events/APIs)【17†L92-L100】【17†L169-L174】, making the system robust and maintainable. 

**Sources:** Career-Ops documentation and case study【19†L80-L89】【22†L725-L733】, principles of DDD and context mapping【17†L62-L70】【17†L92-L100】, plus actual feature descriptions (e.g. ATS resume generation【19†L123-L134】, pipeline tracking【18†L159-L160】). These informed the domain language and decomposition above.