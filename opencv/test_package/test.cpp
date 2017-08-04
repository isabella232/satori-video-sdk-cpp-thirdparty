#include <opencv2/opencv.hpp>
#include <opencv2/tracking.hpp>

int main(int argc, char *argv[]) {
  cv::Mat A;
  cv::CascadeClassifier cascade;

  if (argc > 1) {
    cv::VideoCapture cap(argv[1]);
    cv::Mat frame;
    while (cap.grab()) {
      cap >> frame;
    }
  }

  cv::Ptr<cv::Tracker> tracker = cv::TrackerKCF::create();
  cv::Ptr<cv::BackgroundSubtractorKNN> extractor{
      cv::createBackgroundSubtractorKNN(500, 500.0, true)};
  return 0;
}
