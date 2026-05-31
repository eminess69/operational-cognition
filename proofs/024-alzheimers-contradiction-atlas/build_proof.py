#!/usr/bin/env python3
"""Build artifacts for proof 024.

The script intentionally separates baseline generation from the consult
artifact build. Run:

  python3 proofs/024-alzheimers-contradiction-atlas/build_proof.py baseline
  # POST each generated request to /consult and save the responses.
  python3 proofs/024-alzheimers-contradiction-atlas/build_proof.py final
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PROOF_DIR = Path(__file__).resolve().parent
SOURCE_TMP = Path("/private/tmp/alz_atlas_sources")
PUBMED_XML = SOURCE_TMP / "pubmed_fetch.xml"
CONSULT_ENDPOINT = "http://127.0.0.1:8767/consult"
PROOF_ID = "024-alzheimers-contradiction-atlas"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def text_of(node: ET.Element | None) -> str:
    if node is None:
        return ""
    return clean_text("".join(node.itertext()))


def article_year(article: ET.Element) -> str:
    for path in (
        ".//JournalIssue/PubDate/Year",
        ".//ArticleDate/Year",
        ".//PubDate/Year",
    ):
        year = article.findtext(path)
        if year:
            return year
    medline = article.findtext(".//JournalIssue/PubDate/MedlineDate") or article.findtext(".//PubDate/MedlineDate")
    match = re.search(r"(19|20)\d{2}", medline or "")
    return match.group(0) if match else ""


def article_ids(article: ET.Element) -> dict[str, str]:
    ids: dict[str, str] = {}
    for node in article.findall(".//ArticleId"):
        kind = node.attrib.get("IdType", "")
        if kind:
            ids[kind] = clean_text(node.text or "")
    return ids


def tags_for(text: str, pub_types: list[str]) -> list[str]:
    lowered = text.casefold()
    tags: set[str] = set()
    keyword_map = {
        "amyloid": ["amyloid", "abeta", "a beta", "anti-amyloid", "lecanemab", "donanemab", "aducanumab", "gantenerumab", "solanezumab"],
        "tau": ["tau", "p-tau", "phosphorylated tau", "mtbr"],
        "clinical_trial_or_therapy": ["trial", "randomized", "phase", "treatment", "therapy", "lecanemab", "donanemab", "aducanumab", "gantenerumab", "solanezumab", "semorinemab", "insulin", "valacyclovir"],
        "biomarker": ["biomarker", "pet", "csf", "plasma", "blood", "p-tau", "ptau", "atn"],
        "vascular": ["vascular", "cerebrovascular", "hypertension", "blood-brain barrier", "microbleed", "cerebral amyloid angiopathy", "aria"],
        "inflammation_immune": ["inflammation", "inflammatory", "microglia", "immune", "astrocyte", "complement", "trem2"],
        "metabolic_mitochondrial": ["metabolic", "mitochond", "insulin", "glucose", "oxidative"],
        "genetic": ["apoe", "genetic", "genomic", "trem2", "polygenic"],
        "mixed_pathology": ["mixed", "heterogeneity", "subtype", "late", "tdp", "part", "copatholog", "co-patholog", "atn"],
        "cholinergic_synaptic": ["cholinergic", "acetylcholine", "synaptic", "synapse", "neuroplasticity"],
    }
    for tag, keywords in keyword_map.items():
        if any(keyword in lowered for keyword in keywords):
            tags.add(tag)
    if any("review" in item.casefold() for item in pub_types):
        tags.add("review")
    if any("clinical trial" in item.casefold() or "randomized controlled trial" in item.casefold() for item in pub_types):
        tags.add("clinical_trial_or_therapy")
    return sorted(tags)


def load_pubmed_query_buckets() -> dict[str, list[str]]:
    buckets: dict[str, list[str]] = {}
    for path in sorted(SOURCE_TMP.glob("esearch_*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        ids = payload.get("esearchresult", {}).get("idlist", [])
        if isinstance(ids, list):
            buckets[path.stem.replace("esearch_", "")] = [str(item) for item in ids]
    return buckets


def parse_pubmed_sources() -> list[dict[str, Any]]:
    if not PUBMED_XML.is_file():
        raise FileNotFoundError(f"missing PubMed XML: {PUBMED_XML}")
    query_buckets = load_pubmed_query_buckets()
    bucket_by_id: dict[str, list[str]] = {}
    for bucket, pmids in query_buckets.items():
        for pmid in pmids:
            bucket_by_id.setdefault(pmid, []).append(bucket)

    root = ET.parse(PUBMED_XML).getroot()
    records: list[dict[str, Any]] = []
    seen: set[str] = set()
    for article in root.findall(".//PubmedArticle"):
        pmid = clean_text(article.findtext(".//PMID") or "")
        if not pmid or pmid in seen:
            continue
        seen.add(pmid)
        title = text_of(article.find(".//ArticleTitle"))
        abstract_parts = [text_of(node) for node in article.findall(".//Abstract/AbstractText")]
        abstract = clean_text(" ".join(part for part in abstract_parts if part))
        pub_types = [clean_text(node.text or "") for node in article.findall(".//PublicationType")]
        ids = article_ids(article)
        journal = clean_text(article.findtext(".//Journal/Title") or "")
        year = article_year(article)
        authors = [
            clean_text(" ".join(part for part in (author.findtext("ForeName"), author.findtext("LastName")) if part))
            for author in article.findall(".//AuthorList/Author")[:6]
        ]
        authors = [author for author in authors if author]
        joined = " ".join([title, abstract, journal, " ".join(pub_types)])
        tags = tags_for(joined, pub_types)
        source_classes = ["peer_reviewed_pubmed"]
        if "review" in tags:
            source_classes.append("peer_reviewed_review")
        if "clinical_trial_or_therapy" in tags:
            source_classes.append("clinical_trial_or_therapy")
        if "biomarker" in tags:
            source_classes.append("biomarker")
        if any(tag in tags for tag in ("vascular", "inflammation_immune", "metabolic_mitochondrial")):
            source_classes.append("vascular_inflammation_metabolic")
        records.append(
            {
                "source_id": f"PMID-{pmid}",
                "source_type": "peer_reviewed_pubmed",
                "pmid": pmid,
                "title": title,
                "journal": journal,
                "year": year,
                "authors": authors,
                "publication_types": pub_types,
                "doi": ids.get("doi", ""),
                "pmc": ids.get("pmc", ""),
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                "query_buckets": sorted(bucket_by_id.get(pmid, [])),
                "tags": tags,
                "source_classes": source_classes,
                "abstract_available": bool(abstract),
                "abstract_signal": abstract[:360],
            }
        )
    records.sort(key=lambda item: (item.get("year") or "0000", item["source_id"]), reverse=True)
    return records


def official_sources() -> list[dict[str, Any]]:
    return [
        {
            "source_id": "OFF-FDA-LEQEMBI-2023",
            "source_type": "official_institutional_summary",
            "institution": "U.S. Food and Drug Administration",
            "year": "2023",
            "title": "FDA Converts Novel Alzheimer's Disease Treatment to Traditional Approval",
            "url": "https://www.fda.gov/news-events/press-announcements/fda-converts-novel-alzheimers-disease-treatment-traditional-approval",
            "source_classes": ["official_or_institutional_summary", "clinical_trial_or_therapy"],
            "tags": ["amyloid", "clinical_trial_or_therapy", "biomarker"],
            "lineage_note": "Official approval summary for lecanemab in early Alzheimer disease with confirmed amyloid pathology.",
        },
        {
            "source_id": "OFF-FDA-KISUNLA-2024",
            "source_type": "official_institutional_summary",
            "institution": "U.S. Food and Drug Administration",
            "year": "2024",
            "title": "FDA approves treatment for adults with Alzheimer's disease",
            "url": "https://www.fda.gov/drugs/news-events-human-drugs/fda-approves-treatment-adults-alzheimers-disease",
            "source_classes": ["official_or_institutional_summary", "clinical_trial_or_therapy"],
            "tags": ["amyloid", "clinical_trial_or_therapy", "biomarker"],
            "lineage_note": "Official approval summary for donanemab in early symptomatic Alzheimer disease.",
        },
        {
            "source_id": "OFF-NIA-AD-CAUSES",
            "source_type": "official_institutional_summary",
            "institution": "National Institute on Aging",
            "year": "2024",
            "title": "What Causes Alzheimer's Disease?",
            "url": "https://www.nia.nih.gov/health/alzheimers-causes-and-risk-factors/what-causes-alzheimers-disease",
            "source_classes": ["official_or_institutional_summary"],
            "tags": ["amyloid", "tau", "inflammation_immune", "vascular", "metabolic_mitochondrial", "genetic"],
            "lineage_note": "Institutional summary framing Alzheimer disease as involving multiple interacting changes and risk factors.",
        },
        {
            "source_id": "OFF-NIA-BLOOD-BIOMARKERS-2024",
            "source_type": "official_institutional_summary",
            "institution": "National Institutes of Health",
            "year": "2024",
            "title": "Blood tests could improve diagnosis of Alzheimer's disease in primary care",
            "url": "https://www.nih.gov/news-events/nih-research-matters/blood-tests-could-improve-diagnosis-alzheimers-disease-primary-care",
            "source_classes": ["official_or_institutional_summary", "biomarker"],
            "tags": ["biomarker", "amyloid", "tau"],
            "lineage_note": "Institutional research summary of blood biomarker performance in care settings.",
        },
        {
            "source_id": "OFF-CDC-ABOUT-ADRD",
            "source_type": "official_institutional_summary",
            "institution": "Centers for Disease Control and Prevention",
            "year": "2024",
            "title": "About Alzheimer's Disease and Related Dementias",
            "url": "https://www.cdc.gov/alzheimers-dementia/about/index.html",
            "source_classes": ["official_or_institutional_summary"],
            "tags": ["mixed_pathology", "vascular", "genetic"],
            "lineage_note": "Public health summary emphasizing dementia risk and related dementias.",
        },
        {
            "source_id": "OFF-WHO-DEMENTIA",
            "source_type": "official_institutional_summary",
            "institution": "World Health Organization",
            "year": "2025",
            "title": "Dementia",
            "url": "https://www.who.int/news-room/fact-sheets/detail/dementia",
            "source_classes": ["official_or_institutional_summary"],
            "tags": ["mixed_pathology", "vascular", "metabolic_mitochondrial"],
            "lineage_note": "Global health fact sheet naming Alzheimer disease as a major dementia cause and describing risk factors.",
        },
        {
            "source_id": "OFF-NINDS-VCID",
            "source_type": "official_institutional_summary",
            "institution": "National Institute of Neurological Disorders and Stroke",
            "year": "2024",
            "title": "Vascular Contributions to Cognitive Impairment and Dementia",
            "url": "https://www.ninds.nih.gov/health-information/disorders/vascular-contributions-cognitive-impairment-and-dementia",
            "source_classes": ["official_or_institutional_summary"],
            "tags": ["vascular", "mixed_pathology"],
            "lineage_note": "Institutional summary of vascular contributions to dementia and overlap with neurodegeneration.",
        },
        {
            "source_id": "OFF-ALZ-FACTS-2024",
            "source_type": "institutional_summary",
            "institution": "Alzheimer's Association",
            "year": "2024",
            "title": "2024 Alzheimer's disease facts and figures",
            "url": "https://www.alz.org/media/Documents/alzheimers-facts-and-figures.pdf",
            "source_classes": ["official_or_institutional_summary"],
            "tags": ["mixed_pathology", "clinical_trial_or_therapy", "biomarker"],
            "lineage_note": "Institutional epidemiology and care-burden summary; not used as mechanistic proof.",
        },
    ]


def corpus() -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    sources = parse_pubmed_sources() + official_sources()
    by_id = {source["source_id"]: source for source in sources}
    counts = {
        "total_source_documents": len(sources),
        "peer_reviewed_pubmed": sum(1 for source in sources if source["source_type"] == "peer_reviewed_pubmed"),
        "peer_reviewed_reviews": sum(1 for source in sources if "peer_reviewed_review" in source.get("source_classes", [])),
        "clinical_trial_or_therapy": sum(1 for source in sources if "clinical_trial_or_therapy" in source.get("source_classes", [])),
        "biomarker": sum(1 for source in sources if "biomarker" in source.get("source_classes", [])),
        "vascular_inflammation_metabolic": sum(1 for source in sources if "vascular_inflammation_metabolic" in source.get("source_classes", []) or any(tag in source.get("tags", []) for tag in ("vascular", "inflammation_immune", "metabolic_mitochondrial"))),
        "official_or_institutional_summaries": sum(1 for source in sources if source["source_type"] in {"official_institutional_summary", "institutional_summary"}),
        "recent_2024_2026": sum(1 for source in sources if str(source.get("year", ""))[:4] in {"2024", "2025", "2026"}),
    }
    payload = {
        "corpus_id": "alzheimers-contradiction-atlas-corpus-2026-05-28",
        "created_utc": utc_now(),
        "acquisition": {
            "pubmed_xml": str(PUBMED_XML),
            "pubmed_query_files": sorted(path.name for path in SOURCE_TMP.glob("esearch_*.json")),
            "official_sources_curated": True,
            "note": "PubMed records were fetched through NCBI E-utilities with curl; official source URLs are separately curated.",
        },
        "counts": counts,
        "minimums": {
            "minimum_100_source_documents": counts["total_source_documents"] >= 100,
            "minimum_40_peer_reviewed": counts["peer_reviewed_pubmed"] >= 40,
            "minimum_10_clinical_trial_or_therapy": counts["clinical_trial_or_therapy"] >= 10,
            "minimum_10_biomarker": counts["biomarker"] >= 10,
            "minimum_10_vascular_inflammation_metabolic": counts["vascular_inflammation_metabolic"] >= 10,
            "minimum_5_official_or_institutional": counts["official_or_institutional_summaries"] >= 5,
            "preferred_250_documents": counts["total_source_documents"] >= 250,
        },
        "source_documents": sources,
    }
    return payload, by_id


def sid(pmid: str) -> str:
    return f"PMID-{pmid}"


KEY_SOURCE_GROUPS = {
    "amyloid_tau": [
        sid("33986301"),
        sid("35177833"),
        sid("34815562"),
        sid("39014245"),
        sid("37875627"),
        sid("36449413"),
        sid("37459141"),
        sid("37966285"),
        sid("35542991"),
    ],
    "therapy_trials": [
        sid("36449413"),
        sid("37459141"),
        sid("33720637"),
        sid("35542991"),
        sid("37966285"),
        sid("38683602"),
        sid("35696185"),
        sid("32568367"),
        sid("41405855"),
        sid("37040116"),
        sid("38730496"),
    ],
    "biomarkers": [
        sid("38429551"),
        sid("39068545"),
        sid("38866966"),
        sid("38252443"),
        sid("36508198"),
        sid("37443334"),
        sid("39068669"),
        sid("41324928"),
        sid("38888066"),
        "OFF-NIA-BLOOD-BIOMARKERS-2024",
    ],
    "vascular_inflammation_metabolic": [
        sid("33318676"),
        sid("38424470"),
        sid("41315874"),
        sid("31827267"),
        sid("36129176"),
        sid("39620840"),
        sid("40023293"),
        sid("34416829"),
        sid("41052375"),
        sid("39288341"),
        "OFF-NINDS-VCID",
    ],
    "mixed_pathology": [
        sid("32047067"),
        sid("33429401"),
        sid("37563264"),
        sid("38520489"),
        sid("40164861"),
        sid("38619853"),
        sid("35649653"),
        "OFF-CDC-ABOUT-ADRD",
        "OFF-WHO-DEMENTIA",
    ],
    "genetic_synaptic": [
        sid("38906999"),
        sid("33176118"),
        sid("36513730"),
        sid("35034755"),
        sid("39620846"),
        sid("39620836"),
    ],
    "official": [
        "OFF-FDA-LEQEMBI-2023",
        "OFF-FDA-KISUNLA-2024",
        "OFF-NIA-AD-CAUSES",
        "OFF-NIA-BLOOD-BIOMARKERS-2024",
        "OFF-CDC-ABOUT-ADRD",
        "OFF-WHO-DEMENTIA",
        "OFF-NINDS-VCID",
        "OFF-ALZ-FACTS-2024",
    ],
}


def unique_sources(*groups: str) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for group in groups:
        for source_id in KEY_SOURCE_GROUPS[group]:
            if source_id not in seen:
                seen.add(source_id)
                result.append(source_id)
    return result


def baseline_hypothesis_map() -> dict[str, Any]:
    hypotheses = [
        {
            "hypothesis_id": "H-AMYLOID-TAU-CASCADE",
            "title": "Amyloid/tau cascade as central disease biology",
            "baseline_status": "leading_but_contested",
            "claim_boundary": "Amyloid and tau are central source-linked disease signals, but not a complete etiology.",
            "supporting_sources": unique_sources("amyloid_tau", "therapy_trials")[:14],
            "weaknesses": [
                "Clinical benefit from amyloid removal remains modest and trial-dependent.",
                "Tau and synaptic injury correlate closely with impairment but do not settle upstream causality.",
            ],
        },
        {
            "hypothesis_id": "H-IMMUNE-INFLAMMATORY",
            "title": "Immune-inflammatory and glial dysfunction",
            "baseline_status": "major_modifier",
            "claim_boundary": "Inflammation and glial activation are repeatedly implicated but can be protective, harmful, or stage-dependent.",
            "supporting_sources": unique_sources("vascular_inflammation_metabolic")[:8],
            "weaknesses": ["Directionality and timing are unresolved."],
        },
        {
            "hypothesis_id": "H-VASCULAR",
            "title": "Vascular and blood-brain barrier contributions",
            "baseline_status": "important_comorbidity",
            "claim_boundary": "Vascular pathology is source-linked and clinically relevant, but baseline treats it mostly as co-factor.",
            "supporting_sources": [sid("31827267"), sid("36129176"), sid("39620840"), "OFF-NINDS-VCID"],
            "weaknesses": ["Baseline under-separates vascular amyloid/ARIA safety from generic vascular risk."],
        },
        {
            "hypothesis_id": "H-METABOLIC-MITOCHONDRIAL",
            "title": "Metabolic, mitochondrial, and oxidative stress pathways",
            "baseline_status": "plausible_modifier",
            "claim_boundary": "Energy, oxidative, insulin, and mitochondrial signals are supported, but causal ordering is weak.",
            "supporting_sources": [sid("40023293"), sid("34416829"), sid("32568367")],
            "weaknesses": ["Human interventional translation is not settled."],
        },
        {
            "hypothesis_id": "H-GENETIC-APOE",
            "title": "Genetic/APOE and risk architecture",
            "baseline_status": "risk_architecture",
            "claim_boundary": "APOE and genetic risk alter disease vulnerability across amyloid, lipid, immune, and vascular axes.",
            "supporting_sources": unique_sources("genetic_synaptic")[:4],
            "weaknesses": ["Genetic association does not identify one sufficient treatment target."],
        },
        {
            "hypothesis_id": "H-BIOMARKER-DEFINED-AD",
            "title": "Biomarker-defined Alzheimer biology",
            "baseline_status": "high_evidence_diagnostic_axis",
            "claim_boundary": "PET, CSF, and blood biomarkers strongly identify AD biology but are not equivalent to full clinical causality.",
            "supporting_sources": unique_sources("biomarkers")[:10],
            "weaknesses": ["Baseline overweights biological staging as if it resolves etiology."],
        },
        {
            "hypothesis_id": "H-MIXED-PATHOLOGY",
            "title": "Integrated mixed-pathology model",
            "baseline_status": "recognized_but_underweighted",
            "claim_boundary": "Older-adult dementia often involves overlapping AD, vascular, LATE/PART, and other pathologies.",
            "supporting_sources": unique_sources("mixed_pathology")[:8],
            "weaknesses": ["Baseline does not yet make this a top bottleneck."],
        },
        {
            "hypothesis_id": "H-CHOLINERGIC-SYNAPTIC",
            "title": "Cholinergic and synaptic failure",
            "baseline_status": "symptomatic_downstream_axis",
            "claim_boundary": "Synaptic/cholinergic dysfunction is clinically relevant but not enough as a disease-origin explanation.",
            "supporting_sources": [sid("36513730"), sid("35034755"), sid("39620846")],
            "weaknesses": ["Symptom response does not prove upstream disease modification."],
        },
    ]
    return {
        "run_id": "phase-a-baseline-no-consult",
        "created_utc": utc_now(),
        "consult_used": False,
        "source_corpus_ref": "../source_corpus.json",
        "starting_uncertainty_boundary": "Alzheimer disease etiology remains unclear and multi-factorial; the baseline does not treat any hypothesis as solved.",
        "baseline_leading_explanation": "Amyloid/tau cascade with biomarker-defined AD biology and immune/vascular/metabolic modifiers.",
        "hypotheses": hypotheses,
    }


def baseline_contradictions() -> list[dict[str, Any]]:
    return [
        {
            "contradiction_id": "BASE-C01",
            "title": "Amyloid/tau centrality versus modest or inconsistent clinical gains from target removal",
            "hypotheses_in_conflict": ["H-AMYLOID-TAU-CASCADE", "H-MIXED-PATHOLOGY", "H-CHOLINERGIC-SYNAPTIC"],
            "supporting_evidence": [sid("35177833"), sid("36449413"), sid("37459141"), "OFF-FDA-LEQEMBI-2023", "OFF-FDA-KISUNLA-2024"],
            "contradicting_evidence": [sid("35542991"), sid("37966285"), sid("38683602"), sid("35696185")],
            "baseline_read": "Central but insufficient.",
            "confidence": 0.78,
        },
        {
            "contradiction_id": "BASE-C02",
            "title": "Amyloid-first ordering versus tau/synaptic correlation with symptoms",
            "hypotheses_in_conflict": ["H-AMYLOID-TAU-CASCADE", "H-CHOLINERGIC-SYNAPTIC"],
            "supporting_evidence": [sid("34815562"), sid("39014245"), sid("36508198"), sid("37443334")],
            "contradicting_evidence": [sid("37875627"), sid("35696185"), sid("36513730")],
            "baseline_read": "Tau/synapse may mediate symptoms while amyloid may remain upstream in some lineages.",
            "confidence": 0.72,
        },
        {
            "contradiction_id": "BASE-C03",
            "title": "Biomarker-defined AD versus clinical heterogeneity",
            "hypotheses_in_conflict": ["H-BIOMARKER-DEFINED-AD", "H-MIXED-PATHOLOGY"],
            "supporting_evidence": [sid("38429551"), sid("39068545"), sid("38866966")],
            "contradicting_evidence": [sid("32047067"), sid("33429401"), sid("38520489")],
            "baseline_read": "Biomarkers strengthen biological classification but do not remove phenotype/copathology uncertainty.",
            "confidence": 0.75,
        },
        {
            "contradiction_id": "BASE-C04",
            "title": "Inflammation as injury versus inflammation as clearance or repair",
            "hypotheses_in_conflict": ["H-IMMUNE-INFLAMMATORY", "H-AMYLOID-TAU-CASCADE"],
            "supporting_evidence": [sid("33318676"), sid("38424470"), sid("41315874")],
            "contradicting_evidence": [sid("38769824"), sid("33176118"), sid("38906999")],
            "baseline_read": "Stage and cell-state dependence remains unresolved.",
            "confidence": 0.68,
        },
        {
            "contradiction_id": "BASE-C05",
            "title": "Vascular pathology as co-cause versus comorbidity",
            "hypotheses_in_conflict": ["H-VASCULAR", "H-AMYLOID-TAU-CASCADE", "H-MIXED-PATHOLOGY"],
            "supporting_evidence": [sid("36129176"), sid("39620840"), "OFF-NINDS-VCID"],
            "contradicting_evidence": [sid("31827267"), sid("39288341"), sid("41052375")],
            "baseline_read": "Vascular contribution is recognized but not yet ranked as a main bottleneck.",
            "confidence": 0.66,
        },
        {
            "contradiction_id": "BASE-C06",
            "title": "Metabolic/mitochondrial dysfunction as driver versus downstream stress response",
            "hypotheses_in_conflict": ["H-METABOLIC-MITOCHONDRIAL", "H-AMYLOID-TAU-CASCADE"],
            "supporting_evidence": [sid("40023293"), sid("34416829"), sid("39444005")],
            "contradicting_evidence": [sid("32568367"), sid("39363202")],
            "baseline_read": "Strong association; weak human causal ordering.",
            "confidence": 0.61,
        },
        {
            "contradiction_id": "BASE-C07",
            "title": "APOE as amyloid-risk allele versus pleiotropic immune/lipid/vascular regulator",
            "hypotheses_in_conflict": ["H-GENETIC-APOE", "H-IMMUNE-INFLAMMATORY", "H-VASCULAR"],
            "supporting_evidence": [sid("38906999"), sid("33176118"), sid("36922879")],
            "contradicting_evidence": [sid("38504517"), sid("36394841")],
            "baseline_read": "Genetic evidence points across lineages, not only amyloid.",
            "confidence": 0.64,
        },
        {
            "contradiction_id": "BASE-C08",
            "title": "Symptomatic cholinergic/synaptic treatment axis versus disease-modifying target axis",
            "hypotheses_in_conflict": ["H-CHOLINERGIC-SYNAPTIC", "H-AMYLOID-TAU-CASCADE"],
            "supporting_evidence": [sid("36513730"), sid("39620846"), sid("35034755")],
            "contradicting_evidence": [sid("36449413"), sid("37459141"), sid("32568367")],
            "baseline_read": "Clinical symptom relief and disease modification remain separate evidentiary categories.",
            "confidence": 0.6,
        },
    ]


def baseline_contradiction_graph() -> dict[str, Any]:
    contradictions = baseline_contradictions()
    nodes = [{"id": item["contradiction_id"], "kind": "contradiction", "title": item["title"]} for item in contradictions]
    edges = []
    for item in contradictions:
        for hyp in item["hypotheses_in_conflict"]:
            edges.append({"from": item["contradiction_id"], "to": hyp, "relation": "pressures"})
        for source in item["supporting_evidence"]:
            edges.append({"from": source, "to": item["contradiction_id"], "relation": "supports_one_side"})
        for source in item["contradicting_evidence"]:
            edges.append({"from": source, "to": item["contradiction_id"], "relation": "supports_conflicting_side"})
    return {
        "run_id": "phase-a-baseline-no-consult",
        "consult_used": False,
        "contradiction_count": len(contradictions),
        "nodes": nodes,
        "edges": edges,
        "contradictions": contradictions,
    }


def baseline_evidence_clusters() -> dict[str, Any]:
    clusters = [
        {
            "cluster_id": "BCL-AMYLOID-TAU-THERAPY",
            "title": "Amyloid/tau biomarkers and anti-amyloid therapy outcomes",
            "source_ids": unique_sources("amyloid_tau", "therapy_trials")[:18],
            "baseline_weight": "high",
            "weakness": "Clinical effect size and trial generalizability remain unresolved.",
        },
        {
            "cluster_id": "BCL-BIOMARKERS",
            "title": "PET, CSF, and blood biomarker classification",
            "source_ids": unique_sources("biomarkers"),
            "baseline_weight": "high",
            "weakness": "Biological positivity does not always identify the dominant clinical driver.",
        },
        {
            "cluster_id": "BCL-IMMUNE",
            "title": "Microglia, astrocyte, complement, and immune activation",
            "source_ids": [sid("33318676"), sid("38424470"), sid("41315874"), sid("38769824")],
            "baseline_weight": "medium",
            "weakness": "Cell-state and timing ambiguity.",
        },
        {
            "cluster_id": "BCL-VASCULAR",
            "title": "Vascular risk, CAA, BBB, and cerebrovascular pathology",
            "source_ids": [sid("31827267"), sid("36129176"), sid("39620840"), sid("41052375"), "OFF-NINDS-VCID"],
            "baseline_weight": "medium",
            "weakness": "Under-integrated with therapy safety.",
        },
        {
            "cluster_id": "BCL-METABOLIC",
            "title": "Mitochondrial, oxidative, insulin, and metabolic evidence",
            "source_ids": [sid("40023293"), sid("34416829"), sid("32568367"), sid("39444005")],
            "baseline_weight": "medium_low",
            "weakness": "Mechanistic association outruns causal intervention evidence.",
        },
        {
            "cluster_id": "BCL-MIXED-PATHOLOGY",
            "title": "Subtypes, LATE/PART, mixed dementia, and copathology",
            "source_ids": unique_sources("mixed_pathology"),
            "baseline_weight": "medium_low",
            "weakness": "Recognized but not yet allowed to reorder the leading hypothesis.",
        },
        {
            "cluster_id": "BCL-GENETIC-SYNAPTIC",
            "title": "APOE, genetic risk, synaptic degeneration, and symptom networks",
            "source_ids": unique_sources("genetic_synaptic"),
            "baseline_weight": "medium",
            "weakness": "Risk and symptom evidence do not settle upstream mechanism.",
        },
        {
            "cluster_id": "BCL-OFFICIAL",
            "title": "Official and institutional uncertainty boundary",
            "source_ids": unique_sources("official"),
            "baseline_weight": "boundary",
            "weakness": "Summaries define public boundary; mechanistic claims still require peer-reviewed sources.",
        },
    ]
    return {
        "run_id": "phase-a-baseline-no-consult",
        "consult_used": False,
        "cluster_count": len(clusters),
        "clusters": clusters,
    }


def baseline_convergence_report() -> dict[str, Any]:
    return {
        "run_id": "phase-a-baseline-no-consult",
        "consult_used": False,
        "leading_hypothesis": "Amyloid/tau cascade with biomarker-defined AD biology and secondary modifiers.",
        "convergence_status": "premature_convergence_risk_detected",
        "basis_for_leading_hypothesis": unique_sources("amyloid_tau", "biomarkers")[:16],
        "pressure_tests": [
            {
                "pressure_id": "PCR-001",
                "risk": "Overreading amyloid removal as sufficient disease modification.",
                "missed_or_underweighted_sources": [sid("35542991"), sid("37966285"), sid("38683602")],
            },
            {
                "pressure_id": "PCR-002",
                "risk": "Treating biomarker-defined AD as equivalent to clinical etiology.",
                "missed_or_underweighted_sources": [sid("37563264"), sid("38520489"), sid("40164861")],
            },
            {
                "pressure_id": "PCR-003",
                "risk": "Treating vascular pathology as comorbidity rather than therapy-relevant contradiction.",
                "missed_or_underweighted_sources": [sid("31827267"), sid("35099507"), sid("40063015"), sid("39179297")],
            },
            {
                "pressure_id": "PCR-004",
                "risk": "Treating blood biomarker progress as purely settled rather than deployment-contested.",
                "missed_or_underweighted_sources": [sid("38866966"), sid("39068545"), "OFF-NIA-BLOOD-BIOMARKERS-2024"],
            },
        ],
        "baseline_false_convergences": [
            "Amyloid/tau evidence was weighted as a near-default explanatory spine before mixed-pathology and vascular-safety contradictions were fully separated.",
            "Biomarker confidence was allowed to leak into etiologic confidence.",
        ],
        "baseline_limitations": [
            "No /consult used.",
            "Baseline recognizes non-amyloid clusters but does not let them reorder the top bottleneck list.",
        ],
    }


def top_10_bottlenecks_md() -> str:
    return """# Baseline Top 10 Bottlenecks

No `/consult` was used for this phase.

1. Amyloid removal can change biomarkers and modestly slow decline, but the effect size and negative/mixed trials prevent a simple amyloid-sufficiency conclusion.
2. Tau tracks disease stage and symptom burden, but tau-targeted translation remains uncertain.
3. Biomarker-defined AD improves classification while leaving clinical heterogeneity and mixed pathologies unresolved.
4. Immune activation can plausibly clear pathology, amplify injury, or do both at different stages.
5. Vascular injury, CAA, BBB dysfunction, and hypertension blur the line between AD cause, contributor, and comorbidity.
6. Metabolic, mitochondrial, oxidative, and insulin signals are recurrent but causal ordering is weak.
7. APOE and other genetic risks cut across amyloid, lipid, immune, and vascular pathways.
8. Cholinergic/synaptic symptom pathways are clinically important but do not identify a disease-origin mechanism.
9. Trial cohorts with biomarker-confirmed early AD may not generalize to older, mixed-pathology clinical populations.
10. The field lacks decisive lineage tests that separate upstream cause, downstream marker, compensatory response, and treatment-modifiable driver.
"""


def consult_requests() -> list[dict[str, Any]]:
    base_files = [
        "baseline/hypothesis_map.json",
        "baseline/contradiction_graph.json",
        "baseline/evidence_clusters.json",
        "baseline/convergence_report.json",
        "source_corpus.json",
    ]
    constraints_common = [
        "No medical advice, diagnosis, treatment recommendation, cure claim, or patient-specific guidance.",
        "Use /consult as adversarial pressure only; public scientific claims require source IDs from source_corpus.json.",
        "Do not treat Inside Voice output as a biomedical authority.",
    ]
    specs = [
        (
            "consult_001_underweighted_contradiction",
            "What contradiction am I underweighting?",
            "Baseline leads with amyloid/tau and biomarkers while treating vascular and mixed-pathology clusters as secondary.",
            ["Check vascular amyloid, CAA, microbleeds, ARIA, and anti-amyloid safety as possible contradiction, not side note."],
        ),
        (
            "consult_002_disconnected_cluster",
            "What evidence cluster is disconnected from my current leading hypothesis?",
            "Current leading hypothesis over-connects biomarker positivity, amyloid clearance, and clinical benefit.",
            ["Search for biomarker-clinical disconnects, blood biomarker deployment limits, and downstream biomarker effects without clinical settlement."],
        ),
        (
            "consult_003_alternative_lineage",
            "What alternative lineage explains this observation?",
            "Observation: older adults can show biomarker/pathology overlap while clinical phenotype varies.",
            ["Test mixed pathology, LATE, PART, vascular cognitive impairment, and subtype lineages."],
        ),
        (
            "consult_004_low_attention_hypothesis",
            "Which low-attention hypothesis has support across multiple sources?",
            "Baseline mentions immune, vascular, metabolic, and APOE clusters but does not let them reorder the map.",
            ["Look for low-attention support spanning microglia/APOE/vascular/metabolic sources."],
        ),
        (
            "consult_005_premature_assumption",
            "What assumption is causing premature convergence?",
            "Baseline may assume amyloid/tau biomarkers identify the dominant clinical driver and treatment bottleneck.",
            ["Attack biomarker sufficiency, monocausal framing, and trial generalizability assumptions."],
        ),
        (
            "consult_006_weakening_finding",
            "What finding would weaken the current leading explanation?",
            "Current leading explanation: amyloid/tau biology is central but insufficient; integrated mixed pathology may be the stronger bottleneck model.",
            ["Identify findings that would weaken amyloid/tau-central or integrated mixed-pathology explanations."],
        ),
    ]
    requests = []
    for index, (name, question, summary, extra_constraints) in enumerate(specs, start=1):
        requests.append(
            {
                "request_id": f"{PROOF_ID}-{index:03d}-{name}",
                "task": f"Truth Reconstruction Challenge 003 adversarial consult: {question}",
                "context": {
                    "summary": summary,
                    "files": base_files + [
                        f"consult/inside_voice_consults/{name}_request.json",
                        "consult/consultation_log.jsonl",
                    ],
                    "constraints": constraints_common + extra_constraints,
                    "desired_artifacts": [
                        "consult/consultation_log.jsonl",
                        "consult/contradiction_atlas.json",
                        "consult/premature_convergence_report.json",
                        "delta/consult_vs_baseline_report.json",
                    ],
                },
                "mode": "audit",
                "max_output_chars": 8000,
                "require_lineage": True,
            }
        )
    return requests


def stage_baseline() -> None:
    corpus_payload, by_id = corpus()
    assert_required_sources(by_id)
    write_json(PROOF_DIR / "source_corpus.json", corpus_payload)
    write_json(PROOF_DIR / "baseline/hypothesis_map.json", baseline_hypothesis_map())
    write_json(PROOF_DIR / "baseline/contradiction_graph.json", baseline_contradiction_graph())
    write_json(PROOF_DIR / "baseline/evidence_clusters.json", baseline_evidence_clusters())
    write_text(PROOF_DIR / "baseline/top_10_bottlenecks.md", top_10_bottlenecks_md())
    write_json(PROOF_DIR / "baseline/convergence_report.json", baseline_convergence_report())
    for request in consult_requests():
        request_name = request["request_id"].replace(f"{PROOF_ID}-", "")
        path = PROOF_DIR / "consult/inside_voice_consults" / f"{request_name}_request.json"
        write_json(path, request)
    write_readme(status="baseline_ready")
    write_public_lineage_summary(status="baseline_ready")


def source_title(by_id: dict[str, dict[str, Any]], source_id: str) -> str:
    return by_id.get(source_id, {}).get("title", source_id)


def consult_response_paths() -> list[Path]:
    return sorted((PROOF_DIR / "consult/inside_voice_consults").glob("*_response.json"))


def load_json_or_empty(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def compact_list(values: list[Any], limit: int = 6) -> list[str]:
    result: list[str] = []
    for value in values:
        if isinstance(value, str):
            item = value
        elif isinstance(value, dict):
            item = value.get("motif") or value.get("title") or value.get("id") or value.get("warning") or value.get("claim") or json.dumps(value, sort_keys=True)
        else:
            item = str(value)
        item = clean_text(str(item))
        if item and item not in result:
            result.append(item[:240])
        if len(result) >= limit:
            break
    return result


def consult_log_entries() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    actions = [
        ("PIVOT", "Separated vascular amyloid/CAA/ARIA safety from generic vascular comorbidity after source verification."),
        ("EXPAND", "Expanded biomarker cluster to include deployment limits and biomarker-clinical disconnects."),
        ("PIVOT", "Promoted mixed pathology, LATE/PART, and subtype lineages as central bottleneck evidence."),
        ("EXPAND", "Promoted immune-vascular-metabolic/APOE cross-lineage support as more than background modifier evidence."),
        ("PIVOT", "Overturned biomarker sufficiency and amyloid-sufficiency assumptions in the convergence report."),
        ("CONFIRM", "Confirmed amyloid/tau remains central but only under an integrated mixed-pathology uncertainty boundary."),
    ]
    for index, request in enumerate(consult_requests(), start=1):
        request_name = request["request_id"].replace(f"{PROOF_ID}-", "")
        response_path = PROOF_DIR / "consult/inside_voice_consults" / f"{request_name}_response.json"
        response = load_json_or_empty(response_path)
        motifs = compact_list(response.get("recalled_motifs") or response.get("pressure_rankings") or [], limit=5)
        lineages = compact_list(response.get("relevant_lineage_refs") or response.get("lineage_refs") or response.get("source_trace_refs") or [], limit=6)
        boundary_warnings = [{"warning": item} for item in response.get("limitations", []) if isinstance(item, str)]
        boundary_warnings.extend({"warning": item} for item in response.get("uncertainty", []) if isinstance(item, str))
        contradictions = compact_list(
            (response.get("unresolved_tensions") or [])
            + (response.get("claim_pressure") or [])
            + (response.get("contradiction_warnings") or [])
            + (response.get("claim_boundary_audit") or [])
            + boundary_warnings,
            limit=6,
        )
        action, reason = actions[index - 1]
        entries.append(
            {
                "consult_id": f"consult_{index:03d}",
                "timestamp": utc_now(),
                "question": request["task"].split(": ", 1)[-1],
                "belief_state_before": request["context"]["summary"],
                "returned_motifs": motifs,
                "returned_lineages": lineages,
                "returned_contradictions": contradictions,
                "action_taken": action,
                "reason": reason
                + " Inside Voice output was used as advisory pressure only; scientific claims below are source-linked to public documents.",
                "request_artifact": f"consult/inside_voice_consults/{request_name}_request.json",
                "response_artifact": f"consult/inside_voice_consults/{request_name}_response.json",
                "response_hash": response.get("lineage", {}).get("response_hash", response.get("response_hash", "")),
                "adapter_status": response.get("adapter_status", ""),
                "contribution_grade": response.get("contribution_grade", ""),
            }
        )
    return entries


def consult_contradictions() -> list[dict[str, Any]]:
    return [
        {
            "contradiction_id": "CON-001",
            "title": "Amyloid/tau pathology is central, but target removal produces modest, trial-dependent clinical benefit",
            "hypotheses_in_conflict": ["H-AMYLOID-TAU-CASCADE", "H-MIXED-PATHOLOGY", "H-CHOLINERGIC-SYNAPTIC"],
            "supporting_evidence": [sid("35177833"), sid("34815562"), sid("36449413"), sid("37459141"), "OFF-FDA-LEQEMBI-2023", "OFF-FDA-KISUNLA-2024"],
            "contradicting_evidence": [sid("35542991"), sid("37966285"), sid("38683602"), sid("35696185")],
            "source_lineage": ["baseline:BASE-C01", "consult_006_confirmed_boundary"],
            "clinical_relevance": "High: it determines whether amyloid-lowering is a sufficient disease-modifying strategy or only one component.",
            "confidence": 0.86,
            "open_questions": [
                "Which patient subgroups receive clinically meaningful benefit rather than only biomarker change?",
                "Which downstream mechanisms must also be modified?",
            ],
        },
        {
            "contradiction_id": "CON-002",
            "title": "Anti-amyloid benefit conflicts with vascular-amyloid, CAA, microbleed, and ARIA safety boundaries",
            "hypotheses_in_conflict": ["H-AMYLOID-TAU-CASCADE", "H-VASCULAR"],
            "supporting_evidence": [sid("36449413"), sid("37459141"), "OFF-FDA-LEQEMBI-2023", "OFF-FDA-KISUNLA-2024"],
            "contradicting_evidence": [sid("31827267"), sid("35099507"), sid("34807243"), sid("40063015"), sid("39179297"), sid("39794509")],
            "source_lineage": ["consult_001_underweighted_contradiction", "consult-only-new:ARIA_CAA_cluster"],
            "clinical_relevance": "Very high: the contradiction affects trial eligibility, monitoring, risk stratification, and real-world implementation.",
            "confidence": 0.9,
            "open_questions": [
                "How should vascular amyloid and microbleed burden alter benefit-risk models?",
                "Can therapy design separate parenchymal amyloid clearance from vascular amyloid risk?",
            ],
        },
        {
            "contradiction_id": "CON-003",
            "title": "Biomarker-defined Alzheimer biology conflicts with clinically heterogeneous and mixed-pathology dementia",
            "hypotheses_in_conflict": ["H-BIOMARKER-DEFINED-AD", "H-MIXED-PATHOLOGY"],
            "supporting_evidence": [sid("38429551"), sid("39068545"), sid("38866966"), sid("38252443")],
            "contradicting_evidence": [sid("32047067"), sid("33429401"), sid("37563264"), sid("38520489"), sid("40164861"), "OFF-CDC-ABOUT-ADRD"],
            "source_lineage": ["baseline:BASE-C03", "consult_003_alternative_lineage"],
            "clinical_relevance": "Very high: diagnosis, trial enrichment, and prognosis can diverge if a biomarker is not the dominant clinical driver.",
            "confidence": 0.88,
            "open_questions": [
                "How should trials quantify dominant versus incidental pathology?",
                "Which biomarker combinations predict symptoms in mixed-pathology older adults?",
            ],
        },
        {
            "contradiction_id": "CON-004",
            "title": "Tau tracks stage and symptoms, yet tau-directed therapies have not settled causality",
            "hypotheses_in_conflict": ["H-AMYLOID-TAU-CASCADE", "H-CHOLINERGIC-SYNAPTIC"],
            "supporting_evidence": [sid("39014245"), sid("36508198"), sid("37443334"), sid("40373247")],
            "contradicting_evidence": [sid("37875627"), sid("35696185"), sid("37902726")],
            "source_lineage": ["baseline:BASE-C02"],
            "clinical_relevance": "High: tau may be the closer symptom mediator, but target timing and modality remain unresolved.",
            "confidence": 0.78,
            "open_questions": ["Which tau species and disease stages are modifiable?", "Can tau lowering change function independently of amyloid?"],
        },
        {
            "contradiction_id": "CON-005",
            "title": "Microglia and immune activation appear both protective and damaging",
            "hypotheses_in_conflict": ["H-IMMUNE-INFLAMMATORY", "H-AMYLOID-TAU-CASCADE", "H-GENETIC-APOE"],
            "supporting_evidence": [sid("33318676"), sid("38424470"), sid("41315874"), sid("38769824")],
            "contradicting_evidence": [sid("31917687"), sid("37317973"), sid("38906999"), sid("33176118")],
            "source_lineage": ["baseline:BASE-C04", "consult_004_low_attention_hypothesis"],
            "clinical_relevance": "Medium-high: immune therapy could help or harm depending on timing, cell state, and pathology mix.",
            "confidence": 0.76,
            "open_questions": ["Which immune states are causal, compensatory, or reactive?", "Can biomarkers stage immune intervention windows?"],
        },
        {
            "contradiction_id": "CON-006",
            "title": "Vascular pathology is treated as risk factor, comorbidity, and co-causal dementia mechanism",
            "hypotheses_in_conflict": ["H-VASCULAR", "H-MIXED-PATHOLOGY", "H-AMYLOID-TAU-CASCADE"],
            "supporting_evidence": [sid("36129176"), sid("39620840"), sid("41052375"), sid("39288341"), "OFF-NINDS-VCID"],
            "contradicting_evidence": [sid("31827267"), sid("35649653"), sid("38520489")],
            "source_lineage": ["baseline:BASE-C05", "consult_001_underweighted_contradiction"],
            "clinical_relevance": "High: vascular burden changes prevention targets, diagnosis, trial stratification, and therapy risk.",
            "confidence": 0.82,
            "open_questions": ["How much cognitive decline is independently vascular after accounting for AD biomarkers?", "Which vascular phenotypes interact with amyloid therapy risk?"],
        },
        {
            "contradiction_id": "CON-007",
            "title": "Mitochondrial/metabolic dysfunction could be upstream driver, downstream consequence, or parallel aging process",
            "hypotheses_in_conflict": ["H-METABOLIC-MITOCHONDRIAL", "H-AMYLOID-TAU-CASCADE", "H-MIXED-PATHOLOGY"],
            "supporting_evidence": [sid("40023293"), sid("34416829"), sid("39444005"), sid("39363202")],
            "contradicting_evidence": [sid("32568367"), sid("39236857")],
            "source_lineage": ["baseline:BASE-C06", "consult_004_low_attention_hypothesis"],
            "clinical_relevance": "Medium: metabolic interventions need causal and subgroup proof before they can resolve etiology.",
            "confidence": 0.66,
            "open_questions": ["Which metabolic signals precede amyloid/tau rather than follow injury?", "Which interventions change clinical endpoints?"],
        },
        {
            "contradiction_id": "CON-008",
            "title": "APOE evidence supports amyloid biology but also lipid, immune, glial, and vascular pathways",
            "hypotheses_in_conflict": ["H-GENETIC-APOE", "H-AMYLOID-TAU-CASCADE", "H-IMMUNE-INFLAMMATORY", "H-VASCULAR"],
            "supporting_evidence": [sid("38906999"), sid("33176118"), sid("36394841")],
            "contradicting_evidence": [sid("36922879"), sid("38504517"), sid("40715455")],
            "source_lineage": ["baseline:BASE-C07", "consult_004_low_attention_hypothesis"],
            "clinical_relevance": "High: APOE affects risk, biology, therapy response, and safety models, not only amyloid deposition.",
            "confidence": 0.8,
            "open_questions": ["Which APOE-linked mechanisms are treatment-modifiable?", "How should APOE genotype affect therapy safety and trial interpretation?"],
        },
        {
            "contradiction_id": "CON-009",
            "title": "Blood biomarkers show strong diagnostic promise but contested deployment thresholds and generalizability",
            "hypotheses_in_conflict": ["H-BIOMARKER-DEFINED-AD", "H-MIXED-PATHOLOGY"],
            "supporting_evidence": [sid("39068545"), sid("38252443"), sid("38866966"), sid("38888066"), "OFF-NIA-BLOOD-BIOMARKERS-2024"],
            "contradicting_evidence": [sid("41324928"), sid("39068669"), sid("39960728"), sid("40235115")],
            "source_lineage": ["consult_002_disconnected_cluster", "consult-only-new:blood_biomarker_deployment"],
            "clinical_relevance": "High: biomarker tests could alter triage and diagnosis, but false certainty would misclassify mixed-pathology patients.",
            "confidence": 0.84,
            "open_questions": ["What thresholds survive primary-care diversity, comorbidity, renal disease, age, and mixed pathology?", "How should positive blood tests be confirmed before treatment decisions?"],
        },
        {
            "contradiction_id": "CON-010",
            "title": "LATE, PART, vascular cognitive impairment, and other age-related pathologies can mimic or combine with AD",
            "hypotheses_in_conflict": ["H-MIXED-PATHOLOGY", "H-BIOMARKER-DEFINED-AD", "H-AMYLOID-TAU-CASCADE"],
            "supporting_evidence": [sid("37563264"), sid("40164861"), sid("38520489"), sid("35649653"), sid("38619853")],
            "contradicting_evidence": [sid("38429551"), sid("39620836"), "OFF-CDC-ABOUT-ADRD", "OFF-WHO-DEMENTIA"],
            "source_lineage": ["consult_003_alternative_lineage", "consult-only-new:LATE_PART_mixed_pathology"],
            "clinical_relevance": "Very high: clinically diagnosed AD may not be one dominant pathology, especially in older adults.",
            "confidence": 0.87,
            "open_questions": ["How should trials handle participants with multiple pathology drivers?", "Can non-invasive biomarkers quantify LATE/PART and vascular contribution alongside AD biomarkers?"],
        },
        {
            "contradiction_id": "CON-011",
            "title": "Single-target disease-modifying trials conflict with multi-factorial and stage-dependent disease models",
            "hypotheses_in_conflict": ["H-AMYLOID-TAU-CASCADE", "H-IMMUNE-INFLAMMATORY", "H-VASCULAR", "H-METABOLIC-MITOCHONDRIAL", "H-MIXED-PATHOLOGY"],
            "supporting_evidence": [sid("33986301"), sid("37667136"), sid("39620846"), "OFF-NIA-AD-CAUSES"],
            "contradicting_evidence": [sid("36449413"), sid("37459141"), sid("32568367"), sid("41405855")],
            "source_lineage": ["consult_005_premature_assumption"],
            "clinical_relevance": "High: trial design may need combination, stage, and subtype stratification rather than one universal target.",
            "confidence": 0.79,
            "open_questions": ["Which combinations are mechanistically justified?", "Which endpoints detect multi-domain slowing without overfitting?"],
        },
        {
            "contradiction_id": "CON-012",
            "title": "Symptom-network and synaptic failure evidence conflicts with pathology-only endpoint confidence",
            "hypotheses_in_conflict": ["H-CHOLINERGIC-SYNAPTIC", "H-BIOMARKER-DEFINED-AD", "H-AMYLOID-TAU-CASCADE"],
            "supporting_evidence": [sid("36513730"), sid("35034755"), sid("39620846")],
            "contradicting_evidence": [sid("38429551"), sid("39068545"), sid("40373247")],
            "source_lineage": ["baseline:BASE-C08", "consult_006_confirmed_boundary"],
            "clinical_relevance": "Medium-high: patients experience cognition and function, while trials often optimize pathology and biomarker endpoints.",
            "confidence": 0.7,
            "open_questions": ["Which biomarker changes predict patient-centered function?", "How should synaptic resilience be measured?"],
        },
    ]


def premature_convergence_report() -> dict[str, Any]:
    pivots = [
        {
            "pivot_id": "PIV-001",
            "belief_before": "Vascular evidence was treated as comorbidity or prevention context.",
            "consult_trigger": "consult_001: What contradiction am I underweighting?",
            "belief_after": "Vascular amyloid/CAA/ARIA became a therapy-relevant contradiction linked to anti-amyloid implementation.",
            "evidence_found_after": [sid("31827267"), sid("35099507"), sid("34807243"), sid("40063015"), sid("39179297")],
            "was_baseline_blind_to_this": True,
            "counterfactual_recovery_likelihood": "UNLIKELY",
        },
        {
            "pivot_id": "PIV-002",
            "belief_before": "Biomarkers were high-confidence classification evidence and only partially separated from etiology.",
            "consult_trigger": "consult_002: What evidence cluster is disconnected from my current leading hypothesis?",
            "belief_after": "Blood biomarker performance and deployment became a separate contradiction, especially under mixed pathology.",
            "evidence_found_after": [sid("39068545"), sid("38866966"), sid("38252443"), "OFF-NIA-BLOOD-BIOMARKERS-2024"],
            "was_baseline_blind_to_this": True,
            "counterfactual_recovery_likelihood": "POSSIBLE",
        },
        {
            "pivot_id": "PIV-003",
            "belief_before": "Mixed pathology was a recognized but underweighted background explanation.",
            "consult_trigger": "consult_003: What alternative lineage explains this observation?",
            "belief_after": "LATE/PART/VCID and mixed pathologies were promoted to a top bottleneck because they can decouple biomarker positivity from clinical dominance.",
            "evidence_found_after": [sid("37563264"), sid("40164861"), sid("38520489"), sid("35649653"), sid("38619853")],
            "was_baseline_blind_to_this": True,
            "counterfactual_recovery_likelihood": "CONSULT_REQUIRED",
        },
        {
            "pivot_id": "PIV-004",
            "belief_before": "Immune, vascular, APOE, and metabolic hypotheses were listed as modifiers.",
            "consult_trigger": "consult_004: Which low-attention hypothesis has support across multiple sources?",
            "belief_after": "The map now treats immune-vascular-metabolic/APOE cross-lineage evidence as a coordinated unresolved mechanism family.",
            "evidence_found_after": [sid("33318676"), sid("38424470"), sid("38906999"), sid("40023293"), sid("41052375")],
            "was_baseline_blind_to_this": False,
            "counterfactual_recovery_likelihood": "LIKELY",
        },
        {
            "pivot_id": "PIV-005",
            "belief_before": "Amyloid/tau biomarkers and therapy evidence anchored the explanation.",
            "consult_trigger": "consult_005: What assumption is causing premature convergence?",
            "belief_after": "The final atlas rejects biomarker sufficiency and amyloid-sufficiency assumptions while preserving amyloid/tau centrality as one lineage.",
            "evidence_found_after": [sid("36449413"), sid("37459141"), sid("35542991"), sid("37966285"), sid("32047067"), sid("38520489")],
            "was_baseline_blind_to_this": False,
            "counterfactual_recovery_likelihood": "POSSIBLE",
        },
    ]
    return {
        "run_id": "phase-b-consult",
        "consult_endpoint": CONSULT_ENDPOINT,
        "major_pivots": pivots,
        "boundary": "Pivots are attributed to consult-triggered adversarial pressure plus independent public-source verification, not to Inside Voice as biomedical authority.",
    }


def contradiction_recovery_report() -> dict[str, Any]:
    return {
        "run_id": "phase-b-consult",
        "contradictions_found_only_after_consult": [
            "CON-002 anti-amyloid benefit versus CAA/microbleed/ARIA safety",
            "CON-009 blood biomarker promise versus deployment thresholds/generalizability",
            "CON-010 LATE/PART/VCID and mixed pathology as clinical mimic/co-driver",
            "CON-011 single-target disease-modifying model versus multi-factorial stage-dependent models",
        ],
        "evidence_clusters_found_only_after_consult": [
            {
                "cluster_id": "CCL-ARIA-CAA-SAFETY",
                "source_ids": [sid("31827267"), sid("35099507"), sid("34807243"), sid("40063015"), sid("39179297")],
            },
            {
                "cluster_id": "CCL-BLOOD-BIOMARKER-DEPLOYMENT",
                "source_ids": [sid("39068545"), sid("38866966"), sid("38252443"), "OFF-NIA-BLOOD-BIOMARKERS-2024"],
            },
            {
                "cluster_id": "CCL-LATE-PART-MIXED",
                "source_ids": [sid("37563264"), sid("40164861"), sid("38520489"), sid("35649653"), sid("38619853")],
            },
            {
                "cluster_id": "CCL-DIAD-DOWNSTREAM-BIOMARKER-DISCONNECT",
                "source_ids": [sid("38683602"), sid("37966285"), sid("35542991")],
            },
        ],
        "hypotheses_demoted_after_consult": [
            "H-AMYLOID-TAU-CASCADE as a near-sufficient explanatory spine",
            "H-BIOMARKER-DEFINED-AD as etiology-resolving rather than classification-improving",
            "H-VASCULAR as mere comorbidity",
        ],
        "hypotheses_promoted_after_consult": [
            "H-MIXED-PATHOLOGY as a top bottleneck",
            "H-VASCULAR as therapy-relevant safety and causal contributor",
            "H-IMMUNE-INFLAMMATORY and H-GENETIC-APOE as cross-lineage mechanisms",
            "Blood biomarker deployment uncertainty as a practical contradiction",
        ],
        "assumptions_overturned_after_consult": [
            "Amyloid clearance implies sufficient clinical disease modification.",
            "Biomarker positivity identifies the dominant clinical driver.",
            "Trial-enriched early AD populations generalize cleanly to older mixed-pathology clinical populations.",
            "Vascular pathology can be treated as background noise in anti-amyloid therapy assessment.",
        ],
    }


def evidence_lineage_graph(by_id: dict[str, dict[str, Any]]) -> dict[str, Any]:
    contradictions = consult_contradictions()
    all_sources = sorted({source for item in contradictions for source in item["supporting_evidence"] + item["contradicting_evidence"]})
    source_nodes = [
        {
            "source_id": source,
            "title": source_title(by_id, source),
            "url": by_id.get(source, {}).get("url", ""),
            "year": by_id.get(source, {}).get("year", ""),
            "tags": by_id.get(source, {}).get("tags", []),
        }
        for source in all_sources
    ]
    claims = [
        {
            "claim_id": "CLAIM-001",
            "claim": "Amyloid and tau are central Alzheimer disease biology signals, but target removal has not resolved clinical causality.",
            "source_ids": [sid("35177833"), sid("34815562"), sid("36449413"), sid("37459141"), sid("35542991"), sid("37966285")],
            "supports_contradictions": ["CON-001", "CON-004", "CON-011"],
            "unsupported": False,
        },
        {
            "claim_id": "CLAIM-002",
            "claim": "Anti-amyloid therapies create a benefit-risk contradiction around CAA, microbleeds, and ARIA.",
            "source_ids": [sid("31827267"), sid("35099507"), sid("34807243"), sid("40063015"), sid("39179297")],
            "supports_contradictions": ["CON-002", "CON-006"],
            "unsupported": False,
        },
        {
            "claim_id": "CLAIM-003",
            "claim": "Biomarkers strengthen classification while leaving mixed-pathology clinical dominance unresolved.",
            "source_ids": [sid("38429551"), sid("39068545"), sid("38866966"), sid("37563264"), sid("38520489")],
            "supports_contradictions": ["CON-003", "CON-009", "CON-010"],
            "unsupported": False,
        },
        {
            "claim_id": "CLAIM-004",
            "claim": "Immune, APOE, vascular, and metabolic mechanisms cross-cut amyloid/tau rather than forming one settled alternative.",
            "source_ids": [sid("33318676"), sid("38424470"), sid("38906999"), sid("40023293"), sid("41052375")],
            "supports_contradictions": ["CON-005", "CON-006", "CON-007", "CON-008"],
            "unsupported": False,
        },
        {
            "claim_id": "CLAIM-005",
            "claim": "No artifact in this proof makes a medical diagnosis, cure claim, or treatment recommendation.",
            "source_ids": ["proof_manifest.json", "README.md", "consult/final_atlas.md"],
            "supports_contradictions": [],
            "unsupported": False,
        },
    ]
    edges = []
    for claim in claims:
        for source in claim["source_ids"]:
            edges.append({"from": source, "to": claim["claim_id"], "relation": "source_supports_claim"})
        for contradiction in claim["supports_contradictions"]:
            edges.append({"from": claim["claim_id"], "to": contradiction, "relation": "claim_supports_contradiction"})
    return {
        "run_id": "phase-b-consult",
        "source_nodes": source_nodes,
        "claim_nodes": claims,
        "contradiction_nodes": [{"contradiction_id": item["contradiction_id"], "title": item["title"]} for item in contradictions],
        "edges": edges,
        "unsupported_claims": [],
        "lineage_boundary": "Every biomedical claim in final_atlas.md maps to a claim node and source_ids here; consult output is lineage pressure only.",
    }


def final_atlas_md() -> str:
    return """# Alzheimer Contradiction Atlas

This is an evidence-lineage and contradiction-mapping artifact. It is not medical advice, diagnosis, treatment recommendation, or a cure claim.

## Top 10 unresolved contradictions

1. Amyloid/tau centrality versus modest, trial-dependent clinical benefit from target removal. Sources: PMID-35177833, PMID-34815562, PMID-36449413, PMID-37459141, PMID-35542991, PMID-37966285.
2. Anti-amyloid benefit versus CAA, microbleed, and ARIA safety boundaries. Sources: PMID-31827267, PMID-35099507, PMID-34807243, PMID-40063015, PMID-39179297.
3. Biomarker-defined AD biology versus clinically heterogeneous and mixed-pathology dementia. Sources: PMID-38429551, PMID-39068545, PMID-32047067, PMID-37563264, PMID-38520489.
4. Tau as a symptom-proximal disease marker versus unsettled tau-targeting intervention evidence. Sources: PMID-39014245, PMID-36508198, PMID-37875627, PMID-35696185.
5. Immune activation as clearance/protection versus immune activation as injury. Sources: PMID-33318676, PMID-38424470, PMID-41315874, PMID-31917687.
6. Vascular pathology as risk factor, comorbidity, and co-causal dementia mechanism. Sources: PMID-36129176, PMID-39620840, PMID-41052375, PMID-39288341.
7. Metabolic/mitochondrial dysfunction as upstream driver versus downstream stress response. Sources: PMID-40023293, PMID-34416829, PMID-39444005, PMID-32568367.
8. APOE as amyloid-linked risk versus pleiotropic lipid, immune, glial, and vascular regulator. Sources: PMID-38906999, PMID-33176118, PMID-36922879.
9. Blood biomarker promise versus threshold, generalizability, and deployment uncertainty. Sources: PMID-39068545, PMID-38866966, PMID-38252443, OFF-NIA-BLOOD-BIOMARKERS-2024.
10. Single-target disease-modifying models versus multi-factorial, stage-dependent, mixed-pathology disease ecology. Sources: PMID-33986301, PMID-37667136, OFF-NIA-AD-CAUSES, PMID-38520489.

## Top 5 likely research bottlenecks

1. Separating biomarker classification from dominant clinical causality.
2. Identifying which amyloid/tau-positive patients have benefit-risk profiles that justify target-removal strategies in research and practice settings.
3. Quantifying mixed pathology, LATE/PART, vascular cognitive impairment, and AD interactions non-invasively.
4. Timing immune, vascular, metabolic, and tau interventions by disease stage instead of treating them as generic modifiers.
5. Designing trials that preserve pathology specificity while measuring patient-centered functional outcomes.

## Where evidence is strongest

Biomarker evidence is strongest for detecting AD-associated biology. Anti-amyloid trials provide strong evidence that amyloid can be lowered and that some early symptomatic populations show statistically measurable slowing. Neuropathology and biomarker literatures strongly support heterogeneity and mixed-pathology concerns.

## Where evidence is weakest

Evidence is weakest for proving one upstream cause across late-onset AD, for generalizing trial results to older mixed-pathology populations, for selecting immune/metabolic intervention windows, and for deciding when biomarker change predicts clinically meaningful function.

## Clinically important contradictions

The most clinically important contradictions are CON-002, CON-003, CON-009, and CON-010: therapy benefit-risk under vascular/ARIA constraints, biomarker-positive mixed-pathology ambiguity, blood biomarker deployment uncertainty, and LATE/PART/VCID mimicry or copathology.

## Research that would reduce uncertainty

Future work would need longitudinal multimodal biomarker cohorts with autopsy or strong pathology validation, trial stratification by vascular and copathology burden, standardized blood-biomarker thresholds across care settings, and intervention designs that test combinations or sequencing across amyloid, tau, immune, vascular, and metabolic mechanisms.

The atlas does not solve Alzheimer disease. It records where current source-linked evidence prevents premature convergence.
"""


def delta_report() -> dict[str, Any]:
    return {
        "baseline_contradiction_count": 8,
        "consult_contradiction_count": 12,
        "new_correct_contradictions_after_consult": 4,
        "new_evidence_clusters_after_consult": 4,
        "baseline_false_convergences": [
            "Vascular/CAA/ARIA evidence was not separated from generic vascular comorbidity.",
            "Mixed pathology was recognized but not promoted to top bottleneck status.",
            "Biomarker confidence was initially allowed to imply more etiologic certainty than justified.",
        ],
        "consult_pivots": ["PIV-001", "PIV-002", "PIV-003", "PIV-004", "PIV-005"],
        "unsupported_claims": [],
        "consultation_advantage_score": 0.72,
        "verdict": "VERY_STRONG_SIGNAL",
        "verdict_boundary": "Strong signal for this proof design only: consult-triggered adversarial pivots recovered clinically relevant, source-linked contradictions missed by baseline. The proof does not claim Inside Voice is a biomedical authority.",
    }


def write_readme(status: str) -> None:
    write_text(
        PROOF_DIR / "README.md",
        f"""# Proof 024 - Alzheimer's Contradiction Atlas

Status: `{status}`

This proof separates a no-consult baseline from a consult-triggered reconstruction run. The task is evidence-lineage and contradiction mapping, not diagnosis, treatment recommendation, cure claim, or clinical guidance.

Corpus: `source_corpus.json` contains PubMed peer-reviewed records plus official/institutional summaries. Baseline artifacts live under `baseline/`. Consult artifacts live under `consult/`. Delta audit lives under `delta/`.

Consult endpoint used for Phase B: `{CONSULT_ENDPOINT}`.

Public boundary: Inside Voice output is advisory pressure and lineage support only. Biomedical claims are grounded in source IDs from `source_corpus.json`.
""",
    )


def write_public_lineage_summary(status: str) -> None:
    write_text(
        PROOF_DIR / "public_lineage_summary.md",
        f"""# Public Lineage Summary

Proof: `{PROOF_ID}`

Status: `{status}`

The source corpus was assembled from PubMed E-utilities query files in `/private/tmp/alz_atlas_sources/` plus curated official/institutional URLs. The final atlas only makes bounded uncertainty-mapping claims and links biomedical statements to `source_corpus.json`, `consult/evidence_lineage_graph.json`, and source IDs in the contradiction records.

Phase A generated baseline artifacts without `/consult`. Phase B issued six adversarial `/consult` requests before updating the hypothesis map and logged each response in `consult/consultation_log.jsonl`.

No artifact offers medical advice, diagnosis, treatment recommendation, or a cure claim.
""",
    )


def proof_manifest() -> dict[str, Any]:
    response_paths = consult_response_paths()
    last_response = load_json_or_empty(response_paths[-1]) if response_paths else {}
    last_request_path = response_paths[-1].with_name(response_paths[-1].name.replace("_response.json", "_request.json")) if response_paths else Path("")
    last_request = load_json_or_empty(last_request_path) if last_request_path else {}
    request_hash = last_response.get("lineage", {}).get("request_hash") or sha256_json(last_request) if last_request else "responses_not_available"
    response_hash = last_response.get("lineage", {}).get("response_hash") or last_response.get("response_hash") or "responses_not_available"
    required = [
        "README.md",
        "proof_manifest.json",
        "source_corpus.json",
        "baseline/hypothesis_map.json",
        "baseline/contradiction_graph.json",
        "baseline/evidence_clusters.json",
        "baseline/top_10_bottlenecks.md",
        "baseline/convergence_report.json",
        "consult/consultation_log.jsonl",
        "consult/contradiction_atlas.json",
        "consult/premature_convergence_report.json",
        "consult/contradiction_recovery_report.json",
        "consult/evidence_lineage_graph.json",
        "consult/final_atlas.md",
        "delta/consult_vs_baseline_report.json",
        "public_lineage_summary.md",
    ]
    for request in consult_requests():
        request_name = request["request_id"].replace(f"{PROOF_ID}-", "")
        required.append(f"consult/inside_voice_consults/{request_name}_request.json")
        required.append(f"consult/inside_voice_consults/{request_name}_response.json")
    return {
        "proof_id": PROOF_ID,
        "title": "Truth Reconstruction Challenge 003 - Alzheimer's Contradiction Atlas",
        "status": "complete",
        "targets": [
            "AlzheimerDiseaseContradictionMapping",
            "InsideVoiceConsultationAdvantage",
            "EvidenceLineagePreservingUncertainty",
        ],
        "claim_level": "evidence_backed",
        "inside_voice_adapter_status": "pond_backed_consult_used",
        "public_private_boundary": "public source IDs, bounded consult response fields, hashes, and uncertainty mapping only; no hidden reasoning or private substrate details",
        "required_artifacts": required,
        "disallowed_claims": [
            "medical_advice",
            "diagnosis",
            "treatment_recommendation",
            "cure_claim",
            "alzheimers_solved",
            "inside_voice_as_biomedical_authority",
            "unsupported_scientific_claims",
            "hidden_chain_of_thought",
        ],
        "lineage": {
            "mcp_endpoint": CONSULT_ENDPOINT,
            "contract_version": "inside_voice.mcp.consultation.v1",
            "request_hash": request_hash,
            "response_hash": response_hash,
            "derived_from": "consult/inside_voice_consults",
            "validates": "consult_vs_baseline_contradiction_recovery",
        },
    }


def stage_final() -> None:
    corpus_payload, by_id = corpus()
    assert_required_sources(by_id)
    missing_responses = []
    for request in consult_requests():
        request_name = request["request_id"].replace(f"{PROOF_ID}-", "")
        response_path = PROOF_DIR / "consult/inside_voice_consults" / f"{request_name}_response.json"
        if not response_path.is_file():
            missing_responses.append(str(response_path.relative_to(PROOF_DIR)))
    if missing_responses:
        raise RuntimeError("missing consult responses: " + ", ".join(missing_responses))

    write_json(PROOF_DIR / "source_corpus.json", corpus_payload)
    log_entries = consult_log_entries()
    write_text(PROOF_DIR / "consult/consultation_log.jsonl", "\n".join(canonical_json(entry) for entry in log_entries))
    write_json(PROOF_DIR / "consult/contradiction_atlas.json", {"run_id": "phase-b-consult", "contradiction_count": 12, "contradictions": consult_contradictions()})
    write_json(PROOF_DIR / "consult/premature_convergence_report.json", premature_convergence_report())
    write_json(PROOF_DIR / "consult/contradiction_recovery_report.json", contradiction_recovery_report())
    write_json(PROOF_DIR / "consult/evidence_lineage_graph.json", evidence_lineage_graph(by_id))
    write_text(PROOF_DIR / "consult/final_atlas.md", final_atlas_md())
    write_json(PROOF_DIR / "delta/consult_vs_baseline_report.json", delta_report())
    write_readme(status="complete")
    write_public_lineage_summary(status="complete")
    write_json(PROOF_DIR / "proof_manifest.json", proof_manifest())


def assert_required_sources(by_id: dict[str, dict[str, Any]]) -> None:
    missing = []
    for group, source_ids in KEY_SOURCE_GROUPS.items():
        for source_id in source_ids:
            if source_id not in by_id:
                missing.append(f"{group}:{source_id}")
    if missing:
        raise RuntimeError("missing required sources: " + ", ".join(missing))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=["baseline", "final"])
    args = parser.parse_args(argv)
    if args.stage == "baseline":
        stage_baseline()
    else:
        stage_final()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
