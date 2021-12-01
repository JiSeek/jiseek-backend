docker run -ti -p 8000:8000 -e AWS_PROFILE=zappa -v "$(pwd):/var/task" -v ~/.aws/:/root/.aws  --rm zappa-docker-image

