# JAX/jaxfne and Release-Control Doctrine

**Source:** hnyxj oracle (canonical workspace knowledge)  
**Date:** 2026-05-29  
**Status:** Live doctrine for all jaxfne and release work

---

## JAX Numerics Doctrine — Speed + Correctness

### [INVARIANT] Enable x64 before constructing arrays.

float64 is only honored when `jax_enable_x64` is set, **and only if set before arrays are created**. Use `jaxfne.enable_x64()` at the top of a session/script. `_dtype_from_policy` silently falls back to float32 otherwise—a run can *appear* float64 and not be.

**Always** read back `runtime_report()["actual_dtype"]`, never trust the requested dtype.

### [DEFAULT] Stay on JAX-native paths the kernels already use.

| Operation | JAX path | Avoid | Reason |
|-----------|----------|-------|--------|
| Time evolution | `jax.lax.scan` | Python for loops over timesteps | Enables grad through time; preserves tracing |
| Edge aggregation | `jax.ops.segment_sum` | Densify edge list to N×N matmul | Preserves sparsity and double-count guard |
| Seed/replicate batching | `jax.vmap` over PRNG keys | Python-loop replication | Throughput; JIT friendly |
| Compilation | `jit=True` in RuntimeConfig | One-shot jit on trivial calls | Reuse: amortize trace cost |

### [INVARIANT] Explicit PRNG only.

Every stochastic path takes an explicit `jax.random.PRNGKey` and uses `split`/`fold_in`. No global RNG; no `numpy.random` for anything reproducible.

### [DEFAULT] Performance debugging: cheapest first.

1. Confirm `jit`/`vmap` actually on via `runtime_report()`
2. Check `recurrent_backend` — sparse wins over dense for large W
3. Reduce `n_steps` before profiling kernels
4. Keep shapes/dtypes stable across calls to avoid recompilation

### [DEFAULT] Finiteness is a gate, not a nicety.

Reuse `_finite_or_none`, `_finite_bool`, `validate_*` helpers. JSON uses `allow_nan=False`; catch NaN/inf early.

---

## jaxfne Core Invariants

### [INVARIANT] Truth gates never escalate upward.

Conservative defaults (foundational floors):
```python
physical_amplitude_claim_allowed = False
claim_level = "computational_scaffold"
field_solver_status = "laminar_proxy_no_pde"
```

Code may *read* these gates; code must never flip them upward.

### [INVARIANT] Proxy ≠ PDE.

fields.py computes a laminar proxy readout: Gaussian contact kernel + finite-difference CSD. This is **not** a resistive field solve.

**What does not exist yet:**
- The real operator: `div(-σ ∇φ_e) = q` (Poisson)
- Solver status: no iterative method, no convergence residual, no boundary-condition enforcement

**Naming and reporting:**
- Any output from fields.py must carry the `*_proxy` suffix
- Status marker: `field_solver_status = "laminar_proxy_no_pde"`
- Never synthesize `J_e`. Return the existing `"not_computed_without_real_field_solver"` marker

### [INVARIANT] Receipts are write-once.

`save_receipt()` refuses to overwrite without `overwrite=True` and raises `receipt_file_exists`. Do not hand-edit receipts, manifests, or any committed truth artifact. Regenerate them from a run.

### [DEFAULT] Vocabulary discipline in code and reports.

**Forbidden without evidence:**
- "proved", "confirmed", "validated", "physical", "calibrated", "biological truth", "mechanism"

**Preferred terms:**
- "proxy", "scaffold", "declared", "uncalibrated", "native", "computational diagnostic"

Never upgrade jaxfne outputs to physical or mechanism claims; cite the truth gates and claim boundary in your report.

---

## Release-Control Doctrine

### Release Target Identity

For every release, define exactly one `intended_release_sha`.

**Before tag repair, GitHub Release edits, TestPyPI upload, or PyPI upload, verify:**

```text
origin/main == intended_release_sha
CI run headSha == intended_release_sha
CI conclusion == success
working tree clean
```

**[INVARIANT] For annotated tags, always report both:**

```bash
git ls-remote origin refs/tags/vX.Y.Z          # tag object SHA
git ls-remote origin "refs/tags/vX.Y.Z^{}"      # peeled tag commit SHA
```

Use the **peeled tag commit SHA** as the release commit target, never the tag object SHA.

**[DEFAULT] If `origin/main` differs from CI `headSha`, stop and report SHA reconciliation options. Do not repair tags or upload artifacts.**

### Release Freeze Mode

**[INVARIANT] When release CI is running or has passed for a candidate SHA, agents enter release freeze mode.**

**During release freeze, do not push unrelated commits to `main`.**

**Allowed:**
- Read-only diagnostics (`git status`, `gh run view`, `git ls-remote`)
- CI status checks
- Tag repair after explicit authorization
- TestPyPI/PyPI publication after explicit authorization

**Deferred (until release complete or cancelled):**
- Root cleanup commits
- Docs cleanup commits
- Receipt relocation
- Formatting-only commits
- Branch hygiene

**[DEFAULT] If a commit is pushed to `main` during release freeze, that commit becomes the new candidate only after release CI passes on that exact SHA.**

### Remote Mutation Protocol

**Before any remote mutation, report:**

```text
mutation type
target ref (main | tags/vX.Y.Z | GitHub Release)
current ref SHA
intended new SHA
reason
commands to run
rollback path
```

**Remote mutation examples (each is a separate gate):**
- Pushing to `main`
- Deleting or recreating tags
- Creating or editing GitHub Releases
- Uploading to TestPyPI
- Uploading to PyPI

**[INVARIANT] Do not combine multiple mutation classes in one step.** Tag repair, TestPyPI upload, PyPI upload, and GitHub Release asset edits are separate authorization gates.

### CI Monitoring Discipline

**For long CI jobs, emit one receipt only when the run reaches a terminal state:**

```text
success
failure
cancelled
timed_out
```

**The receipt must include:**

```text
run URL
status + conclusion
headSha
job matrix results
origin/main SHA
working tree status
confirmation of no unauthorized mutations
next safe action
```

**[DEFAULT] Avoid repeated progress-only updates** ("still running", "standing by", "monitoring continues"). Receipt on terminal state only.

### Mutation Intent Gate

**[INVARIANT] Require explicit authorization before destructive or publication mutations.**

| Class                | Examples                           | Authorization                   |
| -------------------- | ---------------------------------- | ------------------------------- |
| Read-only            | status, ls-remote, gh run view     | Allowed                         |
| Local-only           | build, test, inspect               | Allowed unless risky            |
| Remote branch        | git push origin main               | Explicit task scope required    |
| Tag mutation         | delete/recreate/push tag           | Explicit authorization required |
| Distribution         | TestPyPI/PyPI upload               | Explicit authorization required |
| GitHub Release       | create/edit/release assets         | Explicit authorization required |

### Root Hygiene Preflight

**[DEFAULT] Fix root clutter before release freeze, not during it.**

**Policy:**
- Root cleanup must happen before release candidate CI.
- During release freeze, root cleanup is deferred unless user explicitly changes the release target.
- Add `.gitignore` and repo-layout rules before release branch is merged.

**Checks:**
```bash
git ls-files . | wc -l      # confirm only tracked files
find . -maxdepth 1 -type f  # confirm no untracked root clutter
git status --short          # confirm clean
```

---

## Related Skills & Rules

See hnyxj oracle for durable skills and rules:
- **skills:** release-target-reconciler, release-freeze-guard, tag-object-vs-peeled-tag-auditor, noiseless-monitor, mutation-intent-gate, root-hygiene-preflight, tsx-to-html-dashboard-builder
- **rules:** jax_computational_biophysics_style.md, tfne_claim_and_source_field_discipline.md, mathematical_glossary_flow.md, manuscript_structure_and_equation_style.md

