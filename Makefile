LIBS=libcbor boost opencv openssl gsl beast rapidjson

.RECIPEPREFIX = >
.PHONY: all ${LIBS}

CONAN_LOGIN_COMMAND=conan remote add video http://10.199.28.20:80/ && conan user --remote video -p ${CONAN_PASSWORD} ${CONAN_USER}
CONAN_UPLOAD_COMMAND=conan upload --confirm --remote video --all '*@satorivideo/*' && echo 'SUCCESS'
COMMON_CONAN_OPTIONS=--build=missing -s compiler.libcxx=libstdc++11

CONAN_OPTIONS_libcbor=${COMMON_CONAN_OPTIONS} --options fPIC=True --options shared=False
CONAN_OPTIONS_boost=${COMMON_CONAN_OPTIONS} --options fPIC=True --options shared=False
CONAN_OPTIONS_opencv=${COMMON_CONAN_OPTIONS} --options fPIC=True --options shared=False
CONAN_OPTIONS_openssl=${COMMON_CONAN_OPTIONS} --options fPIC=True --options shared=False
CONAN_OPTIONS_gsl=${COMMON_CONAN_OPTIONS}
CONAN_OPTIONS_rapidjson=${COMMON_CONAN_OPTIONS}
CONAN_OPTIONS_beast=${COMMON_CONAN_OPTIONS}

all: ${LIBS}

${LIBS}:
> docker build --build-arg LIB=$@ --build-arg CONAN_OPTIONS="-s build_type=Debug ${CONAN_OPTIONS_$@}" -t $@ .
>- docker run --rm $@ bash -ceux "${CONAN_LOGIN_COMMAND} && ${CONAN_UPLOAD_COMMAND}"
> docker build --build-arg LIB=$@ --build-arg CONAN_OPTIONS="-s build_type=Release ${CONAN_OPTIONS_$@}" -t $@ .
>- docker run --rm $@ bash -ceux "${CONAN_LOGIN_COMMAND} && ${CONAN_UPLOAD_COMMAND}"
> echo "DONE"
