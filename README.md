#  Multilevel Cache Simulator  

This **Python-based Multilevel Cache Simulator** models a **two-level cache system (L1 & L2)**, allowing users to specify cache parameters such as **size, block size, associativity, and replacement policies** (**LRU, FIFO, or Random**).  

The simulator processes memory accesses in a **multithreaded environment**, mimicking multiple CPU cores accessing the cache in **parallel**. It logs the results and visualizes cache performance with a **bar chart**.  

## 🛠 Features  

- **Multilevel Cache (L1 & L2)** – Simulates two levels of cache to improve memory access efficiency.  
- **Configurable Replacement Policies** – Supports:  
  - **LRU** (Least Recently Used)  
  - **FIFO** (First-In-First-Out)  
  - **Random** replacement strategies  
- **Associative Mapping** – Allows both:  
  - **Direct Mapping** (1-way)  
  - **N-Way Set Associative Mapping** based on user input  
- **Parallel Processing (Multithreading)** – Simulates multiple CPUs accessing the cache simultaneously.  
- **Performance Logging & Visualization** –  
  - Saves results to a text file (**results.txt**).  
  - Generates a **bar chart** (**cache_performance.png**) for analysis.  
