1. Entities & Relationships
1. Users

    user_id (PK)
    name
    email (Unique)
    password (Hashed)
    phone_number
    address_id (FK)
    role (Customer, Admin, Vendor, Delivery Partner)
    created_at
    updated_at

2. Addresses

    address_id (PK)
    user_id (FK)
    street
    city
    state
    zipcode
    country
    latitude
    longitude

3. Vendors (For multi-vendor support)

    vendor_id (PK)
    user_id (FK) (Vendor account)
    store_name
    store_address_id (FK)
    store_phone_number
    status (Active, Inactive)
    created_at
    updated_at

4. Products

    product_id (PK)
    vendor_id (FK)
    name
    description
    category_id (FK)
    price
    stock_quantity
    image_url
    rating
    created_at
    updated_at

5. Categories

    category_id (PK)
    name
    description

6. Product Reviews & Ratings

    review_id (PK)
    user_id (FK)
    product_id (FK)
    rating (1-5)
    review_text
    created_at

7. Shopping Cart

    cart_id (PK)
    user_id (FK)

8. Cart Items

    cart_item_id (PK)
    cart_id (FK)
    product_id (FK)
    quantity
    price_at_time_of_addition

9. Orders

    order_id (PK)
    user_id (FK)
    total_price
    status (Pending, Confirmed, Shipped, Delivered, Cancelled)
    payment_status (Paid, Unpaid, Refunded)
    created_at
    updated_at

10. Order Items

    order_item_id (PK)
    order_id (FK)
    product_id (FK)
    quantity
    price_at_purchase

11. Payments

    payment_id (PK)
    order_id (FK)
    user_id (FK)
    payment_method (Credit Card, PayPal, UPI, Cash on Delivery)
    payment_status (Pending, Successful, Failed)
    transaction_id
    payment_date

12. Delivery & Logistics

    delivery_id (PK)
    order_id (FK)
    delivery_partner_id (FK)
    delivery_status (Out for Delivery, Delivered, Failed)
    estimated_delivery_time
    actual_delivery_time

13. Wishlist

    wishlist_id (PK)
    user_id (FK)
    product_id (FK)

14. Coupons & Discounts

    coupon_id (PK)
    code (Unique)
    discount_percentage
    valid_from
    valid_to
    min_order_value
    max_discount

15. Admin & Reports

    admin_id (PK)
    user_id (FK)
    role (Super Admin, Moderator)
    permissions

2. Relationships

    One-to-Many
        Users → Orders (One user can have multiple orders)
        Users → Shopping Cart (One user has one cart)
        Vendors → Products (One vendor can have multiple products)
        Categories → Products (One category can have multiple products)
        Orders → Order Items (One order contains multiple products)
        Orders → Payments (One order has one payment)

    Many-to-Many
        Users ↔ Products (Users can rate/review multiple products)
        Users ↔ Products (Users can have multiple items in wishlist)
        Users ↔ Coupons (Users can use multiple coupons, but once per order)