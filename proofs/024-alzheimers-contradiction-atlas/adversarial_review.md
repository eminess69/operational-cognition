# Hostile Verification Review

This review uses only `proofs/024-alzheimers-contradiction-atlas`. It does not add sources, modify the corpus, or run new consultations.

## Strongest Criticism

The proof does not demonstrate consultation-caused Alzheimer contradiction recovery. The consult responses logged in `consult/consultation_log.jsonl` contain generic pressure IDs, internal lineage refs, public/private boundary warnings, and output-compaction warnings. They do not return Alzheimer-specific contradictions such as ARIA, CAA, LATE, PART, blood biomarker thresholds, or mixed pathology.

The alleged consult effects are mostly encoded outside the consult response. The consult request prompts themselves contain steering text such as checking vascular amyloid, CAA, microbleeds, ARIA, biomarker-clinical disconnects, LATE, PART, and mixed pathology. The builder then maps each consultation to a predetermined action. That is not strong evidence that Inside Voice recovered the contradiction; it is consistent with the author prompting the expected search path and later attributing it to consultation.

The baseline already contained most of the supposedly recovered material. `baseline/convergence_report.json` explicitly names vascular therapy relevance, blood biomarker deployment uncertainty, and mixed-pathology sources. `baseline/evidence_clusters.json` already contains the CAA/vascular, blood biomarker, and LATE/PART/mixed-pathology clusters. Under hostile assumptions, the consult-only recovery claim collapses.

## Weakest Evidence

The weakest evidence is the consultation causality evidence. The response fields are bounded and generic. `returned_contradictions` is populated by boundary warnings such as unresolved tensions remaining open, not by Alzheimer-domain content. `returned_lineages` point to internal proof/pond artifacts rather than public Alzheimer sources. This supports a claim-boundary audit, not a biomedical contradiction-recovery event.

Several source-lineage claims are also weak. APOE pleiotropy is counted as contradiction even though it is compatible with amyloid biology. Mitochondrial upstream/downstream ordering is uncertainty, not contradiction. Blood biomarker threshold uncertainty is implementation uncertainty, not contradiction. Synaptic symptom evidence and pathology endpoint evidence operate at different measurement levels and do not inherently conflict.

## Likely Overclaims

The `VERY_STRONG_SIGNAL` verdict is overclaimed. The proof reports four new correct contradictions after consult, but the hostile audit finds that three were baseline-present and one was baseline-weak. None is baseline-absent.

The consultation advantage score is inflated by counting semantic relabeling as recovery. CON-003, CON-009, and CON-010 are variants of biomarker classification versus mixed-pathology heterogeneity. CON-001, CON-004, and CON-012 are variants of pathology or biomarker evidence versus clinical/symptom/function outcomes. CON-011 is an umbrella restatement of the whole multifactorial uncertainty boundary.

The source corpus size is not proof quality. The audit finds all cited source IDs exist, but source existence does not prove each source supports the contradiction. Some sources support background association, method development, or implementation uncertainty rather than the asserted conflict.

## Unsupported Assumptions

The proof assumes that a consult call made before a pivot caused the pivot. The logged responses do not support that assumption.

The proof assumes that underweighted baseline evidence counts as consult recovery. A hostile standard does not allow this; if the baseline already named the source cluster or pressure test, the recovery is not consult-only.

The proof assumes that uncertainty, compatibility, or multi-level measurement disagreement can be counted as contradiction. That inflates the contradiction count.

The proof assumes that stronger final synthesis implies consultation advantage. It could instead reflect second-pass analysis over the same corpus.

## Alternative Explanations

The final atlas likely improved because the second pass was adversarial and because the consult prompts themselves named the missing directions. That is search-prompt improvement, not demonstrated Inside Voice recovery.

The apparent contradiction expansion likely comes from splitting broad uncertainty clusters into finer labels. Biomarker heterogeneity, vascular interaction, and amyloid/tau clinical translation were already in the baseline.

The proof may be measuring the benefit of a hostile audit checklist rather than consultation-induced cognition. A non-consult second pass using the same adversarial questions could probably recover the same contradictions from the baseline files.
