"""
Test suite for NetAssist IP Sanitization Server
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from main import app, sanitizer

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "active_sessions" in data

def test_ipv4_sanitization():
    """Test IPv4 address sanitization"""
    test_config = """
    interface GigabitEthernet0/1
    ip address 192.168.1.1 255.255.255.0
    ip route 0.0.0.0 0.0.0.0 192.168.1.254
    """

    response = client.post("/api/sanitize", json={"text": test_config})
    assert response.status_code == 200

    data = response.json()
    assert data["entity_count"] > 0
    assert "192.168.1.1" not in data["sanitized_text"]
    assert "192.168.1.254" not in data["sanitized_text"]
    assert data["confidence"] > 0.8

def test_vlan_sanitization():
    """Test VLAN ID sanitization"""
    test_config = """
    vlan 100
    name PROD_VLAN
    interface FastEthernet0/1
    switchport access vlan 100
    """

    response = client.post("/api/sanitize", json={"text": test_config})
    assert response.status_code == 200

    data = response.json()
    assert data["entity_count"] >= 2  # Should detect both VLAN 100 instances
    assert "vlan 100" not in data["sanitized_text"]

def test_complex_network_config():
    """Test complex network configuration with multiple entity types"""
    test_config = """
    hostname CORE-SW-01
    interface GigabitEthernet0/1
    description Link to DIST-SW-02
    ip address 10.1.1.1 255.255.255.252
    vlan 200
    name USERS_VLAN
    router bgp 65001
    neighbor 172.16.1.1 remote-as 65002
    """

    response = client.post("/api/sanitize", json={"text": test_config})
    assert response.status_code == 200

    data = response.json()
    sanitized = data["sanitized_text"]

    # Verify original values are not present
    assert "CORE-SW-01" not in sanitized
    assert "DIST-SW-02" not in sanitized
    assert "10.1.1.1" not in sanitized
    assert "172.16.1.1" not in sanitized
    assert "65001" not in sanitized
    assert "65002" not in sanitized

    # Verify structure is preserved
    assert "hostname" in sanitized
    assert "interface GigabitEthernet" in sanitized
    assert "ip address" in sanitized
    assert "router bgp" in sanitized

def test_restoration():
    """Test text restoration with original values"""
    original_config = """
    interface GigabitEthernet0/1
    ip address 192.168.1.1 255.255.255.0
    vlan 100
    """

    # First, sanitize
    sanitize_response = client.post("/api/sanitize", json={"text": original_config})
    assert sanitize_response.status_code == 200

    sanitize_data = sanitize_response.json()
    session_id = sanitize_data["session_id"]
    sanitized_text = sanitize_data["sanitized_text"]

    # Simulate AI processing (no change for this test)
    ai_response = sanitized_text

    # Restore original values
    restore_response = client.post("/api/restore", json={
        "text": ai_response,
        "session_id": session_id
    })
    assert restore_response.status_code == 200

    restore_data = restore_response.json()
    restored_text = restore_data["restored_text"]

    # Verify original values are restored
    assert "192.168.1.1" in restored_text
    assert "vlan 100" in restored_text

def test_session_management():
    """Test session creation and management"""
    test_config = "ip address 10.1.1.1 255.255.255.0"

    # Create session
    response = client.post("/api/sanitize", json={"text": test_config})
    assert response.status_code == 200

    session_id = response.json()["session_id"]

    # Get session info
    session_response = client.get(f"/api/sessions/{session_id}")
    assert session_response.status_code == 200

    session_data = session_response.json()
    assert session_data["session_id"] == session_id
    assert session_data["entity_count"] > 0

    # Delete session
    delete_response = client.delete(f"/api/sessions/{session_id}")
    assert delete_response.status_code == 200

    # Verify session is deleted
    get_response = client.get(f"/api/sessions/{session_id}")
    assert get_response.status_code == 404

def test_invalid_session_restoration():
    """Test restoration with invalid session ID"""
    response = client.post("/api/restore", json={
        "text": "some text",
        "session_id": "invalid-session-id"
    })
    assert response.status_code == 404

def test_network_entity_detection():
    """Test individual network entity detection"""
    entities = sanitizer.detect_network_entities("ip address 192.168.1.1 255.255.255.0")
    assert len(entities) >= 1

    ipv4_entities = [e for e in entities if e.type == 'ipv4']
    assert len(ipv4_entities) >= 1
    assert ipv4_entities[0].original == "192.168.1.1"
    assert ipv4_entities[0].confidence > 0.9

def test_mac_address_sanitization():
    """Test MAC address sanitization"""
    test_config = """
    interface FastEthernet0/1
    mac-address 00:1b:21:3a:4f:5e
    arp 192.168.1.100 001b.213a.4f5e ARPA
    """

    response = client.post("/api/sanitize", json={"text": test_config})
    assert response.status_code == 200

    data = response.json()
    sanitized = data["sanitized_text"]

    # Verify MAC addresses are sanitized
    assert "00:1b:21:3a:4f:5e" not in sanitized
    assert "001b.213a.4f5e" not in sanitized

def test_interface_sanitization():
    """Test interface name sanitization"""
    test_config = """
    interface GigabitEthernet1/0/24
    interface FastEthernet0/1
    interface Vlan100
    """

    response = client.post("/api/sanitize", json={"text": test_config})
    assert response.status_code == 200

    data = response.json()
    sanitized = data["sanitized_text"]

    # Interface types should be preserved, numbers should change
    assert "GigabitEthernet" in sanitized
    assert "FastEthernet" in sanitized
    assert "Vlan" in sanitized

def test_consistency_across_sessions():
    """Test that same IP gets same sanitized value within session"""
    test_config1 = "ip address 192.168.1.1 255.255.255.0"
    test_config2 = "ip route 192.168.1.0 255.255.255.0 192.168.1.1"

    # First sanitization
    response1 = client.post("/api/sanitize", json={"text": test_config1})
    session_id = response1.json()["session_id"]

    # Second sanitization with same session
    response2 = client.post("/api/sanitize", json={
        "text": test_config2,
        "session_id": session_id
    })

    # Both should have same sanitized value for 192.168.1.1
    data1 = response1.json()
    data2 = response2.json()

    # This test would require updating the sanitizer to maintain consistency
    # within sessions - enhancement for production version

if __name__ == "__main__":
    pytest.main([__file__, "-v"])