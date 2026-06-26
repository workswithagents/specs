---
name: Agent-Friendly Task
description: Structured for AI agents — clear input, output, and success criteria
title: "[agent-friendly] "
labels: [agent-friendly]
body:
  - type: markdown
    attributes:
      value: |
        This issue is structured for AI agent execution. Read the YAML block below for exact instructions.
  - type: textarea
    id: agent-instructions
    attributes:
      label: Agent Instructions
      description: YAML block with goal, inputs, outputs, and success criteria
      placeholder: |
        ```yaml
        agent: Claude Code, Codex, Cursor, Copilot, Generic MCP
        goal: ...
        inputs: [...]
        outputs: [...]
        success_criteria: [...]
        ```
      value: |
        ```yaml
        agent: ""
        goal: ""
        inputs: []
        outputs: []
        success_criteria: []
        ```
    validations:
      required: true
  - type: textarea
    id: human-context
    attributes:
      label: Context
      description: Additional context for human reviewers
      placeholder: Why this is useful, related issues, gotchas
    validations:
      required: false
  - type: checkboxes
    id: submission
    attributes:
      label: Submission Checklist
      options:
        - label: I have read AGENTS.md for the contribution workflow
          required: true
        - label: My PR includes a metadata.yaml with agent_id
          required: true
        - label: My script has a README.md with usage instructions
          required: true
