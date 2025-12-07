#!/bin/bash

# Pre-Deployment Testing Script
# Run this before deploying to catch issues early

echo "🧪 MMU Bicycle Rental - Pre-Deployment Testing"
echo "=============================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
passed=0
failed=0

# Function to run test
run_test() {
    test_name=$1
    command=$2
    
    echo -n "Testing: $test_name... "
    
    if eval $command > /dev/null 2>&1; then
        echo -e "${GREEN}✅ PASS${NC}"
        ((passed++))
        return 0
    else
        echo -e "${RED}❌ FAIL${NC}"
        ((failed++))
        return 1
    fi
}

# Test 1: Python version
run_test "Python version (3.10+)" "python3 --version | grep -E 'Python 3\.(1[0-9]|[2-9][0-9])'"

# Test 2: Dependencies
run_test "Dependencies installed" "pip list | grep Django"

# Test 3: Build script executable
if [ -x build.sh ]; then
    echo -e "Testing: build.sh executable... ${GREEN}✅ PASS${NC}"
    ((passed++))
else
    echo -e "Testing: build.sh executable... ${RED}❌ FAIL${NC}"
    ((failed++))
fi

# Test 4: .gitignore exists
run_test ".gitignore exists" "test -f .gitignore"

# Test 5: .env.example exists
run_test ".env.example exists" "test -f .env.example"

# Test 6: Git repository
run_test "Git repository initialized" "test -d .git"

# Test 7: Migrations
echo -n "Testing: Creating migrations... "
if python3 manage.py makemigrations --dry-run > /dev/null 2>&1; then
    echo -e "${GREEN}✅ PASS${NC}"
    ((passed++))
else
    echo -e "${YELLOW}⚠️  WARN (may need to create)${NC}"
fi

# Test 8: Check for missing migrations
echo -n "Testing: Migrations up to date... "
if python3 manage.py showmigrations | grep -q '\[ \]'; then
    echo -e "${YELLOW}⚠️  WARN (unapplied migrations)${NC}"
else
    echo -e "${GREEN}✅ PASS${NC}"
    ((passed++))
fi

# Test 9: Static files
echo -n "Testing: Static files collection... "
if python3 manage.py collectstatic --noinput --dry-run > /dev/null 2>&1; then
    echo -e "${GREEN}✅ PASS${NC}"
    ((passed++))
else
    echo -e "${RED}❌ FAIL${NC}"
    ((failed++))
fi

# Test 10: Check syntax
echo -n "Testing: Python syntax... "
if python3 -m py_compile manage.py config/*.py 2> /dev/null; then
    echo -e "${GREEN}✅ PASS${NC}"
    ((passed++))
else
    echo -e "${RED}❌ FAIL${NC}"
    ((failed++))
fi

# Test 11: Settings module
echo -n "Testing: Production settings... "
if python3 -c "import os; os.environ['DJANGO_SETTINGS_MODULE']='config.settings.production'; import django; django.setup()" 2> /dev/null; then
    echo -e "${GREEN}✅ PASS${NC}"
    ((passed++))
else
    echo -e "${RED}❌ FAIL${NC}"
    ((failed++))
fi

# Test 12: Required files
files=("requirements.txt" "manage.py" "build.sh" "config/wsgi.py")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "Testing: $file exists... ${GREEN}✅ PASS${NC}"
        ((passed++))
    else
        echo -e "Testing: $file exists... ${RED}❌ FAIL${NC}"
        ((failed++))
    fi
done

# Summary
echo ""
echo "=============================================="
echo "Test Summary:"
echo -e "  ${GREEN}Passed: $passed${NC}"
echo -e "  ${RED}Failed: $failed${NC}"
echo "=============================================="

if [ $failed -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed! Ready to deploy!${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. ./deploy_to_render.sh"
    echo "  2. Push to GitHub"
    echo "  3. Deploy on Render"
    exit 0
else
    echo -e "${RED}⚠️  Some tests failed. Fix issues before deploying.${NC}"
    echo ""
    echo "Common fixes:"
    echo "  - chmod +x build.sh"
    echo "  - pip install -r requirements.txt"
    echo "  - python manage.py makemigrations"
    exit 1
fi