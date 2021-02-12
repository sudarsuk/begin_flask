# Guest
- `/`           ?new ?edit POST-create POST-edit
- `/confirm`
- `/thanks`

# Admin
- `/admin`
- `/admin/archive`
- `/admin/product`
- `/admin/product/new`
- `/admin/product/<int>`
- `/admin/config`
> endfold

- todo: use text mask on (1.phone, 2.account number)
  uselooper.com/form-autocompletes.html

- todo: /admin/product/list хуудсанд "бараа нэмэх"-н зүүн талд link => "Draft (3)"
- todo: /admin/product/list remove table tabs
- todo: create /admin/product/list-draft

- todo: pagination on `/admin/order/list-finished`
- todo: `grep 'href="' -r . | grep '?'`
- todo: rename to `templates/admin/product-list-draft.html`

- todo: add class `.tugrik`
  - product related pages
  - ✓ templates/Layout.html
  - ✓ templates/admin/Layout.html
  - ✓ templates/admin/manager.html
- ✓ test_data_sql/order-tagtaa-mn--order.sql
- ✓ templates/admin/debug.html
- ✓ web.py
- ✓ todo: rename `draft-list.html`
  - ✓ ...in/{admin-list-draft.html → product-draft-list.html}
- ✓ utils.py
- ✓ templates/index.html
- ✓ templates/confirm.html
- ✓ templates/thanks.html
- ✓ templates/admin/{admin-config.html → config.html}
- ✓ templates/admin/product-list.html
- ✓ templates/admin/order-list-deleted.html

- README.md
- templates/admin/admin.html
- templates/admin/order-list-finished.html
  - pagination

- debt: remove Data `sale` on mostmn.com (database)
- debt: change rule of shipping is free
