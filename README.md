contains 4 algorithms for branch  (Used for speculative execution)

1. 1-bit branch predictor
  a simple branch predicton algorithm.
  keeps a BHT(Branch history table) for each branch and intially assumes that the branch is not taken. 
  updates the status of the branch when executing. 
  
2. 2-bit branch predictor
  maintains the status history using 2 bits
  changes status based on 2 bit branch predictor state machine.
  
3. 2,2 branch predictor
  Has 4 BHTs that are identified by 2 bit addresses. 
  the 2 previously executed branches decide the BHT to be updated. 
  
4. Custom branch predictor
  not a conventional algorithm.
  Contains 8 tables addressed by 3 bit IDs. 
  keeps history of three last executed branches. 
