#include <iostream>

#include "gtest/gtest.h"

TEST(dummy, test) {
    ASSERT_EQ(1, 1) << "1 should be equal to 1";
}

int main(int argc, char *argv[]) {
    std::cout << "checking if gtest is available\n";
    ::testing::InitGoogleTest(&argc, argv);
    int err = RUN_ALL_TESTS();
    if (err) {
        std::cerr << "gtest check failed\n";
        return err;
    }

    std::cout << "gtest check succeeded\n";
    return 0;
}
