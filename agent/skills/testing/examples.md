# Testing examples

Read the relevant example only when a concrete pytest or Jest pattern is needed and the repository's existing tests do not provide one. These examples support [the testing skill](SKILL.md); they are not a required checklist.

Commands are illustrative, not authorization to run tests or collect coverage. Follow the testing skill's workflow and the global execution policy.

Preserved from the testing skill. License: MIT. Attribution: awesome-ai-agent-skills contributors.

### Example 1 — Python with pytest

Given this source file `src/cart.py`:

```python
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, name: str, price: float, quantity: int = 1):
        if price < 0:
            raise ValueError("Price cannot be negative")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1")
        self.items.append({"name": name, "price": price, "quantity": quantity})

    def total(self) -> float:
        return sum(item["price"] * item["quantity"] for item in self.items)

    def remove_item(self, name: str):
        self.items = [item for item in self.items if item["name"] != name]
```

The agent generates `tests/test_cart.py`:

```python
import pytest
from src.cart import ShoppingCart

@pytest.fixture
def cart():
    return ShoppingCart()

def test_add_item_and_total(cart):
    cart.add_item("Widget", 9.99, 2)
    assert cart.total() == pytest.approx(19.98)

def test_empty_cart_total_is_zero(cart):
    assert cart.total() == 0.0

def test_add_item_negative_price_raises(cart):
    with pytest.raises(ValueError, match="Price cannot be negative"):
        cart.add_item("Bad", -1.0)

def test_add_item_zero_quantity_raises(cart):
    with pytest.raises(ValueError, match="Quantity must be at least 1"):
        cart.add_item("Bad", 5.0, 0)

def test_remove_item(cart):
    cart.add_item("A", 1.0)
    cart.add_item("B", 2.0)
    cart.remove_item("A")
    assert cart.total() == 2.0

def test_remove_nonexistent_item_does_nothing(cart):
    cart.add_item("A", 1.0)
    cart.remove_item("Z")
    assert cart.total() == 1.0
```

Run: `pytest tests/test_cart.py --cov=src -v`

### Example 2 — JavaScript with Jest

Given this source file `src/validator.js`:

```javascript
function isValidEmail(email) {
  if (typeof email !== "string") return false;
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
}

function isStrongPassword(password) {
  if (typeof password !== "string") return false;
  return (
    password.length >= 8 &&
    /[A-Z]/.test(password) &&
    /[a-z]/.test(password) &&
    /[0-9]/.test(password)
  );
}

module.exports = { isValidEmail, isStrongPassword };
```

The agent generates `src/__tests__/validator.test.js`:

```javascript
const { isValidEmail, isStrongPassword } = require("../validator");

describe("isValidEmail", () => {
  test.each([
    ["user@example.com", true],
    ["name+tag@sub.domain.org", true],
    ["missing-at-sign.com", false],
    ["@no-local.com", false],
    ["spaces in@email.com", false],
    ["", false],
  ])("isValidEmail(%s) => %s", (input, expected) => {
    expect(isValidEmail(input)).toBe(expected);
  });

  test("returns false for non-string input", () => {
    expect(isValidEmail(null)).toBe(false);
    expect(isValidEmail(42)).toBe(false);
  });
});

describe("isStrongPassword", () => {
  test("accepts a strong password", () => {
    expect(isStrongPassword("Str0ngPwd")).toBe(true);
  });

  test("rejects short password", () => {
    expect(isStrongPassword("Ab1")).toBe(false);
  });

  test("rejects password without uppercase", () => {
    expect(isStrongPassword("alllower1")).toBe(false);
  });

  test("rejects non-string input", () => {
    expect(isStrongPassword(undefined)).toBe(false);
  });
});
```

Run: `npx jest --coverage --verbose`
