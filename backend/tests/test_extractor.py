import os
import sys
import unittest

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(TEST_DIR)
UMLREV_ROOT = os.path.dirname(BACKEND_DIR)
if UMLREV_ROOT not in sys.path:
    sys.path.insert(0, UMLREV_ROOT)

from backend.umlrev.pipeline.extractor import SymbolExtractor


class TestSymbolExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = SymbolExtractor()
        self.benchmark_path = os.path.join(UMLREV_ROOT, "examples", "tell_story")

    def test_extract_tell_story_classes(self):
        """Verifies that Tell Story benchmark discovers all 4 expected classes."""
        project = self.extractor.scan_directory(self.benchmark_path, "TellStoryTest")
        class_names = list(project.classes.keys())

        self.assertIn("Enemy", class_names)
        self.assertIn("Hero", class_names)
        self.assertIn("Princess", class_names)
        self.assertIn("Story", class_names)
        self.assertEqual(len(project.classes), 4)

    def test_extract_methods_and_relationships(self):
        """Verifies method symbols and structural relationships are correctly derived."""
        project = self.extractor.scan_directory(self.benchmark_path, "TellStoryTest")
        story_class = project.get_class("Story")
        self.assertIsNotNone(story_class)
        
        method_names = [m.name for m in story_class.methods]
        self.assertIn("start", method_names)
        self.assertIn("tell", method_names)
        self.assertGreater(len(project.relationships), 0)

    def test_extract_python_functional_module(self):
        """Verifies that Python files without explicit classes are extracted as functional modules."""
        py_code = """
def calculate_tax(amount: float) -> float:
    return amount * 0.18

def generate_invoice(user_id: str, total: float):
    print("Invoice generated")
"""
        symbols = self.extractor.extract_from_file("services/billing.py", py_code, ".py", default_pkg="services")
        self.assertEqual(len(symbols), 1)
        sym = symbols[0]
        self.assertEqual(sym.name, "Billing")
        method_names = [m.name for m in sym.methods]
        self.assertIn("calculate_tax", method_names)
        self.assertIn("generate_invoice", method_names)

    def test_extract_react_and_typescript(self):
        """Verifies that TSX / JSX React components and TS classes are extracted cleanly."""
        ts_code = """
import { useState } from 'react';
export class OrderController extends BaseController {
    public placeOrder(orderId: string): boolean {
        return true;
    }
}
export function OrderView(props) {
    return <div>Order</div>;
}
"""
        symbols = self.extractor.extract_from_file("components/OrderView.tsx", ts_code, ".tsx", default_pkg="components")
        self.assertGreaterEqual(len(symbols), 1)
        class_names = [s.name for s in symbols]
        self.assertIn("OrderController", class_names)

    def test_extract_csharp_and_go(self):
        """Verifies C# class and Go struct extraction."""
        cs_code = """
namespace Banking.Core {
    public class AccountManager : IAccountService {
        public decimal GetBalance(int accountId) {
            return 1000m;
        }
    }
}
"""
        cs_symbols = self.extractor.extract_from_file("AccountManager.cs", cs_code, ".cs")
        self.assertEqual(len(cs_symbols), 1)
        self.assertEqual(cs_symbols[0].name, "AccountManager")
        self.assertIn("IAccountService", cs_symbols[0].interfaces)

        go_code = """
package auth
type SessionManager struct {
    Token string
}
func (s *SessionManager) ValidateToken(t string) bool {
    return true
}
"""
        go_symbols = self.extractor.extract_from_file("session.go", go_code, ".go")
        self.assertEqual(len(go_symbols), 1)
        self.assertEqual(go_symbols[0].name, "SessionManager")


if __name__ == "__main__":
    unittest.main()
