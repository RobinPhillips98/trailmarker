echo 'Running flake8...'
poetry run flake8

echo 'Running isort...'
poetry run isort . --check-only

echo 'Running black...'
poetry run black --line-length=79 . --check

echo 'Running unit tests...'
poetry run pytest -x

cd ../frontend

echo 'Running prettier...'
npm run format:check

echo 'Running ESLint...'
npm run lint

echo 'Completed checks'
