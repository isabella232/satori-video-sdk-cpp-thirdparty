#include <opencv2/opencv.hpp>
#include <opencv2/tracking.hpp>

int main(int argc, char *argv[]) {
  cv::Mat A;
  cv::CascadeClassifier cascade;
  cv::Ptr<cv::Tracker> tracker = cv::Tracker::create("KCF");
  cv::Ptr<cv::BackgroundSubtractorKNN> extractor{
      cv::createBackgroundSubtractorKNN(500, 500.0, true)};
  return 0;
}
