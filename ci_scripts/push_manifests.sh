export IMAGE_TAG=$(cat VERSION)

docker manifest create --amend cachengo/sso_example:$IMAGE_TAG cachengo/sso_example-x86_64:$IMAGE_TAG cachengo/sso_example-aarch64:$IMAGE_TAG
docker manifest push cachengo/sso_example:$IMAGE_TAG