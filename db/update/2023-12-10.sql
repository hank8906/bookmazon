GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA bookmazon TO user_001;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA bookmazon TO app_001;
GRANT SELECT ON TABLE bookmazon.cart_item TO rl_sel;
GRANT DELETE ON TABLE bookmazon.cart_item TO rl_sel;
GRANT UPDATE ON TABLE bookmazon.cart_item TO rl_sel;
GRANT INSERT ON TABLE bookmazon.cart_item TO rl_sel;
