
echo 'Running flake8...'
poetry run flake8

echo 'Running isort...'
poetry run isort . --check-only

echo 'Running black...'
poetry run black --line-length=79 . --check

echo 'Completed checks'