"""
JWT Analyzer - Advanced JWT token analysis and vulnerability detection
"""

import jwt
import json
import base64
import hashlib
import hmac
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

class JWTAnalyzer:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.jwt_config = config_manager.get_jwt_config()
        self.weak_secrets = self.load_weak_secrets()
        
    def load_weak_secrets(self) -> List[str]:
        """Load weak secrets for JWT testing"""
        try:
            secrets_file = self.jwt_config.get('weak_secrets_file', 'wordlists/jwt_secrets.txt')
            with open(secrets_file, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            return self.get_default_weak_secrets()
    
    def get_default_weak_secrets(self) -> List[str]:
        """Get default weak secrets"""
        return [
            'secret', 'key', 'jwt', 'token', 'password', '123456', 'admin',
            'test', 'dev', 'your-256-bit-secret', 'mysecret', 'jwtsecret',
            'secretkey', 'mykey', 'defaultsecret', 'changeme', 'insecure',
            'weak', 'simple', 'easy', 'basic', 'common', 'default',
            'qwerty', 'letmein', 'welcome', 'hello', 'world'
        ]
    
    def analyze_token(self, token: str) -> Dict:
        """Comprehensive JWT token analysis"""
        analysis = {
            'token': token,
            'valid': False,
            'header': None,
            'payload': None,
            'signature_valid': False,
            'vulnerabilities': [],
            'recommendations': [],
            'decoded_successfully': False
        }
        
        try:
            # Decode header and payload without verification
            analysis['header'] = jwt.get_unverified_header(token)
            analysis['payload'] = jwt.decode(token, options={"verify_signature": False})
            analysis['decoded_successfully'] = True
            
            # Analyze header
            self._analyze_header(analysis)
            
            # Analyze payload
            self._analyze_payload(analysis)
            
            # Test for weak secrets
            weak_secret = self._test_weak_secrets(token, analysis['header'])
            if weak_secret:
                analysis['vulnerabilities'].append({
                    'type': 'Weak Secret',
                    'severity': 'Critical',
                    'description': f'JWT signed with weak secret: "{weak_secret}"',
                    'impact': 'Account takeover possible through JWT manipulation',
                    'secret': weak_secret
                })
            
            # Test for algorithm confusion
            self._test_algorithm_confusion(token, analysis)
            
            # Test for none algorithm
            self._test_none_algorithm(token, analysis)
            
        except jwt.DecodeError:
            analysis['vulnerabilities'].append({
                'type': 'Invalid Token',
                'severity': 'High',
                'description': 'JWT token is malformed or invalid',
                'impact': 'Token cannot be processed'
            })
        except Exception as e:
            analysis['vulnerabilities'].append({
                'type': 'Analysis Error',
                'severity': 'Medium',
                'description': f'Error analyzing token: {str(e)}',
                'impact': 'Unable to complete security analysis'
            })
        
        return analysis
    
    def _analyze_header(self, analysis: Dict):
        """Analyze JWT header for vulnerabilities"""
        header = analysis['header']
        
        # Check algorithm
        alg = header.get('alg', '').upper()
        
        if alg == 'NONE':
            analysis['vulnerabilities'].append({
                'type': 'None Algorithm',
                'severity': 'Critical',
                'description': 'JWT uses "none" algorithm - no signature verification',
                'impact': 'Token can be modified without detection'
            })
        
        if alg in ['HS256', 'HS384', 'HS512']:
            analysis['recommendations'].append(
                'Consider using RS256 instead of HMAC for better security'
            )
        
        # Check for key ID manipulation
        if 'kid' in header:
            analysis['recommendations'].append(
                'Validate key ID (kid) parameter to prevent key confusion attacks'
            )
        
        # Check for JWK URL
        if 'jku' in header:
            analysis['vulnerabilities'].append({
                'type': 'JWK URL Present',
                'severity': 'High',
                'description': 'JWT header contains JWK URL which can be manipulated',
                'impact': 'Attacker can specify their own key server'
            })
    
    def _analyze_payload(self, analysis: Dict):
        """Analyze JWT payload for vulnerabilities"""
        payload = analysis['payload']
        current_time = datetime.now(timezone.utc).timestamp()
        
        # Check expiration
        if 'exp' in payload:
            exp_time = payload['exp']
            if exp_time < current_time:
                analysis['vulnerabilities'].append({
                    'type': 'Expired Token',
                    'severity': 'Medium',
                    'description': 'JWT token has expired',
                    'impact': 'Token should not be accepted'
                })
        else:
            analysis['vulnerabilities'].append({
                'type': 'No Expiration',
                'severity': 'Medium',
                'description': 'JWT token has no expiration time',
                'impact': 'Token remains valid indefinitely'
            })
        
        # Check issued at
        if 'iat' in payload:
            iat_time = payload['iat']
            if iat_time > current_time:
                analysis['vulnerabilities'].append({
                    'type': 'Future Issued Time',
                    'severity': 'Medium',
                    'description': 'JWT issued time is in the future',
                    'impact': 'Token may be invalid or clock skew issue'
                })
        
        # Check not before
        if 'nbf' in payload:
            nbf_time = payload['nbf']
            if nbf_time > current_time:
                analysis['vulnerabilities'].append({
                    'type': 'Not Yet Valid',
                    'severity': 'Low',
                    'description': 'JWT is not yet valid (nbf claim)',
                    'impact': 'Token should not be accepted yet'
                })
        
        # Check for sensitive information
        sensitive_keys = ['password', 'secret', 'key', 'token', 'ssn', 'credit_card']
        for key in payload:
            if any(sensitive in key.lower() for sensitive in sensitive_keys):
                analysis['vulnerabilities'].append({
                    'type': 'Sensitive Data Exposure',
                    'severity': 'High',
                    'description': f'Sensitive information in payload: {key}',
                    'impact': 'Sensitive data exposed in JWT token'
                })
    
    def _test_weak_secrets(self, token: str, header: Dict) -> Optional[str]:
        """Test JWT against weak secrets"""
        alg = header.get('alg', 'HS256')
        
        # Only test HMAC algorithms
        if not alg.startswith('HS'):
            return None
        
        for secret in self.weak_secrets:
            try:
                jwt.decode(token, secret, algorithms=[alg])
                return secret
            except jwt.InvalidSignatureError:
                continue
            except Exception:
                continue
        
        return None
    
    def _test_algorithm_confusion(self, token: str, analysis: Dict):
        """Test for algorithm confusion attacks"""
        header = analysis['header']
        original_alg = header.get('alg', '')
        
        # Test RS256 to HS256 confusion
        if original_alg.startswith('RS'):
            try:
                # Try to decode as HMAC using common public keys
                public_keys = [
                    '-----BEGIN PUBLIC KEY-----',
                    'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA',
                    'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQ'
                ]
                
                for key in public_keys:
                    try:
                        jwt.decode(token, key, algorithms=['HS256'])
                        analysis['vulnerabilities'].append({
                            'type': 'Algorithm Confusion',
                            'severity': 'Critical',
                            'description': 'JWT vulnerable to RS256/HS256 algorithm confusion',
                            'impact': 'Attacker can forge tokens using public key as HMAC secret'
                        })
                        break
                    except:
                        continue
            except:
                pass
    
    def _test_none_algorithm(self, token: str, analysis: Dict):
        """Test for none algorithm vulnerability"""
        try:
            # Create token with none algorithm
            parts = token.split('.')
            if len(parts) == 3:
                # Modify header to use none algorithm
                header = json.loads(base64.urlsafe_b64decode(parts[0] + '=='))
                header['alg'] = 'none'
                
                new_header = base64.urlsafe_b64encode(
                    json.dumps(header).encode()
                ).decode().rstrip('=')
                
                # Create token without signature
                none_token = f"{new_header}.{parts[1]}."
                
                try:
                    jwt.decode(none_token, options={"verify_signature": False})
                    analysis['vulnerabilities'].append({
                        'type': 'None Algorithm Accepted',
                        'severity': 'Critical',
                        'description': 'Application may accept tokens with "none" algorithm',
                        'impact': 'Tokens can be forged without signature'
                    })
                except:
                    pass
        except:
            pass
    
    def generate_exploit_token(self, original_token: str, payload_modifications: Dict, secret: str = None) -> Optional[str]:
        """Generate exploit token with modified payload"""
        try:
            # Decode original token
            header = jwt.get_unverified_header(original_token)
            payload = jwt.decode(original_token, options={"verify_signature": False})
            
            # Apply modifications
            for key, value in payload_modifications.items():
                payload[key] = value
            
            # Generate new token
            if secret:
                return jwt.encode(payload, secret, algorithm=header.get('alg', 'HS256'))
            else:
                # Try with none algorithm
                header['alg'] = 'none'
                return jwt.encode(payload, '', algorithm='none')
                
        except Exception as e:
            print(f"Error generating exploit token: {e}")
            return None
    
    def brute_force_secret(self, token: str, wordlist: List[str] = None) -> Optional[str]:
        """Brute force JWT secret"""
        if wordlist is None:
            wordlist = self.weak_secrets
        
        try:
            header = jwt.get_unverified_header(token)
            alg = header.get('alg', 'HS256')
            
            if not alg.startswith('HS'):
                return None
            
            for secret in wordlist:
                try:
                    jwt.decode(token, secret, algorithms=[alg])
                    return secret
                except jwt.InvalidSignatureError:
                    continue
                except Exception:
                    continue
                    
        except Exception as e:
            print(f"Error brute forcing secret: {e}")
        
        return None
    
    def validate_token_structure(self, token: str) -> Dict:
        """Validate JWT token structure"""
        validation = {
            'valid_structure': False,
            'parts_count': 0,
            'header_valid': False,
            'payload_valid': False,
            'signature_present': False,
            'errors': []
        }
        
        try:
            parts = token.split('.')
            validation['parts_count'] = len(parts)
            
            if len(parts) != 3:
                validation['errors'].append(f"Invalid parts count: {len(parts)} (expected 3)")
                return validation
            
            # Validate header
            try:
                header_data = base64.urlsafe_b64decode(parts[0] + '==')
                json.loads(header_data)
                validation['header_valid'] = True
            except Exception as e:
                validation['errors'].append(f"Invalid header: {str(e)}")
            
            # Validate payload
            try:
                payload_data = base64.urlsafe_b64decode(parts[1] + '==')
                json.loads(payload_data)
                validation['payload_valid'] = True
            except Exception as e:
                validation['errors'].append(f"Invalid payload: {str(e)}")
            
            # Check signature presence
            validation['signature_present'] = len(parts[2]) > 0
            
            validation['valid_structure'] = (
                validation['header_valid'] and 
                validation['payload_valid'] and 
                len(parts) == 3
            )
            
        except Exception as e:
            validation['errors'].append(f"Structure validation error: {str(e)}")
        
        return validation