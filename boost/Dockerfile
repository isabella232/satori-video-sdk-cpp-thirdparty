FROM gcr.io/kubernetes-live/video/cpp-builder

COPY . /src
WORKDIR /src

RUN conan create satorivideo/master -k -s build_type=Release --options fPIC=True
RUN conan create satorivideo/master -k -s build_type=Debug --options fPIC=True