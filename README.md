# Little Lemon API Documentation

## Introduction
The Little Lemon API allows developers to build web and mobile applications for the Little Lemon restaurant. The API enables users to browse, add, and edit menu items, place and manage orders, assign delivery crew to orders, and track order delivery status.

## Getting Started
Follow these instructions to get the Little Lemon API up and running:

1. Navigate to the project directory:
    ```sh
    cd LittleLemon
    ```

2. Activate the virtual environment:
    ```sh
    pipenv shell
    ```

3. Install the project dependencies:
    ```sh
    pipenv install
    ```

4. Create the initial database migrations:
    ```sh
    python manage.py makemigrations
    ```

5. Apply the migrations to the database:
    ```sh
    python manage.py migrate
    ```

6. Start the development server:
    ```sh
    python manage.py runserver
    ```
## User Roles
- **Customer**: Can browse menu items, manage their cart, and place orders.
- **Manager**: Can manage menu items, user groups, and view all orders.
- **Delivery Crew**: Can view and update orders assigned to them.

## Status Codes
| Status Code | Description                                      |
|-------------|--------------------------------------------------|
| 200 OK      | Successful GET, PUT, PATCH, and DELETE calls     |
| 201 Created | Successful POST requests                         |
| 401 Unauthorized | Failed authentication                       |
| 403 Forbidden | Failed authorization                           |
| 400 Bad Request | Validation failed for POST, PUT, PATCH, DELETE calls |
| 404 Not Found | Requested resource does not exist              |

## Endpoints

### User Registration and Authentication
| Endpoint               | Method | Role                        | Description                                        |
|------------------------|--------|-----------------------------|----------------------------------------------------|
| `/api/users`           | POST   | No role required            | Creates a new user with name, email, and password   |
| `/api/users/me/`       | GET    | Anyone with a valid user token | Retrieves details of the currently authenticated user |
| `/token/login/`        | POST   | Anyone with a valid username and password | Generates an access token using the user's credentials |

### Menu Items
| Endpoint                       | Method       | Role                        | Description                                        |
|--------------------------------|--------------|-----------------------------|----------------------------------------------------|
| `/api/menu-items`              | GET          | Customer, Delivery Crew, Manager | Retrieves a list of all menu items               |
| `/api/menu-items`              | POST         | Manager                     | Adds a new menu item                               |
| `/api/menu-items/{menuItem}`   | GET          | Customer, Delivery Crew, Manager | Retrieves details of a specific menu item       |
| `/api/menu-items/{menuItem}`   | PUT, PATCH   | Manager                     | Updates a specific menu item                       |
| `/api/menu-items/{menuItem}`   | DELETE       | Manager                     | Deletes a specific menu item                       |

### User Group Management
| Endpoint                               | Method | Role    | Description                                        |
|----------------------------------------|--------|---------|----------------------------------------------------|
| `/api/groups/manager/users`            | GET    | Manager | Retrieves a list of all managers                   |
| `/api/groups/manager/users`            | POST   | Manager | Assigns a user to the manager group                |
| `/api/groups/manager/users/{userId}`   | DELETE | Manager | Removes a user from the manager group              |
| `/api/groups/delivery-crew/users`      | GET    | Manager | Retrieves a list of all delivery crew members      |
| `/api/groups/delivery-crew/users`      | POST   | Manager | Assigns a user to the delivery crew group          |
| `/api/groups/delivery-crew/users/{userId}` | DELETE | Manager | Removes a user from the delivery crew group        |

### Cart Management
| Endpoint                  | Method | Role     | Description                                        |
|---------------------------|--------|----------|----------------------------------------------------|
| `/api/cart/menu-items`    | GET    | Customer | Retrieves current items in the user's cart         |
| `/api/cart/menu-items`    | POST   | Customer | Adds a menu item to the user's cart                |
| `/api/cart/menu-items`    | DELETE | Customer | Deletes all items from the user's cart             |

### Order Management
| Endpoint                  | Method       | Role          | Description                                        |
|---------------------------|--------------|---------------|----------------------------------------------------|
| `/api/orders`             | GET          | Customer      | Retrieves all orders placed by the user            |
| `/api/orders`             | POST         | Customer      | Creates a new order using items in the user's cart |
| `/api/orders/{orderId}`   | GET          | Customer      | Retrieves items for a specific order               |
| `/api/orders`             | GET          | Manager       | Retrieves all orders                               |
| `/api/orders/{orderId}`   | PUT, PATCH   | Manager       | Updates an order, assigns delivery crew, changes order status |
| `/api/orders/{orderId}`   | DELETE       | Manager       | Deletes a specific order                           |
| `/api/orders`             | GET          | Delivery Crew | Retrieves all orders assigned to the delivery crew |
| `/api/orders/{orderId}`   | PATCH        | Delivery Crew | Updates the status of an order to indicate delivery progress |

### Additional Features
- **Filtering, Pagination, and Sorting**: Implement these capabilities for `/api/menu-items` and `/api/orders` endpoints to enhance data retrieval.
- **Throttling**: Apply rate limiting for authenticated and unauthenticated users to prevent abuse of the API.

