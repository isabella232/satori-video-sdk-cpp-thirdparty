LIBS=gsl rapidjson libcbor boost beast opencv openssl darknet libvpx ffmpeg zlib sdl bzip2 loguru tensorflow-serving

DOCKER_BUILDER_IMAGE=gcr.io/kubernetes-live/video/video-thirdparty

.RECIPEPREFIX = >
.PHONY: all video-thirdparty push ${LIBS}

CONAN_LOGIN_COMMAND=conan remote add video http://10.199.28.20:80/ && conan user --remote video -p ${CONAN_PASSWORD} ${CONAN_USER}
CONAN_UPLOAD_COMMAND=conan upload --confirm --remote video --all '*@satorivideo/*' && echo 'SUCCESS'

COMMON_CONAN_OPTIONS=create satorivideo/master --build=missing -s compiler.libcxx=libstdc++11
CONAN_OPTIONS_libcbor=${COMMON_CONAN_OPTIONS} --options Libcbor:fPIC=True --options Libcbor:shared=False
CONAN_OPTIONS_boost=${COMMON_CONAN_OPTIONS} --options Boost:fPIC=True --options Boost:shared=False
CONAN_OPTIONS_opencv=${COMMON_CONAN_OPTIONS} --options Opencv:fPIC=True --options Opencv:shared=False
CONAN_OPTIONS_openssl=${COMMON_CONAN_OPTIONS} --options Openssl:fPIC=True --options Openssl:shared=False
CONAN_OPTIONS_libvpx=${COMMON_CONAN_OPTIONS} --options Libvpx:fPIC=True --options Libvpx:shared=False
CONAN_OPTIONS_ffmpeg=${COMMON_CONAN_OPTIONS} --options Ffmpeg:fPIC=True --options Ffmpeg:shared=False
CONAN_OPTIONS_sdl=${COMMON_CONAN_OPTIONS} --options Sdl:fPIC=True --options Sdl:shared=False
CONAN_OPTIONS_gsl=${COMMON_CONAN_OPTIONS}
CONAN_OPTIONS_rapidjson=${COMMON_CONAN_OPTIONS}
CONAN_OPTIONS_beast=${COMMON_CONAN_OPTIONS}
CONAN_OPTIONS_darknet=${COMMON_CONAN_OPTIONS}
CONAN_OPTIONS_zlib=${COMMON_CONAN_OPTIONS}
CONAN_OPTIONS_bzip2=${COMMON_CONAN_OPTIONS}
CONAN_OPTIONS_loguru=${COMMON_CONAN_OPTIONS}
CONAN_OPTIONS_tensorflow-serving=${COMMON_CONAN_OPTIONS}

all: ${LIBS}

# Builds and uploads the package
${LIBS}: CONAN_CREATE_COMMAND=conan ${CONAN_OPTIONS_$@}
${LIBS}:
> docker run --pull --rm ${DOCKER_BUILDER_IMAGE} -ceux "${CONAN_LOGIN_COMMAND} && cd $@ && ${CONAN_CREATE_COMMAND} -s build_type=Release && ${CONAN_UPLOAD_COMMAND}"
> docker run --pull --rm ${DOCKER_BUILDER_IMAGE} bash -ceux "${CONAN_LOGIN_COMMAND} && cd $@ && ${CONAN_CREATE_COMMAND} -s build_type=Debug && ${CONAN_UPLOAD_COMMAND}"
> echo "DONE"

video-thirdparty:
> docker build --pull -t ${DOCKER_BUILDER_IMAGE} .

push:
> docker push ${DOCKER_BUILDER_IMAGE}
