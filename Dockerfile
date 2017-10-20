FROM gcr.io/kubernetes-live/video/cpp-builder

ARG BAZEL_VERSION="0.6.0"

# tensorflow build tools
# todo: extract separate Dockerfile
RUN apt-get update && \
    apt-get install -y pkg-config zip unzip wget python-numpy python-dev python-pip python-wheel curl locate autoconf && \
    updatedb
RUN cd /tmp \
    && wget https://github.com/bazelbuild/bazel/releases/download/${BAZEL_VERSION}/bazel-${BAZEL_VERSION}-installer-linux-x86_64.sh \
    && chmod +x bazel-${BAZEL_VERSION}-installer-linux-x86_64.sh \
    && ./bazel-${BAZEL_VERSION}-installer-linux-x86_64.sh


COPY . /src
WORKDIR /src
