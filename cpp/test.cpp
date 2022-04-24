#include <vector>
#include <iostream>
#include <omp.h>
#include <chrono>

template<typename T>
T InnerProd(const std::vector<T> &vec) {
   
   T val = 0.0;
   
#pragma omp parallel for reduction (+: val)
   for (std::size_t i = 0; i < vec.size(); ++i) {
      for (std::size_t j = 0; j < vec.size(); ++j) {
         val += vec[i]*vec[j];
      }
   }
   
   return val;
   
}

int main(void) {
   
   const std::int64_t N = 100000;
   std::vector<double> v_d(N, 1.0);
   
   auto start = std::chrono::system_clock::now();
   auto ans = InnerProd(v_d);
   auto end = std::chrono::system_clock::now();
   double elapsed = static_cast<double>(std::chrono::duration_cast<std::chrono::milliseconds>(end-start).count())/1000.0;

   std::cout << ans << ": " << elapsed << std::endl;
   
   return 0;
}

