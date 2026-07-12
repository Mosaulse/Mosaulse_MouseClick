export const meta = {
  name: "python-dev",
  description: "Python development workflow for PyQt5 applications"
};

export default async function workflow(args, ctx) {
  const { phase, agent, parallel, log } = ctx;
  
  // Phase 1: Code Review
  await phase("code-review", async () => {
    log("Starting code review...");
    const reviewer = await agent("explore", {
      prompt: `Review the following Python code for:
        1. PEP 8 compliance
        2. Type hints usage
        3. Error handling
        4. Performance issues
        5. Security concerns
        
        Focus on PyQt5-specific patterns and MVP architecture.
        Provide specific file:line references for any issues found.`
    });
    return reviewer;
  });
  
  // Phase 2: Testing
  await phase("testing", async () => {
    log("Running tests...");
    const tester = await agent("general", {
      prompt: `Run pytest tests and analyze results:
        1. Run: python -m pytest Scripts/tests/ -v
        2. Check for test failures
        3. Analyze test coverage
        4. Identify untested code paths
        5. Suggest additional tests if needed`
    });
    return tester;
  });
  
  // Phase 3: Documentation
  await phase("documentation", async () => {
    log("Updating documentation...");
    const docWriter = await agent("general", {
      prompt: `Review and update project documentation:
        1. Check README.md for accuracy
        2. Update AGENTS.md if needed
        3. Verify docstrings in public APIs
        4. Check for outdated information`
    });
    return docWriter;
  });
  
  // Phase 4: Packaging
  await phase("packaging", async () => {
    log("Testing packaging...");
    const packager = await agent("general", {
      prompt: `Test PyInstaller packaging:
        1. Run: pyinstaller MouseClicker.spec
        2. Verify EXE creation
        3. Test basic functionality
        4. Check for missing dependencies
        5. Verify icon and resources`
    });
    return packager;
  });
  
  return {
    summary: "Python development workflow completed",
    phases: ["code-review", "testing", "documentation", "packaging"]
  };
}