import pandas as pd

df = pd.read_json("trial_task.json", orient="columns")

###############################################################
#                         Задание №1                          #
###############################################################

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

print("РЕШЕНИЕ ЗАДАЧИ №1 \n Тарифы стоимости доставки для каждого склада:")
print(pd.DataFrame(res))

###############################################################
#                         Задание №2                          #
###############################################################

products_dict = {}
for elem in range(len(df)):
    row = df.loc[elem]
    warehouse_name = row["warehouse_name"]
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

print("РЕШЕНИЕ ЗАДАЧИ №2 \n Суммарные: количество, доход, расход и прибыль для каждого товара:")
print(pd.DataFrame(res))


###############################################################
#                         Задание №3                          #
###############################################################

order_dict = {}
for elem in range(len(df)):
    row = df.loc[elem]
    warehouse_name = row["warehouse_name"]
    order_id = row["order_id"]
    products = row["products"]
    for product in products:
        profit = (product["price"] * product["quantity"]) + (delivery_prices[warehouse_name] * product["quantity"])
        if order_id not in order_dict:
            order_dict[order_id] = profit
        else:
            order_dict[order_id] += profit

orders = set(order_dict)
res = []
for order in orders:
    res.append(
        {
            "order_id" : order,
            "order_profit" : order_dict[order],
         }
    )
orders_df = pd.DataFrame(res)
mean_profit = orders_df['order_profit'].mean()


print("РЕШЕНИЕ ЗАДАЧИ №3 \n Составить табличку с id заказа, прибылью с заказа + средняя прибыль:")
print(orders_df)
print(f"Среднее значение прибыли по всем заказам составила {mean_profit}")


###############################################################
#                         Задание №4                          #
###############################################################

warehouse_df = df[["warehouse_name", "products"]]
warehouse_dict = {}
for elem in range(len(warehouse_df)):
    row = warehouse_df.loc[elem]
    warehouse_name = row["warehouse_name"]
    products = row["products"]
    if warehouse_name in warehouse_dict:
         warehouse_dict[warehouse_name] += products
    else:
        warehouse_dict[warehouse_name] = []
        warehouse_dict[warehouse_name] += products

warehouse_names = set(warehouse_dict)

for name in warehouse_names:
    summ_of_profit = 0
    for product in warehouse_dict[name]:
        profit = (product["price"] * product["quantity"]) + (delivery_prices["Мордор"] * product["quantity"])
        product["profit"] = profit
        summ_of_profit += profit
    for product in warehouse_dict[name]:
        product["percent"] = (product["profit"] * 100) / summ_of_profit

for name in warehouse_names:
    warehouse_products = warehouse_dict[name]
    products_dict = {}
    for product_dict in warehouse_products:
        product_name = product_dict["product"]
        quantity = product_dict["quantity"]
        profit = product_dict["profit"]
        percent = product_dict["percent"]
        if product_name not in products_dict:
            products_dict[product_name] = {"quantity" : quantity,
                                           "profit": profit,
                                           "percent": percent}
        else:
            products_dict[product_name]["quantity"] += quantity
            products_dict[product_name]["profit"] += profit
            products_dict[product_name]["percent"] += percent

    warehouse_dict[name] = products_dict

res = []
for name in warehouse_names:
    warehouse_products = warehouse_dict[name]
    product_names = set(warehouse_products)
    # print(product_names)
    for product_name in product_names:
        product = warehouse_products[product_name]
        res.append(
            {
                "warehouse_name": name,
                "product" : product_name,
                "quantity" : product["quantity"],
                "profit" : product["profit"],
                "percent": product["percent"],
            }
        )


warehouse_df = pd.DataFrame(res)

print("РЕШЕНИЕ ЗАДАЧИ №4 \n Составить табличку типа 'warehouse_name', 'product','quantity', 'profit', 'percent'  \n \
(процент прибыли продукта заказанного из определенного склада к прибыли этого склада)")
print(warehouse_df)


###############################################################
#                         Задание №5                          #
###############################################################

sorted_df = warehouse_df.sort_values(['warehouse_name', 'percent'], ascending=False)

sorted_df['accumulated_percent'] = sorted_df.groupby('warehouse_name')['percent'].cumsum()

print("РЕШЕНИЕ ЗАДАЧИ №5 \n # Oтсортировать предыдущую табличку по убыванию процента, после посчитать накопленный процент.")
print(sorted_df)

###############################################################
#                         Задание №6                          #
###############################################################

def f(row):
    if row['accumulated_percent'] <= 70:
        val = 'A'
    elif 70 < row['accumulated_percent'] <= 90:
        val = 'B'
    else :
        val = 'C'
    return val

sorted_df['category'] = sorted_df.apply (f, axis=1)

print("РЕШЕНИЕ ЗАДАЧИ №6 \n # Oтсортировать предыдущую табличку по убыванию процента, после посчитать накопленный процент.")
print(sorted_df)


