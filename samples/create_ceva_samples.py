#!/usr/bin/env python3
"""
Create realistic CEVA Logistics sample data for WIGEON demo
"""

import pandas as pd
import random
from datetime import datetime, timedelta

# Generate sample CEVA Open Orders data
def create_open_orders():
    orders = []
    for i in range(100):
        order_date = datetime.now() - timedelta(days=random.randint(1, 30))
        orders.append({
            'Order Number': f'ORD-{10000 + i}',
            'Customer': random.choice(['Walmart', 'Amazon', 'Best Buy', 'Target', 'TD Synnex']),
            'SKU': f'A-SKU-{random.randint(1000, 9999):04d}',
            'Product': random.choice(['R4 Reader', 'Stand', 'Terminal', 'Dock', 'Cable']),
            'Quantity': random.randint(10, 500),
            'Order Date': order_date.strftime('%Y-%m-%d'),
            'Ship By Date': (order_date + timedelta(days=random.randint(1, 5))).strftime('%Y-%m-%d'),
            'Status': random.choice(['Open', 'Processing', 'Ready to Ship', 'Allocated']),
            'Warehouse': random.choice(['CVU - Plainfield', 'CVC - Georgetown', 'GBR - Coalville']),
            'Priority': random.choice(['Standard', 'Expedited', 'Rush'])
        })
    return pd.DataFrame(orders)

# Generate sample CEVA Service Level data
def create_service_level():
    service = []
    for i in range(50):
        report_date = datetime.now() - timedelta(days=i % 7)
        service.append({
            'Date': report_date.strftime('%Y-%m-%d'),
            'Warehouse': random.choice(['CVU - Plainfield', 'CVC - Georgetown', 'GBR - Coalville']),
            'Orders Shipped': random.randint(50, 200),
            'On-Time Shipments': random.randint(45, 195),
            'On-Time %': round(random.uniform(92, 99), 2),
            'Same Day Shipments': random.randint(40, 180),
            'Same Day %': round(random.uniform(85, 98), 2),
            'Order Fill Accuracy': round(random.uniform(97, 99.9), 2),
            'Delivery Performance': round(random.uniform(94, 99), 2),
            'Retailer Compliance': round(random.uniform(96, 100), 2)
        })
    return pd.DataFrame(service)

# Generate sample CEVA Inventory Transaction data
def create_inventory_transactions():
    transactions = []
    transaction_types = ['Receipt', 'Shipment', 'Adjustment', 'Transfer', 'Return']
    
    for i in range(150):
        trans_date = datetime.now() - timedelta(days=random.randint(1, 7))
        transactions.append({
            'Transaction ID': f'TXN-{20000 + i}',
            'Date': trans_date.strftime('%Y-%m-%d %H:%M:%S'),
            'Type': random.choice(transaction_types),
            'SKU': f'A-SKU-{random.randint(1000, 9999):04d}',
            'Product': random.choice(['R4 Reader', 'Stand', 'Terminal', 'Dock', 'Cable', 'Charger']),
            'Quantity': random.randint(-100, 500),
            'Warehouse': random.choice(['CVU - Plainfield', 'CVC - Georgetown', 'GBR - Coalville']),
            'Location': f'{random.choice(["A", "B", "C"])}{random.randint(1, 20):02d}-{random.randint(1, 10):02d}',
            'Reference': f'REF-{random.randint(1000, 9999)}',
            'Status': random.choice(['Completed', 'Pending', 'Verified'])
        })
    return pd.DataFrame(transactions)

# Generate sample CEVA Returns data
def create_returns():
    returns = []
    return_reasons = ['Defective', 'Customer Return', 'Wrong Item', 'Damaged', 'DOA']
    
    for i in range(75):
        return_date = datetime.now() - timedelta(days=random.randint(1, 14))
        returns.append({
            'RMA Number': f'RMA-{30000 + i}',
            'Return Date': return_date.strftime('%Y-%m-%d'),
            'Original Order': f'ORD-{random.randint(10000, 10999)}',
            'SKU': f'A-SKU-{random.randint(1000, 9999):04d}',
            'Product': random.choice(['R4 Reader', 'Stand', 'Terminal', 'Dock']),
            'Quantity': random.randint(1, 20),
            'Reason': random.choice(return_reasons),
            'Disposition': random.choice(['Refurbish', 'Scrap', 'Return to Vendor', 'Resell']),
            'Warehouse': random.choice(['CVU - Plainfield', 'CVC - Georgetown', 'GBR - Coalville']),
            'Status': random.choice(['Received', 'Inspected', 'Processed', 'Completed']),
            'Receipt Time (hrs)': round(random.uniform(2, 48), 1)
        })
    return pd.DataFrame(returns)

# Main execution
if __name__ == '__main__':
    print("🦆 Creating CEVA Logistics sample data...\n")
    
    # Create Open Orders
    print("1. Creating Block Open Orders...")
    df_orders = create_open_orders()
    df_orders.to_excel('ceva_open_orders.xlsx', index=False)
    print(f"   ✅ Created ceva_open_orders.xlsx ({len(df_orders)} orders)\n")
    
    # Create Service Level
    print("2. Creating Block Service Level Detail...")
    df_service = create_service_level()
    df_service.to_excel('ceva_service_level.xlsx', index=False)
    print(f"   ✅ Created ceva_service_level.xlsx ({len(df_service)} records)\n")
    
    # Create Inventory Transactions
    print("3. Creating Block Inventory Transaction Detail...")
    df_inventory = create_inventory_transactions()
    df_inventory.to_excel('ceva_inventory_transactions.xlsx', index=False)
    print(f"   ✅ Created ceva_inventory_transactions.xlsx ({len(df_inventory)} transactions)\n")
    
    # Create Returns
    print("4. Creating Block SRL Return Receipts...")
    df_returns = create_returns()
    df_returns.to_excel('ceva_returns.xlsx', index=False)
    print(f"   ✅ Created ceva_returns.xlsx ({len(df_returns)} returns)\n")
    
    print("✅ All CEVA sample files created successfully!")
    print(f"\nTotal records: {len(df_orders) + len(df_service) + len(df_inventory) + len(df_returns)}")
    print("\nFiles location: ~/WIGEON/samples")
