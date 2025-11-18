#!/bin/bash

# PhD Application Automation System - Test Script
# Run all tests

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  PhD Application Automation System - Running Tests           ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if running from project root
if [ ! -d "backend" ]; then
    echo -e "${RED}✗ Error: Please run this script from the project root directory${NC}"
    exit 1
fi

echo -e "${YELLOW}Running backend tests...${NC}"
cd backend

if [ ! -d "venv" ]; then
    echo -e "${RED}✗ Virtual environment not found. Please run: ./scripts/setup.sh${NC}"
    exit 1
fi

source venv/bin/activate

# Run pytest
pytest tests/ -v --tb=short

TEST_EXIT_CODE=$?

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
else
    echo -e "${RED}✗ Some tests failed${NC}"
fi

cd ..

exit $TEST_EXIT_CODE
