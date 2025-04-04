#!/bin/bash
# Script to test GoBolt API directly from the command line

# Set your API credentials here
API_KEY="your_api_key"
CLIENT_ID="your_client_id"
CLIENT_SECRET="your_client_secret"
ACCOUNT_NUMBER="your_account_number"

# Base URL
BASE_URL="https://www.parcel.gobolt.com/v1"

# Headers
HEADERS=(
  -H "Content-Type: application/json"
  -H "Authorization: Bearer $API_KEY"
  -H "Accept: application/json"
)

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to create a shipment
create_shipment() {
  echo -e "${CYAN}Creating a shipment...${NC}"
  
  # Request body
  REQUEST_BODY=$(cat <<EOF
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
  "reference": "TEST-SHIPMENT-CLI-$(date +%s)"
}
EOF
)

  # Make the API call
  RESPONSE=$(curl -s "${HEADERS[@]}" -X POST "$BASE_URL/shipments" -d "$REQUEST_BODY")
  
  # Check if the response contains a tracking number
  if [[ "$RESPONSE" == *"tracking_number"* ]]; then
    echo -e "${GREEN}Shipment created successfully!${NC}"
    echo "$RESPONSE" | jq '.'
    
    # Extract the tracking number
    TRACKING_NUMBER=$(echo "$RESPONSE" | jq -r '.tracking_number')
    echo -e "${CYAN}Tracking number: $TRACKING_NUMBER${NC}"
    
    # Return the tracking number
    echo "$TRACKING_NUMBER"
  else
    echo -e "${RED}Failed to create shipment:${NC}"
    echo "$RESPONSE" | jq '.'
    return 1
  fi
}

# Function to track a shipment
track_shipment() {
  local tracking_number=$1
  
  echo -e "${CYAN}Tracking shipment with number: $tracking_number${NC}"
  
  # Request body
  REQUEST_BODY=$(cat <<EOF
{
  "tracking_number": "$tracking_number"
}
EOF
)

  # Make the API call
  RESPONSE=$(curl -s "${HEADERS[@]}" -X POST "$BASE_URL/track" -d "$REQUEST_BODY")
  
  # Check if the response contains tracking information
  if [[ "$RESPONSE" == *"tracking_number"* ]]; then
    echo -e "${GREEN}Tracking information retrieved:${NC}"
    echo "$RESPONSE" | jq '.'
  else
    echo -e "${RED}Failed to retrieve tracking information:${NC}"
    echo "$RESPONSE" | jq '.'
    return 1
  fi
}

# Function to get rates
get_rates() {
  echo -e "${CYAN}Getting rates...${NC}"
  
  # Request body
  REQUEST_BODY=$(cat <<EOF
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
EOF
)

  # Make the API call
  RESPONSE=$(curl -s "${HEADERS[@]}" -X POST "$BASE_URL/rate" -d "$REQUEST_BODY")
  
  # Check if the response contains rates
  if [[ "$RESPONSE" == *"rates"* ]]; then
    echo -e "${GREEN}Rates retrieved:${NC}"
    echo "$RESPONSE" | jq '.'
  else
    echo -e "${RED}Failed to retrieve rates:${NC}"
    echo "$RESPONSE" | jq '.'
    return 1
  fi
}

# Main function
main() {
  echo -e "${CYAN}=== GoBolt API Test Script ===${NC}"
  
  # Check if jq is installed
  if ! command -v jq &> /dev/null; then
    echo -e "${RED}Error: jq is required but not installed. Please install jq first.${NC}"
    exit 1
  fi
  
  # Display menu
  echo "1. Create a shipment"
  echo "2. Track a shipment"
  echo "3. Get rates"
  echo "4. Create and track shipment"
  echo "5. Exit"
  
  read -p "Enter your choice (1-5): " choice
  
  case $choice in
    1)
      create_shipment
      ;;
    2)
      read -p "Enter tracking number: " tracking_number
      track_shipment "$tracking_number"
      ;;
    3)
      get_rates
      ;;
    4)
      # Create a shipment and then track it
      echo -e "${CYAN}Creating and tracking a shipment...${NC}"
      tracking_number=$(create_shipment)
      
      if [[ -n "$tracking_number" ]]; then
        echo -e "${CYAN}Now tracking the shipment...${NC}"
        track_shipment "$tracking_number"
      fi
      ;;
    5)
      echo "Exiting..."
      exit 0
      ;;
    *)
      echo -e "${RED}Invalid choice. Please enter a number from 1 to 5.${NC}"
      ;;
  esac
}

# Run the main function
main 