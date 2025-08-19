from django.shortcuts import render

def get_all_product(request):
  
  context={
    "Food": [
        ("Pizza", "Delicious cheese pizza", 12.50, "product_img/pizza.jpg"),
        ("Burger", "Beef burger with fries", 8.75, "product_img/burger.jpg"),
        ("Pasta", "Italian pasta with sauce", 10.00, "product_img/pasta.jpg"),
        ("Salad", "Fresh vegetable salad", 6.25, "product_img/salad.jpg"),
    ],
  }

  return render(request,'index.html',context)