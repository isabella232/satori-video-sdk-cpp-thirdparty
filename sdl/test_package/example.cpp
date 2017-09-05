#include <iostream>
#include <SDL2/SDL.h>

int main() {
  if (SDL_Init(SDL_INIT_TIMER) < 0) {
    std::cerr << "SDL could not initialize! SDL_Error: " << SDL_GetError() << "\n";
    return 1;
  }
}
