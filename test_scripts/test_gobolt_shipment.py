#!/usr/bin/env python
"""
Test script for GoBolt shipment creation.
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Get the absolute path of this script
script_path = Path(os.path.abspath(__file__))
# Add the root directory to the path
karrio_root = script_path.parent.parent
sys.path.append(str(karrio_root))

# Import directly from the local examples directory
from examples.gobolt.karrio.mappers.gobolt.settings import Settings
from examples.gobolt.karrio.providers.gobolt.ship import Ship
# Try to import from the core models
try:
    from karrio.core.models import ShipmentRequest, Address, Parcel, Weight
except ImportError:
    print("Could not import from karrio.core.models, trying the examples module...")
    # Fall back to importing from modules directory if needed
    try:
        from modules.sdk.karrio.core.models import ShipmentRequest, Address, Parcel, Weight
    except ImportError:
        print("Failed to import core models. Make sure the karrio package is installed.")
        sys.exit(1)


def test_gobolt_shipment():
    """Test creating a shipment with GoBolt."""
    # Create settings instance with API credentials
    settings = Settings(
        api_key="your_api_key",  # Replace with your actual API key
        client_id="your_client_id",  # Replace with your actual client ID
        client_secret="your_client_secret",  # Replace with your actual client secret
        account_number="your_account_number",  # Replace with your actual account number
    )
    
    # Create a shipment request
    request = ShipmentRequest(
        shipper=Address(
            person_name="John Sender",
            company_name="Sender Company",
            address_line1="123 Sender St",
            city="San Francisco",
            state_code="CA",
            postal_code="94105",
            country_code="US",
            phone_number="555-123-4567",
            email="sender@example.com"
        ),
        recipient=Address(
            person_name="Jane Recipient",
            company_name="Recipient Company",
            address_line1="456 Recipient Ave",
            city="Los Angeles",
            state_code="CA",
            postal_code="90001",
            country_code="US",
            phone_number="555-987-6543",
            email="recipient@example.com"
        ),
        parcels=[
            Parcel(
                weight=Weight(10.0, "LB"),
                length=12.0,
                width=10.0,
                height=8.0,
            )
        ],
        service="STANDARD",
        reference="TEST-SHIPMENT-123",
    )
    
    # Create a shipment
    ship_service = Ship(settings)
    shipment = ship_service.create(request)
    
    # Print the results
    if shipment:
        print("Shipment created successfully!")
        print(f"Tracking number: {shipment.tracking_number}")
        print(f"Shipment ID: {shipment.shipment_identifier}")
        print(f"Label URL: {shipment.label_url}")
    else:
        print("Failed to create shipment.")


if __name__ == "__main__":
    test_gobolt_shipment() 
