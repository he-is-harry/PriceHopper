companies_file = open("companies.txt", "r")
products_file = open("product_types.txt", "r")

companies = companies_file.read().splitlines()
products = products_file.read().splitlines()

wishlist = []
for product in products:
    for company in companies:
        wishlist.append(company + " " + product + "\n" + product)

wishlist_file = open("wishlist.txt", "w")
for search in wishlist:
    wishlist_file.write(search + "\n")

companies_file.close()
products_file.close()
wishlist_file.close()