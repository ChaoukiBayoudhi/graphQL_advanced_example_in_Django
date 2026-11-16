# Graph QL advanced example in Django

A Django project with 4 models and a GraphQL API (Graphene-Django).

## Tech stack

- Python 3
- Django
- Graphene-Django (GraphQL)
- Graphene
- psycopg2 (PostgreSQL)
- Database: SQLite

## Project structure

- `graphQL_example/`: project settings and root URLs
- `publications/`: Django app
- `reviewers/`: Django app
- Tests: `publications/tests.py`, `reviewers/tests.py`

## Data model

| Model | App | Fields |
|---|---|---|
| `Publication` | `publications` | title, abstract, authors, published_date, reviewers |
| `ReviewAssignment` | `publications` | publication, reviewer, assigned_at, status |
| `Reviewer` | `reviewers` | name, email, expertise |
| `Review` | `reviewers` | assignment, comments, score, created_at |

## URL routes

Declared in `urls.py`:

- `/blog/`
- `/graphql/`

## How to run

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Then open `http://127.0.0.1:8000/`.

---

Author: [Chaouki Bayoudhi](https://github.com/ChaoukiBayoudhi)
