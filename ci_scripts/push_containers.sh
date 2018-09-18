export IMAGE_TAG=$(cat VERSION)
export AARCH=`uname -m`

docker build -t cachengo/sso_example-$AARCH:$IMAGE_TAG .
docker push cachengo/sso_example-$AARCH:$IMAGE_TAG