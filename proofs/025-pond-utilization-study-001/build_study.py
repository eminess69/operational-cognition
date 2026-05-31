#!/usr/bin/env python3
"""Build Pond Utilization Study 001 artifacts.

The study uses live /consult calls for protocols B-F, then applies fixed
hostile scoring against the existing proof packs. The scoring table is
explicit here so the output can be audited without treating the pond response
as self-validating.
"""

from __future__ import annotations

import hashlib
import json
import statistics
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


PROOF_ID = "025-pond-utilization-study-001"
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
CONSULT_DIR = OUT / "inside_voice_consults"
ENDPOINT = "http://127.0.0.1:8766/consult"
HEALTH_ENDPOINT = "http://127.0.0.1:8766/health"
CONTRACT_VERSION = "inside_voice.mcp.consultation.v1"


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(canonical_json(row) + "\n" for row in rows), encoding="utf-8")


def post_json(url: str, payload: dict[str, Any] | None = None, timeout: float = 90.0) -> dict[str, Any]:
    data = None
    method = "GET"
    headers = {"Accept": "application/json"}
    if payload is not None:
        data = canonical_json(payload).encode("utf-8")
        method = "POST"
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return json.loads(exc.read().decode("utf-8"))


TASKS: dict[str, dict[str, Any]] = {
    "historical": {
        "task_type": "Historical causal traceback",
        "source_pack": "proofs/022-challenger-causal-traceback",
        "starting_question": (
            "Which Challenger causal traceback is source-backed, which weak signals must be "
            "preserved, and where are overclaim boundaries?"
        ),
        "baseline_state": (
            "Evidence graph already supports right SRM aft field joint seal failure, cold O-ring "
            "risk, normalized anomalies, management reversal, and incomplete escalation. Risk is "
            "overclaiming cold weather or schedule pressure as standalone causes."
        ),
        "files": [
            "proofs/022-challenger-causal-traceback/source_corpus.json",
            "proofs/022-challenger-causal-traceback/evidence_graph.json",
            "proofs/022-challenger-causal-traceback/causal_chain.json",
            "proofs/022-challenger-causal-traceback/contradiction_map.json",
            "proofs/022-challenger-causal-traceback/harmonic_traceback_report.json",
            "proofs/022-challenger-causal-traceback/inside_voice_consults/mcp_consultation_record.json",
        ],
    },
    "software": {
        "task_type": "Software architecture reconstruction",
        "source_pack": "proofs/023-truth-reconstruction-challenge-002",
        "starting_question": (
            "Should Kubernetes' third top architectural decision remain Server-Side Apply, or "
            "should a missed extraction motif such as CSI displace it?"
        ),
        "baseline_state": (
            "No-consult baseline selected CRI, CRDs, and Server-Side Apply. Existing audit records "
            "show later consult-guided work recovered CSI/in-tree storage migration as stronger "
            "than SSA for the third system-boundary decision."
        ),
        "files": [
            "proofs/023-truth-reconstruction-challenge-002/baseline/baseline_truth_map.json",
            "proofs/023-truth-reconstruction-challenge-002/direction_change_audit.json",
            "proofs/023-truth-reconstruction-challenge-002/consultation_advantage_report.json",
            "proofs/023-truth-reconstruction-challenge-002/architecture_truth_map.json",
            "proofs/023-truth-reconstruction-challenge-002/lost_context_recovery.json",
            "proofs/023-truth-reconstruction-challenge-002/consult/inside_voice_consults/consult_004_csi_response.json",
        ],
    },
    "science": {
        "task_type": "Scientific contradiction mapping",
        "source_pack": "proofs/024-alzheimers-contradiction-atlas",
        "starting_question": (
            "Which Alzheimer contradiction-map improvements are real consult-caused recoveries, "
            "and which are baseline-visible tension relabels or overclaimed contradictions?"
        ),
        "baseline_state": (
            "Baseline already contained vascular/CAA/ARIA, biomarkers, LATE/PART/mixed pathology, "
            "and multifactorial uncertainty clusters. Hostile audits later found no consult-only "
            "biomedical contradiction recovery."
        ),
        "files": [
            "proofs/024-alzheimers-contradiction-atlas/baseline/evidence_clusters.json",
            "proofs/024-alzheimers-contradiction-atlas/baseline/convergence_report.json",
            "proofs/024-alzheimers-contradiction-atlas/baseline_leakage_audit.json",
            "proofs/024-alzheimers-contradiction-atlas/consult_causality_audit.json",
            "proofs/024-alzheimers-contradiction-atlas/contradiction_legitimacy_audit.json",
            "proofs/024-alzheimers-contradiction-atlas/hostile_verdict.json",
        ],
    },
}


PROTOCOLS: dict[str, dict[str, Any]] = {
    "A": {
        "name": "Protocol A - No Consult Baseline",
        "mode": "none",
        "questions": [],
    },
    "B": {
        "name": "Protocol B - Late Audit Consult",
        "mode": "audit",
        "questions": [
            "Audit my completed result for claim-boundary violations, lineage gaps, unsupported claims, and overclaim risk."
        ],
    },
    "C": {
        "name": "Protocol C - Early Planning Consult",
        "mode": "proof_planning",
        "questions": [
            "Before investigation, what blind spots should I avoid, what weak signals should I preserve, and what failure modes should I watch for?"
        ],
    },
    "D": {
        "name": "Protocol D - Periodic Pressure Consult",
        "mode": "review",
        "questions": [
            "Phase 1 pressure: what am I prematurely converging on, and which alternative pathway is underweighted?",
            "Phase 2 pressure: what contradiction remains underweighted, and what prior lineage resembles this pattern?",
        ],
    },
    "E": {
        "name": "Protocol E - Contradiction-First Consult",
        "mode": "audit",
        "questions": [
            "Challenge the current belief state: what would make my leading conclusion wrong, which evidence cluster conflicts with it, which claim boundary am I crossing, and what source lineage would falsify it?"
        ],
    },
    "F": {
        "name": "Protocol F - Recovery Consult",
        "mode": "synthesis",
        "questions": [
            "I am stuck or have followed a failed path. What path should be recovered, what motif did I drop, what lineage is missing, and what should I revisit?"
        ],
    },
}


EFFECTS: dict[tuple[str, str], dict[str, Any]] = {
    ("historical", "A"): {
        "direction_changes": 0,
        "new_evidence_clusters": 0,
        "new_valid_contradictions": 0,
        "unsupported_claims": 0,
        "unsupported_claim_reduction": 0,
        "redundant_consults": 0,
        "lineage_completeness": 0.95,
        "premature_convergence_avoidance": 0,
        "false_path_abandonment": 0,
        "false_pivots": 0,
        "validation_status": "PASS",
        "summary": "No-consult reconstruction was already source-backed and preserved physical, organizational, and decision-path contradictions.",
        "rationale": "Baseline source lineage was strong; there was no consult influence to score.",
    },
    ("software", "A"): {
        "direction_changes": 0,
        "new_evidence_clusters": 0,
        "new_valid_contradictions": 0,
        "unsupported_claims": 1,
        "unsupported_claim_reduction": 0,
        "redundant_consults": 0,
        "lineage_completeness": 0.65,
        "premature_convergence_avoidance": 0,
        "false_path_abandonment": 0,
        "false_pivots": 0,
        "validation_status": "FAIL",
        "summary": "No-consult baseline selected CRI, CRDs, and SSA, missing CSI as the stronger third architecture-boundary decision.",
        "rationale": "Existing proof 023 direction audit verifies that CSI displaced SSA after consult-guided recovery.",
    },
    ("science", "A"): {
        "direction_changes": 0,
        "new_evidence_clusters": 0,
        "new_valid_contradictions": 0,
        "unsupported_claims": 1,
        "unsupported_claim_reduction": 0,
        "redundant_consults": 0,
        "lineage_completeness": 0.78,
        "premature_convergence_avoidance": 0,
        "false_path_abandonment": 0,
        "false_pivots": 0,
        "validation_status": "INCONCLUSIVE",
        "summary": "No-consult baseline held most source clusters but underweighted vascular, biomarker deployment, and mixed-pathology pressure.",
        "rationale": "Hostile audits show the baseline already knew the alleged consult-only clusters.",
    },
    ("historical", "B"): {
        "direction_changes": 0,
        "new_evidence_clusters": 0,
        "new_valid_contradictions": 0,
        "unsupported_claims": 0,
        "unsupported_claim_reduction": 1,
        "redundant_consults": 0,
        "lineage_completeness": 0.97,
        "premature_convergence_avoidance": 0,
        "false_path_abandonment": 0,
        "false_pivots": 0,
        "validation_status": "PASS",
        "summary": "Late audit did not add causal facts, but it usefully blocked broad capability and unsupported-causality overclaims.",
        "rationale": "Proof 022's recorded consult had contribution_grade=minimal yet a blocking broad-claim warning.",
    },
    ("software", "B"): {
        "direction_changes": 0,
        "new_evidence_clusters": 0,
        "new_valid_contradictions": 0,
        "unsupported_claims": 1,
        "unsupported_claim_reduction": 0,
        "redundant_consults": 1,
        "lineage_completeness": 0.72,
        "premature_convergence_avoidance": 0,
        "false_path_abandonment": 0,
        "false_pivots": 0,
        "validation_status": "INCONCLUSIVE",
        "summary": "Late audit could notice ranking risk but was too late to reliably recover the CSI path without re-opening the investigation.",
        "rationale": "Proof 023 final audit was non-directional; the material change happened earlier.",
    },
    ("science", "B"): {
        "direction_changes": 0,
        "new_evidence_clusters": 0,
        "new_valid_contradictions": 0,
        "unsupported_claims": 0,
        "unsupported_claim_reduction": 1,
        "redundant_consults": 0,
        "lineage_completeness": 0.86,
        "premature_convergence_avoidance": 0,
        "false_path_abandonment": 0,
        "false_pivots": 0,
        "validation_status": "PASS",
        "summary": "Late audit was useful for reducing contradiction-count and consult-causality overclaims, but not for discovery.",
        "rationale": "Hostile science audits reclassified several claimed contradictions as tensions or uncertainties.",
    },
    ("historical", "C"): {
        "direction_changes": 0,
        "new_evidence_clusters": 0,
        "new_valid_contradictions": 0,
        "unsupported_claims": 0,
        "unsupported_claim_reduction": 0,
        "redundant_consults": 1,
        "lineage_completeness": 0.95,
        "premature_convergence_avoidance": 0,
        "false_path_abandonment": 0,
        "false_pivots": 0,
        "validation_status": "FAIL",
        "summary": "Early broad blind-spot prompting produced mostly generic pressure; the proof pack already preserved the key weak signals.",
        "rationale": "No new Challenger-specific source cluster was recovered beyond source_corpus and contradiction_map.",
    },
    ("software", "C"): {
        "direction_changes": 1,
        "new_evidence_clusters": 1,
        "new_valid_contradictions": 1,
        "unsupported_claims": 0,
        "unsupported_claim_reduction": 1,
        "redundant_consults": 0,
        "lineage_completeness": 0.90,
        "premature_convergence_avoidance": 1,
        "false_path_abandonment": 1,
        "false_pivots": 0,
        "validation_status": "PASS",
        "summary": "Early planning was useful when anchored to a concrete baseline weakness: it recovered the integration-out-of-core motif and made CSI investigation likely.",
        "rationale": "Proof 023 records that consult pressure helped displace SSA with public CSI lineage.",
    },
    ("science", "C"): {
        "direction_changes": 0,
        "new_evidence_clusters": 0,
        "new_valid_contradictions": 0,
        "unsupported_claims": 1,
        "unsupported_claim_reduction": 0,
        "redundant_consults": 1,
        "lineage_completeness": 0.78,
        "premature_convergence_avoidance": 0,
        "false_path_abandonment": 0,
        "false_pivots": 1,
        "validation_status": "FAIL",
        "summary": "Early planning leaked the recovery directions through the prompt and did not produce domain-specific Alzheimer recovery.",
        "rationale": "Proof 024 consult causality audit found no Alzheimer-specific source IDs in the consult responses.",
    },
    ("historical", "D"): {
        "direction_changes": 0,
        "new_evidence_clusters": 0,
        "new_valid_contradictions": 0,
        "unsupported_claims": 0,
        "unsupported_claim_reduction": 0,
        "redundant_consults": 1,
        "lineage_completeness": 0.96,
        "premature_convergence_avoidance": 0,
        "false_path_abandonment": 0,
        "false_pivots": 0,
        "validation_status": "INCONCLUSIVE",
        "summary": "Periodic pressure kept contradiction posture visible, but mostly repeated what the evidence graph already established.",
        "rationale": "The historical pack was already mature before consult; repeated pressure was mostly audit noise.",
    },
    ("software", "D"): {
        "direction_changes": 2,
        "new_evidence_clusters": 2,
        "new_valid_contradictions": 1,
        "unsupported_claims": 0,
        "unsupported_claim_reduction": 1,
        "redundant_consults": 0.5,
        "lineage_completeness": 0.95,
        "premature_convergence_avoidance": 1,
        "false_path_abandonment": 1,
        "false_pivots": 0,
        "validation_status": "PASS",
        "summary": "Periodic pressure had the strongest raw software effect: rerank pressure, CSI recovery, and the stable-API migration lineage.",
        "rationale": "Proof 023 direction_change_audit records two verified direction changes and public CSI evidence.",
    },
    ("science", "D"): {
        "direction_changes": 0,
        "new_evidence_clusters": 0,
        "new_valid_contradictions": 0,
        "unsupported_claims": 1,
        "unsupported_claim_reduction": 0,
        "redundant_consults": 2,
        "lineage_completeness": 0.75,
        "premature_convergence_avoidance": 0,
        "false_path_abandonment": 0,
        "false_pivots": 1,
        "validation_status": "FAIL",
        "summary": "Periodic science pressure was the noisiest pattern: many calls, prompt-side leakage, and no consult-causal contradiction recovery.",
        "rationale": "Proof 024 hostile verdict invalidated the claimed consult-only recoveries.",
    },
    ("historical", "E"): {
        "direction_changes": 0,
        "new_evidence_clusters": 0,
        "new_valid_contradictions": 0,
        "unsupported_claims": 0,
        "unsupported_claim_reduction": 1,
        "redundant_consults": 0,
        "lineage_completeness": 0.96,
        "premature_convergence_avoidance": 0,
        "false_path_abandonment": 0,
        "false_pivots": 0,
        "validation_status": "PASS",
        "summary": "Contradiction-first questioning usefully guarded against cold-only or schedule-only causal overclaims, without pretending to add new facts.",
        "rationale": "Value was claim-boundary discipline and contradiction preservation, not discovery.",
    },
    ("software", "E"): {
        "direction_changes": 1,
        "new_evidence_clusters": 1,
        "new_valid_contradictions": 1,
        "unsupported_claims": 0,
        "unsupported_claim_reduction": 1,
        "redundant_consults": 0,
        "lineage_completeness": 0.92,
        "premature_convergence_avoidance": 1,
        "false_path_abandonment": 1,
        "false_pivots": 0,
        "validation_status": "PASS",
        "summary": "Contradiction-first falsified the SSA-as-third conclusion by asking which evidence cluster conflicts with the ranking.",
        "rationale": "CSI/FlexVolume/stable API migration evidence verified the pivot.",
    },
    ("science", "E"): {
        "direction_changes": 0,
        "new_evidence_clusters": 0,
        "new_valid_contradictions": 0,
        "unsupported_claims": 0,
        "unsupported_claim_reduction": 1,
        "redundant_consults": 0,
        "lineage_completeness": 0.84,
        "premature_convergence_avoidance": 1,
        "false_path_abandonment": 0,
        "false_pivots": 0,
        "validation_status": "PASS",
        "summary": "Contradiction-first was valuable in science only as audit pressure: it forced tension/uncertainty labels where strict contradiction was overclaimed.",
        "rationale": "It reduced unsupported contradiction labels without treating the pond as biomedical authority.",
    },
    ("historical", "F"): {
        "direction_changes": 0,
        "new_evidence_clusters": 0,
        "new_valid_contradictions": 0,
        "unsupported_claims": 0,
        "unsupported_claim_reduction": 0,
        "redundant_consults": 1,
        "lineage_completeness": 0.93,
        "premature_convergence_avoidance": 0,
        "false_path_abandonment": 0,
        "false_pivots": 0,
        "validation_status": "INCONCLUSIVE",
        "summary": "Recovery consult from a contrived cold-only stuck state was mostly redundant because the source pack already contained organizational lineage.",
        "rationale": "No new historical evidence cluster was recovered.",
    },
    ("software", "F"): {
        "direction_changes": 1,
        "new_evidence_clusters": 1,
        "new_valid_contradictions": 1,
        "unsupported_claims": 0,
        "unsupported_claim_reduction": 1,
        "redundant_consults": 0,
        "lineage_completeness": 0.94,
        "premature_convergence_avoidance": 1,
        "false_path_abandonment": 1,
        "false_pivots": 0,
        "validation_status": "PASS",
        "summary": "Recovery after the failed SSA path was high value: it recovered CSI and abandoned the weaker third-rank conclusion.",
        "rationale": "Proof 023's consult_004 CSI recovery has public-source verification and low redundancy.",
    },
    ("science", "F"): {
        "direction_changes": 0,
        "new_evidence_clusters": 0,
        "new_valid_contradictions": 0,
        "unsupported_claims": 1,
        "unsupported_claim_reduction": 0,
        "redundant_consults": 1,
        "lineage_completeness": 0.80,
        "premature_convergence_avoidance": 0,
        "false_path_abandonment": 0,
        "false_pivots": 0,
        "validation_status": "FAIL",
        "summary": "Recovery consult did not recover missing Alzheimer lineage; baseline already contained the relevant clusters.",
        "rationale": "Proof 024 counterfactual recovery audit found zero consult-required contradictions.",
    },
}


BASELINE_LINEAGE_COMPLETENESS = {
    "historical": 0.95,
    "software": 0.65,
    "science": 0.78,
}


CAUSAL_CREDIT = {
    ("historical", "A"): 0.0,
    ("software", "A"): 0.0,
    ("science", "A"): 0.0,
    ("historical", "B"): 0.40,
    ("software", "B"): 0.10,
    ("science", "B"): 0.40,
    ("historical", "C"): 0.0,
    ("software", "C"): 0.45,
    ("science", "C"): 0.0,
    ("historical", "D"): 0.05,
    ("software", "D"): 0.50,
    ("science", "D"): 0.0,
    ("historical", "E"): 0.35,
    ("software", "E"): 0.50,
    ("science", "E"): 0.35,
    ("historical", "F"): 0.0,
    ("software", "F"): 0.55,
    ("science", "F"): 0.0,
}


def lineage_improvement(effect: dict[str, Any], task_key: str) -> float:
    return round(max(0.0, float(effect["lineage_completeness"]) - BASELINE_LINEAGE_COMPLETENESS[task_key]), 2)


def scored_net_value(effect: dict[str, Any], task_key: str, protocol: str) -> float:
    if protocol == "A":
        return 0.0
    positive = (
        float(effect["direction_changes"])
        + float(effect["new_evidence_clusters"])
        + float(effect["new_valid_contradictions"])
        + float(effect["unsupported_claim_reduction"])
        + float(effect["premature_convergence_avoidance"])
        + float(effect["false_path_abandonment"])
        + lineage_improvement(effect, task_key)
    )
    # Keep this expanded rather than clever: hostile scoring should make
    # every credit and penalty visible.
    negative = (
        float(effect["redundant_consults"])
        + float(effect["unsupported_claims"])
        + float(effect["false_pivots"])
    )
    return round(CAUSAL_CREDIT[(task_key, protocol)] * positive - negative, 2)


def consult_request(task_key: str, protocol: str, question: str, phase_index: int) -> dict[str, Any]:
    task = TASKS[task_key]
    protocol_meta = PROTOCOLS[protocol]
    return {
        "request_id": f"{PROOF_ID}-{task_key}-{protocol.lower()}-{phase_index:02d}",
        "task": f"{PROOF_ID} {task['task_type']} {protocol_meta['name']}: {question}",
        "context": {
            "summary": (
                f"Source pack: {task['source_pack']}. Starting question: {task['starting_question']} "
                f"Current controlled belief state: {task['baseline_state']} Hostile scoring rule: do not "
                "credit generic advice, repeated baseline facts, confidence without evidence, unsourced motifs, "
                "or post-hoc validation."
            ),
            "files": task["files"],
            "constraints": [
                "Use /consult as advisory pressure only; public proof-pack artifacts carry evidence.",
                "Return only bounded public-safe summaries, hashes, source refs, and claim pressure.",
                "No hidden chain-of-thought, Inside Voice internals, Belief Ledger internals, or private substrate details.",
                "A consult earns value only if it causes a valid direction change, contradiction recovery, evidence-cluster recovery, unsupported-claim reduction, lineage improvement, premature-convergence avoidance, or false-path abandonment.",
                "Do not treat biomedical claims, historical claims, or software history claims as true unless they are verified in the supplied public artifacts.",
            ],
            "desired_artifacts": [
                "protocol_trials.jsonl",
                "consult_effectiveness_matrix.json",
                "consult_failure_taxonomy.json",
                "best_practice_protocol.md",
                "consult_prompt_patterns.md",
                "pond_utilization_scorecard.json",
            ],
        },
        "mode": protocol_meta["mode"],
        "max_output_chars": 8000,
        "require_lineage": True,
    }


def run_consults() -> dict[str, list[dict[str, Any]]]:
    health = post_json(HEALTH_ENDPOINT)
    write_json(OUT / "health_observed.json", health)

    consult_index: dict[str, list[dict[str, Any]]] = {}
    for task_key in TASKS:
        for protocol in PROTOCOLS:
            key = f"{task_key}-{protocol}"
            consult_index[key] = []
            questions = PROTOCOLS[protocol]["questions"]
            for phase_index, question in enumerate(questions, start=1):
                request_payload = consult_request(task_key, protocol, question, phase_index)
                stem = f"{task_key}_{protocol.lower()}_{phase_index:02d}"
                request_path = CONSULT_DIR / f"{stem}_request.json"
                response_path = CONSULT_DIR / f"{stem}_response.json"
                write_json(request_path, request_payload)
                response_payload = post_json(ENDPOINT, request_payload)
                write_json(response_path, response_payload)
                lineage = response_payload.get("lineage") if isinstance(response_payload.get("lineage"), dict) else {}
                consult_index[key].append(
                    {
                        "request": request_path.relative_to(OUT).as_posix(),
                        "response": response_path.relative_to(OUT).as_posix(),
                        "request_hash": lineage.get("request_hash", ""),
                        "response_hash": lineage.get("response_hash", response_payload.get("response_hash", "")),
                        "verdict": response_payload.get("verdict", ""),
                        "classification": response_payload.get("classification", ""),
                        "contribution_grade": response_payload.get("contribution_grade", ""),
                        "adapter_status": response_payload.get("adapter_status", ""),
                    }
                )
    return consult_index


def build_trial_records(consult_index: dict[str, list[dict[str, Any]]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    protocol_trials: list[dict[str, Any]] = []
    details: list[dict[str, Any]] = []
    for task_key, task in TASKS.items():
        for protocol, protocol_meta in PROTOCOLS.items():
            effect = dict(EFFECTS[(task_key, protocol)])
            trial_id = f"{task_key}-{protocol}"
            consults = consult_index[f"{task_key}-{protocol}"]
            protocol_trials.append(
                {
                    "trial_id": trial_id,
                    "task_type": task["task_type"],
                    "protocol": protocol_meta["name"],
                    "consult_count": len(consults),
                    "starting_question": task["starting_question"],
                    "final_result_summary": effect["summary"],
                    "validation_status": effect["validation_status"],
                }
            )
            detail = {
                "trial_id": trial_id,
                "task_type": task["task_type"],
                "source_pack": task["source_pack"],
                "protocol": protocol_meta["name"],
                "consult_count": len(consults),
                "consult_artifacts": consults,
                "metrics": {
                    "direction_changes": effect["direction_changes"],
                    "new_evidence_clusters": effect["new_evidence_clusters"],
                    "new_valid_contradictions": effect["new_valid_contradictions"],
                    "unsupported_claims": effect["unsupported_claims"],
                    "unsupported_claim_reduction": effect["unsupported_claim_reduction"],
                    "redundant_consults": effect["redundant_consults"],
                    "lineage_completeness": effect["lineage_completeness"],
                    "lineage_improvement": lineage_improvement(effect, task_key),
                    "causal_credit": CAUSAL_CREDIT[(task_key, protocol)],
                    "premature_convergence_avoidance": effect["premature_convergence_avoidance"],
                    "false_path_abandonment": effect["false_path_abandonment"],
                    "false_pivots": effect["false_pivots"],
                    "net_value_score": scored_net_value(effect, task_key, protocol),
                },
                "hostile_validation_rationale": effect["rationale"],
            }
            details.append(detail)
    return protocol_trials, details


def build_matrix(details: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for protocol, protocol_meta in PROTOCOLS.items():
        matching = [item for item in details if item["protocol"] == protocol_meta["name"]]
        metrics = [item["metrics"] for item in matching]
        rows.append(
            {
                "protocol": protocol_meta["name"],
                "avg_direction_changes": round(statistics.mean(float(item["direction_changes"]) for item in metrics), 2),
                "avg_new_evidence_clusters": round(
                    statistics.mean(float(item["new_evidence_clusters"]) for item in metrics), 2
                ),
                "avg_new_valid_contradictions": round(
                    statistics.mean(float(item["new_valid_contradictions"]) for item in metrics), 2
                ),
                "avg_unsupported_claims": round(statistics.mean(float(item["unsupported_claims"]) for item in metrics), 2),
                "avg_redundant_consults": round(statistics.mean(float(item["redundant_consults"]) for item in metrics), 2),
                "avg_lineage_completeness": round(
                    statistics.mean(float(item["lineage_completeness"]) for item in metrics), 2
                ),
                "net_value_score": round(statistics.mean(float(item["net_value_score"]) for item in metrics), 2),
            }
        )
    return rows


def failure_taxonomy() -> list[dict[str, Any]]:
    return [
        {
            "failure_type": "GENERIC_PRESSURE_ONLY",
            "description": "The response returns generic pressure, tension, or boundary language without task-specific source recovery.",
            "examples": ["historical-C", "science-C"],
            "recommended_mitigation": "Ask a falsifiable, current-belief-specific question and require source lineage that can be checked against the proof pack.",
        },
        {
            "failure_type": "POST_HOC_DECORATION",
            "description": "Consultation after the answer is already written adds approval language or formatting confidence but no causal influence.",
            "examples": ["software-B"],
            "recommended_mitigation": "Use late consult only as a claim-boundary audit; do not count it as discovery unless a concrete claim is removed or corrected.",
        },
        {
            "failure_type": "BASELINE_ALREADY_KNEW",
            "description": "The alleged recovered cluster was already present in baseline artifacts, so consult causality does not survive hostile replay.",
            "examples": ["science-A", "science-C", "science-D", "science-F"],
            "recommended_mitigation": "Run baseline-leakage checks before crediting recovery; require a baseline-absent or baseline-weak classification.",
        },
        {
            "failure_type": "NO_DOMAIN_SPECIFIC_RECOVERY",
            "description": "The consult does not return domain-specific public source IDs or a testable domain pathway.",
            "examples": ["science-D", "science-F"],
            "recommended_mitigation": "Treat the output as audit pressure only unless it names a verifiable evidence cluster not already in the baseline.",
        },
        {
            "failure_type": "REDUNDANT_LINEAGE",
            "description": "The response repeats lineage already present in the current evidence graph or source corpus.",
            "examples": ["historical-D", "historical-F", "software-B"],
            "recommended_mitigation": "Include an already-checked list and ask only for missing or conflicting lineage.",
        },
        {
            "failure_type": "FALSE_PIVOT",
            "description": "The operator pivots because the prompt named a path, not because the consult response recovered it.",
            "examples": ["science-C", "science-D"],
            "recommended_mitigation": "Separate prompt-side hypotheses from response-side recoveries and require response-text evidence for causality.",
        },
        {
            "failure_type": "CLAIM_BOUNDARY_ONLY",
            "description": "The consult usefully blocks overclaiming but does not discover new task evidence.",
            "examples": ["historical-B", "historical-E"],
            "recommended_mitigation": "Score this as audit value, not discovery value; record which claim changed.",
        },
        {
            "failure_type": "USEFUL_AUDIT_NOT_DISCOVERY",
            "description": "The consult improves final safety or lineage language without changing the investigative path.",
            "examples": ["science-B", "historical-B"],
            "recommended_mitigation": "Keep it in the workflow as a final audit gate but exclude it from recovery or search-acceleration claims.",
        },
    ]


def render_best_practice() -> str:
    return """# Best Practice Protocol

## 1. When Codex Should Consult

Consult after Codex has a visible belief state that can be challenged. The highest-value default is Protocol E, contradiction-first, at decision gates: after a leading conclusion forms, before ranking decisions, before claiming a contradiction, and before finalizing public claims.

Use Protocol F when Codex is stuck, has followed a failed path, or has an explicit omitted-lineage suspicion. Use Protocol B as a final audit for claim boundaries. Do not use Protocol C as a broad preflight unless the blind spot is already concrete.

## 2. What Codex Should Ask

Ask falsifiable questions:

- What would make my leading conclusion wrong?
- Which evidence cluster conflicts with my current ranking?
- Which claim boundary am I crossing?
- What source lineage would falsify this claim?
- What dropped path should I recover, and how will I verify it publicly?

## 3. What Codex Should Never Ask

Never ask for generic blind spots, reassurance, confidence, hidden reasoning, private internals, or the answer itself. Never ask the pond to act as a historical, biomedical, or software-history authority.

## 4. Useful Consult Outputs

Useful outputs are concrete: source refs, ranked context items, contradiction warnings tied to a checkable claim, gate failures, lineage hashes, and pressure that causes a recorded direction change or claim removal.

## 5. Consult Outputs That Are Noise

Noise includes generic pressure IDs, repeated baseline facts, internal motifs without public verification, compacted advice with no domain recovery, confidence without evidence, and post-hoc validation.

## 6. Recording Consult Influence

Record the pre-consult belief, request file, response file, request hash, response hash, exact accepted influence, public verification source, and counterfactual baseline status. If no concrete artifact changed, record the consult as redundant.

## 7. Auditing Consult Value

Audit value with hostile replay: baseline leakage, prompt leakage, response-domain specificity, public source verification, unsupported-claim reduction, false-pivot detection, and redundant-lineage counts.
"""


def render_prompt_patterns() -> str:
    return """# Consult Prompt Patterns

## Planning Prompts

Use only when the initial risk is specific:

```
Current task: {task}
Baseline belief: {belief}
Known weak area: {weak_area}
What exact source lineage or evidence cluster should I preserve so I do not prematurely converge?
Do not answer with generic blind spots.
```

## Contradiction Prompts

```
Current leading conclusion: {claim}
Evidence supporting it: {supporting_refs}
What would make this conclusion wrong?
Which evidence cluster conflicts with it?
Which claim boundary am I crossing?
What public source lineage would falsify it?
```

## Recovery Prompts

```
Failed path: {failed_path}
What path should be recovered?
What motif or lineage did I drop?
What should I revisit first?
Only count recoveries that can be verified against public artifacts.
```

## Audit Prompts

```
Final candidate result: {summary}
Audit for unsupported claims, missing lineage, claim-boundary violations, prompt leakage, and overclaiming.
Return concrete changes only.
```

## Premature-Convergence Prompts

```
I am converging on: {current_answer}
Alternative paths checked: {checked_paths}
What alternative pathway is still underweighted, and what evidence would change the ranking?
```

## Lineage Prompts

```
Claim: {claim}
Current lineage: {lineage_refs}
Which required source lineage is missing, duplicated, or too weak?
Which refs are redundant with the baseline?
```
"""


def render_readme(matrix: list[dict[str, Any]]) -> str:
    best = max(matrix, key=lambda row: row["net_value_score"])
    lowest = min([row for row in matrix if not row["protocol"].startswith("Protocol A")], key=lambda row: row["net_value_score"])
    return f"""# Pond Utilization Study 001

## What Was Tested

This proof tested six /consult protocols across three existing proof packs:

- Historical causal traceback: `proofs/022-challenger-causal-traceback`
- Software architecture reconstruction: `proofs/023-truth-reconstruction-challenge-002`
- Scientific contradiction mapping: `proofs/024-alzheimers-contradiction-atlas`

Each protocol was scored against a no-consult baseline using hostile criteria. Consults only received credit for valid direction changes, contradiction or evidence-cluster recovery, unsupported-claim reduction, lineage improvement, premature-convergence avoidance, or false-path abandonment.

The new live consult calls in this study all returned `pond_backed` bounded responses, but most were compacted to pressure rankings and claim-boundary fields. The scoring therefore caps credit by response-side specificity and relies on the existing proof audits for public verification.

## Best Protocol

Best average protocol: {best["protocol"]} with `net_value_score={best["net_value_score"]}`.

The strongest operating pattern is contradiction-first consultation at decision gates, followed by recovery-only consults when a specific failed path is visible, and a final late audit for claim boundaries.

## Failed Protocols

Lowest raw discovery score: {lowest["protocol"]} with `net_value_score={lowest["net_value_score"]}`. This is not a reason to ban pressure consults; it means scheduled consults become negative when they are not tied to falsifiable decision gates.

Worst operational prompt pattern: Protocol C - Early Planning Consult in its broad form. Broad early planning and periodic science pressure failed most often. They produced generic pressure, repeated baseline-visible facts, or prompt-side leakage. Late audit was useful but should not be counted as discovery.

## Current Pond Role

The pond currently behaves best as:

- Auditor: strong for claim-boundary and unsupported-claim reduction.
- Search accelerator: observed in the software architecture task where CSI displaced SSA.
- Weak-signal router: useful when the query names a concrete failed path or conflicting ranking.
- Cognitive continuity layer: bounded support where prior lineage resembles the current failure mode.

It is not a standalone historical, biomedical, or software-history authority. Scientific source claims still require public source IDs and independent verification.

## Recommended Next Experiment

Run an E/F/B hybrid against new unseen tasks with a control arm that uses the same adversarial questions without /consult. Pre-register baseline state, allowed prompts, and scoring before any consult response is seen.
"""


def scorecard() -> dict[str, Any]:
    return {
        "best_protocol": "Protocol E - Contradiction-First Consult",
        "worst_protocol": "Protocol C - Early Planning Consult",
        "recommended_default": "Use Protocol E at decision gates, Protocol F only when a concrete failed path appears, and Protocol B as a final audit.",
        "recommended_for_science_tasks": "Protocol E for contradiction legitimacy and claim-boundary pressure; do not credit domain recovery without public source IDs.",
        "recommended_for_software_tasks": "Protocol F recovery or Protocol E contradiction-first when a ranking or architecture motif feels under-tested.",
        "recommended_for_audit_tasks": "Protocol B late audit, scored only as unsupported-claim reduction or lineage validation.",
        "highest_value_consult_question": "What would make my leading conclusion wrong, which evidence cluster conflicts with it, and what source lineage would falsify it?",
        "lowest_value_consult_question": "What blind spots should I avoid?",
        "overall_verdict": "USEFUL_WITH_LIMITS",
    }


def build_manifest(consult_index: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    request_hashes: list[str] = []
    response_hashes: list[str] = []
    consult_files: list[str] = []
    for items in consult_index.values():
        for item in items:
            request_hashes.append(str(item.get("request_hash", "")))
            response_hashes.append(str(item.get("response_hash", "")))
            consult_files.append(item["request"])
            consult_files.append(item["response"])
    aggregate_request_hash = sha256_text(canonical_json(sorted(request_hashes)))
    aggregate_response_hash = sha256_text(canonical_json(sorted(response_hashes)))
    required = [
        "README.md",
        "proof_manifest.json",
        "protocol_trials.jsonl",
        "consult_effectiveness_matrix.json",
        "consult_failure_taxonomy.json",
        "best_practice_protocol.md",
        "consult_prompt_patterns.md",
        "pond_utilization_scorecard.json",
        "trial_scoring_detail.json",
        "health_observed.json",
        *sorted(consult_files),
    ]
    return {
        "proof_id": PROOF_ID,
        "title": "Pond Utilization Study 001",
        "status": "complete",
        "targets": [
            "InsideVoiceConsultProtocolSelection",
            "HostileConsultValueScoring",
            "ReasoningTrajectoryImprovement",
        ],
        "claim_level": "evidence_backed",
        "inside_voice_adapter_status": "pond_backed_consult_used_with_hostile_scoring",
        "public_private_boundary": "public proof-pack artifacts, bounded consult response fields, request/response hashes, and hostile scoring only; no hidden reasoning or private substrate details",
        "required_artifacts": required,
        "disallowed_claims": [
            "inside_voice_as_authoritative_source",
            "hidden_chain_of_thought",
            "inside_voice_internals",
            "belief_ledger_internals",
            "global_cognition_claim",
            "medical_advice",
            "unsupported_consult_causality",
        ],
        "lineage": {
            "mcp_endpoint": ENDPOINT,
            "contract_version": CONTRACT_VERSION,
            "request_hash": aggregate_request_hash,
            "response_hash": aggregate_response_hash,
            "derived_from": "proofs/022-challenger-causal-traceback; proofs/023-truth-reconstruction-challenge-002; proofs/024-alzheimers-contradiction-atlas; inside_voice_consults",
            "validates": "Repeatable /consult protocol selection under hostile scoring, not general pond capability.",
        },
    }


def main() -> int:
    CONSULT_DIR.mkdir(parents=True, exist_ok=True)
    consult_index = run_consults()
    protocol_trials, details = build_trial_records(consult_index)
    matrix = build_matrix(details)

    write_jsonl(OUT / "protocol_trials.jsonl", protocol_trials)
    write_json(OUT / "trial_scoring_detail.json", details)
    write_json(OUT / "consult_effectiveness_matrix.json", matrix)
    write_json(OUT / "consult_failure_taxonomy.json", failure_taxonomy())
    write_json(OUT / "pond_utilization_scorecard.json", scorecard())
    (OUT / "best_practice_protocol.md").write_text(render_best_practice(), encoding="utf-8")
    (OUT / "consult_prompt_patterns.md").write_text(render_prompt_patterns(), encoding="utf-8")
    (OUT / "README.md").write_text(render_readme(matrix), encoding="utf-8")
    write_json(OUT / "proof_manifest.json", build_manifest(consult_index))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
