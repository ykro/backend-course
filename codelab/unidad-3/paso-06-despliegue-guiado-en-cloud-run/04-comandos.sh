docker build -t estatehub .
docker run --rm -p 8080:8080 --env-file .env estatehub
