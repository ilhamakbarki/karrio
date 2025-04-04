# Testing GoBolt API with Insomnia

This guide provides examples for testing the GoBolt API using Insomnia REST client.

## Authentication

GoBolt API uses API keys for authentication. You'll need:

-   `api_key`
-   `client_id`
-   `client_secret`
-   `account_number`

Add these as environment variables in Insomnia.

## Base URL

The base URL for GoBolt API is: `https://www.parcel.gobolt.com/v1`

## Create Shipment

### Request

-   **Method**: POST
-   **URL**: `https://www.parcel.gobolt.com/v1/shipments`
-   **Headers**:
    -   `Content-Type`: `application/json`
    -   `Authorization`: `Bearer [YOUR_API_KEY]`
    -   `Accept`: `application/json`

### Request Body

```json
{
    "shipper": {
        "name": "John Sender",
        "company": "Sender Company",
        "address_line1": "123 Sender St",
        "address_line2": "",
        "city": "San Francisco",
        "province": "CA",
        "postal_code": "94105",
        "country": "US",
        "phone": "555-123-4567",
        "email": "sender@example.com"
    },
    "recipient": {
        "name": "Jane Recipient",
        "company": "Recipient Company",
        "address_line1": "456 Recipient Ave",
        "address_line2": "",
        "city": "Los Angeles",
        "province": "CA",
        "postal_code": "90001",
        "country": "US",
        "phone": "555-987-6543",
        "email": "recipient@example.com"
    },
    "parcels": [
        {
            "weight": 10.0,
            "length": 12.0,
            "width": 10.0,
            "height": 8.0
        }
    ],
    "service_type": "STANDARD",
    "reference": "TEST-SHIPMENT-123"
}
```

### Expected Response

```json
{
    "id": "shp_123456789",
    "tracking_number": "GB123456789",
    "label_url": "https://api.gobolt.com/v1/labels/shp_123456789.pdf"
}
```

## Track Shipment

### Request

-   **Method**: GET
-   **URL**: `https://www.parcel.gobolt.com/v1/track`
-   **Headers**:
    -   `Content-Type`: `application/json`
    -   `Authorization`: `Bearer [YOUR_API_KEY]`
    -   `Accept`: `application/json`

### Request Body

```json
{
    "tracking_number": "GB123456789"
}
```

### Expected Response

```json
{
    "tracking_number": "GB123456789",
    "status": "in_transit",
    "events": [
        {
            "date": "2023-04-04T15:30:00Z",
            "description": "Package picked up",
            "location": "San Francisco, CA"
        },
        {
            "date": "2023-04-04T12:34:56Z",
            "description": "Shipment created",
            "location": "San Francisco, CA"
        }
    ]
}
```

## Get Rates

### Request

-   **Method**: POST
-   **URL**: `https://www.parcel.gobolt.com/v1/rate`
-   **Headers**:
    -   `Content-Type`: `application/json`
    -   `Authorization`: `Bearer [YOUR_API_KEY]`
    -   `Accept`: `application/json`

### Request Body (based on implementation)

```json
{
    "shipper": {
        "address_line1": "123 Main St",
        "address_line2": "",
        "city": "San Francisco",
        "province": "CA",
        "postal_code": "94105",
        "country": "US"
    },
    "recipient": {
        "address_line1": "456 Market St",
        "address_line2": "",
        "city": "Los Angeles",
        "province": "CA",
        "postal_code": "90001",
        "country": "US"
    },
    "parcels": [
        {
            "weight": 10.0,
            "length": 10.0,
            "width": 10.0,
            "height": 10.0
        }
    ],
    "service_type": "STANDARD"
}
```

### Expected Response

```json
{
    "rates": [
        {
            "service_code": "STANDARD",
            "service_name": "GoBolt Standard",
            "total": 25.99,
            "currency": "USD",
            "transit_days": 3,
            "estimated_delivery": "2023-04-07T12:00:00Z"
        },
        {
            "service_code": "EXPRESS",
            "service_name": "GoBolt Express",
            "total": 45.99,
            "currency": "USD",
            "transit_days": 1,
            "estimated_delivery": "2023-04-05T12:00:00Z"
        }
    ]
}
```

## Notes

-   This API structure is based on the implementation in the karrio codebase
-   You need to replace placeholder values with your actual API credentials
-   Make sure to check for any additional requirements or headers that may be needed
