#include <tensorflow/core/framework/tensor.h>
#include <tensorflow/core/platform/types.h>
#include <tensorflow/core/public/session.h>

#include <tensorflow/cc/saved_model/loader.h>
#include <tensorflow/cc/saved_model/signature_constants.h>
#include <tensorflow/cc/saved_model/tag_constants.h>

void load_model() {
  tensorflow::SavedModelBundle bundle;
  tensorflow::Status load_model_status = tensorflow::LoadSavedModel(
      tensorflow::SessionOptions(), tensorflow::RunOptions(), "fake_model_dir",
      {tensorflow::kSavedModelTagTrain}, &bundle);
}

int main() {
  tensorflow::string str;
  tensorflow::Tensor tensor;
}
