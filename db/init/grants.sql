-- 為新增、刪除、修改、查詢賦予角色
GRANT SELECT ON TABLE bookmazon.book TO rl_sel;
GRANT SELECT ON TABLE bookmazon.cart TO rl_sel;
GRANT SELECT ON TABLE bookmazon.item TO rl_sel;
GRANT SELECT ON TABLE bookmazon.order TO rl_sel;
GRANT SELECT ON TABLE bookmazon.order_item TO rl_sel;
GRANT SELECT ON TABLE bookmazon.user TO rl_sel;

GRANT DELETE ON TABLE bookmazon.book TO rl_del;
GRANT DELETE ON TABLE bookmazon.cart TO rl_del;
GRANT DELETE ON TABLE bookmazon.item TO rl_del;
GRANT DELETE ON TABLE bookmazon.order TO rl_del;
GRANT DELETE ON TABLE bookmazon.order_item TO rl_del;
GRANT DELETE ON TABLE bookmazon.user TO rl_del;

GRANT UPDATE ON TABLE bookmazon.book TO rl_upd;
GRANT UPDATE ON TABLE bookmazon.cart TO rl_upd;
GRANT UPDATE ON TABLE bookmazon.item TO rl_upd;
GRANT UPDATE ON TABLE bookmazon.order TO rl_upd;
GRANT UPDATE ON TABLE bookmazon.order_item TO rl_upd;
GRANT UPDATE ON TABLE bookmazon.user TO rl_upd;

GRANT INSERT ON TABLE bookmazon.book TO rl_ins;
GRANT INSERT ON TABLE bookmazon.cart TO rl_ins;
GRANT INSERT ON TABLE bookmazon.item TO rl_ins;
GRANT INSERT ON TABLE bookmazon.order TO rl_ins;
GRANT INSERT ON TABLE bookmazon.order_item TO rl_ins;
GRANT INSERT ON TABLE bookmazon.user TO rl_ins;
