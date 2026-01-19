# test_insert.py
from insert_log import insert_log

# testa tre olika fall
insert_log("INFO",    "PaymentService",  "Payment processed", {"amount": 100, "currency": "SEK"})
insert_log("WARNING", "AuthService",     "Login attempt from blocked IP")
insert_log("ERROR",   "InventoryService", "Failed to update stock", {"sku": "A123", "delta": -5})