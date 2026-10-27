"""Supplier purchase order tracker for a stores department.

Places orders with suppliers, marks deliveries as received, notifies the
warehouse and cleans up fulfilled orders.
"""
import sqlite3


def create_database():
    """Create an in-memory database with an empty orders table."""
    connection = sqlite3.connect(":memory:")
    connection.execute(
        "CREATE TABLE orders (id INTEGER PRIMARY KEY, supplier TEXT, "
        "item TEXT, quantity INTEGER, received INTEGER, remarks TEXT)"
    )
    return connection


def place_order(connection, supplier, item, quantity):
    """Record a new order and return the quantity that was ordered."""
    connection.execute(
        "INSERT INTO orders (supplier, item, quantity, received) "
        "VALUES (?, ?, ?, 0)",
        (supplier, item, quantity),
    )
    return quantity


def mark_received(connection, order_id, remarks):
    """Mark an order as received and store the delivery remarks."""
    connection.execute(
        "UPDATE orders SET received = 1, remarks = ? WHERE id = ?",
        (remarks, order_id),
    )


def notify_warehouse(supplier):
    """Tell the warehouse that a supplier's delivery has arrived."""
    print("notifying warehouse about " + supplier)


def cleanup(connection):
    """Delete orders that have already been received."""
    try:
        connection.execute("DELETE FROM orders WHERE received = 1")
    except sqlite3.Error as err:
        print("cleanup failed: " + str(err))


def pending_count(connection):
    """Return the number of orders that have not been received yet."""
    cursor = connection.execute(
        "SELECT COUNT(*) FROM orders WHERE received = 0"
    )
    return cursor.fetchone()[0]


def main():
    """Run a short demonstration of the order tracker."""
    connection = create_database()
    order_total = 0
    order_total += place_order(connection, "Acme Steel", "rods", 40)
    order_total += place_order(connection, "Bolt Co", "bolts", 500)
    mark_received(connection, 1, "ok")
    notify_warehouse("Acme")
    print(pending_count(connection), order_total)
    cleanup(connection)
    connection.close()


if __name__ == "__main__":
    main()
