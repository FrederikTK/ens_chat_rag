install:
    pip install -r requirements.txt

run:
    docker-compose up --build

test:
    pytest --cov=src tests/