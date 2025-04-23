import csv
from uuid import UUID
from faker import Faker  # Corrected import statement

fake = Faker('en_IN')  # You can change the locale if needed

start_uuid = UUID('5ae9d535-7333-49ac-bc68-ca4717a62fe0')
base_uuid_str = str(start_uuid)[:-1]  # Remove the last hex digit

data = []
header = ["Transaction_ID", "Customer_ID", "Name", "Address", "Transaction_Date", "Transaction_Type", "Amount", "Payment_Mode", "Status", "Channel"]
data.append(header)

for i in range(6000):
    customer_id = i + 6
    last_hex = hex(i % 16)[2:].lower()
    transaction_id = base_uuid_str + last_hex
    name = fake.name()
    address = fake.address().replace('\n', ', ') # Replace newlines for single CSV cell

    transaction_date = fake.date_between(start_date='-2y', end_date='today')
    transaction_type = fake.random_element(elements=('Purchase', 'Return'))
    amount = round(fake.pyfloat(left_digits=3, right_digits=2, positive=True), 2)
    payment_mode = fake.random_element(elements=('Credit Card', 'Debit Card', 'Cash', 'Bank Transfer', 'UPI'))
    status = fake.random_element(elements=('Completed', 'Pending', 'Failed', 'Refunded'))
    channel = fake.random_element(elements=('Online', 'In-Store', 'Mobile App'))

    data.append([transaction_id, customer_id, name, address, transaction_date, transaction_type, amount, payment_mode, status, channel])

with open('transactions_data_6000.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)

print("Generated transactions_data_6000.csv")