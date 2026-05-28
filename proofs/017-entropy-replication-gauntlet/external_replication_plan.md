# External Replication Plan

Another evaluator can rerun this gauntlet with only public-safe fixtures, validator scripts, the blind pack, and deterministic hashes.

1. Copy `proofs/017-entropy-replication-gauntlet/` and `tools/validate_entropy_replication_gauntlet.py`.
2. Run `python3 blind_pack/blind_scorer.py` from the proof directory or through the validator.
3. Run `python3 tools/validate_entropy_replication_gauntlet.py proofs/017-entropy-replication-gauntlet`.
4. Compare scenario hashes in each `environment_refs.json` and `replay_integrity_results.json`.
5. Review only public-safe scenario files, scorer outputs, deterministic hashes, and consult response metadata.

The replication path does not require private substrate internals, hidden reasoning, private traces, or non-public runtime state. Inside Voice evidence is represented by response metadata, pressure rankings, retrieved refs, and runtime hashes.

