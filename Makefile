.RECIPEPREFIX = >
.PHONY: all libcbor boost

CONAN_LOGIN_COMMAND=conan remote add video http://10.199.28.20:80/ && conan user --remote video -p 52WnSCzO1BoI video-rw
CONAN_UPLOAD_COMMAND=conan upload --confirm --remote video --all '*@satorivideo/*' && echo 'SUCCESS'

all: libcbor boost

libcbor:
> docker build -t $@ $@
>- docker run --rm $@ bash -ceux "${CONAN_LOGIN_COMMAND} && ${CONAN_UPLOAD_COMMAND}"
> echo "DONE"

boost:
> docker build -t $@ $@
>- docker run --rm $@ bash -ceux "${CONAN_LOGIN_COMMAND} && ${CONAN_UPLOAD_COMMAND}"
> echo "DONE"


