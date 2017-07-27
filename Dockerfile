FROM gcr.io/kubernetes-live/video/cpp-builder

ARG LIB=""
ARG CONAN_OPTIONS=""

COPY . /src
WORKDIR /src

RUN cd $LIB && \
    echo "conan create satorivideo/master -k $CONAN_OPTIONS" && \
    conan create satorivideo/master -k $CONAN_OPTIONS
