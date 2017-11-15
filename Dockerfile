FROM gcr.io/kubernetes-live/video/cpp-builder

COPY . /src
WORKDIR /src

ARG LIB
ARG CONAN_LOGIN_COMMAND
ARG CONAN_CREATE_COMMAND

RUN bash -cx "${CONAN_LOGIN_COMMAND}"
RUN cd ${LIB} && bash -cx "${CONAN_CREATE_COMMAND}"
