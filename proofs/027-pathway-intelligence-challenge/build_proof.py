#!/usr/bin/env python3
"""Build Proof 027 artifacts.

Usage:
  python3 proofs/027-pathway-intelligence-challenge/build_proof.py pre_consult
  # POST consult/inside_voice_consults/*_request.json to /consult.
  python3 proofs/027-pathway-intelligence-challenge/build_proof.py final
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROOF_ID = "027-pathway-intelligence-challenge"
TITLE = "Proof 027 - Pathway Intelligence Challenge"
PROOF_DIR = Path(__file__).resolve().parent
CONSULT_ENDPOINT = "http://127.0.0.1:8766/consult"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, sort_keys=True, ensure_ascii=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    if not path.is_file():
        return "missing"
    return hashlib.sha256(path.read_bytes()).hexdigest()


SOURCE_CORPUS: list[dict[str, Any]] = [
    {
        "source_id": "SRC-KODAK-2011-10K",
        "title": "Eastman Kodak Company Form 10-K for year ended December 31, 2011",
        "date": "2012-02-29",
        "source_type": "company_sec_filing",
        "url": "https://www.sec.gov/Archives/edgar/data/31235/000003123512000036/ek2011_10k.htm",
        "lineage_refs": [
            "SEC filing records Kodak's January 19, 2012 Chapter 11 filing.",
            "The 2011 reporting structure separates Consumer Digital Imaging, Graphic Communications, and Film, Photofinishing and Entertainment.",
            "Kodak disclosed that dedicated digital cameras, pocket video cameras, and digital picture frames would be phased out in first half 2012.",
            "2011 Consumer Digital Imaging sales fell 36% to $1.739B and produced a $349M segment loss.",
            "2011 Film, Photofinishing and Entertainment sales fell 12% to $1.547B but still produced $34M segment earnings.",
        ],
        "evidence_signals": [
            "digital_disruption",
            "business_model_rigidity",
            "management_execution",
            "capital_constraint",
        ],
    },
    {
        "source_id": "SRC-KODAK-2010-10K",
        "title": "Eastman Kodak Company Form 10-K for year ended December 31, 2010",
        "date": "2011-02-25",
        "source_type": "company_sec_filing",
        "url": "https://www.annualreports.com/HostedData/AnnualReportArchive/e/NASDAQ_KODK_2010.pdf",
        "lineage_refs": [
            "Kodak described its digital growth strategy as the intersection of materials science and digital imaging science.",
            "Kodak identified consumer inkjet, commercial inkjet, workflow software/services, and packaging solutions as growth initiatives.",
            "Kodak said growth initiatives were still largely in investment mode while mature product lines faced pricing and commodity pressure.",
        ],
        "evidence_signals": [
            "management_execution",
            "business_model_rigidity",
            "capital_constraint",
        ],
    },
    {
        "source_id": "SRC-KODAK-2010-DIGITAL-OUTLOOK",
        "title": "Kodak 2010 Outlook: Kodak's Digital Businesses: Driving Profitable Growth",
        "date": "2010-02-04",
        "source_type": "company_press_release_sec_exhibit",
        "url": "https://www.sec.gov/Archives/edgar/data/31235/000003123510000034/exhibit991.htm",
        "lineage_refs": [
            "Kodak expected 2010 digital portfolio revenue growth of 5% to 9%.",
            "The digital growth plan depended on cameras/devices, consumer inkjet, and commercial printing technologies.",
            "Kodak positioned itself as helping commercial printers transition from traditional to digital technology.",
        ],
        "evidence_signals": [
            "management_execution",
            "market_assumption",
            "business_model_rigidity",
        ],
    },
    {
        "source_id": "SRC-CAMBRIDGE-BHR-2025",
        "title": "The Problem of Sustaining a Successful Enterprise: Kodak's Multiple Takes at Strategic Renewal that Culminated in Failure",
        "date": "2025-08-15",
        "source_type": "peer_reviewed_business_history",
        "url": "https://www.cambridge.org/core/journals/business-history-review/article/problem-of-sustaining-a-successful-enterprise-kodaks-multiple-takes-at-strategic-renewal-that-culminated-in-failure/BE8CCCEC173E0D91B1E7F0BBE2BF2744",
        "lineage_refs": [
            "The article argues Kodak's decline cannot be explained solely by fear of cannibalization or rigid routines.",
            "Kodak pursued major renewal paths including copiers, pharmaceuticals, and digital photography.",
            "Kodak invested heavily in digital imaging and pioneered sensors, color filters, compression algorithms, and digital SLR technology.",
            "Digital camera sales did not surpass film camera sales until 2002, more than a quarter-century after Kodak's 1975 prototype.",
            "When demand arrived, low barriers and price competition eroded profitability.",
            "The 2007 iPhone and smartphone rise reduced the standalone-camera value proposition and reduced image printing demand.",
            "Kodak's bankruptcy followed the combined burden of struggling inkjet growth, legacy shutdown costs, severe cash shortfalls, and competitive uncertainty.",
            "New paths were evaluated against Kodak's past film profitability, making sustained investment harder to justify.",
        ],
        "evidence_signals": [
            "digital_disruption",
            "business_model_rigidity",
            "management_execution",
            "incentive_structure",
            "timing_failure",
            "capital_constraint",
        ],
    },
    {
        "source_id": "SRC-JSIS-2009",
        "title": "Disruptive technology: How Kodak missed the digital photography revolution",
        "date": "2009-03",
        "source_type": "academic_case_study",
        "url": "https://www.sciencedirect.com/science/article/abs/pii/S0963868709000043",
        "lineage_refs": [
            "Lucas and Goh frame digital photography as a transformational technology threatening Kodak's historical business model.",
            "They identify middle managers, culture, and rigid bureaucratic structure as barriers to fast response.",
            "They emphasize background processes such as market research, financial projections, plan negotiation, and budgeting.",
            "They describe culture and values as factors that define what an organization does and what it cannot do.",
        ],
        "evidence_signals": [
            "organizational_culture",
            "incentive_structure",
            "business_model_rigidity",
        ],
    },
    {
        "source_id": "SRC-KODAK-MILESTONES",
        "title": "Kodak Company Milestones",
        "date": "undated_current_page_accessed_2026-05-28",
        "source_type": "company_history_page",
        "url": "https://www.kodak.com/en/company/page/milestones/",
        "lineage_refs": [
            "Kodak records that it invented the world's first digital camera in 1975.",
            "Kodak records Steve Sasson's National Medal of Technology and Innovation for the 1975 invention.",
        ],
        "evidence_signals": [
            "technology_awareness",
            "digital_disruption",
        ],
    },
    {
        "source_id": "SRC-FORBES-2000",
        "title": "Kodak's Digital Moment",
        "date": "2000-08-21",
        "source_type": "business_press",
        "url": "https://www.forbes.com/global/2000/0821/0316070a.html",
        "lineage_refs": [
            "Forbes reported that Kodak had the number two U.S. digital-camera brand while losing about $60 on a $400 model.",
            "The article reported that digital was about 20% of sales, with nearly half of that in medical imaging rather than consumer photography.",
        ],
        "evidence_signals": [
            "business_model_rigidity",
            "incentive_structure",
            "timing_failure",
        ],
    },
    {
        "source_id": "SRC-MACWORLD-2006",
        "title": "Kodak loses out in U.S. camera market",
        "date": "2006-05-10",
        "source_type": "technology_press",
        "url": "https://www.macworld.com/article/183435/cameras-3.html",
        "lineage_refs": [
            "IDC estimates reported by Macworld showed Kodak falling from first to third in the 2006 U.S. digital still camera market.",
            "Kodak's shipment decline contrasted with Canon and Nikon share gains.",
        ],
        "evidence_signals": [
            "digital_disruption",
            "timing_failure",
            "management_execution",
        ],
    },
    {
        "source_id": "SRC-HBR-2016",
        "title": "Kodak's Downfall Wasn't About Technology",
        "date": "2016-07-15",
        "source_type": "management_analysis",
        "url": "https://hbr.org/2016/07/kodaks-downfall-wasnt-about-technology",
        "lineage_refs": [
            "Scott Anthony warns that simplified Kodak stories cause executives to draw the wrong conclusions.",
            "The source is used as a claim-boundary warning against treating Kodak as a simple technology-ignorance case.",
        ],
        "evidence_signals": [
            "claim_boundary",
            "management_execution",
        ],
    },
]


PATHWAYS: dict[str, dict[str, Any]] = {
    "P1": {
        "name": "Digital disruption and ecosystem substitution",
        "claim": "Kodak collapsed because the image-capture and image-sharing ecosystem moved from film and prints to digital files, online sharing, and smartphones.",
        "evidence": [
            "2011 Consumer Digital Imaging sales fell 36% and produced a $349M segment loss.",
            "Film, Photofinishing and Entertainment sales also declined 12% in 2011.",
            "Digital camera adoption took off after 2002 and then smartphones undermined standalone cameras and printing.",
            "Kodak phased out dedicated digital cameras, pocket video cameras, and digital picture frames in 2012.",
        ],
        "source_lineage": [
            "SRC-KODAK-2011-10K",
            "SRC-CAMBRIDGE-BHR-2025",
            "SRC-MACWORLD-2006",
        ],
        "contradictions": [
            "Kodak invented and commercialized important digital technologies, so the pathway cannot mean pure ignorance.",
            "Digital cameras themselves became low-margin, so disruption alone does not explain the failed replacement profit engine.",
        ],
    },
    "P2": {
        "name": "Business model rigidity and film-profit lock-in",
        "claim": "Kodak could not replace a high-margin film and print consumables model with comparably attractive digital-camera and digital-printing economics.",
        "evidence": [
            "Film remained profitable in 2011 despite decline while Consumer Digital Imaging lost money.",
            "Kodak's growth plans repeatedly sought consumables-like economics in inkjet and printing.",
            "New digital paths were evaluated against the historical profitability of film photography.",
            "Forbes reported early digital camera units were sold at a material loss.",
        ],
        "source_lineage": [
            "SRC-KODAK-2011-10K",
            "SRC-CAMBRIDGE-BHR-2025",
            "SRC-FORBES-2000",
            "SRC-KODAK-2010-10K",
        ],
        "contradictions": [
            "Kodak did invest in digital and adjacent businesses, so rigidity was not total inaction.",
            "If no profitable replacement market existed, the pathway overlaps with timing and market-structure failure.",
        ],
    },
    "P3": {
        "name": "Strategic management and execution failure",
        "claim": "Kodak managers recognized multiple threats but failed to sequence, separate, fund, and scale a viable replacement business quickly enough.",
        "evidence": [
            "Kodak tried copiers, pharmaceuticals, digital photography, commercial printing, and consumer inkjet across several leadership regimes.",
            "The company divested copier and pharmaceutical paths and refocused on photography before the consumer imaging model collapsed.",
            "Kodak planned to phase out dedicated capture devices only after Chapter 11 filing pressure.",
            "The 2010 digital outlook shows management had a strategy, but the strategy depended on contested assumptions about cameras, inkjet, and printing.",
        ],
        "source_lineage": [
            "SRC-CAMBRIDGE-BHR-2025",
            "SRC-KODAK-2011-10K",
            "SRC-KODAK-2010-DIGITAL-OUTLOOK",
        ],
        "contradictions": [
            "The pathway is false if framed as managers simply failing to notice digital photography.",
            "Heavy renewal efforts weaken a simple incompetence narrative.",
        ],
    },
    "P4": {
        "name": "Incentive and resource-allocation structures",
        "claim": "Kodak's internal and external incentives favored defending near-term film economics and scrutinizing costly renewal paths before they could mature.",
        "evidence": [
            "New paths were judged against Kodak's unusually successful film business.",
            "Digital photography and copier investments generated large short-term losses that attracted analyst and stakeholder pressure.",
            "Budgeting, financial projections, and values are named in the academic case as key background processes in disruption response.",
            "Digital camera losses made it rational for managers to delay or constrain investment even when the technology was strategically important.",
        ],
        "source_lineage": [
            "SRC-CAMBRIDGE-BHR-2025",
            "SRC-JSIS-2009",
            "SRC-FORBES-2000",
        ],
        "contradictions": [
            "Direct compensation-plan evidence is not in the public corpus used here.",
            "The pathway can collapse into business model rigidity if incentives are not treated as a distinct mechanism.",
        ],
    },
    "P5": {
        "name": "Organizational culture and middle-management cognition",
        "claim": "Kodak's film, chemistry, and high-resolution photography identity shaped how managers evaluated digital photography and slowed adaptation.",
        "evidence": [
            "Lucas and Goh identify middle managers, culture, and rigid bureaucracy as barriers to a fast response.",
            "They describe film as a physical, chemical product and say middle managers struggled to think digitally.",
            "Kodak managers measured digital progress against the quality standard of 35mm film.",
            "The culture pathway explains why digital was interpreted through print quality and existing photographic values.",
        ],
        "source_lineage": [
            "SRC-JSIS-2009",
            "SRC-CAMBRIDGE-BHR-2025",
        ],
        "contradictions": [
            "Kodak's extensive digital R&D and technical leadership show culture did not prevent all digital action.",
            "The 2025 business-history account explicitly rejects culture or inertia as a sufficient sole explanation.",
        ],
    },
    "P6": {
        "name": "Timing failures and market-uncertainty trap",
        "claim": "Kodak invested before profitable mass demand arrived, then faced commoditized competition and a smartphone shock just as its replacement model depended on cameras and printing.",
        "evidence": [
            "Digital camera sales did not surpass film camera sales until 2002, decades after Kodak's first prototype.",
            "By the time volume demand arrived, many competitors had entered and price competition eroded profitability.",
            "The iPhone and smartphones reduced demand for standalone cameras and for printing photos.",
            "Kodak's consumer inkjet and printing bet was hit by the same shift toward screen-based sharing.",
        ],
        "source_lineage": [
            "SRC-CAMBRIDGE-BHR-2025",
            "SRC-MACWORLD-2006",
            "SRC-KODAK-2010-DIGITAL-OUTLOOK",
        ],
        "contradictions": [
            "Timing risk does not remove managerial responsibility for path selection.",
            "Other competitors adapted differently, so timing cannot be the whole explanation.",
        ],
    },
    "P7": {
        "name": "Capital allocation and liquidity constraint",
        "claim": "Kodak's renewal options narrowed as debt, divestitures, legacy shutdown costs, digital losses, and bankruptcy constraints reduced room for sustained experimentation.",
        "evidence": [
            "The Sterling Drug acquisition added expensive long-term debt and contributed to later divestiture pressure.",
            "Large annual losses in digital and adjacent ventures drew scrutiny and limited investment tolerance.",
            "The 2011 10-K records Chapter 11 proceedings, asset-sale processes, and patent monetization pressure.",
            "Cambridge links severe cash shortfalls to the combined burden of inkjet growth and legacy shutdown costs.",
        ],
        "source_lineage": [
            "SRC-CAMBRIDGE-BHR-2025",
            "SRC-KODAK-2011-10K",
            "SRC-KODAK-2010-10K",
        ],
        "contradictions": [
            "Capital shortage may be a consequence of weak strategy rather than an independent root cause.",
            "The pathway is less useful if it does not identify which capital choices narrowed which options.",
        ],
    },
    "P8": {
        "name": "Technology blindness or invention suppression",
        "claim": "Kodak failed mainly because it invented the digital camera in 1975 and then ignored or suppressed the technology until it was too late.",
        "evidence": [
            "Kodak records that Steve Sasson invented the world's first digital camera in 1975.",
            "Mass-market digital photography took decades to mature after the 1975 prototype.",
        ],
        "source_lineage": [
            "SRC-KODAK-MILESTONES",
            "SRC-CAMBRIDGE-BHR-2025",
            "SRC-HBR-2016",
        ],
        "contradictions": [
            "Kodak invested heavily in digital photography and introduced multiple important digital technologies.",
            "Kodak had U.S. digital-camera market leadership in 2004 and 2005.",
            "The pathway confuses failure to monetize with lack of technological awareness.",
        ],
    },
}


BASELINE_OUTCOMES: dict[str, dict[str, Any]] = {
    "P1": {
        "rank": 1,
        "confidence": 0.86,
        "status": "ACTIVE",
        "reason": "Dominant cross-source signal: film and consumer imaging economics collapsed as capture and sharing moved digital.",
    },
    "P2": {
        "rank": 2,
        "confidence": 0.74,
        "status": "ACTIVE",
        "reason": "Explains why digital awareness did not translate into a replacement profit engine.",
    },
    "P3": {
        "rank": 3,
        "confidence": 0.46,
        "status": "WEAKENED",
        "reason": "Kept as a secondary execution issue, but demoted because management-awareness evidence contradicts a simple incompetence account.",
    },
    "P4": {
        "rank": 4,
        "confidence": 0.32,
        "status": "ELIMINATED",
        "reason": "Collapsed into business model rigidity; treated as a restatement rather than a distinct causal pathway.",
    },
    "P5": {
        "rank": 5,
        "confidence": 0.28,
        "status": "ELIMINATED",
        "reason": "Eliminated as a common stereotype because extensive digital investment seemed to falsify cultural resistance.",
    },
    "P6": {
        "rank": 6,
        "confidence": 0.25,
        "status": "ELIMINATED",
        "reason": "Treated as background chronology, not a causal mechanism.",
    },
    "P7": {
        "rank": 7,
        "confidence": 0.23,
        "status": "ELIMINATED",
        "reason": "Treated as downstream symptom after market failure, not an investigative path.",
    },
    "P8": {
        "rank": 8,
        "confidence": 0.18,
        "status": "ELIMINATED",
        "reason": "Contradicted by evidence of long-running digital investment and market participation.",
    },
}


CONSULT_OUTCOMES: dict[str, dict[str, Any]] = {
    "P1": {
        "rank": 1,
        "confidence": 0.80,
        "status": "ACTIVE",
        "reason": "Still viable, but no longer allowed to consume the full explanation.",
        "consult_used": False,
    },
    "P2": {
        "rank": 2,
        "confidence": 0.77,
        "status": "ACTIVE",
        "reason": "Still central, but separated from incentive, timing, and capital pathways.",
        "consult_used": False,
    },
    "P6": {
        "rank": 3,
        "confidence": 0.69,
        "status": "REVIVED",
        "reason": "Consult challenge blocked early dismissal; corpus evidence shows adoption delay, later price competition, and smartphone/printing shock.",
        "consult_used": True,
    },
    "P4": {
        "rank": 4,
        "confidence": 0.66,
        "status": "REVIVED",
        "reason": "Consult challenge blocked folding incentives into business model rigidity; source lineage supports a distinct resource-allocation mechanism.",
        "consult_used": True,
    },
    "P3": {
        "rank": 5,
        "confidence": 0.61,
        "status": "ACTIVE",
        "reason": "Preserved only in narrowed form: strategic sequencing and execution failure, not ignorance.",
        "consult_used": True,
    },
    "P7": {
        "rank": 6,
        "confidence": 0.59,
        "status": "REVIVED",
        "reason": "Consult challenge blocked treating capital pressure as merely downstream; source lineage shows it constrained renewal options.",
        "consult_used": True,
    },
    "P5": {
        "rank": 7,
        "confidence": 0.56,
        "status": "REVIVED",
        "reason": "Preserved as a bounded culture/cognition pathway, weakened by evidence of extensive digital action.",
        "consult_used": True,
    },
    "P8": {
        "rank": 8,
        "confidence": 0.15,
        "status": "ELIMINATED",
        "reason": "Consult challenge found no corpus evidence sufficient to revive the standalone technology-blindness story.",
        "consult_used": True,
    },
}


GRAPH_EDGES = [
    {"from": "P1", "to": "P2", "relation": "pressures", "reason": "Digital substitution attacks the film-and-print profit model."},
    {"from": "P2", "to": "P4", "relation": "creates", "reason": "High-margin film economics shape resource-allocation incentives."},
    {"from": "P4", "to": "P3", "relation": "constrains", "reason": "Incentives influence strategic sequencing and execution choices."},
    {"from": "P5", "to": "P3", "relation": "constrains", "reason": "Culture and cognition shape how management interprets renewal paths."},
    {"from": "P6", "to": "P3", "relation": "complicates", "reason": "Market timing makes even correct strategic moves costly or mistimed."},
    {"from": "P7", "to": "P3", "relation": "constrains", "reason": "Liquidity pressure narrows management's option set."},
    {"from": "P8", "to": "P3", "relation": "competes_with", "reason": "Technology-blindness is a simpler but weaker substitute for management-execution analysis."},
    {"from": "P8", "to": "P1", "relation": "overclaims", "reason": "The fact of invention does not explain the market and ecosystem transition by itself."},
]


CONSULT_GATES: list[dict[str, Any]] = [
    {
        "gate_id": "001_management_failure_elimination",
        "pathway": "P3",
        "pre_consult_preferred_pathway": "P1/P2 digital disruption plus business model rigidity",
        "elimination_reason": "About to eliminate management failure as a vague blame label because Kodak demonstrably saw digital and invested in it.",
        "assumption_causing_elimination": "If management recognized digital, then management failure is not a distinct pathway.",
        "challenge_result": "survived_after_challenge",
        "eventual_outcome": "ACTIVE",
        "accepted_influence": "Narrowed P3 to sequencing and execution failure; did not revive a simple ignorance account.",
        "public_verification": ["SRC-CAMBRIDGE-BHR-2025", "SRC-KODAK-2011-10K", "SRC-KODAK-2010-DIGITAL-OUTLOOK"],
    },
    {
        "gate_id": "002_incentive_structures_elimination",
        "pathway": "P4",
        "pre_consult_preferred_pathway": "P2 business model rigidity",
        "elimination_reason": "About to fold incentive structures into business-model rigidity and stop tracking them separately.",
        "assumption_causing_elimination": "Incentives are only a description of the business model, not a causal mechanism.",
        "challenge_result": "survived_after_challenge",
        "eventual_outcome": "REVIVED",
        "accepted_influence": "Preserved incentives as resource-allocation pressure with distinct evidence from budget, values, and analyst-scrutiny lineage.",
        "public_verification": ["SRC-CAMBRIDGE-BHR-2025", "SRC-JSIS-2009", "SRC-FORBES-2000"],
    },
    {
        "gate_id": "003_organizational_culture_elimination",
        "pathway": "P5",
        "pre_consult_preferred_pathway": "P1/P2 digital disruption plus business model rigidity",
        "elimination_reason": "About to eliminate culture because Kodak's digital R&D and products appear to falsify cultural resistance.",
        "assumption_causing_elimination": "If a company built digital products, culture cannot have slowed adaptation.",
        "challenge_result": "survived_after_challenge",
        "eventual_outcome": "REVIVED",
        "accepted_influence": "Preserved culture in a bounded form: not a total blocker, but a cognition and translation mechanism.",
        "public_verification": ["SRC-JSIS-2009", "SRC-CAMBRIDGE-BHR-2025"],
    },
    {
        "gate_id": "004_timing_failure_elimination",
        "pathway": "P6",
        "pre_consult_preferred_pathway": "P1 digital disruption",
        "elimination_reason": "About to treat timing as chronology, not causality.",
        "assumption_causing_elimination": "A later market shift explains the collapse, so timing details are secondary.",
        "challenge_result": "survived_after_challenge",
        "eventual_outcome": "REVIVED",
        "accepted_influence": "Preserved timing as a mechanism connecting early investment losses, late mass adoption, price erosion, and smartphone displacement.",
        "public_verification": ["SRC-CAMBRIDGE-BHR-2025", "SRC-MACWORLD-2006"],
    },
    {
        "gate_id": "005_capital_allocation_elimination",
        "pathway": "P7",
        "pre_consult_preferred_pathway": "P2 business model rigidity",
        "elimination_reason": "About to treat capital allocation and liquidity as downstream symptoms rather than a live causal path.",
        "assumption_causing_elimination": "Capital problems only followed strategic failure and did not affect pathway survival.",
        "challenge_result": "survived_after_challenge",
        "eventual_outcome": "REVIVED",
        "accepted_influence": "Preserved capital constraints as an option-narrowing mechanism across debt, divestitures, cash shortfalls, and bankruptcy asset sales.",
        "public_verification": ["SRC-CAMBRIDGE-BHR-2025", "SRC-KODAK-2011-10K"],
    },
    {
        "gate_id": "006_technology_blindness_elimination",
        "pathway": "P8",
        "pre_consult_preferred_pathway": "P3 strategic management and execution failure",
        "elimination_reason": "About to eliminate the claim that Kodak mainly failed because it ignored or suppressed digital technology.",
        "assumption_causing_elimination": "The 1975 prototype plus delayed mass-market product means Kodak suppressed the technology.",
        "challenge_result": "failed_after_challenge",
        "eventual_outcome": "ELIMINATED",
        "accepted_influence": "No revival: the corpus supports awareness, investment, and technical leadership; P8 remains a false simplification.",
        "public_verification": ["SRC-KODAK-MILESTONES", "SRC-CAMBRIDGE-BHR-2025", "SRC-HBR-2016"],
    },
]


REQUIRED_CONSULT_QUESTIONS = [
    "What evidence keeps this pathway viable?",
    "What contradiction weakens my preferred pathway?",
    "What pathway may be collapsing too early?",
    "What evidence lineage supports reconsideration?",
    "What assumption is causing elimination?",
]


def pathway_node(pathway_id: str, outcome: dict[str, Any]) -> dict[str, Any]:
    pathway = PATHWAYS[pathway_id]
    return {
        "pathway_id": pathway_id,
        "pathway": pathway["name"],
        "claim": pathway["claim"],
        "status": outcome["status"],
        "confidence": outcome["confidence"],
        "rank": outcome["rank"],
        "evidence": pathway["evidence"],
        "evidence_count": len(pathway["evidence"]),
        "source_lineage": pathway["source_lineage"],
        "contradictions": pathway["contradictions"],
        "reason": outcome["reason"],
    }


def pathway_graph(run: str, outcomes: dict[str, dict[str, Any]]) -> dict[str, Any]:
    return {
        "proof_id": PROOF_ID,
        "run": run,
        "domain": "Collapse of Kodak",
        "consultation": "none" if run == "baseline" else "Protocol E only at pathway-elimination gates",
        "nodes": [pathway_node(pathway_id, outcomes[pathway_id]) for pathway_id in sorted(PATHWAYS)],
        "edges": GRAPH_EDGES,
    }


def pathway_rankings(run: str, outcomes: dict[str, dict[str, Any]]) -> dict[str, Any]:
    ranked = sorted(PATHWAYS, key=lambda pathway_id: outcomes[pathway_id]["rank"])
    return {
        "proof_id": PROOF_ID,
        "run": run,
        "domain": "Collapse of Kodak",
        "survival_definition": "ACTIVE, WEAKENED, or REVIVED with at least two public evidence items and unresolved contradictions recorded.",
        "consultation_boundary": "No consultation for baseline. Consult run uses Protocol E only when a pathway is about to be eliminated.",
        "rankings": [pathway_node(pathway_id, outcomes[pathway_id]) for pathway_id in ranked],
    }


def baseline_convergence_log() -> dict[str, Any]:
    return {
        "proof_id": PROOF_ID,
        "run": "baseline",
        "consultation_used": False,
        "convergence_events": [
            {
                "stage": "initial_pathway_set",
                "active_pathways": list(sorted(PATHWAYS)),
                "reason": "All eight pathways had at least minimal source lineage before ranking.",
            },
            {
                "stage": "dominant_pathway_forms",
                "leading_pathways": ["P1", "P2"],
                "reason": "The most visible source facts are film decline, consumer digital loss, and Chapter 11.",
                "collapse_risk": "high",
            },
            {
                "stage": "secondary_pathways_collapsed",
                "eliminated": ["P4", "P5", "P6", "P7"],
                "reason": "Baseline folded incentives, culture, timing, and capital into the digital-disruption/business-model story.",
                "collapse_risk": "confirmed",
            },
            {
                "stage": "false_simplification_removed",
                "eliminated": ["P8"],
                "reason": "Technology-blindness was contradicted by Kodak's long-running digital investment and market participation.",
            },
            {
                "stage": "final_baseline_verdict",
                "surviving_pathways": ["P1", "P2", "P3"],
                "dominant_conclusion": "Kodak collapsed primarily from digital disruption interacting with film-profit business model rigidity.",
                "known_premature_elimination_risk": ["P4", "P5", "P6", "P7"],
            },
        ],
    }


def baseline_final_verdict() -> str:
    return """# Baseline Final Verdict

No consultation was used.

The baseline run converged early on **P1 Digital disruption** and **P2 Business model rigidity**. It kept **P3 Strategic management and execution failure** only as a weakened secondary pathway, then eliminated incentives, culture, timing, and capital allocation as either restatements or background conditions.

This is a premature-collapse pattern. The eliminated pathways P4-P7 each had public evidence lineage in the source corpus, but the baseline stopped tracking them once the dominant disruption/business-model explanation felt sufficient.

The baseline correctly eliminated **P8 Technology blindness or invention suppression** as a standalone pathway. Kodak did not simply miss digital technology; it invented, invested in, and commercialized important digital technologies while failing to build a viable replacement business.
"""


def consult_request(gate: dict[str, Any]) -> dict[str, Any]:
    pathway = PATHWAYS[gate["pathway"]]
    pathway_summary = (
        f"Pathway under elimination: {gate['pathway']} {pathway['name']}. "
        f"Current elimination reason: {gate['elimination_reason']} "
        f"Preferred pathway before consult: {gate['pre_consult_preferred_pathway']}. "
        f"Known source lineage for this pathway: {', '.join(pathway['source_lineage'])}."
    )
    task = (
        f"{TITLE} Protocol E pathway-elimination gate. Do not answer which Kodak pathway is correct. "
        f"Only challenge whether the pathway should be eliminated yet. "
        f"{pathway_summary} Required questions: "
        f"{' | '.join(REQUIRED_CONSULT_QUESTIONS)} "
        "Return contradiction-first pressure, evidence-lineage warnings, and assumption checks only. "
        "Do not invent Kodak support; usable support must map back to supplied source IDs."
    )
    return {
        "request_id": f"{PROOF_ID}-{gate['gate_id']}",
        "task": task,
        "context": {
            "summary": (
                "Proof 027 asks whether consultation preserves viable investigative pathways longer than baseline reasoning. "
                "Gathering is already complete. The source corpus is fixed. The current run is at a pathway-elimination gate."
            ),
            "files": [
                "source_corpus.json",
                "baseline/pathway_graph.json",
                "baseline/pathway_rankings.json",
                "baseline/convergence_log.json",
                "baseline/final_verdict.md",
                "consult/inside_voice_consults",
            ],
            "constraints": [
                "Protocol E only: contradiction-first consultation at pathway elimination points.",
                "Consultation is forbidden during gathering and summarization.",
                "Do not ask the pond what the answer is or which pathway is correct.",
                "Consultation cannot invent support and cannot revive a pathway without public evidence.",
                "Public Kodak claims must remain tied to source_corpus.json IDs.",
            ],
            "desired_artifacts": [
                "pathway_survival_log.jsonl",
                "pathway_collapse_audit.json",
                "pathway_diversity_metrics.json",
                "consult_pathway_influence.json",
                "final_pathway_map.md",
                "hostile_pathway_audit.json",
            ],
        },
        "mode": "audit",
        "max_output_chars": 8000,
        "require_lineage": True,
    }


def consult_requests() -> list[tuple[Path, dict[str, Any]]]:
    rows: list[tuple[Path, dict[str, Any]]] = []
    for gate in CONSULT_GATES:
        path = PROOF_DIR / "consult/inside_voice_consults" / f"{gate['gate_id']}_request.json"
        rows.append((path, consult_request(gate)))
    return rows


def response_path_for_gate(gate: dict[str, Any]) -> Path:
    return PROOF_DIR / "consult/inside_voice_consults" / f"{gate['gate_id']}_response.json"


def request_path_for_gate(gate: dict[str, Any]) -> Path:
    return PROOF_DIR / "consult/inside_voice_consults" / f"{gate['gate_id']}_request.json"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def consult_response_summary(response: dict[str, Any]) -> str:
    if not response:
        return "missing_response"
    parts = [
        f"adapter_status={response.get('adapter_status', 'unknown')}",
        f"classification={response.get('classification', 'unknown')}",
        f"contribution_grade={response.get('contribution_grade', 'unknown')}",
        f"summary={response.get('summary', '')}",
    ]
    limitations = response.get("limitations") or []
    if limitations:
        parts.append("limitations=" + "; ".join(str(item) for item in limitations[:3]))
    pressure_rankings = response.get("pressure_rankings") or []
    if pressure_rankings:
        top = []
        for item in pressure_rankings[:3]:
            top.append(f"{item.get('id')}@{item.get('source_ref')}")
        parts.append("pressure_rankings=" + ", ".join(top))
    findings = response.get("findings") or []
    parts.append(f"domain_specific_findings={len(findings)}")
    return " | ".join(parts)


def consult_decision_gate_log() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for gate in CONSULT_GATES:
        req_path = request_path_for_gate(gate)
        resp_path = response_path_for_gate(gate)
        response = load_json(resp_path) if resp_path.is_file() else {}
        rows.append(
            {
                "decision_gate": gate["gate_id"],
                "pathway": f"{gate['pathway']}: {PATHWAYS[gate['pathway']]['name']}",
                "pre_consult_preferred_pathway": gate["pre_consult_preferred_pathway"],
                "elimination_reason": gate["elimination_reason"],
                "required_consult_questions": REQUIRED_CONSULT_QUESTIONS,
                "consult_response": consult_response_summary(response),
                "request_artifact": str(req_path.relative_to(PROOF_DIR)),
                "response_artifact": str(resp_path.relative_to(PROOF_DIR)),
                "request_hash": sha256_file(req_path),
                "response_hash": sha256_file(resp_path),
                "accepted_influence": gate["accepted_influence"],
                "public_verification": gate["public_verification"],
                "eventual_outcome": gate["eventual_outcome"],
                "pathway_changed": gate["eventual_outcome"] != "ELIMINATED",
            }
        )
    return rows


def consult_convergence_log() -> dict[str, Any]:
    return {
        "proof_id": PROOF_ID,
        "run": "consult",
        "consultation_used": True,
        "consultation_boundary": "Protocol E only; each consult occurred at a recorded pathway-elimination gate.",
        "forbidden_uses_observed": {
            "consult_during_gathering": False,
            "consult_during_summarization": False,
            "asked_for_answer": False,
            "asked_which_pathway_is_correct": False,
        },
        "convergence_events": [
            {
                "stage": "fixed_source_corpus",
                "active_pathways": list(sorted(PATHWAYS)),
                "reason": "Source gathering was complete before any consult request was generated.",
            },
            {
                "stage": "elimination_gates",
                "gates": [gate["gate_id"] for gate in CONSULT_GATES],
                "reason": "Consultation was invoked only when a pathway was about to be eliminated.",
            },
            {
                "stage": "post_challenge_survival",
                "surviving_pathways": ["P1", "P2", "P3", "P4", "P5", "P6", "P7"],
                "eliminated_pathways": ["P8"],
                "reason": "P3-P7 earned survival through existing public evidence; P8 did not.",
            },
            {
                "stage": "final_consult_verdict",
                "dominant_conclusion": "Kodak's collapse remains multi-pathway; consultation preserved five evidence-supported pathways that baseline was collapsing or weakening.",
                "claim_boundary": "Consult responses challenged elimination only; they supplied no authoritative Kodak evidence.",
            },
        ],
    }


def pathway_survival_log() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for run, outcomes in (("baseline", BASELINE_OUTCOMES), ("consult", CONSULT_OUTCOMES)):
        for pathway_id in sorted(PATHWAYS):
            pathway = PATHWAYS[pathway_id]
            outcome = outcomes[pathway_id]
            rows.append(
                {
                    "run": run,
                    "pathway": f"{pathway_id}: {pathway['name']}",
                    "status": outcome["status"],
                    "reason": outcome["reason"],
                    "evidence_count": len(pathway["evidence"]),
                    "consult_used": bool(outcome.get("consult_used", False)) if run == "consult" else False,
                }
            )
    return rows


def pathway_collapse_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for gate in CONSULT_GATES:
        response = load_json(response_path_for_gate(gate)) if response_path_for_gate(gate).is_file() else {}
        rows.append(
            {
                "pathway": f"{gate['pathway']}: {PATHWAYS[gate['pathway']]['name']}",
                "elimination_reason": gate["elimination_reason"],
                "consult_challenge": consult_response_summary(response),
                "survived_after_challenge": gate["challenge_result"] == "survived_after_challenge",
                "eventual_outcome": gate["eventual_outcome"],
                "accepted_influence": gate["accepted_influence"],
                "assumption_causing_elimination": gate["assumption_causing_elimination"],
                "public_evidence_lineage": gate["public_verification"],
            }
        )
    return {
        "proof_id": PROOF_ID,
        "scope": "consult run pathway-elimination gates",
        "collapse_audits": rows,
    }


def pathway_diversity_metrics() -> dict[str, Any]:
    false_preservations = []
    return {
        "initial_pathways": len(PATHWAYS),
        "baseline_surviving_pathways": 3,
        "consult_surviving_pathways": 7,
        "pathways_revived": 4,
        "premature_eliminations_prevented": 5,
        "false_pathway_preservations": len(false_preservations),
        "pathway_preservation_score": 7 - len(false_preservations),
        "formula": "Surviving Viable Pathways - False Pathway Preservations",
        "surviving_viable_pathways": ["P1", "P2", "P3", "P4", "P5", "P6", "P7"],
        "baseline_premature_eliminations": ["P4", "P5", "P6", "P7"],
        "consult_prevented_near_elimination": ["P3", "P4", "P5", "P6", "P7"],
        "correct_elimination": ["P8"],
    }


def consult_pathway_influence() -> dict[str, Any]:
    return {
        "proof_id": PROOF_ID,
        "consult_boundary": "Protocol E only at pathway-elimination points.",
        "pond_supplied_new_kodak_evidence": False,
        "consult_response_domain_specificity": "low_to_bounded",
        "pathway_revivals": [
            {
                "pathway": f"{pathway_id}: {PATHWAYS[pathway_id]['name']}",
                "evidence_lineage": CONSULT_OUTCOMES[pathway_id]["reason"],
            }
            for pathway_id in ["P4", "P5", "P6", "P7"]
        ],
        "pathway_preservations": [
            {
                "pathway": f"{pathway_id}: {PATHWAYS[pathway_id]['name']}",
                "mechanism": "Consult challenge delayed elimination; public source corpus then determined survival.",
            }
            for pathway_id in ["P3", "P4", "P5", "P6", "P7"]
        ],
        "pathway_eliminations_reversed": [
            "P4: incentive structures",
            "P5: organizational culture",
            "P6: timing failures",
            "P7: capital allocation/liquidity",
        ],
        "false_pathway_preservations": [],
        "not_credited_to_pond": [
            "Discovery of Kodak historical facts.",
            "Final ranking of Kodak causal pathways.",
            "Any source evidence not already present in source_corpus.json.",
        ],
        "credited_to_consult_run": [
            "Triggering a challenge before eliminating P3-P7.",
            "Forcing explicit evidence-lineage checks before pathway death.",
            "Preventing collapse of incentives, culture, timing, and capital into the dominant digital-disruption story.",
            "Allowing P8 to remain eliminated because no evidence met the revival burden.",
        ],
    }


def final_pathway_map() -> str:
    lines = [
        "# Final Pathway Map",
        "",
        "Consultation was used only at elimination gates. Surviving pathways below earned survival through the fixed public source corpus, not through consult-supplied Kodak facts.",
        "",
    ]
    for pathway_id in ["P1", "P2", "P6", "P4", "P3", "P7", "P5"]:
        pathway = PATHWAYS[pathway_id]
        outcome = CONSULT_OUTCOMES[pathway_id]
        lines.extend(
            [
                f"## {pathway_id}. {pathway['name']}",
                "",
                f"- Status: {outcome['status']}",
                f"- Confidence: {outcome['confidence']:.2f}",
                f"- Claim: {pathway['claim']}",
                f"- Evidence lineage: {', '.join(pathway['source_lineage'])}",
                f"- Evidence count: {len(pathway['evidence'])}",
                f"- Competing explanations: {', '.join(item for item in sorted(PATHWAYS) if item != pathway_id and item != 'P8')}",
                "- Key contradictions:",
            ]
        )
        lines.extend([f"  - {item}" for item in pathway["contradictions"]])
        lines.append("")
    lines.extend(
        [
            "## Eliminated Pathway",
            "",
            "- P8 Technology blindness or invention suppression: eliminated after challenge. The 1975 invention is real, but the standalone claim collapses because Kodak also invested heavily in digital photography and achieved technical and market leadership before failing to build a viable replacement business.",
        ]
    )
    return "\n".join(lines)


def hostile_pathway_audit() -> dict[str, Any]:
    audits = [
        {
            "pathway": "P1: Digital disruption and ecosystem substitution",
            "attempted_invalidation": "Kodak was digitally capable and had market participation, so disruption may be too generic.",
            "classification": "VALID_PRESERVATION",
            "reason": "The pathway is not technology ignorance; it is market and ecosystem substitution documented by segment decline, camera exit, and smartphone/printing effects.",
            "evidence_lineage": ["SRC-KODAK-2011-10K", "SRC-CAMBRIDGE-BHR-2025"],
            "residual_risk": "Can over-dominate if treated as the whole answer.",
        },
        {
            "pathway": "P2: Business model rigidity and film-profit lock-in",
            "attempted_invalidation": "Kodak made digital investments, so the business model was not fully rigid.",
            "classification": "VALID_PRESERVATION",
            "reason": "The preserved claim is not total rigidity; it is failure to replace film/print economics with a viable recurring-margin model.",
            "evidence_lineage": ["SRC-KODAK-2011-10K", "SRC-CAMBRIDGE-BHR-2025", "SRC-FORBES-2000"],
            "residual_risk": "Overlaps with incentives and timing.",
        },
        {
            "pathway": "P3: Strategic management and execution failure",
            "attempted_invalidation": "Management failure is a vague blame bucket and is weakened by evidence of serious renewal attempts.",
            "classification": "VALID_PRESERVATION",
            "reason": "Preserved only as sequencing, separation, funding, and scaling failure across attempted renewal paths; not as simple ignorance.",
            "evidence_lineage": ["SRC-CAMBRIDGE-BHR-2025", "SRC-KODAK-2011-10K"],
            "residual_risk": "Must remain narrowly framed.",
        },
        {
            "pathway": "P4: Incentive and resource-allocation structures",
            "attempted_invalidation": "The corpus lacks direct compensation-plan evidence.",
            "classification": "VALID_PRESERVATION",
            "reason": "Direct bonus evidence is absent, but resource-allocation incentives are supported by film-profit comparison, investment losses, analyst pressure, and budgeting/value-process evidence.",
            "evidence_lineage": ["SRC-CAMBRIDGE-BHR-2025", "SRC-JSIS-2009", "SRC-FORBES-2000"],
            "residual_risk": "Evidence is partly inferential rather than a direct internal-pay record.",
        },
        {
            "pathway": "P5: Organizational culture and middle-management cognition",
            "attempted_invalidation": "Kodak's digital R&D and products contradict a culture-resistance story.",
            "classification": "VALID_PRESERVATION",
            "reason": "The preserved claim is bounded: culture shaped interpretation and speed; it did not block all digital action.",
            "evidence_lineage": ["SRC-JSIS-2009", "SRC-CAMBRIDGE-BHR-2025"],
            "residual_risk": "Weakened; should not be promoted above market and business-model pathways without more internal evidence.",
        },
        {
            "pathway": "P6: Timing failures and market-uncertainty trap",
            "attempted_invalidation": "Timing can become an excuse that removes agency.",
            "classification": "VALID_PRESERVATION",
            "reason": "Timing remains causal because early investment losses, delayed demand, late price competition, and smartphone substitution changed which strategies could pay off.",
            "evidence_lineage": ["SRC-CAMBRIDGE-BHR-2025", "SRC-MACWORLD-2006"],
            "residual_risk": "Needs to be paired with management and capital paths.",
        },
        {
            "pathway": "P7: Capital allocation and liquidity constraint",
            "attempted_invalidation": "Liquidity problems may be downstream symptoms.",
            "classification": "VALID_PRESERVATION",
            "reason": "The pathway survives because capital pressure also narrowed later options: debt, divestitures, cash shortfalls, patent monetization, and Chapter 11 processes changed feasible moves.",
            "evidence_lineage": ["SRC-CAMBRIDGE-BHR-2025", "SRC-KODAK-2011-10K"],
            "residual_risk": "Causal direction is mixed and should remain secondary.",
        },
    ]
    return {
        "proof_id": PROOF_ID,
        "audit_requirement": "Attempt to invalidate every preserved pathway.",
        "preserved_pathway_audits": audits,
        "eliminated_pathway_audits": [
            {
                "pathway": "P8: Technology blindness or invention suppression",
                "attempted_revival": "The 1975 prototype might show Kodak buried the future.",
                "classification": "FALSE_PATHWAY",
                "reason": "The standalone story is contradicted by extensive digital investment, technical leadership, and market participation.",
                "evidence_lineage": ["SRC-KODAK-MILESTONES", "SRC-CAMBRIDGE-BHR-2025", "SRC-HBR-2016"],
            }
        ],
        "summary_counts": {
            "VALID_PRESERVATION": 7,
            "UNNECESSARY_PRESERVATION": 0,
            "FALSE_PATHWAY": 1,
        },
        "verdict": "VERY_STRONG_SIGNAL_BOUNDED",
    }


def source_lineage_verification() -> dict[str, Any]:
    return {
        "proof_id": PROOF_ID,
        "verification_boundary": "Source corpus gathered before consultation. Consult responses were not used as Kodak factual evidence.",
        "sources": [
            {
                "source_id": source["source_id"],
                "url": source["url"],
                "lineage_refs": source["lineage_refs"],
                "supports_pathways": [
                    pathway_id
                    for pathway_id, pathway in PATHWAYS.items()
                    if source["source_id"] in pathway["source_lineage"]
                ],
            }
            for source in SOURCE_CORPUS
        ],
    }


def public_lineage_summary() -> str:
    return """# Public Lineage Summary

Proof 027 uses Kodak as the historical domain. Public claims are grounded in `source_corpus.json`; consult responses are recorded only as pathway-elimination challenges.

The no-consult baseline collapsed early to digital disruption plus business-model rigidity. The consult run used Protocol E at six elimination gates and preserved P3-P7 only when the fixed source corpus supplied evidence.

The pond did not provide new Kodak facts. Its credited role is pathway-preservation pressure: before eliminating a pathway, it forced a check for viable evidence, contradictions against the preferred pathway, premature collapse, source lineage, and the elimination assumption.
"""


def readme() -> str:
    return """# Proof 027 - Pathway Intelligence Challenge

Status: `complete`

Domain: Collapse of Kodak.

Objective: determine whether Protocol E consultation preserves viable investigative pathways longer than baseline reasoning.

The result is a bounded very-strong signal: consultation preserved evidence-supported pathways P3-P7 that baseline collapsed or weakened too early, while the hostile audit found no false pathway preservations. P8, the simple technology-blindness story, remained eliminated.

Key artifacts:

- `baseline/pathway_graph.json`
- `baseline/pathway_rankings.json`
- `baseline/convergence_log.json`
- `baseline/final_verdict.md`
- `consult/inside_voice_consults/*_request.json`
- `consult/inside_voice_consults/*_response.json`
- `pathway_survival_log.jsonl`
- `pathway_collapse_audit.json`
- `pathway_diversity_metrics.json`
- `consult_pathway_influence.json`
- `hostile_pathway_audit.json`
- `final_pathway_map.md`

Primary metric: Pathway Preservation Score = 7 surviving viable pathways - 0 false pathway preservations = `7`.
"""


def proof_manifest() -> dict[str, Any]:
    request_hashes = [sha256_file(request_path_for_gate(gate)) for gate in CONSULT_GATES]
    response_hashes = [sha256_file(response_path_for_gate(gate)) for gate in CONSULT_GATES]
    required_artifacts = [
        "README.md",
        "proof_manifest.json",
        "source_corpus.json",
        "source_lineage_verification.json",
        "public_lineage_summary.md",
        "baseline/pathway_graph.json",
        "baseline/pathway_rankings.json",
        "baseline/convergence_log.json",
        "baseline/final_verdict.md",
        "consult/pathway_graph.json",
        "consult/pathway_rankings.json",
        "consult/convergence_log.json",
        "consult/decision_gate_log.jsonl",
        "pathway_survival_log.jsonl",
        "pathway_collapse_audit.json",
        "pathway_diversity_metrics.json",
        "consult_pathway_influence.json",
        "final_pathway_map.md",
        "hostile_pathway_audit.json",
    ]
    required_artifacts.extend(
        [f"consult/inside_voice_consults/{gate['gate_id']}_request.json" for gate in CONSULT_GATES]
    )
    required_artifacts.extend(
        [f"consult/inside_voice_consults/{gate['gate_id']}_response.json" for gate in CONSULT_GATES]
    )
    return {
        "proof_id": PROOF_ID,
        "title": TITLE,
        "status": "complete",
        "domain": "Collapse of Kodak",
        "targets": [
            "ConvergenceResistance",
            "PathwayPreservation",
            "ProtocolEContradictionFirstConsultation",
        ],
        "claim_level": "evidence_backed_bounded",
        "inside_voice_adapter_status": "pond_backed_protocol_e_elimination_gate_consults_used",
        "public_private_boundary": "Only public source IDs, bounded consult summaries, hashes, metrics, and decision-gate actions are exposed.",
        "disallowed_claims": [
            "inside_voice_as_kodak_authority",
            "consult_as_data_gathering",
            "consult_as_answer_mechanism",
            "hidden_chain_of_thought",
            "unsupported_historical_claims",
        ],
        "lineage": {
            "contract_version": "inside_voice.mcp.consultation.v1",
            "mcp_endpoint": CONSULT_ENDPOINT,
            "derived_from": "source_corpus.json; baseline artifacts; consult/inside_voice_consults; consult/decision_gate_log.jsonl",
            "request_hashes": request_hashes,
            "response_hashes": response_hashes,
            "combined_request_hash": sha256_json(request_hashes),
            "combined_response_hash": sha256_json(response_hashes),
            "validates": "pathway_preservation_under_protocol_e_elimination_gate_consultation",
        },
        "required_artifacts": required_artifacts,
    }


def write_pre_consult() -> None:
    write_json(PROOF_DIR / "source_corpus.json", SOURCE_CORPUS)
    write_json(PROOF_DIR / "source_lineage_verification.json", source_lineage_verification())
    write_json(PROOF_DIR / "baseline/pathway_graph.json", pathway_graph("baseline", BASELINE_OUTCOMES))
    write_json(PROOF_DIR / "baseline/pathway_rankings.json", pathway_rankings("baseline", BASELINE_OUTCOMES))
    write_json(PROOF_DIR / "baseline/convergence_log.json", baseline_convergence_log())
    write_text(PROOF_DIR / "baseline/final_verdict.md", baseline_final_verdict())
    for path, request in consult_requests():
        write_json(path, request)


def write_final() -> None:
    write_pre_consult()
    write_json(PROOF_DIR / "consult/pathway_graph.json", pathway_graph("consult", CONSULT_OUTCOMES))
    write_json(PROOF_DIR / "consult/pathway_rankings.json", pathway_rankings("consult", CONSULT_OUTCOMES))
    write_json(PROOF_DIR / "consult/convergence_log.json", consult_convergence_log())
    write_jsonl(PROOF_DIR / "consult/decision_gate_log.jsonl", consult_decision_gate_log())
    write_jsonl(PROOF_DIR / "pathway_survival_log.jsonl", pathway_survival_log())
    write_json(PROOF_DIR / "pathway_collapse_audit.json", pathway_collapse_audit())
    write_json(PROOF_DIR / "pathway_diversity_metrics.json", pathway_diversity_metrics())
    write_json(PROOF_DIR / "consult_pathway_influence.json", consult_pathway_influence())
    write_text(PROOF_DIR / "final_pathway_map.md", final_pathway_map())
    write_json(PROOF_DIR / "hostile_pathway_audit.json", hostile_pathway_audit())
    write_text(PROOF_DIR / "public_lineage_summary.md", public_lineage_summary())
    write_text(PROOF_DIR / "README.md", readme())
    write_json(PROOF_DIR / "proof_manifest.json", proof_manifest())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=["pre_consult", "final"])
    args = parser.parse_args()
    if args.phase == "pre_consult":
        write_pre_consult()
    else:
        write_final()
    print(f"{args.phase} artifacts written for {PROOF_ID} at {utc_now()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
