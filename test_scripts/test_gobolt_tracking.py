#!/usr/bin/env python
"""
Test script for tracking a GoBolt shipment.
"""

import sys
import os
from pathlib import Path

# Get the absolute path of this script
script_path = Path(os.path.abspath(__file__))
# Add the root directory to the path
karrio_root = script_path.parent.parent
sys.path.append(str(karrio_root))

# Import directly from the local examples directory
from examples.gobolt.karrio.mappers.gobolt.settings import Settings
from examples.gobolt.karrio.providers.gobolt.track import Track
# Try to import from the core models
try:
    from karrio.core.models import TrackingRequest
except ImportError:
    print("Could not import from karrio.core.models, trying the examples module...")
    # Fall back to importing from modules directory if needed
    try:
        from modules.sdk.karrio.core.models import TrackingRequest
    except ImportError:
        print("Failed to import core models. Make sure the karrio package is installed.")
        sys.exit(1)


def track_gobolt_shipment(tracking_number):
    """Track a shipment with GoBolt."""
    # Create settings instance with API credentials
    settings = Settings(
        api_key="your_api_key",  # Replace with your actual API key
        client_id="your_client_id",  # Replace with your actual client ID
        client_secret="your_client_secret",  # Replace with your actual client secret
        account_number="your_account_number",  # Replace with your actual account number
    )
    
    # Create a tracking request
    request = TrackingRequest(
        tracking_number=tracking_number,
    )
    
    # Track the shipment
    track_service = Track(settings)
    tracking_details, messages = track_service.create(request)
    
    # Print the results
    if tracking_details:
        print("Tracking information retrieved successfully!")
        
        for detail in tracking_details:
            print(f"Tracking number: {detail.tracking_number}")
            print(f"Status: {detail.status}")
            print(f"Updated at: {detail.updated_at}")
            
            if detail.events:
                print("\nShipment events:")
                for event in detail.events:
                    print(f"  {event.date}: {event.description} at {event.location}")
    else:
        print("Failed to retrieve tracking information.")
        
        if messages:
            print("Error messages:")
            for message in messages:
                print(f"  {message.code}: {message.message}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_gobolt_tracking.py <tracking_number>")
        sys.exit(1)
    
    tracking_number = sys.argv[1]
    track_gobolt_shipment(tracking_number) 
