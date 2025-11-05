# ChainLink-Order-Tracking-Prototype
This project is a Python-based blockchain simulation designed to demonstrate how blockchain technology can enhance transparency, accountability, and efficiency in supply chain and logistics operations.

This prototype showcases how immutable records and cryptographic validation can solve real-world coordination challenges across multiple offices or warehouses.

Features:

- Blockchain Core Structure  
  Each order event is stored as a block linked by cryptographic hashes. Any modification to a block automatically invalidates the chain.

- Order Tracking Simulation  
  Demonstrates two example orders (#12345 and #67890) moving through offices, warehouses, and logistics partners. Includes timestamps, employee actions, and data integrity validation.

- Tampering Detection  
  The system automatically detects any unauthorised changes and demonstrates blockchain’s immutability through integrity checks.

- Readable Output  
  Prints complete order journeys with elapsed time, actions, and hashes. Provides a summary and highlights the benefits of blockchain for organisations.

Technologies Used

- Python 3.10+
- hashlib (SHA-256 hashing)
- datetime (timestamps and time deltas)
- json (data serialisation)



Key Concepts Demonstrated

- Blockchain fundamentals (blocks, hashes, linking)
- Data immutability and tamper detection
- Transparency in multi-location business processes
- Applying blockchain in logistics and internal collaboration



 How to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/<your-username>/chainlink-order-tracking.git
   cd chainlink-order-tracking
