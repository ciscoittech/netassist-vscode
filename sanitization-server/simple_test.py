#!/usr/bin/env python3
"""
Simple test of the sanitization logic without FastAPI dependencies
"""

import re
import ipaddress
from typing import List, Dict, Tuple

class NetworkEntity:
    def __init__(self, type: str, original: str, sanitized: str, confidence: float):
        self.type = type
        self.original = original
        self.sanitized = sanitized
        self.confidence = confidence

class SimpleNetworkSanitizer:
    """Simplified network entity detection and sanitization for testing"""

    def __init__(self):
        # Core network patterns
        self.patterns = {
            'ipv4': [
                r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b',
            ],
            'vlan': [
                r'\bvlan\s+(\d+)',
            ],
            'hostname': [
                r'\bhostname\s+([a-zA-Z0-9\-\.]+)',
                r'\b([A-Z][A-Z0-9\-]+-[A-Z0-9\-]+)\b',  # Match device names like CORE-SW-01, DIST-SW-02
            ]
        }

        self.fake_counters = {
            'ipv4': 1,
            'vlan': 100,
            'hostname': 1,
        }

    def detect_and_sanitize(self, text: str) -> Tuple[str, List[NetworkEntity]]:
        """Detect and sanitize network entities"""
        entities = []
        sanitized_text = text

        for entity_type, patterns in self.patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    original = match.group(0)

                    # Skip if already processed
                    if any(e.original == original for e in entities):
                        continue

                    # Generate sanitized version
                    sanitized = self._generate_sanitized_value(entity_type, original)
                    confidence = 0.95

                    entities.append(NetworkEntity(
                        type=entity_type,
                        original=original,
                        sanitized=sanitized,
                        confidence=confidence
                    ))

                    # Replace in text
                    sanitized_text = sanitized_text.replace(original, sanitized)

        return sanitized_text, entities

    def _generate_sanitized_value(self, entity_type: str, original: str) -> str:
        """Generate consistent sanitized replacement"""

        if entity_type == 'ipv4':
            return self._sanitize_ipv4(original)
        elif entity_type == 'vlan':
            vlan_id = self.fake_counters['vlan']
            self.fake_counters['vlan'] += 1
            vlan_match = re.search(r'\d+', original)
            if vlan_match:
                return original.replace(vlan_match.group(), str(vlan_id))
            return original
        elif entity_type == 'hostname':
            hostname_num = self.fake_counters['hostname']
            self.fake_counters['hostname'] += 1
            # Handle hostname command
            if original.startswith('hostname'):
                hostname_match = re.search(r'hostname\s+([a-zA-Z0-9\-\.]+)', original)
                if hostname_match:
                    return original.replace(hostname_match.group(1), f'device{hostname_num}')
            else:
                # Handle device names in descriptions
                return f'device{hostname_num}'

        return original  # Fallback

    def _sanitize_ipv4(self, ip_str: str) -> str:
        """Intelligently sanitize IPv4 addresses"""
        try:
            ip = ipaddress.IPv4Address(ip_str)

            if ip.is_private:
                if ip_str.startswith('192.168'):
                    octets = ip_str.split('.')
                    return f"10.255.{octets[2]}.{octets[3]}"
                elif ip_str.startswith('10.'):
                    octets = ip_str.split('.')
                    return f"172.31.{octets[2]}.{octets[3]}"
            else:
                # Public IP - use test range
                octets = ip_str.split('.')
                return f"203.0.113.{octets[3]}"

        except ipaddress.AddressValueError:
            pass

        # Fallback
        return ip_str.replace(ip_str.split('.')[0], '203')

def test_basic_sanitization():
    """Test basic IP and VLAN sanitization"""
    print("🧪 Testing Basic Sanitization")
    print("=" * 50)

    sanitizer = SimpleNetworkSanitizer()

    test_config = """
interface GigabitEthernet0/1
ip address 192.168.1.1 255.255.255.0
ip route 0.0.0.0 0.0.0.0 192.168.1.254
vlan 100
name PROD_VLAN
hostname CORE-SW-01
"""

    print("Original configuration:")
    print(test_config)

    sanitized_text, entities = sanitizer.detect_and_sanitize(test_config)

    print("Sanitized configuration:")
    print(sanitized_text)

    print(f"\n{len(entities)} entities detected and sanitized:")
    for entity in entities:
        print(f"  {entity.type}: {entity.original} → {entity.sanitized}")

    return len(entities) > 0

def test_complex_config():
    """Test complex network configuration"""
    print("\n🧪 Testing Complex Configuration")
    print("=" * 50)

    sanitizer = SimpleNetworkSanitizer()

    test_config = """
hostname DIST-SW-02
interface GigabitEthernet1/0/24
description Link to CORE-SW-01
ip address 10.1.1.2 255.255.255.252
interface FastEthernet0/1
switchport access vlan 200
vlan 200
name USERS_VLAN
"""

    print("Original configuration:")
    print(test_config)

    sanitized_text, entities = sanitizer.detect_and_sanitize(test_config)

    print("Sanitized configuration:")
    print(sanitized_text)

    print(f"\n{len(entities)} entities detected and sanitized:")
    for entity in entities:
        print(f"  {entity.type}: {entity.original} → {entity.sanitized}")

    # Verify no original values remain
    sensitive_values = ['DIST-SW-02', 'CORE-SW-01', '10.1.1.2', 'vlan 200']
    leaked_values = [val for val in sensitive_values if val in sanitized_text]

    if leaked_values:
        print(f"\n❌ SECURITY ISSUE: Original values found in sanitized text: {leaked_values}")
        return False
    else:
        print(f"\n✅ Security check passed: No original values leaked")
        return True

def test_restoration():
    """Test restoration process"""
    print("\n🧪 Testing Restoration Process")
    print("=" * 50)

    sanitizer = SimpleNetworkSanitizer()

    original = "ip address 192.168.1.1 255.255.255.0"
    print(f"Original: {original}")

    # Sanitize
    sanitized_text, entities = sanitizer.detect_and_sanitize(original)
    print(f"Sanitized: {sanitized_text}")

    # Create mapping for restoration
    mapping = {entity.sanitized: entity.original for entity in entities}
    print(f"Mapping: {mapping}")

    # Simulate AI response (no change for this test)
    ai_response = sanitized_text

    # Restore
    restored_text = ai_response
    for sanitized_val, original_val in mapping.items():
        restored_text = restored_text.replace(sanitized_val, original_val)

    print(f"Restored: {restored_text}")

    success = restored_text == original
    print(f"✅ Restoration {'successful' if success else 'failed'}")

    return success

def main():
    """Run all tests"""
    print("🔒 NetAssist IP Sanitization Tests")
    print("=" * 60)

    tests = [
        test_basic_sanitization,
        test_complex_config,
        test_restoration
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            results.append(False)

    # Summary
    passed = sum(results)
    total = len(results)

    print(f"\n🎯 Test Summary")
    print("=" * 30)
    print(f"Tests passed: {passed}/{total}")

    if passed == total:
        print("🎉 All tests passed! Sanitization system is working correctly.")
        print("✅ Ready for VS Code extension integration")
    else:
        print("⚠️  Some tests failed. Review implementation before deployment.")

    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)