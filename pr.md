## Summary

### Demo mode
- Add `DEMO_MODE` environment variable
- Add demo banner when demo mode is enabled
- Add `populate_demo_data` management command
- Add demo data regeneration button in `/functions`

### Configuration
- Fix `DEBUG` loading from environment variables
- Add `.env.example`

### Repository cleanup
- Remove tracked secrets (`vars.env`)
- Remove tracked `__pycache__` files
- Update `.gitignore` with standard Python/Django entries

### Code quality
- Remove duplicate URL pattern
- Remove stray `print()`
- Remove hardcoded password from comment

## Test Plan

- [ ] Verify `DEMO_MODE=True` displays the demo banner
- [ ] Verify the "Regenerate Demo Data" button is only visible when:
  - `DEMO_MODE=True`
  - User is a superuser
- [ ] Verify `vars.env` is no longer tracked after merge
- [ ] Verify application starts correctly with `.env.example`
