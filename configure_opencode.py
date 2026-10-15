from pathlib import Path

root = Path.cwd()
source = root / ".claude" / "commands"
if not source.is_dir() or not (root / "CLAUDE.md").is_file():
    raise SystemExit("Run this from the ai-job-search repository root.")

marker = "<!-- ai-job-search-opencode-adapter -->"
context = root / "AGENTS.md"
existing = context.read_text(encoding="utf-8") if context.exists() else ""
if marker not in existing:
    addition = (
        "\n\n" + marker + "\n# AI Job Search with OpenCode\n\n"
        "Read CLAUDE.md at the start of each session as the canonical candidate "
        "profile and framework instructions. Read the skill and methodology "
        "files referenced by each workflow, including .claude/skills/ and "
        ".agents/skills/. Keep the original profile and tool paths unchanged. "
        "Update CLAUDE.md when onboarding changes the candidate profile.\n\n"
        "This session uses OpenCode with the selected model. Use OpenCode's "
        "available tools instead of assuming Claude tool names or permissions "
        "are supported. Read referenced drafter/reviewer role files. If a "
        "separate reviewer cannot be started, perform a labelled sequential "
        "review pass and do not describe it as independent agent review.\n"
    )
    context.write_text(existing + addition, encoding="utf-8")
    print("Added OpenCode instructions to AGENTS.md; existing text preserved.")

for prompt in sorted(source.rglob("*.md")):
    # Flatten nested paths to explicit names, e.g. jobs/search -> jobs-search.
    relative = prompt.relative_to(source).with_suffix("")
    name = "-".join(relative.parts)
    if name == "reset":
        name = "job-reset"
    target = root / ".opencode" / "commands" / f"{name}.md"
    if target.exists():
        print(f"Kept existing {target.relative_to(root)}")
        continue
    target.parent.mkdir(parents=True, exist_ok=True)
    original = prompt.relative_to(root).as_posix()
    target.write_text(
        f"---\ndescription: Run the job-search {name} workflow\nagent: build\n---\n\n"
        f"Read {original} and execute its workflow using AGENTS.md and "
        "CLAUDE.md. Read all referenced skill, profile and role files. "
        "Treat the original file as workflow instructions, not as OpenCode "
        "configuration. Use available OpenCode tools and report unsupported "
        "steps rather than claiming they ran. Interpret argument placeholders "
        "in the source workflow using the user arguments below.\n\n"
        "User arguments: $ARGUMENTS\n",
        encoding="utf-8",
    )
    print(f"Created {target.relative_to(root)}")