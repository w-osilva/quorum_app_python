# Questions

After completing your implementation, you should include a write up that answers the following questions:

1. Discuss your strategy and decisions implementing the application. Please, consider time complexity, effort cost, technologies used and any other variable that you understand important on your development process.
2. How would you change your solution to account for future columns that might be requested, such as “Bill Voted On Date” or “Co-Sponsors”?
3. How would you change your solution if instead of receiving CSVs of data, you were given a list of legislators or bills that you should generate a CSV for?
4. How long did you spend working on the assignment?

## Answers

### Question 1

For this version of the challenge, I've chosen rewriting the a [**Ruby** application](https://github.com/w-osilva/quorum-app) which I wrote last year in **Python** using **Flask** and **SQLAlchemy**. My main goals were:
- **Simplicity**: Flask provides a clean, lightweight framework that's easy to understand and maintain
- **Modern Stack**: SQLAlchemy 2.0 with Pydantic for validation, pytest for testing
- **Developer Experience**: Clear project structure with separation of concerns (models, schemas, services, routes)
- **Performance**: Batch upserts for CSV importing to minimize database transactions
- **Flexibility**: Multi-format API responses (HTML, JSON, CSV) with content negotiation
- **Quality**: Comprehensive test suite and modern tooling (Ruff, djLint)

The architecture prioritizes maintainability and extensibility while keeping the codebase simple and well-tested.

### Question 2

To support future columns like “Bill Voted On Date” or “Co-Sponsors”, I would:
- For "Bill Voted On Date": Add a `created_at` or `voted_on` column to the `votes` table (already present in the current schema), and expose it in the API and templates.
- For "Co-Sponsors": Introduce a many-to-many relationship between `bills` and `legislators` via a `bill_sponsors` table, with a `sponsor_type` field to distinguish primary/co-sponsors. This is straightforward with SQLAlchemy's relationship features.

### Question 3

If the requirement changed to exporting CSVs instead of importing, I would leverage the existing multi-format API infrastructure. All endpoints already support CSV output via content negotiation, so this would mainly involve:
- Extending the current CSV response formatters
- Adding batch export utilities for large datasets
- Implementing query parameter filtering for custom export criteria

### Question 4

**Work journal:**

**Friday 2025-07-11**
- 1 hour: Project planning the migration strategy from Rails to Flask

**Saturday 2025-07-12**  
- 3 hours: Database models, Pydantic schemas, and CSV importers
- 2 hour: API routes and multi-format response logic

**Sunday 2025-07-13**
- 2 hours: Jinja2 templates, web interface, and documentation
- 2 hours: Testing, tooling setup (Ruff, djLint), and final polish

**Total time: ~10 hours** (including migration, new features, comprehensive testing, and documentation)