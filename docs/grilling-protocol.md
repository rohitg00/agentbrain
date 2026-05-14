# Grilling Protocol

Grilling is not negativity. It is pressure-testing before wasteful execution.

## Grill targets

- Vague user
- Vague problem
- Vague audience
- Vague success metric
- Solution-first thinking
- Too many features
- No wedge
- No proof artifact
- No distribution path
- No maintenance plan
- No failure criteria

## The seven grills

### 1. Problem grill

Ask: Is this a real pain or just a cool capability?

Reject if:
- The user cannot name who suffers.
- The pain is not frequent, expensive, or emotionally strong.
- The current workaround is acceptable.

### 2. Audience grill

Ask: Who exactly is this for first?

Reject if:
- The answer is “everyone.”
- The audience has conflicting needs.
- The buyer and user are confused.

### 3. Wedge grill

Ask: What is the smallest sharp entrypoint?

Reject if:
- v0 requires a platform, marketplace, or ecosystem.
- There is no single workflow that can win alone.

### 4. Design grill

Ask: Will the user understand what to do without being trained?

Reject if:
- The first screen has no obvious action.
- The system requires users to think like builders.
- Error states are not designed.

### 5. Engineering grill

Ask: Can this be built safely and verified in small steps?

Reject if:
- The plan lacks data flow.
- The plan lacks tests.
- Critical operations have no rollback.

### 6. Trust grill

Ask: What would make users stop trusting this?

Reject if:
- It touches secrets without a clear boundary.
- It automates destructive actions without confirmation.
- It stores personal data without retention rules.

### 7. Learning grill

Ask: What will we learn from v0?

Reject if:
- There is no measurable signal.
- Success depends on subjective excitement only.
- The team cannot decide after the experiment.

## Output format

```markdown
## Grill Findings

### Strong
- ...

### Weak
- ...

### Must answer before build
1. ...

### Assumptions I will use if unanswered
- ...

### Recommended v0
- ...
```
