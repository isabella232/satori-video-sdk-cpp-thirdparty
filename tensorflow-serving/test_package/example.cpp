#include <iostream>

#include <tensorflow/cc/framework/scope.h>
#include <tensorflow/cc/ops/const_op.h>
#include <tensorflow/cc/ops/standard_ops.h>
#include <tensorflow/core/framework/graph.pb.h>
#include <tensorflow/core/framework/tensor.h>
#include <tensorflow/core/graph/default_device.h>
#include <tensorflow/core/graph/graph_def_builder.h>
#include <tensorflow/core/lib/core/errors.h>
#include <tensorflow/core/platform/init_main.h>
#include <tensorflow/core/platform/types.h>
#include <tensorflow/core/public/session.h>

tensorflow::Status get_top(const std::vector<tensorflow::Tensor> &outputs, int how_many_labels,
                   tensorflow::Tensor *indices, tensorflow::Tensor *scores) {
  auto root = tensorflow::Scope::NewRootScope();

  tensorflow::ops::TopK(root.WithOpName("top_k"), outputs[0], how_many_labels);

  tensorflow::GraphDef graph;
  TF_RETURN_IF_ERROR(root.ToGraphDef(&graph));

  std::unique_ptr<tensorflow::Session> session(
      tensorflow::NewSession(tensorflow::SessionOptions()));
  TF_RETURN_IF_ERROR(session->Create(graph));

  std::vector<tensorflow::Tensor> out_tensors;
  TF_RETURN_IF_ERROR(session->Run({}, {"top_k:0", "top_k:1"}, {}, &out_tensors));
  *scores = out_tensors[0];
  *indices = out_tensors[1];
  return tensorflow::Status::OK();
}

int main() {
  tensorflow::string str;
  tensorflow::Tensor tensor;
  auto root = tensorflow::Scope::NewRootScope();

}
