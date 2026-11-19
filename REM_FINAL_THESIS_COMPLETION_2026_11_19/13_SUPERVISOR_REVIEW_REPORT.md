# 13 Supervisor review report

**Runtime Evaluation and Mitigation (REM) Framework for Financial AI Agent Security**

- **For:** Dr. Husam Fakhouri and Prof. Omar. Al-Balqa Applied University, Faculty of Artificial Intelligence, Cyberspace Security.
- **Status:** thesis R8 (19 November 2026) is **ready for supervisor review**. It has **not** been approved, examined or submitted.
- **Files:**
  - `REM_THESIS_FINAL.docx` and `REM_THESIS_FINAL.pdf` (230 pages);
  - chapter files `CHAPTER_1..5_FINAL.md`;
  - evidence in `01`–`17` of this folder.

## English technical summary

### 1. What is the research problem?

- **The threat.** A tool-using LLM agent that can make payments can be steered by **indirect prompt injection**: text inside a tool output (a bill, a transaction note, a file) that the agent obeys. The harm happens only when a **state-changing tool call** (a transfer, a standing-order change, a password change) is executed.
- **The research question.** Can a runtime layer at the tool-execution boundary decide, call by call, whether to allow, modify, escalate or block, and so reduce attack success without destroying legitimate work? Does a *learned, consequence-aware* decision add value over simple rules?

### 2. What is REM?

REM is a five-layer runtime framework placed between the agent and its tools:
1. Input & Context;
2. Detection;
3. Behavioural Analysis;
4. Decision Engine;
5. Mitigation.

Offline fitting and recalibration are cross-cutting. Every verdict writes an audit record. Linear SHAP attribution is recorded for audit and cannot change a verdict.

### 3. How does the architecture work?

For each proposed call:
1. **Evidence.** It is assembled from three groups:
   - **context:** an instruction-pattern indicator;
   - **behavioural:** e.g. privilege escalation and transition deviation;
   - **action / provenance:** whether arguments come from the user's request or from untrusted tool output.
2. **Estimation.** Ridge logistic regression gives a score s. The logistic (Platt-type) recalibration gives p = σ(γ₁s + γ₀), with γ₁ > 0.
3. **Consequence tier.** A declared tier k is assigned to the tool.
4. **Predicates.** D1 blocks prohibited tools. D2 escalates high-tier calls with missing evidence.
5. **Decision.** Otherwise the verdict minimises the conditional risk R(v) = (1−p)·L(v,0,k) + p·L(v,1,k) over Allow / Modify / Escalate / Block. This is cost-sensitive Bayes decision (Elkan), with Chow-style abstention as escalation.
6. **Mitigation.** Deterministic, before execution:
   - **Allow:** release the call.
   - **Modify:** restrict the tool for this call.
   - **Escalate:** withhold the call pending review.
   - **Block:** prevent the call.

### 4. Which attacks does it address?

- **Addressed:** indirect prompt injection in AgentDojo's banking suite, with the `important_instructions` attack. There are 9 attacker objectives: redirecting payments, leaking data through transfer notes, changing recurring payments, changing the password, and others.
- **Not addressed:** direct jailbreaks of the user, compromised tools or backends, and adaptive attackers that know REM.

### 5. How was REM implemented?

- **Code:** Python package `rem/`, with 806 automated tests passing.
- **Integration:** wraps AgentDojo's tool executor.
- **Fitting:** cross-fitting with nine outer folds, each holding out one attacker objective.
- **Fail-closed design:** the software refuses to run if a design value is undeclared.
- **REM v1.0 is frozen.** `rem/` has not changed since `9fddfa7` apart from three added files outside the decision path. Today's fresh run reproduced the published counts exactly.

### 6. What datasets and benchmarks were used?

- **Benchmark:** AgentDojo 0.1.35, banking suite (16 user tasks × 9 injection tasks).
- **Data source:** the benchmark's recorded runs of real agents (commit `089ed468`).
- **Primary population:** 3,313 eligible episodes across 21 backbones (2,979 attacked, 334 benign).
- **Second population:** 2,113 episodes, used once for a confirmatory run.
- **External comparison:** recorded runs of gpt-4o with no defence and with the four defences distributed in AgentDojo, 144 attacked and 16 benign runs each.
- **Evaluation mode:** offline replay that assumes the agent does not adapt to refusals (NO-ADAPT).
- **No live model was run.**

### 7. How were the ablation studies designed?

- **Pre-registration.** Protocol `02` was committed with code hashes **before** any arm was scored, after a reproduction gate.
- **Arms.** Ten arms on identical episodes and fold models:

  | Arm | Change |
  |---|---|
  | B0 | no defence |
  | A0 | full REM v1.0 |
  | A1 | − behavioural evidence |
  | A2 | − Platt calibration (boundaries fixed) |
  | A3 | consequence-independent thresholds (selected on training folds) |
  | A4a | − context evidence |
  | A4b | − action / provenance evidence |
  | A5 | − Modify |
  | A6 | − the learned decision (predicates only) |
  | A7 | − predicates |

- **Metrics.**
  - Security, utility, call-level and verdict metrics.
  - Calibration on held-out steps.
  - Latency.
  - Call-level reachability.
  - Paired grouped-bootstrap intervals against A0.
- **Interpretation rules** were fixed in advance.

### 8. Which components contributed to security and utility?

| Component | Security | Utility | Verdict |
|---|---|---|---|
| Learned decision (A6) | +22.19 ASR points without it [14.55, 28.86]; 661 attacks prevented, 0 admitted | Costs 22.5 benign points | **Contributes to security**, at a measurable utility cost |
| Expected loss vs thresholds (A3) | Thresholds admit 153 more attacks (+5.14 [0.70, 13.05]) | Thresholds complete 19.5 more benign points | **Trade-off** |
| Behavioural evidence (A1) | no effect | Removing it gives +10.5 benign [1.2, 22.6] | **Negative net effect** |
| Calibration (A2) | no attack outcome changes | Removing it gives +24 tasks | **Does not improve protection.** Raw probabilities are equally well calibrated. |
| Action / provenance evidence (A4b) | 17 vs 11 attacks, not resolved | – | Carries the discrimination (ROC-AUC 0.94 → 0.80) |
| Context evidence (A4a), predicates (A7) | no measurable effect | – | – |
| Modify (A5) | no episode changes | no episode changes | **Redundant without a reviewer** |

### 9. How does REM compare with external defences?

**Recorded closed loop, gpt-4o, 144 attacked runs each:**

| Defence | ASR | Benign utility |
|---|---|---|
| none | 62.5% | 12/16 |
| repeat_user_prompt | 46.5% | 15/16 |
| spotlighting_with_delimiting | 61.8% | 13/16 |
| tool_filter | 11.1% | 13/16 |
| transformers_pi_detector | 0.7% | 7/16 |

**REM v1.0 replayed on the undefended traces:**
- 2 / 134 attacks and 5 / 15 benign.
- On the same task pairs this is fewer successes than three defences and about as many as the injection classifier, with lower benign completion.
- This comparison is **descriptive only**: the defended agents adapted and REM's replay did not. **No superiority is claimed.**

**Layered on a defence's own traces**, REM removes almost every remaining success: D1 62 → 0, D2 82 → 1, D4 1 → 0. It also removes about half of the benign completions.

**Not available:**
- **tool_filter:** cannot be replayed with the frozen harness.
- **MELON:** not executed (it needs a model, embeddings and a budget).

### 10. What are the strongest and weakest results?

- **Strongest:**
  - exact reproduction;
  - pre-registered ablation showing that REM's protection comes from its learned decision (661 / 0);
  - large and robust ASR reductions in replay;
  - a confirmatory utility gain from removing behavioural evidence;
  - transparent negative results.
- **Weakest:**
  - **utility.** REM v1.0 releases 4 / 89 legitimate payments and completes 31% of benign tasks;
  - simple provenance rules match its security with more utility;
  - all evidence is replay on one benchmark, mostly development data;
  - no closed-loop or LLM-based comparison.

### 11. What is the confirmed scientific contribution?

A transparent, tested instance of a widely proposed design, with:
- a rigorous replay evaluation;
- a pre-registered decomposition of where its protection and its cost come from;
- a descriptive placement against the benchmark's distributed defences;
- documented negative results, showing that the learned, consequence-aware decision buys security by over-withholding, and that representing *what the user authorised* is the limiting factor.

It is an empirical and methodological contribution, not a new algorithm (`15`).

### 12. What limitations remain?

- NO-ADAPT replay; no live agents.
- One benchmark and one attacker account; development-data reuse.
- Few clusters, so the intervals are descriptive.
- Unapproved design values; no human label audit.
- No injection classifier in the Detection Layer.
- No reviewer model.
- External comparison descriptive and with one model.
- tool_filter not replayable; MELON not run.
- University template and proposal file missing.

See `12`.

### 13. What supervisor decisions are needed?

1. **Approval of the frozen design values** (costs, tiers, predicates, features, label rule): SD-FREEZE, D-9.
2. **REM v1.1** (behavioural evidence removed): adopt or keep v1.0 (SD-FEAT).
3. **Authorisation for live experiments** (D-15): a model endpoint, a spending cap, backbone, decoding and repeats. Without it, the thesis is submitted with replay-only evidence and MELON NOT EXECUTED.
4. **Research-question wording** (D-10, still [PD]).
5. **Whether to keep the exploratory extensions** (SD-PERM, SD-AMT, new SD-ARCH for the REM-B family) as exploratory chapters, or move them to future work.
6. **The tool_filter replay:** accept it as not replayable, or authorise a separately labelled adapter.
7. **The university thesis template and formatting rules** (N-9); front-matter items N-1 to N-8.

---

## الملخص العربي للمشرفَين (إجابات الأسئلة الثلاثة عشر)

**الحالة:** الإصدار الثامن من الرسالة (19 تشرين الثاني 2026) **جاهز لمراجعة المشرفَين**، وهو **غير معتمد** ولم يُناقش ولم يُسلَّم بعد.

### 1. ما مشكلة البحث؟

- يمكن خداع وكيل ذكاء اصطناعي مالي يستخدم الأدوات بواسطة **حقن الأوامر غير المباشر**، أي نص مدسوس في مخرجات أداة يتّبعه الوكيل.
- لا يقع الضرر إلا عند تنفيذ استدعاء يغيّر الحالة، كالتحويل أو تعديل الدفعات الدورية أو تغيير كلمة المرور.
- **السؤال:** هل تستطيع طبقة تشغيلية عند حدّ تنفيذ الأدوات أن تقرّر لكل استدعاء السماحَ أو التعديلَ أو التصعيدَ أو الحجب، فتخفّض نجاح الهجمات دون إتلاف العمل المشروع؟ وهل يضيف القرار المتعلَّم المراعي للعواقب قيمةً على القواعد البسيطة؟

### 2. ما REM؟

- إطار من خمس طبقات بين الوكيل وأدواته:
  - المدخلات والسياق؛
  - الكشف؛
  - التحليل السلوكي؛
  - محرك القرار؛
  - التخفيف.
- الملاءمة وإعادة المعايرة تتمّان خارج وقت التشغيل.
- يُكتب سجل تدقيق لكل حكم. أما SHAP الخطي فللتدقيق فقط، ولا يغيّر الحكم.

### 3. كيف يعمل؟

1. **الأدلة.** تُجمع لكل استدعاء أدلة من ثلاث مجموعات: السياق، والسلوك، ومصدر وسائط الاستدعاء (هل جاءت من طلب المستخدم أم من مخرجات غير موثوقة).
2. **التقدير والمعايرة.** يقدّر الانحدار اللوجستي المنتظم درجةً، تُعايَر بطريقة Platt إلى احتمال.
3. **مستوى العاقبة.** يُحدَّد مستوى العاقبة المعلن للأداة.
4. **الشروط.** تطبَّق شروط السياسة D1 وD2.
5. **القرار.** يُختار الحكم الذي يقلّل الخسارة المتوقعة. ثم يطبَّق التخفيف قبل التنفيذ.

### 4. ما الهجمات المعالجة؟

- **المعالَج:** هجمات الحقن غير المباشر في بيئة AgentDojo المصرفية: تسعة أهداف للمهاجم، منها تحويل الأموال وتسريب البيانات وتغيير الدفعات الدورية وكلمة المرور.
- **غير المعالَج:**
  - الهجمات المباشرة على المستخدم؛
  - اختراق الأدوات نفسها؛
  - المهاجم المتكيّف الذي يعرف REM.

### 5. كيف نُفّذ؟

- **الشيفرة:** حزمة بايثون `rem/`، مع 806 اختبارات آلية ناجحة.
- **الدمج:** تُغلَّف أداة تنفيذ AgentDojo.
- **الملاءمة:** ملاءمة متقاطعة تستبعد في كل طيّة هدفاً هجومياً كاملاً.
- **الرفض الآمن:** يرفض البرنامج العمل إذا غابت قيمة تصميم معلنة.
- **إعادة الإنتاج:** أُعيد اليوم إنتاج النتائج المنشورة للإصدار المجمَّد REM v1.0 حرفياً: 11 هجوماً ناجحاً من 2,979، و105 مهام سليمة من 334.

### 6. ما البيانات والمعايير؟

- **المعيار:** AgentDojo 0.1.35 (القطاع المصرفي، 16 مهمة مستخدم × 9 مهام حقن).
- **المجتمع الأساسي:** 3,313 حلقة مسجّلة لوكلاء حقيقيين من 21 نموذجاً.
- **المجتمع الثاني:** 2,113 حلقة استُخدمت مرة واحدة للتأكيد.
- **المقارنة الخارجية:** التشغيلات المسجّلة لـ gpt-4o مع الدفاعات الأربعة الموزّعة مع المعيار.
- **طريقة التقييم:** إعادة تشغيل دون تكيّف الوكيل. **ولم يُشغَّل أي نموذج لغوي حيّ.**

### 7. كيف صُمّمت دراسة الاستئصال؟

- **التسجيل المسبق:** ثُبّت البروتوكول مع بصمات الشيفرة قبل قياس أي ذراع، وبعد التحقق من إعادة الإنتاج.
- **الأذرع:** عشرة أذرع على الحلقات ونماذج الطيّات نفسها:
  - النموذج الكامل؛
  - بدون الأدلة السلوكية؛
  - بدون المعايرة؛
  - بعتبات مستقلة عن العاقبة؛
  - بدون أدلة السياق؛
  - بدون أدلة المصدر؛
  - بدون حكم التعديل؛
  - بدون القرار المتعلَّم؛
  - بدون الشروط؛
  - بدون دفاع.
- **التحليل:** فروق مزدوجة مع فترات ثقة بالإقلاع العنقودي، مع قواعد تفسير مسبقة.

### 8. ما المكوّنات التي أسهمت؟

- **القرار المتعلَّم** هو مصدر الحماية: يمنع 661 من 672 هجوماً ولا يسمح بأي هجوم إضافي، لكنه يكلّف 22.5 نقطة من إنجاز المهام السليمة.
- **قاعدة الخسارة المتوقعة** تمنع 153 هجوماً تسمح بها العتبات، على حساب 19.5 نقطة.
- **الأدلة السلوكية** ذات أثر صافٍ سلبي.
- **المعايرة** لا تحسّن الحماية.
- **حكم التعديل** زائد عن الحاجة بلا مراجع بشري.
- **أدلة السياق والشروط** بلا أثر ملموس.

### 9. كيف يقارَن بالدفاعات الخارجية؟

- **تشغيلات gpt-4o المسجّلة:**

  | الدفاع | نسبة نجاح الهجمات |
  |---|---|
  | بلا دفاع | 62.5% |
  | تكرار طلب المستخدم | 46.5% |
  | التحديد بالفواصل | 61.8% |
  | تصفية الأدوات | 11.1% |
  | مصنِّف الحقن | 0.7% |

- **REM على المسارات غير المحمية (إعادة تشغيل):** هجومان ناجحان من 134، وخمس مهام سليمة من 15.
- **القراءة:** ترك REM هجمات أقل من ثلاثة دفاعات، ونحو العدد نفسه الذي تركه مصنِّف الحقن، مع منفعة أقل.
- **وهي مقارنة وصفية فقط** لأن نوعي الأدلة مختلفان، **ولا يُدّعى أي تفوّق**.
- **غير المنفَّذ:**
  - لم يمكن إعادة تشغيل تصفية الأدوات بالأداة المجمَّدة؛
  - لم يُنفَّذ MELON.

### 10. ما أقوى النتائج وأضعفها؟

- **الأقوى:**
  - إعادة الإنتاج الحرفية؛
  - الاستئصال المسجَّل مسبقاً؛
  - خفض كبير لنجاح الهجمات في إعادة التشغيل؛
  - مكسب منفعة مؤكَّد بإزالة الأدلة السلوكية؛
  - شفافية النتائج السلبية.
- **الأضعف:**
  - المنفعة: لا يُطلَق إلا 4 من 89 دفعة مشروعة؛
  - القواعد البسيطة تماثله أماناً بمنفعة أعلى؛
  - كل الأدلة إعادة تشغيل على معيار واحد.

### 11. ما المساهمة العلمية المؤكَّدة؟

- **ما هي:**
  - تنفيذ شفاف ومختبَر لتصميم شائع؛
  - تقييم صارم؛
  - تفكيك مسجَّل مسبقاً لمصادر حمايته وكلفته؛
  - موقع وصفي بين الدفاعات الموزّعة؛
  - نتائج سلبية موثّقة تبيّن أن العامل الحاسم هو تمثيل ما فوّض به المستخدم.
- **ما ليست:** خوارزمية جديدة.

### 12. ما القيود الباقية؟

- لا وكلاء أحياء؛ معيار واحد؛ إعادة استخدام بيانات التطوير.
- قلّة العناقيد.
- قيم تصميم غير معتمدة؛ لا تدقيق بشري للتسميات.
- غياب مصنِّف الحقن.
- مقارنة خارجية وصفية.
- غياب قالب الجامعة وملف المقترح.

### 13. ما القرارات المطلوبة من المشرفَين؟

1. اعتماد قيم التصميم.
2. اعتماد REM v1.1 أو الإبقاء على v1.0.
3. الإذن بالتجارب الحية مع سقف إنفاق، أو قبول الرسالة دونها.
4. صياغة أسئلة البحث.
5. مصير الامتدادات الاستكشافية.
6. إعادة تشغيل تصفية الأدوات.
7. قالب الجامعة وبيانات الصفحات الأولى.
