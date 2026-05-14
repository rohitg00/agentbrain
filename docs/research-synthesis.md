# Research Synthesis

This document summarizes patterns learned from current public discussion and open-source agent workflow repositories without copying names, branding, or runtime-specific assumptions into the product surface.

## Signals from the last 30 days

- People respond strongly to agent memory that compounds over time.
- “Skills as prompts” is a clearer mental model than giant system prompts.
- Users want opinionated workflows, not just tools.
- Product and planning review before coding is a major unmet need.
- Multi-role agent workflows are attractive, but they need observability and safety.
- The strongest criticism is that these systems can become giant brittle prompt piles unless they have evaluation, consolidation, and maintenance.

## Patterns worth adopting

- Markdown as the portable source of truth
- Skills with explicit triggers and verification
- Question-first product development
- Multi-pass review from different roles
- Skill creation from repeated failure
- Searchable long-term memory with selective always-on memory
- Review gates before shipping
- QA evidence, not “looks good” claims

## Patterns to avoid

- Vendor-specific naming
- Copying command names from another ecosystem
- Huge skills that are expensive to load
- Hidden writes to memory without user understanding
- A single “do everything” command with no artifacts
- Comparing against other tools in public docs

## Product direction

Agent Brain should become the neutral brain layer: not a competitor comparison, not a prompt pack clone, but a disciplined operating system for agents that helps users create better products.
