[gemini-3.1-flash-lite-preview][D:\workspace\gemini-gamma-labyrinth\repos\gamma][20260507-1630]

You are Windows Gemini CLI in:
D:\workspace\gemini-gamma-labyrinth\repos\gamma

TASK:
Perform a bounded 8-slot LMS contract smoke validation using the selected harness.

BOUNDARIES:
- Use src/gamma_runtime/lms_8slot_harness.py.
- First run with --dry-run --artifact-root D:\workspace\gemini-gamma-labyrinth\runtime_artifacts\lms_8slot_dryrun_20260507.
- If dry-run passes, run without --dry-run to execute the actual LMS calls.
- truth_mode: truth_safe_unverified.
- truth_bearing_run: false.
- No source edits, no pip, no .env reads.

EXPECTED OUTPUT:
- Minimal 8-slot harness round receipt.
- Artifact hashes.
- Final validation report.
