"""Three Crazy Bakers — verified first-party content.

Sources: threecrazybakers.com pages (text) + menu scans transcribed 2026-07-24
(menu.jpg 2022 dinner; Lunch-ToGo-Menu_2023 pages 1-2) + selected-b asset
package implementation-data.json. Prices/hours are the business's own posted
values as of harvest; the site carries a "call to confirm" softener per
factory precedent. Never invent items, prices, or hours.
"""

FACTS = {
    'name': 'Three Crazy Bakers',
    'tagline': 'On the Square. At the Table.',
    'address': '102 S Main St, Moultrie, GA 31768',
    'address_short': '102 S Main St, Moultrie GA',
    'phone': '(229) 985-8809',
    'phone_href': 'tel:+12299858809',
    'hours': [('Monday – Saturday', '10:00am – 9:00pm'), ('Sunday', '11:00am – 8:00pm')],
    'est': '1998',
    'origin': 'We are Three Crazy Bakers because there once were three crazy people who wanted a bakery.',
    'founders': 'Larry and Donna Grimm and their daughter Paige',
    'owners': 'Maggie and Hart Brown',
    'order_url': 'https://order.online/business/Three%20Crazy%20Bakers-308079',
    'closing_line': 'Come to Moultrie and eat some of the best food East of the Mississippi.',
}

DISCLAIMER = ('Steaks are cooked to order. Consuming raw or undercooked meats, poultry, seafood, '
              'shellfish, or eggs may increase your risk of food-borne illness, especially if you '
              'have certain medical conditions.')

PRICE_NOTE = ('Prices and selections are from our posted menus — call '
              f"{FACTS['phone']} to confirm today's offerings.")

BREAKFAST = {
    'title': 'Breakfast',
    'items': [
        ('Quiche Plate', '7.25', 'Dependent on availability: Ham & Cheese, Bacon & Tomato, Spinach & Swiss or Crazy (bacon, spinach, tomato, onion, cheese). Served with fresh fruit and a warm mini-muffin.'),
        ('Quiche Slice', '3.00', ''),
        ('Sausage & Cheese Roll', '1.50', ''),
        ('Cinnamon Roll', '1.25', ''),
        ('Side of Fruit', '3.00', ''),
    ],
    'beverages': [
        ('Coffee', 'Small .75 · Large 1.00'),
        ('Orange Juice', '1.75'),
        ('Coke Products', '1.25'),
    ],
}

ROLLUPS_NOTE = ('Served with chips. Substitute Pasta Salad, Fresh Fruit, Broccoli Salad or Green '
                'Salad 1.50 · Cup of Potato Soup 2.00 · Cup of White Chicken Chili 2.75')

ROLLUPS = [
    ('Honey Bacon Chicken', '7.75', 'Warm chicken, cheddar cheese, bacon & honey mustard dressing rolled up tight & grilled golden brown in a giant flour tortilla.'),
    ('Blackened Chicken', '7.75', 'Spicy chicken, Monterey Jack cheese & honey mustard dressing rolled up tight & grilled golden brown in a giant flour tortilla.'),
    ('Southwestern Chicken', '7.75', 'Spicy chicken, cheddar & Monterey Jack cheeses, bacon, scallions & BBQ sauce rolled up tight & grilled golden brown in a giant flour tortilla.'),
    ('Chicken Popper', '7.75', 'Cream cheese, warm chicken, onion, jalapeño peppers & ranch dressing rolled up tight & grilled golden brown in a giant flour tortilla.'),
    ('Crazy Chicken', '8.50', 'Warm chicken, cheddar & Monterey Jack cheeses, spinach, onion, bacon, tomato & a spicy chipotle ranch dressing rolled up tight & grilled golden brown in a giant tomato basil tortilla.'),
    ('Chicken Cordon Blue', '8.50', 'Warm chicken, Swiss cheese, ham, mushrooms, tomatoes and basil mayonnaise rolled up tight in a giant tomato basil tortilla.'),
    ('Buffalo Chicken', '7.75', 'Warm chicken tossed in spicy buffalo sauce with Monterey Jack cheese & ranch dressing rolled up tight & grilled golden brown in a giant flour tortilla.'),
    ('Catalina Chicken', '8.50', 'Warm chicken, cheddar cheese, bacon, avocado, lettuce and basil mayonnaise rolled up tight in a giant tomato basil tortilla.'),
    ('Caesar Chicken', '7.75', 'Warm chicken, Parmesan cheese, fresh romaine lettuce and creamy Caesar dressing rolled up tight in a giant flour tortilla.'),
    ('California', '8.50', 'Smoked turkey, cheddar cheese, bacon, lettuce, scallions, avocado and ranch dressing rolled up tight in a giant spinach tortilla.'),
    ('Roly Poly', '7.75', 'Smoked turkey, Monterey Jack cheese, bacon and honey mustard dressing rolled up tight & grilled golden brown in a giant flour tortilla.'),
    ('The Club', '7.75', 'Smoked turkey, ham, Swiss cheese, bacon, lettuce and mayonnaise rolled up tight in a giant flour tortilla.'),
    ('Pig Roast', '7.75', 'Smoked ham, Swiss cheese, onion, pineapple and dill horseradish sauce rolled up tight & grilled golden brown in a giant flour tortilla.'),
    ('The Cuban', '8.50', 'Roasted pork, smoked ham, Swiss cheese, dill pickles & yellow mustard rolled up tight & grilled golden brown in a giant tomato basil tortilla.'),
    ('The Big Pig', '8.50', 'Roasted pork, ham, bacon, Swiss and cheddar cheeses, tomato, onion and honey mustard dressing rolled up tight & grilled golden brown in a giant tomato basil tortilla.'),
    ('The Philly', '9.25', 'Shaved beef, green peppers, onion, Monterey Jack & our secret sauce all rolled up tight & grilled golden brown in a giant flour tortilla.'),
    ('Pepper Steak', '9.25', 'Shaved beef, cheddar cheese, onion, green pepper & horseradish sauce rolled up tight & grilled golden brown in a giant flour tortilla.'),
    ('The Ultimate Veggie', '7.75', 'Monterey Jack cheese, lettuce, tomatoes, green pepper, onion, cucumber, carrots, mushrooms, spinach & ranch dressing rolled up tight in a giant spinach tortilla.'),
]

BURGERS = [
    ('The Burger', '8.50', '1/3 lb. fresh Angus beef patty with ketchup, mayonnaise, mustard, pickle, onion, lettuce and tomato.'),
    ('Hickory Bacon Burger', '9.25', '1/3 lb. fresh Angus beef burger topped with bacon, cheddar & Jack cheeses, BBQ sauce; served with a pickle spear.'),
    ('Portobello & Swiss Burger', '9.25', '1/3 lb. fresh Angus beef burger topped with sautéed portobello mushrooms and Swiss cheese; with lettuce, tomato and mayonnaise on the side.'),
    ('Guacamole Bacon Burger', '9.25', '1/3 lb. fresh Angus beef burger topped with crispy bacon and homemade guacamole, drizzled with chipotle ranch dressing and served with lettuce, tomato.'),
    ('Frisco Burger', '9.25', '1/3 lb. fresh Angus beef burger on sourdough covered with sautéed onions, 1000 Island dressing & Swiss cheese.'),
    ('Turkey Bacon Swiss', '8.50', 'Grilled turkey, crispy bacon on a sub roll with lettuce, tomato and mayonnaise on the side.'),
    ('Blackened Grouper Po-Boy', '10.95', 'Blackened grouper, lettuce, tomato, onion and homemade tartar sauce on a hoagie roll.'),
    ('Chicken Salad Sandwich', '6.75', 'Our famous almond chicken salad on fresh Italian bread.'),
    ('The Bag Lunch', '7.25', 'Your choice of pimiento cheese, egg or tuna salad or PB&J sandwich served with chips, pickle, celery or carrot sticks and brownie.'),
]

SALADS = [
    ('Homemade Almond Chicken Salad with Fruit', '9.25', 'Chunky white meat with grapes, celery & almonds. Served with fresh fruit (drizzled w/ poppy seed dressing) and bread.'),
    ('Chefs Salad', '8.50', 'Romaine lettuce tossed with ham, turkey and Swiss cheese, garnished with tomato and egg. Served with a roll.'),
    ('Chicken Caesar Salad', '8.50', ''),
    ('Santé Fe Salad', '8.50', 'Warm grilled chicken spread over crisp lettuce, fresh veggies and cheese, topped with croutons and served with a roll.'),
    ('Big Green Salad', '7.25', 'Fresh veggies, raisins and cheese on a bed of lettuce; served with a roll.'),
    ('Taco Salad', '9.25', 'Spicy taco meat served over a tasty taco mixture, with sour cream and avocado.'),
]

DRESSINGS = ('Homemade dressings: Honey Mustard, Poppy Seed, Mustard Vinaigrette or Ranch. '
             'Or try: Chipotle Ranch, Blue Cheese, Thousand Island, Italian, Vidalia Onion '
             'Peppercorn, Caesar or Oil & Vinegar.')

QUICHE = {
    'varieties': 'Ham & Cheese · Bacon Tomato · Spinach & Swiss · Crazy',
    'items': [('Quiche Plate', '7.75', 'Served with fresh fruit and a mini-muffin.'),
              ('Quiche Slice', '3.50', '')],
}

SOUP = [
    ('Loaded Potato Soup', 'Bowl 6.75 · Cup 3.75'),
    ('White Chicken Chili', 'Bowl 7.50 · Cup 4.50'),
]

LITTLE_BAKERS = ('Little Bakers · $5 — choose one: Peanut Butter & Jelly, Grilled Cheese, or '
                 'Hot Dog. Served with chips; substitutions available.')

A_LA_CARTE = [
    ('Side of Fruit', '4.00'), ('Broccoli Salad', '4.00'), ('Pasta Salad', '4.00'),
    ('Side Salad', '4.00'), ('Loaded Potato', '4.75'), ('Side Chips', '2.00'),
]

DINNER = {
    'starters': [
        ('Spinach Artichoke Dip', '8', 'Fresh spinach with artichoke hearts & mozzarella cheeses. Served with tortilla chips, sour cream and salsa.'),
        ('Baby Portobellos', '7', 'Filled with sausage stuffing and served with tiger sauce.'),
        ('Grilled or Blackened Shrimp', '8', 'Six large, wild caught, Gulf shrimp served with cocktail sauce.'),
        ('Potato Skins', '7', 'With cheddar cheese, bacon, scallions and sour cream.'),
    ],
    'entree_note': ('Entrées served with your choice of baked potato, steamed veggies or rice. '
                    'All entrées served with side salad.'),
    'entrees': [
        ('6oz Filet', 'Market Price', 'Six ounces of Angus tenderloin.'),
        ('Bourbon Street Steak', 'Market Price', 'Slow roasted prime rib cut jazzed up with Cajun spice, garnished with sautéed onions, mushrooms & green peppers.'),
        ('Slow Roasted Prime Rib', 'Market Price', 'Sliced to order 10oz cut. Crusted with a house seasoning blend and a side of au jus.'),
        ('Beef Tips', '15', 'Marinated tenderloin served over wild rice, sautéed onions, mushrooms & green peppers. Side salad only.'),
        ('Honey Bacon Chicken', '13', 'Grilled chicken covered in our famous honey mustard & garnished with bacon, cheddar & Jack cheese, tomatoes & scallions.'),
        ('Smothered Chicken', '13', 'Grilled chicken topped with sautéed onions, mushrooms & green peppers smothered with Monterey Jack.'),
        ('Southwestern Chicken', '13', 'Blackened chicken covered in BBQ sauce, garnished with bacon, cheddar & Jack cheese, tomatoes & scallions.'),
        ('Seafood Pasta', '14', 'Wild caught Gulf shrimp & bay scallops, tossed with spaghetti in creamy garlic butter sauce. Side salad only.'),
        ('Folly Island Shrimp & Grits', '12', 'Delicious, creamy grits topped with large, wild caught, Gulf shrimp, garnished with scallions. Side salad only.'),
        ('Grilled or Blackened Shrimp', '16', 'Twelve large, wild caught, Gulf shrimp, grilled or blackened to your liking.'),
    ],
}

CASSEROLES = {
    'note': ('Our dinner casseroles are available to order by 2pm and pick up by 3pm daily. '
             '$15 each.'),
    'items': [
        ('Chicken Tetrazini', 'Bite-sized chicken in cream sauce with spaghetti, mushrooms, topped with mozzarella.'),
        ('Lasagna', 'Prepared from scratch using an old family recipe.'),
        ('Taco Casserole', 'Tortilla chip foundation with seasoned taco meat, tomatoes, green chilies, and cheddar cheese.'),
        ('King Ranch', 'Tortilla chip base featuring diced chicken, cream of chicken soup, tomatoes, green chilies, sour cream, and cheddar cheese.'),
        ('Chicken Florentine', 'Spinach, Swiss cheese, chicken, and sour cream.'),
        ('Shepherds Pie', 'Ground beef, onions, green beans, mashed potatoes, and cheddar cheese.'),
        ('Escalloped Potato with Chicken', 'Diced chicken layered with sliced potatoes in cream sauce, topped with cheddar cheese.'),
        ('Hamburger Casserole', 'Kid-friendly layered noodle dish topped with cheddar cheese.'),
        ('Chicken & Broccoli Casserole', 'Served over white rice.'),
        ('Whole Quiche', 'Ham & Cheese, Spinach & Swiss, Bacon & Tomato, or Crazy (bacon, spinach, onion, tomato, cheese).'),
    ],
}

CATERING = {
    'intro': ('We cater business events for breakfast, lunch and dinner. Please give us a day '
              'ahead to organize your order.'),
    'breakfast': [
        'Individual baked treats or custom variety platters',
        'Whole quiches — Ham & Cheese, Bacon & Tomato, Spinach & Swiss, or Crazy',
        'Quiche plates with fruit and mini-muffins',
        'Fresh fruit boxes — personal or large',
        'Orange juice and coffee service',
    ],
    'lunch_dinner': [
        'Casseroles, large salads and platters',
        'Italian bread and roll-up varieties',
        'Coke products, iced & hot tea, juice and lemonade',
        'Baked treats, cheesecake, key lime pie and cookie pie',
    ],
}
