# API Reference

## Code Management

- `POST /api/v1/code/upload` - Upload code
- `GET /api/v1/code` - List code files
- `GET /api/v1/code/{id}` - Get code details
- `DELETE /api/v1/code/{id}` - Delete code

## Analysis

- `POST /api/v1/analysis/parse` - Parse code
- `POST /api/v1/analysis/complexity` - Analyze complexity
- `POST /api/v1/analysis/bugs` - Detect bugs
- `POST /api/v1/analysis/security` - Security analysis
- `GET /api/v1/analysis/{id}` - Get analysis

## Documentation

- `POST /api/v1/docs/generate` - Generate docs
- `GET /api/v1/docs/{id}` - Get docs
- `POST /api/v1/docs/export` - Export docs

## Q&A

- `POST /api/v1/qa` - Ask question
- `GET /api/v1/qa/history` - Get history
- `POST /api/v1/qa/batch` - Batch questions

## Review

- `POST /api/v1/review` - Code review
- `GET /api/v1/review/{id}` - Get review
- `POST /api/v1/refactor` - Get refactoring suggestions
