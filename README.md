# Vendor Management System

The Vendor Management System is a web application built with Django that allows users to manage vendors, their contact details, and performance metrics.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [API Documentation](#api-documentation)
  - [Authentication](#authentication)
  - [Endpoints](#endpoints)
- [Contributing](#contributing)
- [License](#license)

## Features

- :pencil: CRUD operations for vendors
- :chart_with_upwards_trend: Performance metrics calculation
- :lock: Authentication with token-based authentication
- :gear: API endpoints for integration with other systems

## Installation

1. Clone the repository:

    ```bash
    git clone <repository-url>
    ```

2. Navigate to the project directory:

    ```bash
    cd vms
    ```

3. Install dependencies using pipenv:

    ```bash
    pipenv install
    ```

4. Activate the virtual environment:

    ```bash
    pipenv shell
    ```

5. Apply migrations:

    ```bash
    python manage.py migrate
    ```

6. Run the development server:

    ```bash
    python manage.py runserver
    ```
7. Run the tests:

    ```bash
    python manage.py test
    ```

The application will be accessible at `http://localhost:8000`.

## Usage

### API Documentation
API documentation is available at 
- Redoc - `/api/docs/`
- Swagger - `/api/docs/swagger/`

endpoints when the server is running. You can explore and test the API endpoints using Swagger UI.

### Authentication

The API endpoints require authentication using a token. To obtain a token, send a POST request to `/api/token/` with your username and password in the request body. You will receive a token in the response, which you can use to authenticate subsequent requests by including it in the Authorization header as `Bearer <token>`.

### Endpoints
#### General API endpoints available are:
- **POST /api/token/**: Obtain a token for authentication.

#### Vendor Management System specific API endpoints available are:
##### API endpoints for vendors:
- **GET /api/vendors/**: Retrieve a list of all vendors.
- **GET /api/vendors/{id}/**: Retrieve details of a specific vendor.
- **POST /api/vendors/**: Create a new vendor.
- **PUT /api/vendors/{id}/**: Update details of a specific vendor.
- **PATCH /api/vendors/{id}/**: Update status of a specific vendor.
- **DELETE /api/vendors/{id}/**: Delete a specific vendor.
- **GET /api/vendors/{id}/performance/**: Retrieve performance metrics of a specific vendor.
##### API endpoints for purchase orders:
- **GET /api/purchase_orders/**: Retrieve a list of all purchase orders.
- **GET /api/purchase_orders/{id}/**: Retrieve details of a specific purchase order.
- **POST /api/purchase_orders/**: Create a new purchase order.
- **PUT /api/purchase_orders/{id}/**: Update details of a specific purchase order.
- **PATCH /api/purchase_orders/{id}/**: Update status of a specific purchase order.
- **DELETE /api/purchase_orders/{id}/**: Delete a specific purchase order.

## Contributing

Contributions are welcome! Feel free to open issues or pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
