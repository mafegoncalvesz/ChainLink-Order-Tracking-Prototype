import hashlib # For SHA-256 hashing
import json #format the data before hashing
from datetime import datetime, timedelta #timestamp every event

class Block:
    """
    Represents a single block in the blockchain.
    Each block records an order event at a specific office/location.
    """
    def __init__(self, index, timestamp, order_id, location, action, previous_hash, data=None):
        self.index = index
        self.timestamp = timestamp
        self.order_id = order_id
        self.location = location  # Which office/warehouse
        self.action = action  # What happened (received, picked, packed, dispatched, delivered)
        self.data = data or {}  # Additional data (employee, notes, etc.)
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
    
    def calculate_hash(self): #creates a unique digital fingerprint
        """
        Creates a SHA-256 hash of the block's contents.
        This makes the block immutable - any change will alter the hash.
        """
        block_string = json.dumps({
            "index": self.index,
            "timestamp": str(self.timestamp),
            "order_id": self.order_id,
            "location": self.location,
            "action": self.action,
            "data": self.data,
            "previous_hash": self.previous_hash
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def __repr__(self):
        return f"Block {self.index}: {self.location} - {self.action} (Hash: {self.hash[:8]}...)"


class OrderBlockchain:
    """
    Manages the blockchain for order tracking across multiple offices.
    """
    def __init__(self):
        self.chain = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """
        Creates the first block in the chain (genesis block).
        """
        genesis_block = Block(0, datetime.now(), "GENESIS", "System", "Chain Initialized", "0")
        self.chain.append(genesis_block)
    
    def get_latest_block(self):
        """Returns the most recent block in the chain."""
        return self.chain[-1]
    
    def add_block(self, order_id, location, action, data=None):
        """
        Adds a new block to the chain representing an order event.
        """
        previous_block = self.get_latest_block()
        new_index = previous_block.index + 1
        new_timestamp = datetime.now()
        new_block = Block(new_index, new_timestamp, order_id, location, action, 
                         previous_block.hash, data)
        self.chain.append(new_block)
        return new_block
    
    def validate_chain(self): #security guard
        """
        Validates the integrity of the blockchain.
        Checks if any blocks have been tampered with.
        Returns True if valid, False if tampered.
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            # Check if current block's hash is correct
            if current_block.hash != current_block.calculate_hash():
                print(f"❌ TAMPERING DETECTED at Block {i}: Hash mismatch!")
                return False
            
            # Check if current block points to correct previous block
            if current_block.previous_hash != previous_block.hash:
                print(f"❌ TAMPERING DETECTED at Block {i}: Chain broken!")
                return False
        
        return True
    
    def get_order_journey(self, order_id):
        """
        Retrieves all blocks related to a specific order ID.
        Shows the complete journey of an order through offices.
        """
        order_blocks = [block for block in self.chain if block.order_id == order_id]
        return order_blocks
    
    def display_order_journey(self, order_id):
        """
        Displays a formatted view of an order's journey through the system.
        """
        blocks = self.get_order_journey(order_id)
        
        if not blocks:
            print(f"No blocks found for Order #{order_id}")
            return
        
        print("\n" + "="*80)
        print(f"ORDER #{order_id} - COMPLETE JOURNEY")
        print("="*80)
        
        start_time = blocks[0].timestamp
        
        for block in blocks:
            time_elapsed = block.timestamp - start_time
            hours = time_elapsed.total_seconds() / 3600
            
            print(f"\n📦 Block {block.index}")
            print(f"   🕐 Timestamp: {block.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   ⏱️  Time Elapsed: {hours:.1f} hours")
            print(f"   📍 Location: {block.location}")
            print(f"   ✅ Action: {block.action}")
            if block.data:
                print(f"   📝 Details: {block.data}")
            print(f"   🔐 Hash: {block.hash[:16]}...")
            print(f"   🔗 Previous Hash: {block.previous_hash[:16]}...")
        
        total_time = blocks[-1].timestamp - start_time
        print("\n" + "-"*80)
        print(f"⏱️  TOTAL DELIVERY TIME: {total_time.days} days, {total_time.seconds // 3600} hours")
        print("="*80 + "\n")
    
    def display_all_blocks(self):
        """Displays all blocks in the blockchain."""
        print("\n" + "="*80)
        print("COMPLETE BLOCKCHAIN - ALL ORDERS")
        print("="*80)
        for block in self.chain:
            print(f"\nBlock {block.index}: Order #{block.order_id}")
            print(f"  Location: {block.location} | Action: {block.action}")
            print(f"  Hash: {block.hash[:16]}... | Previous: {block.previous_hash[:16]}...")
        print("="*80 + "\n")


def simulate_order_tracking():
    """
    Demonstrates the blockchain system with realistic order scenarios.
    Shows how orders move through OneStop's offices and warehouses.
    """
    
    print("\n CHAINLINK OPERATIONS SYSTEM - DEMONSTRATION")
    print("="*80)
    print("Blockchain-Based Internal Collaboration for OneStop")
    print("="*80 + "\n")
    
    # Initialize blockchain
    blockchain = OrderBlockchain()
    
    # Simulate Order #12345 (Ana's order - Electronics)
    print("📱 Simulating Order #12345 (Ana - Marketing Specialist - Laptop)")
    print("-"*80)
    
    base_time = datetime.now() - timedelta(days=3)
    
    # Order received at Brisbane office
    blockchain.chain.append(Block(1, base_time, "12345", "Brisbane Office", 
                                  "Order Received", blockchain.chain[0].hash,
                                  {"customer": "Ana", "product": "Laptop", "employee": "Sarah J"}))
    
    # Warehouse picks item
    blockchain.chain.append(Block(2, base_time + timedelta(hours=2), "12345", 
                                  "Sydney Warehouse", "Items Picked", blockchain.chain[-1].hash,
                                  {"picker": "John D", "quantity": "1 unit"}))
    
    # Warehouse packs item
    blockchain.chain.append(Block(3, base_time + timedelta(hours=3, minutes=30), "12345",
                                  "Sydney Warehouse", "Items Packed", blockchain.chain[-1].hash,
                                  {"packer": "Maria K", "box_id": "BOX-7821"}))
    
    # Logistics partner dispatches
    blockchain.chain.append(Block(4, base_time + timedelta(days=1, hours=8), "12345",
                                  "Logistics Partner (AusPost)", "Package Dispatched", 
                                  blockchain.chain[-1].hash,
                                  {"tracking": "AP123456789AU", "driver": "Mike T"}))
    
    # Delivered to customer
    blockchain.chain.append(Block(5, base_time + timedelta(days=2, hours=11), "12345",
                                  "Customer Location (Brisbane)", "Delivered Successfully", 
                                  blockchain.chain[-1].hash,
                                  {"recipient": "Ana", "signature": "Confirmed"}))
    
    # Simulate Order #67890 (Erick's B2B order - Bulk office supplies)
    print("\n🏢 Simulating Order #67890 (Erick - B2B Purchasing Manager - Bulk Supplies)")
    print("-"*80)
    
    b2b_time = datetime.now() - timedelta(days=5)
    
    blockchain.chain.append(Block(6, b2b_time, "67890", "Melbourne Office",
                                  "B2B Order Received", blockchain.chain[-1].hash,
                                  {"customer": "Erick Corp", "value": "$15,000", "priority": "HIGH"}))
    
    blockchain.chain.append(Block(7, b2b_time + timedelta(hours=1), "67890",
                                  "Melbourne Warehouse", "Items Picked (Bulk)", 
                                  blockchain.chain[-1].hash,
                                  {"items": "Office supplies x500", "pallets": "4"}))
    
    blockchain.chain.append(Block(8, b2b_time + timedelta(days=1), "67890",
                                  "Melbourne Warehouse", "Quality Check Completed",
                                  blockchain.chain[-1].hash,
                                  {"inspector": "Linda P", "status": "PASSED"}))
    
    blockchain.chain.append(Block(9, b2b_time + timedelta(days=1, hours=4), "67890",
                                  "Logistics Partner (StarTrack)", "Freight Dispatched",
                                  blockchain.chain[-1].hash,
                                  {"vehicle": "TRUCK-45", "driver": "Tom R"}))
    
    blockchain.chain.append(Block(10, b2b_time + timedelta(days=3, hours=9), "67890",
                                  "Erick Corp Warehouse (Sydney)", "Delivered & Signed",
                                  blockchain.chain[-1].hash,
                                  {"recipient": "Erick", "invoice": "INV-67890"}))
    
    # Display individual order journeys
    blockchain.display_order_journey("12345")
    blockchain.display_order_journey("67890")
    
    # Validate blockchain integrity
    print("\n🔐 BLOCKCHAIN VALIDATION")
    print("="*80)
    if blockchain.validate_chain():
        print("✅ BLOCKCHAIN VALID - No tampering detected")
        print("   All blocks are cryptographically linked and verified")
    else:
        print("❌ BLOCKCHAIN COMPROMISED - Tampering detected!")
    print("="*80 + "\n")
    
    # Demonstrate tampering detection
    print("\n  TAMPERING DETECTION DEMONSTRATION")
    print("="*80)
    print("Attempting to modify Block 4 (Logistics dispatch for Order #12345)...")
    
    # Tamper with a block
    original_action = blockchain.chain[4].action
    blockchain.chain[4].action = "PACKAGE LOST"  # Malicious modification
    
    print(f"❌ Modified: '{original_action}' → 'PACKAGE LOST'\n")
    
    if blockchain.validate_chain():
        print("✅ Blockchain still valid (this shouldn't happen!)")
    else:
        print(" TAMPERING DETECTED!")
        print("   The blockchain's cryptographic integrity has been violated")
        print("   Any attempt to alter records is immediately visible")
        print("   This ensures complete accountability across all offices")
    
    # Restore original
    blockchain.chain[4].action = original_action
    blockchain.chain[4].hash = blockchain.chain[4].calculate_hash()
    
    print("\n Block restored to original state")
    print("="*80 + "\n")
    
    # Show key benefits
    print("\n KEY BENEFITS FOR ONESTOP")
    print("="*80)
    benefits = [
        "✅ Complete Visibility: Every office sees real-time order status",
        "✅ Accountability: Immutable records show exactly who did what and when",
        "✅ Faster Resolution: Customer service instantly knows order location",
        "✅ B2B Compliance: Erick's company gets auditable chain of custody",
        "✅ Analytics Ready: Data reveals bottlenecks and inefficiencies",
        "✅ Tamper-Proof: Cryptographic security prevents record manipulation"
    ]
    for benefit in benefits:
        print(benefit)
    print("="*80 + "\n")
    
    return blockchain


# Run the simulation
if __name__ == "__main__":
    blockchain = simulate_order_tracking()
    
    print("\n📊 SUMMARY STATISTICS")
    print("="*80)
    print(f"Total Blocks in Chain: {len(blockchain.chain)}")
    print(f"Orders Tracked: 2 (Order #12345, Order #67890)")
    print(f"Offices/Locations: 5 (Brisbane, Sydney, Melbourne, Logistics, Customers)")
    print(f"Chain Integrity: {'✅ VALID' if blockchain.validate_chain() else '❌ INVALID'}")
    print("="*80 + "\n")
    
    print("🎯 ASSESSMENT 2 DEMONSTRATION COMPLETE")
    print("This prototype demonstrates blockchain-based internal collaboration")
    print("solving OneStop's coordination problems identified in Assessment 1.\n")

#References:
#https://github.com/amandladev/Blockchain-prototype/tree/v1
#https://www.youtube.com/watch?v=Jt9MYcSsVzs
