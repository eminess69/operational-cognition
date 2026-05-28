# Blind Pack Design

The blind pack separates visible inputs from hidden expected reconstruction keys. `blind_inputs.json` contains case metadata, submitted reconstruction keys, and expected-key digests. It does not contain expected outcomes. `blind_expected_hidden.json` contains expected keys and is used only by `blind_scorer.py`.

The scorer reads key lists only. It does not parse comparative reports, scenario prose, final verdicts, or claim register text.

