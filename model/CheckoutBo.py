class CheckoutBo:
    def __init__(self, user_account, cart_items, recipient_name, recipient_city,
                 recipient_district, recipient_address, payment_method):
        self.user_account = user_account
        self.cart_items = cart_items
        self.recipient_name = recipient_name
        self.recipient_city = recipient_city
        self.recipient_district = recipient_district
        self.recipient_address = recipient_address
        self.payment_method = payment_method
