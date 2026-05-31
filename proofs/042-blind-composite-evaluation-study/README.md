# Proof 042 - Blind Composite Evaluation Study

Proof 042 tests whether composite candidates remain useful after removing the internal Proof 041 scoring formula from final pathway selection.

## Result

`STRONG_SIGNAL`

## Findings

1. Did composite advantage disappear without internal scoring?
   - No. Mode C blind valid rate was 0.7667.
2. Did randomized candidate order break the result?
   - No. Mode B valid rate was 0.7667; Mode B/Mode C exact agreement was 0.9667.
3. Did current deterministic scoring still matter?
   - Mode A valid rate was 0.8667. Mode A preserves the Proof 041 scored-window baseline, not a blind final-winner selection. The hostile audit marks internal scoring as dominant: false.
4. Did pathway inflation remain a concern?
   - Yes in bounded form. The full candidate set averaged 24.4667 candidates per case, with false-composite candidate rate 0.3311.
5. What exact bounded claim survives?
   - Score-free composite candidates remained useful under blind evaluation, but the result is still bounded by deterministic cue evaluation and candidate-generation effects.

## Metrics

- Mode A valid rate: 0.8667
- Mode B valid rate: 0.7667
- Mode C valid rate: 0.7667
- Mode A/Mode B agreement: 0.5333
- Mode A/Mode C agreement: 0.5
- Mode B/Mode C agreement: 0.9667
