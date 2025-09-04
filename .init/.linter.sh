#!/bin/bash
cd /home/kavia/workspace/code-generation/event-planning-suite-130267-130276/event_planning_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

