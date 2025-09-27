"""
NetAssist IP Sanitization Server
Secure FastAPI server for sanitizing network configurations before AI processing
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Tuple
import uuid
import re
import hashlib
import json
from datetime import datetime, timedelta
import ipaddress
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models
class SanitizationRequest(BaseModel):
    text: str
    session_id: Optional[str] = None

class SanitizationResponse(BaseModel):
    sanitized_text: str
    session_id: str
    entity_count: int
    confidence: float
    mapping_id: str

class RestorationRequest(BaseModel):
    text: str
    session_id: str

class RestorationResponse(BaseModel):
    restored_text: str
    entity_count: int
    success: bool

class NetworkEntity(BaseModel):
    type: str  # 'ipv4', 'ipv6', 'vlan', 'asn', 'hostname'
    original: str
    sanitized: str
    confidence: float

# Global session storage (in production, use Redis or database)
sessions: Dict[str, Dict] = {}

app = FastAPI(
    title="NetAssist IP Sanitization Server",
    description="Secure network configuration sanitization for AI processing",
    version="1.0.0"
)

# CORS middleware for VS Code extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to VS Code extension
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NetworkSanitizer:
    """Advanced network entity detection and sanitization"""

    def __init__(self):
        # Comprehensive network patterns
        self.patterns = {
            'ipv4': [
                r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b',
                r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\/(?:3[0-2]|[12]?[0-9])\b',  # CIDR
            ],
            'ipv6': [
                r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b',
                r'\b(?:[0-9a-fA-F]{1,4}:){1,7}:\b',
                r'\b::(?:[0-9a-fA-F]{1,4}:){0,6}[0-9a-fA-F]{1,4}\b',
            ],
            'vlan': [
                r'\bvlan\s+(\d+)\b',
                r'\bvlan(\d+)\b',
                r'\b(?:access|trunk)\s+vlan\s+(\d+)\b',
            ],
            'asn': [
                r'\bas(?:-number)?\s+(\d+)\b',
                r'\basn\s+(\d+)\b',
                r'\bbgp\s+(\d+)\b',
            ],
            'hostname': [
                r'\bhostname\s+([a-zA-Z0-9\-\.]+)\b',
                r'\bdevice\s+([a-zA-Z0-9\-\.]+)\b',
            ],
            'interface': [
                r'\binterface\s+((?:GigabitEthernet|FastEthernet|Ethernet|Serial|Loopback|Vlan)\d+(?:\/\d+)*)\b',
                r'\bint\s+((?:Gi|Fa|Eth|Se|Lo|Vl)\d+(?:\/\d+)*)\b',
            ],
            'mac': [
                r'\b(?:[0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}\b',
                r'\b(?:[0-9a-fA-F]{4}\.){2}[0-9a-fA-F]{4}\b',
            ]
        }

        # Fake IP ranges for consistent replacement
        self.fake_ip_ranges = {
            'private_a': '10.255.',      # Replace 192.168.x.x
            'private_b': '172.31.',      # Replace 10.x.x.x
            'private_c': '192.0.2.',     # Replace 172.16-31.x.x (RFC 5737 test range)
            'public': '203.0.113.',      # RFC 5737 test range for public IPs
        }

        self.fake_counters = {
            'ipv4': 1,
            'vlan': 100,
            'asn': 65000,
            'hostname': 1,
            'interface': 1,
            'mac': 1
        }

    def detect_network_entities(self, text: str) -> List[NetworkEntity]:
        """Detect all network entities in text"""
        entities = []

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
                    confidence = self._calculate_confidence(entity_type, original)

                    entities.append(NetworkEntity(
                        type=entity_type,
                        original=original,
                        sanitized=sanitized,
                        confidence=confidence
                    ))

        return entities

    def _generate_sanitized_value(self, entity_type: str, original: str) -> str:
        """Generate consistent sanitized replacement"""

        if entity_type == 'ipv4':
            return self._sanitize_ipv4(original)
        elif entity_type == 'vlan':
            vlan_id = self.fake_counters['vlan']
            self.fake_counters['vlan'] += 1
            return original.replace(re.search(r'\d+', original).group(), str(vlan_id))
        elif entity_type == 'asn':
            asn = self.fake_counters['asn']
            self.fake_counters['asn'] += 1
            return original.replace(re.search(r'\d+', original).group(), str(asn))
        elif entity_type == 'hostname':
            hostname_num = self.fake_counters['hostname']
            self.fake_counters['hostname'] += 1
            return original.replace(re.search(r'[a-zA-Z0-9\-\.]+', original).group(), f'device{hostname_num}')
        elif entity_type == 'interface':
            int_num = self.fake_counters['interface']
            self.fake_counters['interface'] += 1
            # Keep interface type, change number
            int_match = re.search(r'(\w+)(\d+(?:\/\d+)*)', original)
            if int_match:
                return original.replace(int_match.group(2), f'{int_num}')
        elif entity_type == 'mac':
            mac_num = self.fake_counters['mac']
            self.fake_counters['mac'] += 1
            return f'00:11:22:33:44:{mac_num:02x}'

        return original  # Fallback

    def _sanitize_ipv4(self, ip_str: str) -> str:
        """Intelligently sanitize IPv4 addresses based on type"""
        try:
            # Handle CIDR notation
            if '/' in ip_str:
                ip_part, prefix = ip_str.split('/')
                sanitized_ip = self._sanitize_ipv4(ip_part)
                return f"{sanitized_ip}/{prefix}"

            ip = ipaddress.IPv4Address(ip_str)

            # Determine IP type and apply appropriate fake range
            if ip.is_private:
                if ip_str.startswith('192.168'):
                    octets = ip_str.split('.')
                    return f"{self.fake_ip_ranges['private_a']}{octets[2]}.{octets[3]}"
                elif ip_str.startswith('10.'):
                    octets = ip_str.split('.')
                    return f"{self.fake_ip_ranges['private_b']}{octets[1]}.{octets[2]}.{octets[3]}"
                elif ip_str.startswith('172.'):
                    octets = ip_str.split('.')
                    return f"{self.fake_ip_ranges['private_c']}{octets[2]}.{octets[3]}"
            else:
                # Public IP - use test range
                octets = ip_str.split('.')
                return f"{self.fake_ip_ranges['public']}{octets[3]}"

        except ipaddress.AddressValueError:
            pass

        # Fallback for malformed IPs
        return ip_str.replace(ip_str.split('.')[0], '203')

    def _calculate_confidence(self, entity_type: str, original: str) -> float:
        """Calculate confidence score for detection"""
        confidence_map = {
            'ipv4': 0.95,
            'ipv6': 0.90,
            'vlan': 0.85,
            'asn': 0.80,
            'hostname': 0.75,
            'interface': 0.90,
            'mac': 0.95
        }
        return confidence_map.get(entity_type, 0.50)

# Global sanitizer instance
sanitizer = NetworkSanitizer()

@app.post("/api/sanitize", response_model=SanitizationResponse)
async def sanitize_text(request: SanitizationRequest):
    """Sanitize network configuration text"""
    try:
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())

        # Detect network entities
        entities = sanitizer.detect_network_entities(request.text)

        # Apply sanitization
        sanitized_text = request.text
        entity_mapping = {}

        for entity in entities:
            sanitized_text = sanitized_text.replace(entity.original, entity.sanitized)
            entity_mapping[entity.original] = {
                'sanitized': entity.sanitized,
                'type': entity.type,
                'confidence': entity.confidence
            }

        # Store mapping in session
        sessions[session_id] = {
            'mapping': entity_mapping,
            'created_at': datetime.now(),
            'expires_at': datetime.now() + timedelta(hours=24)
        }

        # Calculate overall confidence
        avg_confidence = sum(e.confidence for e in entities) / len(entities) if entities else 1.0

        mapping_id = hashlib.md5(f"{session_id}-{datetime.now()}".encode()).hexdigest()[:16]

        logger.info(f"Sanitized {len(entities)} entities for session {session_id}")

        return SanitizationResponse(
            sanitized_text=sanitized_text,
            session_id=session_id,
            entity_count=len(entities),
            confidence=avg_confidence,
            mapping_id=mapping_id
        )

    except Exception as e:
        logger.error(f"Sanitization error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Sanitization failed: {str(e)}")

@app.post("/api/restore", response_model=RestorationResponse)
async def restore_text(request: RestorationRequest):
    """Restore original values from sanitized text"""
    try:
        if request.session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found or expired")

        session_data = sessions[request.session_id]

        # Check if session expired
        if datetime.now() > session_data['expires_at']:
            del sessions[request.session_id]
            raise HTTPException(status_code=410, detail="Session expired")

        # Restore original values
        restored_text = request.text
        entity_count = 0

        for original, mapping_data in session_data['mapping'].items():
            sanitized = mapping_data['sanitized']
            if sanitized in restored_text:
                restored_text = restored_text.replace(sanitized, original)
                entity_count += 1

        logger.info(f"Restored {entity_count} entities for session {request.session_id}")

        return RestorationResponse(
            restored_text=restored_text,
            entity_count=entity_count,
            success=True
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Restoration error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Restoration failed: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_sessions": len(sessions),
        "version": "1.0.0"
    }

@app.get("/api/sessions/{session_id}")
async def get_session_info(session_id: str):
    """Get session information (for debugging)"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session_data = sessions[session_id]
    return {
        "session_id": session_id,
        "entity_count": len(session_data['mapping']),
        "created_at": session_data['created_at'].isoformat(),
        "expires_at": session_data['expires_at'].isoformat(),
        "is_expired": datetime.now() > session_data['expires_at']
    }

@app.delete("/api/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete session and clear mappings"""
    if session_id in sessions:
        del sessions[session_id]
        logger.info(f"Deleted session {session_id}")
        return {"message": "Session deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Session not found")

@app.on_event("startup")
async def startup_event():
    """Startup event"""
    logger.info("Starting NetAssist Sanitization Server")

@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event"""
    logger.info("Shutting down NetAssist Sanitization Server")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")