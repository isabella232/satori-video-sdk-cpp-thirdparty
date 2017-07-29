#include <opencv2/opencv.hpp>

int main(int argc, char *argv[]) {
  cv::Mat A;
  cv::CascadeClassifier cascade;
  cv::Ptr<cv::BackgroundSubtractorKNN> extractor{
      cv::createBackgroundSubtractorKNN(500, 500.0, true)};
  return 0;
}
