FROM gcr.io/kubernetes-live/video/cpp-builder

ARG LIB=""
ARG CONAN_OPTIONS=""

COPY . /src
WORKDIR /src

RUN cd $LIB && conan create satorivideo/master -k $CONAN_OPTIONS
