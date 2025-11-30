from product import UnlimitedLifeProduct
from transaction import Transaction

def test_total_price():
    print("Test 1: total price")
    product = UnlimitedLifeProduct("T001", "Pen", 3000, 100)
    transaction = Transaction()
    transaction.additem(product, 3)
    total = transaction.calculatetotal()
    print("Expected total: 9000")
    print("Actual total:  ", total)
    if total == 9000:
        print("Test: PASS\n")
    else:
        print("Test: FAIL\n")

def test_stock_reduction():
    print("Test 2: stock reduction")
    product = UnlimitedLifeProduct("T002", "Book", 5000, 10)
    print("Initial stock:", product.stock)
    product.reducestock(3)
    print("Expected stock: 7")
    print("Actual stock:  ", product.stock)
    if product.stock == 7:
        print("Test: PASS\n")
    else:
        print("Test: FAIL\n")

if __name__ == "__main__":
    test_total_price()
    test_stock_reduction()
