import pandas as pd

df = pd.read_json("trial_task.json", orient="columns")

######################################################
#   Извлекаем тарифы за доставку по каждому складу   #
######################################################

delivery_prices = {}
for elem in range(len(df)):
    row = df.loc[elem]
    highway_cost, warehouse_name = row["highway_cost"], row["warehouse_name"]
    products = row["products"]
    quantity_count = 0
    quantity_count += sum([product["quantity"] for product in products])
    delivery_cost = highway_cost / quantity_count
    delivery_prices[warehouse_name] = delivery_cost


warehouse_names = set(delivery_prices)
res = []
for name in warehouse_names:
    price = delivery_prices[name]
    # print(row)
    res.append(
        {"warehouse": name,
         "expenses_per_product": price,}
    )

print(pd.DataFrame(res))

######################################################
#   Извлекаем тарифы за доставку по каждому складу   #
######################################################

products_dict = {}
for elem in range(len(df)):
    row = df.loc[elem]
    warehouse_name = row["warehouse_name"]

    order_id = row["order_id"]
    products = row["products"]
    for product in products:
        name = product["product"]
        quantity = product["quantity"]
        price = product["price"]
        income = price * quantity
        expenses = delivery_prices[warehouse_name] * quantity
        profit = income + expenses
        if product["product"] not in products_dict:
            products_dict[name] = {"quantity": quantity,
                                   "income": income,
                                   "expenses": expenses,
                                   "profit": profit}
        else:
            products_dict[name]["quantity"] += quantity
            products_dict[name]["income"] += income
            products_dict[name]["expenses"] += expenses
            products_dict[name]["profit"] += profit


score = pd.DataFrame(products_dict)
product_names = set(products_dict)
res = []
for name in product_names:
    row = score[name]
    res.append(
        {"product": name,
         "quantity" : row["quantity"],
         "income" : row["income"],
         "expenses" : row["expenses"],
         "profit" : row["profit"]}
    )
print(pd.DataFrame(res))
