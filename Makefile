# Should be defined by environment
CONAN_SERVER?=
CONAN_SERVER2?=
CONAN_UPLOAD_OPTIONS?=--all
CONAN_UPLOAD_OPTIONS2?=--all

CONAN_PASSWORD?=
CONAN_USER?=
DOCKER_BUILD_OPTIONS?=

LIBS=gsl rapidjson libcbor boost beast opencv openssl darknet \
	 libvpx ffmpeg zlib sdl bzip2 loguru tensorflow protobuf \
	 prometheus-cpp gperftools json
DOCKER_BUILDER_IMAGE=gcr.io/kubernetes-live/video/video-thirdparty
BUILD_TYPE=RelWithDebInfo

.RECIPEPREFIX = >
.PHONY: all ${LIBS}

CONAN_LOGIN_COMMAND=conan remote remove video; conan remote add video ${CONAN_SERVER} && \
                    conan user --remote video -p ${CONAN_PASSWORD} ${CONAN_USER}
CONAN_LOGIN_COMMAND2=conan remote remove video; conan remote add video ${CONAN_SERVER2} && \
                    conan user --remote video -p ${CONAN_PASSWORD} ${CONAN_USER}

CONAN_UPLOAD_COMMAND=conan upload --confirm --force --remote video ${CONAN_UPLOAD_OPTIONS} '*@satorivideo/*'
CONAN_UPLOAD_COMMAND2=conan upload --confirm --force --remote video ${CONAN_UPLOAD_OPTIONS2} '*@satorivideo/*'

COMMON_CONAN_CREATE_OPTIONS=-s build_type=${BUILD_TYPE} --build=missing -s compiler.libcxx=libstdc++11
CONAN_CREATE_OPTIONS_libcbor=--options Libcbor:fPIC=True --options Libcbor:shared=False
CONAN_CREATE_OPTIONS_boost=--options Boost:fPIC=True --options Boost:shared=False
CONAN_CREATE_OPTIONS_opencv=--options Opencv:fPIC=True --options Opencv:shared=False
CONAN_CREATE_OPTIONS_openssl=--options Openssl:fPIC=True --options Openssl:shared=False
CONAN_CREATE_OPTIONS_libvpx=--options Libvpx:fPIC=True --options Libvpx:shared=False
CONAN_CREATE_OPTIONS_ffmpeg=--options Ffmpeg:fPIC=True --options Ffmpeg:shared=False
CONAN_CREATE_OPTIONS_sdl=--options Sdl:fPIC=True --options Sdl:shared=False
CONAN_CREATE_OPTIONS_protobuf=--options Protobuf:fPIC=True --options Protobuf:shared=False
CONAN_CREATE_OPTIONS_prometheus-cpp=--options PrometheusCpp:fPIC=True --options PrometheusCpp:shared=False
CONAN_CREATE_OPTIONS_gperftools=--options GPerfTools:shared=False --options GPerfTools:fPIC=True

all: ${LIBS}

# Builds and uploads the package
${LIBS}: DOCKER_BUILDER_IMAGE=gcr.io/kubernetes-live/video/video-thirdparty-$@
${LIBS}: CONAN_CREATE_COMMAND=conan create . satorivideo/master ${COMMON_CONAN_CREATE_OPTIONS} ${CONAN_CREATE_OPTIONS_$@}
${LIBS}:
> docker build ${DOCKER_BUILD_OPTIONS} \
	--build-arg LIB=$@ \
	--build-arg CONAN_LOGIN_COMMAND="${CONAN_LOGIN_COMMAND}" \
	--build-arg CONAN_CREATE_COMMAND="${CONAN_CREATE_COMMAND}" \
	-t ${DOCKER_BUILDER_IMAGE} .
> docker run --rm ${DOCKER_BUILDER_IMAGE} bash -ceux "${CONAN_LOGIN_COMMAND} && ${CONAN_UPLOAD_COMMAND}"
> docker run --rm ${DOCKER_BUILDER_IMAGE} bash -ceux "${CONAN_LOGIN_COMMAND2} && ${CONAN_UPLOAD_COMMAND2}"
> docker rmi ${DOCKER_BUILDER_IMAGE}
