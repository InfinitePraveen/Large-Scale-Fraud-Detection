# Contributing

Thanks for helping improve this project.

## Good Contributions

- Improve notebook explanations or visualisations.
- Add a lightweight fraud feature.
- Improve the streaming simulation.
- Add tests or validation without introducing a large framework.
- Improve Flask accessibility and usability.
- Document Kafka or feature-store design decisions.

## Guidelines

1. Keep the repository simple and notebook-first.
2. Do not add a `src/` directory.
3. Avoid separate preprocessing/module scripts unless there is a strong reason.
4. Prefer CPU-friendly solutions.
5. Keep sample data and generated artifacts small.
6. Explain non-obvious changes in the pull request.
7. Update `CHANGELOG.md` for user-visible changes.

## Local Development

Create a virtual environment, install `requirements.txt`, run the notebooks,
and verify that `python app.py` starts successfully before submitting changes.
