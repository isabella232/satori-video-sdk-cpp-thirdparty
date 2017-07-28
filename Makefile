LIBS=gsl rapidjson libcbor boost beast opencv openssl darknet

.RECIPEPREFIX = >
.PHONY: all video-thirdparty ${LIBS}

CONAN_LOGIN_COMMAND=conan remote add video http://10.199.28.20:80/ && conan user --remote video -p ${CONAN_PASSWORD} ${CONAN_USER}
CONAN_UPLOAD_COMMAND=conan upload --confirm --remote video --all '*@satorivideo/*' && echo 'SUCCESS'

COMMON_CONAN_OPTIONS=create satorivideo/master --build=missing -s compiler.libcxx=libstdc++11
CONAN_OPTIONS_libcbor=${COMMON_CONAN_OPTIONS} --options fPIC=True --options shared=False
CONAN_OPTIONS_boost=${COMMON_CONAN_OPTIONS} --options fPIC=True --options shared=False
CONAN_OPTIONS_opencv=${COMMON_CONAN_OPTIONS} --options fPIC=True --options shared=False
CONAN_OPTIONS_openssl=${COMMON_CONAN_OPTIONS} --options fPIC=True --options shared=False
CONAN_OPTIONS_gsl=${COMMON_CONAN_OPTIONS}
CONAN_OPTIONS_rapidjson=${COMMON_CONAN_OPTIONS}
CONAN_OPTIONS_beast=${COMMON_CONAN_OPTIONS}
CONAN_OPTIONS_darknet=${COMMON_CONAN_OPTIONS}

all: video-thirdparty ${LIBS}

# Builds and uploads the package
${LIBS}: CONAN_CREATE_COMMAND=conan ${CONAN_OPTIONS_$@}
${LIBS}: 
>- docker run --rm video-thirdparty bash -ceux "${CONAN_LOGIN_COMMAND} && cd $@ && ${CONAN_CREATE_COMMAND} -s build_type=Release && ${CONAN_UPLOAD_COMMAND}"
> echo "DONE"

video-thirdparty:
> docker build -t $@ .
